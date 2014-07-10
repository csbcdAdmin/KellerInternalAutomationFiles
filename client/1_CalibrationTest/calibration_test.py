#--------
# File: calibration_test.py
# By  : Reed Shinsato
# Date: 2014-07-09
#--------
"""
    This is a test script to check if the callibrations are added properly.
"""
import csv

sensor_id = "ai0"
value = 2
value = float(value)

calibration_filename = "NICalibrate.csv"
calibration_file = open(calibration_filename, "r")

reader = csv.reader(calibration_file)

row = reader.next()

for row in reader:
    if row[0] == sensor_id:
        premultiplier = float(row[1])
        preoffset = float(row[2])
        multiplier = float(row[3])
        offset = float(row[4])
print premultiplier, preoffset, multiplier,offset
value = multiplier * ((premultiplier * value) + preoffset) + offset
print value


calibration_file.close()
