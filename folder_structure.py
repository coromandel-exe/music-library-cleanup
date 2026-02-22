from sorting_algos import create_folder, Folder

# Create root folder object for your target directory.
target_folder = Folder(name='target_dir')

# Use the create_folder function with the name, parent folder and branching conditions parameters to create the folder structure you want.
starter = create_folder('starters', target_folder, {'comment': ['Start']})
slow = create_folder('slow', starter, {'bpm': (0, 100)})
fast = create_folder('fast', starter, {'bpm': (100, 300)})
