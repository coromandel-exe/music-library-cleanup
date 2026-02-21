~ a music library sorting programme for quickly organising mp3 files into hierarchical folder structures based on descriptive metadata

~ metadata can be edited easily using the free, insanely generous [OneTagger software](https://onetagger.github.io/)

~ made with creative djing and quick set prepartion in mind

~ currently in proof of concept phase

~ let me know if you find this useful and what you'd like to see next!

# current functionality

* copy files from current library into sandbox for experimenting with folder structure
* filter music automatically based on genre, bpm and descriptive tags
* restructure your tagged library from the ground up in seconds!

# get started quickly (see how it works)

1. clone the repo
2. install the dependencies: `pip install -r requirements.txt`
3. copy a few mp3 files of your own to the `source_dir` folder in the repo
4. use the OneTagger software to mark all the tracks with a 'Happy' mood marker
5. use the OneTagger software to give some tracks the 'Start' quick tag
6. execute `python program.py`. you should see a new `target_dir` folder with your tagged music sorted into two folders
