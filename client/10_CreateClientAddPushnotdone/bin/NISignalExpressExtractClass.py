#-------------------
# Author: Christian A. Damo
# file name: NISignalExpressExtractClass.py
# rev. by: Reed Shinsato
# rev. date: 2014-07-11
#------------------
#
# Patch Notes: Cleaned up class
#
#------------------
"""
    This script convertes .tdms files from NISignalExpress into .csv files.
    Then, it pushes the .csv files to a server with a specified ip.
"""

# Import Libraries
from nptdms import TdmsFile
import sys
import os
import datetime
import csv 

# Create Classes
class GroupChannel:
    """
        This class holds the group and channel names from a metafile.
    """
    def __init__(self, meta_filename):
        print 
        self._channel_type = ""
        self._start_time = datetime.datetime.now()
        self._meta_filename = meta_filename
        self._group_name = ""
        self._channel_names = []
        self.__get_group_name(self._meta_filename)
        # self.__str__()
        
    def __str__(self):
        print "\nCalling GroupChannels __str__()"
        print "Type: ", self._channel_type
        print "Start: ", self._start_time
        print "Group Name: ", self._group_name
        print "Channel Names: \n\n", self._channel_names
	
    def __get_start_and_names(self, meta_filename, temp_names):
        """
            This function stores the start time and channel names
        """
        # Check the meta_file for " ", which is the line of the channel names.
        # Check the meta_file for "Log start time", which holds the start time.
        meta_file = open(meta_filename)        
        for line in meta_file:
            if line[0] == " ":
	           temp_names.append(line)
            if "Log start time" in line:
	          self._start_time = self.__start_convert_to_datetime_object(line)
        meta_file.close()

    def __start_convert_to_datetime_object(self, line):
        """
            This function turns the given line into a datetime object.
        """
        # Find each element of the given line
        # Turn the elements into a datetime object
        # Return the datetime object
        line = line.split(" ")
        date = line[3]
        date = date.split("/")
        year = int(date[2])
        day = int(date[1])
        month = int(date[0])
        time = line[4]
        time = time[:-1]
        time = time.split(":")
        hour = int(time[0])
        minute = int(time[1])
        second = time[2].split(".")
        second = int(second[0])	
        begin_time = datetime.datetime(year, month, day, hour, minute, second)
        return begin_time

    def __get_group_name(self, meta_filename):
        """
            This functions determines the group_name
        """
        # Get the start time and channel names
        # Determine the timestamp
        # Store the channel names
        # Determine the data type
        # Create the group name
        temp_names = []
        self.__get_start_and_names(meta_filename, temp_names)
        for line in temp_names:
            temp_line = line.split("-")
            timestamp = temp_line[0]
            timestamp = timestamp[5: -1]
            channel_name = temp_line[-1]
            channel_name = channel_name[1: -1]
            self._channel_names.append(channel_name)
            data_type = temp_line[1]
            data_type = data_type[1: -1]
            self._channel_type = data_type
            self._group_name = (timestamp + " - " + data_type + 
                                " - " + "All Data")

    def return_group_name(self):
        """
            This function returns the group name.
        """
        # Retunr group_name
        return self._group_name

    def return_channel_names(self):
        """
            This function returns the channel names.
        """
        # Return channel_names
        return self._channel_names

    def return_start_time(self):
        """
            This function returns the start time.
        """
        # Return start_time
        return self._start_time

