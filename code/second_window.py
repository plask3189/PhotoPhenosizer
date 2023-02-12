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
import PIL
from PIL import ImageTk, Image
from configparser import ConfigParser
import make_directories
import tkinter.messagebox
from pathlib import Path
import kickoff_window
global folder_selected_as_project_directory

from run_process_images import run_process_images


def create_second_window(folder_selected_as_project_directory, window, tif_file_names_in_images_directory, res_dir):
    import kickoff_window

    config = PPConfig(folder_selected_as_project_directory)
    color = '#0C064A'
    #window.configure(bg = color)
    fontColor = '#FFFFFF'
    global list_of_configuration_entry_boxes
    list_of_configuration_entry_boxes = []

    frame_2 = Frame(window, bg = color, width=999, height=699)
    #button_frame_frame.pack()
    frame_2.place(relx=0.5, rely=0.5, anchor=CENTER)
    introTextLine1 = Label(frame_2, text = 'Welcome to Photo Phenosizer', font = ('Arial', 50), bg = color, fg = fontColor)
    introTextLine1.place(relx=0.5, rely=0.1, anchor=CENTER)

    #----------------------- Threshold label ---------------------------
    threshold_label = Label(frame_2, text = 'Threshold value: ', font = ('Arial', 15), bg = color, fg = fontColor)
    threshold_label.place(relx=0.4, rely=0.2, anchor=CENTER)

    #----------------------- More info button for threshold -------------------------
    the_code_directory = os.path.dirname(os.path.abspath('second_window.py')) # get the code directory, which is the same directory where this file is located! That way, we do not need to use 'getcwd(),' which we are trying to avoid.
    more_info_image = Image.open(the_code_directory + '/more_info_icon.png')
    more_info_image = ImageTk.PhotoImage(more_info_image)
    img = Label(frame_2, image=more_info_image)
    more_info_image.image = more_info_image

    more_info_button= Button(window, image = more_info_image, command=lambda: info_popup('threshold'), borderwidth=0, height= 18, width= 22)
    more_info_button.place(relx=0.32, rely=0.2, anchor=CENTER)

    #----------------------- Checkbox ---------------------------
    threshold_entry_box = tk.Entry(frame_2, bd =5)
    threshold_entry_box.insert(END, str(config.threshold))
    threshold_entry_box.place(relx=0.6, rely=0.2, anchor=CENTER)
    list_of_configuration_entry_boxes.append(threshold_entry_box)

    #--------------- Label and text entry box for kernel size ------------
    kernel_size_label = Label(window, text = 'Kernel size: ', font = ('Arial', 15), bg = color, fg = fontColor)
    kernel_size_label.place(relx=0.4, rely=0.3, anchor=CENTER)
    kernel_size_entry_box = tk.Entry(frame_2, bd =5)
    kernel_size_entry_box.insert(END, str(config.kernel_size))
    kernel_size_entry_box.place(relx=0.6, rely=0.3, anchor=CENTER)
    list_of_configuration_entry_boxes.append(kernel_size_entry_box)

    #----------------------- More info button for kernel size -----------------------
    more_info_button_for_kernel_size= Button(frame_2, image = more_info_image,command= lambda: info_popup('kernel_size'), borderwidth=0, height= 18, width= 22)
    more_info_button_for_kernel_size.place(relx=0.32, rely=0.3, anchor=CENTER)

    #--------------- Label and text entry box for min size ------------
    min_size_label = Label(frame_2, text = 'Min size: ', font = ('Arial', 15), bg = color, fg = fontColor)
    min_size_label.place(relx=0.4, rely=0.4, anchor=CENTER)
    min_size_entry_box = tk.Entry(frame_2, bd =5)
    min_size_entry_box.insert(END, str(config.min_size))
    min_size_entry_box.place(relx=0.6, rely=0.4, anchor=CENTER)
    list_of_configuration_entry_boxes.append(min_size_entry_box)

    #----------------------- More info button for min size ---------------------------
    more_info_button_for_min_size= Button(frame_2, image = more_info_image,command = lambda: info_popup('min_size'), borderwidth=0, height= 18, width= 22)
    more_info_button_for_min_size.place(relx=0.32, rely=0.4, anchor=CENTER)

    #------------- To upload weights file------------------
    ask_to_select_weights_file_label = Label(frame_2, text = 'Select the weights file:', font = ('Arial', 15), bg = color, fg = fontColor)
    ask_to_select_weights_file_label.place(relx=0.1, rely=0.5, anchor=CENTER)

    entry_box_for_weights_path=tk.Entry(frame_2, width = 60, font=40)
    entry_box_for_weights_path.insert(END, os.path.join(folder_selected_as_project_directory, config.weights_file)) # automatically chose the weights.pt file that is in the main project directory
    entry_box_for_weights_path.place(relx=0.5, rely=0.5, anchor=CENTER)
    list_of_configuration_entry_boxes.append(entry_box_for_weights_path)
    file_image_to_click = PhotoImage(file='weights_file_upload_image.png')
    file_image_label = Label(image = file_image_to_click)
    file_image_label.image = file_image_to_click
    file_image_button= Button(window, image = file_image_to_click,command= open_weights_file, borderwidth=0, height= 23, width= 25)
    file_image_button.place(relx=0.758, rely=0.5, anchor=CENTER)

    #----------------------- Checkbox ----------------------------------
    checked_or_unchecked = tk.IntVar()
    checkbox = tk.Checkbutton(frame_2, text='Check here if you would like to save area filtered, NN, and threshold mask images',variable=checked_or_unchecked, onvalue=1, offvalue=0, command= lambda: make_mask_directories_here(res_dir, checked_or_unchecked))
    checkbox.place(relx=0.5, rely=0.6, anchor=CENTER)

    #------------------------------- Button Frame---------------------
    white_color = '#FFFFFF'
    button_frame_frame = Frame(frame_2, bg = white_color, width = 205, height = 51.25)
    #button_frame_frame.pack()
    button_frame_frame.place(relx=0.5, rely=0.7, anchor=CENTER)
    grey_color = '#000000'
    button_frame = Frame(button_frame_frame, bg = grey_color, width = 200.5, height = 49.5)
    #button_frame.pack()
    button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    # ------------------------------- Run Button---------------------
    #the_code_directory = os.path.dirname(os.path.abspath('second_window.py'))
    run_button = Button(button_frame, text ='Run', command = lambda: run_process_images(folder_selected_as_project_directory, tif_file_names_in_images_directory, window, res_dir)) # look into ways to pass the project dir at binding time. Project dir is param for process, in process, get list of images.
    run_button.place(relx=0.8, rely=0.5, anchor=CENTER)

    # --------------------- Back Button ---------------------
    back_button = Button(button_frame, text ='Back', command = back)
    back_button.place(relx=0.2, rely=0.5, anchor=CENTER)

    # thresh_val = threshold_entry_box.get()
    # kernel_val = kernel_size_entry_box.get()
    # min_val = min_size_entry_box.get()

    # update_configs(thresh_val, kernel_val, min_val, folder_selected_as_project_directory, res_dir)
    return window

