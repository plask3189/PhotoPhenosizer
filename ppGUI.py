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

    threshold_label = Label(window, text = 'Threshold value: ', font = ('Courier New', 15), bg = color, fg = fontColor)
    threshold_label.place(relx=0.4, rely=0.2, anchor=CENTER)
    threshold_entry_box = Entry(window, bd =5)
    threshold_entry_box.place(relx=0.6, rely=0.2, anchor=CENTER)

    kernel_size_label = Label(window, text = 'Kernel size: ', font = ('Courier New', 15), bg = color, fg = fontColor)
    kernel_size_label.place(relx=0.4, rely=0.3, anchor=CENTER)
    kernel_size_entry_box = Entry(window, bd =5)
    kernel_size_entry_box.place(relx=0.6, rely=0.3, anchor=CENTER)

    # min size Filters out groups of pixels that are below 700 pixels in area.
    min_size_label = Label(window, text = 'Min size: ', font = ('Courier New', 15), bg = color, fg = fontColor)
    min_size_label.place(relx=0.4, rely=0.4, anchor=CENTER)
    min_size_entry_box = Entry(window, bd =5)
    min_size_entry_box.place(relx=0.6, rely=0.4, anchor=CENTER)

    #------------------- Introduction Text ----------------------------------
    introTextLine1 = Label(window, text = 'Welcome to Photo Phenosizer', font = ('Courier New', 40), bg = color, fg = fontColor)
    introTextLine1.place(relx=0.5, rely=0.1, anchor=CENTER)

    # introTextLine3 = Label(window, text = 'Make sure that your pics and weights file are in the same folder that you choose below.', font = ('Courier New', 15), bg = color, fg = fontColor)
    # introTextLine3.place(relx=0.5, rely=0.3, anchor=CENTER)

#------------------------ Get project directory ------------------------
def get_project_directory():
    uploadCellImageFolderButton = Button(window, text ='Click here to upload your photos', command = lambda:open_file())
    uploadCellImageFolderButton.place(relx=0.5, rely=0.5, anchor=CENTER)

def open_file():
    folderSelected = filedialog.askdirectory()
    if folderSelected is not None:
        # Change directory to the directory where the images are.
        os.chdir(folderSelected)
        cwd = os.getcwd()
        print(cwd)
        # we are in the directory where the images are. Now we want to run process_images.py
        command = "python3 process_images.py *tif"
        os.system(command)

#------------------------ Entries ------------------------
#def configuration_entries



def main():
    window_dispay()
    get_project_directory()

if __name__ == "__main__":
    main()



window.mainloop()
