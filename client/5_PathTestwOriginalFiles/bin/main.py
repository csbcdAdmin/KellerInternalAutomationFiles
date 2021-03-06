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

def return_bin_directory():
    """
        This returns the current working directory for the script.
        Since, the scripts should all be in the bin directory.
    """
    # Return the path of the script directory
    return os.path.dirname(os.path.abspath(__file__))
    
def return_files_directory():
    """
        This returns the directory of the log files.    
    """
    # Find the script directory
    # Go to the parent directory of the script directory
    # Find the Data Files directory
    # Return the Data Files directory
    script_directory = return_bin_directory()
    script_directory_list = str(script_directory).split("\\")
    files_directory_list = script_directory_list[:-1]
    files_directory_list.append("Data Files")
    files_directory = "\\".join(files_directory_list)
    files_directory += "\\"
    return os.path.dirname(files_directory)
    
    
#setup the server connection for data transferring
input_file = open("archive.csv","r")
reader = csv.reader(input_file)
#test to see if the API on the HIG205 server is listening

target_directories = return_files_directory()
target_directories_list = os.listdir(target_directories)

try:
	archived_directories = reader.next()
	input_file.close()
	output_file=open("archive.csv","wb")
	writer = csv.writer(output_file)
	new_row = list(archived_directories)
	#remove all archived directories from target directories list
	for archived_directory in archived_directories:
		target_directories_list.remove(archived_directory)
	print target_directories_list
except:
	new_row=[]	
	print "no archived directories this time"

#start building the new archive.csv content

#subprocess.call(["gvim",os.path.join(directories[0],"Voltage_meta.txt")])
target_directory_list = []
for target_directory in target_directories_list:
    target_directory_list.append(target_directory)

for target_directory in target_directory_list:
    check_target = target_directories
    check_target = os.path.join(check_target, target_directory)
    target_files = os.listdir(check_target)
    if len(target_files) == 6:
        print "working on " + target_directory + " files..."
        for target_file in target_files:
            directory_path = os.path.join(target_directories, target_directory)
            print directory_path
            file_path = os.path.join(directory_path, target_file)
            #with open(file_path, "rb") as handle:
                # binary_data = xmlrpclib.Binary(handle.read())
                # server.push_file_to_server(binary_data, target_directory, target_file)
        print target_directory
        #subprocess.call(["python", "NISignalExpressExtractClass.py", directory_path])
        new_row.append(target_directory)

input_file.close()
output_file = open("archive.csv", "wb")
writer = csv.writer(output_file)
writer.writerow(new_row)
output_file.close()
