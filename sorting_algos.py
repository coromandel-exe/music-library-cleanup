import os
import shutil
import pathlib
from tinytag import TinyTag
import re
from tqdm import tqdm
import sys
from tabulate import tabulate

############################# Folder object #############################

class Folder:
    def __init__(self, name, parent_node=None, local_conditions=None):
        self.name = name
        self.parent_node = parent_node
        self._path = None
        self._local_conditions = local_conditions if local_conditions is not None else {}
        self.child_nodes = []
        if self.parent_node:
            self.parent_node.child_nodes.append(self)
        
    @property # Calculate full path based on parent node
    def path(self):
        if self.parent_node:
            return os.path.join(self.parent_node.path, self.name)
        else:
            return self.name

    @property # Aggregate conditions from parent nodes
    def conditions(self):
        inherited = {}
        if self.parent_node:
            inherited.update(self.parent_node.conditions)
        inherited.update(self._local_conditions)
        return inherited
    
    @property # Calculate depth in tree
    def depth(self):
        if self.parent_node:
            return self.parent_node.depth + 1
        else:
            return 0
        
    @property # Check if node is a leaf node
    def leaf_node(self):
        if not self.child_nodes:
            return True
        else:
            return False
        
    @property # Calculate how many files within folder
    def files(self):
        return len([item for item in pathlib.Path(self.path).iterdir() if item.is_file()])

    @property
    def total_files(self):
        file_count = 0
        queue = [self]
        while queue:
            current_folder = queue.pop(0)
            file_count += current_folder.files
            queue.extend(current_folder.child_nodes)
        return file_count
        

############################# Creation functions #############################


def create_folder(name, parent_node=None, local_conditions=None):
    new_folder = Folder(name, parent_node, local_conditions)
    if not os.path.exists(new_folder.path):
        os.makedirs(new_folder.path, exist_ok=True)
    return new_folder


############################# Extraction functions #############################


def get_track_values(track, property):
    if property == 'bpm':
        value = track.other.get(property)
        if value is not None:
            numeric_value = re.sub('[^0-9]', '', value[0])
            return float(numeric_value)
        else:
            return 0
    
    elif property == 'lyricist':
        value = track.other.get(property)
        if value is not None:
            return str(value[0]).split(', ')
        else:
            return []
    
    else:
        values = getattr(track, property)
        if values is not None:
            return str(values).replace(" ","").split(',')
        else:
            return []
        

def get_file_list(folder):
    return [item for item in pathlib.Path(folder.path).iterdir() if item.is_file()]


def get_all_real_subfolders(folder):
    return [item for item in pathlib.Path(folder.path).rglob("*") if item.is_dir()]


def get_all_expected_subfolders(folder):
    queue = [folder]
    expected_paths = []
    while queue:
        current_folder = queue.pop(0)
        for node in current_folder.child_nodes:
            expected_paths.append(pathlib.Path(node.path))
            queue.append(node)
    return (expected_paths)

def get_filter_condition_keys(folder):
    set_keys = set()
    for node in folder.child_nodes:
        set_keys.update(node.conditions.keys())
    return list(set_keys)


def find_root_folder(folder):
    current_node = folder
    while current_node.parent_node is not None:
        current_node = current_node.parent_node
    return current_node


############################# Matching functions #############################    

def composer_filter(condition, track_value):
    # If condition is substring of the track composer value, return True
    return condition in str(track_value) 


def bpm_filter(condition, track_value):
    # Normalise BPM value
    if track_value < 90:
        bpm = track_value * 2
    else:
        bpm = track_value
    # If normalised BPM is within the condition range, return True
    return bpm >= condition[0] and bpm < condition[1]


def tag_filter(conditions, track_values):
    # For tuples, all values must be present
    if isinstance(conditions, tuple):
        return all(value in track_values for value in conditions)
    # For lists, any value can be present
    elif isinstance(conditions, list):
        return any(value in track_values for value in conditions)
    else:
        return False


def condition_match(condition, track_value, key):
    # Check for match with appropriate filter function
    if key == 'composer':
        return composer_filter(condition, track_value)
    elif key == 'bpm':
        return bpm_filter(condition, track_value)
    elif key == 'comment':
        return tag_filter(condition, track_value)
    elif key == 'lyricist':
        return tag_filter(condition, track_value)
    elif key == 'genre':
        return tag_filter(condition, track_value)
    else:
        return False

############################# Execution functions #############################

