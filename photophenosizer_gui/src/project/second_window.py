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
import selecting_project_directory_window
from run_process_images import run_process_images


def create_second_window(folder_selected_as_project_directory, window, tif_file_names_in_images_directory, res_dir):
    config = PPConfig(folder_selected_as_project_directory)
    color = '#0C064A'
    fontColor = '#FFFFFF'
    global list_of_configuration_entry_boxes
    list_of_configuration_entry_boxes = []
    frame_2 = Frame(window, bg = color, width=999, height=699)
    frame_2.place(relx=0.5, rely=0.5, anchor=CENTER)
    introTextLine1 = Label(frame_2, text = 'Welcome to Photo Phenosizer', font = ('Arial', 50), bg = color, fg = fontColor)
    introTextLine1.place(relx=0.5, rely=0.1, anchor=CENTER)

    #----------------------- Threshold ---------------------------
    threshold_label = Label(frame_2, text = 'Threshold value: ', font = ('Arial', 15), bg = color, fg = fontColor)
    threshold_label.place(relx=0.43, rely=0.2, anchor=CENTER)
    threshold_entry_box = ttk.Entry(frame_2, width = 7, font=40)
    threshold_entry_box.insert(END, str(config.threshold)) # automatically insert the last-used threshold value into the entry box.
    threshold_entry_box.place(relx=0.55, rely=0.2, anchor=CENTER)
    # Threshold Domain Checking:
    reg = frame_2.register(thresh_callback) # the registered callback
    threshold_entry_box.config(validate="focusout", validatecommand=(reg, '%P'))
    # "validate" is used to specify when the callback function will be called. So when "focusout" of entry box, do the validate command. validatecommand is used to specify the callback function. ‘%P’ is the value that the text will have if the change is allowed.

    list_of_configuration_entry_boxes.append(threshold_entry_box) # if valid, append to list.

    #----- More info button for threshold: -----
    more_info_image = os.path.join(os.path.dirname(__file__), 'data', 'more_info_icon.png')
    more_info_image = Image.open(more_info_image)

    more_info_image = ImageTk.PhotoImage(more_info_image)
    img = Label(frame_2, image=more_info_image)
    more_info_image.image = more_info_image

    more_info_button = Button(frame_2, image = more_info_image, command=lambda: info_popup('threshold'), borderwidth=0, height= 18, width= 22)
    more_info_button.place(relx=0.32, rely=0.2, anchor=CENTER)

    #----------------------- Kernel Size ---------------------------
    kernel_size_label = Label(frame_2, text = 'Kernel size: ', font = ('Arial', 15), bg = color, fg = fontColor)
    kernel_size_label.place(relx=0.43, rely=0.3, anchor=CENTER)
    #kernel_size_entry_box = tk.Entry(frame_2, bd =5)
    kernel_size_entry_box= ttk.Entry(frame_2, width = 7, font=40)
    kernel_size_entry_box.insert(END, str(config.kernel_size))
    kernel_size_entry_box.place(relx=0.55, rely=0.3, anchor=CENTER)
    # Kernel Size Domain Checking:
    kern_reg = frame_2.register(kern_callback)
    kernel_size_entry_box.config(validate="focusout", validatecommand=(kern_reg, '%P'))
    list_of_configuration_entry_boxes.append(kernel_size_entry_box)

    #----------------------- Min Size ---------------------------
    more_info_button_for_kernel_size= Button(frame_2, image = more_info_image,command= lambda: info_popup('kernel_size'), borderwidth=0, height= 18, width= 22)
    more_info_button_for_kernel_size.place(relx=0.32, rely=0.3, anchor=CENTER)

    # Label and text entry box for min size:
    min_size_label = Label(frame_2, text = 'Min size: ', font = ('Arial', 15), bg = color, fg = fontColor)
    min_size_label.place(relx=0.43, rely=0.4, anchor=CENTER)
    min_size_entry_box= ttk.Entry(frame_2, width = 7, font=40)
    min_size_entry_box.insert(END, str(config.min_size))
    min_size_entry_box.place(relx=0.55, rely=0.4, anchor=CENTER)
    # Kernel Size Domain Checking:
    min_reg = frame_2.register(min_callback)
    min_size_entry_box.config(validate="focusout", validatecommand=(min_reg, '%P'))
    list_of_configuration_entry_boxes.append(min_size_entry_box)

    # More info button for min size:
    more_info_button_for_min_size= Button(frame_2, image = more_info_image,command = lambda: info_popup('min_size'), borderwidth=0, height= 18, width= 22)
    more_info_button_for_min_size.place(relx=0.32, rely=0.4, anchor=CENTER)


    #-------------------------- Upload Weights File------------------
    ask_to_select_weights_file_label = Label(frame_2, text = 'Select the weights file:', font = ('Arial', 15), bg = color, fg = fontColor)
    ask_to_select_weights_file_label.place(relx=0.12, rely=0.5, anchor=CENTER)

    entry_box_for_weights_path=ttk.Entry(frame_2, width = 60, font=40)
    path_of_weights_file = str(config.weights_file)
    entry_box_for_weights_path.insert(END, config.weights_file) # automatically chose the last used weights.pt file.
    entry_box_for_weights_path.place(relx=0.5, rely=0.5, anchor=CENTER)
    list_of_configuration_entry_boxes.append(path_of_weights_file)

    file_image_to_click = os.path.join(os.path.dirname(__file__), 'data', 'weights_file_upload_image.png')
    file_image_to_click = Image.open(file_image_to_click)
    file_image_to_click = ImageTk.PhotoImage(file_image_to_click)
    #file_image_to_click = PhotoImage(file='weights_file_upload_image.png')
    file_image_label = Label(image = file_image_to_click)
    file_image_label.image = file_image_to_click
    file_image_button= Button(frame_2, image = file_image_to_click,command= lambda:  open_weights_file(entry_box_for_weights_path), borderwidth=0, height= 23, width= 25)
    file_image_button.place(relx=0.758, rely=0.5, anchor=CENTER)

    weights_reg = frame_2.register(weights_callback)
    entry_box_for_weights_path.config(validate="focusout", validatecommand=(weights_reg, '%P'))

    #------------------------------ Checkbox ----------------------------------
    checked_or_unchecked = tk.IntVar()
    checkbox = tk.Checkbutton(frame_2, text='Check here if you would like to save area filtered, NN, and threshold mask images',variable=checked_or_unchecked, onvalue=1, offvalue=0, command= lambda: make_mask_directories_here(res_dir, checked_or_unchecked))
    checkbox.place(relx=0.5, rely=0.6, anchor=CENTER)

    #----------------------------- Button Frame---------------------
    white_color = '#FFFFFF'
    button_frame = Frame(frame_2, bg = white_color, width = 205, height = 51.25)
    button_frame.place(relx=0.5, rely=0.7, anchor=CENTER)

    # ------------------------------- Run Button---------------------
    length = len(list_of_configuration_entry_boxes)
    run_button = Button(button_frame, text ='Run', command = lambda: run_process_images(folder_selected_as_project_directory, tif_file_names_in_images_directory, window, res_dir, list_of_configuration_entry_boxes))
    run_button.place(relx=0.8, rely=0.5, anchor=CENTER)

    # --------------------- Back Button ---------------------
    back_button = Button(button_frame, text ='Back', command = lambda: back( window))
    back_button.place(relx=0.2, rely=0.5, anchor=CENTER)
    return window


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

