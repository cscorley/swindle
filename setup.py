# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='swindle',
    version='0.0.1',
    description='A LISP-like that throws away parentheses for Python-style indentation.',
    long_description=readme,
    author='Christopher S. Corley',
    author_email='cscorley@ua.edu',
    url='https://github.com/cscorley/swindle',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

