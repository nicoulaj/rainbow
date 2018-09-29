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

import os

from rainbow import DEFAULT_PATH
from rainbow.command.print_path import PrintPathCommand


def test_empty_path(capsys):
    assert PrintPathCommand().run() == 0
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


def test_default_path(capsys):
    assert PrintPathCommand(DEFAULT_PATH).run() == 0
    out, err = capsys.readouterr()
    assert os.path.expanduser('~/.rainbow') in out
    assert os.path.join(os.sep, 'etc', 'rainbow') in out
    assert os.path.join(os.sep, 'rainbow', 'config', 'builtin') in out
