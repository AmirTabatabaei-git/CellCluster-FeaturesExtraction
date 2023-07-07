# This script does the following tasks:
# Extracting features from cell images with the hyperparameters
# Creating required feature vector
# Doing the KMeans clustering
# Generating the parameters required to fill the table that exists in the report
# Generates a JSON file containing cell labels and clustered labels as well as coordinates and whole image names
#       which will be used later to visualize (clusterLabel.json)

# python3 featureExtraction.py --cellfolder AllCells_N30 --json ActualAndFake.json


# importing necessary libraries
import json
import numpy as np
import cv2
import argparse
import glob
import os
from sklearn.cluster import KMeans


# Parsing the required arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cellfolder")
ap.add_argument("-j", "--json")
args = vars(ap.parse_args())

# Creating some variables
cellfolder_path = args["cellfolder"]
image_files = glob.glob(cellfolder_path + '/*')
ActualJsonFile = args["json"]

# Calculate Intensity matrix
def calculateIntensityFeatures(patch, binNumber):
    # Calculate mean and standard deviation
    mean = np.mean(patch)
    std = np.std(patch)

    # Calculate histogram
    hist, bin_edges = np.histogram(patch, bins=binNumber, range=(0,255))

    # Calculate entropy
    entropy = -np.sum(hist * np.log2(hist + np.finfo(float).eps))

    # Return features
    intensityFeat = [mean, std, entropy]
    return intensityFeat

# Calculate co-occurrence matrix
def calculateCooccurrenceMatrix(patch, binNumber, di, dj):

    # Calculate co-occurrence matrix
    normalized_patch = (patch / np.max(patch)) * (binNumber - 1)
    rounded_patch = np.round(normalized_patch).astype(int)
    M = np.zeros((binNumber, binNumber), dtype=int)

    # Creating co-occurrence matrix
    for i in range(len(patch[0]) - abs(di)):
        for j in range(len(patch[1]) - abs(dj)):

            # Get the bin indices of the current pixel and its neighbor
            current_pixel = rounded_patch[i, j]
            neighbor_pixel = rounded_patch[i + di, j + dj]

            # Increment the co-occurrence count in the matrix
            M[current_pixel, neighbor_pixel] += 1
    return M

# Accumulate co-occurrence matrices
def calculateAccumulatedCooccurrenceMatrix(patch, binNumber, d):

    # Calculate accumulated co-occurrence matrix
    accM = np.zeros((binNumber, binNumber), dtype="int")
    distances = [(d, 0), (d, d), (0, d), (-d, d), (-d, 0), (-d, -d), (0, -d), (d, -d)]
    for distance in distances:
        di = distance[0]
        dj = distance[1]
        M = calculateCooccurrenceMatrix(patch, binNumber, di, dj)
        accM += M
    return accM

# Calculate co-occurrence features
def calculateCooccurrenceFeatures(accM):

    # Normalize matrix
    norm = np.linalg.norm(accM)
    accM_norm = accM / norm
    asm = np.sum(accM_norm**2)
    max_prob = np.max(accM_norm)
    idm = np.sum(accM_norm / (1 + (accM_norm.shape[0] - accM_norm.shape[1])**2))
    entropy = -np.sum(accM_norm * np.log2(accM_norm + np.finfo(float).eps))

    # Return features
    texturalFeat = [asm, max_prob, idm, entropy]
    return texturalFeat

# Initiating features and image names list
features = []
image_names = []

# Defining the Hyperparameters
binNumber = 10
d = 2

