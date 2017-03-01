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
import signal
import sys
from threading import Timer
from time import sleep

import pytest

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from rainbow import ansi
from rainbow.runner import CommandRunner
from rainbow.runner import STDINRunner
from rainbow.transformer import ReplaceTransformer


def test_command_line_runner_true(capsys):
    assert CommandRunner(['true']).run() == 0
    out, err = capsys.readouterr()
    assert out == ansi.ANSI_RESET_ALL
    assert err == ansi.ANSI_RESET_ALL


def test_command_line_runner_false(capsys):
    assert CommandRunner(['false']).run() == 1
    out, err = capsys.readouterr()
    assert out == ansi.ANSI_RESET_ALL
    assert err == ansi.ANSI_RESET_ALL


# TODO stderr handling not implemented
@pytest.mark.skip(reason="stderr handling not implemented")
def test_command_line_runner_identity(capsys):
    assert CommandRunner(['/bin/bash', '-c', 'echo "stdout"; echo "stderr" >&2']).run() == 0
    out, err = capsys.readouterr()
    assert out == 'stdout\n' + ansi.ANSI_RESET_ALL
    assert err == 'stderr\n' + ansi.ANSI_RESET_ALL


# TODO stderr handling not implemented
@pytest.mark.skip(reason="stderr handling not implemented")
def test_command_line_runner_stdout_transformer(capsys):
    assert CommandRunner(
        args=['/bin/bash', '-c', 'echo "message"; echo "message" >&2'],
        stdout_transformer=ReplaceTransformer('message', 'REPLACED', )
    ).run() == 0
    out, err = capsys.readouterr()
    assert out == 'REPLACED\n' + ansi.ANSI_RESET_ALL
    assert err == 'message\n' + ansi.ANSI_RESET_ALL


# TODO stderr handling not implemented
@pytest.mark.skip(reason="stderr handling not implemented")
def test_command_line_runner_stderr_transformer(capsys):
    assert CommandRunner(
        args=['/bin/bash', '-c', 'echo "message"; echo "message" >&2'],
        stderr_transformer=ReplaceTransformer('message', 'REPLACED', )
    ).run() == 0
    out, err = capsys.readouterr()
    assert out == 'message\n' + ansi.ANSI_RESET_ALL
    assert err == 'REPLACED\n' + ansi.ANSI_RESET_ALL


# TODO stderr handling not implemented
@pytest.mark.skip(reason="stderr handling not implemented")
def test_command_line_runner_stdout_and_stderr_transformers(capsys):
    assert CommandRunner(
        args=['/bin/bash', '-c', 'echo "stdout"; echo "stderr" >&2'],
        stdout_transformer=ReplaceTransformer('stdout', 'STDOUT_REPLACED'),
        stderr_transformer=ReplaceTransformer('stderr', 'STDERR_REPLACED')
    ).run() == 0
    out, err = capsys.readouterr()
    assert out == 'STDOUT_REPLACED\n' + ansi.ANSI_RESET_ALL
    assert err == 'STDERR_REPLACED\n' + ansi.ANSI_RESET_ALL


@pytest.mark.timeout(5)
def test_command_line_runner_interrupted():
    Timer(0.5, os.kill, [os.getpid(), signal.SIGINT]).start()
    assert CommandRunner(['sleep', '100']).run() == -2


def test_stdin_runner_empty(capsys):
    assert STDINRunner().run() == 0
    out, err = capsys.readouterr()
    assert out == ansi.ANSI_RESET_ALL
    assert err == ''


def test_stdin_runner_one_line(capsys):
    sys.stdin = StringIO("line")
    assert STDINRunner().run() == 0
    out, err = capsys.readouterr()
    assert out == "line\n" + ansi.ANSI_RESET_ALL
    assert err == ''


def test_stdin_runner_several_lines(capsys):
    sys.stdin = StringIO("line1\nline2")
    assert STDINRunner().run() == 0
    out, err = capsys.readouterr()
    assert out == "line1\nline2\n" + ansi.ANSI_RESET_ALL
    assert err == ''


@pytest.mark.timeout(5)
def test_stdin_runner_interrupted(capsys):
    Timer(0.5, os.kill, [os.getpid(), signal.SIGINT]).start()
    assert STDINRunner(input_=lambda: sleep(100)).run() == 1
    out, err = capsys.readouterr()
    assert out == ansi.ANSI_RESET_ALL
    assert err == ''
