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

import sys

from . import *
from .ansi import ANSI_RESET_ALL
from .cli import CommandLineParser
from .runner import CommandLineRunner, STDINRunner


def main(args=None):
    logger_console_handler = logging.StreamHandler()
    logger_formatter = logging.Formatter("[%(name)s|%(levelname)s] %(message)s")
    logger_console_handler.setFormatter(logger_formatter)
    LOGGER.addHandler(logger_console_handler)
    LOGGER.setLevel(logging.WARNING)

    try:

        (command, stdout_transformer, stderr_transformer) = CommandLineParser([os.path.curdir,
                                                                               USER_CONFIGS_HOME,
                                                                               RAINBOW_CONFIGS_HOME]).parse(args)

        if command:
            LOGGER.info("Will run command '%s'." % command)
            runner = CommandLineRunner(command, stdout_transformer, stderr_transformer)

        else:
            LOGGER.info("No arguments given, using STDIN as input.")
            runner = STDINRunner(stdout_transformer)

        return runner.run()

    except Exception as e:
        LOGGER.exception(e)
        return 1
    finally:
        sys.stdout.write(ANSI_RESET_ALL)
        sys.stderr.write(ANSI_RESET_ALL)
        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == "__main__":
    sys.exit(main())
