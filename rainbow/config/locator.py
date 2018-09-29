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

import os
from os.path import isfile, join

from rainbow import LOGGER


class ConfigLocator(object):
    def __init__(self, paths=None):
        self.paths = paths or []

    def locate_config_file(self, config, working_directory=None):

        LOGGER.debug('Trying to find config "%s"', config)

        config_file = self.locate_config_file_in_directory(os.getcwd(), config)
        if config_file:
            return config_file

        if working_directory:
            config_file = self.locate_config_file_in_directory(working_directory, config)
            if config_file:
                return config_file

        for directory in self.paths:
            if directory:
                config_file = self.locate_config_file_in_directory(directory, config)
                if config_file:
                    return config_file

    @staticmethod
    def locate_config_file_in_directory(directory, config):

        config_file = config
        if isfile(config_file):
            return config_file

        config_file = config + '.cfg'
        if isfile(config_file):
            return config + '.cfg'

        config_file = join(directory, config)
        if isfile(config_file):
            return config_file

        config_file = join(directory, config + '.cfg')
        if isfile(config_file):
            return config_file
