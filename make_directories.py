
import time
import os
from datetime import datetime

global results_directory_name

# param return results directory name
# What to do is 1 or 0

# how to pass in boolean
# def make_results_directory(what_to_do):
#     if(what_to_do == 1): # if we want to make the directories
#         # ----------- Make results directory ---------
#         current_time = datetime.now() # datetime object containing current date and time
#         date_and_time_string = current_time.strftime("Results %Y-%m-%d %H-%M-%S")
#         global results_directory_name
#         results_directory_name = date_and_time_string
#         #x = str(os.path.join(project_directory, results_directory_name))
#         os.makedirs(results_directory_name, exist_ok=True) # Make the directory called results_directory_name so that we can add the csv files to this directory
#         print(results_directory_name)
#     if(what_to_do == 0):
#         return results_directory_name

def make_results_directory():
    # ----------- Make results directory ---------
    current_time = datetime.now() # datetime object containing current date and time
    date_and_time_string = current_time.strftime("Results %Y-%m-%d %H-%M-%S")
    global results_directory_name
    results_directory_name = date_and_time_string
    #x = str(os.path.join(project_directory, results_directory_name))
    os.makedirs(results_directory_name, exist_ok=True) # Make the directory called results_directory_name so that we can add the csv files to this directory
    return results_directory_name

def get_results_directory():
    results_directory_from_above_method = make_results_directory()
    # current_time = datetime.now() # datetime object containing current date and time
    # date_and_time_string = current_time.strftime("Results %Y-%m-%d %H-%M-%S")
    # results_directory_name = date_and_time_string
    return results_directory_from_above_method

def make_mask_directories():
#def make_area_filtered_masks_directory():
    # ----------- Make area_filtered_masks directory ---------
    area_filtered_masks_directory = 'area_filtered_masks'
    path_for_area_filtered_masks_directory = os.path.join(results_directory_name, area_filtered_masks_directory) # The results_directory_name is the parent directory for area_filtered_masks_directory
    os.mkdir(path_for_area_filtered_masks_directory)
    #return area_filtered_masks_directory
#def make_nn_masks_directory():
    # ----------- Make nn_masks directory ---------
    nn_masks_directory = 'nn_masks'
    path_for_nn_masks_directory = os.path.join(results_directory_name, nn_masks_directory) # The results_directory_name is the parent directory for nn_masks_directory
    os.mkdir(path_for_nn_masks_directory)
    #return nn_masks_directory

#def  make_theshold_masks_directory():
    # ----------- Make threshold_masks directory ---------
    threshold_masks_directory = 'threshold_masks'
    path_for_threshold_masks_directory = os.path.join(results_directory_name, threshold_masks_directory) # The results_directory_name is the parent directory for threshold_masks_directory
    os.mkdir(path_for_threshold_masks_directory)
    #return threshold_masks_directory


# do all of the above functions
def main_for_directories():
    make_results_directory()
    make_mask_directories()


if __name__ == "__main_for_directories__":
    main_for_directories()
