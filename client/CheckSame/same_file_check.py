#--------------
# File: same_file_check.py
# By  : Reed Shinsato
# Date: 2014-07-09
#--------------

"""
    This script does a simple check for two .csv files
    to determine if they are the same.
    Two files: correct.py
               check.py
"""
# Open the two files
# Check each line at a time
# Record any differences
# Return the number of differences
import csv

input_file1 = open("correct.csv", "r")
reader1 = csv.reader(input_file1)

input_file2 = open("check.csv", "r")
reader2 = csv.reader(input_file2)

failed_check = []
for row1 in reader1:
	row2 = reader2.next()
	if row1 != row2:
		failed_check.append((row1, row2))
		print "Failed"
		print "correct:", row1
		print "check:  ", row2
print len(failed_check)

input_file1.close()
input_file2.close()
