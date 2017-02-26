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

from os.path import basename, isfile, join

from . import LOGGER
from .filter import FILTERS_BY_NAME, FILTERS_BY_SHORT_OPTION, FILTERS_BY_LONG_OPTION

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class ConfigLoader:
    def __init__(self, paths=None):
        self.paths = paths or []

    def load_config_from_command_line(self, command_line_args, stdout_builder, stderr_builder,
                                      error_handler=lambda error: None):
        LOGGER.debug('Trying to load config from command line "%s".', command_line_args)

        config_name = self.find_config_name_from_command_line(command_line_args)
        if config_name:
            config_file = self.find_config_file_by_name(config_name)
            if config_file:
                self.load_config_file(config_file, stdout_builder, stderr_builder, error_handler)

    @staticmethod
    def find_config_name_from_command_line(command_line_args):

        if not command_line_args:
            return

        # TODO detect precommands like 'sudo','builtin', 'command', 'exec', 'nocorrect', 'noglob', 'pkexec'
        # => skip to first non option argument

        # TODO level 2: detect command wrappers like 'su', 'bash -c', etc
        # => skip to first non option argument

        return basename(command_line_args[0])

    def find_config_file_by_name(self, config_name):

        LOGGER.debug('Trying to find config "%s"', config_name)

        if isfile(config_name):
            return config_name

        for directory in self.paths:
            config_file = join(directory, config_name + ".cfg")
            if isfile(config_file):
                return config_name

    def load_config_file(self, config_file, stdout_builder, stderr_builder, error_handler=lambda error: None):

        LOGGER.debug('Loading the config file "%s"', config_file)

        config_parser = configparser.ConfigParser()
        if not config_parser.read(config_file):
            error_handler('Could not open config file "%s"' % config_file)
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
                                    config_import_stripped = config_import.strip()
                                    config_import_file = self.find_config_file_by_name(config_import_stripped)
                                    if config_import_file:
                                        self.load_config_file(config_import_file, stdout_builder, stderr_builder)
                                    else:
                                        error_handler('Failed to resolve import of "%s" in config "%s"'
                                                      % (config_import_stripped, config_file))

                    elif key == 'enable-stderr-filtering':
                        lowercase_value = value.lower()
                        if lowercase_value in ['true', 'on', 'yes', 'y', '1']:
                            enable_stderr_filtering = True
                        elif lowercase_value in ['false', 'off', 'no', 'n', '0']:
                            enable_stderr_filtering = False
                        else:
                            error_handler('Invalid value "%s" for key "%s" in config "%s"' % (value, key, config_file))

                    else:
                        error_handler('Invalid key "%s" in general section of config "%s"' % (key, config_file))

            elif section == 'filters':

                for filter_name, pattern_lines in config_parser.items(section):

                    if not pattern_lines:
                        error_handler('Empty pattern for "%s" in config "%s"' % (filter_name, config_file))

                    else:
                        resolved_filter = FILTERS_BY_NAME.get(filter_name) or \
                                          FILTERS_BY_LONG_OPTION.get(filter_name) or \
                                          FILTERS_BY_SHORT_OPTION.get(filter_name)

                        if resolved_filter:
                            for pattern in pattern_lines.splitlines():
                                stdout_builder.add_mapping(pattern, resolved_filter)
                                if enable_stderr_filtering:
                                    stderr_builder.add_mapping(pattern, resolved_filter)
                        else:
                            error_handler('Unknown filter "%s" in config "%s"' % (filter_name, config_file))

            else:
                error_handler('Invalid section "%s" in config "%s"' % (section, config_file))

        LOGGER.info('Loaded config "%s"', config_file)
