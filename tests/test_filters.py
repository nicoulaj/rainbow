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

import re

import pytest

from rainbow.filter import FILTERS
from .test_utils import FILTERS_NAMES, FILTERS_HELPS, FILTERS_SHORT_OPTIONS, FILTERS_LONG_OPTIONS, \
    FILTER_GROUPS_NAMES, FILTER_GROUPS, FILTER_GROUPS_HELPS, FILTER_GROUPS_FILTERS


@pytest.mark.parametrize("filter_group", FILTER_GROUPS, ids=str)
def test_filter_group_has_name(filter_group):
    assert filter_group.name is not None


@pytest.mark.parametrize("filter_group", FILTER_GROUPS, ids=str)
def test_filter_group_has_help(filter_group):
    assert filter_group.help is not None


@pytest.mark.parametrize("filter_group", FILTER_GROUPS, ids=str)
def test_filter_group_has_filters(filter_group):
    assert filter_group.filters


@pytest.mark.parametrize("filter_group_name", FILTER_GROUPS_NAMES)
def test_filter_group_has_a_unique_name(filter_group_name):
    assert FILTER_GROUPS_NAMES.count(filter_group_name) == 1


@pytest.mark.parametrize("filter_group_name", FILTER_GROUPS_NAMES)
def test_filter_group_name_syntax(filter_group_name):
    assert bool(re.compile(r'[A-Z][a-z\s]+').match(filter_group_name))


@pytest.mark.parametrize("filter_group_help", FILTER_GROUPS_HELPS)
def test_filter_group_has_a_unique_help(filter_group_help):
    assert FILTER_GROUPS_HELPS.count(filter_group_help) == 1


@pytest.mark.parametrize("filter_group_help", FILTER_GROUPS_HELPS)
def test_filter_group_help_syntax(filter_group_help):
    assert bool(re.compile(r'[A-Z][a-z\s]+.').match(filter_group_help))


@pytest.mark.parametrize("filter_group_filters", FILTER_GROUPS_FILTERS)
def test_filter_group_has_unique_list_of_filters(filter_group_filters):
    assert FILTER_GROUPS_FILTERS.count(filter_group_filters) == 1


@pytest.mark.parametrize("filter", FILTERS, ids=str)
def test_filter_has_name(filter):
    assert filter.name


@pytest.mark.parametrize("filter", FILTERS, ids=str)
def test_filter_has_help(filter):
    assert filter.help


@pytest.mark.parametrize("filter", FILTERS, ids=str)
def test_filter_has_long_option(filter):
    assert filter.long_option


@pytest.mark.parametrize("filter", FILTERS, ids=str)
def test_filter_has_before_or_after(filter):
    assert filter.before or filter.after


@pytest.mark.parametrize("filter_name", FILTERS_NAMES)
def test_filter_has_a_unique_name(filter_name):
    assert FILTERS_NAMES.count(filter_name) == 1


@pytest.mark.parametrize("filter_name", FILTERS_NAMES)
def test_filter_name_syntax(filter_name):
    assert bool(re.compile(r'[a-z\-]+').match(filter_name))


@pytest.mark.parametrize("filter_help", FILTERS_HELPS)
def test_filter_has_a_unique_help(filter_help):
    assert FILTERS_HELPS.count(filter_help) == 1


@pytest.mark.parametrize("filter_help", FILTERS_HELPS)
def test_filter_help_syntax(filter_help):
    assert bool(re.compile(r'[a-z\s]+').match(filter_help))


@pytest.mark.parametrize("filter_short_option", FILTERS_SHORT_OPTIONS)
def test_filter_has_a_unique_short_option(filter_short_option):
    assert filter_short_option is None or FILTERS_SHORT_OPTIONS.count(filter_short_option) == 1


@pytest.mark.parametrize("filter_short_option", FILTERS_SHORT_OPTIONS)
def test_filter_short_option_syntax(filter_short_option):
    assert filter_short_option is None or bool(re.compile(r'[a-z]').match(filter_short_option))


@pytest.mark.parametrize("filter_long_option", FILTERS_LONG_OPTIONS)
def test_filter_has_a_unique_long_option(filter_long_option):
    assert FILTERS_LONG_OPTIONS.count(filter_long_option) == 1


@pytest.mark.parametrize("filter_long_option", FILTERS_LONG_OPTIONS)
def test_filter_long_option_syntax(filter_long_option):
    assert bool(re.compile(r'[a-z\-]+').match(filter_long_option))
