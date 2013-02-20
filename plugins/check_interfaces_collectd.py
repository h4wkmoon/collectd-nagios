#!/usr/bin/python
import collectd
import string
import sys

from NagAconda import Plugin

MyPlugin = Plugin("Plugin to check swap usage from collectd", "1.0")
MyPlugin.add_option('H', 'host', 'host to check.',   required=True)
MyPlugin.add_option('S','socket','Socket to connect to. (default=/var/run/collectd-unixsock)',required=False,default='/var/run/collectd-unixsock')
MyPlugin.add_option('I','interfaces','interfaces to check (default=all)',required=False,default='all')
MyPlugin.add_option('v','version','CollectD version default=5.x',required=False,default=5)

MyPlugin.enable_status('warning')
MyPlugin.enable_status('critical')
MyPlugin.start()

c = collectd.Collect(MyPlugin.options.socket)


interfaces=[]
if MyPlugin.options.interfaces == 'all':
		interfaces=c.interfaces(MyPlugin.options.host)
else:
	interfaces=MyPlugin.options.interfaces.split(',')

for interface in interfaces:
	if MyPlugin.options.version == '4':
		formula="#"+MyPlugin.options.host+"/interface/if_errors-"+interface+" 0#" 
		err_rx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface/if_errors-"+interface+" 1#" 
		err_tx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface/if_octets-"+interface+" 0#" 
		oct_rx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface/if_octets-"+interface+" 1#" 
		oct_tx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface/if_packets-"+interface+" 0#" 
		pkt_rx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface/if_packets-"+interface+" 1#" 
		pkt_tx=c.calculate(formula)
	else:
		formula="#"+MyPlugin.options.host+"/interface-"+interface+"/if_errors 0#" 
		err_rx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface-"+interface+"/if_errors 1#" 
		err_tx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface-"+interface+"/if_octets 0#" 
		oct_rx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface-"+interface+"/if_octets 1#" 
		oct_tx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface-"+interface+"/if_packets 0#" 
		pkt_rx=c.calculate(formula)
		formula="#"+MyPlugin.options.host+"/interface-"+interface+"/if_packets 1#" 
		pkt_tx=c.calculate(formula)
	MyPlugin.set_value('err_tx-'+interface, err_tx)
	MyPlugin.set_value('err_rx-'+interface, err_rx)
	MyPlugin.set_value('oct_tx-'+interface, oct_tx)
	MyPlugin.set_value('oct_rx-'+interface, oct_rx)
	MyPlugin.set_value('pkt_tx-'+interface, pkt_tx)
	MyPlugin.set_value('pkt_rx-'+interface, pkt_rx)



MyPlugin.finish()

