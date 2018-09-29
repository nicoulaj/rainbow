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
import logging
from logging import Formatter

import rainbow
from . import LOGGER, DEFAULT_PATH
from .cli import CommandLineParser
from .transformer import DummyTransformerBuilder


def main(args=None):
    logger_console_handler = logging.StreamHandler(sys.stderr)
    try:
        logger_console_handler.setFormatter(Formatter("%(levelname)s %(message)s"))
        logging.addLevelName(logging.CRITICAL, 'rainbow error:')
        logging.addLevelName(logging.FATAL, 'rainbow error:')
        logging.addLevelName(logging.ERROR, 'rainbow error:')
        logging.addLevelName(logging.WARNING, 'rainbow warning:')
        logging.addLevelName(logging.INFO, 'rainbow:')
        logging.addLevelName(logging.DEBUG, 'rainbow:')
        logging.addLevelName(logging.NOTSET, 'rainbow:')
        LOGGER.addHandler(logger_console_handler)
        LOGGER.setLevel(logging.WARNING)

        errors = []

        parser = CommandLineParser(
            paths=DEFAULT_PATH,
            stdout_builder=None if rainbow.ENABLE_STDOUT else DummyTransformerBuilder(),
            stderr_builder=None if rainbow.ENABLE_STDERR else DummyTransformerBuilder(),
            error_handler=errors.append
        )

        command = parser.parse_args(args)

        if command:
            for message in errors:
                LOGGER.warning(message)
            return command.run()

        else:
            for message in errors:
                LOGGER.error(message)
            LOGGER.setLevel(logging.INFO)
            LOGGER.info(parser.get_usage())
            return 1

    except Exception as e:
        LOGGER.exception(e)
        return 1
    finally:
        LOGGER.removeHandler(logger_console_handler)
        LOGGER.setLevel(logging.INFO)
