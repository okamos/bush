#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages


ROOT_DIR = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')

requires = [
    'boto3',
    'botocore'
]


def get_version():
    line = open(os.path.join(ROOT_DIR, 'boto3', '__init__.py')).read()
    return VERSION_RE.search(line).group(1)


setup(
    name='bush',
    version=get_version(),
    description='Easy to use, AWS operations by cli',
    # long_description=open('README.rst').read(),
    author='Shinichi Okamoto',
    url='https://github.com/okamos/bush',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requires,
    license="MIT",
    # ref https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'
    ],
)
