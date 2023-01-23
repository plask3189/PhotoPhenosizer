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
def kickoff_window():
    '''
    The kickoff frame is where the project directory is chosen. Once chosen, the user presses the next button which 'routes' to the second window.
    '''
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
    ask_to_select_main_directory_label = Label(window, text = 'Select your project directory:', font = ('Arial', 15), bg = color, fg = fontColor)
    ask_to_select_main_directory_label.place(relx=0.32, rely=0.25, anchor=CENTER)

    #------------------- Entry textbox for main directory file path -----------------
    global entry_box_for_file_path
    entry_box_for_file_path=tk.Entry(window, width = 60, font=40)
    entry_box_for_file_path.place(relx=0.5, rely=0.3, anchor=CENTER)
    folder_image_to_click = PhotoImage(file='file_upload_image4.png')

    # ----------------- Folder image -------------------
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

def kickoff_window_widgets_to_create_after_pressing_back_button():
    '''
    This is the method called after pressing the back button. It is essentially the same as the kickoff_window() method but without the window creation. This is so that a new window doesn't pop up when we press the next button. Rather, we stay on the same window but recreate the kickoff window widgets.
    '''
    color = '#0C064A'
    window.configure(bg = color)
    fontColor = '#FFFFFF'  # font color is white
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
    global folder_has_been_selected
    folder_has_been_selected = 0
    global folder_selected_as_project_directory
    folder_selected_as_project_directory = filedialog.askdirectory() # folder selected should be the folder with the tif files
    return_folder_selected_as_project_directory(folder_selected_as_project_directory)
    if folder_selected_as_project_directory is not None:
        folder_has_been_selected = 1
        # Change the working directory to the directory where the images are.

        entry_box_for_file_path.insert(tk.END, folder_selected_as_project_directory) # populate the entry box with the file path.
        get_tif_files()



def return_folder_selected_as_project_directory(folder_selected_as_project_directory):
    return folder_selected_as_project_directory


# -------------------------------- Clear kickoff window ----------------------------
def should_we_clear_window(): # destroy the kickoff window
    entry_box_for_file_path.destroy()
    folder_image_button.destroy()
    next_button.destroy()
    ask_to_select_main_directory_label.destroy()
    #global cleared
    cleared = 1
    #did_the_user_select_a_project_directory()
    return cleared
    create_second_window(cleared)


