#!/usr/bin/env python
# ----------------------------------------------------------------------
# rainbow, a terminal colorizer - https://github.com/nicoulaj/rainbow
# copyright (c) 2010-2018 rainbow contributors
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
# ----------------------------------------------------------------------

import os
from setuptools import setup, find_packages

from rainbow import __prog__, __version__, __license__, __author__, __email__, __url__, __description__
from rainbow.build import Clean, Build, GenerateCompletion, GenerateManPage

setup(
    name=__prog__,
    version=__version__,
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=__license__,
    description=__description__,
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    keywords='color colorize colorizer pattern',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Topic :: System',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'License :: OSI Approved :: GNU General Public License (GPL)'
    ],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    python_requires='>=3.6',
    extras_require={
        'build': [
            'Jinja2==3.0.3',
        ],
        'test': [
            'pytest==6.2.5',
            'coverage==6.2',
            'pytest-cov==3.0.0',
            'pytest-html==3.1.1',
            'pytest-timeout==2.0.2',
            'flake8==4.0.1',
            'pygal==3.0.0',
            'pygaljs==1.0.2',
            'pytest-benchmark==3.4.1'
        ]
    },
    scripts=['scripts/rainbow'],
    cmdclass={
        'clean': Clean,
        'build': Build,
        'build_completion_bash': GenerateCompletion,
        'build_completion_zsh': GenerateCompletion,
        'build_man_page': GenerateManPage
    }
)
