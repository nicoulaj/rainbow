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

import sys

import logging
import os

__prog__ = __name__
__author__ = 'Julien Nicoulaud'
__email__ = 'julien.nicoulaud@gmail.com'
__url__ = 'https://github.com/nicoulaj/rainbow'
__copyright__ = 'copyright 2010-2018 rainbow contributors'
__license__ = 'GPLv3'
__description__ = 'Colorize commands output using patterns.'
__version__ = '2.7.1'

LOGGER = logging.getLogger(__prog__)

DEFAULT_PATH = [
    os.environ.get('RAINBOW_CONFIGS'),
    os.path.join(os.environ.get('XDG_CONFIG_HOME') or os.path.expanduser('~/.config'), __prog__),
    os.path.join(os.path.expanduser('~'), '.' + __prog__),
    os.path.join(os.sep, 'etc', __prog__),
    os.path.join(os.sep, os.path.dirname(__file__), 'config', 'builtin')
]

ENABLE_STDOUT = bool(os.environ.get('RAINBOW_ENABLE_STDOUT', sys.stdout.isatty()))
ENABLE_STDERR = bool(os.environ.get('RAINBOW_ENABLE_STDERR', sys.stderr.isatty()))
