#!/usr/bin/env python

import re
from distutils.core import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('actiontecssl/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


setup(name='python-actiontecssl',
      version=version,
      description='Actiontec API for SSL Telnet',
      author='Derek Yarnell',
      author_email='derek@umiacs.umd.edu',
      url='https://github.com/dyarnell/python-actiontecssl',
      packages=['actiontecssl'],
     )

