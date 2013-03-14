#!/usr/bin/env python

from core import __appname__, __version__
from setuptools import setup

long_description = open('README.md', 'r').read()

setup(
	name=__appname__,
	version=__version__,
	packages=[
		'core',
		'modules',
	],
	author="Johnathon Mlady",
	long_description=long_description,
	description='Rapier - IRC Bot',
	license="Expat",
	url="",
	platforms=['any']
)
