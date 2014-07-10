#----
# File: pathtest.py
# By  : Reed Shinsato
# Date: 2014-07-09
#----
"""
    This is a test script to check where the paths are for the folders
"""

import os

script_directory = os.path.dirname(os.path.abspath(__file__))
script_directory_list = str(script_directory).split("\\")
files_directory_list = script_directory_list[:-1]
files_directory_list.append("Data Files")
files_directory = "\\".join(files_directory_list)
files = os.listdir(files_directory)

print "\n"
print "Script Directory: ", script_directory
print "Files in Script Directory: ", os.listdir(script_directory)
print "\n"
print "Files Directory: ", files_directory
print "Files in Files Directory: ", os.listdir(files_directory)
print "\n" 
