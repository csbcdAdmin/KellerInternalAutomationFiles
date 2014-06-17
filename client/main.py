#--------------------------
# Author: Christian A. Damo
# date: 2014-06-17
#--------------------------

import os
import subprocess
import os
import csv
import shutil
import sys
import xmlrpclib

#setup the server connection for data transferring
server = xmlrpclib.Server('http://128.171.152.55:9000')
inputFile = open("archive.csv","r")
reader=csv.reader(inputFile)

#test to see if the API on the HIG205 server is listening
try:
	server.hello_world("Christian")
except:
	quit()


targetDirectories = os.walk('.').next()[1]
try:
	archivedDirectories = reader.next()
	inputFile.close()
	outputFile=open("archive.csv","wb")
	writer = csv.writer(outputFile)
	newRow = list(archivedDirectories)
	#remove all archived directories from target directories list
	for archivedDirectory in archivedDirectories:
		targetDirectories.remove(archivedDirectory)
except:
	newRow=[]	
	print "no archived directories this time"

#start building the new archive.csv content

#subprocess.call(["gvim",os.path.join(directories[0],"Voltage_meta.txt")])
for targetDirectory in targetDirectories:
	targetFiles = os.listdir(targetDirectory)
	#if it is a proper target directory
	if len(targetFiles) == 6:
		print "working on "+targetDirectory+" files"
		#transfer each file over to the server
		for targetFile in targetFiles:
			path = os.path.join(targetDirectory,targetFile)
			with open(path,"rb") as handle:
				binary_data = xmlrpclib.Binary(handle.read())
				server.push_file_to_server(binary_data,targetDirectory,targetFile)
				handle.close()
		#run the extraction and upload it to the server
		subprocess.call(["python","extractData_r3cd.py",targetDirectory])
		#record that it was archived
		newRow.append(targetDirectory)

#write the list of directories uploaded to file
writer.writerow(newRow)
