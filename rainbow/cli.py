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

from optparse import OptionParser, OptionGroup

from . import *
from .colorizer import RegexColorizer
from .config import ConfigLoader
from .filter import FILTER_GROUPS, FILTERS_BY_LONG_OPTION
from .settings import Settings

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class CommandLineParser:
    def __init__(self, paths=None):
        self.loader = ConfigLoader(paths)
        self.settings = None
        self.colorizer = None

    def parse(self, args):

        self.colorizer = RegexColorizer()
        self.settings = Settings()

        parser = OptionParser(usage='%prog [options] -- command [args...] ',
                              version='%prog ' + RAINBOW_VERSION,
                              description='Colorize commands output using patterns.')
        parser.formatter.max_help_position = 50
        parser.formatter.width = 150

        parser.add_option(
            '-f',
            '--config',
            action='callback',
            callback=self.handle_config_option,
            type='string',
            help='Load a config file defining patterns. Go to %s for examples. '
                 'The option can be called several times.' % RAINBOW_CONFIGS_HOME
        )
        parser.add_option(
            '-v',
            '--verbose',
            action='callback',
            callback=self.handle_verbosity_option,
            help='Turn on verbose mode. This option can be called several times to increase the verbosity level.'
        )
        parser.add_option(
            '--disable-stderr-filtering',
            action='store_false',
            dest='enable_stderr_filtering',
            default=True,
            help='Disable STDERR filtering, which can have unexpected effects on commands directly using tty.'
        )

        for group in FILTER_GROUPS:
            option_group = OptionGroup(parser, group.name, group.help)
            for f in group.filters:
                if f.short_option:
                    option_group.add_option('-' + f.short_option,
                                            '--' + f.long_option,
                                            action='callback',
                                            callback=self.handle_pattern_option,
                                            type='string',
                                            help=f.help)
                else:
                    option_group.add_option('--' + f.long_option,
                                            action='callback',
                                            callback=self.handle_pattern_option,
                                            type='string',
                                            help=f.help)
            parser.add_option_group(option_group)

        (values, remaining_args) = parser.parse_args(args=args)

        if remaining_args and not self.colorizer:
            self.loader.load_config_from_command_line(remaining_args, self.settings, self.colorizer)

        self.settings.enable_stderr_filtering = not values.enable_stderr_filtering

        return remaining_args, self.settings, self.colorizer

    def handle_config_option(self, option, opt, value, parser):
        self.loader.load_config_by_name(value, self.settings, self.colorizer)

    def handle_pattern_option(self, option, opt, value, parser):
        self.colorizer.register_pattern_with_filter(value, FILTERS_BY_LONG_OPTION[option.get_opt_string()[2:]])

    @staticmethod
    def handle_verbosity_option(option, opt, value, parser):
        LOGGER.setLevel(LOGGER.level - 10)
