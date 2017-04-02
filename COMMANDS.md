Commands support
================

This table lists all commands we could potentially support in rainbow, with their current status:

| command / format     | rainbow support      | third party support                      | status                               |
| -------------------- | -------------------- | ---------------------------------------- | ------------------------------------ |
| acpi                 | :x:                  | cope                                     | TODO (not decided)                   |
| ant                  | :x:                  | builtin color support, colorlogs         | :ok:                                 |
| apm                  | :x:                  | ccze                                     | TODO (not decided)                   |
| arp                  | :x:                  | cope, cwrapper                           | TODO (not decided)                   |
| arping               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| auth.log             | :x:                  | cwrapper                                 | TODO (not decided)                   |
| blockdev             | :x:                  | cwrapper                                 | TODO (not decided)                   |
| cal                  | :x:                  | cwrapper                                 | TODO (not decided)                   |
| cc                   | :x:                  | cope                                     | rainbow config needed                |
| cksum                | :x:                  | cwrapper                                 | rainbow config needed                |
| clock                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| configure            | :x:                  | cwrapper, grc                            | rainbow config needed                |
| cpuinfo              | :x:                  | cwrapper                                 | rainbow config needed                |
| crontab              | :x:                  | cwrapper                                 | TODO (not decided)                   |
| cvs                  | :x:                  | colorcvs, grc                            | no interest                          |
| date                 | :x:                  | cwrapper                                 | TODO (not decided)                   |
| df                   | :heavy_check_mark:   | dfc, cope, cwrapper, grc                 | :ok:                                 |
| diff                 | :heavy_check_mark:   | colordiff, grc, cwrapper                 | :ok:                                 |
| dig                  | :x:                  | cwrapper                                 | rainbow config needed                |
| distcc               | :x:                  | ccze                                     | TODO (not decided)                   |
| dmesg                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| dpkg                 | :x:                  | ccze                                     | TODO (not decided)                   |
| dprofpp              | :x:                  | cope                                     | TODO (not decided)                   |
| du                   | :x:                  | cwrapper                                 | TODO (not decided)                   |
| env                  | :heavy_check_mark:   | cwrapper                                 | :ok:                                 |
| esperanto            | :x:                  | grc                                      | TODO (not decided)                   |
| example              | :x:                  | colorlogs                                | TODO (not decided)                   |
| exim                 | :x:                  | ccze                                     | TODO (not decided)                   |
| fdisk                | :x:                  | cope                                     | TODO (not decided)                   |
| fetchmail            | :x:                  | ccze                                     | TODO (not decided)                   |
| figlet               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| file                 | :x:                  | cwrapper                                 | TODO (not decided)                   |
| find                 | :x:                  | cwrapper                                 | rainbow config needed                |
| finger               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| free                 | :x:                  | cwrapper, cope                           | rainbow config needed                |
| fstab                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| ftpstats             | :x:                  | ccze                                     | TODO (not decided)                   |
| fuser                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| gcc                  | :x:                  | colorgcc, cope, cwrapper, grc            | TODO (not decided)                   |
| g++                  | :x:                  | cwrapper, cope                           | TODO (not decided)                   |
| git                  | :x:                  | partial builtin color support, colorlogs | TODO (not decided)                   |
| group                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| groups               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| hdparm               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| hexdump              | :x:                  | cwrapper                                 | TODO (not decided)                   |
| host                 | :heavy_check_mark:   | cwrapper                                 | :ok:                                 |
| hosts                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| httpd                | :x:                  | ccze                                     | TODO (not decided)                   |
| icecast              | :x:                  | ccze                                     | TODO (not decided)                   |
| id                   | :x:                  | cope, cwrapper                           | rainbow config needed                |
| ifconfig             | :heavy_check_mark:   | cwrapper, cope                           | :ok:                                 |
| inittab              | :x:                  | cwrapper                                 | TODO (not decided)                   |
| iptables             | :x:                  | cwrapper                                 | TODO (not decided)                   |
| irclog               | :x:                  | grc                                      | TODO (not decided)                   |
| java stack traces    | :heavy_check_mark:   |                                          | :ok:                                 |
| last                 | :x:                  | cwrapper                                 | TODO (not decided)                   |
| lastlog              | :x:                  | cwrapper                                 | TODO (not decided)                   |
| ldap                 | :x:                  | grc                                      | TODO (not decided)                   |
| log                  | :x:                  | grc                                      | TODO (not decided)                   |
| lsattr               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| ls                   | :x:                  | dircolors, cope                          | no interest                          |
| lsmod                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| lsof                 | :x:                  | cwrapper                                 | rainbow config needed                |
| lspci                | :x:                  | cope                                     | TODO (not decided)                   |
| lsusb                | :x:                  | cope                                     | TODO (not decided)                   |
| ltrace-color         | :x:                  | cwrapper                                 | TODO (not decided)                   |
| make                 | :x:                  | colormake, cwrapper, cope                | rainbow config needed                |
| md5sum               | :heavy_check_mark:   | cwrapper, cope                           | :ok:                                 |
| meminfo              | :x:                  | cwrapper                                 | TODO (not decided)                   |
| messages             | :x:                  | cwrapper                                 | TODO (not decided)                   |
| mount                | :x:                  | grc, cwrapper                            | rainbow config needed                |
| mpc                  | :x:                  | cope                                     | TODO (not decided)                   |
| mpg123               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| mvn                  | :heavy_check_mark:   | colorslogs                               | :ok:                                 |
| netstat              | :x:                  | grc, cope, cwrapper                      | rainbow config needed                |
| nfsstat              | :x:                  | cwrapper                                 | rainbow config needed                |
| nmap                 | :x:                  | cwrapper, cope                           | TODO (not decided)                   |
| nm                   | :x:                  | cope                                     | TODO (not decided)                   |
| nocope               | :x:                  | cope                                     | TODO (not decided)                   |
| nslookup             | :x:                  | cwrapper                                 | TODO (not decided)                   |
| objdump              | :x:                  | cwrapper                                 | TODO (not decided)                   |
| oops                 | :x:                  | ccze                                     | TODO (not decided)                   |
| passwd               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| php                  | :x:                  | ccze                                     | TODO (not decided)                   |
| ping                 | :heavy_check_mark:   | grc, cwrapper, cope                      | :ok:                                 |
| pmap                 | :x:                  | cwrapper, cope                           | TODO (not decided)                   |
| pmap_dump            | :x:                  | cwrapper                                 | TODO (not decided)                   |
| postfix              | :x:                  | ccze                                     | TODO (not decided)                   |
| praliases            | :x:                  | cwrapper                                 | TODO (not decided)                   |
| procmail             | :x:                  | ccze                                     | TODO (not decided)                   |
| proftpd              | :x:                  | grc, ccze                                | TODO (not decided)                   |
| ps                   | :x:                  | cwrapper, cope                           | rainbow config needed                |
| pstree               | :x:                  | cwrapper                                 | rainbow config needed                |
| quota                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| quotastats           | :x:                  | cwrapper                                 | TODO (not decided)                   |
| readelf              | :x:                  | cope                                     | TODO (not decided)                   |
| resolv               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| route                | :x:                  | cwrapper, cope                           | TODO (not decided)                   |
| routel               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| screen               | :x:                  | cope                                     | TODO (not decided)                   |
| sdiff                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| services             | :x:                  | cwrapper                                 | TODO (not decided)                   |
| sha1sum              | :x:                  | cope                                     | rainbow config needed                |
| sha224sum            | :x:                  | cope                                     | rainbow config needed                |
| sha256sum            | :x:                  | cope                                     | rainbow config needed                |
| sha384sum            | :x:                  | cope                                     | rainbow config needed                |
| sha512sum            | :x:                  | cope                                     | rainbow config needed                |
| shasum               | :x:                  | cope                                     | rainbow config needed                |
| showmount            | :x:                  | cwrapper                                 | TODO (not decided)                   |
| smbstatus            | :x:                  | cwrapper                                 | TODO (not decided)                   |
| socklist             | :x:                  | cope                                     | TODO (not decided)                   |
| squid                | :x:                  | ccze                                     | TODO (not decided)                   |
| stat                 | :x:                  | cwrapper, cope                           | TODO (not decided)                   |
| strace               | :x:                  | cope                                     | rainbow config needed                |
| sulog                | :x:                  | ccze                                     | TODO (not decided)                   |
| super                | :x:                  | ccze                                     | TODO (not decided)                   |
| svn                  | :x:                  | colorsvn                                 | no interest                          |
| sysctl               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| syslog               | :x:                  | cwrapper, ccze                           | TODO (not decided)                   |
| tar                  | :x:                  | cwrapper                                 | TODO (not decided)                   |
| tcpdump              | :x:                  | cwrapper, cope                           | TODO (not decided)                   |
| tomcat               | :heavy_check_mark:   |                                          | :ok:                                 |
| tracepath            | :x:                  | cwrapper, cope                           | TODO (not decided)                   |
| traceroute           | :heavy_check_mark:   | cope, grc, cwrapper                      | :ok:                                 |
| ulogd                | :x:                  | ccze                                     | TODO (not decided)                   |
| umount               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| uname                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| uptime               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| users                | :x:                  | cwrapper                                 | TODO (not decided)                   |
| vmstat               | :x:                  | cwrapper                                 | TODO (not decided)                   |
| vsftpd               | :x:                  | ccze                                     | TODO (not decided)                   |
| wc                   | :x:                  | cwrapper                                 | TODO (not decided)                   |
| w                    | :x:                  | cwrapper, cope                           | TODO (not decided)                   |
| wdiff                | :x:                  | grc                                      | TODO (not decided)                   |
| wget                 | :x:                  | cope                                     | TODO (not decided)                   |
| whereis              | :x:                  | cwrapper                                 | TODO (not decided)                   |
| who                  | :x:                  | cwrapper, cope                           | TODO (not decided)                   |
| xferlog              | :x:                  | cwrapper, ccze                           | TODO (not decided)                   |
| xrandr               | :x:                  | cope                                     | TODO (not decided)                   |
