#!/usr/bin/env python
# ----------------------------------------------------------------------
# rainbow, a command line colorizer
# Copyright (C) 2011-2017 Julien Nicoulaud <julien.nicoulaud@gmail.com>
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

from setuptools import setup

from rainbow import VERSION

setup(
    name='rainbow',
    version=VERSION,
    author='Julien Nicoulaud',
    author_email='julien.nicoulaud@gmail.com',
    description='Colorize commands output or STDIN using patterns.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    license='GPLv3',
    url='https://github.com/nicoulaj/rainbow',
    keywords='color colorize colorizer pattern',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: System',
        'Topic :: Utilities',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License (GPL)'
    ],
    packages=['rainbow'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['rainbow = rainbow.__main__:main']
    }
)
