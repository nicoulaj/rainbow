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

from rainbow.__main__ import main as rainbow
from rainbow.ansi import *


def test_exit_code_0():
    assert rainbow(['true']) == 0


def test_exit_code_1():
    assert rainbow(['false']) == 1


def test_empty_output(capsys):
    rainbow(['true'])
    out, err = capsys.readouterr()
    assert out == ANSI_RESET_ALL
    assert err == ANSI_RESET_ALL
