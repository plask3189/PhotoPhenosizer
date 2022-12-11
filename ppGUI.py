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


window = tk.Tk()
window.title('Photo Phenosizer')
window.geometry('1000x700') # width by height
color = '#0C064A'
bg = color
window.configure(bg = color)
fontColor = '#FFFFFF'
#bg = tk.PhotoImage(file = '~/Documents/GitHub/PhotoPhenosizer/q1Green.png')
#canvas = Canvas(window,width= 400, height= 200)
#canvas.pack(expand=True, fill= BOTH)
#canvas.create_image(0,0,image=bg, anchor="nw")
canvas = Canvas()

#------------------- Introduction Text -------------------------------------------------------------

introTextLine1 = Label(window, text = 'Welcome to Photo Phenosizer', font = ('Courier New', 40), bg = color, fg = fontColor)
introTextLine1.place(relx=0.5, rely=0.1, anchor=CENTER)

introTextLine2 = Label(window, text = 'Ensure that you have the weights.pt file in the same folder as the images you would like to run.', font = ('Courier New', 15), bg = color, fg = fontColor)
introTextLine2.place(relx=0.5, rely=0.2, anchor=CENTER)

introTextLine3 = Label(window, text = 'Make sure that your pics and weights file are in the same folder that you choose below.', font = ('Courier New', 15), bg = color, fg = fontColor)
introTextLine3.place(relx=0.5, rely=0.3, anchor=CENTER)

# var1 = tk.IntVar()
# c1 = tk.Checkbutton(window, text='Check here if this is your first time running Photo Phenosizer',variable=var1, onvalue=1, offvalue=0, font = ('Courier New', 15), bg = color, fg = fontColor)
# c1.place(relx=0.5, rely=0.4, anchor=CENTER)

uploadCellImageFolderButton = Button(window, text ='Click here to upload your photos', command = lambda:open_file())
uploadCellImageFolderButton.place(relx=0.5, rely=0.5, anchor=CENTER)


#-------------------- Upload folder with cell images and weights.pt --------------------------------

# if NOT check marked
def open_file():
    # if (var1.get() == 1): # the checkbox is checked, so first time running
    #     folderSelected = filedialog.askdirectory()
    #     # print(folderSelected) :
    #     # /Users/kateplas/Documents/GitHub/PhotoPhenosizer/imagesExample
    #     if folderSelected is not None:
    #         # Change directory to the directory where the images are.
    #         os.chdir(folderSelected)
    #         cwd = os.getcwd()
    #         print(cwd)
    #         # we are in the directory where the images are. Now we want to run process_images.py
    #         # ----------Dowloads check -----------------------
    #         command0 = 'sudo apt-get install git'
    #         command1 = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    #         command2 = 'sudo apt install curl'
    #         command3 = 'sudo apt install python-is-python3'
    #         command4 = 'sudo apt install python3-pip'
    #         command5 = 'pip install opencv-python'
    #         command6 = 'pip install xgboost'
    #         command7 = 'pip install feret'
    #         command8 = 'git clone git@github.com:XavierCompBio/PhotoPhenosizer.git'
    #         command9 = 'pip install nx_config'
    #         command = "python3 process_images.py *tif"
    #         os.system(command0)
    #         os.system(command1)
    #         os.system(command2)
    #         os.system(command3)
    #         os.system(command4)
    #         os.system(command5)
    #         os.system(command6)
    #         os.system(command7)
    #         os.system(command8)
    #         os.system(command9)
    #         os.system(command)
    # else: # the checkbox is not checked, so we've run pp before.
    folderSelected = filedialog.askdirectory()
    # print(folderSelected) :
    # /Users/kateplas/Documents/GitHub/PhotoPhenosizer/imagesExample
    if folderSelected is not None:
        # Change directory to the directory where the images are.
        os.chdir(folderSelected)
        cwd = os.getcwd()
        print(cwd)
        # we are in the directory where the images are. Now we want to run process_images.py
        command = "python3 process_images.py *tif"
        os.system(command)
        
window.mainloop()
