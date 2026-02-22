from track_copy import copy_files_to_root
from sorting_algos import *

# Point to source and target directories
source_dir = "source_dir" # Add path to your source directory here
target_dir = 'target_dir' # Add path to your target directory here

############# Copy marked files to drop point #############

# Create a list of tags that indicate a file should be copied to the target directory.
markers = ['Happy']
copy_files_to_root(source_dir, target_dir, markers)

############# Establish folder structure and filtering conditions #############

# Import all the Folder objects created in folder_structure.py
from folder_structure import * 

############# Scan directory for incorrect file storage #############

# Point these functions at the root folder object, not the target directory path
library_sweep(target_folder, 'folder_scan')
library_sweep(target_folder, 'file_scan')

############# Filter tracks down from current position in directory #############

library_sweep(target_folder, 'filter')
display_status(target_folder)