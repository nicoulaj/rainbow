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
from os.path import basename, isfile, join, dirname

from . import LOGGER
from .filter import FILTERS_BY_NAME, FILTERS_BY_SHORT_OPTION, FILTERS_BY_LONG_OPTION

try:
    import configparser
except ImportError:  # no cover
    import ConfigParser as configparser


class ConfigLoader(object):
    def __init__(self, paths=None):
        self.paths = paths or []

    def load_config_from_command_line(self,
                                      command_line_args,
                                      stdout_builder,
                                      stderr_builder,
                                      error_handler=lambda error: None):
        LOGGER.debug('Trying to load config from command line "%s".', command_line_args)

        config_name = self.find_config_name_from_command_line(command_line_args)
        if config_name:
            config_file = self.resolve_config_file(config_name)
            if config_file:
                self.load_config_file(config_file, stdout_builder, stderr_builder, error_handler)

    @staticmethod
    def find_config_name_from_command_line(command_line_args):

        if not command_line_args:
            return

        return basename(command_line_args[0])

    def resolve_and_load_config(self,
                                config,
                                stdout_builder,
                                stderr_builder,
                                error_handler=lambda error: None):
        config_file = self.resolve_config_file(config)
        if config_file:
            self.load_config_file(config_file, stdout_builder, stderr_builder, error_handler)
        else:
            error_handler('Could not resolve config "%s"' % config)

    def resolve_config_file(self, config, working_directory=None):

        LOGGER.debug('Trying to find config "%s"', config)

        config_file = self.resolve_config_file_in_directory(os.getcwd(), config)
        if config_file:
            return config_file

        if working_directory:
            config_file = self.resolve_config_file_in_directory(working_directory, config)
            if config_file:
                return config_file

        for directory in self.paths:
            if directory:
                config_file = self.resolve_config_file_in_directory(directory, config)
                if config_file:
                    return config_file

    @staticmethod
    def resolve_config_file_in_directory(directory, config):

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

    def load_config_file(self, config_file, stdout_builder, stderr_builder, error_handler=lambda error: None):

        LOGGER.debug('Loading the config file "%s"', config_file)

        config_parser = configparser.ConfigParser()
        try:
            if not config_parser.read(config_file):
                error_handler('Could not open config file "%s"' % config_file)
                return
        except configparser.DuplicateSectionError as e:  # no cover (inconsistent between Python 2 and 3)
            error_handler('Duplicate section "%s" in "%s"' % (e.section, config_file))
            return

        enable_stderr_filtering = True

        for section in config_parser.sections():

            if section == 'general':

                for key, value in config_parser.items(section):

                    if key == 'imports':
                        if not value:
                            error_handler('Empty imports section in config "%s"' % config_file)
                        else:
                            for config_import in [v.strip() for v in value.split(',')]:
                                if not config_import:
                                    error_handler('Empty import in config "%s"' % config_file)
                                else:
                                    config_import_file = self.resolve_config_file(config_import,
                                                                                  dirname(config_file))
                                    if config_import_file:
                                        self.load_config_file(config_import_file, stdout_builder, stderr_builder)
                                    else:
                                        error_handler('Failed to resolve import of "%s" in config "%s"'
                                                      % (config_import, config_file))

                    elif key == 'enable-stderr-filtering':
                        try:
                            enable_stderr_filtering = config_parser.getboolean(section, 'enable-stderr-filtering')
                        except ValueError as e:
                            error_handler('Invalid value "%s" for key "%s" in config "%s"' % (value, key, config_file))

                    else:
                        error_handler('Invalid key "%s" in general section of config "%s"' % (key, config_file))

            elif section == 'filters':

                for filter_name, pattern_lines in config_parser.items(section):

                    resolved_filter = \
                        FILTERS_BY_NAME.get(filter_name) or \
                        FILTERS_BY_LONG_OPTION.get(filter_name) or \
                        FILTERS_BY_SHORT_OPTION.get(filter_name)

                    if not resolved_filter:
                        error_handler('Unknown filter "%s" in config "%s"' % (filter_name, config_file))
                        continue

                    if not pattern_lines:
                        error_handler('Empty pattern for "%s" in config "%s"' % (filter_name, config_file))
                        continue

                    for pattern in pattern_lines.splitlines():
                        stdout_builder.add_mapping(pattern, resolved_filter)
                        if enable_stderr_filtering:
                            stderr_builder.add_mapping(pattern, resolved_filter)

            else:
                error_handler('Invalid section "%s" in config "%s"' % (section, config_file))

        LOGGER.info('Loaded config "%s"', config_file)
