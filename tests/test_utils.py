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
import sys
import tempfile

from rainbow.filter import FILTER_GROUPS

FILTER_GROUPS_NAMES = [g.name for g in FILTER_GROUPS]
FILTER_GROUPS_HELPS = [g.help for g in FILTER_GROUPS]
FILTER_GROUPS_FILTERS = [g.filters for g in FILTER_GROUPS]

FILTERS = [f for g in FILTER_GROUPS for f in g.filters]
FILTERS_NAMES = [f.name for g in FILTER_GROUPS for f in g.filters]
FILTERS_HELPS = [f.help for g in FILTER_GROUPS for f in g.filters]
FILTERS_SHORT_OPTIONS = [f.short_option for g in FILTER_GROUPS for f in g.filters]
FILTERS_LONG_OPTIONS = [f.long_option for g in FILTER_GROUPS for f in g.filters]


def all_stdin_types(contents=''):
    return [stdin_file(contents),
            stdin_pipe(contents)]


def stdin_file(contents=''):
    return FileStdin(contents)


def stdin_pipe(contents=''):
    return PipeStdin(contents)


class FileStdin:
    def __init__(self, contents):
        self.contents = contents
        self.saved_stdin = None

    def __enter__(self):
        self.saved_stdin = sys.stdin
        stdin_file = tempfile.mktemp()
        with open(stdin_file, 'w') as f:
            f.write(self.contents)
        sys.stdin = open(stdin_file, 'r')

    def __exit__(self, type, value, traceback):
        sys.stdin = self.saved_stdin

    def __str__(self):
        return "file stdin"


class PipeStdin:
    def __init__(self, contents):
        self.contents = contents
        self.saved_stdin = None

    def __enter__(self):
        self.saved_stdin = sys.stdin
        pipein, pipeout = os.pipe()
        with os.fdopen(pipeout, 'w') as f:
            f.write(self.contents)
        sys.stdin = os.fdopen(pipein, 'r')

    def __exit__(self, type, value, traceback):
        sys.stdin = self.saved_stdin

    def __str__(self):
        return "pipe stdin"