# -------------------------------- Create second window ----------------------------
def create_second_window(cleared):
    global list_of_second_window_widgets
    list_of_second_window_widgets = []
    if (cleared == 1): #if we just cleared the kickoff window, we create the second window.
        return_folder_selected_as_project_directory() # get the folder
        config = PPConfig(folder_selected_as_project_directory)
        color = '#0C064A'
        window.configure(bg = color)
        fontColor = '#FFFFFF'

        #----------------------- Threshold label ---------------------------
        threshold_label = Label(window, text = 'Threshold value: ', font = ('Arial', 15), bg = color, fg = fontColor)
        list_of_second_window_widgets.append(threshold_label)
        threshold_label.place(relx=0.4, rely=0.2, anchor=CENTER)

        #----------------------- More info button for threshold ---------------------------
        more_info_image = PhotoImage(file='more_info_icon.png')
        more_info_label = Label(image = more_info_image)
        more_info_label.image = more_info_image
        list_of_second_window_widgets.append(more_info_label)
        more_info_button= Button(window, image = more_info_image,command= threshold_info_popup, borderwidth=0, height= 18, width= 22)
        list_of_second_window_widgets.append(more_info_button)
        more_info_button.place(relx=0.32, rely=0.2, anchor=CENTER)

        #----------------------- Checkbox ---------------------------
        global threshold_entry_box
        threshold_entry_box = tk.Entry(window, bd =5)
        list_of_second_window_widgets.append(threshold_entry_box)
        threshold_entry_box.insert(END, str(config.threshold))
        threshold_entry_box.place(relx=0.6, rely=0.2, anchor=CENTER)

        #--------------- Label and text entry box for kernel size ------------
        kernel_size_label = Label(window, text = 'Kernel size: ', font = ('Arial', 15), bg = color, fg = fontColor)
        kernel_size_label.place(relx=0.4, rely=0.3, anchor=CENTER)
        list_of_second_window_widgets.append(kernel_size_label)
        global kernel_size_entry_box
        kernel_size_entry_box = tk.Entry(window, bd =5)
        list_of_second_window_widgets.append(kernel_size_entry_box)
        kernel_size_entry_box.insert(END, str(config.kernel_size))
        kernel_size_entry_box.place(relx=0.6, rely=0.3, anchor=CENTER)
        kernel_size_input_value = kernel_size_entry_box.get()

        #----------------------- More info button for kernel size ---------------------------
        more_info_button_for_kernel_size= Button(window, image = more_info_image,command= kernel_size_info_popup, borderwidth=0, height= 18, width= 22)
        list_of_second_window_widgets.append(more_info_button_for_kernel_size)
        more_info_button_for_kernel_size.place(relx=0.32, rely=0.3, anchor=CENTER)

        #--------------- Label and text entry box for min size ------------
        min_size_label = Label(window, text = 'Min size: ', font = ('Arial', 15), bg = color, fg = fontColor)
        min_size_label.place(relx=0.4, rely=0.4, anchor=CENTER)
        list_of_second_window_widgets.append(min_size_label)
        global min_size_entry_box
        min_size_entry_box = tk.Entry(window, bd =5)
        min_size_entry_box.insert(END, str(config.min_size))
        min_size_entry_box.place(relx=0.6, rely=0.4, anchor=CENTER)
        list_of_second_window_widgets.append(min_size_entry_box)

        #----------------------- More info button for min size ---------------------------
        more_info_button_for_min_size= Button(window, image = more_info_image,command= min_size_info_popup, borderwidth=0, height= 18, width= 22)
        list_of_second_window_widgets.append(more_info_button_for_min_size)
        more_info_button_for_min_size.place(relx=0.32, rely=0.4, anchor=CENTER)

        #------------- To upload weights file------------------
        ask_to_select_weights_file_label = Label(window, text = 'Select the weights file:', font = ('Arial', 15), bg = color, fg = fontColor)
        ask_to_select_weights_file_label.place(relx=0.1, rely=0.5, anchor=CENTER)
        list_of_second_window_widgets.append(ask_to_select_weights_file_label)
        global entry_box_for_weights_path
        entry_box_for_weights_path=tk.Entry(window, width = 60, font=40)
        entry_box_for_weights_path.insert(END, os.path.join(folder_selected_as_project_directory, config.weights_file)) # automatically chose the weights.pt file that is in the main project directory
        list_of_second_window_widgets.append(entry_box_for_weights_path)
        entry_box_for_weights_path.place(relx=0.5, rely=0.5, anchor=CENTER)

        file_image_to_click = PhotoImage(file='weights_file_upload_image.png')
        file_image_label = Label(image = file_image_to_click)
        file_image_label.image = file_image_to_click
        list_of_second_window_widgets.append(file_image_label)
        file_image_button= Button(window, image = file_image_to_click,command= open_weights_file, borderwidth=0, height= 23, width= 25)
        list_of_second_window_widgets.append(file_image_button)
        file_image_button.place(relx=0.758, rely=0.5, anchor=CENTER)
        #----------------------- Checkbox ----------------------------------
        global var1
        var1 = tk.IntVar()
        c1 = tk.Checkbutton(window, text='Check here if you would like to save area filtered, NN, and threshold mask images',variable=var1, onvalue=1, offvalue=0, command=make_directories_here)
        c1.select() #automatically checks this button
        c1.place(relx=0.5, rely=0.6, anchor=CENTER)
        list_of_second_window_widgets.append(c1)
        #------------------------------- Button Frame---------------------
        white_color = '#FFFFFF'
        button_frame_frame = Frame(window, bg = white_color, width = 205, height = 51.25)
        #button_frame_frame.pack()
        button_frame_frame.place(relx=0.5, rely=0.7, anchor=CENTER)

        grey_color = '#000000'
        button_frame = Frame(button_frame_frame, bg = grey_color, width = 200.5, height = 49.5)
        #button_frame.pack()
        button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # ------------------------------- Run Button---------------------
        run_button = Button(button_frame, text ='Run', command = on_click) # look into ways to pass the project dir at binding time. Project dir is param for process, in process, get list of images.
        run_button.place(relx=0.8, rely=0.5, anchor=CENTER)
        list_of_second_window_widgets.append(run_button)
        # --------------------- Back Button ---------------------
        global back_button
        back_button = Button(button_frame, text ='Back', command = back)
        back_button.place(relx=0.2, rely=0.5, anchor=CENTER)
        #list_of_second_window_widgets(back_button)

        return window

