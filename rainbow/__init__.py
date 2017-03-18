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

import logging
import os
import sys

LOGGER = logging.getLogger('rainbow')

VERSION = '2.6.1'

DEFAULT_PATH = [
    os.environ.get('RAINBOW_CONFIGS'),
    os.path.expanduser('~/.rainbow'),
    os.path.join(os.sep, 'etc', 'rainbow'),
    os.path.join(os.sep, os.path.dirname(__file__), 'configs')
]

ENABLE_STDOUT = bool(os.environ.get('RAINBOW_ENABLE_STDOUT', sys.stdout.isatty()))
ENABLE_STDERR = bool(os.environ.get('RAINBOW_ENABLE_STDERR', sys.stderr.isatty()))
