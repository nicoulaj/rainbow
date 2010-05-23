# Colorex


## Description
**Colorize files using patterns.**

This is a repackaging of [Linibou's colorex](http://www.linibou.com/colorex/).


## Features
Colorex colors parts of files or STDIN using words or regexps, for example:

    tail -f some-log-file | colorex --red='^\[ERROR\].*' --yellow='^\[WARN\].*'


## Installing

### Using the PPA
colorex is available as a Debian package in a
[Launchpad.net PPA](https://launchpad.net/~julien-nicoulaud/+archive/colorex).
To install on Ubuntu 9.10+, just run the following commands:
    sudo add-apt-repository ppa:julien-nicoulaud/colorex
    sudo apt-get update
    sudo apt-get install colorex

### Downloading the Debian package
You can find the last version of the Debian package in the
[downloads](http://github.com/nicoulaj/colorex/downloads) section.

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
