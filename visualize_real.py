# This script uses the actual30.json file to visualize the actual labels provided

# python3 visualize_real.py --folder nucleus-dataset/ --json actual.json

# importing necessary libraries
import json
import os
import cv2
import argparse
import imutils

# Parsing the required arguments
ap = argparse.ArgumentParser()
ap.add_argument('-f', "--folder", type=str, help='Path to the folder of whole images')
ap.add_argument('-j', "--json", type=str, help='Path to the json file of cluser labels')
args = vars(ap.parse_args())

# Loading folder path of whole images
folder_path = args["folder"]

# Loading the actual JSON file
with open(args["json"], 'r') as file:
    clusterDict = json.load(file)

color = ()

# Looping over folder items
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    labeledImage = cv2.imread(file_path)
    if os.path.isfile(file_path):
        # choosing only files with .png format
        if filename.endswith('.png'):

            # Looping over JSON file
            for key, value in clusterDict.items():

                # Selecting only actual cell images from actual.json file NOT generated files
                if int(key) < 3183:

                    # Checking if the current wholeImage belongs to the current cell in JSON file
                    if filename[:-4] == value['image_name']:

                        # Assigning a color to each Label
                        if value['label'] == 'inflammation':
                            color = (0,0,255)
                        elif value['label'] == 'epithelial':
                            color = (0, 255, 0)
                        elif value['label'] == 'spindle':
                            color = (255, 0, 0)

                        # Drawing circles on the coordination of each cell in the current image
                        cv2.circle(labeledImage, (int(value['coordinate'][1]), int(value['coordinate'][0])), 5,color, -1)

            # Assigning the name of actual Labeled of wholeImage
            filename1 = filename[:-4] + '_real.png'

            # Saving and Showing the Image
            cv2.imwrite(filename1, labeledImage)
            cv2.imshow("i", imutils.resize(labeledImage, width=700))
            cv2.waitKey(0)




