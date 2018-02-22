#!/usr/bin/env python3

"""

Print out targets with matching roles:

tfu [-f ./pillar/top.sls] targets <ROLE1 ROLE2 ... ROLEN>

Print out nodes with matching roles:

tfu [-f ./pillar/top.sls] nodes [-o (pretty|txt|json|yaml)] <NODELIST> <ROLE1 ROLE2 ... ROLEN>


Example:

./tu.py targets elasticsearch.master elasticsearch.data
./tu.py nodes nodes-up.yaml elasticsearch.master elasticsearch.data

"""

import re
import json
from pathlib import Path

import yaml
import click


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class Topfile(object):
    def __init__(self, path='./top.sls'):
        # print(path.name)
        self.path = Path(path.name)
        self.text = path.read()
        # stores whole pillar in yaml, everything is under `base` though
        self.yaml = yaml.load(self.text, Loader=Loader)

    def __repr__(self):
        return "Topfile: " + str(self.path)

    @property
    def data(self):
        return self.yaml['base']

    def targets(self, roles=None):
        """Returns the dictionary of targets that match role.

            {
                'role1': ['target1a', 'target1b'],
                'role2': ['target2']
            }
        """
        results = {}
        if roles:
            for role in roles:
                # print(f"role: {role}")
                for target in self.data.keys():
                    # print(f"\t{target}")
                    # print(f"\t\t{self.data[target]}")
                    if role in self.data[target]:
                        if role in results:
                            results[role].append(target)
                        else:
                            results[role] = [target]
        else:
            results['*'] = list(self.data.keys())
        return results


@click.group()
@click.option('--topfile', '-t', default='./top.sls', type=click.File('r'), help="Path to topfile")
@click.pass_context
def cli(ctx, topfile):
    ctx.obj = Topfile(topfile)


@cli.command(help="Print salt targets that match roles.")
@click.argument('roles', nargs=-1)
@click.pass_obj
def targets(topfile, roles):
    target_dict = topfile.targets(roles)
    if target_dict:
        for role in target_dict.keys():
            print(role)
            for target in target_dict[role]:
                print("\t%s" % target)
    else:
        print('No roles found to match:\n\t' + ', '.join(roles))


# TODO: Things below could be refactored into a Nodes class
NODE_OUTPUT_TYPES = ["pretty", "txt", "json", "yaml"]


@cli.command(help="Print nodes that match roles.")
@click.argument('nodelist', nargs=1, type=click.File('r'))
@click.argument('roles', nargs=-1)
@click.option(
    '--out', '-o',
    type=click.Choice(NODE_OUTPUT_TYPES),
    default='pretty',
    help='Output format.'
)
@click.pass_obj
def nodes(topfile, nodelist, roles, out):
    target_dict = topfile.targets(roles)
    nodes = yaml.load(nodelist.read(), Loader=Loader)

    if target_dict:
        role_node_dict = make_role_node_dict(target_dict, nodes)
        if out == 'pretty':
            node_output_pretty(role_node_dict)
        elif out == 'txt':
            node_output_list(role_node_dict)
        elif out == 'json':
            node_output_json(role_node_dict)
        elif out == 'yaml':
            node_output_yaml(role_node_dict)
    else:
        print('No roles found to match:\n\t' + ', '.join(roles))


def node_output_pretty(role_node_dict):
    for role in role_node_dict:
        print("\n%s" % role)
        for target in role_node_dict[role]:
            print("\t" + target)
            for node in role_node_dict[role][target]:
                print("\t\t%s" % node)


def node_output_json(role_node_dict):
    print(json.dumps(role_node_dict))


def node_output_yaml(role_node_dict):
    print(yaml.dump(role_node_dict))


def node_output_list(role_node_dict):
    for role in role_node_dict:
        print("#\n# %s\n#" % role)
        nodelist = []
        for target in role_node_dict[role]:
            for node in role_node_dict[role][target]:
                nodelist.append(node)
        nodelist.sort()
        print("\n".join(nodelist))


def make_role_node_dict(target_dict, nodes):
    """Given the target dict containing targets grouped by nodes and the list of
       nodes, this function returns a dictionary containing the list of nodes
       grouped by target and by role:

       {
            'role1':
                {
                    'target1a': ['node1aa', 'node1ab'],
                    'target1b': ['node1ba']
                },
            'role2':
                {
                    'target2a': ['node2aa']
                }
       }

    """
    result_dict = {}

    for role in target_dict.keys():
        result_dict[role] = {}
        for target in target_dict[role]:
            result_dict[role][target] = []
            if target[:2] == 'E@':
                # target is a regular expression
                target_re = re.compile(target[2:])
                for node in nodes:
                    if target_re.match(node):
                        result_dict[role][target].append(node)
            else:
                # assume target is hostname
                result_dict[role][target].append(target)
    return result_dict


if __name__ == '__main__':
    cli()
