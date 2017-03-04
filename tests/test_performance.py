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
import os
import subprocess
from textwrap import dedent

PYTHON_EXECUTABLE = sys.executable
RAINBOW_EXECUTABLE = os.path.join(os.path.dirname(PYTHON_EXECUTABLE), 'rainbow')


def run(command):
    print('Running: ', command)
    return subprocess.call(command)


def run_python(script):
    return run([PYTHON_EXECUTABLE, '-c', script])


def run_rainbow(command):
    return run([RAINBOW_EXECUTABLE] + command)


def test_invoke_command(benchmark):
    assert benchmark(run, ['true']) == 0


def test_invoke_python(benchmark):
    assert benchmark(run_python, '') == 0


def test_python_invoke_command(benchmark):
    assert benchmark(run_python, dedent(r'''
        import sys, subprocess
        sys.exit(subprocess.call(['true']))
    ''')) == 0


def test_rainbow_no_matching_config(benchmark):
    assert benchmark(run_rainbow, ['true']) == 0


def test_rainbow_config_by_path_empty(benchmark):
    assert benchmark(run_rainbow, ['--config', 'tests/configs/config001.cfg', 'true']) == 0


def test_rainbow_config_by_path_many_filters(benchmark):
    assert benchmark(run_rainbow, ['--config', 'tests/configs/config031.cfg', 'true']) == 0