def one_folder_filter(folder):
    file_list = get_file_list(folder)
    condition_keys = get_filter_condition_keys(folder)

    for entry in file_list: # Iterate over files
        track = TinyTag.get(entry)
        track_path = pathlib.Path(track.filename)
            
        for node in folder.child_nodes: # Check track values against conditions for each child node
            match_dict = {'node_matches': []} # Log the matches for each condition key

            for key in condition_keys: # Iterate over relevant condition keys
                track_value = get_track_values(track, key) # Get the track value for the condition key
                
                if key in node.conditions:
                    condition = node.conditions[key]
                    match_dict['node_matches'].append(condition_match(condition, track_value, key))
                    # Apply appropriate filter function

            # If all conditions for a node are met, move the file to that node's folder
            if all(match_dict['node_matches']):
                shutil.move(track_path, os.path.join(node.path, track_path.name))
                break 


def one_folder_scan(folder):
    file_list = get_file_list(folder)
    root_folder = find_root_folder(folder)
    
    for entry in file_list: # Iterate over files
        track = TinyTag.get(entry)
        track_path = pathlib.Path(track.filename)

        for key in folder.conditions.keys(): # Iterate over relevant condition keys
            track_value = get_track_values(track, key) # Get the track value for the condition key
            condition = folder.conditions[key]
            if not condition_match(condition, track_value, key):
                shutil.move(track_path, os.path.join(root_folder.path, track_path.name))
            else:
                continue


def redundant_folders_scan(folder, delete_empty=True):
    root_folder = find_root_folder(folder)
    actual_paths = get_all_real_subfolders(folder)
    expected_paths = get_all_expected_subfolders(folder)
    redundant_paths = set(actual_paths) - set(expected_paths)
    for path in redundant_paths:
        file_list = [item for item in pathlib.Path(path).iterdir() if item.is_file()]
        for entry in file_list:
            track = TinyTag.get(entry)
            track_path = pathlib.Path(track.filename)
            shutil.move(track_path, os.path.join(root_folder.path, track_path.name))

        # Delete empty folders intentionally
        subfolders = [item for item in path.rglob("*") if item.is_dir()] # Check to see if folder is a leaf node
        if delete_empty and subfolders == []:
            choose_delete = query_yes_no(f"About to delete the folder {path}. Continue? (y/n)")
            if choose_delete:
                os.chmod(path, 0o644)
                path.rmdir()



def library_sweep(start_folder, operation=None, delete_empty=True): # Sweep through folder tree from chosen start point, applying specified operation
    
    if not operation == 'folder_scan':
    # Breadth-first traversal algorithm (following folder objects, not filesystem)
        queue = [start_folder]
        while queue:
            current_folder = queue.pop(0)
            # print(f"Processing {current_folder.name } at depth {current_folder.depth}")
            if operation == 'filter':
                one_folder_filter(current_folder)
            elif operation == 'file_scan':
                one_folder_scan(current_folder)
            elif operation == None:
                pass
            queue.extend(current_folder.child_nodes)

    elif operation == 'folder_scan':
        # Breadth-first traversal algorithm (following filesystm, not folder objects)
        redundant_folders_scan(start_folder, delete_empty=delete_empty)
        
    print(f"Library", operation, "complete.")


############################# Display functions #############################

def query_yes_no(question, default=None):
    valid = {"y": True, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with'y' or 'n').\n")


def display_status(root_folder):
    
    # Count individual and cumulative files 
    visited = set()
    stack = [root_folder]
    library_stats = []
    leaf_node_files = 0

    # Depth-first algorithm
    while stack:
        current_folder = stack.pop()
        leaf_sign = ""
        if current_folder not in visited:
            visited.add(current_folder)
            if current_folder.leaf_node:
                leaf_node_files += current_folder.files
                leaf_sign = "!"
            library_stats.append([current_folder.depth * "---" + current_folder.name, leaf_sign, current_folder.total_files, current_folder.files])
            stack.extend(reversed(current_folder.child_nodes))
            

    try: 
        percent_sorted = round(leaf_node_files / root_folder.total_files * 100, ndigits=2)
    except ZeroDivisionError:
        percent_sorted = 0

    print(f"\n\033[1mLibrary stats\033[0m\n")
    print(tabulate(library_stats, headers=["Folder", "Leaf node", "Total files", "Files"]))
    print(f"\nSorted {leaf_node_files} out of {root_folder.total_files} files ({percent_sorted}%) into leaf nodes")