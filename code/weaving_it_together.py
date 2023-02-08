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
global folder_has_been_selected
folder_has_been_selected = 0
from pathlib import Path

import kickoff_window

import second_window
#window = tk.Tk()

def weave_it_all_together():
    import kickoff_window
    #get_code_directory()
    kickoff_window.main() # Display the kickoff window
    final_folder = kickoff_window.uggg_return() # get the final folder value from kickoff window file
    #clear_kickoff_window()
    #final_folder = return_final_folder(final_folder)
    print('final fold: ' + str(final_folder))

    #lambda: second_window.create_second_window()
    return kickoff_window






# def get_code_directory():
#     code_dir = os.getcwd()
#     return code_dir


def main(): # main listens for events to happen
    weave = weave_it_all_together()
    weave.mainloop()

if __name__ == "__main__":
    weave = weave_it_all_together()
    weave.mainloop()
