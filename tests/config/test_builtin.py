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

import pytest

from rainbow.ansi import ANSI_BACKGROUND_BLUE, ANSI_BACKGROUND_CYAN, ANSI_BACKGROUND_GREEN, ANSI_BACKGROUND_MAGENTA, \
    ANSI_BACKGROUND_RED, ANSI_BACKGROUND_RESET, ANSI_BACKGROUND_YELLOW, ANSI_BLINK, ANSI_BLINK_RAPID, ANSI_BOLD, \
    ANSI_FAINT, ANSI_FOREGROUND_BLUE, ANSI_FOREGROUND_CYAN, ANSI_FOREGROUND_GREEN, ANSI_FOREGROUND_MAGENTA, \
    ANSI_FOREGROUND_RED, ANSI_FOREGROUND_RESET, ANSI_FOREGROUND_YELLOW, ANSI_HIDE, ANSI_ITALIC, ANSI_NEGATIVE, \
    ANSI_RESET_ALL, ANSI_RESET_BLINK, ANSI_RESET_HIDE, ANSI_RESET_INTENSITY, ANSI_RESET_ITALIC, ANSI_RESET_NEGATIVE, \
    ANSI_RESET_UNDERLINE, ANSI_UNDERLINE, ANSI_UNDERLINE_DOUBLE
from rainbow.config.loader import ConfigLoader
from rainbow.transformer import DummyTransformerBuilder, TransformerBuilder, ListTransformer, ReplaceTransformer
from tests.test_utils import BUILTIN_CONFIGS_NAMES, BUILTIN_CONFIGS_REFERENCES, BUILTIN_CONFIGS_REFERENCE_PAIRS

# Use this to update references.
# NEVER commit it with True!
GENERATE_REFERENCES = False


def load_builtin_config(config):
    stdout_builder = TransformerBuilder()
    errors = []
    ConfigLoader(stdout_builder=stdout_builder,
                 stderr_builder=DummyTransformerBuilder(),
                 paths=['rainbow/config/builtin'],
                 error_handler=errors.append) \
        .load_config_by_name(config)
    return stdout_builder.build(), errors


def test_generate_flag_has_not_been_committed():
    assert not (bool(os.environ.get('CI', False)) and GENERATE_REFERENCES)


@pytest.mark.parametrize("config", BUILTIN_CONFIGS_NAMES)
def test_config_has_at_least_one_reference(config):
    assert len(BUILTIN_CONFIGS_REFERENCES[config]) > 0


@pytest.mark.parametrize("config", BUILTIN_CONFIGS_NAMES)
def test_config_loads_without_errors(config):
    (transformer, errors) = load_builtin_config(config)
    assert not errors


@pytest.mark.parametrize("test", BUILTIN_CONFIGS_REFERENCE_PAIRS, ids=str)
def test_config_by_reference(test):
    config_name = test[0]
    input_file = test[1]
    expected_file = input_file + '.out'

    (transformer, errors) = load_builtin_config(config_name)
    assert not errors

    transformer = ListTransformer([
        transformer,
        ReplaceTransformer(ANSI_FOREGROUND_RED, '[FOREGROUND_RED]'),
        ReplaceTransformer(ANSI_FOREGROUND_GREEN, '[FOREGROUND_GREEN]'),
        ReplaceTransformer(ANSI_FOREGROUND_YELLOW, '[FOREGROUND_YELLOW]'),
        ReplaceTransformer(ANSI_FOREGROUND_BLUE, '[FOREGROUND_BLUE]'),
        ReplaceTransformer(ANSI_FOREGROUND_MAGENTA, '[FOREGROUND_MAGENTA]'),
        ReplaceTransformer(ANSI_FOREGROUND_CYAN, '[FOREGROUND_CYAN]'),
        ReplaceTransformer(ANSI_FOREGROUND_RESET, '[FOREGROUND_RESET]'),
        ReplaceTransformer(ANSI_BACKGROUND_RED, '[BACKGROUND_RED]'),
        ReplaceTransformer(ANSI_BACKGROUND_GREEN, '[BACKGROUND_GREEN]'),
        ReplaceTransformer(ANSI_BACKGROUND_YELLOW, '[BACKGROUND_YELLOW]'),
        ReplaceTransformer(ANSI_BACKGROUND_BLUE, '[BACKGROUND_BLUE]'),
        ReplaceTransformer(ANSI_BACKGROUND_MAGENTA, '[BACKGROUND_MAGENTA]'),
        ReplaceTransformer(ANSI_BACKGROUND_CYAN, '[BACKGROUND_CYAN]'),
        ReplaceTransformer(ANSI_BACKGROUND_RESET, '[BACKGROUND_RESET]'),
        ReplaceTransformer(ANSI_BOLD, '[BOLD]'),
        ReplaceTransformer(ANSI_FAINT, '[FAINT]'),
        ReplaceTransformer(ANSI_ITALIC, '[ITALIC]'),
        ReplaceTransformer(ANSI_UNDERLINE, '[UNDERLINE]'),
        ReplaceTransformer(ANSI_UNDERLINE_DOUBLE, '[UNDERLINE_DOUBLE]'),
        ReplaceTransformer(ANSI_BLINK, '[BLINK]'),
        ReplaceTransformer(ANSI_BLINK_RAPID, '[BLINK_RAPID]'),
        ReplaceTransformer(ANSI_NEGATIVE, '[NEGATIVE]'),
        ReplaceTransformer(ANSI_HIDE, '[HIDE]'),
        ReplaceTransformer(ANSI_RESET_INTENSITY, '[RESET_INTENSITY]'),
        ReplaceTransformer(ANSI_RESET_ITALIC, '[RESET_ITALIC]'),
        ReplaceTransformer(ANSI_RESET_UNDERLINE, '[RESET_UNDERLINE]'),
        ReplaceTransformer(ANSI_RESET_BLINK, '[RESET_BLINK]'),
        ReplaceTransformer(ANSI_RESET_NEGATIVE, '[RESET_NEGATIVE]'),
        ReplaceTransformer(ANSI_RESET_HIDE, '[RESET_HIDE]'),
        ReplaceTransformer(ANSI_RESET_ALL, '[RESET_ALL]')
    ])

    with open(input_file) as f:
        actual_lines = [transformer.transform(l) for l in f.read().splitlines()]

    if GENERATE_REFERENCES:
        with open(expected_file, 'w') as f:
            for line in actual_lines:
                f.write('%s\n' % line)

    with open(expected_file) as f:
        expected_lines = f.read().splitlines()

    assert actual_lines == expected_lines
