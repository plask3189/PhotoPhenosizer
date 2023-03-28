#Now, suppose that we would like to provide some way of executing the function hello_world() from the command-line. One way to do this is to create a file src/timmins/__main__.py providing a hook as follows:

import selecting_project_directory_window
import second_window
import make_directories
import process_images

# THIS FILE JUST RUNS startup() in init.py (which used to be kickoffwindow.py)
from . import startup # import the init.py

if __name__ == '__main__':
    startup()
