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
import re
import signal
import subprocess
import sys
from select import select

from rainbow.ansi import ANSI_RESET_ALL
from rainbow.transformer import IdentityTransformer

NEW_LINE = re.compile("\n|\r\n")


class ExecuteCommand(object):
    def __init__(self, args, stdout_transformer=IdentityTransformer(), stderr_transformer=IdentityTransformer()):
        self.args = args
        self.stdout_transformer = stdout_transformer
        self.stderr_transformer = stderr_transformer

    def run(self):
        stdin_fd = sys.stdin.fileno()
        in_master, in_slave = pty.openpty() if sys.stdin.isatty() else os.pipe()
        out_master, out_slave = pty.openpty() if sys.stdout.isatty() else os.pipe()
        err_master, err_slave = pty.openpty() if sys.stderr.isatty() else os.pipe()
        p = subprocess.Popen(args=self.args, stdin=in_master, stdout=out_slave, stderr=err_slave)
        try:
            os.close(out_slave)
            os.close(err_slave)
            readables = [stdin_fd, out_master, err_master]
            writables = {stdin_fd: os.fdopen(in_slave, 'w'), out_master: sys.stdout, err_master: sys.stderr}
            buffers = {out_master: '', err_master: ''}
            transformers = {out_master: self.stdout_transformer, err_master: self.stderr_transformer}
            while True:
                for fd in select(readables, [], [])[0]:
                    try:
                        data = os.read(fd, 4096)
                    except OSError as e:
                        if e.errno != errno.EIO:
                            raise  # no cover
                        data = None
                    writable = writables[fd]
                    if data:
                        data_str = data.decode()
                        if fd == stdin_fd:
                            writable.write(data_str)
                            for fd in buffers:
                                buffers[fd] = ''
                        else:
                            lines = NEW_LINE.split(buffers[fd] + data_str)
                            transformer = transformers[fd]
                            if lines[0] and buffers[fd]:
                                writable.write('\r')
                            for line in lines[:-1]:
                                writable.write(transformer.transform(line) + '\n')
                            if lines[-1]:
                                writable.write(transformer.transform(lines[-1]))
                                buffers[fd] = lines[-1]
                            else:
                                buffers[fd] = ''
                            writable.flush()
                    else:
                        if fd == stdin_fd:
                            writable.close()
                        else:
                            writable.write(ANSI_RESET_ALL)
                            writable.flush()
                            os.close(fd)
                        readables.remove(fd)
                        if out_master not in readables and err_master not in readables:
                            return p.wait()
        except KeyboardInterrupt:
            os.kill(p.pid, signal.SIGINT)
        return p.wait()
