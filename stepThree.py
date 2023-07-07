# This script handles the Imbalance problem regarding the dataset
# In total we have 3182 cells with the combination explained below:
# 1500 spindle
# 1122 epithelial
# 560 inflammation
# We want the number of each cell to be equal, so we do Data Augmentation with rotating some cell images:
# we rotate 378 (1500-1122) of epithelial cells with degree of 90
# we rotate 560 of inflammation cells with degree of 90 and rotate 380 (150-560-560) with degree of 180.
# we also add these new images to Allcells_N folder with ids starting from 3183

# python3 stepThree.py --cells AllCells_N30/ --json actual.json --fakeJson ActualAndFake.json


# importing necessary libraries
import argparse
import json
import os
import cv2
import imutils


# Parsing the required arguments
ap = argparse.ArgumentParser()
ap.add_argument('-j', "--json", help='Path to the actual json file')
ap.add_argument('-c', "--cells", help='Path to the folder that generated cells will be saved into that')
ap.add_argument('-f', "--fakeJson", help='Path to the actualAndFake json file')
args = vars(ap.parse_args())


def generate_new_cells(cellFolderPath, ActualJsonFilePath):

    # initiating the 'newID' of generated cells and variable related to it's counting
    newID = 3183
    newCellCount = 0

    # reading the actual JSON file and assigning it's data to realCell dictionary
    with open(ActualJsonFilePath, 'r') as file:
        realCell = json.load(file)

        # Initiating the fakeCell dictionary
        fakeCell = {}

    # Looping over items inside realCell dictionary
    for key, value in realCell.items():

        # checking whether the label of the realCell item is our considered label
        if value['label'] == 'epithelial':

            # Looping over cells in the Cell folder
            for cell in os.listdir(cellFolderPath):

                # checking whether the name of cell is the same as our key in actual JSON file
                if str(cell[:-4]) == key:

                    # Reading and rotating the cell with desired degree
                    file_path = os.path.join(cellFolderPath, cell)
                    image = cv2.imread(file_path)
                    rotated = imutils.rotate(image, 90)
                    cell_name = os.path.join(str(cellFolderPath), str(newID)+ '.png')

                    # Adding info of generated cell to the fakeCell dictionary
                    # This info does not contain coordination and the image name is just 'Generated Cell'
                    fakeCell[newID] = {'coordinate': (None, None),'label': value['label'], 'image_name': 'Generated cell'}

                    # Adding 1 to new ID so that the next item uses it
                    newID += 1

                    # Writing and Saving the fake Cell
                    cv2.imwrite(cell_name, rotated)

                    # Adding 1 to newCelCount name
                    newCellCount += 1

                    # Checking if the number of new fake cells have reached to our desired number or not
                if newCellCount == 378:
                    break

    # Returning the fakeCell dictionary
    return fakeCell

def merge_real_and_fake_cells(ActualJsonFilePath, ActualAndFakeJsonFilePath,  fakeCells):

    # Reading actual JSON file
    with open(ActualJsonFilePath, 'r') as file1:
        Cells = json.load(file1)

    # Updating the dictionary with fakeCell dictionary
    Cells.update(fakeCells)

    # Dumbing the New Dictionary to the other JSON file which is ActualAndFake.json
    with open(ActualAndFakeJsonFilePath, 'w') as file2:
        json.dump(Cells, file2, indent=4)


# Calling Functions
fakeCellsDictionary = generate_new_cells(cellFolderPath=args["cells"], ActualJsonFilePath=args["json"])
merge_real_and_fake_cells(ActualJsonFilePath=args["json"], ActualAndFakeJsonFilePath=args["fakeJson"], fakeCells=fakeCellsDictionary)

