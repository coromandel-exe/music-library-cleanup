from sorting_algos import create_folder, Folder

######################### Folder structure conventions #########################

# Using the create_folder function, you can create a folder structure with any number of levels and branching conditions.
# The branching conditions are defined as a dictionary where the keys are the tag properties to filter on and the values are the conditions for those properties.
# Subfolders inherit local conditions from their parent folders.

# Current condition keys include:
#   - composer: A string (e.g., 'Happy') [this is the deault location used for marking files to be copied to the target directory]
#   - bpm:      A tuple of two integers representing the minimum and maximum BPM (e.g., (0, 100))
#   - comment:  A list or tuple of strings (e.g., ['Jazzy', 'Chill']) 
#   - genre:    A list or tuple of strings (e.g., ['House', 'Techno']))
#   - lyricist: A list or tuple of strings (e.g., ['Build', 'Release']))

#   Note: list indicates 'either or' conditions, while tuple indicates 'both and' conditions.
#   (e.g., ['Jazzy', 'Chill'] = 'Jazzy' OR 'Chill'; ('Jazzy', 'Chill') = 'Jazzy' AND 'Chill')

################################################################################

# Create root folder object for your target directory.
target_folder = Folder(name='target_dir')

# Use the create_folder function with the name, parent folder and branching conditions parameters to create the folder structure you want.
starter = create_folder(name='starters', parent_node=target_folder, local_conditions={'comment': ['Start']})
slow = create_folder(name='slow', parent_node=starter, local_conditions={'bpm': (0, 100)})
fast = create_folder(name='fast', parent_node=starter, local_conditions={'bpm': (100, 300)})
