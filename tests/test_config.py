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

import pytest

from rainbow.ansi import *
from rainbow.config import *
from rainbow.transformer import TransformerBuilder, IdentityTransformer, InsertBeforeAndAfterRegexTransformer, \
    ListTransformer


def load_config_file(config_file):
    stdout_builder = TransformerBuilder()
    stderr_builder = TransformerBuilder()
    errors = []

    ConfigLoader().load_config_file(config_file,
                                    stdout_builder,
                                    stderr_builder,
                                    lambda error: errors.append(error))

    return stdout_builder.build(), stderr_builder.build(), errors


def test_find_config_name_from_command_line_001_empty_args():
    assert not ConfigLoader.find_config_name_from_command_line([])


def test_find_config_name_from_command_line_002_one_arg():
    assert ConfigLoader.find_config_name_from_command_line(['foo']) == 'foo'


def test_find_config_name_from_command_line_003_several_args():
    assert ConfigLoader.find_config_name_from_command_line(['foo', 'bar', 'bar']) == 'foo'


def test_load_config_file_001_file_does_not_exist():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('does_not_exist.cfg')
    assert errors == ['Could not open config file "does_not_exist.cfg"']


def test_load_config_file_002_empty_config():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config001.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_003_empty_filters_section():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config002.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_004_empty_general_section():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config003.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_005_empty_filters_and_general_sections():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config004.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


@pytest.mark.skip(reason="Not implemented")  # TODO
def test_load_config_file_006_two_empty_filters_sections():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config005.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_007_one_filter():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config006.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ANSI_FOREGROUND_RESET


def test_load_config_file_007_two_different_filters():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config007.cfg')
    assert not errors
    assert isinstance(stdout_transformer, ListTransformer)
    assert isinstance(stderr_transformer, ListTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stderr_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stdout_transformer.transformers[0].before == ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[0].before == ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[0].after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[0].after == ANSI_FOREGROUND_RESET
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[1].regex.pattern == 'WARN'
    assert stderr_transformer.transformers[1].regex.pattern == 'WARN'
    assert stdout_transformer.transformers[1].before == ANSI_FOREGROUND_YELLOW
    assert stderr_transformer.transformers[1].before == ANSI_FOREGROUND_YELLOW
    assert stdout_transformer.transformers[1].after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[1].after == ANSI_FOREGROUND_RESET


@pytest.mark.skip(reason="Not implemented")  # TODO
def test_load_config_file_007_two_times_same_filter():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config008.cfg')
    assert not errors
    assert isinstance(stdout_transformer, ListTransformer)
    assert isinstance(stderr_transformer, ListTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stderr_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stdout_transformer.transformers[0].before == ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[0].before == ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[0].after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[0].after == ANSI_FOREGROUND_RESET
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[1].regex.pattern == 'WARN'
    assert stderr_transformer.transformers[1].regex.pattern == 'WARN'
    assert stdout_transformer.transformers[1].before == ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[1].before == ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[1].after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[1].after == ANSI_FOREGROUND_RESET


@pytest.mark.skip(reason="Not implemented")  # TODO
def test_load_config_file_008_filter_outside_section():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config009.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_009_one_filter_and_stderr_setting_enabled():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config010.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ANSI_FOREGROUND_RESET


def test_load_config_file_010_one_filter_and_stderr_setting_enabled():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config011.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ANSI_FOREGROUND_RESET


def test_load_config_file_011_one_filter_and_stderr_setting_disabled():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config012.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET


def test_load_config_file_012_one_filter_and_stderr_setting_disabled():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config013.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET


def test_load_config_file_013_one_filter_uppercase():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config014.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ANSI_FOREGROUND_RESET


def test_load_config_file_014_one_filter_extra_spaces_before_regex():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config015.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ANSI_FOREGROUND_RESET


def test_load_config_file_015_unknown_filter():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config016.cfg')
    assert errors == ['Unknown filter "foo" in config "tests/configs/config016.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_016_unresolved_import():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config017.cfg')
    assert errors == ['Failed to resolve import of "foo" in config "tests/configs/config017.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_017_unresolved_import_and_valid_filter():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config018.cfg')
    assert errors == ['Failed to resolve import of "foo" in config "tests/configs/config018.cfg"']
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ANSI_FOREGROUND_RESET


@pytest.mark.skip(reason="Not implemented")  # TODO
def test_load_config_file_018_relative_import_without_extension():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config019.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ANSI_FOREGROUND_RESET


@pytest.mark.skip(reason="Not implemented")  # TODO
def test_load_config_file_019_relative_import_with_extension():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config020.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ANSI_FOREGROUND_RESET


def test_load_config_file_020_invalid_key_in_general_section():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config021.cfg')
    assert errors == ['Invalid key "foo" in general section of config "tests/configs/config021.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


@pytest.mark.skip(reason="Not implemented")  # TODO
def test_load_config_file_021_two_times_same_filter_once_in_config_once_in_import():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config022.cfg')
    assert not errors
    assert isinstance(stdout_transformer, ListTransformer)
    assert isinstance(stderr_transformer, ListTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stderr_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stdout_transformer.transformers[0].before == ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[0].before == ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[0].after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[0].after == ANSI_FOREGROUND_RESET
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[1].regex.pattern == 'WARNING'
    assert stderr_transformer.transformers[1].regex.pattern == 'WARNING'
    assert stdout_transformer.transformers[1].before == ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[1].before == ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[1].after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[1].after == ANSI_FOREGROUND_RESET


@pytest.mark.skip(reason="Not implemented")  # TODO
def test_load_config_file_022_multiple_relative_imports_without_extension():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config023.cfg')
    assert not errors
    assert isinstance(stdout_transformer, ListTransformer)
    assert isinstance(stderr_transformer, ListTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stderr_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stdout_transformer.transformers[0].before == ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[0].before == ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[0].after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[0].after == ANSI_FOREGROUND_RESET
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[1].regex.pattern == 'WARN'
    assert stderr_transformer.transformers[1].regex.pattern == 'WARN'
    assert stdout_transformer.transformers[1].before == ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[1].before == ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[1].after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[1].after == ANSI_FOREGROUND_RESET


def test_load_config_file_023_filter_using_filter_name():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config024.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ANSI_FOREGROUND_RESET


def test_load_config_file_024_filter_with_empty_pattern():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config025.cfg')
    assert errors == ['Empty pattern for "red" in config "tests/configs/config025.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_025_empty_imports_section():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config026.cfg')
    assert errors == ['Empty imports section in config "tests/configs/config026.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


@pytest.mark.skip(reason="Not implemented")  # TODO
def test_load_config_file_026_multiple_imports_with_empty_one():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config027.cfg')
    assert errors == ['Empty imports section in config "tests/configs/config026.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_027_invalid_section():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config028.cfg')
    assert errors == ['Invalid section "foo" in config "tests/configs/config028.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_027_invalid_stderr_filtering_value():
    (stdout_transformer, stderr_transformer, errors) = load_config_file('tests/configs/config029.cfg')
    assert errors == ['Invalid value "foo" for key "enable-stderr-filtering" in config "tests/configs/config029.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)
