from track_copy import copy_files_to_root
from sorting_algos import *
import os
import pathlib
from tinytag import TinyTag
import shutil

# Point to source and target directories
source_dir = "MG Library" # Add path to your source directory here
target_dir = 'Drop Point' # Add path to your target directory here

############# STEP 1: Copy marked files to drop point #############

# Create a list of tags that indicate a file should be copied to the target directory.
markers = ['MW-Solid', 'MW-Liquid', 'MW-Air', 'CC-Party', 'CC-Signature', 'CC-Classic', 'Home', 'DELETE']
copy_files_to_root(source_dir, target_dir, markers)

############# STEP 2: Establish folder structure and filtering conditions #############

# Import all the Folder objects created in folder_structure.py
from folder_structure import * 

############# STEP 3: Scan directory for incorrect file storage #############

library_sweep(drop_point, 'folder_scan')
library_sweep(drop_point, 'file_scan')

############# STEP 4: Filter tracks down from current position in directory #############

library_sweep(drop_point, 'filter')
display_status(drop_point)