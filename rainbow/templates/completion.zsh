#compdef rainbow
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

typeset -A opt_args
local context state line curcontext="$curcontext"

_arguments \
{%- for filter in filters %}
  {%- if filter.short_option %}
  '*'{-{{ filter.short_option }}+,--{{ filter.long_option }}}'[{{ filter.help }}]' \
  {%- else %}
  '*--{{ filter.long_option }}[{{ filter.help }}]' \
  {%- endif %}
{%- endfor %}
  '(- 1 *)'{-h,--help}'[print program usage]' \
  '(- 1 *)--version[print program version]' \
  '*'{-v,--verbose}'[verbose mode]' \
  '--disable-stderr-filtering[disable STDERR filtering]' \
  {-f,--config}'[rainbow config file]:rainbow config:_files -W "( $(pwd) ~/.rainbow /usr/share/rainbow/configs )" -g "*.cfg(\:r\:t)"' # 32: Need to use the real paths here
