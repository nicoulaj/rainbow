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
from .config import ConfigLoader
from .filter import FILTER_GROUPS, FILTERS_BY_LONG_OPTION
from .transformer import TransformerBuilder, IdentityTransformer


class CommandLineParser:
    def __init__(self, paths=None, error_handler=lambda error: None):
        self.loader = ConfigLoader(paths)
        self.stdout_builder = None
        self.stderr_builder = None
        self.error_handler = error_handler

    def parse(self, args):

        self.stdout_builder = TransformerBuilder()
        self.stderr_builder = TransformerBuilder()

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

        if remaining_args and not self.stdout_builder.transformers:
            self.loader.load_config_from_command_line(remaining_args,
                                                      self.stdout_builder,
                                                      self.stderr_builder,
                                                      self.error_handler)

        stdout_transformer = self.stdout_builder.build()
        stderr_transformer = self.stderr_builder.build() if values.enable_stderr_filtering else IdentityTransformer

        return remaining_args, stdout_transformer, stderr_transformer

    def handle_config_option(self, option, opt, value, parser):
        config_file = self.loader.find_config_file_by_name(value)

        if config_file:
            self.loader.load_config_file(config_file, self.stdout_builder, self.stderr_builder, self.error_handler)
        else:
            parser.error('Could not find config "%s"', value)

    def handle_pattern_option(self, option, opt, value, parser):
        filter_name = option.get_opt_string()[2:]
        filter = FILTERS_BY_LONG_OPTION[filter_name]

        if not filter:
            parser.error('Could not find filter "%s"', filter_name)

        self.stdout_builder.add_mapping(value, filter)
        self.stderr_builder.add_mapping(value, filter)

    @staticmethod
    def handle_verbosity_option(option, opt, value, parser):
        LOGGER.setLevel(LOGGER.level - 10)
