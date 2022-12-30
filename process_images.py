import csv
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory

import cv2
import torch
from PIL import Image
from torchvision import transforms
from torchvision.utils import save_image
import numpy as np
from skimage.measure import label, regionprops
from skimage import morphology, img_as_ubyte
from configparser import ConfigParser
import feret
from datetime import datetime
from pp_config import PPConfig
import make_directories



config_object = ConfigParser()
config_object.read("config.ini") # Read the config.ini file that is generated from pp_config.py



def write_image(original_filename, string_label, image, results_directory):
    """
    Writes an image to a file. The filename is constructed by inserting string_label
    before the extension of original_filename.

    For example: if original_filename is 'image.tif' and string_label is '-label',
    then the filename of the new file will be 'image-label.tif'

    :param original_filename: the name of the image
    :param string_label: the name of the arguments. The string label is '-nn_mask," "-threshold," or "-area_filtered."
    :param image: the wanted image based on the arguments
    :return: the images at the argument checkpoints
    """
    original_path = Path(original_filename) # original_filename is the name of the original picture like 522_1_1.tif
    new_stem = original_path.stem + string_label # take off '.tif' from '522_1_1.tif'
    new_filename = original_path.with_stem(new_stem) # print(new_filename)   output: 522_1_1-nn_mask.tif

    #----------- Add the mask images to their respective directories -------------

    os.chdir(results_directory) # The current working directory is the project directory, so we need to change it to the results directory which is where the images and other subdirectories will be placed.

    if string_label == '-nn_mask': # Check if the image to be created ends with 'nn-mask'
        new_path2 = os.path.join(os.getcwd(), 'nn_masks')
        if(os.path.exists(new_path2)): # chek to see that there is an 'nn_masks' directory in the results folder. This folder would have been made if the checkbox was checked in the gui.
            os.chdir('nn_masks') # Change the working directory to 'nn_masks'
            new_path = os.path.join(results_directory, 'nn_masks', str(new_filename))

            cv2.imwrite(str(new_filename), image) # saves the image to the filepath called new_filename to the current working directory
            os.chdir('../') # move back up to the parent directory (aka the results directory)

    if string_label == '-area_filtered': # Check if the image created ends with '-area_filtered'
        new_path2 = os.path.join(os.getcwd(), 'area_filtered_masks')
        if(os.path.exists(new_path2)): # chek to see that there is an 'nn_masks' directory in the
            os.chdir('area_filtered_masks') # Change the working directory to 'area_filtered_masks'
            new_path = os.path.join(results_directory, 'area_filtered', str(new_filename))
            cv2.imwrite(str(new_filename), image) # saves the image to the filepath called new_filename to the current working directory
            os.chdir('../') # move back up to the parent directory (aka the results directory)

    if string_label == '-threshold': # Check if the image created ends with '-threshold'
        new_path2 = os.path.join(os.getcwd(), 'threshold_masks')
        if(os.path.exists(new_path2)): # chek to see that there is an 'nn_masks' directory in the
            os.chdir('threshold_masks') # Change the working directory to 'threshold_masks'
            new_path = os.path.join(results_directory, 'threshold', str(new_filename))
            cv2.imwrite(str(new_filename), image) # saves the image to the filepath called new_filename to the current working directory
            os.chdir('../') # move back up to the parent directory (aka the results directory)

    os.chdir('../') # move back to the main project directory from the results directory


def process_image(image_filename, args):
    """
    Processes the (image_filename) image to get dimensions of
    areas, lengths, and width in pixels. Writes out a csv file
    with the number of cells and its dimensions

    :param image_filename: the name of the image
    :param args: any arguments that was passed from the user
    to the terminal.

     args is a dictionary that is defined either in main or from the sample_gui.

    """
    input_img = Image.open(image_filename).convert("RGB")
    nn_mask = nn_predict(input_img, args['weights_file'])
    threshold_mask = threshold(nn_mask, args["config"].threshold)
    threshold_mask = erod_dilate(threshold_mask, args["config"].kernel_size)
    area_filtered = area_filter(threshold_mask, args["config"].min_size)

    results_directory = args['results_directory']
    write_dimensions(area_filtered, image_filename, results_directory)
    if args['write_nn_mask']: # With the key, get the dictionary value
        write_image(image_filename, '-nn_mask', nn_mask, results_directory)
    if args["write_threshold_mask"]:
        write_image(image_filename, '-threshold', threshold_mask, results_directory)
    if args["write_area_filtered"]:
        write_image(image_filename, '-area_filtered', area_filtered, results_directory)


