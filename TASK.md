In this assignment, you will design an algorithm to cluster cells in various tissue images based on their
handcrafted intensity-based and textural features and correlate the obtained cluster ids with the actual
classes of the cells.
You will work on the cells in the six images provided in nucleus-dataset.zip. This is a small subset of a publicly
available [Dataset](https://warwick.ac.uk/fac/cross_fac/tia/data/hovernet/). For each image, there are two
files in the zip file:

- **#.png:** RGB image file. You will extract the features from its gray-level image equivalent.
- **#_cells:** Text file containing the coordinates of cells in this image together with their actual class labels (either inflammation, epithelial, or spindle). Note that there might be missing cells or
inconsistencies in the cell coordinates or the labels. Please use them as they are, and do not try to
fix them.

# **PART 1: Implementations**

This algorithm relies on representing each cell with a set of handcrafted intensity-based and textural
features, and clustering all cells found in all provided images based on their extracted features.
You will extract these features for each cell separately, considering the patch cropped around this cell. This
patch should be cropped by locating the coordinates of the cell at the center of this patch. (Here it is
important to noting that the first and the second numbers in the file correspond to x and y coordinates,
respectively. However, the x-axis corresponds to columns and the y-axis to rows in an image. Please be
sure that you will crop the patch correctly.)
In this task, you will extract the following two sets of features.
- **1) Intensity-based features.** Extract three of these features: mean, standard deviation, and entropy.
- **2) Co-cooccurrence features.** Extract four of these features: angular second moment, maximum probability, inverse difference
moment, and entropy.


Implement the following four functions using a programming language you will prefer. You may implement
other auxiliary functions, if necessary. All these functions should be your implementations. In other words,
you are NOT allowed to use any built-in library functions to implement these functions. (Of course, you
may use built-in library functions for mathematical operations such as log. You may also use built-in
functions to read an RGB image and convert it to its gray-level equivalent.)

- ***intensityFeat = calculateIntensityFeatures(patch, binNumber)***
This function takes a gray-level patch ***patch*** as an input and extracts three intensity-based
features: average, standard deviation, and entropy. It calculates the average and standard
deviation of the pixels in the gray-level patch. Then, it groups the patch pixels into ***binNumber***
bins, and calculates the entropy on this histogram. Note that you will need to first calculate the
frequencies (probabilities) of the histogram bins and then use them for entropy calculation.

- ***M = calculateCooccurrenceMatrix(patch, binNumber, di, dj)***
This function takes a gray-level patch ***patch*** as an input, groups its pixels into ***binNumber*** bins,
and returns a co-occurrence matrix ***M*** calculated on these grouped pixels for a given distance
***(di, dj)***. See the slides for the notation.
  
- ***accM = calculateAccumulatedCooccurrenceMatrix(patch, binNumber, d)***
This function accumulates co-occurrence matrices calculated for different distances specified by
the parameter ***d*** and returns the accumulated matrix accM. To do so, it calculates eight different
co-occurrence matrices for the following distances (d, 0), (d, d), (0, d) (-d, d), (-d, 0), (-d, -d), (0, -d), (d, -d)
and returns the sum of the calculated matrices. See the slides for the notation.

- ***texturalFeat = calculateCooccurrenceFeatures(accM)***
This function takes an accumulated co-occurrence matrix accM as an input and calculates four
texture features on the normalized matrix (i.e., you will need to first normalize the matrix and then
calculate the features on this normalized matrix). These four features are the angular second
moment, maximum probability, inverse difference moment, and entropy. See the slides for their
definitions.


# **PART 2: Cluster cells**
Repeat it for every cell in every image: Crop a patch with a size of NxN, where N is the window size, and
extract its intensity-based and textural features. The overall feature vector of a cell will be the
concatenation of these features.
Run the k-means algorithm on the extracted features to find clustering vectors. (Run it on the features of
all cells in all images, do NOT run the k-means algorithm for each image separately.) Here you may use a
built-in library function for the k-means clustering algorithm.
Consider the importance of normalizing the features. Try to understand why this
is also important for the k-means clustering algorithm. Also remember the class
imbalance problem (check the total number of inflammatory, epithelial, and spindle-shaped cells in all
images). You may want to take actions to alleviate these problems.

# **PART 3: Experiments**
There are three parameters involved in feature extraction: *binNumber*, *d*, and *N*. The selection of the
proper parameter values is a part of this assignment. For this selection, you may want to observe how
different types of cells look like as well as an approximate cell size in pixels. Then, you are required to
report the results of the following experiments for at least two combinations of these parameters.

**1.** For each cluster, calculate the ratio of inflammatory, epithelial and spindle-shaped cells. Report
these ratios for all clusters in a tabular format, where the rows correspond to clusters and the
columns to the cell types.

**2.** For each image, visualize the clustering results. To do so, illustrate the cells of different clusters in
different colors. Use one color for each cluster; use the same color to visualize the results of all
images.

Provide your quantitative and visual results for **k=3** and **k=5**, separately, as well as for at least two combinations of the parameters. Thus, you will have at least four sets of results. Interpret these
results and briefly explain your conclusions. Additionally, briefly explain how you select the parameter
values. 
