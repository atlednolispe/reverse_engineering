# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme_ = f.read()

with open('LICENSE') as f:
    license_ = f.read()

setup(
    name='nubia',
    version='0.1.0',
    description='Python SDK for successful request of Nubia',
    long_description=readme_,
    author='atlednolispe',
    author_email='atlednolispe@gmail.com',
    url='https://github.com/atlednolispe/reverse_engineering/nubia',
    license=license_,
    packages=find_packages(exclude=('extras', 'requirements', 'static', 'tests', 'docs'))
)
