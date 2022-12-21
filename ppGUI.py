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
from configparser import ConfigParser
# list all image names in ttext box on ppGUI.
# combine submit and upload button functions
# check boxes to ask if want images
# make images folder


config_object = ConfigParser()
config_object["IMAGEPROCESSING"] = { "threshold" : '200', 'kernel_size' : '3', 'min_size' : '700'}

def window_dispay():
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

    #--------------- Label and text entry box for threshold ------------
    threshold_label = Label(window, text = 'Threshold value: ', font = ('Courier New', 15), bg = color, fg = fontColor)
    threshold_label.place(relx=0.4, rely=0.2, anchor=CENTER)
    global threshold_entry_box
    threshold_entry_box = Entry(window, bd =5)
    threshold_entry_box.insert(END, '200')
    threshold_entry_box.place(relx=0.6, rely=0.2, anchor=CENTER)
    # ------------ To print configuration value ------------
    global final_threshold_value_label
    final_threshold_value_label = tk.Label(window, text = "")
    final_threshold_value_label.place(relx=0.8, rely=0.2, anchor=CENTER)

    #--------------- Label and text entry box for kernel size ------------
    kernel_size_label = Label(window, text = 'Kernel size: ', font = ('Courier New', 15), bg = color, fg = fontColor)
    kernel_size_label.place(relx=0.4, rely=0.3, anchor=CENTER)
    global kernel_size_entry_box
    kernel_size_entry_box = Entry(window, bd =5)
    kernel_size_entry_box.insert(END, '3')
    kernel_size_entry_box.place(relx=0.6, rely=0.3, anchor=CENTER)
    kernel_size_input_value = kernel_size_entry_box.get()
    # ------------ To print configuration value ------------
    global final_kernel_size_value_label
    final_kernel_size_value_label = tk.Label(window, text = "")
    final_kernel_size_value_label.place(relx=0.8, rely=0.3, anchor=CENTER)

    #--------------- Label and text entry box for min size ------------
    # min size Filters out groups of pixels that are below 700 pixels in area.
    min_size_label = Label(window, text = 'Min size: ', font = ('Courier New', 15), bg = color, fg = fontColor)
    min_size_label.place(relx=0.4, rely=0.4, anchor=CENTER)
    global min_size_entry_box
    min_size_entry_box = Entry(window, bd =5)
    min_size_entry_box.insert(END, '700')
    min_size_entry_box.place(relx=0.6, rely=0.4, anchor=CENTER)
    # ------------ To print configuration value ------------
    global final_min_size_value_label
    final_min_size_value_label = tk.Label(window, text = "")
    final_min_size_value_label.place(relx=0.8, rely=0.4, anchor=CENTER)

    #------------------- Introduction Text ----------------------------------
    introTextLine1 = Label(window, text = 'Welcome to Photo Phenosizer', font = ('Courier New', 40), bg = color, fg = fontColor)
    introTextLine1.place(relx=0.5, rely=0.1, anchor=CENTER)
# choose file before anything else. You can type i nthe path or button thing with file pic.

#------------------------ Get project directory ------------------------
def get_project_directory():
    uploadCellImageFolderButton = Button(window, text ='Click here to upload your photos', command = lambda: [open_file(), get_tif_files(), update_GUI()])

    uploadCellImageFolderButton.place(relx=0.5, rely=0.6, anchor=CENTER)

