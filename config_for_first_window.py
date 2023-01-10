from configparser import ConfigParser
import os


class PPConfigForDir:
    def __init__(self, project_directory): # parameter is project_directory to be able to get process_images.py and load configs
        # ------------------ instance variables -----------------
        self.filename = os.path.join(project_directory, 'config_for_directory.ini') # create a config.ini
        self.config_parser = ConfigParser()
        cwd = os.getcwd()
        self.project_directory_path = str(cwd)

        if os.path.isfile(self.filename): # if there is already a 'config.ini' file, we read the values from the parser and overwrite the defaults
            
            self.config_parser.read(self.filename) # read config.ini
            sections = self.config_parser.sections() # get the sections of config.ini

            if 'DIRECTORY' in sections:
                if 'project_directory_path' in self.config_parser['DIRECTORY']:
                    self.project_directory_path = self.config_parser['DIRECTORY']['project_directory_path']

        else: # if there is not already a config.ini file, make one.
            self.write_config()

    def write_config(self):

        self.config_parser['DIRECTORY'] = {
            'project_directory_path': self.project_directory_path,
        }

        with open(self.filename, 'w') as f:
            self.config_parser.write(f)
