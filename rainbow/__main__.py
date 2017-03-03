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

import logging
import sys

from . import LOGGER, DEFAULT_PATH
from .cli import CommandLineParser
from .runner import CommandRunner, STDINRunner
from .transformer import IdentityTransformer


def main(args=None):
    logger_console_handler = logging.StreamHandler()
    logger_formatter = logging.Formatter("[%(name)s|%(levelname)s] %(message)s")
    logger_console_handler.setFormatter(logger_formatter)
    LOGGER.addHandler(logger_console_handler)
    LOGGER.setLevel(logging.WARNING)

    try:
        (command, stdout, stderr) = CommandLineParser(DEFAULT_PATH).parse(args)

        if not sys.stdout.isatty():
            stdout = IdentityTransformer()
        if not sys.stderr.isatty():
            stderr = IdentityTransformer()

        if command:
            LOGGER.info("Will run command '%s'." % command)
            runner = CommandRunner(command, stdout, stderr)

        else:
            LOGGER.info("No arguments given, using STDIN as input.")
            runner = STDINRunner(stdout)

        return runner.run()

    except Exception as e:  # no cover
        LOGGER.exception(e)
        return 1
