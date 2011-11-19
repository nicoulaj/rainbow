Rainbow
=======

Description
-----------

**Colorize commands output or STDIN using patterns.**

This is a fork of `Linibou's colorex <http://bitbucket.org/linibou/colorex>`_.

Features
--------

Rainbow colors parts of commands output or STDIN using words or regexps.
Just prepend ``rainbow`` with patterns<=>colors associations to your
command, for example:

-  Tail some log file with lines containing *ERROR* in red:

   ``rainbow --red '.*ERROR.*' -- tail -f /var/log/my.log``

-  Ping Google with IP addresses colorized in yellow:

   ``rainbow --yellow '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' -- ping www.google.com``

-  Rainbow can also read from STDIN instead of providing a command:

   ``tail -f /var/log/my.log | rainbow --red '.*ERROR.*'``

Rainbow can read patterns<=>colors associations from config files, which
is the most common way to use it. It automatically uses the config file
if there is one named after the command name. Rainbow comes bundled with
`several
configs <https://github.com/nicoulaj/rainbow/blob/master/configs>`_
for common commands:

-  Colorize the 'diff' command output using the provided config:

   ``rainbow diff file1 file2``

-  Start JBoss application server with colorized logs:

   ``rainbow --config=jboss -- jboss/bin/run.sh run``

See ``man rainbow`` for details on how using config files and writing
your own ones.

Installing
----------

ArchLinux
~~~~~~~~~

rainbow is available in `AUR <TODO>`_.

Building from sources
~~~~~~~~~~~~~~~~~~~~~

You can build from sources this way:

::

    git clone git://github.com/nicoulaj/rainbow.git
    cd rainbow
    sudo python setup.py install

Getting started
---------------

After installing the package, call the help to get started:

::

    rainbow --help

License
-------

This project is released under the terms of the `GNU General Public
License <http://www.gnu.org/licenses/gpl.html>`_. See COPYING for
details.
