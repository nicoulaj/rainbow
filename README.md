# Colorex


## Description
**Colorize commands output or STDIN using patterns.**

This is a fork of [Linibou's colorex](http://www.linibou.com/colorex/).


## Features
Colorex colors parts of commands output or STDIN using words or regexps, for example:


* Ping Google with IP addresses colorized in red:

    `colorex --red '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' -- ping www.google.com`


Patterns can be defined in config files. Colorex automatically loads the config file if it is named after the command name.
Colorex comes bundled with [several configs](http://github.com/nicoulaj/colorex/tree/master/src/configs) for common commands:


* Colorize the 'diff' command output using the provided config:

    `colorex diff file1 file2`


* Colorize the 'ping' command output using the provided config:

    `colorex ping www.google.com`


* Start JBoss application server with colorized logs:

    `colorex --config=jboss -- jboss/bin/run.sh run`


Colorex can also read from STDIN instead of providing a command:

* Pipe content to colorex:

    `tail -f some-log-file | colorex --red='\[ERROR\].\*' --yellow='\[WARN\].\*'`


## Installing

### Using the PPA
colorex is available as a Debian package in a
[Launchpad.net PPA](https://launchpad.net/~julien-nicoulaud/+archive/colorex).
To install on Ubuntu 9.10+, just run the following commands:
    sudo add-apt-repository ppa:julien-nicoulaud/colorex
    sudo apt-get update
    sudo apt-get install colorex

### Building from sources
You can build the .deb package from the sources:
    git clone git://github.com/nicoulaj/colorex.git
    cd colorex
    make

## Getting started
After installing the package, call the help or read the man page to get started:
    man colorex
    colorex --help


## License
This project is released under the terms of the [GNU General Public License](http://www.gnu.org/licenses/gpl.html).
See COPYING for details.