def threshold_info_popup():
    print('threshold')
    popup_title = "More info on threshold"
    tkinter.messagebox.showinfo(popup_title,  "I am telling you about what threshold configuration does.")
def kernel_size_info_popup():
    # populate popup box with kernel_size info
    print('hi')
    popup_title = "More info on kernel size"
    tkinter.messagebox.showinfo(popup_title,  "I am telling you about what kernel size configuration does.")
def min_size_info_popup():
    # populate popup box with min_size info
    print('hi')
    popup_title = "More info on min size"
    tkinter.messagebox.showinfo(popup_title,  "I am telling you about what min size configuration does.")


def clear_second_window(): # if we press the back button on the second window, we need to clear this second window.
    for x in list_of_second_window_widgets:
        x.destroy()

def back():
    '''
    The command called when the back button is pressed.
    '''
    clear_second_window()
    kickoff_window_widgets_to_create_after_pressing_back_button()
    back_button.destroy()

# ---------------------------- Second window reference methods ---------------------
def open_weights_file():
     global weights_file_selected
     weights_file_selected = filedialog.askopenfile() # ask what weights file to use.

def make_directories_here():
    make_directories.make_results_directory()
    if(var1.get() == 1): # if the user checks the box saying that they want to save the configuration images, make the directories to save those images
        make_directories.make_mask_directories()

def on_click(): # when click the RUN button
    return_list_of_images() #
    #update_GUI()
    run_process_images()



# *****************************************************************************************************************************************************************************************************
def run_process_images():
    # parent_of_images_directory = Path(os.getcwd()).resolve().parents[0] # should be photophenosizerkp
    # print(parent_of_images_directory)
    # find tif files here
    return_folder_selected_as_project_directory() # get the folder
    parent_of_project_directory = (folder_selected_as_project_directory).resolve().parents[0] # should be photophenosizerkp
    print(str(parent_of_project_directory))
    os.chdir(folder_selected_as_project_directory)

    make_directories_here() # pass in folder_selected_as_project_directory

    #navigate to code directory? j
    #join(parent_of_project_directoryfolder_selected_as_project_directory)
    print("hi" + folder_selected_as_project_directory)
    configuration = PPConfig(folder_selected_as_project_directory)
    configuration.threshold = int(threshold_entry_box.get())
    configuration.kernel_size = int(kernel_size_entry_box.get())
    configuration.min_size = int(min_size_entry_box.get())
    configuration.write_config()
    #make_directories_here()
    global args
    args = {
        "results_directory": make_directories.get_results_directory(),
        "weights_file": entry_box_for_weights_path.get(),
        "write_nn_mask": kernel_size_entry_box.get(),
        "write_threshold_mask": threshold_entry_box.get(),
        "write_area_filtered" : min_size_entry_box.get(),
        "config": configuration
    }
    global already_processed
    images_dir_path = os.path.join(folder_selected_as_project_directory, 'Images')
    print('in sample_gui, the images dir:' + str(images_dir_path))
    os.chdir(images_dir_path)
    already_processed = []
    index = 0
    #print(list_of_tif_files_in_directory)
    for image in list_of_tif_files_in_directory: #for each image in the Images directory:
        os.chdir(images_dir_path)
        already_processed.append(image) # add the image name to the list of already processed images
        update_scroll() # update the section with the scrollbar to display images names as they are processed
        process_images.process_image(image, args)
        index = index + 1
        if(index+1 == len(list_of_tif_files_in_directory)):
            print("DONEEE")

