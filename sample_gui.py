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

# the kickoff frame is where the files can be chosen
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

    #-------------------Folder upload-----------------
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


def open_file():
    global folderSelected
    folderSelected = filedialog.askdirectory() # folder selected should be the folder with the tif files
    if folderSelected is not None:
        # Change the working directory to the directory where the images are.
        os.chdir(folderSelected) # change the current working directory to the directory selected.
        # populate the entry box with the file path.
        entry_box_for_file_path.insert(tk.END, folderSelected)
        get_tif_files()

def should_we_clear_window():
    # destroy the kickoff window
    entry_box_for_file_path.destroy()
    folder_image_button.destroy()
    next_button.destroy()
    global cleared
    cleared = 1
    create_second_window()

def create_second_window():
    if (cleared == 1):
        color = '#0C064A'
        window.configure(bg = color)
        fontColor = '#FFFFFF'
        threshold_label = Label(window, text = 'Threshold value: ', font = ('Arial', 15), bg = color, fg = fontColor)
        threshold_label.place(relx=0.4, rely=0.2, anchor=CENTER)
        global threshold_entry_box
        threshold_entry_box = Entry(window, bd =5)
        threshold_entry_box.insert(END, '200')
        threshold_entry_box.place(relx=0.6, rely=0.2, anchor=CENTER)

        #--------------- Label and text entry box for kernel size ------------
        kernel_size_label = Label(window, text = 'Kernel size: ', font = ('Arial', 15), bg = color, fg = fontColor)
        kernel_size_label.place(relx=0.4, rely=0.3, anchor=CENTER)
        global kernel_size_entry_box
        kernel_size_entry_box = Entry(window, bd =5)
        kernel_size_entry_box.insert(END, '3')
        kernel_size_entry_box.place(relx=0.6, rely=0.3, anchor=CENTER)
        kernel_size_input_value = kernel_size_entry_box.get()


        #--------------- Label and text entry box for min size ------------
        # min size Filters out groups of pixels that are below 700 pixels in area.
        min_size_label = Label(window, text = 'Min size: ', font = ('Arial', 15), bg = color, fg = fontColor)
        min_size_label.place(relx=0.4, rely=0.4, anchor=CENTER)
        global min_size_entry_box
        min_size_entry_box = Entry(window, bd =5)
        min_size_entry_box.insert(END, '700')
        min_size_entry_box.place(relx=0.6, rely=0.4, anchor=CENTER)

        #-------------to upload weights file------------------
        # global entry_box_for_weights_path
        # entry_box_for_weights_path=tk.Entry(window, width = 60, font=40)
        # entry_box_for_weights_path.place(relx=0.5, rely=0.3, anchor=CENTER)
        #
        # file_image_to_click = PhotoImage(file='file_upload_image4.png')
        # global folder_image_button
        # file_image_label = Label(image = file_image_to_click)
        # file_image_label.image = file_image_to_click
        # file_image_button= Button(window, image = file_image_label,command= open_weights_file, borderwidth=0, height= 20, width= 20)
        # file_image_button.place(relx=0.76, rely=0.5, anchor=CENTER)

        #----------------------- Checkboxes ----------------------------------
        var1 = 0
        c1 = tk.Checkbutton(window, text='Check here if you would like area filtered masks, nn masks, and threshold masks',variable=var1, onvalue=1, offvalue=0, command=checkbox_selection)
        c1.place(relx=0.5, rely=0.6, anchor=CENTER)

        # ------------------------------- Run ---------------------
        uploadCellImageFolderButton = Button(window, text ='Run', command = on_click)
        uploadCellImageFolderButton.place(relx=0.5, rely=0.7, anchor=CENTER)

# def open_weights_file():
#     global weights_file_selected
#     weights_file_selected = filedialog.askdirectory() # folder selected should be the folder with the tif files
#     if weights_file_selected is not None:
#
#         entry_box_for_weights_path.insert(tk.END, weights_file_selected)


def checkbox_selection():
         x =1 # just a filler
    #     if var1.get ==1: # if the box is checked
            # call process_images.make_directories()
        # else do nothing. do not make directories.

def on_click():
    #configurations()
    get_tif_files()
    update_GUI()
    run_process_images()

def run_process_images():
    global args
    args = {
        "weights_file": cli_args.weights_file,
        "write_nn_mask": kernel_size_entry_box.get(),
        "write_threshold_mask": int(threshold_entry_box.get()),
        "write_area_filtered" : int(min_size_entry_box.get()),
        "config": PPConfig(os.getcwd())
    }

    #for each image in the Images directory:
    for image in list_of_tif_files_in_directory:
        process_images.process_image(image, args)

    #process_images.process_image()
    #command = "python3 process_images.py *tif"
    #os.system(command)

def get_tif_files():
    cwd = os.getcwd() # Get the file path of the directory with the images
    global list_of_tif_files_in_directory
    list_of_tif_files_in_directory = []
    list_of_files_in_project_directory = os.listdir(os.path.join(folderSelected, "Images"))

    for filename_to_examine_for_tif_suffix in list_of_files_in_project_directory: # traverse whole directory
        if filename_to_examine_for_tif_suffix.endswith('.tif'): # check the extension of files
            list_of_tif_files_in_directory.append(filename_to_examine_for_tif_suffix) # add the tif files to the list_of_files_in_project_directory

def update_GUI():
    get_tif_files()
    black_font_color = '#000000'
    tif_files_that_will_run_through_process_images = Label(window, text = str(list_of_tif_files_in_directory ), font = ('Arial', 20), fg = black_font_color)
    tif_files_that_will_run_through_process_images.place(relx=0.5, rely=0.8, anchor=CENTER)


#------------------------ Configuration ------------------------
def getInput():
    # ------- get input for theshold -----------
    global threshold_input_value
    threshold_input_value = threshold_entry_box.get() # get the input text
    # ------- get input for min size -----------
    global min_size_input_value
    min_size_input_value = min_size_entry_box.get() # get the input text
    # ------- get input for kernel_size -----------
    global kernel_size_input_value
    kernel_size_input_value = kernel_size_entry_box.get()

def configurations():
    global folderSelected
    os.chdir(folderSelected)
    configuration = PPConfig
    configuration = PPConfig(folderSelected)

    configuration.write_config()
    configuration.theshold = int(threshold_entry_box.get())
    print(configuration.threshold)
    configuration.write_config()

def main(): # main listens for events to happen
    window = kickoff_window()
    window.mainloop()



if __name__ == "__main__":
    main()
