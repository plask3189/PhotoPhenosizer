import os
import sys
sys.path.append('project')
# print("from sys: " + str(syst))
# cwd = os.getcwd()
# print("cwd: " + cwd)
# path1 = (os.path.dirname(__file__))
# print("path1 " + path1)

# Within __init__.py, we import all the modules that we think are necessary for our project.

import selecting_project_directory_window
import second_window
import make_directories
import process_images

def startup():
    print("Running __init__.py")
    selecting_project_directory_window.main()
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'data1.txt')
    with open(data_path, 'r') as data_file:
        file = data_file.read()
    print(str(file))
