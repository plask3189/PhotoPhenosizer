from configparser import ConfigParser
import os


class PPConfig:
    def __init__(self, project_directory):
        self.filename = os.path.join(project_directory, 'config.ini')
        self.config_parser = ConfigParser()

        self.threshold = 200
        self.kernel_size = 3
        self.min_size = 700
        self.weights_file = os.path.join(project_directory, 'weights.pt')

        if os.path.isfile(self.filename):
            self.config_parser.read(self.filename)

            sections = self.config_parser.sections()

            if 'IMAGEPROCESSING' in sections:
                if 'threshold' in self.config_parser['IMAGEPROCESSING']:
                    self.threshold = int(self.config_parser['IMAGEPROCESSING']['threshold'])
                if 'kernel_size' in self.config_parser['IMAGEPROCESSING']:
                    self.kernel_size = int(self.config_parser['IMAGEPROCESSING']['kernel_size'])
                if 'min_size' in self.config_parser['IMAGEPROCESSING']:
                    self.min_size = int(self.config_parser['IMAGEPROCESSING']['min_size'])

            if 'NN' in sections:
                if 'weights_file' in self.config_parser['NN']:
                    self.weights_file = self.config_parser['NN']['weights_file']
        else:
            self.write_config()

    def write_config(self):
        self.config_parser['IMAGEPROCESSING'] = {
            'threshold': self.threshold,
            'kernel_size': self.kernel_size,
            'min_size': self.min_size,
        }

        self.config_parser['NN'] = {
            'weights_file': self.weights_file,
        }

        with open(self.filename, 'w') as f:
            self.config_parser.write(f)