def open_file():
    folderSelected = filedialog.askdirectory() # folder selected should be the folder with the tif files
    if folderSelected is not None:
        # Change the working directory to the directory where the images are.
        os.chdir(folderSelected) # change the current working directory to the directory selected.
        get_tif_files()
        # cwd = os.getcwd() # Get the file path of the directory with the images
        # #list_of_tif_files = os.listdir(cwd) # Get the list of image names
        # #list_of_tif_files_without_commas_and_spaces = ' '.join(list_of_tif_files)
        # #print(list_of_tif_files_without_commas_and_spaces)
        # list_of_tif_files_in_directory = []
        # list_of_files_in_project_directory = os.listdir(cwd)
        # for filename_to_examine_for_tif_suffix in list_of_files_in_project_directory: # traverse whole directory
        #     if filename_to_examine_for_tif_suffix.endswith('.tif'): # check the extension of files
        #         list_of_tif_files_in_directory.append(filename_to_examine_for_tif_suffix) # add the tif files to the list_of_files_in_project_directory

        # we are in the directory where the images are. Now we want to run process_images.py
        #process_images.main()
        #os.chdir('../') # move back to the main project directory
        #command = "python3 process_images.py " + list_of_tif_files_without_commas_and_spaces

        # import process_image from make_directories()  . NEED THIS FOR ERROR HANDLING
        # "processing this image now..."

def run_process_images():
    command = "python3 process_images.py *tif"
    os.system(command)


def get_tif_files():
    cwd = os.getcwd() # Get the file path of the directory with the images
    global list_of_tif_files_in_directory
    list_of_tif_files_in_directory = []
    list_of_files_in_project_directory = os.listdir(cwd)
    for filename_to_examine_for_tif_suffix in list_of_files_in_project_directory: # traverse whole directory
        if filename_to_examine_for_tif_suffix.endswith('.tif'): # check the extension of files
            list_of_tif_files_in_directory.append(filename_to_examine_for_tif_suffix) # add the tif files to the list_of_files_in_project_directory

def update_GUI():
    get_tif_files()
    black_font_color = '#000000'
    tif_files_that_will_run_through_process_images = Label(window, text = str(list_of_tif_files_in_directory ), font = ('Courier New', 20), fg = black_font_color)
    tif_files_that_will_run_through_process_images.place(relx=0.5, rely=0.8, anchor=CENTER)


#------------------------ Configuration ------------------------
def submit_button():
    submit_button = tk.Button(window, text = "Submit configs", command = lambda: [getInput(), configure(), printInput()])
    submit_button.place(relx=0.5, rely=0.5, anchor=CENTER)

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

def configure():
    image_processing_section = config_object["IMAGEPROCESSING"] # Get the IMAGEPROCESSING section
    # ----------- cheeck if text was entered in threshold entry box -------------
    if len(threshold_input_value) != 0 : # We check to see if the entry box is empty by determining if the entry's length is zero. So if not then overwrite the default value.
        image_processing_section["threshold"] = str(threshold_input_value) # Get the threshold key and update its value the threshold
    # ----------- cheeck if text was entered in min_size entry box -------------
    if len(min_size_input_value) != 0 : # We check to see if the entry box is empty by determining if the entry's length is zero. So if not then overwrite the default value.
        image_processing_section["min_size"] = str(min_size_input_value) # Get the threshold key and update its value the threshold
    if len(kernel_size_input_value) != 0:
        image_processing_section["kernel_size"] = str(kernel_size_input_value)

def printInput():
    image_processing_section = config_object["IMAGEPROCESSING"] # Get the IMAGEPROCESSING section
    # ------- print input for theshold -----------
    final_theshold_input_value = image_processing_section["threshold"]
    final_threshold_value_label.config(text = "Provided Input: "+ final_theshold_input_value)
    # ------- print input for min_size -----------
    final_min_size_input_value = image_processing_section["min_size"]
    final_min_size_value_label.config(text = "Provided Input: "+ final_min_size_input_value )
    # ------- print input for kernel_size -----------
    final_kernel_size_input_value = image_processing_section["kernel_size"]
    final_kernel_size_value_label.config(text = "Provided Input: "+ final_kernel_size_input_value )

#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)


def main():
    window_dispay()
    # now do pp_config.py
    submit_button()
    get_project_directory() # gets the project directory
    


if __name__ == "__main__":
    main()


window.mainloop()
run_process_images() # run process_images with command line