def return_list_of_configuration_boxes():
    return list_of_configuration_entry_boxes

# def update_configs(thresh_val, kernel_val, min_val, folder_selected_as_project_directory, res_dir):
#
#     print('threshbox: ' + thresh_val)
#
#
#     configuration = PPConfig(folder_selected_as_project_directory)
#     configuration.threshold = int(thresh_val)
#     configuration.kernel_size = int(kernel_val)
#     configuration.min_size = int(min_val)
#     configuration.write_config()
#
#     #global args
#     args = {
#         "results_directory": res_dir,
#         "weights_file": weights_box,
#         "write_nn_mask": kern_box,
#         "write_threshold_mask": thresh_box,
#         "write_area_filtered" : min_box,
#         "config": configuration
#     }

def info_popup(threshold_or_kernel_size_or_min_size):
    if (threshold_or_kernel_size_or_min_size == 'threshold'):
        popup_title = "More info on threshold"
        tkinter.messagebox.showinfo(popup_title,  "The threshold value can be 0-255. The higher the threshold, the higher the Neural Network's confidence for more pixels.")
    if (threshold_or_kernel_size_or_min_size == 'kernel_size'):
        popup_title = "More info on kernel size"
        tkinter.messagebox.showinfo(popup_title,  "The kernel size value can be 2-500. Kernel size the the number of neighboring pixels around a cell to consider for erotion and dilation. Erosion and dilation processes disconnect adjacent cells, remove small artifacts, and fill in holes.")
    if (threshold_or_kernel_size_or_min_size == 'min_size'):
        popup_title = "More info on min size"
        tkinter.messagebox.showinfo(popup_title,  "The min size can be 1-1000. This is the minimum Feret diameter. ")

def back():
    return 'back'

def open_weights_file():
     weights_file_selected = filedialog.askopenfile() # ask what weights file to use.

def make_mask_directories_here(res_dir, checked_or_unchecked):
    if(checked_or_unchecked.get() == 1): # if the user checks the box saying that they want to save the configuration images, make the directories to save those images
        make_directories.make_mask_directories(res_dir)

def main(): # main listens for events to happen
    window = create_second_window()
    window.mainloop()

if __name__ == "__main__":
    main()
