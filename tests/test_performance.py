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

from textwrap import dedent
from .test_utils import run, run_python, run_rainbow, stdin_empty


def test_invoke_command(benchmark):
    with stdin_empty():
        assert benchmark(
            run,
            ['true'],
            pipe=False
        ) == 0


def test_invoke_python(benchmark):
    with stdin_empty():
        assert benchmark(
            run_python,
            '',
            pipe=False
        ) == 0


def test_python_invoke_command(benchmark):
    with stdin_empty():
        assert benchmark(
            run_python,
            dedent(r'''
                import sys, subprocess
                sys.exit(subprocess.call(['true']))
            '''),
            pipe=False
        ) == 0


def test_rainbow_no_matching_config(benchmark):
    with stdin_empty():
        assert benchmark(
            run_rainbow,
            ['true'],
            pipe=False
        ) == 0


def test_rainbow_config_by_path_empty(benchmark):
    with stdin_empty():
        assert benchmark(
            run_rainbow,
            ['--config', 'tests/data/cfg/config001.cfg', 'true'],
            pipe=False
        ) == 0


def test_rainbow_config_by_path_many_filters(benchmark):
    with stdin_empty():
        assert benchmark(
            run_rainbow,
            ['--config', 'tests/data/cfg/config031.cfg', 'true'],
            pipe=False
        ) == 0