def nn_predict(input_img, weights_filename):
    """
    Uses a trained NN model to segment the cells from the image

    :param input_img: the input image
    :param weights_filename: if an argument was passed through to
    specify another weights file to be used, then use it
    :return: an approximation of a mask indicating where the cells are
    """
    model = torch.load(weights_filename)
    model.eval()
    model.to('cpu')

    data_transforms = transforms.Compose([transforms.ToTensor()])
    # transforms in torchvision only work on PIL images?
    input_img = data_transforms(input_img)

    # nn.Conv2d(?) expects a 4-dimensional input tensor as [batch_size, channels, height, width], so unsqueeze is necessary
    input_img = input_img.unsqueeze(0)
    input_img.to('cpu')
    torch.set_grad_enabled(False)
    prediction = model(input_img)
    out = prediction['out'].data.cpu()
    # saves output image in a temporary directory to be later deleted
    with TemporaryDirectory() as temp_dir_path:
        temp_file_path = os.path.join(temp_dir_path, 'output.tif')
        save_image(out, temp_file_path)
        out = cv2.imread(temp_file_path, cv2.IMREAD_GRAYSCALE)
    return out


def threshold(nn_mask, threshold_value):
    """
    Thresholds the NN image

    :param nn_mask: the NN image
    :return: the threshold mask of the NN image
    """

    # turns threshold into white (255)
    th, threshold_mask = cv2.threshold(nn_mask, threshold_value, 255, cv2.THRESH_BINARY)
    return threshold_mask

def erod_dilate(threshold_mask, kernel_size):
    """
    Applies closing, erosion, and dilation morphological changes to the threshold image
    to close any holes, remove noise, and separate groups of cells.

    :param threshold_mask: threshold mask of the NN image
    :return: another threshold mask that have the new morphological changes
    """
    # closing
    kernel = np.ones((kernel_size, kernel_size), np.uint8) # kernel size is the number of pixels around the pixel being examined
    closing = cv2.morphologyEx(
        threshold_mask, cv2.MORPH_CLOSE, kernel, iterations=3)

    # erosion
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    thresh_erosion = cv2.erode(closing, kernel, iterations=3)

    # opening
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    opening = cv2.morphologyEx(
        thresh_erosion, cv2.MORPH_OPEN, kernel, iterations=4)

    # dilation
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    thresh_dilation = cv2.dilate(opening, kernel, iterations=2)

    return thresh_dilation

def area_filter(threshold_mask, min_size):
    """
    Filters out groups of pixels that are below 700 pixels in area.

    :param threshold_mask: threshold mask of the NN image
    :return: the image with the filtered areas
    """
    image = threshold_mask.copy()
    arr = image > 0
    area_filtered = morphology.remove_small_objects(arr, min_size=min_size)
    area_filtered = img_as_ubyte(area_filtered)
    return area_filtered


def write_dimensions(area_filtered, image_filename, results_directory):
    """
    Write the dimensions for the cell dimensions in a csv file. The dimensions are measured
    using scikit-image's regionprops_table function. Area is represented by area_filled,
    Length is represented by maximum feret diameter,
    and Width is represented by minimum feret diameter

    :param area_filtered: the image with the filtered areas
    :param image_filename: the filename of the original image input
    """

    csv_filename = Path(image_filename).with_suffix('.csv') # Get the path of image_filename and add '.csv' to the end
    image = area_filtered.copy()
    label_img = label(image)
    with open(str(Path(results_directory) / csv_filename), 'w') as f:
        writer = csv.writer(f) # returns a writer object that converts f into a delimited string
        writer.writerow(['Number', 'Area', 'Feret', 'MinFeret'])
        for region in regionprops(label_img):
            label_img_copy = label_img.copy()
            label_img_copy[label_img_copy != region.label] = 0

            maxf = feret.max(label_img_copy, edge=True)
            minf = feret.min(label_img_copy, edge=True)
            writer.writerow([region.label, region.area_filled, maxf, minf])

def main():
    """
    Main function with listed arguments that can be passed through
    the terminal
    """
    parser = ArgumentParser()
    parser.add_argument('--write_nn_mask', action='store_true',
                        help='Write the mask images produced by the neural '
                             'network')
    parser.add_argument('--write_threshold_mask', action='store_true',
                        help='Write the result of thresholding')
    parser.add_argument('--write_area_filtered', action='store_true',
                        help='Write the result of area filtering')
    parser.add_argument('--weights_file',
                        help='Specify the path to the weights file')
    parser.add_argument('image_files', nargs='+')
    parser.add_argument('--write_results_directory', nargs='+')
    # cli means command line
    cli_args = parser.parse_args()
    cli_args.write_nn_mask = '--write_nn_mask' #so if '--write_nn_mask' was written on the terminal, write_nn_mask would happen
    cli_args.write_threshold_mask = '--write_threshold_mask'
    cli_args.write_area_filtered = '--write_area_filtered'
    cli_args.get_res_dir = '--write_results_directory'


    if cli_args.weights_file is None:
        cli_args.weights_file = 'weights.pt'

    make_directories.main_for_directories() # make the directories for results, nn_mask, threshold, and area filtered


    global args
    args = { # if command line configurations were given, they are assigned to keys.
        # add " " here
        "results_directory": make_directories.get_results_directory(),
        "weights_file": cli_args.weights_file,
        "write_nn_mask": cli_args.write_nn_mask,
        "write_threshold_mask": cli_args.write_threshold_mask,
        "write_area_filtered": cli_args.write_area_filtered,
        "config": PPConfig(os.getcwd())
    }


    for filename in cli_args.image_files: # for each .tif file
        process_image(filename, args)



if __name__ == "__main__":

    main()
