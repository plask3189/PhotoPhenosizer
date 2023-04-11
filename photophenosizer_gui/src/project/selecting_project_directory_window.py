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
import second_window


def kickoff_window():
    global window
    window = tk.Tk()
    window.title('Photo Phenosizer')
    window_width = 1000
    window_height = 700
    window.resizable(False, False)
    window.geometry(str(window_width) + 'x' + str(window_height)) # width by height
    color = '#0C064A'
    window.configure(bg = color)
    fontColor = '#FFFFFF'  # font color is white

    frame_1 = Frame(window, bg= color, width=999, height=699)
    frame_1.pack()
    frame_1.pack_propagate(0)
    #frame_1.place(x = window_width, y = window_height)

    introTextLine1 = Label(window, text = 'Welcome to Photo Phenosizer', font = ('Arial', 50), bg = color, fg = fontColor)
    introTextLine1.place(relx=0.5, rely=0.1, anchor=CENTER)

    introTextLine1 = Label(window, text = "A rapid machine learning-based method to measure cell dimensions", font = ('Arial', 15), bg = color, fg = fontColor)
    introTextLine1.place(relx=0.5, rely=0.17, anchor=CENTER)

    verticle_axis_for_selection_label = 0.25
    horizontal_axis_for_selection_label = 0.32
    ask_to_select_main_directory_label = Label(frame_1, text = 'Select your project folder:', font = ('Arial', 15), bg = color, fg = fontColor)
    ask_to_select_main_directory_label.place(relx=horizontal_axis_for_selection_label, rely=verticle_axis_for_selection_label, anchor=CENTER)

    more_info_image = os.path.join(os.path.dirname(__file__), 'data', 'more_info_icon.png')
    more_info_image = Image.open(more_info_image)
    more_info_image = ImageTk.PhotoImage(more_info_image)
    img = Label(frame_1, image=more_info_image)
    more_info_image.image = more_info_image
    more_info_button = Button(frame_1, image = more_info_image, command=lambda: info_popup(), borderwidth=0, height= 18, width= 22)
    more_info_button.place(relx=(horizontal_axis_for_selection_label-0.1), rely=verticle_axis_for_selection_label, anchor=CENTER)

    entry_box_for_file_path= ttk.Entry(frame_1, width = 60, font=40)
    entry_box_for_file_path.place(relx=0.5, rely=0.3, anchor=CENTER)

    #folder_selected_as_project_directory = entry_box_for_file_path.get()
    home_directory = os.path.expanduser( '~' )
    projdir_path = os.path.join(home_directory, "pp", "user_project_directory.txt") # this is the hidden file. Maybe put it in the data dir? If not look into how to include this file when the user downloads.

    with open(projdir_path) as f:
        folder_selected_as_project_directory = f.readlines() # get whatever is in the text file.
    folder_selected_as_project_directory = ''.join(map(str,folder_selected_as_project_directory)) # The folder_selected_as_project_directory was a list, so converting it into a string.
    entry_box_for_file_path.insert(END, folder_selected_as_project_directory) # insert whatever what was in the text file into the entry box. When the user first executes this program, the file will be blank, so nothing will be inserted into the entry box.

    # this is a test to see if we can access the data folder.
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'data1.txt')
    with open(data_path, 'r') as data_file:
        file = data_file.read()
    print(str(file))

    filepath_for_image = os.path.join(os.path.dirname(__file__), 'data', 'getFolder.png')
    folder_image_to_click = Image.open(filepath_for_image)
    folder_image_to_click = ImageTk.PhotoImage(folder_image_to_click)
    #folder_image_to_click = PhotoImage(file='folder_download_image.png')

    folder_image_label = Label(image = folder_image_to_click)
    folder_image_label.image = folder_image_to_click
    folder_image_button= tk.Button(frame_1, image = folder_image_to_click,command= lambda: open_file(entry_box_for_file_path), borderwidth=0, height= 20, width= 24.2)
    folder_image_button.place(relx=0.80, rely=0.3, anchor=CENTER)

    #---------------------- next button ------------------------
    # next_button = Button(frame_1, text ='  Next  ', command = lambda: get_tif_files(folder_selected_as_project_directory, frame_1, entry_box_for_file_path), borderwidth=0) # need lambda bc otherwise get_tif_files runs immedietly when we execute this file
    # next_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    next_button_image_filepath = os.path.join(os.path.dirname(__file__), 'data', 'next_button.png')
    next_button_img_to_click = Image.open(next_button_image_filepath)
    next_button_img_to_click = ImageTk.PhotoImage(next_button_img_to_click)


    next_button_label = Label(image = next_button_img_to_click)
    next_button_label.image = next_button_img_to_click
    next_button= tk.Button(frame_1, image = next_button_img_to_click,command= lambda:get_tif_files(folder_selected_as_project_directory, frame_1, entry_box_for_file_path), borderwidth=0, height= 50, width= 123) # need lambda bc otherwise get_tif_files runs immedietly when we execute this file



    next_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    # next_button.bind("<Enter>", on_enter)
    # next_button.bind("<Leave>", on_leave)


    return window


