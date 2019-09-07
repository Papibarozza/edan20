from indexing_toolbox import *
import os

import sys
if(len(sys.argv[1:]) < 2):
  print(Exception("Too few arguments, expected ['input_directory', 'output_directory'] but got {}".format(sys.argv[1:])))
else:
  input_folder_name,output_foldername = sys.argv[1:]

if not os.path.exists(output_foldername):
    os.makedirs(output_foldername)

generate_masterfile(input_folder_name,output_foldername+'master.idx')




