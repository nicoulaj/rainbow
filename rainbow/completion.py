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
from distutils.core import Command
from distutils.errors import DistutilsOptionError
from jinja2 import Environment, PackageLoader
from .filter import FILTERS


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

        directory = os.path.dirname(self.output)
        if not os.path.exists(directory):
            os.makedirs(directory)  # no cover

        Environment(loader=PackageLoader('rainbow', 'templates')) \
            .get_template('completion.%s' % self.shell) \
            .stream(filters=FILTERS) \
            .dump(self.output)