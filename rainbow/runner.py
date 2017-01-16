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

import subprocess
import sys


class Runner:
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError()


class CommandLineRunner(Runner):
    def __init__(self, args, stdout_colorizer, stderr_colorizer):
        Runner.__init__(self)
        self.args = args
        self.stdout_colorizer = stdout_colorizer
        self.stderr_colorizer = stderr_colorizer

    def run(self):
        p = subprocess.Popen(args=self.args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        try:
            for line in iter(p.stdout.readline, b''):
                print(self.stdout_colorizer.colorize(line[:-1].decode()))

                # TODO
                # stdout = p.stdout
                # stderr = p.stderr
                # stdout_fileno = stdout.fileno()
                # stderr_fileno = stderr.fileno()
                # while True:
                #    for fd in select.select([stdout_fileno, stderr_fileno], [], [])[0]:
                #        if fd == stdout_fileno:
                #            colorizer = self.stdout_colorizer
                #            line = stdout.readline()
                #        else:
                #            colorizer = self.stderr_colorizer
                #            line = stderr.readline()
                #        print(colorizer.colorize(line[:-1].decode()))
                #    if p.poll() is not None:
                #        break

        except KeyboardInterrupt:
            return 1
        return p.wait()


class STDINRunner(Runner):
    def __init__(self, colorizer):
        Runner.__init__(self)
        self.colorizer = colorizer

    def run(self):
        input_ = raw_input if sys.version_info[0] < 3 else input
        try:
            while True:
                print(self.colorizer.colorize(input_()))
        except EOFError:
            return 0
        except KeyboardInterrupt:
            return 1
