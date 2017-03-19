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

import pytest

from rainbow.command.noop import NoOpCommand


def test_noop(capsys):
    assert NoOpCommand().run() == 0
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


@pytest.mark.parametrize("exit_code", range(-256, 256), ids=str)
def test_noop_with_exit_code(capsys, exit_code):
    assert NoOpCommand(exit_code).run() == exit_code
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''
