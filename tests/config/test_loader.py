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

import pytest

from rainbow import ansi
from rainbow.config.loader import ConfigLoader
from rainbow.transformer import IdentityTransformer
from rainbow.transformer import InsertBeforeAndAfterRegexTransformer
from rainbow.transformer import ListTransformer
from rainbow.transformer import TransformerBuilder


def load(config):
    stdout_builder = TransformerBuilder()
    stderr_builder = TransformerBuilder()
    errors = []

    ConfigLoader().load_config_file(config,
                                    stdout_builder,
                                    stderr_builder,
                                    lambda error: errors.append(error))

    return stdout_builder.build(), stderr_builder.build(), errors


def resolve_and_load(config):
    stdout_builder = TransformerBuilder()
    stderr_builder = TransformerBuilder()
    errors = []

    ConfigLoader().resolve_and_load_config(config,
                                           stdout_builder,
                                           stderr_builder,
                                           lambda error: errors.append(error))

    return stdout_builder.build(), stderr_builder.build(), errors


def load_from_command_line(args):
    stdout_builder = TransformerBuilder()
    stderr_builder = TransformerBuilder()
    errors = []

    ConfigLoader(['tests/data/cfg']).load_config_from_command_line(args,
                                                                   stdout_builder,
                                                                   stderr_builder,
                                                                   lambda error: errors.append(error))

    return stdout_builder.build(), stderr_builder.build(), errors


def test_resolve_config_file_empty_path():
    assert not ConfigLoader([]).resolve_config_file("does_not_exist")


def test_resolve_config_file_none_in_path():
    assert not ConfigLoader([None]).resolve_config_file("does_not_exist")


def test_resolve_config_file_path_without_extension():
    assert ConfigLoader().resolve_config_file("tests/data/cfg/config001") == "tests/data/cfg/config001.cfg"


def test_resolve_config_file_path():
    assert ConfigLoader().resolve_config_file("tests/data/cfg/config001.cfg") == "tests/data/cfg/config001.cfg"


def test_find_config_name_from_command_line_empty_args():
    assert not ConfigLoader.find_config_name_from_command_line([])


def test_find_config_name_from_command_line_one_arg():
    assert ConfigLoader.find_config_name_from_command_line(['foo']) == 'foo'


def test_find_config_name_from_command_line_several_args():
    assert ConfigLoader.find_config_name_from_command_line(['foo', 'bar', 'bar']) == 'foo'


def test_resolve_and_load_config_file_file_does_not_exist():
    (stdout_transformer, stderr_transformer, errors) = resolve_and_load('does_not_exist.cfg')
    assert errors == ['Could not resolve config "does_not_exist.cfg"']


def test_resolve_and_load_unresolvable_config_file():
    (stdout_transformer, stderr_transformer, errors) = resolve_and_load('does_not_exist')
    assert errors == ['Could not resolve config "does_not_exist"']


def test_load_config_file_unresolvable():
    (stdout_transformer, stderr_transformer, errors) = load('does_not_exist')
    assert errors == ['Could not open config file "does_not_exist"']


def test_load_config_file_empty_config():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config001.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_empty_filters_section():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config002.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_empty_general_section():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config003.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_empty_filters_and_general_sections():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config004.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


