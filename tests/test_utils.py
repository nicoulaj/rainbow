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

from rainbow.filter import FILTER_GROUPS


FILTER_GROUPS_NAMES = [g.name for g in FILTER_GROUPS]
FILTER_GROUPS_HELPS = [g.help for g in FILTER_GROUPS]
FILTER_GROUPS_FILTERS = [g.filters for g in FILTER_GROUPS]

FILTERS = [f for g in FILTER_GROUPS for f in g.filters]
FILTERS_NAMES = [f.name for g in FILTER_GROUPS for f in g.filters]
FILTERS_HELPS = [f.help for g in FILTER_GROUPS for f in g.filters]
FILTERS_SHORT_OPTIONS = [f.short_option for g in FILTER_GROUPS for f in g.filters if f.short_option is not None]
FILTERS_LONG_OPTIONS = [f.long_option for g in FILTER_GROUPS for f in g.filters]


def filter_group_label(filter_group):
    return filter_group.__str__()


def filter_label(filter):
    return filter.__str__()
