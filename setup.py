import os

from setuptools import setup, find_packages


def here(*path):
    return os.path.join(os.path.dirname(__file__), *path)


# This is a quick and dirty way to include everything from
# requirements.txt as package dependencies.
with open(here('requirements.txt')) as fp:
    install_requires = fp.read().split()


setup(
    name='graph-data',
    version='0.1.0a0',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'graph-data= graph_data.cli:main',
        ],
    }
)
