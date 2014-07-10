#-----
# File: extracttest.py
# By  : Reed Shinsato
# Date: 2014-07-09
#-----
"""
    This is a test script to check if the paths are working properly
"""
script_path = os.path.dirname(os.path.abspath(__file__))

path = os.listdir(script_path)
print path[1]

path = os.path.join(script_path, path[1])
print path
#Extract = NISignalExpressExtractClass.NISignalExpressExtract(path)
