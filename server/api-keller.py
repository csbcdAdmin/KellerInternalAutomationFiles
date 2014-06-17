#----------------------
# Author: Christian Damo
# Date: 2014-05-08
# rev.: 2014-06-17
#----------------------

from SimpleXMLRPCServer import SimpleXMLRPCServer
import psycopg2
import sys
import datetime
import os
import subprocess

address = ("", 9000)
server = SimpleXMLRPCServer(address)

def hello_world(name):
	return "Hello World, How are you doing " + name + "?"
server.register_function(hello_world)

def server_receive_file(arg):
	with open("output","wb") as handle:
		handle.write(arg.data)
		return True
server.register_function(server_receive_file)

def push_csv_to_server(arg,filename):
	path = os.path.join('Keller_indoor_csv_files',filename)
	with open(path,"wb") as handle:
		handle.write(arg.data)
		return True
server.register_function(push_csv_to_server)	

def push_file_to_server(arg,directory,filename):
	#check to see if the directory exists
	#get list of directories
	directories = os.walk('Keller_indoor_raw_data').next()[1]
	#check to see if directory is in directories
	if directory not in directories:
		path = os.path.join('Keller_indoor_raw_data',directory)
		subprocess.call(["mkdir",path])
	path = os.path.join('Keller_indoor_raw_data',directory,filename)
	with open(path,"wb") as handle:
		handle.write(arg.data)
		return True
server.register_function(push_file_to_server)

try:
	print "serving..."
	server.serve_forever()
except KeyboardInterrupt:
	print "stopping!"
	server.server_close()
