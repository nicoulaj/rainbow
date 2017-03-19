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

import re

import pytest

from rainbow import LOGGER, DEFAULT_PATH
from rainbow.cli import CommandLineParser
from rainbow.command.execute import ExecuteCommand
from rainbow.command.noop import NoOpCommand
from rainbow.command.print_config_names import PrintConfigNamesCommand
from rainbow.command.print_path import PrintPathCommand
from rainbow.command.stdin import STDINCommand
from rainbow.filter import FILTERS_BY_NAME
from rainbow.transformer import TransformerBuilder, DummyTransformerBuilder, IdentityTransformer
from .test_utils import FILTERS_WITH_SHORT_OPTION, FILTERS_WITH_LONG_OPTION


def parse(args, stdout_builder=None, stderr_builder=None):
    errors = []

    command = CommandLineParser(
        paths=None,
        stdout_builder=stdout_builder,
        stderr_builder=stderr_builder,
        error_handler=lambda error: errors.append(error)
    ).parse_args(args)

    return command, errors


def test_empty_args():
    (command, errors) = parse([])
    assert not errors
    assert isinstance(command, STDINCommand)
    assert command.transformer == IdentityTransformer()


@pytest.mark.parametrize("filter", FILTERS_WITH_SHORT_OPTION, ids=str)
def test_filter_short_option(filter):
    (command, errors) = parse(['-' + filter.short_option, 'test'])
    assert not errors
    assert isinstance(command, STDINCommand)
    assert command.transformer == TransformerBuilder.make_transformer(re.compile('test'), filter)


@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
def test_filter_long_option(filter):
    (command, errors) = parse(['--' + filter.long_option, 'test'])
    assert not errors
    assert isinstance(command, STDINCommand)
    assert command.transformer == TransformerBuilder.make_transformer(re.compile('test'), filter)


@pytest.mark.parametrize("filter", FILTERS_WITH_SHORT_OPTION, ids=str)
def test_filter_short_option_without_value(filter):
    (command, errors) = parse(['-' + filter.short_option])
    assert len(errors) == 1
    assert re.match(r'%s option requires (an|1) argument' % ('-' + filter.short_option), errors[0])
    assert not command


@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
def test_filter_long_option_without_value(filter):
    (command, errors) = parse(['--' + filter.long_option])
    assert len(errors) == 1
    assert re.match(r'%s option requires (an|1) argument' % ('--' + filter.long_option), errors[0])
    assert not command


