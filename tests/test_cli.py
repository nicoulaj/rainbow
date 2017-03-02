# ----------------------------------------------------------------------
# rainbow, a command line colorizer
# Copyright (C) 2011-2017 Julien Nicoulaud <julien.nicoulaud@gmail.com>
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

from rainbow import LOGGER
from rainbow.cli import CommandLineParser
from rainbow.filter import FILTERS_BY_NAME
from rainbow.transformer import TransformerBuilder
from .test_utils import FILTERS_WITH_SHORT_OPTION, FILTERS_WITH_LONG_OPTION


def parse(args):
    errors = []

    (command, stdout, stderr) = CommandLineParser(
        paths=None,
        error_handler=lambda error: errors.append(error)
    ).parse(args)

    return command, stdout, stderr, errors


@pytest.mark.parametrize("filter", FILTERS_WITH_SHORT_OPTION, ids=str)
def test_filter_short_option(filter):
    (command, stdout_transformer, stderr_transformer, errors) = parse(['-' + filter.short_option, 'test'])
    assert not errors
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert stdout_transformer == transformer
    assert stderr_transformer == transformer


@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
def test_filter_long_option(filter):
    (command, stdout_transformer, stderr_transformer, errors) = parse(['--' + filter.long_option, 'test'])
    assert not errors
    transformer = TransformerBuilder.make_transformer(re.compile('test'), filter)
    assert stdout_transformer == transformer
    assert stderr_transformer == transformer


def test_unresolvable_config_file_short_option():
    (command, stdout_transformer, stderr_transformer, errors) = parse(['-f', 'does_not_exist'])
    assert errors == ['Could not resolve config "does_not_exist"']


def test_unresolvable_config_file_long_option():
    (command, stdout_transformer, stderr_transformer, errors) = parse(['--config', 'does_not_exist'])
    assert errors == ['Could not resolve config "does_not_exist"']


def test_config_file_by_relative_path_short_option():
    (command, stdout_transformer, stderr_transformer, errors) = parse(['-f', 'tests/configs/config006.cfg'])
    assert not errors
    transformer = TransformerBuilder.make_transformer(re.compile(u'ERROR'), FILTERS_BY_NAME['foreground-red'])
    assert stdout_transformer == transformer
    assert stderr_transformer == transformer


def test_config_file_by_relative_path_without_extension_short_option():
    (command, stdout_transformer, stderr_transformer, errors) = parse(['-f', 'tests/configs/config006'])
    assert not errors
    transformer = TransformerBuilder.make_transformer(re.compile(u'ERROR'), FILTERS_BY_NAME['foreground-red'])
    assert stdout_transformer == transformer
    assert stderr_transformer == transformer


def test_config_file_by_relative_path_long_option():
    (command, stdout_transformer, stderr_transformer, errors) = parse(['--config', 'tests/configs/config006.cfg'])
    assert not errors
    transformer = TransformerBuilder.make_transformer(re.compile(u'ERROR'), FILTERS_BY_NAME['foreground-red'])
    assert stdout_transformer == transformer
    assert stderr_transformer == transformer


def test_config_file_by_relative_path_without_extension_long_option():
    (command, stdout_transformer, stderr_transformer, errors) = parse(['--config', 'tests/configs/config006'])
    assert not errors
    transformer = TransformerBuilder.make_transformer(re.compile(u'ERROR'), FILTERS_BY_NAME['foreground-red'])
    assert stdout_transformer == transformer
    assert stderr_transformer == transformer


def test_verbose_short_option():
    level = LOGGER.level
    try:
        (command, stdout_transformer, stderr_transformer, errors) = parse(['-v'])
        assert not errors
        assert LOGGER.level == level - 10
    finally:
        LOGGER.setLevel(level)


def test_verbose_long_option():
    level = LOGGER.level
    try:
        (command, stdout_transformer, stderr_transformer, errors) = parse(['--verbose'])
        assert not errors
        assert LOGGER.level == level - 10
    finally:
        LOGGER.setLevel(level)


def test_verbose_twice_short_option():
    level = LOGGER.level
    try:
        (command, stdout_transformer, stderr_transformer, errors) = parse(['-vv'])
        assert not errors
        assert LOGGER.level == level - 20
    finally:
        LOGGER.setLevel(level)


def test_verbose_twice_long_option():
    level = LOGGER.level
    try:
        (command, stdout_transformer, stderr_transformer, errors) = parse(['--verbose', '--verbose'])
        assert not errors
        assert LOGGER.level == level - 20
    finally:
        LOGGER.setLevel(level)
