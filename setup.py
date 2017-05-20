#!/usr/bin/env python3

from distutils.core import setup

setup(name='1password',
      version='0.1',
      description='A python client for 1pasword vaults',
      author='Sean Richardson',
      author_email='richasea@gmail.com',
      packages=['onepassword'],
      package_dir={'':'python'},
      scripts=['bin/1password'])

# vim: et ai ts=4
