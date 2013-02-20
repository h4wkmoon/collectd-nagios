#!/usr/bin/python
import collectd
import datetime

c = collectd.Collect('/var/run/collectd-unixsock')

disco=c.discover()

for host in disco:
	print host+"::collectd=1"
	for table in ['mounts','interfaces','processes','disks']:
		if disco[host][table]:
			print host+"::_"+table+"="+','.join(disco[host][table])
		
	print host+"::_cpus="+str(disco[host]['cpus'])
	

