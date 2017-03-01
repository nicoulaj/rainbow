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

import os
import signal
import subprocess
import sys

from .ansi import ANSI_RESET_ALL
from .transformer import IdentityTransformer


class CommandRunner:
    def __init__(self, args, stdout_transformer=IdentityTransformer(), stderr_transformer=IdentityTransformer()):
        self.args = args
        self.stdout_transformer = stdout_transformer
        self.stderr_transformer = stderr_transformer

    # TODO stderr handling not implemented
    def run(self):
        p = subprocess.Popen(args=self.args, stdout=subprocess.PIPE)
        try:
            for line in iter(p.stdout.readline, b''):
                print(self.stdout_transformer.transform(line[:-1].decode()))
        except KeyboardInterrupt:
            os.kill(p.pid, signal.SIGINT)
        finally:
            sys.stdout.write(ANSI_RESET_ALL)
            sys.stderr.write(ANSI_RESET_ALL)
            sys.stdout.flush()
            sys.stderr.flush()
        return p.wait()


class STDINRunner:
    def __init__(self,
                 transformer=IdentityTransformer(),
                 input_=raw_input if sys.version_info[0] < 3 else input):  # noqa: F821
        self.transformer = transformer
        self.input_ = input_

    def run(self):
        try:
            while True:
                print(self.transformer.transform(self.input_()))
        except KeyboardInterrupt:
            return 1
        except EOFError:
            return 0
        finally:
            sys.stdout.write(ANSI_RESET_ALL)
            sys.stdout.flush()
