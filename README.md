# topfile_util

These Salt topfile utilities are designed to help inspect and troubleshoot
complex top files.  The toplevel command is `tfu` or `topfile_util` and
requires at least one subcommand as shown below.  It will look in the current
directory for a `top.sls` or you can specify a file using the `-t <FILENAME>`
option.

> Note: What I refer to here as roles, are actually salt state files.  See
> the [example directory](example) for the simplified example used in the
> examples below.

```
$ tfu

Usage: tfu [OPTIONS] COMMAND [ARGS]...

Options:
  -t, --topfile FILENAME  Path to topfile
  --help                  Show this message and exit.

Commands:
  nodes    Print nodes that match roles.
  targets  Print salt targets that match roles.
```

## Targets

The `targets` subcommand will print out all of the targets in the topfile
found to match the specified `<ROLES>`.

Usage:

```
$ tfu targets --help

Usage: tfu targets [OPTIONS] [ROLES]...

  Print salt targets that match roles.

Options:
  --help  Show this message and exit.
```

Example:

```
$ tfu targets elasticsearch.master

elasticsearch.master
	E@r1[012]c1n1.example.lan
```

## Nodes

The `nodes` subcommand requires a YAML formatted node list as the first
argument, followed by option `<ROLES>`.  It also takes an optional output
formatter.

Usage:

```
$ tfu nodes --help

Usage: tfu nodes [OPTIONS] NODELIST [ROLES]...

  Print nodes that match roles.

Options:
  -o, --out [pretty|txt|json|yaml]
                                  Output format.
  --help                          Show this message and exit.
```

Example using the `pretty` formatter:

```
$ tfu nodes nodes.yml elasticsearch.master

elasticsearch.master
	E@r1[012]c1n1.example.lan
		r10c1n1.example.lan
		r11c1n1.example.lan
		r12c1n1.example.lan
```

```
$ tfu nodes -o txt nodes.yml elasticsearch.master

#
# elasticsearch.master
#
r10c1n1.example.lan
r11c1n1.example.lan
r12c1n1.example.lan
```

# Misc

A yaml file suitable for use as your nodes list can probably be generated with
the following salt command:

```
salt-run manage.up > nodes.yaml
```

# Limitations

I've only really run this on 3.6, it's pretty simple though so fixing it
shouldn't be too hard.