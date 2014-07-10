#--------------------------
# Author: Christian A. Damo
# date: 2014-06-17
# rev by: Reed Shinsato 
# rev date: 2014-07-09
#--------------------------
#
# Patch Notes: Fixed the path problems and problem data from NI logs
#
#--------------------------
import os
import subprocess
import os
import csv
import shutil
import sys
import xmlrpclib
import NISignalExpressExtractClass as NI

def return_errors_list():
    return errors_list

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
    
errors_list = []
    
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
    project_directory = target_directories
    data_directory = os.path.join(project_directory, target_directory)
    target_files = os.listdir(data_directory)
    if len(target_files) == 6:
        print "working on " + target_directory + " files..."
        for target_file in target_files:
            directory_path = os.path.join(target_directories, target_directory)
            file_path = os.path.join(directory_path, target_file)
            #with open(file_path, "rb") as handle:
                # binary_data = xmlrpclib.Binary(handle.read())
                # server.push_file_to_server(binary_data, target_directory, target_file)
    try:
        ExtractTarget = NI.NISignalExpressExtract(data_directory, project_directory)
        ExtractTarget.calibrate_output()
    except Exception, e:
        print "Error:"
        print "\t", e
        print "skipping...\n"
        errors_list.append(e)
    new_row.append(target_directory)

    try:
        print ExtractTarget.return_output_path()
        # ADD CSV PUSH HERE

        ExtractTarget.clean_folder()
    except:
        pass
input_file.close()
output_file = open("archive.csv", "wb")
writer = csv.writer(output_file)
writer.writerow(new_row)
output_file.close()
