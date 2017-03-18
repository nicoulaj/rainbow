# ----------------------------------------------------------------------
# rainbow, a terminal colorizer - https://github.com/nicoulaj/rainbow
# copyright (c) 2010-2017 rainbow contributors
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

import errno
import os
import pty
import signal
import subprocess
import sys
from select import select

from rainbow.ansi import ANSI_RESET_ALL
from rainbow.transformer import IdentityTransformer


class ExecuteCommand(object):
    def __init__(self, args, stdout_transformer=IdentityTransformer(), stderr_transformer=IdentityTransformer()):
        self.args = args
        self.stdout_transformer = stdout_transformer
        self.stderr_transformer = stderr_transformer

    def run(self):
        masters, slaves = zip(pty.openpty(), pty.openpty())
        p = subprocess.Popen(args=self.args, stdin=sys.stdin, stdout=slaves[0], stderr=slaves[1])
        try:
            for fd in slaves:
                os.close(fd)
            readables = {masters[0]: sys.stdout, masters[1]: sys.stderr}
            buffers = {masters[0]: '', masters[1]: ''}
            transformers = {masters[0]: self.stdout_transformer, masters[1]: self.stderr_transformer}
            while readables:
                for fd in select(readables, [], [])[0]:
                    try:
                        data = os.read(fd, 64)
                    except OSError as e:
                        if e.errno != errno.EIO:
                            raise  # no cover
                        data = None
                    readable = readables[fd]
                    transformer = transformers[fd]
                    if data:
                        buffers[fd] += data.decode()
                        lines = buffers[fd].splitlines()
                        if len(lines) > 0:
                            for line in lines[:-1]:
                                readable.write(transformer.transform(line) + '\n')
                            if buffers[fd][-1] == '\n':
                                readable.write(transformer.transform(lines[-1]) + '\n')
                                buffers[fd] = ''
                            else:
                                buffers[fd] = lines[-1]
                            readable.flush()
                    else:
                        for line in buffers[fd].splitlines():
                            readable.write(transformer.transform(line) + '\n')
                        readable.write(ANSI_RESET_ALL)
                        readable.flush()
                        del readables[fd]
            for fd in masters:
                os.close(fd)
        except KeyboardInterrupt:
            os.kill(p.pid, signal.SIGINT)
        return p.wait()
