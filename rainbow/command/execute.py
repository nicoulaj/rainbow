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
    def __init__(self,
                 args,
                 stdout_transformer=IdentityTransformer(),
                 stderr_transformer=IdentityTransformer(),
                 encoding=sys.getdefaultencoding()):
        self.args = args
        self.stdout_transformer = stdout_transformer
        self.stderr_transformer = stderr_transformer
        self.encoding = encoding

    def encode(self, string):
        return string.encode(self.encoding, 'replace')

    def decode(self, bytes):
        return bytes.decode(self.encoding, 'replace')

    def run(self):

        stdin_fd = sys.stdin.fileno()
        stdout_fd = sys.stdout.fileno()
        stderr_fd = sys.stderr.fileno()

        in_master, in_slave = pty.openpty() if sys.stdin.isatty() else os.pipe()
        out_master, out_slave = pty.openpty() if sys.stdout.isatty() else os.pipe()
        err_master, err_slave = pty.openpty() if sys.stderr.isatty() else os.pipe()

        p = subprocess.Popen(args=self.args, stdin=in_master, stdout=out_slave, stderr=err_slave)

        readables = [stdin_fd, out_master, err_master]
        writables = {stdin_fd: in_slave, out_master: stdout_fd, err_master: stderr_fd}
        buffers = {out_master: '', err_master: ''}
        transformers = {out_master: self.stdout_transformer, err_master: self.stderr_transformer}

        try:
            os.close(out_slave)
            os.close(err_slave)
            while True:
                for read_fd in select(readables, [], [])[0]:
                    try:
                        data = os.read(read_fd, 4096)
                    except OSError as e:
                        if e.errno != errno.EIO:
                            raise  # no cover
                        data = None
                    write_fd = writables[read_fd]
                    if data:
                        data_str = self.decode(data)
                        if read_fd == stdin_fd:
                            os.write(write_fd, self.encode(data_str))
                            for read_fd in buffers:
                                buffers[read_fd] = ''
                        else:
                            lines = NEW_LINE.split(buffers[read_fd] + data_str)
                            transformer = transformers[read_fd]
                            if lines[0] and buffers[read_fd]:
                                os.write(write_fd, self.encode('\r'))
                            for line in lines[:-1]:
                                os.write(write_fd, self.encode(transformer.transform(line) + '\n'))
                            if lines[-1]:
                                os.write(write_fd, self.encode(transformer.transform(lines[-1])))
                                buffers[read_fd] = lines[-1]
                            else:
                                buffers[read_fd] = ''
                    else:
                        if read_fd == stdin_fd:
                            os.close(write_fd)
                        else:
                            os.write(write_fd, self.encode(ANSI_RESET_ALL))
                            os.close(read_fd)
                        readables.remove(read_fd)
                        if out_master not in readables and err_master not in readables:
                            return p.wait()
        except KeyboardInterrupt:
            os.kill(p.pid, signal.SIGINT)
        return p.wait()
