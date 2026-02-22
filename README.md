~ a music library sorting programme for quickly organising mp3 files into hierarchical folder structures based on descriptive metadata

~ metadata can be edited easily using the free, insanely generous [OneTagger software](https://onetagger.github.io/)

~ made with creative djing and quick set prepartion in mind

~ currently in proof of concept phase

~ let me know if you find this code useful ! (coromandel.music@gmail.com)

# current functionality

* copy marked files into a tagged library without affecting your current library structure
* filter music automatically into folders based on genre, mood, energy, bpm and descriptive tags
* restructure your tagged library from the ground up in seconds!

# get started quickly (see how it works)

1. clone the repo
2. install the dependencies: `pip install -r requirements.txt`
3. copy a few mp3 files of your own to the `source_dir` folder in the repo. add a range of bpms if possible.
4. use the OneTagger software to mark all the tracks with a 'Happy' mood marker
5. use the OneTagger software to give some tracks the 'Start' quick tag
6. execute `python program.py`.

you should see a new `target_dir` folder with your tagged music sorted into a 'starter' folder and further separated into 'slow' and 'fast' folders based on bpm. you can run the programme again to copy more marked files from the source directory or filter newly tagged files in the target directory.

# use with your own library

1. change the source directory filepath to the root of of your music library in `program.py`
2. change the target directory filepath to where you want your new tagged library to appear.
3. customise your tagging settings in OneTagger or otherwise.

> **_note_**: currently supports filtering based on composer, bpm, lyricist and comment metadata attributes.

3. specify your desired new folder structure to the `folder_structure.py` file
4. tag your music
5. run the programme
