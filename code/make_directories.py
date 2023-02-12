
import time
import os
from datetime import datetime


def make_results_directory(folder_selected_as_project_directory):
    # ----------- Make results directory ---------
    current_time = datetime.now() # datetime object containing current date and time
    date_and_time_string = current_time.strftime("Results %Y-%m-%d %H-%M-%S")
    global results_directory_name
    results_directory_name = date_and_time_string
    #x = str(os.path.join(project_directory, results_directory_name))
    results_directory_name = os.path.join(folder_selected_as_project_directory, results_directory_name)
    os.makedirs(results_directory_name, exist_ok=True) # Make the directory called results_directory_name so that we can add the csv files to this directory
    return results_directory_name

def make_mask_directories(res_dir):
    # ----------- Make area_filtered_masks directory ---------
    path_for_area_filtered_masks_directory = os.path.join(res_dir, 'area_filtered_masks') # The results_directory_name is the parent directory for area_filtered_masks_directory
    os.mkdir(path_for_area_filtered_masks_directory)

    # ----------- Make nn_masks directory ---------
    path_for_nn_masks_directory = os.path.join(res_dir, 'nn_masks') # The results_directory_name is the parent directory for nn_masks_directory
    os.mkdir(path_for_nn_masks_directory)

    # ----------- Make threshold_masks directory ---------
    path_for_threshold_masks_directory = os.path.join(res_dir, 'threshold_masks') # The results_directory_name is the parent directory for threshold_masks_directory
    os.mkdir(path_for_threshold_masks_directory)


# do all of the above functions
def main_for_directories():
    make_results_directory()
    make_mask_directories()


if __name__ == "__main_for_directories__":
    main_for_directories()
