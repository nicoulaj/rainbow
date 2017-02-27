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

import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from rainbow.__main__ import main as rainbow
from rainbow.ansi import *


def test_001_true(capsys):
    assert rainbow(['true']) == 0
    out, err = capsys.readouterr()
    assert out == ANSI_RESET_ALL
    assert err == ANSI_RESET_ALL


def test_002_false(capsys):
    assert rainbow(['false']) == 1
    out, err = capsys.readouterr()
    assert out == ANSI_RESET_ALL
    assert err == ANSI_RESET_ALL


def test_003_read_from_stdin(capsys):
    sys.stdin = StringIO("line")
    assert rainbow([]) == 0
    out, err = capsys.readouterr()
    assert out == "line\n" + ANSI_RESET_ALL
    assert err == ANSI_RESET_ALL
