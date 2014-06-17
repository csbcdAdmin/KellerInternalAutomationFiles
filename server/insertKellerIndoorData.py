#!/usr/bin/env python
import subprocess
import shutil
import os

#set global variables
tableName = "keller_indoor_data"


#create the script that will run to insert
#the csv files
outputFilename = "/usr/local/smb-share/1.Projects/1.12.NaturalVentilation/Keller_indoor_csv_files/insert.psql"
outputFile = open(outputFilename,"wb")

#get the files that's in the folder
files = os.listdir("/usr/local/smb-share/1.Projects/1.12.NaturalVentilation/Keller_indoor_csv_files/")
archivedFiles = os.listdir("/usr/local/smb-share/1.Projects/1.12.NaturalVentilation/Keller_indoor_csv_files/archive/")


#write the psql command lines to the script
for file_ in files:
	if file_ not in archivedFiles:
		if file_.endswith(".csv"):
			line = "\COPY "+tableName+" FROM '/usr/local/smb-share/1.Projects/1.12.NaturalVentilation/Keller_indoor_csv_files/"+file_+"' DELIMITER ',' CSV HEADER;\n"
			outputFile.write(line)
		

outputFile.close()


#run psql script
subprocess.call(["psql","natural_ventilation","-f","/usr/local/smb-share/1.Projects/1.12.NaturalVentilation/Keller_indoor_csv_files/insert.psql"])

#move file to archive
for file_ in files:
	if file_.endswith(".csv"):
		shutil.move("/usr/local/smb-share/1.Projects/1.12.NaturalVentilation/Keller_indoor_csv_files/"+file_,"/usr/local/smb-share/1.Projects/1.12.NaturalVentilation/Keller_indoor_csv_files/archive/"+file_)