# Loop over each image
for images in image_files:

    # Extract the image name
    image_name = os.path.split(images)[-1]

    # appent this name to the image_names list
    image_names.append(image_name)
    # Reading image
    image = cv2.imread(images)

    # Converting the image to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Applying a preprocessing stage which is Contrast Limited Adaptive Histogram Equalization (CLAHE)
    CLAHE = cv2.createCLAHE(clipLimit=15, tileGridSize=(30, 30))
    CLAHE = CLAHE.apply(gray)

    # Calculating the accm Matrix for image with desired binNumber and d
    accM = calculateAccumulatedCooccurrenceMatrix(CLAHE, binNumber=binNumber, d=d)

    # Extracting Textural Features
    TexturalFeatures = np.array(calculateCooccurrenceFeatures(accM))
    TexturalFeatures = np.reshape(TexturalFeatures, (1, 4))

    # Extracting Intensity Features
    IntensityFeatures = np.array(calculateIntensityFeatures(gray, 4))
    IntensityFeatures = np.reshape(IntensityFeatures, (1, 3))

    # Concatinating Textural and Intensity Features
    concat = np.concatenate((TexturalFeatures, IntensityFeatures), axis=1)[0]

    # Appending the concatination matrix to the feature matrix
    features.append(concat)

# Converting the feature matrix to Numpy Array
features = np.array(features)

# Find the minimum and maximum values for each feature
min_vals = np.min(features, axis=0)
max_vals = np.max(features, axis=0)

# Normalize the features
normalized_features = (features - min_vals) / (max_vals - min_vals)

# Applying KMeans Clustering
k = 3
kmeans = KMeans(n_clusters=k, random_state=42)
labels = kmeans.fit_predict(normalized_features)

# Reading the JSON file
with open(ActualJsonFile, 'r') as file:
    ActualLabelFile = json.load(file)


cluster = {}
# Initiating the parameters needed for Tables
S0, S1, S2, S3, S4, E0, E1, E2, E3, E4, I0, I1, I2, I3, I4 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

# Loop over image names and labels determined by KMeans clustering:
for image_name, clusterLabel in zip(image_names, labels):
    image_name = image_name[:-4]

    # to count properties only for real images, this line of code only is performed on images with id's lower than
    # 3183. because the ID's greater than 3182 belong to the fake cell images
    if int(image_name) < 3183:
        for key, value in ActualLabelFile.items():
            if key == str(image_name):

                # generating the clusterLabel dictionary
                cluster[image_name] = {'clusterLabel': str(clusterLabel), 'coordinate':value['coordinate'], 'wholeImageName':value['image_name']}
                ####

                if value['label'] == 'epithelial' and clusterLabel == 0:
                    E0 += 1
                elif value['label'] == 'epithelial' and clusterLabel == 1:
                    E1 += 1
                elif value['label'] == 'epithelial' and clusterLabel == 2:
                    E2 += 1
                elif value['label'] == 'epithelial' and clusterLabel == 3:
                    E3 += 1
                elif value['label'] == 'epithelial' and clusterLabel == 4:
                    E4 += 1
                elif value['label'] == 'inflammation' and clusterLabel == 0:
                    I0 += 1
                elif value['label'] == 'inflammation' and clusterLabel == 1:
                    I1 += 1
                elif value['label'] == 'inflammation' and clusterLabel == 2:
                    I2 += 1
                elif value['label'] == 'inflammation' and clusterLabel == 3:
                    I3 += 1
                elif value['label'] == 'inflammation' and clusterLabel == 4:
                    I4 += 1
                elif value['label'] == 'spindle' and clusterLabel == 0:
                    S0 += 1
                elif value['label'] == 'spindle' and clusterLabel == 1:
                    S1 += 1
                elif value['label'] == 'spindle' and clusterLabel == 2:
                    S2 += 1
                elif value['label'] == 'spindle' and clusterLabel == 3:
                    S3 += 1
                elif value['label'] == 'spindle' and clusterLabel == 4:
                    S4 += 1

print("K = {}, N = 30, binNumber = {}, d = {}".format(k, binNumber, d))
print("E0:{} -- E1:{} -- E2:{} -- E3:{} -- E4:{} -- I0:{} -- I1:{} -- I2:{} -- I3:{} -- "
      "I4:{} -- S0:{} -- S1:{} -- S2:{}-- S3:{} -- S4:{}".format(E0, E1, E2, E3, E4, I0, I1, I2, I3, I4, S0, S1, S2, S3, S4))

with open('clusterLabel.json', 'w') as fileCluster:
    json.dump(cluster, fileCluster, indent=4)
##################################################
