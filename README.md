# CellCluster-FeaturesExtraction
Cell clustering of tissue images using handcrafted intensity-based and textural features.

### Introduction:
This report focuses on designing an algorithm for clustering cells in tissue images based on their handcrafted intensity-based and textural features. The algorithm's performance is evaluated by correlating the obtained cluster IDs with the actual classes of the cells in a subset of a publicly available dataset. The dataset contains images and corresponding text files with cell coordinates or labels. Aiming to do so, we used Scikit-learn, OpenCV, and Matplotlib libraries in Python programming language to process the images. For each part of assignment, there are different steps followed for clustering the cells at the end. We will explain them in following sections.

# <p align="center"> **Part 1**

This part focuses on extracting handcrafted intensity-based and textural features for each cell in the provided tissue images. We implemented an algorithm that reads the image file and coordinates from the text file, and based on the cell's class label (spindle, epithelial, or inflammation), assigns a corresponding color and directory. A patch is then cropped around each cell by centering it at the given coordinates. The patch size is determined by the variable N which is equal to 30*30 and 40*40 in our algorithm. The extracted patches are saved in separate directories based on their class labels. Then we combine and shuffle all patches in a single folder. Also, the implementation ensures that the patch is correctly cropped by considering the coordinates' correspondence to the x and y axes in the image. The resulting code efficiently processes the cells and saves them as individual patches for subsequent feature extraction and clustering analysis. Figure 1 shows some samples of the patched images.

<p align="center">
  <img src="https://github.com/AmirTabatabaei-git/CellCluster-FeaturesExtraction/assets/132440248/d5cdb7cd-b784-43e0-9220-b9790e97b2aa" width="600" height="100">
</p> 
<p align="center">Figure 1. samples of extracted patches

After patching the cell images, we implemented several functions to extract intensity-based and co-occurrence features from the gray-level image patches. The implemented functions are as follows:

- **calculateIntensityFeatures(patch, binNumber):** This function takes a gray-level patch as input and extracts three intensity-based features: mean, standard deviation, and entropy. The mean and standard deviation are calculated directly from the pixel values in the patch. To calculate the entropy, a histogram is constructed by grouping the patch pixels into binNumber bins. The probabilities of the histogram bins are calculated, and the entropy is computed using the probability values.
  
- **calculateCooccurrenceMatrix(patch, binNumber, di, dj):** This function takes a gray-level patch as input and computes a co-occurrence matrix for a given distance (di, dj). The patch pixels are grouped into binNumber bins, and the matrix is initialized with zeros. The function then iterates over the patch, considering each pixel and its neighboring pixel based on the given distance. The corresponding bin indices of the current pixel and its neighbor are determined, and the co-occurrence count in the matrix is incremented accordingly.
  
- **calculateAccumulatedCooccurrenceMatrix(patch, binNumber, d):** This function accumulates co-occurrence matrices calculated for different distances specified by the parameter d. It iterates over eight different distances, including (d, 0), (d, d), (0, d), (-d, d), (-d, 0), (-d, -d), (0, -d), and (d, -d). For each distance, the function calls the calculateCooccurrenceMatrix function to obtain the co-occurrence matrix and accumulates them to create an accumulated matrix.
  
- **calculateCooccurrenceFeatures(accM):** This function takes the accumulated co-occurrence matrix as input and calculates four texture features: angular second moment, maximum probability, inverse difference moment, and entropy. Firstly, the matrix is normalized by dividing it by its norm. Then, the angular second moment is computed by summing the squared values of the normalized matrix. The maximum probability is determined by finding the highest value in the normalized matrix. The inverse difference moment is calculated by summing the normalized matrix divided by ***(1 + (number of rows - number of columns) ^2)***. Finally, the entropy is computed by multiplying the normalized matrix with its logarithm and summing the resulting values.

By implementing these functions, we have the necessary tools to extract both intensity-based and co-occurrence features from the image patches. These features will be essential for subsequent steps in the algorithm, including clustering and correlation analysis between the obtained cluster IDs and the actual cell classes.

# <p align="center"> **Part 2**

In this part of the assignment, we focus on clustering the cells based on their extracted intensity-based and textural features. The process involves cropping patches of size NxN around each cell in every image, where N represents the window size. We extract the intensity-based and textural features from each patch, resulting in a feature vector for each cell. The feature vector is obtained by concatenating the intensity-based and textural features together. 
To perform the clustering, we utilize the k-means algorithm. The extracted features from all cells in all images are used as input for the k-means algorithm, allowing us to find the clustering vectors. The built-in library function for the k-means algorithm is employed for this task. It is crucial to normalize the features before applying the k-means algorithm. Normalization ensures that all features are on a similar scale, preventing any particular feature from dominating the clustering process. By normalizing the features, we treat each feature equally in the clustering algorithm.
Additionally, we need to address the issue of class imbalance. It is important to consider the total number of inflammatory, epithelial, and spindle-shaped cells across all images. If there is a significant class imbalance, certain cell types may dominate the clustering results. To alleviate this problem, we tried oversampling techniques with generating the fake images for each group by performing 90-degree rotation to each patch of the image to balance the classes and ensure a more equitable representation of cell types in the clustering process.

# Code interpretation:

The provided code can be implemented by the below steps:

- ### stepOne.py script:
This script generates a JSON file that contains information about cells in images. It expects a folder path as a command-line argument. The script reads each text file in the specified folder, where each file represents an image. Each line in the text file represents a cell in the image.
For each cell, the script extracts the X-coordinate, Y-coordinate, and label. It creates a dictionary for each cell containing these values, along with the image name. The cell dictionaries are then stored in a larger dictionary, where the cell IDs act as keys.
Finally, the script writes the resulting dictionary to a JSON file named 'actual.json' with proper indentation. The JSON file will have the cell IDs as keys and the corresponding cell information (coordinates, label, and image name) as values.

