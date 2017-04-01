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

from os.path import basename

from rainbow import LOGGER
from rainbow.config.locator import ConfigLocator
from rainbow.config.parser import ConfigParser


class ConfigLoader(object):
    def __init__(self,
                 stdout_builder,
                 stderr_builder,
                 paths=None,
                 error_handler=lambda error: None):
        self.locator = ConfigLocator(paths)
        self.parser = ConfigParser(stdout_builder, stderr_builder, paths, error_handler)
        self.error_handler = error_handler

    def load_config_by_name(self, config):
        config_file = self.locator.locate_config_file(config)
        if config_file:
            self.parser.parse_file(config_file)
        else:
            self.error_handler('Could not resolve config "%s"' % config)

    def load_config_from_command_line(self, command_line_args):
        LOGGER.debug('Trying to load config from command line "%s".', command_line_args)

        config_name = self.find_config_name_from_command_line(command_line_args)
        if config_name:
            config_file = self.locator.locate_config_file(config_name)
            if config_file:
                self.parser.parse_file(config_file)

    @staticmethod
    def find_config_name_from_command_line(command_line_args):

        if not command_line_args:
            return

        return basename(command_line_args[0])
