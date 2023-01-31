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


def weave_it_all_together():
    import kickoff_window

    kickoff_window.main() # Display the kickoff window
    final_folder = kickoff_window.uggg_return()
    #final_folder = return_final_folder(final_folder)
    print('final fold: ' + str(final_folder))
    is_kickoff_window_cleared = kickoff_window.get_cleared_value(1) # get the cleared value from the kickoff window to check if all of the widgets have been removed in order to clear the window for the second window.


    return 'hi'





# def main(): # main listens for events to happen
#     weave = weave_it_all_together()
#     weave.mainloop()

if __name__ == "__main__":
    weave = weave_it_all_together()
    weave.mainloop()
