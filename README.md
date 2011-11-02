# Colorex


## Description

**Colorize commands output or STDIN using patterns.**

This is a fork of [Linibou's colorex](http://bitbucket.org/linibou/colorex).


## Features

Colorex colors parts of commands output or STDIN using words or regexps.
Just prepend `colorex` with patterns<=>colors associations to your command,
for example:

* Tail some log file with line containing *ERROR* in red:

    `colorex --red '.*ERROR.*' -- tail -f /var/log/my.log`

* Ping Google with IP addresses colorized in yellow:

    `colorex --yellow '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' -- ping www.google.com`

Colorex can also read from STDIN instead of providing a command:

    `tail -f /var/log/my.log | colorex --red '.*ERROR.*'`

Colorex can read patterns<=>colors associations from config files, which
is the most common way to use it. It automatically uses the config file
if there is one named after the command name. Colorex comes bundled with
[several configs](http://bitbucket.org/nicoulaj/colorex/src/1a5e13e44088/src/configs)
for common commands:

* Colorize the 'diff' command output using the provided config:

    `colorex diff file1 file2`


* Start JBoss application server with colorized logs:

    `colorex --config=jboss -- jboss/bin/run.sh run`

See `man colorex` for details on how using config files and writing your own ones.


## Installing

### Debian/Ubuntu
colorex is available as a Debian package in a
[Launchpad.net PPA](https://launchpad.net/~colorex/+archive/ppa).
To install on Ubuntu, just run the following commands:

    sudo add-apt-repository ppa:colorex/ppa
    sudo apt-get update
    sudo apt-get install colorex

### ArchLinux
colorex is available in [AUR](TODO).

### Building from sources
You can build the .deb package from the sources:

    git clone git@bitbucket.org:nicoulaj/colorex.git
    cd colorex
    make

## Getting started
After installing the package, call the help or read the man page to get started:

    man colorex
    colorex --help


## License
This project is released under the terms of the [GNU General Public License](http://www.gnu.org/licenses/gpl.html).
See COPYING for details.
