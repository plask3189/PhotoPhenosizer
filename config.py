# config.py creates a config.ini file
# https://tutswiki.com/read-write-config-files-in-python/

from configparser import ConfigParser

#Get the configparser object
config_object = ConfigParser()

config_object["THRESHOLD"] = {
    # threshold is the value of the pixel RGB color that will be turned to white during thresholding. The default is 200 which is light grey
    "threshold" : '200'
}
# check if config.ini exists. if not, use defaults.


#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)
