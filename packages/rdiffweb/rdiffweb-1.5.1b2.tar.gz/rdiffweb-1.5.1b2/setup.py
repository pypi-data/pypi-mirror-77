#!/usr/bin/env python
# -*- coding: utf-8 -*-
# rdiffweb, A web interface to rdiff-backup repositories
# Copyright (C) 2019 rdiffweb contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

from distutils.cmd import Command
from distutils.command.build import build as build_
from distutils.dist import DistributionMetadata
from distutils.errors import DistutilsExecError
from io import open
import os
import subprocess
import sys


PY2 = sys.version_info[0] == 2

# Check running python version.
if not PY2 and not sys.version_info >= (3, 4):
    print('python version 3.4 is required.')
    sys.exit(1)

if PY2 and not sys.version_info >= (2, 7):
    print('python version 2.7 is required.')
    sys.exit(1)


try:
    from setuptools import setup
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup

DistributionMetadata.templates = None


class compile_all_catalogs(Command):
    """
    This is implementation of command which complies all catalogs
    (dictionaries).
    """

    description = 'compile message catalogs for all languages to binary MO files'
    user_options = [
        ('domain=', 'D',
         "domain of PO file (default 'messages')"),
        ('directory=', 'd',
         'path to base directory containing the catalogs'),
        ('locales=', 'l',
         'locale of the catalogs to compile'),
        ('use-fuzzy', 'f',
         'also include fuzzy translations'),
        ('statistics', None,
         'print statistics about translations')
    ]
    boolean_options = ['use-fuzzy', 'statistics']

    def initialize_options(self):
        self.domain = None
        self.directory = None
        self.locales = None
        self.use_fuzzy = False
        self.statistics = False

    def finalize_options(self):
        self.locales = list(map(str.strip, self.locales.split(',')))

    def run(self):
        from babel.messages.frontend import compile_catalog
        for locale in self.locales:
            compiler = compile_catalog(self.distribution)
            compiler.initialize_options()
            compiler.domain = self.domain
            compiler.directory = self.directory
            compiler.locale = locale
            compiler.use_fuzzy = self.use_fuzzy
            compiler.statistics = self.statistics
            compiler.finalize_options()
            compiler.run()


class build_less(Command):
    """
    Command to build less file with lessc.
    """

    description = 'compile *.less files with lessc command.'
    user_options = [
        ('files=', 'f',
         "List of less files to compile. Separated by `;`."),
        ('include-path=', None,
         'Set include paths. Separated by `;`'),
        ('compress', 'x',
         'Compress output by removing some whitespaces.'),
        ('output-dir', None,
         'Output directory where to generate the .less files. Default to current.'),
    ]
    boolean_options = ['compress']

    def initialize_options(self):
        self.files = None
        self.include_path = None
        self.compress = False
        self.output_dir = False

    def finalize_options(self):
        self.files = self.files.split(';')

    def run(self):
        """
        Run `lessc` for each file.
        """
        if not self.files:
            return
        # lessc --include-path=/home/ikus060/workspace/Minarca/rdiffweb.git/rdiffweb/static/less minarca_brand/main.less
        for f in self.files:
            args = ['lessc']
            if self.include_path:
                args.append('--include-path=' + self.include_path)
            if self.compress:
                args.append('--compress')
            # Source
            args.append(f)
            # Destination
            destination = f.replace('.less', '.css')
            if self.output_dir:
                destination = os.path.join(self.output_dir, os.path.basename(destination))
            args.append(destination)
            # Execute command line.
            try:
                subprocess.check_call(args)
            except:
                raise DistutilsExecError('fail to compile .less files into ' + f)


class build(build_):
    """
    This is modification of build command, compile_all_catalogs
    is added as last/first command
    """

    sub_commands = build_.sub_commands[:]
    sub_commands.insert(0, ('compile_all_catalogs', None))


# Compute requirements
if PY2:
    install_requires = [
        "CherryPy>=3.5,<17.0",
        "Jinja2>=2.6,!=2.9",
        "future>=0.15.2",
        "psutil>=2.1.1",
        "babel>=0.9.6",
        "python-ldap",
        "WTForms",
        "distro",
    ]
else:
    install_requires = [
        "CherryPy>=3.5",
        "Jinja2>=2.6,!=2.9",
        "future>=0.15.2",
        "psutil>=2.1.1",
        "babel>=0.9.6",
        "python-ldap",
        "WTForms",
        "distro",
    ]

setup_requires=[
    "babel>=0.9.6",
    "setuptools_scm",
    "minify",
]
tests_require=[
    "mock>=1.3.0",
    "coverage>=4.0.1",
    "mockldap>=0.2.6",
    "pytest<5.0.0",
]
extras_require={'tox': tests_require}

long_description_content_type = long_description = None
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    long_description_content_type = 'text/markdown'

setup(
    name='rdiffweb',
    use_scm_version=True,
    description='A web interface to rdiff-backup repositories',
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author='Patrik Dufresne',
    author_email='patrik@ikus-soft.com',
    url='https://rdiffweb.org/',
    license="GPLv3",
    packages=['rdiffweb'],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "rdiffweb = rdiffweb.main:start",
            "rdiffweb-restore = rdiffweb.core.restore:main",
        ],
        "rdiffweb.plugins": []
    },
    # new commands added and build command modified
    cmdclass={
        'build': build,
        'compile_all_catalogs': compile_all_catalogs,
        'build_less': build_less,
    },
    install_requires=install_requires,
    # required packages for build process
    setup_requires=setup_requires,
    # requirement for testing
    tests_require=tests_require,
    extras_require=extras_require,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: CherryPy',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
)
