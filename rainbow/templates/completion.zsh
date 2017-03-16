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

_rainbow() {
  typeset -A opt_args
  local context state line curcontext="$curcontext"

  _arguments \
{%- for filter in filters %}
  {%- if filter.short_option %}
    '*'{-{{ filter.short_option }}+,--{{ filter.long_option }}=}'[{{ filter.help }}]:pattern:_rainbow_patterns' \
  {%- else %}
    '*--{{ filter.long_option }}=[{{ filter.help }}]:pattern:_rainbow_patterns' \
  {%- endif %}
{%- endfor %}
    '(- 1 *)'{-h,--help}'[print program usage]' \
    '(- 1 *)--version[print program version]' \
    '(- 1 *)--print-path[print config paths]' \
    '(- 1 *)--print-config-names[print config names]' \
    '*'{-v,--verbose}'[verbose mode]' \
    '--disable-stderr-filtering[disable STDERR filtering]' \
    '*'{-f,--config=}'[rainbow config file]:rainbow config:_rainbow_configs' \
      '(-):command name: _command_names -e' \
      '*::arguments:_normal' && ret=0
}

(( $+functions[_rainbow_patterns] )) ||
_rainbow_patterns() {
  _message -e pattern "pattern"
}

(( $+functions[_rainbow_configs] )) ||
_rainbow_configs() {
  _alternative \
    'config-names:config name:_rainbow_config_names' \
    'config-files:config file:_rainbow_config_files'
}

(( $+functions[_rainbow_config_names] )) ||
_rainbow_config_names() {
  local rainbow_config_names
  rainbow_config_names=( "${(f)$(_call_program configs rainbow --print-config-names 2>/dev/null)}" )
  _describe -t 'rainbow config names' 'rainbow config name' rainbow_config_names
}

(( $+functions[_rainbow_config_files] )) ||
_rainbow_config_files() {
  _files -g "*.cfg"
}

_rainbow "$@"
