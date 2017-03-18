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


from distutils.dist import Distribution

import pytest

from rainbow.filter import FILTERS
from rainbow.manpage import GenerateManPage
from .test_utils import FILTER_GROUPS, FILTERS_WITH_SHORT_OPTION, FILTERS_WITH_LONG_OPTION


def generate_man_page(request):
    path = 'build/tests-workspace/manpage_' + request.node.name
    command = GenerateManPage(Distribution(), output=path)
    command.run()
    return open(path).read()


@pytest.mark.parametrize("filter_group", FILTER_GROUPS, ids=str)
def test_filter_group_name_included(request, filter_group):
    man_page = generate_man_page(request)
    assert filter_group.name in man_page


@pytest.mark.parametrize("filter_group", FILTER_GROUPS, ids=str)
def test_filter_group_help_included(request, filter_group):
    man_page = generate_man_page(request)
    assert filter_group.help in man_page


@pytest.mark.parametrize("filter", FILTERS_WITH_SHORT_OPTION, ids=str)
def test_filter_short_option_included(request, filter):
    man_page = generate_man_page(request)
    assert '\-' + filter.short_option in man_page


@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
def test_filter_long_option_included(request, filter):
    man_page = generate_man_page(request)
    assert '\-\-' + filter.long_option in man_page


@pytest.mark.parametrize("filter", FILTERS, ids=str)
def test_filter_help_included(request, filter):
    man_page = generate_man_page(request)
    assert filter.help in man_page
