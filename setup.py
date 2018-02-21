from setuptools import setup

setup(
    name='topfile_util',
    version='0.1',
    py_modules=['topfile_util'],
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        tfu=topfile_util:cli
        topfile_util=topfile_util:cli
    ''',
)
