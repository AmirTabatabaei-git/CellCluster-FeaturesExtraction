# This script generates a json file that the keys are the id's and the values are coordinates, labels and regarding image
# of each cell

# python3 stepOne.py --folder nucleus-dataset


# importing necessary libraries
import argparse
import json
import os

# Parsing the required arguments
ap = argparse.ArgumentParser()
ap.add_argument('-f', "--folder", type=str, help='Path to the folder')
args = vars(ap.parse_args())



def create_json_of_actual(folder_path):
    # initiating the variables
    data = {}
    ID = 1

    # Looping over items in the folder that contains our files including whole images and text files
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):

            # choosing only files with .txt format
            if filename.endswith('.txt'):

                # accessing to the text file
                with open(file_path, 'r') as file:

                    # reading the lines in the text files
                    for line in (file):

                        # splitting info existing in each line
                        cell = line.split()
                        print(ID, cell, str(filename)[:-4])

                        # assigning coordination and labels to the related variables
                        m, n, label = cell[1], cell[0], cell[2]

                        # creating the 'value' of json file
                        coordinates = {'coordinate': (m, n), 'label': label, 'image_name': str(filename)[:-4]}

                        # assigning the created 'value' to a specific ID as the 'key'
                        data[ID] = coordinates

                        # dumping the information to the JSON file
                        with open('actual.json', 'w') as file1:
                            json.dump(data, file1, indent=4)
                        ID += 1

create_json_of_actual(args["folder"])


