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

# the kickoff frame is where the project directory is chosen
def kickoff_window():
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
    introTextLine1 = Label(window, text = 'Welcome to Photo Phenosizer', font = ('Arial', 50), bg = color, fg = fontColor)
    introTextLine1.place(relx=0.5, rely=0.1, anchor=CENTER)

    #------------------- Main directory selection-----------------
    global ask_to_select_main_directory_label
    ask_to_select_main_directory_label = Label(window, text = 'Select the project directory:', font = ('Arial', 15), bg = color, fg = fontColor)
    ask_to_select_main_directory_label.place(relx=0.32, rely=0.25, anchor=CENTER)

    global entry_box_for_file_path
    entry_box_for_file_path=tk.Entry(window, width = 60, font=40)
    entry_box_for_file_path.place(relx=0.5, rely=0.3, anchor=CENTER)

    folder_image_to_click = PhotoImage(file='file_upload_image4.png')
    global folder_image_button
    folder_image_label = Label(image = folder_image_to_click)
    folder_image_label.image = folder_image_to_click
    folder_image_button= Button(window, image = folder_image_to_click,command= open_file, borderwidth=0, height= 20, width= 20)
    folder_image_button.place(relx=0.76, rely=0.3, anchor=CENTER)

    # --------------------- Next button ---------------------
    global next_button
    next_button = Button(window, text ='  Next  ', command = should_we_clear_window, borderwidth=0)
    next_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    return window

# -------------------------------- Open project directory ----------------------------
def open_file():
    global folder_selected_as_project_directory
    folder_selected_as_project_directory = filedialog.askdirectory() # folder selected should be the folder with the tif files
    if folder_selected_as_project_directory is not None:
        # Change the working directory to the directory where the images are.
        os.chdir(folder_selected_as_project_directory) # change the current working directory to the directory selected.
        # populate the entry box with the file path.
        entry_box_for_file_path.insert(tk.END, folder_selected_as_project_directory)
        get_tif_files()

# -------------------------------- Clear kickoff window ----------------------------
def should_we_clear_window():
    # destroy the kickoff window
    entry_box_for_file_path.destroy()
    folder_image_button.destroy()
    next_button.destroy()
    ask_to_select_main_directory_label.destroy()
    global cleared
    cleared = 1
    create_second_window()

