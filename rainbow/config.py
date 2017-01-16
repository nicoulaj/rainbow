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
from .filter import FILTERS_BY_NAME, FILTERS_BY_LONG_OPTION


class ConfigLoader:
    def __init__(self, paths=None):
        self.paths = paths or []

    def load_config_from_command_line(self, command_line_args, settings, colorizer):
        LOGGER.debug('Trying to load config from command line "%s".', command_line_args)
        return self.load_config_by_name(basename(command_line_args[0]), settings, colorizer)

    def load_config_by_name(self, name, settings, colorizer):

        LOGGER.debug('Trying to load config "%s".', name)

        for directory in self.paths:
            config_file = join(directory, name + ".cfg")
            if isfile(config_file):
                return self.load_config_file(config_file, settings, colorizer)

        LOGGER.error('Could not locate the config "%s".', name)
        return False

    def load_config_file(self, config_file, settings, colorizer):

        LOGGER.debug('Loading the config file "%s."', config_file)

        result = True

        config_parser = configparser.RawConfigParser()
        config_parser.read(config_file)

        if config_parser.has_section('general'):

            if config_parser.has_option('general', 'imports'):
                for config_import in [v.strip() for v in config_parser.get('general', 'imports').split(',')]:
                    result &= self.load_config_by_name(config_import, settings, colorizer)

            if config_parser.has_option('general', 'enable-stderr-filtering'):
                settings.enable_stderr_filtering = config_parser.get('general', 'enable-stderr-filtering')

        if config_parser.has_section('filters'):
            for filter_name, pattern_lines in config_parser.items('filters'):

                resolved_filter = FILTERS_BY_NAME[filter_name] or FILTERS_BY_LONG_OPTION[filter_name]
                if resolved_filter:
                    for pattern in pattern_lines.splitlines():
                        colorizer.register_pattern_with_filter(pattern, resolved_filter)
                else:
                    LOGGER.warning('Unknown filter "%s."', filter_name)

        LOGGER.info('Loaded config "%s."', config_file)
        return result
