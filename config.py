# config.py creates a config.ini file
# https://tutswiki.com/read-write-config-files-in-python/

from configparser import ConfigParser
import ppGUI

#Get the configparser object
config_object = ConfigParser()

# if entry in ppGUI is NULL then use default

config_object["IMAGEPROCESSING"] = {
    "threshold" : '200', # threshold is the value of the pixel RGB color that will be turned to white during thresholding. The default is 200 which is light grey
    "kernel_size" : '3',
    "min_size" : '700'
}

image_processing_section = config_object["IMAGEPROCESSING"] # Get the IMAGEPROCESSING section
if len(ppGUI.threshold_input_value) != 0 : # We check to see if the entry box is emptry by seeing if the entry's length is zero. So if not then overwrite the default value.

    image_processing_section["threshold"] = ppGUI.threshold_input_value #Update the threshold

if len(ppGUI.kernel_size_input_value) != 0 : # We check to see if the entry box is emptry by seeing if the entry's length is zero. So if not then overwrite the default value.
    image_processing_section["kernel_size"] = ppGUI.kernel_size_input_value #Update the kernel_size

if len(ppGUI.min_size_input_value) != 0 : # We check to see if the entry box is emptry by seeing if the entry's length is zero. So if not then overwrite the default value.
    image_processing_section["min_size"] = ppGUI.min_size_input_value #Update the min_size

config_object["IMAGEPROCESSING"] = {
    "threshold" : str(), # threshold is the value of the pixel RGB color that will be turned to white during thresholding. The default is 200 which is light grey
    "kernel_size" : '3',
    "min_size" : '700'
}

#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)
