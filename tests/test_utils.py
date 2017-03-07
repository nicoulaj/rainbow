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

import tempfile
import sys
import os
import subprocess

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
# Subcommand helpers
# ----------------------------------------------------------------------

PYTHON_EXECUTABLE = sys.executable
RAINBOW_EXECUTABLE = os.path.join(os.path.dirname(PYTHON_EXECUTABLE), 'rainbow')


def run(command, pipe=True):
    return subprocess.call(args=command,
                           stdin=sys.stdin if pipe else None,
                           stdout=sys.stdout if pipe else None,
                           stderr=sys.stderr if pipe else None)


def run_python(script, pipe=True):
    return run([PYTHON_EXECUTABLE, '-c', script], pipe)


def run_rainbow(args, pipe=True):
    return run([RAINBOW_EXECUTABLE] + args, pipe)


# ----------------------------------------------------------------------
# Custom STDIN helpers
# ----------------------------------------------------------------------

def stdin_empty():
    return StringAsPipeStdin('')


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
        sys.stdin = self.make_stdin()

    def __exit__(self, type, value, traceback):
        sys.stdin = self.saved_stdin

    def make_stdin(self):
        return sys.stdin


class FileStdin(CustomStdin):
    def __init__(self, path):
        CustomStdin.__init__(self)
        self.path = path

    def make_stdin(self):
        return open(self.path)

    def __str__(self):
        return "file stdin"


class StringAsFileStdin(CustomStdin):
    def __init__(self, contents):
        CustomStdin.__init__(self)
        self.contents = contents

    def make_stdin(self):
        stdin_file = tempfile.mktemp()
        with open(stdin_file, 'w') as f:
            f.write(self.contents)
        return open(stdin_file)

    def __str__(self):
        return "file stdin"


class StringAsPipeStdin(CustomStdin):
    def __init__(self, contents):
        CustomStdin.__init__(self)
        self.contents = contents

    def make_stdin(self):
        pipein, pipeout = os.pipe()
        with os.fdopen(pipeout, 'w') as f:
            f.write(self.contents)
        return os.fdopen(pipein, 'r')

    def __str__(self):
        return "pipe stdin"
