# This script creates cell images from whole images according to json file that has been created in previous step

# python3 stepTwo.py --folder nucleus-dataset/ --json actual.json --cells AllCells_N30/


# importing necessary libraries
import argparse
import json
import os
import cv2
import numpy as np

# Parsing the required arguments
ap = argparse.ArgumentParser()
ap.add_argument('-f', "--folder", help='Path to the folder that contains whole images')
ap.add_argument('-j', "--json", help='Path to the actual json file')
ap.add_argument('-c', "--cells", help='Path to the folder that generated cells will be saved into that')
args = vars(ap.parse_args())


def create_cell_patches(folder_path, json_path, cell_folder, N=30):
    # Reading the JSON file
    with open(json_path, 'r') as file:

        # Assigning the files in the JSON to the 'dataPoint' variable
        dataPoint = json.load(file)

        # Looping over keys and values of dictionary in the items of JSON file which now is in the 'dataPoint'
        for key, value in dataPoint.items():

            # Extracting info in the dictionary to variables
            id = key
            coordinate = value['coordinate']
            image_name = value['image_name']

            # Adding the '.png' to the image name so that it can be comparable with the 'filename' later in the script (Line 43)
            image_name = image_name + '.png'

            # Looping over items in the folder containing our whole images
            for filename in os.listdir(folder_path):

                # check if the filename and the relating image of the cell is the same
                if filename == image_name:

                    # Reading the whole image
                    file_path = os.path.join(folder_path, filename)
                    image = cv2.imread(file_path)

                    # Creating patch with size of N
                    patch = np.zeros((N + 1, N + 1), dtype="uint8")

                    # Cropping the patch from the image according to the coordination available
                    patch = image[int(coordinate[0]) - N // 2: int(coordinate[0]) + N // 2,
                            int(coordinate[1]) - N // 2:int(coordinate[1]) + N // 2]

                    # Creating cell image name with '.png' format
                    cell_name = os.path.join(str(cell_folder), id+'.png' )

                    # Writing and saving each cell
                    cv2.imwrite(cell_name, patch)


create_cell_patches(folder_path=args["folder"], json_path=args["json"], cell_folder=args["cells"])