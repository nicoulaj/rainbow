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

import glob
import os
import subprocess
import sys
import tempfile

from rainbow.filter import FILTER_GROUPS

# ----------------------------------------------------------------------
# Filters collections
# ----------------------------------------------------------------------

FILTER_GROUPS_NAMES = [g.name for g in FILTER_GROUPS]
FILTER_GROUPS_HELPS = [g.help for g in FILTER_GROUPS]
FILTER_GROUPS_FILTERS = [g.filters for g in FILTER_GROUPS]

FILTERS_NAMES = [f.name for g in FILTER_GROUPS for f in g.filters]
FILTERS_HELPS = [f.help for g in FILTER_GROUPS for f in g.filters]
FILTERS_SHORT_OPTIONS = [f.short_option for g in FILTER_GROUPS for f in g.filters]
FILTERS_LONG_OPTIONS = [f.long_option for g in FILTER_GROUPS for f in g.filters]
FILTERS_WITH_SHORT_OPTION = [f for g in FILTER_GROUPS for f in g.filters if f.short_option]
FILTERS_WITH_LONG_OPTION = [f for g in FILTER_GROUPS for f in g.filters if f.long_option]

# ----------------------------------------------------------------------
# Configs collections
# ----------------------------------------------------------------------

BUILTIN_CONFIGS_NAMES = [os.path.splitext(os.path.basename(f))[0] for f in glob.glob('rainbow/data/cfg/*.cfg')]
BUILTIN_CONFIGS_REFERENCES = dict((f, glob.glob('tests/data/ref/%s-*.log' % f)) for f in BUILTIN_CONFIGS_NAMES)
BUILTIN_CONFIGS_REFERENCE_PAIRS = [(f, r) for f in BUILTIN_CONFIGS_NAMES for r in BUILTIN_CONFIGS_REFERENCES[f]]

# ----------------------------------------------------------------------
# Subcommand helpers
# ----------------------------------------------------------------------

PYTHON_EXECUTABLE = sys.executable
RAINBOW_EXECUTABLE = os.path.join(os.path.dirname(PYTHON_EXECUTABLE), 'rainbow')


def run(command, pipe=True):
    return subprocess.call(
        args=command,
        stdin=sys.stdin if pipe else None,
        stdout=sys.stdout if pipe else None,
        stderr=sys.stderr if pipe else None,
        env=dict(os.environ, **{
            'RAINBOW_ENABLE_STDOUT': str(True),
            'RAINBOW_ENABLE_STDERR': str(True)
        })
    )


def run_python(script, pipe=True):
    return run([PYTHON_EXECUTABLE, '-c', script], pipe)


def run_rainbow(args, pipe=True):
    return run([RAINBOW_EXECUTABLE] + args, pipe)


# ----------------------------------------------------------------------
# Custom STDIN helpers
# ----------------------------------------------------------------------

def stdin_empty():
    return StringAsPipeStdin('')


def stdin_pipe():
    return PipeStdin()


def stdin_empty_all_variants():
    return stdin_from_string_all_variants('')


def stdin_from_file_all_variants(path):
    return [FileStdin(path)]


def stdin_from_string_all_variants(contents):
    return [StringAsFileStdin(contents),
            StringAsPipeStdin(contents)]


class CustomStdin:
    def __init__(self):
        self.saved_stdin = None

    def __enter__(self):
        self.saved_stdin = sys.stdin
        sys.stdin = self.setup()

    def __exit__(self, type, value, traceback):
        self.teardown()
        sys.stdin = self.saved_stdin
        self.saved_stdin = None

    def setup(self):
        return sys.stdin

    def teardown(self):
        pass


class FileStdin(CustomStdin):
    def __init__(self, path):
        CustomStdin.__init__(self)
        self.path = path

    def setup(self):
        return open(self.path)

    def __str__(self):
        return "file stdin with fixed contents"


class StringAsFileStdin(CustomStdin):
    def __init__(self, contents):
        CustomStdin.__init__(self)
        self.contents = contents

    def setup(self):
        stdin_file = tempfile.mktemp()
        with open(stdin_file, 'w') as f:
            f.write(self.contents)
        return open(stdin_file, 'r')

    def __str__(self):
        return "file stdin with fixed contents"


class StringAsPipeStdin(CustomStdin):
    def __init__(self, contents):
        CustomStdin.__init__(self)
        self.contents = contents

    def setup(self):
        pipein, pipeout = os.pipe()
        with os.fdopen(pipeout, 'w') as f:
            f.write(self.contents)
        return os.fdopen(pipein, 'r')

    def __str__(self):
        return "pipe stdin with fixed contents"


class PipeStdin(CustomStdin):
    def __init__(self):
        CustomStdin.__init__(self)
        self.out = None

    def setup(self):
        pipein, pipeout = os.pipe()
        self.out = os.fdopen(pipeout, 'w')
        return os.fdopen(pipein, 'r')

    def teardown(self):
        self.out.close()
        self.out = None

    def write(self, string):
        self.out.write(string)

    def __str__(self):
        return "pipe stdin"