# def on_enter(next_button):
#     print("next button on enter: " + str(next_button))
#     next_button['background'] = 'FFFFFF'
#
# def on_leave(e):
#     next_button['background'] = '000000'


def open_file(entry_box_for_file_path):
    # If the user presses the button to upload a new path for the project directory
    entry_box_for_file_path.delete(0, END) # Delete the text that was in the entry box for project directory submission.
    home_directory = os.path.expanduser( '~' )
    projdir_path = os.path.join(home_directory, "pp", "user_project_directory.txt")
    with open(projdir_path,'w') as file: # Delete the contents of the user_project_directory.txt file
        pass
    folder_selected_as_project_directory = filedialog.askdirectory() # Ask the user to select a project directory. The selected one is assigned to folder_selected_as_project_directory
    folder_selected_as_project_directory = ''.join(map(str,folder_selected_as_project_directory)) # The folder_selected_as_project_directory was a list, so converting it into a string.
    entry_box_for_file_path.insert(tk.END, folder_selected_as_project_directory) # populate the entry box with the file path.
    # ------- Update text file with newly specified user project directory----------
    with open(projdir_path, 'w') as f:
        f.write(folder_selected_as_project_directory) # write the folder selected as project directory to the user project directory text file.

    return folder_selected_as_project_directory


def get_tif_files(folder_selected_as_project_directory, frame_1, entry_box_for_file_path):
    project_dir = entry_box_for_file_path.get() # retrieve the text that is in the entry box
    tif_file_names_in_images_directory = [] # the list where tif files will be added
    list_of_all_files_in_directory = []
    print("proj dir: " + project_dir)

    images_dir_name = os.path.join(project_dir, 'Images') # This would be the path to the images directory (it may or may not be valid)
    print('images dir name: ' + images_dir_name)


    if os.path.exists(images_dir_name):
        res_dir = make_directories.make_results_directory(project_dir) # create the results directory in the specified project directory
        list_of_all_files_in_directory = os.listdir(images_dir_name) # get a list of all names in the Images directory.
        good_image_types = 0 # set as false initially
        for filename_to_examine_for_tif_suffix in list_of_all_files_in_directory: # traverse whole directory
            print("********** filename: " + filename_to_examine_for_tif_suffix)
            if filename_to_examine_for_tif_suffix.endswith((".tif", ".tiff", ".png", ".jpg")) or (filename_to_examine_for_tif_suffix == ".DS_Store"): # check the extension of files. There is usually a sneaky .DS-Store file that requires us to weed it out. If the string ends with any item of the tuple, endswith() returns True
                print("true case where good suffix")
                if filename_to_examine_for_tif_suffix.endswith((".tif", ".tiff", ".png", ".jpg")):
                    tif_file_names_in_images_directory.append(filename_to_examine_for_tif_suffix) # add the tif files to the list_of_files_in_project_directory
                good_image_types = 1

            else:
                tkinter.messagebox.showwarning("Image type error",  "Please use images with extensions '.tif', '.tiff', .png', or '.jpg'")
        if good_image_types == 1: # if the image is a tif or tiff or png or jpg:
                clear_kickoff_window(frame_1)
                second_win = second_window.create_second_window(project_dir, window, tif_file_names_in_images_directory, res_dir)
                return_tif_files(tif_file_names_in_images_directory)
    else:
        choose_valid_folder_popup() # Must choose a project directory that has a subfolder called 'Images'

def info_popup():
    tkinter.messagebox.showinfo("What is the Project Folder?",  "This is where you choose your project folder. You make your own folder that includes an 'Images' folder, and a 'weights.pt' file. \n The 'Images' folder has the images of your cells. \n The 'weights.pt' file is for the neural network to know how to work with your specific cell type. \n \n After running this program, a new folder with your results will appear within this project folder.")

def return_tif_files(tif_file_names_in_images_directory):
     return tif_file_names_in_images_directory

def clear_kickoff_window(frame_1): # destroy the kickoff window
    exists = frame_1.winfo_exists() # check if frame exists.
    if exists == 1: # If the frame exists, destroy the widgets.
        for widget in frame_1.winfo_children():
            widget.destroy()

def choose_valid_folder_popup():
    popup_title = "Error"
    tkinter.messagebox.showwarning(popup_title,  "Please select a project directory contianing an 'Images' folder")

def main(): # main listens for events to happen
    print("✨✨✨✨✨✨✨✨✨✨✨\n✨ PhotoPhenosizer  ✨\n✨✨✨✨✨✨✨✨✨✨✨")
    window = kickoff_window()
    window.mainloop()

if __name__ == "__main__":
    main()
