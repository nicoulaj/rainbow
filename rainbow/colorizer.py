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

from . import LOGGER


class Colorizer:
    def __init__(self):
        pass

    def colorize(self, line):
        raise NotImplementedError()


class NoColorizer:
    def __init__(self):
        pass

    @staticmethod
    def colorize(line):
        return line


class RegexColorizer(Colorizer, dict):
    def register_pattern_with_filter(self, pattern, filter):
        LOGGER.debug('Binding pattern "%s" with filter "%s".', pattern, filter)

        regex = re.compile(pattern)

        if pattern in self:
            if filter.before:
                self[regex]['before'] += filter.before

            if filter.after:
                self[regex]['after'] += filter.after

        else:
            self[regex] = {'before': filter.before or '', 'after': filter.after or ''}

    def colorize(self, line):
        for (regex, filters) in self:
            line = regex.sub(filters['before'] + r'\g<0>' + filters['after'], line)
        return line.rstrip()
