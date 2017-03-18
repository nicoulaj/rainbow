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


import sys

from rainbow.ansi import ANSI_RESET_ALL
from rainbow.transformer import IdentityTransformer


class STDINCommand(object):
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
