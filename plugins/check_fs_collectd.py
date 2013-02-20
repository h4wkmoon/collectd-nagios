#!/usr/bin/python
import collectd
import string
import sys

from NagAconda import Plugin

MyPlugin = Plugin("Plugin to check partition usage from collectd", "1.0")
MyPlugin.add_option('H', 'host', 'host to check.',   required=True)
MyPlugin.add_option('S','socket','Socket to connect to. (default=/var/run/collectd-unixsock)',required=False,default='/var/run/collectd-unixsock')
MyPlugin.add_option('M','mounts','Mount-points to check (default=all)',required=False,default='all')
MyPlugin.add_option('v','version','CollectD version default=5.x',required=False,default=5)

MyPlugin.enable_status('warning')
MyPlugin.enable_status('critical')
MyPlugin.start()

c = collectd.Collect(MyPlugin.options.socket)


mounts=[]
if MyPlugin.options.mounts == 'all':
		mounts=c.mounts(MyPlugin.options.host)
else:
	mounts=MyPlugin.options.mounts.split(',')
	
for mount in mounts:
	mount=mount.replace('/','_').lstrip('/_')
	if mount == '':
		mount ="root"
	if MyPlugin.options.version == '4':
		formula="100 * #"+MyPlugin.options.host+"/df/df/"+mount+"/free 0# / ( #"+MyPlugin.options.host+"/df/df/"+mount+"/used 0# + #"+MyPlugin.options.host+"/df/df/"+mount+"/free 0# ) "
	else:
		formula="100 * #"+MyPlugin.options.host+"/df-"+mount+"/df_complex-free 0# / ( #"+MyPlugin.options.host+"/df-"+mount+"/df_complex-free 0#+ #"+MyPlugin.options.host+"/df-"+mount+"/df_complex-used 0# + #"+MyPlugin.options.host+"/df-"+mount+"/df_complex-reserved 0# ) "

		
	pct_free=c.calculate(formula)
	MyPlugin.set_value('pcr_free-'+mount, pct_free,scale='%')
	



MyPlugin.finish()

