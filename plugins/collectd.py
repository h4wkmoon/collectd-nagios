#-*- coding: ISO-8859-1 -*-
# collect.py: the python collectd-unixsock module.
#
# Requires collectd to be configured with the unixsock plugin, like so:
#
# LoadPlugin unixsock
# <Plugin unixsock>
#   SocketFile "/var/run/collectd-unixsock"
#   SocketPerms "0775"
# </Plugin>
#
# Copyright (C) 2008 Clay Loveless <clay@killersoft.com>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the author be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import socket, string, re

class Collect(object):

    def __init__(self, path='/var/run/collectd-unixsock'):
        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._path =  path
        self._sock.connect(self._path)
        
    def list(self):
        numvalues = self._cmd('LISTVAL')
        lines = []
        if numvalues:
            lines = self._readlines(numvalues)
        return lines
        
    def get(self, val, flush=True):
        numvalues = self._cmd('GETVAL "' + val + '"')
        lines = []
        if numvalues:
            lines = self._readlines(numvalues)
        if flush:
            self._cmd('FLUSH identifier="' + val + '"')
        return lines
            
    def _cmd(self, c):
        self._sock.send(c + "\n")
        stat = string.split(self._readline())
        status = int(stat[0])
        if status:
            return status
        return False
    
    '''
    _readline and _readlines methods borrowed from the _fileobject class 
    in sockets.py, tweaked a little bit for use in the collectd context.
    '''
    def _readline(self):
        data = ''
        buf = []
        recv = self._sock.recv
        while data != "\n":
            data = recv(1)
            if not data:
                break
            if data != "\n":
                buf.append(data)
        return ''.join(buf)
        
    def _readlines(self, sizehint=0):
        total = 0
        list = []
        while True:
            line = self._readline()
            if not line:
                break
            list.append(line)
            total = len(list)
            if sizehint and total >= sizehint:
                break
        return list
    
    def __del__(self):
        self._sock.close()    

    def gethosts(self):
		vals=self.list()
		hosts=[]
		for val in vals:
			host=val.split(' ')[1].split("/")[0]
			if not host in hosts:
				hosts.append(host)
		
		return hosts
				
    def cpu_number(self,host):
		vals=self.list()
		number=0
		for val in vals:
			if re.search("^[0-9\.]* "+host+"/cpu-[0-9]*/cpu-idle$",val):
				number = number + 1
		
		return number
	
    def mounts(self,host):
		vals=self.list()
		mounts=[]
		for val in vals:
			matches = re.findall("^[0-9\.]* "+host+"/df\-([a-zA-Z0-9_\-\.]*)/df_complex-free$",val)
			for match in  matches:
				mounts.append(match)
		
		for val in vals:
			matches = re.findall("^[0-9\.]* "+host+"/df/df\-([a-zA-Z0-9_\-\.]*)$",val)
			for match in  matches:
				mounts.append(match)
				
				
		return mounts
		
    def disks(self,host):
		vals=self.list()
		disks=[]
		for val in vals:
			matches = re.findall("^[0-9\.]* "+host+"/disk\-([a-zA-Z0-9_\-\.]*)/disk_merged$",val)
			for match in  matches:
				disks.append(match)
					
		return disks

    def interfaces(self,host):
		vals=self.list()
		interfaces=[]
		for val in vals:
			# Collectd 5
			matches = re.findall("^[0-9\.]* "+host+"/interface-([a-zA-Z0-9_\-\.]*)/if_errors$",val)
			for match in  matches:
				interfaces.append(match)
			# Collectd 4
			matches = re.findall("^[0-9\.]* "+host+"/interface/if_errors-([a-zA-Z0-9_\-\.]*)$",val)
			for match in  matches:
				interfaces.append(match)
					
		return interfaces
		
    def processes(self):
		#processes-XBMC/ps_code
		vals=self.list()
		processes=[]
		for val in vals:
			matches = re.findall("^[0-9\.]* "+host+"/processes-([a-zA-Z0-9_\-\.]*)/ps_code$",val)
			for match in  matches:
				processes.append(match)

    def discover(self):
		discovery={}
		vals=self.list()
		hosts=[]
		for val in vals:
			host=val.split(' ')[1].split("/")[0]
			if not host in hosts:
				hosts.append(host)
				discovery[host]={'interfaces':[] , 'mounts':[], 'cpus':0, 'disks':[], 'processes':[]}
				
			# Interfaces block
			# Collectd 5
			matches = re.findall("^[0-9\.]* "+host+"/interface-([a-zA-Z0-9_\-\.]*)/if_errors$",val)
			for match in  matches:
				discovery[host]['interfaces'].append(match)
			# Collectd 4
			matches = re.findall("^[0-9\.]* "+host+"/interface/if_errors-([a-zA-Z0-9_\-\.]*)$",val)
			for match in  matches:
				discovery[host]['interfaces'].append(match)
			
			# Mounts
			matches = re.findall("^[0-9\.]* "+host+"/df\-([a-zA-Z0-9_\-\.]*)/df_complex-free$",val)
			for match in  matches:
				discovery[host]['mounts'].append(match)	
			matches = re.findall("^[0-9\.]* "+host+"/df/df\-([a-zA-Z0-9_\-\.]*)$",val)
			for match in  matches:
				discovery[host]['mounts'].append(match)	
								
			# Cpu number
			if re.search("^[0-9\.]* "+host+"/cpu-[0-9]*/cpu-idle$",val):
				discovery[host]['cpus'] = discovery[host]['cpus'] + 1	
			
			
			matches = re.findall("^[0-9\.]* "+host+"/disk\-([a-zA-Z0-9_\-\.]*)/disk_merged$",val)
			for match in  matches:
				discovery[host]['disks'].append(match)
				
			matches = re.findall("^[0-9\.]* "+host+"/processes-([a-zA-Z0-9_\-\.]*)/ps_code$",val)
			for match in  matches:
				discovery[host]['processes'].append(match)
				
		return  discovery
		
		


