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


import codecs
import os
import sys

from rainbow.ansi import ANSI_RESET_ALL
from rainbow.transformer import IdentityTransformer


class STDINCommand(object):
    def __init__(self,
                 transformer=IdentityTransformer(),
                 encoding=sys.getdefaultencoding()):
        self.transformer = transformer
        self.encoding = encoding

    def run(self):

        stdin_fd = sys.stdin.fileno()
        stdout_fd = sys.stdout.fileno()

        reader = codecs.getreader(self.encoding)(os.fdopen(stdin_fd, 'rb'), errors='replace')
        try:
            while True:
                line = reader.readline()
                if line:
                    os.write(stdout_fd, self.transformer.transform(line).encode(self.encoding, 'replace'))
                else:
                    return 0
        except KeyboardInterrupt:
            return 1
        finally:
            os.write(stdout_fd, ANSI_RESET_ALL.encode(self.encoding, 'replace'))
