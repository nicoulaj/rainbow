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

from rainbow.completion import GenerateCompletion
from .test_utils import FILTERS_WITH_SHORT_OPTION, FILTERS_WITH_LONG_OPTION

SHELLS = ['bash', 'zsh']


def generate_completion(request, shell):
    path = 'build/tests-workspace/completion_' + shell + '_' + request.node.name
    command = GenerateCompletion(Distribution(), shell=shell, output=path)
    command.run()
    return open(path).read()


@pytest.mark.parametrize("shell", SHELLS)
@pytest.mark.parametrize("filter", FILTERS_WITH_SHORT_OPTION, ids=str)
def test_filter_short_option_included(request, shell, filter):
    completion = generate_completion(request, shell)
    assert '-' + filter.short_option in completion


@pytest.mark.parametrize("shell", SHELLS)
@pytest.mark.parametrize("filter", FILTERS_WITH_LONG_OPTION, ids=str)
def test_filter_long_option_included(request, shell, filter):
    completion = generate_completion(request, shell)
    assert '--' + filter.long_option in completion