def test_command():
    (command, errors) = parse(['true'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_command_remaining_args_separator():
    (command, errors) = parse(['--', 'true'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_command_with_option():
    (command, errors) = parse(['true', '--option'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true', '--option']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_command_with_option_remaining_args_separator():
    (command, errors) = parse(['--', 'true', '--option'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true', '--option']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_command_that_looks_like_a_short_option():
    (command, errors) = parse(['-a'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['-a']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_command_that_looks_like_a_short_option_remaining_args_separator():
    (command, errors) = parse(['--', '-a'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['-a']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_command_that_looks_like_a_long_option():
    (command, errors) = parse(['--true'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['--true']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_command_that_looks_like_a_long_option_remaining_args_separator():
    (command, errors) = parse(['--', '--true'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['--true']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
def test_command_with_long_option_filter(filter):
    (command, errors) = parse(['--' + filter.long_option, 'test', 'true'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true']
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert command.stdout_transformer == transformer
    assert command.stderr_transformer == transformer


@pytest.mark.parametrize("filter", FILTERS_WITH_SHORT_OPTION, ids=str)
def test_command_with_short_option_filter(filter):
    (command, errors) = parse(['-' + filter.short_option, 'test', 'true'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true']
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert command.stdout_transformer == transformer
    assert command.stderr_transformer == transformer


@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
def test_command_remaining_args_separator_with_long_option_filter(filter):
    (command, errors) = parse(['--' + filter.long_option, 'test', '--', 'true'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true']
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert command.stdout_transformer == transformer
    assert command.stderr_transformer == transformer


@pytest.mark.parametrize("filter", FILTERS_WITH_SHORT_OPTION, ids=str)
def test_command_remaining_args_separator_with_short_option_filter(filter):
    (command, errors) = parse(['-' + filter.short_option, 'test', '--', 'true'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true']
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert command.stdout_transformer == transformer
    assert command.stderr_transformer == transformer


@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
def test_command_with_option_with_long_option_filter(filter):
    (command, errors) = parse(['--' + filter.long_option, 'test', 'true', '--option'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true', '--option']
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert command.stdout_transformer == transformer
    assert command.stderr_transformer == transformer


@pytest.mark.parametrize("filter", FILTERS_WITH_SHORT_OPTION, ids=str)
def test_command_with_option_with_short_option_filter(filter):
    (command, errors) = parse(['-' + filter.short_option, 'test', 'true', '--option'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true', '--option']
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert command.stdout_transformer == transformer
    assert command.stderr_transformer == transformer


@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
def test_command_with_option_remaining_args_separator_with_long_option_filter(filter):
    (command, errors) = parse(['--' + filter.long_option, 'test', '--', 'true', '--option'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true', '--option']
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert command.stdout_transformer == transformer
    assert command.stderr_transformer == transformer


@pytest.mark.parametrize("filter", FILTERS_WITH_SHORT_OPTION, ids=str)
def test_command_with_option_remaining_args_separator_with_short_option_filter(filter):
    (command, errors) = parse(['-' + filter.short_option, 'test', '--', 'true', '--option'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true', '--option']
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert command.stdout_transformer == transformer
    assert command.stderr_transformer == transformer


def test_command_with_same_option_as_rainbow():
    (command, errors) = parse(['command', '--red', 'test'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['command', '--red', 'test']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_command_with_same_option_as_rainbow_remaining_args_separator():
    (command, errors) = parse(['command', '--red', 'test'])
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['command', '--red', 'test']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_unresolvable_config_file_short_option():
    (command, errors) = parse(['-f', 'does_not_exist'])
    assert errors == ['Could not resolve config "does_not_exist"']
    assert isinstance(command, STDINCommand)


def test_unresolvable_config_file_long_option():
    (command, errors) = parse(['--config', 'does_not_exist'])
    assert errors == ['Could not resolve config "does_not_exist"']
    assert isinstance(command, STDINCommand)


def test_config_file_by_relative_path_short_option():
    (command, errors) = parse(['-f', 'tests/configs/config006.cfg'])
    assert not errors
    assert isinstance(command, STDINCommand)
    assert command.transformer == TransformerBuilder.make_transformer(re.compile(u'ERROR'),
                                                                      FILTERS_BY_NAME['foreground-red'])


def test_config_file_by_relative_path_without_extension_short_option():
    (command, errors) = parse(['-f', 'tests/configs/config006'])
    assert not errors
    assert isinstance(command, STDINCommand)
    assert command.transformer == TransformerBuilder.make_transformer(re.compile(u'ERROR'),
                                                                      FILTERS_BY_NAME['foreground-red'])


def test_config_file_by_relative_path_long_option():
    (command, errors) = parse(['--config', 'tests/configs/config006.cfg'])
    assert not errors
    assert isinstance(command, STDINCommand)
    assert command.transformer == TransformerBuilder.make_transformer(re.compile(u'ERROR'),
                                                                      FILTERS_BY_NAME['foreground-red'])


def test_config_file_by_relative_path_without_extension_long_option():
    (command, errors) = parse(['--config', 'tests/configs/config006'])
    assert not errors
    assert isinstance(command, STDINCommand)
    assert command.transformer == TransformerBuilder.make_transformer(re.compile(u'ERROR'),
                                                                      FILTERS_BY_NAME['foreground-red'])


def test_dummy_transfomer_builder():
    (command, errors) = parse(['true'],
                              stdout_builder=DummyTransformerBuilder(),
                              stderr_builder=DummyTransformerBuilder())
    assert not errors
    assert isinstance(command, ExecuteCommand)
    assert command.args == ['true']
    assert command.stdout_transformer == IdentityTransformer()
    assert command.stderr_transformer == IdentityTransformer()


def test_verbose_short_option():
    level = LOGGER.level
    try:
        (command, errors) = parse(['-v'])
        assert not errors
        assert isinstance(command, STDINCommand)
        assert LOGGER.level == level - 10
    finally:
        LOGGER.setLevel(level)


def test_verbose_long_option():
    level = LOGGER.level
    try:
        (command, errors) = parse(['--verbose'])
        assert not errors
        assert isinstance(command, STDINCommand)
        assert LOGGER.level == level - 10
    finally:
        LOGGER.setLevel(level)


def test_verbose_twice_short_option():
    level = LOGGER.level
    try:
        (command, errors) = parse(['-vv'])
        assert not errors
        assert isinstance(command, STDINCommand)
        assert LOGGER.level == level - 20
    finally:
        LOGGER.setLevel(level)


def test_verbose_twice_long_option():
    level = LOGGER.level
    try:
        (command, errors) = parse(['--verbose', '--verbose'])
        assert not errors
        assert isinstance(command, STDINCommand)
        assert LOGGER.level == level - 20
    finally:
        LOGGER.setLevel(level)


def test_print_path():
    (command, errors) = parse(['--print-path'])
    assert not errors
    assert isinstance(command, PrintPathCommand)
    assert command.paths == DEFAULT_PATH


def test_print_path_with_extra_args():
    (command, errors) = parse(['--print-path', 'foo'])
    assert not errors
    assert isinstance(command, PrintPathCommand)
    assert command.paths == DEFAULT_PATH


def test_print_config_names():
    (command, errors) = parse(['--print-config-names'])
    assert not errors
    assert isinstance(command, PrintConfigNamesCommand)
    assert command.paths == DEFAULT_PATH


def test_print_config_names_with_extra_args():
    (command, errors) = parse(['--print-config-names', 'foo'])
    assert not errors
    assert isinstance(command, PrintConfigNamesCommand)
    assert command.paths == DEFAULT_PATH


def test_version():
    (command, errors) = parse(['--version', 'foo'])
    assert not errors
    assert isinstance(command, NoOpCommand)
    assert command.exit_code == 0


def test_help():
    (command, errors) = parse(['--help', 'foo'])
    assert not errors
    assert isinstance(command, NoOpCommand)
    assert command.exit_code == 0
