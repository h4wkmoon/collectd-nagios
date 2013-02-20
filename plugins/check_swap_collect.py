#!/usr/bin/python
import collectd
import string
import sys

from NagAconda import Plugin

MyPlugin = Plugin("Plugin to check swap usage from collectd", "1.0")
MyPlugin.add_option('H', 'host', 'host to check.',   required=True)
MyPlugin.add_option('S','socket','Socket to connect to. (default=/var/run/collectd-unixsock)',required=False,default='/var/run/collectd-unixsock')

MyPlugin.enable_status('warning')
MyPlugin.enable_status('critical')
MyPlugin.start()


formula = "#"+MyPlugin.options.host+"/swap/swap-free 0# / ( #"+MyPlugin.options.host+"/swap/swap-free 0# + #"+MyPlugin.options.host+"/swap/swap-used 0#)*100"

c = collectd.Collect(MyPlugin.options.socket)
val=c.calculate(formula)


MyPlugin.set_value('Swap free', val, scale='%')

MyPlugin.finish()

