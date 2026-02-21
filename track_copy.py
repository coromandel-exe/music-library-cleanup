import os
import shutil
import pathlib
from tinytag import TinyTag
from tqdm import tqdm

def copy_files_to_root(source_path, target_path, markers):

    # Create counters and blank list for files needing attention
    copy_counter = 0
    pass_counter = 0
    total_files = 0
    attention_files = []

    # Create list of all subdirectory paths in the source directory using rglob()
    source = pathlib.Path(source_path)
    source.rglob('*')
    source_dir_list = [item for item in source.rglob('*') if item.is_dir()]
    source_dir_list.append(source_path)
    folder_counter = len(source_dir_list)

    # Create list of all file titles and artists in the target directory using rglob()
    target = pathlib.Path(target_path)
    target.rglob('*')
    target_file_list = [{'artist': TinyTag.get(item).artist, 'title': TinyTag.get(item).title} for item in target.rglob('*') if item.is_file()]

    # Scan over source directory list
    for i in tqdm(range(len(source_dir_list)), bar_format='{l_bar}{bar:50}{r_bar}{bar:-50b}'):
        dir = source_dir_list[i]

        for entry in os.scandir(dir):

            # Process only mp3 files
            if entry.is_file() and entry.name.endswith('.mp3'):
                file_path = entry.path
                try:
                    track = TinyTag.get(file_path)
                    marker = track.composer if track.composer else '' # get marker

                    # Check if file is the marked for copying
                    if marker in markers:
                        artist = track.artist if track.artist else ''
                        title = track.title if track.title else ''

                        # Check if track matches any in the target directory
                        if any(d['artist'] == artist and d['title'] == title for d in target_file_list):
                            pass_counter += 1
                            pass
                        
                        else:
                            destination_path = os.path.join(target_path, entry.name)
                            shutil.copy2(file_path, destination_path) # Overwrites duplicates
                            copy_counter += 1

                except Exception as e:
                    attention_files.append(file_path)
                    print(f"Error processing {entry.name}: {e}")

            # Flag non-mp3 files for attention
            elif entry.is_file() and (entry.name.endswith('.wav') or entry.name.endswith('.aiff') or entry.name.endswith('.flac') or entry.name.endswith('.m4a') or entry.name.endswith('.mp4') or entry.name.endswith('.wma') or entry.name.endswith('.aac') or entry.name.endswith('.ogg') or entry.name.endswith('.alac')):
                file_path = entry.path
                attention_files.append(file_path)
            total_files += 1
        
    print(f"\n{copy_counter} files copied from {total_files} total files in {folder_counter} folders.")
    print(f"\n{pass_counter} files matched existing files in the target directory and were not copied.")
    print(f"\n\033[1mYou have completed {round((pass_counter + copy_counter) / total_files * 100, ndigits=2)}% of the transfer from this root folder.\033[0m")
    print(f"\n{len(attention_files)} files need attention (non-mp3 files or errors).")
    # print(f"\n Files needing attention:")
    # pprint.pprint(attention_files)