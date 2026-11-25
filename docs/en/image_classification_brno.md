# From pixel to class: classifying Sentinel-2 near the Brno reservoir

Description of the notebook for the lab [From pixel to class](https://openskylab.space/edu_viz_image_classification.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/image_classification_brno_en.ipynb) · version 1.0 · about 50 min · six tasks

## What the notebook is about

In the lab you split pixels with an index threshold, compared classic classifiers and watched a neural network overfit. Here you do the same on a real Sentinel-2 image near the Brno reservoir with ESA WorldCover as reference and assess accuracy with a confusion matrix.

## Goal

Find an NDVI and SAVI threshold for vegetation, compare minimum distance, maximum likelihood, k-NN, random forest and a neural network on training and test pixels, and compute producer's and user's accuracy and kappa.

## Data

Sentinel-2 L2A `S2B_33UXQ_20240814_0_L2A` (14 August 2024) from the Earth Search catalogue on AWS, a 4 × 4 km window around the Brno reservoir and Bystrc; reference ESA WorldCover 10 m 2021 v200. About 20 MB is downloaded.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The notebook is stored without outputs; numbers and plots appear when it runs and may differ between runs where the data are updated continuously.

## Step by step

### 1. Setup and data

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

### 2. NDVI threshold: two errors against each other

Vegetation = forest, meadow and field according to WorldCover, the rest = built-up and water. For each threshold we count how much vegetation we miss and how much non-vegetation we label as vegetation.

Parameters the student changes:

- `L = 0.5`: SAVI soil adjustment factor (0 = NDVI, 0.5 usual, 1 sparse vegetation)

**Task 1.** Which NDVI threshold is best and which errors remain? Why can you not get rid of both errors at once? Which “vegetation” pixels have a low NDVI (look at the fields: after harvest there is stubble, in spring the soil may still be bare) and why are they counted as vegetation in WorldCover?

**Task 2.** Compare NDVI and SAVI. Set `L = 0`, `0.25` and `1`. How do the range of values and the best threshold change? Why does SAVI depend less on soil brightness and why does it hardly matter in dense vegetation?

### 3. Training and test pixels

Neighbouring pixels are similar, so a random split would overstate accuracy. We therefore train on the northern half of the window and test on the southern half.

We take **up to `n_train` pixels of each class** in the north for training and up to
2,000 pixels of each class in the south for testing. If fewer suitable pixels exist,
we take all of them. The mask `ok` already restricts the pixels to a suitable SCL class
and to one of the selected WorldCover reference classes.

North and south are two copies of the mask `ok`: in the northern mask we switch off
the bottom half of the rows, in the southern one the top half. The function `sample` then, for each class:

1. Uses the mask to select its pixels in the given half of the image.
2. Builds `class_features`: each row is one pixel, the columns are its
   six spectral features.
3. Picks rows at random with `rng.choice`. `replace=False` means the same
   pixel is never picked twice. `min` limits the requested count to the available pixels.
4. Appends the reference class converted to a number 0–4 in the order of `CLASSES`.

The output `X` is the feature table of the selected pixels and `y` their reference classes.
`np.vstack` stacks the groups of pixels on top of each other. Sampling per class limits
the dominance of abundant classes; the test accuracy therefore does not reflect the natural
areal share of the classes in the whole landscape.

The seed `1` makes the whole selection repeatable. Each call of `sample` advances
the state of the generator. **After changing `n_train`, run this cell and the following
models again.**

### How we will evaluate the classifiers

The function `report` compares the model's prediction on the test pixels with the WorldCover
reference classes. It returns the confusion matrix with producer's (PA) and
user's (UA) accuracy and prints the overall accuracy on the test and training pixels and the kappa coefficient.
We use the same function for all models below.

Parameters the student changes:

- `n_train = 300`: at most this many training pixels per class

### 4. Minimum distance and maximum likelihood

Loads the libraries and downloads the data.

**Task 3.** Read the maximum likelihood confusion matrix: rows are the reference, columns the result. Which class has a low producer's accuracy (PA, it is missed) and which a low user's accuracy (UA, other classes fall into it)? Which pairs of classes are confused most and why? Which of the two methods did better? Maximum likelihood accounts for the spread and correlation of bands within each class; why might it still not win (classes are not normally distributed, meadow and forest have similar spectra, the reference has errors)?

### 5. How complex a model? k-NN and random forest

Loads the libraries and downloads the data.

**Task 4.** With k = 1 the accuracy on training pixels is 100 % or nearly so. Why does that mean nothing? Which k and which tree depth give the best test accuracy? Describe what overfitting and underfitting look like in both plots.

### 6. A neural network and overfitting

A small network with one hidden layer. We train it on few pixels and watch training and test accuracy over the epochs.

Parameters the student changes:

- `hidden = 64`: number of hidden neurons
- `n_small = 30`: at most this many training pixels per class

**Task 5.** Try `hidden` 4, 64 and 256 and `n_small` 30 and 300. When does the network overfit (training rises, test falls or stalls)? What would help: more data, a smaller network or stopping earlier? Why is the training–test gap larger for the network than for maximum likelihood?

### 7. Result map

For the final map we use `forest`: a random forest with **200 trees and a maximum
depth of 12**. Its settings are fixed here in advance; the code does not automatically pick
the best model from the comparison above. After training we show its confusion
matrix with the same `report` function.

The classifier expects one pixel per row, so we turn the input image into a
feature table and the prediction `pred` back into a map. Converting to `float`
lets us mark hidden pixels with `NaN`.

The mask `visible_pixels` keeps the SCL classes **4 = vegetation, 5 = not vegetated
surfaces, 6 = water**. `~visible_pixels` selects all other pixels, for example
clouds, shadows or snow; setting them to `NaN` hides them in the map. This is a display
mask: unlike the training mask `ok`, it does not require a selected WorldCover
class.

The WorldCover 2021 reference stays on the left, the prediction from Sentinel-2 2024 on the right.
The white line in the right map marks the split into the training north and the test south.

**Task 6.** Find places where the map differs from WorldCover. Is the error always in the classification? Consider that WorldCover is from 2021 and has errors of its own, that a single image from one day cannot tell a meadow from a field of forage crops, nor green spring cereals from grass, and that a 10 m pixel at a forest edge is a mixture. How would you assess accuracy honestly?

**Extension (optional).** Compare your results with a classmate who has the notebook for another place (Roztoky, Brno, Hluboká nad Vltavou). Which classes are confused more elsewhere, and why (season of the image, type of landscape, field size)?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.
- Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Huete, A. R. (1988). A soil-adjusted vegetation index (SAVI). *Remote Sensing of Environment* 25, 295–309. https://doi.org/10.1016/0034-4257(88)90106-X
- Congalton, R. G., Green, K. (2019). *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices*, 3rd ed. CRC Press.
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
