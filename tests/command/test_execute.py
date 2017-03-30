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
import sys
from textwrap import dedent
from threading import Timer

import pytest

from rainbow import ansi
from rainbow.command.execute import ExecuteCommand
from rainbow.transformer import ReplaceTransformer
from tests.test_utils import stdin_empty_all_variants, stdin_from_string_all_variants


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_true(capfd, stdin):
    with stdin:
        assert ExecuteCommand(['true']).run() == 0
        out, err = capfd.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_false(capfd, stdin):
    with stdin:
        assert ExecuteCommand(['false']).run() == 1
        out, err = capfd.readouterr()
        assert out == ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_identity(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            [sys.executable, '-c', dedent(r'''
                import sys
                sys.stdout.write('stdout\n')
                sys.stdout.flush()
                sys.stderr.write('stderr\n')
                sys.stderr.flush()
            ''')]
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'stdout\n' + ansi.ANSI_RESET_ALL
        assert err == 'stderr\n' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_identity_no_newline(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            [sys.executable, '-c', dedent(r'''
                import sys
                sys.stdout.write('stdout')
                sys.stdout.flush()
                sys.stderr.write('stderr')
                sys.stderr.flush()
            ''')]
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'stdout' + ansi.ANSI_RESET_ALL
        assert err == 'stderr' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_identity_partial_line(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            [sys.executable, '-c', dedent(r'''
                import sys, time
                sys.stdout.write('stdout1')
                sys.stdout.flush()
                time.sleep(0.5)
                sys.stderr.write('stderr1')
                sys.stderr.flush()
                time.sleep(0.5)
                sys.stdout.write('stdout2')
                sys.stdout.flush()
                time.sleep(0.5)
                sys.stderr.write('stderr2')
            ''')]
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'stdout1\rstdout1stdout2' + ansi.ANSI_RESET_ALL
        assert err == 'stderr1\rstderr1stderr2' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_identity_overwritten_line(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            [sys.executable, '-c', dedent(r'''
                import sys, time
                sys.stdout.write('stdout1')
                sys.stdout.flush()
                time.sleep(0.5)
                sys.stderr.write('stderr1')
                sys.stderr.flush()
                time.sleep(0.5)
                sys.stdout.write('\rstdout2')
                sys.stdout.flush()
                time.sleep(0.5)
                sys.stderr.write('\rstderr2')
                sys.stderr.flush()
                time.sleep(0.5)
            ''')]
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'stdout1\rstdout1\rstdout2' + ansi.ANSI_RESET_ALL
        assert err == 'stderr1\rstderr1\rstderr2' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_identity_bash(capfd, stdin):
    with stdin:
        assert ExecuteCommand(['/bin/bash', '-c', 'echo "stdout"; echo "stderr" >&2']).run() == 0
        out, err = capfd.readouterr()
        assert out == 'stdout\n' + ansi.ANSI_RESET_ALL
        assert err == 'stderr\n' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_identity_mixed_stdin_and_err(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            [sys.executable, '-c', dedent(r'''
                import sys
                sys.stdout.write('stdout1\n')
                sys.stderr.write('stderr2\n')
                sys.stdout.write('stdout3')
                sys.stdout.write('stdout4\n')
                sys.stderr.write('stderr4')
                sys.stderr.write('stderr5\n')
            ''')]
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'stdout1\nstdout3stdout4\n' + ansi.ANSI_RESET_ALL
        assert err == 'stderr2\nstderr4stderr5\n' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_bufferized_output(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            [sys.executable, '-c', dedent(r'''
                import sys, time
                sys.stdout.write('stdout1\n')
                sys.stdout.flush()
                time.sleep(0.5)
                sys.stdout.write('stdout2\nstdout3\n')
                sys.stdout.flush()
                time.sleep(0.5)
                sys.stdout.write('stdout4\n')
            ''')]
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'stdout1\nstdout2\nstdout3\nstdout4\n' + ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_bufferized_partial_lines(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            [sys.executable, '-c', dedent(r'''
                import sys, time
                sys.stdout.write('std')
                sys.stdout.flush()
                time.sleep(0.5)
                sys.stdout.write('out1\nstdout2\n')
            ''')]
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'std\rstdout1\nstdout2\n' + ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_unflushed_output(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            [sys.executable, '-c', dedent(r'''
                import sys
                sys.stdout.write('message')
            ''')]
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'message' + ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.skip(reason="Issue #23: missing unit tests for executing subcommands with stdin")
@pytest.mark.timeout(2)
@pytest.mark.parametrize("stdin", stdin_from_string_all_variants('line\n'), ids=str)
def test_cat_stdin(capfd, stdin):
    with stdin:
        assert ExecuteCommand(['cat']).run() == 0
        out, err = capfd.readouterr()
        assert out == 'line\n' + ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.skip(reason="Issue #23: missing unit tests for executing subcommands with stdin")
@pytest.mark.timeout(2)
@pytest.mark.parametrize("stdin", stdin_from_string_all_variants('line1\nline2\n'), ids=str)
def test_cat_stdin_two_lines(capfd, stdin):
    with stdin:
        assert ExecuteCommand(['cat']).run() == 0
        out, err = capfd.readouterr()
        assert out == 'line1\nline2\n' + ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_stdout_transformer(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            args=[sys.executable, '-c', dedent(r'''
                import sys
                sys.stdout.write('message\n')
                sys.stderr.write('message\n')
            ''')],
            stdout_transformer=ReplaceTransformer('message', 'REPLACED')
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'REPLACED\n' + ansi.ANSI_RESET_ALL
        assert err == 'message\n' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_stdout_transformer_bash(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            args=['/bin/bash', '-c', 'echo "message"; echo "message" >&2'],
            stdout_transformer=ReplaceTransformer('message', 'REPLACED')
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'REPLACED\n' + ansi.ANSI_RESET_ALL
        assert err == 'message\n' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_stderr_transformer(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            args=[sys.executable, '-c', dedent(r'''
                import sys
                sys.stdout.write('message\n')
                sys.stderr.write('message\n')
            ''')],
            stderr_transformer=ReplaceTransformer('message', 'REPLACED')
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'message\n' + ansi.ANSI_RESET_ALL
        assert err == 'REPLACED\n' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_stderr_transformer_bash(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            args=['/bin/bash', '-c', 'echo "message"; echo "message" >&2'],
            stderr_transformer=ReplaceTransformer('message', 'REPLACED')
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'message\n' + ansi.ANSI_RESET_ALL
        assert err == 'REPLACED\n' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_stdout_and_stderr_transformers(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            args=[sys.executable, '-c', dedent(r'''
                import sys
                sys.stdout.write('stdout\n')
                sys.stderr.write('stderr\n')
            ''')],
            stdout_transformer=ReplaceTransformer('stdout', 'STDOUT_REPLACED'),
            stderr_transformer=ReplaceTransformer('stderr', 'STDERR_REPLACED')
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'STDOUT_REPLACED\n' + ansi.ANSI_RESET_ALL
        assert err == 'STDERR_REPLACED\n' + ansi.ANSI_RESET_ALL


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_stdout_and_stderr_transformers_bash(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            args=['/bin/bash', '-c', 'echo "stdout"; echo "stderr" >&2'],
            stdout_transformer=ReplaceTransformer('stdout', 'STDOUT_REPLACED'),
            stderr_transformer=ReplaceTransformer('stderr', 'STDERR_REPLACED')
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'STDOUT_REPLACED\n' + ansi.ANSI_RESET_ALL
        assert err == 'STDERR_REPLACED\n' + ansi.ANSI_RESET_ALL


@pytest.mark.skip(reason="Issue #23: missing unit tests for executing subcommands with stdin")
@pytest.mark.timeout(2)
@pytest.mark.parametrize("stdin", stdin_from_string_all_variants("foo bar"), ids=str)
def test_read_bash(capfd, stdin):
    with stdin:
        assert ExecuteCommand(
            args=['/bin/bash', '-c', 'read -p "Enter your input:" result; echo "You entered: $result"']
        ).run() == 0
        out, err = capfd.readouterr()
        assert out == 'Enter your input:\nYou entered: foo bar' + ansi.ANSI_RESET_ALL
        assert err == ansi.ANSI_RESET_ALL


@pytest.mark.timeout(5)
@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_interrupted(stdin):
    with stdin:
        Timer(1.0, os.kill, [os.getpid(), signal.SIGINT]).start()
        assert ExecuteCommand(['sleep', '100']).run() == -2


@pytest.mark.parametrize("stdin", stdin_empty_all_variants(), ids=str)
def test_malformed_utf8(stdin):
    with stdin:
        assert ExecuteCommand(['cat', 'tests/resources/UTF-8-test.txt']).run() == 0
