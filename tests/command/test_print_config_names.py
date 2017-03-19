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

from rainbow import DEFAULT_PATH
from rainbow.command.print_config_names import PrintConfigNamesCommand


def test_empty_path(capsys):
    assert PrintConfigNamesCommand().run() == 0
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


def test_default_path(capsys):
    assert PrintConfigNamesCommand(DEFAULT_PATH).run() == 0
    out, err = capsys.readouterr()
    assert 'diff\n' in out
    assert 'ping' in out
    assert 'md5sum' in out
    assert 'env' in out
    assert 'java-stack-trace' in out
    assert 'host' in out
    assert 'ifconfig' in out
    assert 'traceroute' in out
    assert 'df' in out
    assert 'mvn' in out
    assert 'tomcat' in out
    assert err == ''
