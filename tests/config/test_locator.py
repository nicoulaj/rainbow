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

from rainbow.config.locator import ConfigLocator


def test_locate_config_file_empty_path():
    assert ConfigLocator([]).locate_config_file("tests/data/cfg/config001") == "tests/data/cfg/config001.cfg"


def test_locate_inexistent_config_file_empty_path():
    assert not ConfigLocator([]).locate_config_file("does_not_exist")


def test_locate_config_file_none_in_path():
    assert ConfigLocator([None]).locate_config_file("tests/data/cfg/config001") == "tests/data/cfg/config001.cfg"


def test_locate_inexistent_config_file_none_in_path():
    assert not ConfigLocator([None]).locate_config_file("does_not_exist")


def test_locate_config_file_path_without_extension():
    assert ConfigLocator().locate_config_file("tests/data/cfg/config001") == "tests/data/cfg/config001.cfg"


def test_locate_config_file_path():
    assert ConfigLocator().locate_config_file("tests/data/cfg/config001.cfg") == "tests/data/cfg/config001.cfg"


def test_locate_config_file_filename():
    assert ConfigLocator(['tests/data/cfg']).locate_config_file("config001.cfg") == "tests/data/cfg/config001.cfg"


def test_locate_config_file_filename_without_extension():
    assert ConfigLocator(['tests/data/cfg']).locate_config_file("config001") == "tests/data/cfg/config001.cfg"


def test_locate_config_file_in_directory_filename():
    assert ConfigLocator().locate_config_file_in_directory('tests/data/cfg',
                                                           "config001.cfg") == "tests/data/cfg/config001.cfg"


def test_locate_config_file_in_directory_filename_without_extension():
    assert ConfigLocator().locate_config_file_in_directory('tests/data/cfg',
                                                           "config001") == "tests/data/cfg/config001.cfg"