class NISignalExpressExtract:
    def __init__(self, file_location, output_file_location):
        self._file_location = file_location        
        self._output_file_location = output_file_location
        self._meta_voltage_filename = (os.path.join(self._file_location, 
                                                    "Voltage_meta.txt"))
        self._meta_current_filename = (os.path.join(self._file_location, 
                                                    "Current_meta.txt"))
        self._tdms_voltage_filename = (os.path.join(self._file_location, 
                                                    "Voltage.tdms"))
        self._tdms_current_filename = (os.path.join(self._file_location, 
                                                    "Current.tdms"))
        self._channel_names = []
        self._tdms_filenames = []
        self._GroupChannels = []

        try:
            self.__check_for_group_channels(self._tdms_voltage_filename, 
                                            self._tdms_filenames, 
                                            self._meta_voltage_filename, 
                                            self._channel_names, 
                                            self._GroupChannels)
        except:
            print "Note: No Voltage Files"
            
        try:
            self.__check_for_group_channels(self._tdms_current_filename, 
                                            self._tdms_filenames, 
                                            self._meta_current_filename, 
                                            self._channel_names, 
                                            self._GroupChannels)
        except:
            print "Note: No Current Files"
        
        self._tdms_to_csv_filename = "output1.csv"
        self.__tdms_to_csv_file(self._channel_names, 
                                self._tdms_filenames, 
                                self._GroupChannels, 
                                self._tdms_to_csv_filename)        
        self.__reshape(self._channel_names)        
        self._output_filename = "output2.csv"

    def __check_for_group_channels(self, tdms_filename, tdms_filenames, 
                                   meta_filename, channel_names, 
                                   GroupChannels):
        """
            This function creates the GroupChannels.
        """
        # Create a tdms object
        # Create a GroupChannel object
        # Add to the list of channel_names
        # Add to the list of tdms_filenames
        # Add to the list of GroupChannels
        tdms_file = TdmsFile(tdms_filename)
        TypeGroupChannel = GroupChannel(meta_filename)
        type_channel_names = TypeGroupChannel.return_channel_names()
        channel_names.append(type_channel_names)
        tdms_filenames.append(tdms_file)
        GroupChannels.append(TypeGroupChannel)
        
        
    def __add_output_file_location(self, filename):
        """
            This function returns the filename in the output directory.
        """
        # Return the joined path of the output directory and the filename
        return os.path.join(self._output_file_location, filename)

    
    def __tdms_to_csv_file(self, channel_names, tdms_filenames, 
                           GroupChannels, output_name):
        """
            This function will convert .tdms files into .csv files
        """
        # Get the data from the .tdms file
        #    Create a channel object from a tdms object
        #    Get the data from the channel
        #    Get the time from the channel
        # Clean up the channel_names to be a single array 
        # Save the data into the output file
        #    Save the timestamp using delta from the start_time
        #    Save the data in a row relative to the channel_id column 
        
        datas = []
        times = []
        for channel_names_index in range(0, len(channel_names)):
            for channel_name in channel_names[channel_names_index]:
                channel = (tdms_filenames[channel_names_index].
    		  object(GroupChannels[channel_names_index].
    		  return_group_name(), channel_name))
                data = channel.data
                datas.append(data)
                times = channel.time_track()
        
        temp_channel_names = []
        for channel_names_index in range(len(channel_names)):
            for name in channel_names[channel_names_index]:
                temp_channel_names.append(name)
        
        channel_names = []
        channel_names = temp_channel_names
      
        
        output_file = open(self.__add_output_file_location(output_name), "wb")
        writer = csv.writer(output_file)
        
        new_row = list(channel_names)
        new_row.insert(0, "timestamp")
        writer.writerow(new_row)

        #iterates through each time element
        for times_index in range(len(times)):
            #created delta object
            delta = datetime.timedelta(seconds = times[times_index] + 1)
            #creates the actual printed time
            current_time = GroupChannels[0].return_start_time() + delta
            #creates new line with time as element 0
            new_row = [current_time]
            #iterating through the datas list          
            for datas_index in range(len(datas)):
                data = datas[datas_index][times_index]
                new_row.append(data)
            writer.writerow(new_row) 
            #print new_row
            #print len(new_row)
            #raw_input("Press Enter to continue...")   
        output_file.close()
   
    
    def __reshape(self, channel_names):
        """
            This function reshapes the data to a specific table format.
        """
        # Find the correct input file
        # Create an output file
        # Write the header
        # Clean up the channel_names
        # Write the output row with the correct format
        #    Add time to the output row
        #        Add the channel_names to the row
        #        Add the data to the row
        #        Write the row with [time, channel_names, data]
        input_file = (open(self.__add_output_file_location(
                      self._tdms_to_csv_filename), "r"))
        reader = csv.reader(input_file)
        
        output_filename = "output2.csv"
        output_file = (open(self.__add_output_file_location(
                       output_filename), "wb"))
        writer = csv.writer(output_file)
        
        reader.next()
        new_row = ["datetime", "position", "value"]
        writer.writerow(new_row)
        
        temp_channel_names = [] 
        for channel_names_index in range(len(channel_names)):
            for names in channel_names[channel_names_index]:
                temp_channel_names.append(names)
        channel_names = []
        channel_names = temp_channel_names
        new_channel_names = []        
        for name in channel_names:
            name = name.split("_")
            name = name[1]
            new_channel_names.append(name)
            
        for row in reader:
            current_time = row[0]
            row = row[1:]
            for new_channel_names_index in range(len(new_channel_names)):                
                new_row = []
                new_row.append(current_time)
                new_row.append(new_channel_names[new_channel_names_index])
                new_row.append(float(row[new_channel_names_index]))
                writer.writerow(new_row)

        input_file.close()
        output_file.close()

    
    def add_calibration(self, sensor_id, premultiplier, 
                        preoffset, multiplier, offset):
        """
            This function adds a calibration to NICalibrate.csv.
        """
        # Open the calibration file
        # Check if the sensor_id is in the calibration file
        # Delete the calibration for the sensor_id
        # if it is in the calibration file
        # Append the new calibration to the calibration file
        calibration_filename = "NICalibrate.csv"
        delete_id = False    
        
        with open(calibration_filename, "r") as calibration_file:
            for row in csv.reader(calibration_file):
                if sensor_id == row[0]:
                    delete_id = True
        
        if delete_id == True:
            self.delete_calibration(sensor_id)
        
        with open(calibration_filename, "a") as calibration_file:
            row = (str(sensor_id) + "," +
                   str(premultiplier) + "," +
                   str(preoffset) + "," +
                   str(multiplier) + "," +
                   str(offset))
            calibration_file.write(row)
                  
        
    def delete_calibration(self, sensor_id):
        """
            This function deletes a calibration from NICalibrate.csv.
        """
        # Copy NICalibrate.csv into a temp.csv
        # skipping the sensor_id to be deleted
        # Delete the old calibration file NICalibrate.csv
        # Rename temp.csv into the new calibration file NICalibrate.csv
        calibration_filename = "NICalibrate.csv"
        temp_filename = "temp.csv"
        with open(temp_filename, "wb") as temp_file:   
            with open(calibration_filename, "r") as calibration_file:
                for row in csv.reader(calibration_file):
                    if sensor_id != row[0]:
                        csv.writer(temp_file).writerow(row)
                        
        os.remove(calibration_filename)
        os.rename(temp_filename, calibration_filename) 
    
    
    def __calibrate_value(self, sensor_id, value):
        """
            This function calibrates the value of the senor_id.
        """
        # Open the calibration file
        # Check if the sensor_id of the calibration file
        # to determine the multipliers and offsets 
        # Return the value with calibration
        calibration_filename = "NICalibrate.csv"
        calibration_file = open(calibration_filename, "r")
        reader = csv.reader(calibration_file)
        
        value = float(value)
        
        premultiplier = 1.0
        preoffset = 0.0
        multiplier = 1.0
        offset = 0.0    
        
        row = reader.next()
        for row in reader:
            if row[0] == str(sensor_id):
                premultiplier = float(row[1])
                preoffset = float(row[2])
                multiplier = float(row[3])
                offset = float(row[4])
        
        value = multiplier * ((premultiplier * value) + preoffset) + offset
        
        calibration_file.close()
        return value

    def clean_folder(self):
        """
            This function deletes all the output files created.
        """
        # Remove the 1st output
        # Remove the 2nd output
        # Remove the calibrated output
        os.remove(self.__add_output_file_location("output1.csv"))
        os.remove(self.__add_output_file_location("output2.csv"))
        try:
            os.remove(self.__add_output_file_location(self._output_filename))
        except:
            pass
    
    def calibrate_output(self):
        """
            This function calibrates the output for given callibrations.
        """
        # Find the correct input file
        # Create a output file for the calibrated values
        # Write the header row
        # Go through each input row and callibrate the value of the row
        # Write the callibrated row to the output file
        input_filename = "output2.csv"
        input_file = (open(self.__add_output_file_location(
                      input_filename), "r"))
        reader = csv.reader(input_file)
                      
        output_pathname = self._file_location.split("\\")[-1]
        output_filename = str(output_pathname) + "_output3.csv"
        self._output_filename = output_filename        
        output_file = (open(self.__add_output_file_location(
                       output_filename), "wb"))
        writer = csv.writer(output_file)
        
        new_row = reader.next()
        writer.writerow(new_row)
        
        for row in reader:
        	value = self.__calibrate_value(row[1], row[2])
        	new_row = [row[0], row[1], round(value,5)]
        	writer.writerow(new_row)
         
        input_file.close()
        output_file.close()
        
        
    def return_output_path(self):
        """
            This function returns the output path.
        """
        # Return the path of the output file
        return os.path.join(self._output_file_location, self._output_filename)
