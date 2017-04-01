# ----------------------------------------------------------------------
# rainbow, a terminal colorizer - https://github.com/nicoulaj/rainbow
# copyright (c) 2010-2017 rainbow contributors
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

import re

import pytest

import rainbow
from rainbow import ansi
from rainbow.__main__ import main
from .test_utils import stdin_empty_all_variants, stdin_from_string_all_variants, stdin_from_file_all_variants, \
    FILTERS_WITH_LONG_OPTION

rainbow.ENABLE_STDOUT = True
rainbow.ENABLE_STDERR = True


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_true(capfd, stdin):
    with stdin:
        assert main(['true']) == 0
        out, err = capfd.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_false(capfd, stdin):
    with stdin:
        assert main(['false']) == 1
        out, err = capfd.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_warning(capfd, stdin):
    with stdin:
        assert main(['--config', 'does-not-exist', 'true']) == 0
        out, err = capfd.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == 'rainbow warning: Could not resolve config "does-not-exist"\n' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_error(capfd, stdin, filter):
    with stdin:
        assert main(['--' + filter.long_option]) == 1
        out, err = capfd.readouterr()
        assert out == ''
        assert re.match(
            r'.*rainbow error: %s option requires (an|1) argument\nrainbow: Usage: .*' % ('--' + filter.long_option),
            err
        )


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_stacktrace(capfd, stdin):
    with stdin:
        assert main(['--does-not-exist']) == 1
        out, err = capfd.readouterr()
        assert out == ''
        assert 'No such file or directory' in err


@pytest.mark.parametrize("stdin", stdin_from_string_all_variants('line\n'), ids=str)
def test_read_from_stdin(capfd, stdin):
    with stdin:
        assert main([]) == 0
        out, err = capfd.readouterr()
        assert out == "line\n" + ansi.ANSI_RESET_ALL
        assert err == ''


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_malformed_utf8_from_command(stdin):
    with stdin:
        assert main(['cat', 'tests/resources/UTF-8-test.txt']) == 0


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_malformed_utf8_from_command_with_filters(stdin):
    with stdin:
        assert main(['--red', 'a', 'cat', 'tests/resources/UTF-8-test.txt']) == 0


@pytest.mark.parametrize("stdin", stdin_from_file_all_variants('tests/resources/UTF-8-test.txt'), ids=str)
def test_malformed_utf8_from_stdin(stdin):
    with stdin:
        assert main([]) == 0


@pytest.mark.parametrize("stdin", stdin_from_file_all_variants('tests/resources/UTF-8-test.txt'), ids=str)
def test_malformed_utf8_from_stdin_with_filters(stdin):
    with stdin:
        assert main(['--red', 'a']) == 0