# -------------------------------- Create second window ----------------------------
def create_second_window():
    if (cleared == 1):
        global folder_selected_as_project_directory
        config = PPConfig(folder_selected_as_project_directory)

        color = '#0C064A'
        window.configure(bg = color)
        fontColor = '#FFFFFF'
        threshold_label = Label(window, text = 'Threshold value: ', font = ('Arial', 15), bg = color, fg = fontColor)
        threshold_label.place(relx=0.4, rely=0.2, anchor=CENTER)
        global threshold_entry_box
        threshold_entry_box = tk.Entry(window, bd =5)
        threshold_entry_box.insert(END, str(config.threshold))
        threshold_entry_box.place(relx=0.6, rely=0.2, anchor=CENTER)

        #--------------- Label and text entry box for kernel size ------------
        kernel_size_label = Label(window, text = 'Kernel size: ', font = ('Arial', 15), bg = color, fg = fontColor)
        kernel_size_label.place(relx=0.4, rely=0.3, anchor=CENTER)
        global kernel_size_entry_box
        kernel_size_entry_box = tk.Entry(window, bd =5)
        kernel_size_entry_box.insert(END, str(config.kernel_size))
        kernel_size_entry_box.place(relx=0.6, rely=0.3, anchor=CENTER)
        kernel_size_input_value = kernel_size_entry_box.get()


        #--------------- Label and text entry box for min size ------------
        # min size Filters out groups of pixels that are below 700 pixels in area.
        min_size_label = Label(window, text = 'Min size: ', font = ('Arial', 15), bg = color, fg = fontColor)
        min_size_label.place(relx=0.4, rely=0.4, anchor=CENTER)
        global min_size_entry_box
        min_size_entry_box = tk.Entry(window, bd =5)
        min_size_entry_box.insert(END, str(config.min_size))
        min_size_entry_box.place(relx=0.6, rely=0.4, anchor=CENTER)

        #-------------to upload weights file------------------
        ask_to_select_weights_file_label = Label(window, text = 'Select the weights file:', font = ('Arial', 15), bg = color, fg = fontColor)
        ask_to_select_weights_file_label.place(relx=0.1, rely=0.5, anchor=CENTER)

        global entry_box_for_weights_path
        entry_box_for_weights_path=tk.Entry(window, width = 60, font=40)
        entry_box_for_weights_path.insert(END, os.path.join(folder_selected_as_project_directory, config.weights_file)) # automatically chose the weights.pt file that is in the main project directory
        entry_box_for_weights_path.place(relx=0.5, rely=0.5, anchor=CENTER)
        file_image_to_click = PhotoImage(file='weights_file_upload_image.png')

        file_image_label = Label(image = file_image_to_click)
        file_image_label.image = file_image_to_click
        file_image_button= Button(window, image = file_image_to_click,command= open_weights_file, borderwidth=0, height= 23, width= 25)
        file_image_button.place(relx=0.758, rely=0.5, anchor=CENTER)

        #----------------------- Checkbox ----------------------------------
        global var1
        var1 = tk.IntVar()
        c1 = tk.Checkbutton(window, text='Check here if you would like to save area filtered, NN, and threshold mask images',variable=var1, onvalue=1, offvalue=0, command=make_directories_here)
        c1.select() #automatically checks this button
        c1.place(relx=0.5, rely=0.6, anchor=CENTER)

        # ------------------------------- Run ---------------------
        uploadCellImageFolderButton = Button(window, text ='Run', command = on_click)
        uploadCellImageFolderButton.place(relx=0.5, rely=0.7, anchor=CENTER)

# ---------------------------- Second window reference methods ---------------------
def open_weights_file():
     global weights_file_selected
     weights_file_selected = filedialog.askdirectory() # ask what weights file to use.

def make_directories_here():
    make_directories.make_results_directory()
    if(var1.get() == 1):
        make_directories.make_mask_directories()

def on_click():
    get_tif_files()
    update_GUI()
    run_process_images()

def run_process_images():
    global folder_selected_as_project_directory
    configuration = PPConfig(folder_selected_as_project_directory)

    configuration.threshold = int(threshold_entry_box.get())
    configuration.kernel_size = int(kernel_size_entry_box.get())
    configuration.min_size = int(min_size_entry_box.get())
    configuration.write_config()

    make_directories_here()

    global args
    args = {
        "results_directory": make_directories.get_results_directory(),
        "weights_file": entry_box_for_weights_path.get(),
        "write_nn_mask": kernel_size_entry_box.get(),
        "write_threshold_mask": threshold_entry_box.get(),
        "write_area_filtered" : min_size_entry_box.get(),
        "config": configuration
    }

    #for each image in the Images directory:
    for image in list_of_tif_files_in_directory:
        process_images.process_image(image, args)



def get_tif_files():
    global list_of_tif_files_in_directory
    list_of_tif_files_in_directory = []
    list_of_files_in_project_directory = os.listdir(os.path.join(folder_selected_as_project_directory, "Images")) # get the Images directory within the project directory

    for filename_to_examine_for_tif_suffix in list_of_files_in_project_directory: # traverse whole directory
        if filename_to_examine_for_tif_suffix.endswith('.tif'): # check the extension of files
            list_of_tif_files_in_directory.append(filename_to_examine_for_tif_suffix) # add the tif files to the list_of_files_in_project_directory

def update_GUI():
    get_tif_files()
    black_font_color = '#000000'
    tif_files_that_will_run_through_process_images = Label(window, text = str(list_of_tif_files_in_directory ), font = ('Arial', 20), fg = black_font_color)
    tif_files_that_will_run_through_process_images.place(relx=0.5, rely=0.8, anchor=CENTER)


def main(): # main listens for events to happen
    window = kickoff_window()
    window.mainloop()



if __name__ == "__main__":
    main()
