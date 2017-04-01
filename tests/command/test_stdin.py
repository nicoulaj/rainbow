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

import os
import signal
from threading import Timer

import pytest

from rainbow import ansi
from rainbow.command.stdin import STDINCommand
from tests.test_utils import stdin_empty_all_variants, stdin_from_string_all_variants, stdin_from_file_all_variants, \
    stdin_pipe


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_empty(capfd, stdin):
    with stdin:
        assert STDINCommand().run() == 0
        out, err = capfd.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ''


@pytest.mark.parametrize("stdin", stdin_from_string_all_variants('line\n'), ids=str)
def test_one_line(capfd, stdin):
    with stdin:
        assert STDINCommand().run() == 0
        out, err = capfd.readouterr()
        assert out == 'line\n' + ansi.ANSI_RESET_ALL
        assert err == ''


@pytest.mark.parametrize("stdin", stdin_from_string_all_variants('line1\nline2\n'), ids=str)
def test_several_lines(capfd, stdin):
    with stdin:
        assert STDINCommand().run() == 0
        out, err = capfd.readouterr()
        assert out == 'line1\nline2\n' + ansi.ANSI_RESET_ALL
        assert err == ''


def test_interrupted(capfd):
    with stdin_pipe():
        Timer(1.0, os.kill, [os.getpid(), signal.SIGINT]).start()
        assert STDINCommand().run() == 1
        out, err = capfd.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ''


@pytest.mark.parametrize("stdin", stdin_from_file_all_variants('tests/data/UTF-8-test.txt'), ids=str)
def test_malformed_utf8(stdin):
    with stdin:
        assert STDINCommand().run() == 0
