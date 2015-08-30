#!/usr/bin/env python
#encoding: utf-8

import os
from setuptools import setup

CURR_PATH = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(CURR_PATH, 'README.md'), 'r') as readme:
    README = readme.read()

setup(
    name='django-zookeeper-manager',
    version='0.1',
    packages=['zookeeper'],
    install_requires = ['kazoo>=2.2.1'],
    include_package_data=True,
    license='BSD License',
    description='zookeeper web manager',
    long_description=README,
    author='Silence',
    author_email='imsilence@outlook.com',
    classifiers=[
    ],
)
