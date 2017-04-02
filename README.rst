rainbow
=======

.. image:: https://img.shields.io/github/tag/nicoulaj/rainbow.svg
   :target: https://github.com/nicoulaj/rainbow/releases
   :alt: last release

.. image:: https://img.shields.io/pypi/pyversions/rainbow.svg
   :target: https://pypi.python.org/pypi/rainbow
   :alt: pypi package

.. image:: https://travis-ci.org/nicoulaj/rainbow.svg?branch=master
   :target: https://travis-ci.org/nicoulaj/rainbow
   :alt: continuous integration

.. image:: https://codecov.io/gh/nicoulaj/rainbow/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/nicoulaj/rainbow
   :alt: test coverage

.. image:: https://scrutinizer-ci.com/g/nicoulaj/rainbow/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/nicoulaj/rainbow/?branch=master
   :alt: scrutinizer-ci.com score

.. image:: https://landscape.io/github/nicoulaj/rainbow/master/landscape.svg?style=flat
   :target: https://landscape.io/github/nicoulaj/rainbow/master
   :alt: landscape.io score

.. image:: https://codeclimate.com/github/nicoulaj/rainbow/badges/gpa.svg
   :target: https://codeclimate.com/github/nicoulaj/rainbow
   :alt: codeclimate.com score

.. image:: https://badges.gitter.im/nicoulaj/rainbow.svg
   :target: https://gitter.im/nicoulaj/rainbow
   :alt: gitter chat

----

**Easily colorize logs or commands output using patterns.**
::

  rainbow [ --COLOR=PATTERN ... | --conf CONF ] COMMAND


Examples
--------

Using the command line
~~~~~~~~~~~~~~~~~~~~~~
Prepend ``rainbow`` with ``--COLOR=PATTERN`` associations to your
command, for example:

-  Tail some log file with lines containing ``ERROR`` in red:
   ::

     rainbow --red='ERROR.*' tailf /var/log/my.log

-  You can also pipe commands output into rainbow:
   ::

     tail -f /var/log/my.log | rainbow --red='.*ERROR.*'

Using configs
~~~~~~~~~~~~~

Rainbow can load configuration for each command from files, which is the most convenient way to use it. When running ``rainbow command``, rainbow will automatically look for a config named ``command.cfg`` in ``/etc/rainbow``, ``~/.rainbow``, or builtin configs:

-  Colorize the ``diff`` command output using the builtin config:
   ::

     rainbow diff file1 file2

-  Start my custom command, using ``~/.rainbow/mycommand.cfg``:
   ::

     rainbow mycommand

The syntax for writing configs is straightforward, see the
`builtin configs <https://github.com/nicoulaj/rainbow/blob/master/rainbow/config/builtin>`_
for examples. See also the `commands support table <https://github.com/nicoulaj/rainbow/blob/master/COMMANDS.md>`_.


Installation
------------

Using packages
~~~~~~~~~~~~~~

============================================  ============================================
 System                                        Installation instructions
============================================  ============================================
 Debian / Ubuntu                               `rainbow repository <https://software.opensuse.org/download.html?project=home%3Anicoulaj%3Arainbow&package=rainbow>`_
 Fedora / CentOS / RHEL / Scientific Linux     `rainbow repository <https://software.opensuse.org/download.html?project=home%3Anicoulaj%3Arainbow&package=rainbow>`_
 OpenSUSE / SLE                                `rainbow repository <https://software.opensuse.org/download.html?project=home%3Anicoulaj%3Arainbow&package=rainbow>`_
 Arch Linux                                    `AUR/rainbow <https://aur.archlinux.org/packages/rainbow>`_ / `AUR/rainbow-git <https://aur.archlinux.org/packages/rainbow-git>`_
 `pip` / `easy_install`                        `PyPI: rainbow <https://pypi.python.org/pypi/rainbow>`_
============================================  ============================================


Building from sources
~~~~~~~~~~~~~~~~~~~~~

You can build from sources this way:

::

    git clone git://github.com/nicoulaj/rainbow.git
    cd rainbow
    python setup.py build
    sudo python setup.py install


Contributing
------------

Contributions are welcome, please see `CONTRIBUTING <https://github.com/nicoulaj/rainbow/blob/master/CONTRIBUTING.md>`_.


License
-------

This project is a fork of `Linibou's colorex <http://bitbucket.org/linibou/colorex>`_.
It is is released under the terms of the `GNU General Public
License <http://www.gnu.org/licenses/gpl.html>`_. See ``COPYING`` for
details.
