#!/usr/bin/env python3

from setuptools import setup

setup(name='1password',
      version='1.0',
      description='A python client for 1pasword vaults',
      author='Sean Richardson',
      author_email='richasea@gmail.com',
      packages=['onepassword'],
      package_dir={'':'python'},
      scripts=['bin/1password'],
      install_requires=["pbkdf2>=1.3", "pycrypto>=2.6.1"])

# vim: et ai ts=4
