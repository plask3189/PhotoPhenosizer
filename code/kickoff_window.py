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
import config_for_first_window
from config_for_first_window import ProjectDirectoryConfig
import second_window
import variable_support



def kickoff_window(): # The parameter is for the back button to not create a window, just create the frame_1 on the existing window.
    global window
    window = tk.Tk()
    window.title('Photo Phenosizer')
    window_width = 1000
    window_height = 700
    window.geometry(str(window_width) + 'x' + str(window_height)) # width by height
    color = '#0C064A'
    window.configure(bg = color)

    # else do not create the window, just make the frame_1.
    color = '#0C064A'
    fontColor = '#FFFFFF'  # font color is white

    frame_1 = tk.Frame(window, bg= color, width=999, height=699)
    frame_1.pack()
    frame_1.pack_propagate(0)

    introTextLine1 = Label(window, text = 'Welcome to Photo Phenosizer', font = ('Arial', 50), bg = color, fg = fontColor)
    introTextLine1.place(relx=0.5, rely=0.1, anchor=CENTER)
    ask_to_select_main_directory_label = Label(frame_1, text = 'Select your project directory:', font = ('Arial', 15), bg = color, fg = fontColor)
    ask_to_select_main_directory_label.place(relx=0.32, rely=0.25, anchor=CENTER)

    entry_box_for_file_path= ttk.Entry(frame_1, width = 60, font=40)
    entry_box_for_file_path.place(relx=0.5, rely=0.3, anchor=CENTER)
    folder_image_to_click = PhotoImage(file='file_upload_image4.png')
    folder_image_label = Label(image = folder_image_to_click)
    folder_image_label.image = folder_image_to_click
    folder_image_button= tk.Button(frame_1, image = folder_image_to_click,command= lambda: open_file(entry_box_for_file_path), borderwidth=0, height= 20, width= 20)
    folder_image_button.place(relx=0.76, rely=0.3, anchor=CENTER)

    the_code_directory = os.path.dirname(os.path.abspath('kickoff_window.py')) # get the code directory, which is the same directory where this file is located! That way, we do not need to use 'getcwd(),' which we are trying to avoid.

    # maybe instead of a config file, get the "last used project dir" frpm a text file.
    config_for_proj_dir = ProjectDirectoryConfig(the_code_directory)
    entry_box_for_file_path.insert(END, str(config_for_proj_dir.project_dir))
    folder_selected_as_project_directory = entry_box_for_file_path.get()

    #---------------------- next button ------------------------
    next_button = Button(frame_1, text ='  Next  ', command = lambda: get_tif_files(folder_selected_as_project_directory, frame_1), borderwidth=0) # need lambda bc otherwise get_tif_files runs immedietly when we execute this file
    next_button.place(relx=0.5, rely=0.5, anchor=CENTER)
    return window

def open_file(entry_box_for_file_path):
    # If the user presses the button to upload a new path for the project directory
    entry_box_for_file_path.delete(0, END) # Delete the text that was in the entry box for project directory submission.
    folder_selected_as_project_directory = filedialog.askdirectory() # Ask the user to select a project directory. The selected one is assigned to folder_selected_as_project_directory
    entry_box_for_file_path.insert(tk.END, folder_selected_as_project_directory) # populate the entry box with the file path.
    the_code_directory = os.path.dirname(os.path.abspath('kickoff_window.py')) # get the code directory, which is the same directory where this file is located! That way, we do not need to use 'getcwd(),' which we are trying to avoid.
    # project directory will be in homedirectory/.config/codedir
    configuration = ProjectDirectoryConfig(the_code_directory) # change weights file to be in project dir
    configuration.project_dir = str(entry_box_for_file_path.get())

    configuration.write_config()
    return folder_selected_as_project_directory


def get_tif_files(folder_selected_as_project_directory, frame_1):
    res_dir = make_directories.make_results_directory(folder_selected_as_project_directory) # we create the results directory
    images_dir_name = os.path.join(folder_selected_as_project_directory, 'Images') # Navigate to the images directory
    if(os.path.isdir(images_dir_name)):
        list_of_all_files_in_directory = os.listdir(images_dir_name) # get a list of all names in the Images directory.
        tif_file_names_in_images_directory = [] # the list where tif files will be added
        for filename_to_examine_for_tif_suffix in list_of_all_files_in_directory: # traverse whole directory
            if filename_to_examine_for_tif_suffix.endswith('.tif'): # check the extension of files. There is usually a sneaky .DS-Store file that requires us to weed it out.
                tif_file_names_in_images_directory.append(filename_to_examine_for_tif_suffix) # add the tif files to the list_of_files_in_project_directory
        clear_kickoff_window(frame_1)
        second_win = second_window.create_second_window(folder_selected_as_project_directory, window, tif_file_names_in_images_directory, res_dir)
        var_support_object = variable_support.Variable_Support("tif_file_names_in_images_directory") # create a class object
        return tif_file_names_in_images_directory
    else:
        choose_valid_folder_popup() # Must choose a project directory that has a subfolder called 'Images'

def return_tif_files(tif_file_names_in_images_directory):
     return tif_file_names_in_images_directory

def clear_kickoff_window(frame_1): # destroy the kickoff window
    exists = frame_1.winfo_exists() # check if frame exists.
    if exists == 1: # If the frame exists, destroy the widgets.
        for widget in frame_1.winfo_children():
            widget.destroy()

def choose_valid_folder_popup():
    popup_title = "Error"
    tkinter.messagebox.showinfo(popup_title,  "Please select a project directory contianing an 'Images' folder")

def main(): # main listens for events to happen
    window = kickoff_window()
    window.mainloop()




if __name__ == "__main__":
    main()
