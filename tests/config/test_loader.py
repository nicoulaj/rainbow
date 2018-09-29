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

import pytest

from rainbow.config.loader import ConfigLoader, PRECOMMANDS
from rainbow.transformer import IdentityTransformer
from rainbow.transformer import TransformerBuilder


def load_by_name(config):
    stdout_builder = TransformerBuilder()
    stderr_builder = TransformerBuilder()
    errors = []

    ConfigLoader(stdout_builder=stdout_builder,
                 stderr_builder=stderr_builder,
                 paths=['tests/data/cfg'],
                 error_handler=errors.append) \
        .load_config_by_name(config)

    return stdout_builder.build(), stderr_builder.build(), errors


def load_from_command_line(args):
    stdout_builder = TransformerBuilder()
    stderr_builder = TransformerBuilder()
    errors = []

    ConfigLoader(stdout_builder=stdout_builder,
                 stderr_builder=stderr_builder,
                 paths=['tests/data/cfg'],
                 error_handler=errors.append) \
        .load_config_from_command_line(args)

    return stdout_builder.build(), stderr_builder.build(), errors


def test_load_unresolvable_config_file():
    (stdout_transformer, stderr_transformer, errors) = load_by_name('does_not_exist')
    assert errors == ['Could not resolve config "does_not_exist"']


def test_load_empty_config_file():
    (stdout_transformer, stderr_transformer, errors) = load_by_name('tests/data/cfg/config001.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_empty_config_file_from_command_line():
    (stdout_transformer, stderr_transformer, errors) = load_from_command_line(['config001'])
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_find_config_name_from_command_line_empty_args():
    assert not ConfigLoader.find_config_name_from_command_line([])


def test_find_config_name_from_command_line_one_arg():
    assert ConfigLoader.find_config_name_from_command_line(['foo']) == 'foo'


def test_find_config_name_from_command_line_several_args():
    assert ConfigLoader.find_config_name_from_command_line(['foo', 'bar', 'bar']) == 'foo'


def test_find_config_name_from_command_line_full_path():
    assert ConfigLoader.find_config_name_from_command_line(['/usr/bin/foo']) == 'foo'


@pytest.mark.parametrize("precommand", PRECOMMANDS)
def test_find_config_name_from_command_line_precommand(precommand):
    assert ConfigLoader.find_config_name_from_command_line([precommand, 'foo']) == 'foo'


@pytest.mark.parametrize("precommand", PRECOMMANDS)
def test_find_config_name_from_command_line_precommand_with_args(precommand):
    assert ConfigLoader.find_config_name_from_command_line([precommand, '--arg', 'foo']) == 'foo'


@pytest.mark.parametrize("precommand", PRECOMMANDS)
def test_find_config_name_from_command_line_full_path_precommand(precommand):
    assert ConfigLoader.find_config_name_from_command_line([precommand, '/usr/bin/foo']) == 'foo'


@pytest.mark.parametrize("precommand", PRECOMMANDS)
def test_find_config_name_from_command_line_full_path_precommand_with_args(precommand):
    assert ConfigLoader.find_config_name_from_command_line([precommand, '--arg', '/usr/bin/foo']) == 'foo'
