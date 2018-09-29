Contributing
============

Contributions are welcome, please take a look at the [issues list](https://github.com/nicoulaj/rainbow/issues).


Development environment
-----------------------

This project uses a standard layout. Here are some example steps to setup
your development environment using [pew](https://github.com/berdario/pew):

1. Checkout project sources:

        git clone https://github.com/nicoulaj/rainbow.git
        cd rainbow

2. To run tests, rainbow uses [tox](https://tox.readthedocs.io):

        tox

   This will run all the tests, for all python versions. To run tests for
   one specific version:

        tox -e py27

   After you run tests, results (test, coverage and benchmark HTML reports) will be available in the `build/tests` directory.


Commands wishlist
-----------------

This table contains an inventory of commands we could potentially support in rainbow, with their current status.
If you want to request and/or plan to working on one, please send a pull request to update this table.

| command / format     | rainbow support      | third party support                      | status                               |
| -------------------- | -------------------- | ---------------------------------------- | ------------------------------------ |
| acpi                 | :x:                  | cope                                     |                                      |
| ant                  | :x:                  | builtin color support, colorlogs         | :ok:                                 |
| apm                  | :x:                  | ccze                                     |                                      |
| arp                  | :x:                  | cope, cwrapper                           |                                      |
| arping               | :x:                  | cwrapper                                 |                                      |
| auth.log             | :x:                  | cwrapper                                 |                                      |
| blockdev             | :x:                  | cwrapper                                 |                                      |
| cal                  | :x:                  | cwrapper                                 |                                      |
| cc                   | :x:                  | cope                                     | rainbow config needed                |
| cksum                | :x:                  | cwrapper                                 | rainbow config needed                |
| clock                | :x:                  | cwrapper                                 |                                      |
| configure            | :x:                  | cwrapper, grc                            | rainbow config needed                |
| cpuinfo              | :x:                  | cwrapper                                 | rainbow config needed                |
| crontab              | :x:                  | cwrapper                                 |                                      |
| cvs                  | :x:                  | colorcvs, grc                            |                                      |
| date                 | :x:                  | cwrapper                                 |                                      |
| df                   | :heavy_check_mark:   | dfc, cope, cwrapper, grc                 | :ok:                                 |
| diff                 | :heavy_check_mark:   | colordiff, grc, cwrapper                 | :ok:                                 |
| dig                  | :x:                  | cwrapper                                 | rainbow config needed                |
| distcc               | :x:                  | ccze                                     |                                      |
| dmesg                | :x:                  | cwrapper                                 |                                      |
| dpkg                 | :x:                  | ccze                                     |                                      |
| dprofpp              | :x:                  | cope                                     |                                      |
| du                   | :x:                  | cwrapper                                 |                                      |
| env                  | :heavy_check_mark:   | cwrapper                                 | :ok:                                 |
| esperanto            | :x:                  | grc                                      |                                      |
| example              | :x:                  | colorlogs                                |                                      |
| exim                 | :x:                  | ccze                                     |                                      |
| fdisk                | :x:                  | cope                                     |                                      |
| fetchmail            | :x:                  | ccze                                     |                                      |
| figlet               | :x:                  | cwrapper                                 |                                      |
| file                 | :x:                  | cwrapper                                 |                                      |
| find                 | :x:                  | cwrapper                                 | rainbow config needed                |
| finger               | :x:                  | cwrapper                                 |                                      |
| free                 | :x:                  | cwrapper, cope                           | rainbow config needed                |
| fstab                | :x:                  | cwrapper                                 |                                      |
| ftpstats             | :x:                  | ccze                                     |                                      |
| fuser                | :x:                  | cwrapper                                 |                                      |
| gcc                  | :x:                  | colorgcc, cope, cwrapper, grc            |                                      |
| g++                  | :x:                  | cwrapper, cope                           |                                      |
| git                  | :x:                  | partial builtin color support, colorlogs |                                      |
| group                | :x:                  | cwrapper                                 |                                      |
| groups               | :x:                  | cwrapper                                 |                                      |
| hdparm               | :x:                  | cwrapper                                 |                                      |
| hexdump              | :x:                  | cwrapper                                 |                                      |
| host                 | :heavy_check_mark:   | cwrapper                                 | :ok:                                 |
| hosts                | :x:                  | cwrapper                                 |                                      |
| httpd                | :x:                  | ccze                                     |                                      |
| icecast              | :x:                  | ccze                                     |                                      |
| id                   | :x:                  | cope, cwrapper                           | rainbow config needed                |
| ifconfig             | :heavy_check_mark:   | cwrapper, cope                           | :ok:                                 |
| inittab              | :x:                  | cwrapper                                 |                                      |
| iptables             | :x:                  | cwrapper                                 |                                      |
| irclog               | :x:                  | grc                                      |                                      |
| java stack traces    | :heavy_check_mark:   |                                          | :ok:                                 |
| last                 | :x:                  | cwrapper                                 |                                      |
| lastlog              | :x:                  | cwrapper                                 |                                      |
| ldap                 | :x:                  | grc                                      |                                      |
| log                  | :x:                  | grc                                      |                                      |
| lsattr               | :x:                  | cwrapper                                 |                                      |
| ls                   | :x:                  | dircolors, cope                          |                                      |
| lsmod                | :x:                  | cwrapper                                 |                                      |
| lsof                 | :x:                  | cwrapper                                 | rainbow config needed                |
| lspci                | :x:                  | cope                                     |                                      |
| lsusb                | :x:                  | cope                                     |                                      |
| ltrace-color         | :x:                  | cwrapper                                 |                                      |
| make                 | :x:                  | colormake, cwrapper, cope                | rainbow config needed                |
| md5sum               | :heavy_check_mark:   | cwrapper, cope                           | :ok:                                 |
| meminfo              | :x:                  | cwrapper                                 |                                      |
| messages             | :x:                  | cwrapper                                 |                                      |
| mount                | :x:                  | grc, cwrapper                            | rainbow config needed                |
| mpc                  | :x:                  | cope                                     |                                      |
| mpg123               | :x:                  | cwrapper                                 |                                      |
| mvn                  | :heavy_check_mark:   | colorslogs                               | :ok:                                 |
| netstat              | :x:                  | grc, cope, cwrapper                      | rainbow config needed                |
| nfsstat              | :x:                  | cwrapper                                 | rainbow config needed                |
| nmap                 | :x:                  | cwrapper, cope                           |                                      |
| nm                   | :x:                  | cope                                     |                                      |
| nocope               | :x:                  | cope                                     |                                      |
| nslookup             | :x:                  | cwrapper                                 |                                      |
| objdump              | :x:                  | cwrapper                                 |                                      |
| oops                 | :x:                  | ccze                                     |                                      |
| passwd               | :x:                  | cwrapper                                 |                                      |
| php                  | :x:                  | ccze                                     |                                      |
| ping                 | :heavy_check_mark:   | grc, cwrapper, cope                      | :ok:                                 |
| pmap                 | :x:                  | cwrapper, cope                           |                                      |
| pmap_dump            | :x:                  | cwrapper                                 |                                      |
| postfix              | :x:                  | ccze                                     |                                      |
| praliases            | :x:                  | cwrapper                                 |                                      |
| procmail             | :x:                  | ccze                                     |                                      |
| proftpd              | :x:                  | grc, ccze                                |                                      |
| ps                   | :x:                  | cwrapper, cope                           | rainbow config needed                |
| pstree               | :x:                  | cwrapper                                 | rainbow config needed                |
| quota                | :x:                  | cwrapper                                 |                                      |
| quotastats           | :x:                  | cwrapper                                 |                                      |
| readelf              | :x:                  | cope                                     |                                      |
| resolv               | :x:                  | cwrapper                                 |                                      |
| route                | :x:                  | cwrapper, cope                           |                                      |
| routel               | :x:                  | cwrapper                                 |                                      |
| screen               | :x:                  | cope                                     |                                      |
| sdiff                | :x:                  | cwrapper                                 |                                      |
| services             | :x:                  | cwrapper                                 |                                      |
| sha1sum              | :x:                  | cope                                     | rainbow config needed                |
| sha224sum            | :x:                  | cope                                     | rainbow config needed                |
| sha256sum            | :x:                  | cope                                     | rainbow config needed                |
| sha384sum            | :x:                  | cope                                     | rainbow config needed                |
| sha512sum            | :x:                  | cope                                     | rainbow config needed                |
| shasum               | :x:                  | cope                                     | rainbow config needed                |
| showmount            | :x:                  | cwrapper                                 |                                      |
| smbstatus            | :x:                  | cwrapper                                 |                                      |
| socklist             | :x:                  | cope                                     |                                      |
| squid                | :x:                  | ccze                                     |                                      |
| stat                 | :x:                  | cwrapper, cope                           |                                      |
| strace               | :x:                  | cope                                     | rainbow config needed                |
| sulog                | :x:                  | ccze                                     |                                      |
| super                | :x:                  | ccze                                     |                                      |
| svn                  | :x:                  | colorsvn                                 |                                      |
| sysctl               | :x:                  | cwrapper                                 |                                      |
| syslog               | :x:                  | cwrapper, ccze                           |                                      |
| tar                  | :x:                  | cwrapper                                 |                                      |
| tcpdump              | :x:                  | cwrapper, cope                           |                                      |
| tomcat               | :heavy_check_mark:   |                                          | :ok:                                 |
| tracepath            | :x:                  | cwrapper, cope                           |                                      |
| traceroute           | :heavy_check_mark:   | cope, grc, cwrapper                      | :ok:                                 |
| ulogd                | :x:                  | ccze                                     |                                      |
| umount               | :x:                  | cwrapper                                 |                                      |
| uname                | :x:                  | cwrapper                                 |                                      |
| uptime               | :x:                  | cwrapper                                 |                                      |
| users                | :x:                  | cwrapper                                 |                                      |
| vmstat               | :x:                  | cwrapper                                 |                                      |
| vsftpd               | :x:                  | ccze                                     |                                      |
| wc                   | :x:                  | cwrapper                                 |                                      |
| w                    | :x:                  | cwrapper, cope                           |                                      |
| wdiff                | :x:                  | grc                                      |                                      |
| wget                 | :x:                  | cope                                     |                                      |
| whereis              | :x:                  | cwrapper                                 |                                      |
| who                  | :x:                  | cwrapper, cope                           |                                      |
| xferlog              | :x:                  | cwrapper, ccze                           |                                      |
| xrandr               | :x:                  | cope                                     |                                      |
