# This script uses the clusterLabel.json file to visualize the generated labels by KMeans algorithm on whole images

# python3 visualize.py --folder nucleus-dataset/ --json clusterLabel.json

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

# Loading the clusterLabel JSON file
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

                # Checking if the current wholeImage belongs to the current cell in JSON file
                if filename[:-4] == value['wholeImageName']:

                    # Assigning a color to each Label
                    if value['clusterLabel'] == '0':
                        color = (0,0,255)
                    elif value['clusterLabel'] == '1':
                        color = (0, 255, 0)
                    elif value['clusterLabel'] == '2':
                        color = (255, 0, 0)

                    # Drawing circles on the coordination of each cell in the current image
                    cv2.circle(labeledImage, (int(value['coordinate'][1]), int(value['coordinate'][0])), 5,color, -1)

            # Assigning the name of new Labeled of wholeImage with Clusters provided
            filename1 = filename[:-4] + '_clustered.png'

            # Saving and Showing the Image
            cv2.imwrite(filename1, labeledImage)
            cv2.imshow("i", imutils.resize(labeledImage, width=700))
            cv2.waitKey(0)




