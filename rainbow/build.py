# ----------------------------------------------------------------------
# rainbow, a terminal colorizer - https://github.com/nicoulaj/rainbow
# copyright (c) 2010-2018 rainbow contributors
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

import errno

import gzip
import logging
import os
import shutil
from distutils import log
from distutils.command.build import build
from distutils.command.clean import clean
from distutils.core import Command
from distutils.dir_util import remove_tree
from distutils.errors import DistutilsOptionError

from .filter import FILTERS, FILTER_GROUPS


class Build(build):  # no cover
    def run(self):
        self.run_command("build_completion_bash")
        self.run_command("build_completion_zsh")
        self.run_command("build_man_page")
        build.run(self)


class Clean(clean):  # no cover

    def __init__(self, dist, **kwargs):
        self.paths = None
        clean.__init__(self, dist, **kwargs)
        self.user_options += [
            ('paths=', 'p', 'paths'),
        ]

    def initialize_options(self):
        clean.initialize_options(self)

    def finalize_options(self):
        clean.finalize_options(self)
        if self.paths is None:  # no cover
            raise DistutilsOptionError('"paths" option is required')

    def run(self):
        clean.run(self)
        if self.all:
            for path in [path.strip() for path in self.paths.split(',')]:
                if os.path.isdir(path):
                    remove_tree(path)
                elif os.path.isfile(path):
                    log.info("removing '%s'", path)
                    os.remove(path)
                else:
                    log.info("'%s' does not exist -- can't clean it", path)


class GenerateCompletion(Command):
    description = 'Generate shell completion script.'

    user_options = [
        ('shell=', 'S', 'shell (bash or zsh)'),
        ('output=', 'O', 'output file')
    ]

    def __init__(self, dist, **kwargs):
        self.shell = None
        self.output = None
        Command.__init__(self, dist, **kwargs)

    def initialize_options(self):
        pass

    def finalize_options(self):
        if self.shell is None:  # no cover
            raise DistutilsOptionError('"shell" option is required')
        if self.output is None:  # no cover
            raise DistutilsOptionError('"output" option is required')

    def run(self):
        self.announce('generating %s completion -> %s' % (self.shell, self.output))

        makeparentdirs(self.output)

        try:
            from jinja2 import Environment, FileSystemLoader
            Environment(loader=FileSystemLoader('templates')) \
                .get_template('completion.%s' % self.shell) \
                .stream(filters=FILTERS) \
                .dump(self.output)
        except ImportError:
            logging.warning('Jinja is not installed, skipping %s completion generation' % self.shell)


class GenerateManPage(Command):
    description = 'Generate man page.'

    user_options = [
        ('output=', 'O', 'output file')
    ]

    def __init__(self, dist, **kwargs):
        self.output = None
        Command.__init__(self, dist, **kwargs)

    def initialize_options(self):
        pass

    def finalize_options(self):
        if self.output is None:  # no cover
            raise DistutilsOptionError('"output" option is required')

    def run(self):
        self.announce('generating man page -> %s' % self.output)

        makeparentdirs(self.output)

        try:
            from jinja2 import Environment, FileSystemLoader
            Environment(loader=FileSystemLoader('templates')) \
                .get_template('rainbow.man') \
                .stream(filter_groups=FILTER_GROUPS) \
                .dump(self.output)

            file_in = None
            file_out = None
            try:
                file_in = open(self.output, 'rb')
                file_out = gzip.open(self.output + '.gz', 'wb')
                shutil.copyfileobj(file_in, file_out)
            finally:
                if file_in:
                    file_in.close()
                if file_out:
                    file_out.close()
        except ImportError:
            logging.warning('Jinja is not installed, skipping man page generation')


def makeparentdirs(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):  # no cover
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
