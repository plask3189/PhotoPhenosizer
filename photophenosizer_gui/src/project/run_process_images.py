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
import process_images
import pp_config
from pp_config import PPConfig
import configparser
from PIL import ImageTk, Image
from configparser import ConfigParser
import make_directories
import tkinter.messagebox
from pathlib import Path
import selecting_project_directory_window
import second_window

def run_process_images(folder_selected_as_project_directory, tif_file_names_in_images_directory, window, res_dir, list_of_configuration_entry_boxes):

    thresh_box = list_of_configuration_entry_boxes[0]
    kern_box = list_of_configuration_entry_boxes[1]
    min_box = list_of_configuration_entry_boxes[2]
    weights_filepath =list_of_configuration_entry_boxes[3] # this is the actual filepath.

    configuration = PPConfig(folder_selected_as_project_directory) # create an object of PPConfig called configuration.

    # ------ Assign values to 'configuration' object's sections--------
    configuration.threshold = int(thresh_box.get()) # get the value from the entry box
    configuration.kernel_size = int(kern_box.get())
    configuration.min_size = int(min_box.get())
    configuration.weights_file = weights_filepath
    configuration.write_config() # update the configuration file with the possibly new values
    #-----------------------------------------

    global args
    args = {
        "results_directory": res_dir,
        "weights_file": weights_filepath,
        "write_nn_mask": kern_box.get(),
        "write_threshold_mask": thresh_box.get(),
        "write_area_filtered" : min_box.get(),
        "config": configuration
    }

    images_dir_path = os.path.join(folder_selected_as_project_directory, 'Images')

    already_processed = []
    index = 0

    for image in tif_file_names_in_images_directory: #for each image in the Images directory:
        os.chdir(images_dir_path)
        already_processed.append(image) # add the image name to the list of already processed images
        update_scroll(window, already_processed) # update the section with the scrollbar to display the list of images names as they are processed
        process_images.process_image(image, args)
        index = index + 1
        if(index+1 == (len(tif_file_names_in_images_directory)+1)):
            already_processed.append('DONE')
            update_scroll(window, already_processed)
            print("done")

# ********************************************************************************
def update_scroll(window, already_processed):

    color = '#0C064A'
    fontColor = '#FFFFFF'
    label_for_scroll_section = Label(window, text = 'Images processed: ', font = ('Arial', 15), bg = color, fg = fontColor)
    label_for_scroll_section.place(relx=0.5, rely=0.76, anchor=CENTER)

    scroll_frame = Frame(window, bg = '#000000', borderwidth=1, relief="sunken")
    scroll_frame.place(relx=0.5, rely=0.9, anchor=CENTER) # scroll_frame defines the display location of text of the processed images with a scrollbar.
    scrollbar_widget = Scrollbar(scroll_frame, orient='vertical')
    scrollbar_widget.pack(side=RIGHT, fill='y')

    text_widget = Text(scroll_frame, height = 8, width = 30, font=("Arial, 14"), yscrollcommand=scrollbar_widget.set)

    for i in range(1,500):
        position = f'{i}.0'
    for image in already_processed: # add text to the text widget to show the screen
        text_widget.insert(position, image + '\n');

    # Attach the scrollbar with the text widget
    scrollbar_widget.config(command=text_widget.yview)
    text_widget.pack()

    Tk.update(window)