## ## ## ## ## ## ## ## ## ## ## ## ##
# Calculates a value using other ones.
# Formula must follow a specific synthax 
# so the code can replace collectd items 
# with their current values.
# Synthax is #collectd_item collectd_value_index#
# For example :
#       #t430s-fpg/memory/memory-free 0#        is the first value in the list of the values
#                                               of the item memory/memory-free of the host ts430s-fpg
# Math operators and paranthesis can be used.
# #t430s-fpg/memory/memory-free 0# + #t430s-fpg/memory/memory-used 0#    adds the free and used memory
########################################
# Evaluate a formula
# collect : Collectd object (unixsocket)
# formula : formula to evaluate
## ## ## ## ## ## ## ## ## ## ## ## ##
    def calculate(self,formula):     
		synthax='#([a-zA-Z0-9/\-_\.]* [0-9])#'  # This is the synthax used to replace collectd items with their value.
						#       #collectd_item collectd_value_index#
						# 	For example : 
						#	#t430s-fpg/memory/memory-free 0# 	is the first value in the list of the values 
						#						of the item memory/memory-free of the host ts430s-fpg
						# Math operators and paranthesis can be used.
						# #t430s-fpg/memory/memory-free 0# + #t430s-fpg/memory/memory-used 0#    adds the free and used memory
	
		vars = re.findall(synthax,formula)
		done=[]				# This array contains the values already get from the socket.
		for match in vars:
			if not match in done:
				var,val=match.split(' ')
				
				val=int(val)
				
				result = str(float(self.get(var)[val].split("=")[1]))
				formula =  re.sub('#'+match+'#',result,formula)
				done.append(match)
				
		return float(eval(formula))

if __name__ == '__main__':
    
    '''
    Example usage:
    Collect values from socket and dump to STDOUT.
    '''
    
    c = Collect('/var/run/collectd-unixsock')
    list = c.list()

    for val in list:
        stamp, key = string.split(val)
        glines = c.get(key)
        print stamp + ' ' + key + ' ' + ', '.join(glines)
    
