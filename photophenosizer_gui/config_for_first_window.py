
from configparser import ConfigParser
import os
from pathlib import Path

class ProjectDirectoryConfig:
    def __init__(self, project_directory): # parameter is project_directory to be able to get process_images.py and load config
        # ------------------ instance variables -----------------
        self.filename = os.path.join(project_directory, 'project_directory_config.ini') # create a project_directory_config.ini
        self.config_parser = ConfigParser()
        self.project_dir = ''

        if os.path.isfile(self.filename): # if there is already a 'project_directory_config.ini' file, we read the values from the parser and overwrite the defaults

            self.config_parser.read(self.filename) # read config.ini
            sections = self.config_parser.sections() # get the sections of config.ini

            if 'PROJECTDIR' in sections:
                if 'project_dir' in self.config_parser['PROJECTDIR']:
                    self.project_dir = str(self.config_parser['PROJECTDIR']['project_dir'])

        else: # if there is not already a config.ini file, make one.
            self.write_config()

    def write_config(self):
        self.config_parser['PROJECTDIR'] = {
            'project_dir': self.project_dir,

        }

        with open(self.filename, 'w') as f:
            self.config_parser.write(f)
