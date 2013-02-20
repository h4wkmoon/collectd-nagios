#!/usr/bin/python
import collectd
import string
import sys

from NagAconda import Plugin

MyPlugin = Plugin("Plugin to check memory usage from collectd", "1.0")
MyPlugin.add_option('H', 'host', 'host to check.',   required=True)
MyPlugin.add_option('S','socket','Socket to connect to. (default=/var/run/collectd-unixsock)',required=False,default='/var/run/collectd-unixsock')

MyPlugin.enable_status('warning')
MyPlugin.enable_status('critical')
MyPlugin.start()


formula = "(#"+MyPlugin.options.host+"/memory/memory-free 0# + #"+MyPlugin.options.host+"/memory/memory-cached 0# + #"+MyPlugin.options.host+"/memory/memory-buffered 0# ) / ( #"+MyPlugin.options.host+"/memory/memory-free 0# + #t430s-fpg/memory/memory-cached 0# + #"+MyPlugin.options.host+"/memory/memory-buffered 0# + #"+MyPlugin.options.host+"/memory/memory-used 0#)*100"

c = collectd.Collect(MyPlugin.options.socket)
val=c.calculate(formula)


MyPlugin.set_value('mem_free', val, scale='%')

MyPlugin.finish()

