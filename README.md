#collectd-nagios
===============

## A set of collectd-nagios plugins ([Nagaconda](http://code.google.com/p/nagaconda/) required)
They connect to the unixsocket of [Collectd](https://collectd.org/) and format the results in a format compatible with
[Shinken](http://www.shinken-monitoring.org/), [Nagios](http://www.nagios.org), [Centreon](http://www.centreon.com/) and [Icinga](https://www.icinga.org/)

* collectd.py (comes from Collectd "contrib" package) Collectd PYTHON API
* collectd_discovery.py -- Discovery script for [Shinken](http://www.shinken-monitoring.org/)
* check_fs_collectd.py

Usage: check_fs_collectd.py -H HOST [-S SOCKET] [-M MOUNTS] [-v VERSION] [-w WARNING] [-c CRITICAL]

Plugin to check partition usage from collectd

    Options:
    -h, --help            show this help message and exit<br>
    -V                    show program's version number and exit
    --verbose             Get more verbose status output. Can be specified up to three times
   
    -H HOST, --host=HOST  host to check.
    -S SOCKET, --socket=SOCKET       Socket to connect to. (default=/var/run/collectd-unixsock)
    -M MOUNTS, --mounts=MOUNTS        Mount-points to check (default=all)
    -v VERSION, --version=VERSION     Collectd version default=5.x
    
    -w WARNING, --warning=WARNING     Set the warning notification level.
    -c CRITICAL, --critical=CRITICAL  Set the critical notification level.



* check_mem_collectd.py -h

Usage: check_mem_collectd.py -H HOST [-S SOCKET] [-w WARNING] [-c CRITICAL]

Plugin to check memory usage from collectd

    Options:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit
    -v, --verbose         Get more verbose status output. Can be specified up to three times
    
    -H HOST, --host=HOST  host to check.
    -S SOCKET, --socket=SOCKET  Socket to connect to. (default=/var/run/collectd-unixsock)
    -w WARNING, --warning=WARNING           Set the warning notification level.
    -c CRITICAL, --critical=CRITICAL        Set the critical notification level.
    
* check_interfaces_collectd.py

Usage: check_interfaces_collectd.py -H HOST [-S SOCKET] [-I INTERFACES] [-v VERSION] [-w WARNING] [-c CRITICAL]

Plugin to check swap usage from collectd

    Options:
    -h, --help            show this help message and exit
    -V                    show program's version number and exit
    --verbose             Get more verbose status output. Can be specified up to three times
    
    -H HOST, --host=HOST  host to check.
    -S SOCKET, --socket=SOCKET                      Socket to connect to. (default=/var/run/collectd-unixsock)
    -I INTERFACES, --interfaces=INTERFACES              Interfaces to check (default=all)
    -v VERSION, --version=VERSION                       CollectD version default=5.x
    -w WARNING, --warning=WARNING                       Set the warning notification level.
    -c CRITICAL, --critical=CRITICAL                    Set the critical notification level.
  
* check_load_collectd.py

Usage: check_load_collectd.py -H HOST [-S SOCKET] [-w WARNING] [-c CRITICAL]

Plugin to check load average from collectd
 
    Options:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit
    -v, --verbose         Get more verbose status output. Can be specified up to three times
    
    -H HOST, --host=HOST  host to check.
    -S SOCKET, --socket=SOCKET                  Socket to connect to. (default=/var/run/collectd-unixsock)
    -w WARNING, --warning=WARNING                        Set the warning notification level.
    -c CRITICAL, --critical=CRITICAL                     Set the critical notification level.  
   
   
* check_load_collectd.py 

Usage: check_load_collect.py -H HOST [-S SOCKET] [-w WARNING] [-c CRITICAL]

Plugin to check load average from collectd

    Options:
    -h, --help            show this help message and exit
    -V, --version         show program's version number and exit
    -v, --verbose         Get more verbose status output. Can be specified up to three times
    
    -H HOST, --host=HOST  host to check.
    -S SOCKET, --socket=SOCKET          Socket to connect to. (default=/var/run/collectd-unixsock)
    -w WARNING, --warning=WARNING       Set the warning notification level.
    -c CRITICAL, --critical=CRITICAL    Set the critical notification level.
    
    
## Pre-requisites
* Nagaconda
* collectd up & running, with unixsocket activated
* collectd df plugin "show reserved" behavior activated


## Install
* install pre-requisites
* download from git, and run.

## Tips
As mush as possible avoid the 'all' value for mount-points and nics. The plugins sends more unixsocket queries with 'all' value.

## Improvements & bugs
The collectd Python API hangs when asked for a item that does not exist in Collectd.
The unixsocket does accept requests on several items at once. This could reduce the number of requests sent.
