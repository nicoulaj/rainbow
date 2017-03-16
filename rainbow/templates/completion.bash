#!/usr/bin/env bash
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

_rainbow()
{
  local offset=0 i
  for (( i=1; i <= COMP_CWORD; i++ )); do
    case ${COMP_WORDS[$i]} in
      --version|-h|--help|--disable-stderr-filtering|--verbose|-f|--config|-{{ filters|selectattr('short_option')|join('|-', attribute='short_option') }}|--{{ filters|join('|--', attribute='long_option') }})
        i=$((i+1))
        continue
        ;;
      -*)
        continue
        ;;
    esac
    offset=$i
    break
  done
  if [[ $offset -gt 0 ]]; then
    _command_offset $offset
  else
  cur=${COMP_WORDS[COMP_CWORD]}
    if [ $COMP_CWORD -eq 1 ]; then
    COMPREPLY=( $( compgen -W "--version -h --help --print-path --print-config-names --disable-stderr-filtering --verbose -f --config -{{ filters|selectattr('short_option')|join(' -', attribute='short_option') }} --{{ filters|join(' --', attribute='long_option') }}" -- $cur ) )
    else
      first=${COMP_WORDS[1]}
      case "$first" in
        --version|-h|--help|--print-path|--print-config-names)
          COMPREPLY=()
          ;;
        *)
          prev=${COMP_WORDS[COMP_CWORD-1]}
          case "$prev" in
            -{{ filters|selectattr('short_option')|join('|-', attribute='short_option') }}|--{{ filters|join('|--', attribute='long_option') }})
              COMPREPLY=()
              ;;
            -f|--config)
              COMPREPLY=( $(rainbow --print-config-names) \
                          $(compgen -d $cur ) \
                          $(compgen -f -X "!*.cfg" $cur ) )
              ;;
            *)
              COMPREPLY=( $( compgen -W "--disable-stderr-filtering --verbose -f --config -{{ filters|selectattr('short_option')|join(' -', attribute='short_option') }} --{{ filters|join(' --', attribute='long_option') }}" -- $cur ) )
              ;;
          esac
          ;;
      esac
    fi
  fi
}

complete -F _rainbow rainbow