def back(window):
    window.destroy()
    selecting_project_directory_window.main()

def open_weights_file(entry_box_for_weights_path):
     weights_filepath_selected = filedialog.askopenfilename() # ask for the weights file
     if not (weights_filepath_selected.endswith('.pt')): # to see if the weights file is acceptable, check if the extension is '.pt'
         tkinter.messagebox.showwarning('Weights File Error',  "Please select a weights file. The file must have extension '.pt'")
     if not os.path.exists(weights_filepath_selected):
         tkinter.messagebox.showwarning('File Path Error',  "Please use a filepath for weights.pt that exists.")
     else: # if the new weights file selected is acceptable, replace the entry box text with the path.
         entry_box_for_weights_path.delete(0, END) # clear the entry box because it had the configured path
         entry_box_for_weights_path.insert(END, str(weights_filepath_selected)) # insert this new path into the entry box.
         del list_of_configuration_entry_boxes[3] # delete the old weights file element in this list. It is at index 3
         list_of_configuration_entry_boxes.insert(3, str(weights_filepath_selected))# write the weights path (at index 3) in the list_of_configuration_entry_boxes

def make_mask_directories_here(res_dir, checked_or_unchecked):
    if(checked_or_unchecked.get() == 1): # if the user checks the box saying that they want to save the configuration images, make the directories to save those images
        make_directories.make_mask_directories(res_dir)

def thresh_callback(input):
    if input.isdigit() == False: # Check if the entry box value is a digit
        tkinter.messagebox.showwarning('Domain Error',  "Please use a threshold value 0-255")
        return False
    input = int(input)
    if input > 255 or input < 0:
        tkinter.messagebox.showwarning('Domain Error',  "Please use a threshold value 0-255")
        return False # callback function returns false if input is invalid. When return false, the user's attempt to edit the entry box's text is refused so the text is unchanged.

def kern_callback(input):
    if input.isdigit() == False: # Check if the entry box value is a digit
        tkinter.messagebox.showwarning('Domain Error',  "Please use a kernel size 2-500")
        return False
    kern = int(input) # convert the input to an integer in order to perform comparison operations.
    if kern > 500 or kern < 2:
        tkinter.messagebox.showwarning('Domain Error',  "Please use a kernel size 2-500")
        return False

def min_callback(input):
    if input.isdigit() == False: # Check if the entry box value is a digit
        tkinter.messagebox.showwarning('Domain Error',  "Please use a min size 1-1000")
        return False
    min = int(input)
    if min < 1 or min > 1000:
        tkinter.messagebox.showwarning('Domain Error',  "Please use a min size 1-1000")
        return False

def weights_callback(input):

    if not (input.endswith('.pt')): # to see if the weights file is acceptable, check if the extension is '.pt'
        tkinter.messagebox.showwarning('Weights File Error',  "Please select a weights file. The file must have extension '.pt'")
        return False
    if not os.path.exists(input):
        tkinter.messagebox.showwarning('File Path Error',  "Please use a filepath for weights.pt that exists.")
        return False
    else:
        return True

def main(): # main listens for events to happen
    window = create_second_window()
    window.mainloop()

if __name__ == "__main__":
    main()
