import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter import Tk
from tkinter.ttk import Label
from tkinter import *
import time
import os

from configparser import ConfigParser

def GUI():
    global window
    window = tk.Tk()
    window.title('Photo Phenosizer')
    window_width = 1000
    window_height = 700
    window.geometry(str(window_width) + 'x' + str(window_height)) # width by height
    color = '#0C064A'
    window.configure(bg = color)
    fontColor = '#FFFFFF'  # font color is white
    canvas = Canvas()
    threshold_label = Label(window, text = 'Threshold value: ', font = ('Courier New', 15), bg = color, fg = fontColor)
    threshold_label.place(relx=0.4, rely=0.2, anchor=CENTER)
    threshold_entry_box = Entry(window, bd =5)
    threshold_entry_box.place(relx=0.6, rely=0.2, anchor=CENTER)


#Get the configparser object
config_object = ConfigParser()

# if entry in ppGUI is NULL then use default

config_object["IMAGEPROCESSING"] = {
    "threshold" : '200', # threshold is the value of the pixel RGB color that will be turned to white during thresholding. The default is 200 which is light grey
    "kernel_size" : '3',
    "min_size" : '700'
}


def submit_button():
    sub_btn=tk.Button(window, text = 'Submit', command = configure)
    sub_btn.place(relx=0.5, rely=0.5, anchor=CENTER)

def configure():
    image_processing_section = config_object["IMAGEPROCESSING"] # Get the IMAGEPROCESSING section
    threshold_input_value = threshold_entry_box.get()
    if len(threshold_input_value) != 0 : # We check to see if the entry box is emptry by seeing if the entry's length is zero. So if not then overwrite the default value.
        image_processing_section["threshold"] = ppGUI.threshold_input_value #Update the threshold


#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)


def main():
    GUI()
    submit_button()
    configure()


if __name__ == "__main__":
    main()

window.mainloop()
