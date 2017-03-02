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

import pytest

from rainbow import ansi
from rainbow.__main__ import main as rainbow
from .test_utils import all_stdin_types


@pytest.mark.parametrize("stdin", all_stdin_types(), ids=str)
def test_true(capsys, stdin):
    with stdin:
        assert rainbow(['true']) == 0
        out, err = capsys.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", all_stdin_types(), ids=str)
def test_false(capsys, stdin):
    with stdin:
        assert rainbow(['false']) == 1
        out, err = capsys.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", all_stdin_types('line\n'), ids=str)
def test_read_from_stdin(capsys, stdin):
    with stdin:
        assert rainbow([]) == 0
        out, err = capsys.readouterr()
        assert out == "line\n" + ansi.ANSI_RESET_ALL
        assert err == ''
