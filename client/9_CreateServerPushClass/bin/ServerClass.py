#--------------------------
# Author: Christian A. Damo
# date: 2014-06-17
# rev by: Reed Shinsato 
# rev date: 2014-07-11
#--------------------------
#
# Patch Notes: Created Server Class (need to rename to client) 
#
#--------------------------
import os
import subprocess
import os
import csv
import shutil
import xmlrpclib
import NISignalExpressExtractClass as NI

class ServerPush:
    def __init__(self, type_of_file, type_of_server, calibrate):
        self._calibrate = calibrate
        self._type_of_file = type_of_file
        self._type_of_server = type_of_server
        self._errors_list = []
        self._target_directories = self.return_files_directory()
        self._target_directories_list = os.listdir(self._target_directories)
        self._output_row = []
        self.__check_archive()
        self.__choose_type_of_push(self._type_of_file, 
                                   self._target_directories_list,
                                   self._type_of_server)
        
    def __choose_type_of_push(self, type_of_file, 
                              target_directories_list, type_of_server):
        """
            This function determines how to push the files.
        """        
        # Check the type_of_file
        # Run the appropriate function for the type_of_file
        if type_of_file == "HOBOWARE":
            self.__push_hoboware(target_directories_list, type_of_server)
        elif type_of_file == "NISIGNALEXPRESS":
            self.__push_nisignalexpress(target_directories_list, 
                                        type_of_server)
        elif type_of_file == "EGAUGE":
            self.__push_egauge(target_directories_list, type_of_server)
        else:
            print "Error: Not an appropriate type_of_file"
            self._input_file.close()            
            quit()
            
        
    def __check_archive(self):
        """
            This function checks if the data is in the archive log,
            and skips the data if it is.
        """
        # Check if the data is already logged
        # If it isn't create a new output row
        try:
            input_file = open("archive.csv", "r")
            reader = csv.reader(input_file)
            archive_directories = reader.next()
            input_file.close()
            self._output_row = list(archive_directories)
            for archived_directory in archive_directories:
                self._target_directories_list.remove(archived_directory)
            print self._target_directories
            input_file.close()
        except:
            self._output_row = []
            print "no archived directories this time..."
    
    def __push_hoboware(self, target_directories_list, type_of_server):
        pass
    
    def __push_nisignalexpress(self, target_directories_list, type_of_server):
        """
            This function pushes the NISignalExpressClass data to the server.
        """
        # Create a list of target directories
        # For each target directory in the list
        #    Get the path of the data directory
        #    Check if the data directory is valid 
        #    (NI logs have exactly 6 files for correct logs)
        #    Extract the data from the data directory
        #    Push the data to the server
        target_directory_list = []
        for target_directory in target_directories_list:
            target_directory_list.append(target_directory)

        for target_directory in target_directory_list:
            project_directory = self._target_directories
            data_directory = os.path.join(project_directory, target_directory)
            target_files = os.listdir(data_directory)
            if len(target_files) == 6:
                print "working on " + target_directory + " files..."
                # for target_file in target_files:
                    # REPLACES THESE WITH TYPE OF SERVER
                    #directory_path = os.path.join(self._target_directories, target_directory)
                    #file_path = os.path.join(directory_path, target_file)
                    #with open(file_path, "rb") as handle:
                    # binary_data = xmlrpclib.Binary(handle.read())
                    # server.push_file_to_server(binary_data, target_directory, target_file)
            try:
                ExtractTarget = NI.NISignalExpressExtract(data_directory, 
                                                          project_directory)
                if self._calibrate == True:
                    ExtractTarget.calibrate_output()
            except Exception, e:
                print "Error:"
                print "\t", e
                print "skipping...\n"
                self._errors_list.append((data_directory, e))
            self._output_row.append(target_directory)

            try:
                print ExtractTarget.return_output_path()
                # ADD CSV PUSH HERE
                ExtractTarget.clean_folder()
            except:
                pass
            
        output_file = open("archive.csv", "wb")
        writer = csv.writer(output_file)
        writer.writerow(self._output_row)
        output_file.close()
        
    def __push_eguage(self, target_directories_list, type_of_server):
        pass
    
    def __type_of_server(self, type_of_server):
        if type_of_server == "LOCAL":
            self.__push_to_local()
        else:
            self.__push_to_ip()
        
    def __push_to_local(self):
        pass
    
    def __push_to_ip(self):
        pass     
        
    def return_errors_list(self):
        """
            This function returns the errors from extracting the data.
        """
        # Return the list of errors
        return self._errors_list
        
    def return_bin_directory(self):
        """
            This returns the current working directory for the script.
            Since, the scripts should all be in the bin directory.
        """
        # Return the path of the script directory
        return os.path.dirname(os.path.abspath(__file__))
        
    def return_files_directory(self):
        """
            This returns the directory of the log files.    
        """
        # Find the script directory
        # Go to the parent directory of the script directory
        # Find the Data Files directory
        # Return the Data Files directory
        script_directory = self.return_bin_directory()
        script_directory_list = str(script_directory).split("\\")
        files_directory_list = script_directory_list[:-1]
        files_directory_list.append("Data Files")
        files_directory = "\\".join(files_directory_list)
        files_directory += "\\"
        return os.path.dirname(files_directory)


        