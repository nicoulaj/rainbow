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

import pytest

import rainbow
from rainbow import ansi, VERSION
from rainbow.filter import FILTERS, FILTER_GROUPS
from .test_utils import run_rainbow, stdin_empty_all_variants, stdin_from_string_all_variants, \
    stdin_from_file_all_variants

rainbow.ENABLE_ANSI_STDOUT = True
rainbow.ENABLE_ANSI_STDERR = True


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_true(capfd, stdin):
    with stdin:
        assert run_rainbow(['true']) == 0
        out, err = capfd.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_false(capfd, stdin):
    with stdin:
        assert run_rainbow(['false']) == 1
        out, err = capfd.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_from_string_all_variants('line\n'), ids=str)
def test_read_from_stdin(capfd, stdin):
    with stdin:
        assert run_rainbow([]) == 0
        out, err = capfd.readouterr()
        assert out == "line\n" + ansi.ANSI_RESET_ALL
        assert err == ''


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_malformed_utf8_from_command(stdin):
    with stdin:
        assert run_rainbow(['cat', 'tests/resources/UTF-8-test.txt']) == 0


@pytest.mark.skip(reason="Issue #17: encoding is not properly managed")
@pytest.mark.parametrize("stdin", stdin_from_file_all_variants('tests/resources/UTF-8-test.txt'), ids=str)
def test_malformed_utf8_from_stdin(stdin):
    with stdin:
        assert run_rainbow([]) == 0


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_version(capfd, stdin):
    with stdin:
        assert run_rainbow(['--version']) == 0
        out, err = capfd.readouterr()
        assert out == 'rainbow %s\n' % VERSION
        assert err == ''


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_help_filter_group(capfd, stdin):
    with stdin:
        assert run_rainbow(['--help']) == 0
        out, err = capfd.readouterr()
        for filter_group in FILTER_GROUPS:
            assert filter_group.name in out
            assert filter_group.help in out
            assert err == ''


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_help_filter_included(capfd, stdin):
    with stdin:
        assert run_rainbow(['--help']) == 0
        out, err = capfd.readouterr()
        for filter in FILTERS:
            if filter.short_option:
                assert '-' + filter.short_option in out
            assert '--' + filter.long_option in out
            assert filter.help in out
            assert err == ''
