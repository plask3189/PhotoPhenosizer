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

def kickoff_window():
    global final_folder
    global window
    global frame_1
    window = tk.Tk()
    cwd = os.getcwd()
    window.title('Photo Phenosizer')
    window_width = 1000
    window_height = 700
    window.geometry(str(window_width) + 'x' + str(window_height)) # width by height
    color = '#0C064A'
    window.configure(bg = color)
    fontColor = '#FFFFFF'  # font color is white

    frame_1 = tk.Frame(window, bg= color, width=999, height=699)
    frame_1.pack()
    frame_1.pack_propagate(0)


    introTextLine1 = Label(window, text = 'Welcome to Photo Phenosizer', font = ('Arial', 50), bg = color, fg = fontColor)
    introTextLine1.place(relx=0.5, rely=0.1, anchor=CENTER)
    ask_to_select_main_directory_label = Label(frame_1, text = 'Select your project directory:', font = ('Arial', 15), bg = color, fg = fontColor)
    ask_to_select_main_directory_label.place(relx=0.32, rely=0.25, anchor=CENTER)
    #choose_the_project_directory_formatting()
    ''' Just the graphical part of choosing a proj directory. '''

    entry_box_for_file_path= ttk.Entry(frame_1, width = 60, font=40)
    entry_box_for_file_path.place(relx=0.5, rely=0.3, anchor=CENTER)
    folder_image_to_click = PhotoImage(file='file_upload_image4.png')
    folder_image_label = Label(image = folder_image_to_click)
    folder_image_label.image = folder_image_to_click
    global folder_image_button
    folder_image_button= tk.Button(frame_1, image = folder_image_to_click,command= open_file, borderwidth=0, height= 20, width= 20)
    folder_image_button.place(relx=0.76, rely=0.3, anchor=CENTER)
    cwd = os.getcwd()
    config_for_proj_dir = ProjectDirectoryConfig(cwd)
    entry_box_for_file_path.insert(END, str(config_for_proj_dir.project_dir))
    folder_selected_as_project_directory = entry_box_for_file_path.get()
    print('folder1 ' + str(folder_selected_as_project_directory))
    final_folder = folder_selected_as_project_directory
    return_final_folder(final_folder)
    #next_button(final_folder)
    return window

def get_window():
    return window

def open_file():

    entry_box_for_file_path.delete(0, END)
    folder_selected_as_project_directory = filedialog.askdirectory() # folder selected should be the folder with the tif files
    entry_box_for_file_path.insert(tk.END, folder_selected_as_project_directory) # populate the entry box with the file path.
    cwd = os.getcwd()
    configuration = ProjectDirectoryConfig(cwd)
    configuration.project_dir = str(entry_box_for_file_path.get())
    configuration.write_config()
    #set_proj_dir(folder_selected_as_project_directory_1) # if open_file is called, the new dir is loaded into final_folder
    print('folder from opening new file:  ' + str(folder_selected_as_project_directory))
    final_folder = folder_selected_as_project_directory
    return_final_folder(final_folder)
    return final_folder

def return_final_folder(final_folder):
    print('heeerrrre' + str(final_folder))
    next_button(final_folder)
    return final_folder

def uggg_return():
    #final_folder = return_final_folder(final_folder)
    print('ugggg return:'+ final_folder)
    return final_folder

def next_button(final_folder):
    #get_tif_files(folder_selected_as_project_directory)
    print('final folder at next' + str(final_folder))
    next_button = Button(frame_1, text ='  Next  ', command = lambda: should_get_tif_files(final_folder), borderwidth=0)
    next_button.place(relx=0.5, rely=0.5, anchor=CENTER)

def should_get_tif_files(final_folder):
    if (os.path.isdir(final_folder)):
        get_tif_files(final_folder)
    else:
        print('ahhhh')

def get_tif_files(final_folder): # parameter: folder_selected_as_project_directory. return list_of_tif_files_in_directory.
    folder_selected_as_project_directory = final_folder
    images_dir_name = os.path.join(folder_selected_as_project_directory, 'Images') # Navigate to the images directory
    if(os.path.isdir(images_dir_name)):
        list_of_all_files_in_directory = os.listdir(images_dir_name) # get a list of all names in the Images directory.
        tif_file_names_in_images_directory = [] # the list where tif files will be added

        for filename_to_examine_for_tif_suffix in list_of_all_files_in_directory: # traverse whole directory
            if filename_to_examine_for_tif_suffix.endswith('.tif'): # check the extension of files. There is usually a sneaky .DS-Store file that requires us to weed it out.
                tif_file_names_in_images_directory.append(filename_to_examine_for_tif_suffix) # add the tif files to the list_of_files_in_project_directory
        print(tif_file_names_in_images_directory)
        #return_final_folder()
        clear_kickoff_window()
        run_second_window()
        return tif_file_names_in_images_directory
    else:
        choose_valid_folder_popup()

def run_second_window():
    second_win = second_window.create_second_window(final_folder)

def choose_valid_folder_popup():
    popup_title = "Error"
    tkinter.messagebox.showinfo(popup_title,  "Please select a project directory contianing an 'Images' folder")

def clear_kickoff_window(): # destroy the kickoff window
    #entry_box_for_file_path.destroy()
    #folder_image_button.destroy()
    for widget in frame_1.winfo_children():
        widget.destroy()
        print('widget list' + str(widget))
    cleared = 1
    get_cleared_value(1)


def get_cleared_value(cleared_val):
    return cleared_val

def main(): # main listens for events to happen
    window = kickoff_window()
    uggg_return()
    window.mainloop()




if __name__ == "__main__":
    main()
