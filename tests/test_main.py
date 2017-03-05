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
from rainbow.__main__ import main
from .test_utils import stdin_empty_all_variants, stdin_from_string_all_variants, stdin_from_file_all_variants


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_true(capsys, stdin):
    with stdin:
        assert main(['true']) == 0
        out, err = capsys.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_false(capsys, stdin):
    with stdin:
        assert main(['false']) == 1
        out, err = capsys.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_from_string_all_variants('line\n'), ids=str)
def test_read_from_stdin(capsys, stdin):
    with stdin:
        assert main([]) == 0
        out, err = capsys.readouterr()
        assert out == "line\n" + ansi.ANSI_RESET_ALL
        assert err == ''


@pytest.mark.skip(reason="Issue #17: encoding is not properly managed")
@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_malformed_utf8_from_command(stdin):
    with stdin:
        assert main(['cat', 'tests/resources/UTF-8-test.txt']) == 0


@pytest.mark.skip(reason="Issue #17: encoding errors not catched when reading from stdin")
@pytest.mark.parametrize("stdin", stdin_from_file_all_variants('tests/resources/UTF-8-test.txt'), ids=str)
def test_malformed_utf8_from_stdin(stdin):
    with stdin:
        assert main([]) == 0