@pytest.mark.skipif(condition=sys.version_info[0] < 3, reason="Issue #2: Python 2 does not detect duplicate sections")
def test_load_config_file_two_empty_filters_sections():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config005.cfg')
    assert errors == ['Duplicate section "filters" in "tests/data/cfg/config005.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_one_filter():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config006.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_two_different_filters():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config007.cfg')
    assert not errors
    assert isinstance(stdout_transformer, ListTransformer)
    assert isinstance(stderr_transformer, ListTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stderr_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stdout_transformer.transformers[0].before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[0].before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[0].after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[0].after == ansi.ANSI_FOREGROUND_RESET
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[1].regex.pattern == 'WARN'
    assert stderr_transformer.transformers[1].regex.pattern == 'WARN'
    assert stdout_transformer.transformers[1].before == ansi.ANSI_FOREGROUND_YELLOW
    assert stderr_transformer.transformers[1].before == ansi.ANSI_FOREGROUND_YELLOW
    assert stdout_transformer.transformers[1].after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[1].after == ansi.ANSI_FOREGROUND_RESET


@pytest.mark.skip(reason="Issue #2: Duplicate key support not implemented")
def test_load_config_file_two_times_same_filter():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config008.cfg')
    assert not errors
    assert isinstance(stdout_transformer, ListTransformer)
    assert isinstance(stderr_transformer, ListTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stderr_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stdout_transformer.transformers[0].before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[0].before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[0].after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[0].after == ansi.ANSI_FOREGROUND_RESET
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[1].regex.pattern == 'WARN'
    assert stderr_transformer.transformers[1].regex.pattern == 'WARN'
    assert stdout_transformer.transformers[1].before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[1].before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[1].after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[1].after == ansi.ANSI_FOREGROUND_RESET


@pytest.mark.skip(reason="Issue #2: Support of filters in global section not implemented")
def test_load_config_file_filter_in_global_section():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config009.cfg')
    assert not errors
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_one_filter_and_stderr_setting_enabled():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config010.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_one_filter_and_stderr_setting_enabled_uppercase():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config011.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_one_filter_and_stderr_setting_disabled():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config012.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_one_filter_and_stderr_setting_disabled_uppercase():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config013.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_one_filter_and_stderr_setting_disabled_with_no():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config030.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_one_filter_uppercase():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config014.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_one_filter_extra_spaces_before_regex():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config015.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_unknown_filter():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config016.cfg')
    assert errors == ['Unknown filter "foo" in config "tests/data/cfg/config016.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_unresolved_import():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config017.cfg')
    assert errors == ['Failed to resolve import of "foo" in config "tests/data/cfg/config017.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_unresolved_import_and_valid_filter():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config018.cfg')
    assert errors == ['Failed to resolve import of "foo" in config "tests/data/cfg/config018.cfg"']
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_relative_import_without_extension():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config019.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_relative_import_with_extension():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config020.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_invalid_key_in_general_section():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config021.cfg')
    assert errors == ['Invalid key "foo" in general section of config "tests/data/cfg/config021.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_two_times_same_filter_once_in_config_once_in_import():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config022.cfg')
    assert not errors
    assert isinstance(stdout_transformer, ListTransformer)
    assert isinstance(stderr_transformer, ListTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[0], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stderr_transformer.transformers[0].regex.pattern == 'ERROR'
    assert stdout_transformer.transformers[0].before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[0].before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[0].after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[0].after == ansi.ANSI_FOREGROUND_RESET
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stdout_transformer.transformers[1], InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.transformers[1].regex.pattern == 'WARNING'
    assert stderr_transformer.transformers[1].regex.pattern == 'WARNING'
    assert stdout_transformer.transformers[1].before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.transformers[1].before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.transformers[1].after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.transformers[1].after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_multiple_relative_imports_without_extension():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config023.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_filter_using_filter_name():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config024.cfg')
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET


def test_load_config_file_filter_with_empty_pattern():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config025.cfg')
    assert errors == ['Empty pattern for "red" in config "tests/data/cfg/config025.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_empty_imports_section():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config026.cfg')
    assert errors == ['Empty imports section in config "tests/data/cfg/config026.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_multiple_imports_with_empty_one():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config027.cfg')
    assert errors == ['Empty import in config "tests/data/cfg/config027.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_invalid_section():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config028.cfg')
    assert errors == ['Invalid section "foo" in config "tests/data/cfg/config028.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_invalid_stderr_filtering_value():
    (stdout_transformer, stderr_transformer, errors) = load('tests/data/cfg/config029.cfg')
    assert errors == ['Invalid value "foo" for key "enable-stderr-filtering" in config "tests/data/cfg/config029.cfg"']
    assert isinstance(stdout_transformer, IdentityTransformer)
    assert isinstance(stderr_transformer, IdentityTransformer)


def test_load_config_file_from_command_line_one_filter():
    (stdout_transformer, stderr_transformer, errors) = load_from_command_line(['config006', '--help'])
    assert not errors
    assert isinstance(stdout_transformer, InsertBeforeAndAfterRegexTransformer)
    assert isinstance(stderr_transformer, InsertBeforeAndAfterRegexTransformer)
    assert stdout_transformer.regex.pattern == 'ERROR'
    assert stderr_transformer.regex.pattern == 'ERROR'
    assert stdout_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stderr_transformer.before == ansi.ANSI_FOREGROUND_RED
    assert stdout_transformer.after == ansi.ANSI_FOREGROUND_RESET
    assert stderr_transformer.after == ansi.ANSI_FOREGROUND_RESET
