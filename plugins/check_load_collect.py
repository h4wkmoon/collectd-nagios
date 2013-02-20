#!/usr/bin/python
import collectd
import string
import sys

from NagAconda import Plugin

MyPlugin = Plugin("Plugin to check load average from collectd", "1.0")
MyPlugin.add_option('H', 'host', 'host to check.',   required=True)
MyPlugin.add_option('S','socket','Socket to connect to. (default=/var/run/collectd-unixsock)',required=False,default='/var/run/collectd-unixsock')

MyPlugin.enable_status('warning')
MyPlugin.enable_status('critical')
MyPlugin.start()

c = collectd.Collect(MyPlugin.options.socket)

formula = "#"+MyPlugin.options.host+"/load/load 0#"
val=c.calculate(formula)


MyPlugin.set_value('Load', val)

MyPlugin.finish()