# *****************************************************************************************************************************************************************************************************




def update_scroll():
    # create the text widget
    global text
    global scrollbar
    color = '#0C064A'
    fontColor = '#FFFFFF'
    label_for_scroll_section = Label(window, text = 'Images processed: ', font = ('Arial', 15), bg = color, fg = fontColor)
    label_for_scroll_section.place(relx=0.5, rely=0.76, anchor=CENTER)

    scroll_frame = Frame(window, bg = '#000000', borderwidth=1, relief="sunken")
    scroll_frame.place(relx=0.5, rely=0.9, anchor=CENTER) # scroll_frame defines the display location of text of the processed images with a scrollbar.
    scrollbar_widget = Scrollbar(scroll_frame, orient='vertical')
    scrollbar_widget.pack(side=RIGHT, fill='y')

    text_widget = Text(scroll_frame, height = 8, width = 30, font=("Arial, 14"), yscrollcommand=scrollbar_widget.set)

    for i in range(1,500):
        position = f'{i}.0'
    for image in already_processed: # add text to the text widget to show the screen
        text_widget.insert(position, image + '\n');

    # Attach the scrollbar with the text widget
    scrollbar_widget.config(command=text_widget.yview)
    text_widget.pack()

    Tk.update(window)

def get_tif_files(): # parameter: folder_selected_as_project_directory. return list_of_tif_files_in_directory.
    global list_of_tif_files_in_directory
    #list_of_all_files_in_directory = []
    list_of_tif_files_in_directory = []
    images_dir_name = os.path.join(folder_selected_as_project_directory, 'Images') # Navigate to the images directory
    print("images dir name: " + images_dir_name)
    list_of_all_files_in_directory = os.listdir(images_dir_name) # get a list of all names in the Images directory.
    print(list_of_tif_files_in_directory)
    for filename_to_examine_for_tif_suffix in list_of_all_files_in_directory: # traverse whole directory
        if filename_to_examine_for_tif_suffix.endswith('.tif'): # check the extension of files. There is usually a sneaky .DS-Store file that requires us to weed it out.
            list_of_tif_files_in_directory.append(filename_to_examine_for_tif_suffix) # add the tif files to the list_of_files_in_project_directory

    #list_of_all_files_in_directory= listdir(folder_selected_as_project_directory)
    #os.path.join(folder_selected_as_project_directory, )
    # for filename_to_examine_for_tif_suffix in list_of_all_files_in_directory: # traverse whole directory
    #     # include the full file path name when appending to the list of tif files
    #     if filename_to_examine_for_tif_suffix.endswith('.tif'): # check the extension of files
    #         list_of_tif_files_in_directory.append(filename_to_examine_for_tif_suffix) # add the tif files to the list_of_files_in_project_directory


def return_list_of_images():
    print(list_of_tif_files_in_directory)
    return list_of_tif_files_in_directory

def update_GUI():
    color = '#0C064A'
    return_list_of_images()
    font_color = '#FFFFFF'

    #------------- print 'done' message --------------
    done_label = Label(window, text = 'Done', font = ('Arial', 20), bg = color, fg = font_color)
    done_label.place(relx=0.5, rely=0.9, anchor=CENTER)


def main(): # main listens for events to happen
    window = kickoff_window()
    window.mainloop()

if __name__ == "__main__":
    main()