- ### stepTwo.py script:
This script takes a folder containing whole images, a JSON file that contains information about cells in those images, and a folder path to save the generated cell images. It reads the JSON file, extracts the coordinates and other details of each cell, and locates the corresponding whole image. It then crops a patch around each cell's coordinates from the whole image, and saves it as a separate cell image in the specified cell folder. The script essentially generates individual cell images from the larger whole images based on the provided cell information.

- ### stepThree.py script:
This script handles the imbalance problem in a dataset containing cell images. The dataset initially consists of 3182 cells, with the following distribution:

-	1500 spindle cells
-	1122 epithelial cells
-	560 inflammation cells

The goal is to balance the number of each cell type. To achieve this, the script performs data augmentation by rotating some of the cell images. Here is the augmentation strategy:

-	Rotate 378 (1500 - 1122) epithelial cells by 90 degrees.
-	Rotate 560 inflammation cells by 90 degrees.
-	Rotate 380 (1500 - 560 - 560) inflammation cells by 180 degrees.

The script also saves these new images to the cell folder with IDs starting from 3183. The augmented cells are then added to a new JSON file that combines the information from the original JSON file and the generated fake cells.

- ### featureExtraction.py script:
All above steps iterating over each image and cell. It extracts the intensity-based and textural features for each cell's patch and concatenates them into a feature vector. These feature vectors are then used as input for the k-means algorithm. The resulting cluster labels and centroids are obtained, allowing for further analysis and interpretation of the clustering results. Additionally, the script generates a JSON file called ***“clusterLabel.json”***, which contains the cell labels, clustered labels, coordinates, and names of the whole images. This JSON file can be used for visualization purposes, allowing for the visualization of the clustered cells with their respective labels and positions in the original images.

- ### Visualize.py script:
This script is for visualizing the clustered labels on each image. 

- ### Visualize_real.py script:
This script is for visualizing the true labels on images. (Ground truth)

# <p align="center"> **Part 3**

By following above steps and using the k-means algorithm on the extracted features, we can effectively cluster the cells based on their characteristics. Table 1 shows the results related to each combination of parameters. 

Labels map: 
> **Inflammatory => I,
> Epithelial => E,
> Spindle => S**

Parameters map: 
> **K => total number of clusters, N => patch size, d => co-occurrence distance, b => bin Number**

<p align="center">
  <img src="https://github.com/AmirTabatabaei-git/CellCluster-FeaturesExtraction/assets/132440248/ca70bc81-1db7-40a4-af60-d003d813c5cd">
<p align="center">
  <img src="https://github.com/AmirTabatabaei-git/CellCluster-FeaturesExtraction/assets/132440248/980a8010-6c2e-405a-ae11-014152c32b8f">
<p align="center"> Table 1. samples of extracted patches

We used two combinations for each K, N, d, and b. 
**K=(3 & 5) | N=(30 & 40) | d=(1 & 2) | b=(4 & 10)**

As results show, for k=3 we have higher true clustering ratios in comparison with k=5. This approves that we have three groups and labels to be clustered. Also, for N parameter, we did trial and error for several times to find the ideal patch size for our cells. N=30 & 40 were efficiently fitted to all cells. Also, since there are some cell coordinates close to the borders of the images, the largest size of N that we could assign without removing the cells was 40, which can cover the whole cell. Results show a very small differences between two N. 

On the other hand, as can be seen from the results, by increasing the binNumber, the clustering algorithm can better distinguish between clusters, leading to a higher percentage of data points being correctly assigned to their true clusters. Also, since we increased the d by one unit, there is no significant change appeared in our results. This shows that the small changes in co-occurrence distance does not have a strong influence on the clustering outcome.

For each image, we visualized the clustering results for the following combination.
**K=3, N=30, d=2, b=10**

We used one color for each cluster and the same color to visualize the results of all images. Table 2 shows the images marked with real labels in the first column and images marked with the clustered labels in the second column.

![Untitledjb](https://github.com/AmirTabatabaei-git/CellCluster-FeaturesExtraction/assets/132440248/a90164a4-6ee6-4b84-ad2c-6afe1fd77ba0)
![Untitledghj](https://github.com/AmirTabatabaei-git/CellCluster-FeaturesExtraction/assets/132440248/c41285b7-0a78-4c00-9bee-6795aabc37fa)
![Untivvtled](https://github.com/AmirTabatabaei-git/CellCluster-FeaturesExtraction/assets/132440248/2fc3853e-e05a-42aa-8bdf-d86a8af406e1)
![Untitcvled](https://github.com/AmirTabatabaei-git/CellCluster-FeaturesExtraction/assets/132440248/f4af5c0e-33c3-4380-b676-32bc84411e42)
![Untvvvcitled](https://github.com/AmirTabatabaei-git/CellCluster-FeaturesExtraction/assets/132440248/75a3c611-4552-44d1-9027-222766fe5d5c)
![Unticscstled](https://github.com/AmirTabatabaei-git/CellCluster-FeaturesExtraction/assets/132440248/fadb1fcd-998e-430d-b1fe-fc847e09ec42)
<p align="center"> Table 2. visualization of the clustering results.

As you can see, using the k-means algorithm on the extracted features, we can effectively cluster the cells based on their characteristics by a reasonable accuracy. However, using some other preprocessing algorithms prior to clustering might be effective in increasing the accuracy of our algorithm. 



