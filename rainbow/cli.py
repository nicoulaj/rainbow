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

import sys
from optparse import OptionParser, OptionGroup, BadOptionError, AmbiguousOptionError

from . import __version__, __description__, LOGGER, DEFAULT_PATH
from .command.execute import ExecuteCommand
from .command.noop import NoOpCommand
from .command.print_config_names import PrintConfigNamesCommand
from .command.print_path import PrintPathCommand
from .command.stdin import STDINCommand
from .config.loader import ConfigLoader
from .filter import FILTER_GROUPS, FILTERS_BY_LONG_OPTION
from .transformer import TransformerBuilder, IdentityTransformer


class CommandLineParser(OptionParser):
    def __init__(self,
                 paths=None,
                 stdout_builder=None,
                 stderr_builder=None,
                 error_handler=lambda error: None):
        OptionParser.__init__(self,
                              usage='%prog [options] -- command [args...] ',
                              version='%prog ' + __version__,
                              description=__description__)
        self.disable_interspersed_args()
        self.formatter.max_help_position = 50
        self.formatter.width = 150
        self.command = None
        self.stdout_builder = stdout_builder or TransformerBuilder()
        self.stderr_builder = stderr_builder or TransformerBuilder()
        self.error_handler = error_handler
        self.config_loader = ConfigLoader(self.stdout_builder, self.stderr_builder, paths, error_handler)
        self.add_option('-f',
                        '--config',
                        action='callback',
                        callback=self.handle_config_option,
                        type='string',
                        help='Load a config file defining patterns. '
                             'This option can be called several times.')
        self.add_option('-v',
                        '--verbose',
                        action='callback',
                        callback=self.handle_verbosity_option,
                        help='Turn on verbose mode. '
                             'This option can be called several times to increase the verbosity level.')
        self.add_option('--print-path',
                        action='callback',
                        callback=self.handle_print_path_option,
                        help='Print config paths.')
        self.add_option('--print-config-names',
                        action='callback',
                        callback=self.handle_print_config_names_option,
                        help='Print config names.')
        self.add_option('--disable-stderr-filtering',
                        action='store_false',
                        dest='enable_stderr_filtering',
                        default=True,
                        help='Disable STDERR filtering, which can have unexpected effects on command directly '
                             'using tty.')

        for group in FILTER_GROUPS:
            option_group = OptionGroup(self, group.name, group.help)
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
            self.add_option_group(option_group)

    def parse_args(self, args=None, values=None):

        try:
            (values, remaining_args) = OptionParser.parse_args(self, args=args)
        except SystemExit:
            return self.command

        if remaining_args:

            if not self.stdout_builder.transformers:
                self.config_loader.load_config_from_command_line(remaining_args)

            stdout_transformer = self.stdout_builder.build()
            stderr_transformer = self.stderr_builder.build() if values.enable_stderr_filtering else IdentityTransformer

            return ExecuteCommand(remaining_args, stdout_transformer, stderr_transformer)

        return STDINCommand(self.stdout_builder.build())

    def _process_args(self, largs, rargs, values):
        while rargs:
            remaining = len(rargs)
            try:
                OptionParser._process_args(self, largs, rargs, values)
                if remaining == len(rargs):
                    break
            except (BadOptionError, AmbiguousOptionError) as e:
                largs.append(e.opt_str)

    def exit(self, status=0, msg=None):
        if msg:
            self.error_handler(msg)
        sys.exit(status)

    def error(self, msg):
        self.exit(1, msg)

    def handle_config_option(self, option, opt, value, parser):
        self.config_loader.load_config_by_name(value)

    def handle_pattern_option(self, option, opt, value, parser):
        filter_name = option.get_opt_string()[2:]
        filter = FILTERS_BY_LONG_OPTION[filter_name]
        self.stdout_builder.add_mapping(value, filter)
        self.stderr_builder.add_mapping(value, filter)

    @staticmethod
    def handle_verbosity_option(option, opt, value, parser):
        LOGGER.setLevel(LOGGER.level - 10)

    def handle_print_path_option(self, option, opt, value, parser):
        self.command = PrintPathCommand(DEFAULT_PATH)
        parser.exit(0)

    def handle_print_config_names_option(self, option, opt, value, parser):
        self.command = PrintConfigNamesCommand(DEFAULT_PATH)
        parser.exit(0)

    def print_help(self, file=None):
        self.command = NoOpCommand()
        return OptionParser.print_help(self, file)

    def print_version(self, file=None):
        self.command = NoOpCommand()
        return OptionParser.print_version(self, file)
