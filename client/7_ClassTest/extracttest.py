#-------------------------
# File: extracttest.py
# By  : Reed Shinsato
# Date: 2014-07-09
#-------------------------


import NISignalExpressExtractClass
import os

script_path = os.path.dirname(os.path.abspath(__file__))

target = os.listdir(script_path)[0]

path = os.path.join(script_path, target)
print path

Extract = NISignalExpressExtractClass.NISignalExpressExtract(path)
print Extract.return_output_path()
Extract.calibrate_output()
print Extract.return_output_path()
