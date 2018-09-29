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


from os.path import dirname

from rainbow import LOGGER
from rainbow.config.locator import ConfigLocator
from rainbow.filter import FILTERS_BY_NAME, FILTERS_BY_SHORT_OPTION, FILTERS_BY_LONG_OPTION

try:
    import configparser
except ImportError:  # no cover
    import ConfigParser as configparser


class ConfigParser(object):
    def __init__(self,
                 stdout_builder,
                 stderr_builder,
                 paths=None,
                 error_handler=lambda error: None):
        self.locator = ConfigLocator(paths)
        self.stdout_builder = stdout_builder
        self.stderr_builder = stderr_builder
        self.error_handler = error_handler

    def parse_file(self, config_file):

        LOGGER.debug('Loading the config file "%s"', config_file)

        config_parser = configparser.ConfigParser()
        try:
            if not config_parser.read(config_file):
                self.error_handler('Could not open config file "%s"' % config_file)
                return
        except configparser.DuplicateSectionError as e:  # no cover (inconsistent between Python 2 and 3)
            self.error_handler('Duplicate section "%s" in "%s"' % (e.section, config_file))
            return

        enable_stderr_filtering = True

        for section in config_parser.sections():

            if section == 'general':

                for key, value in config_parser.items(section):

                    if key == 'imports':
                        if not value:
                            self.error_handler('Empty imports section in config "%s"' % config_file)
                        else:
                            for config_import in [v.strip() for v in value.split(',')]:
                                if not config_import:
                                    self.error_handler('Empty import in config "%s"' % config_file)
                                else:
                                    config_import_file = self.locator.locate_config_file(config_import,
                                                                                         dirname(config_file))
                                    if config_import_file:
                                        self.parse_file(config_import_file)
                                    else:
                                        self.error_handler('Failed to resolve import of "%s" in config "%s"'
                                                           % (config_import, config_file))

                    elif key == 'enable-stderr-filtering':
                        try:
                            enable_stderr_filtering = config_parser.getboolean(section, 'enable-stderr-filtering')
                        except ValueError as e:
                            self.error_handler(
                                'Invalid value "%s" for key "%s" in config "%s"' % (value, key, config_file))

                    else:
                        self.error_handler('Invalid key "%s" in general section of config "%s"' % (key, config_file))

            elif section == 'filters':

                for filter_name, pattern_lines in config_parser.items(section):

                    resolved_filter = \
                        FILTERS_BY_NAME.get(filter_name) or \
                        FILTERS_BY_LONG_OPTION.get(filter_name) or \
                        FILTERS_BY_SHORT_OPTION.get(filter_name)

                    if not resolved_filter:
                        self.error_handler('Unknown filter "%s" in config "%s"' % (filter_name, config_file))
                        continue

                    if not pattern_lines:
                        self.error_handler('Empty pattern for "%s" in config "%s"' % (filter_name, config_file))
                        continue

                    for pattern in pattern_lines.splitlines():
                        self.stdout_builder.add_mapping(pattern, resolved_filter)
                        if enable_stderr_filtering:
                            self.stderr_builder.add_mapping(pattern, resolved_filter)

            else:
                self.error_handler('Invalid section "%s" in config "%s"' % (section, config_file))

        LOGGER.info('Loaded config "%s"', config_file)
