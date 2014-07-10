#-------------------
# Author: Christian A. Damo
# file name: NISignalExpressExtractClass.py
# rev. by: Reed Shinsato
# rev. date: 2014-07-07
#------------------
#
# Patch Notes: Changing to a Class 
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
        self._channel_type = ""
        self._meta_file = open(meta_filename)
        self._temp_names = []
        self._start_time = datetime.datetime.now()
        self._group_name = ""
        self._channel_names = []
        self.__get_group_name()
        self._meta_file.close()
        #self.__str__()
    def __str__(self):
        print "\nCalling GroupChannels __str__()"
        print "Type: ", self._channel_type
        print "Start: ", self._start_time
        print "Group Name: ", self._group_name
        print "Channel Names: \n\n", self._channel_names
	
    def __get_start_names(self):
        """
            This function stores the start time and channel names
        """
        # Check the meta_file for " ", which is the line of the channel names.
        # Check the meta_file for "Log start time", which holds the start time.
        for line in self._meta_file:
            if line[0] == " ":
	           self._temp_names.append(line)
            if "Log start time" in line:
	          self._start_time = self.__start_convert_to_datetime_object(line)

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

    def __get_group_name(self):
        """
            This functions determines the group_name
        """
        # Get the start time and channel names
        # Determine the timestamp
        # Store the channel names
        # Determine the data type
        # Create the group name
        self.__get_start_names()
        for line in self._temp_names:
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
        return self._group_name

    def return_channel_names(self):
	return self._channel_names

    def return_start_time(self):
        return self._start_time

def tdms_to_csv_file(channel_names, tdms_filenames, GroupChannels, output_name):
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

    output_file = open(output_name, "wb")
    writer = csv.writer(output_file)
    
    new_row = list(channel_names)
    new_row.insert(0, "timestamp")
    writer.writerow(new_row)
    for times_index in range(len(times)):
        delta = datetime.timedelta(seconds = times[times_index] + 1)
        current_time = GroupChannels[0].return_start_time() + delta
        new_row = [current_time]
        for datas_index in range(len(datas)):
            data = datas[datas_index][times_index]
            new_row.append(data)
    	writer.writerow(new_row) 
    output_file.close()

def calibrate_value(sensor_id, value):
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

# MAIN
# Find all the NISignalExpress Log Files
meta_voltage_filename = os.path.join(sys.argv[1], "Voltage_meta.txt")
meta_current_filename = os.path.join(sys.argv[1], "Current_meta.txt")
tdms_voltage_filename = os.path.join(sys.argv[1], "Voltage.tdms")
tdms_current_filename = os.path.join(sys.argv[1], "Current.tdms")

# Create TDMS objects
tdms_voltage_file = TdmsFile(tdms_voltage_filename)
tdms_current_file = TdmsFile(tdms_current_filename)

# Create Group Channel objects
VoltageGroupChannel = GroupChannel(meta_voltage_filename)
CurrentGroupChannel = GroupChannel(meta_current_filename)

# Find channel names
voltage_channel_names = VoltageGroupChannel.return_channel_names()
current_channel_names = CurrentGroupChannel.return_channel_names()

channel_names = []
channel_names.append(voltage_channel_names)
channel_names.append(current_channel_names)

tdms_filenames = []
tdms_filenames.append(tdms_voltage_file)
tdms_filenames.append(tdms_current_file)

GroupChannels = []
GroupChannels.append(VoltageGroupChannel)
GroupChannels.append(CurrentGroupChannel)


# Create a csv from the tdms file
tdms_to_csv_filename = "output1.csv"
tdms_to_csv_file(channel_names, tdms_filenames, GroupChannels, tdms_to_csv_filename)

# Reshape the file 
input_file = open(tdms_to_csv_filename, "r")
output_filename = "output2.csv"
output_file = open(output_filename, "wb")

reader = csv.reader(input_file)
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

# Calibrate 
input_filename = "output2.csv"
input_file = open(input_filename, "r")
output_filename = str(sys.argv[1]) + "_output3.csv"
output_file = open(output_filename, "wb")

reader = csv.reader(input_file)
writer = csv.writer(output_file)

new_row = reader.next()
writer.writerow(new_row)
for row in reader:
	value = calibrate_value(row[1], row[2])
	new_row = [row[0], row[1], round(value,5)]
	writer.writerow(new_row)
input_file.close()
output_file.close()

#os.remove(output_filename)
os.remove("output1.csv")
os.remove("output2.csv")

