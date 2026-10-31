# From pixel to class: classifying Sentinel-2 near Hluboká nad Vltavou

Description of the notebook for the visual [From pixel to class](https://openskylab.space/edu_viz_image_classification.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/image_classification_hluboka_en.ipynb) · version 1.0 · about 50 min · six tasks

## What the notebook is about

In the visual you split pixels with an index threshold, compared classic classifiers and watched a neural network overfit. Here you do the same on a real Sentinel-2 image near Hluboká nad Vltavou with ESA WorldCover as reference and assess accuracy with a confusion matrix.

## Goal

Find an NDVI and SAVI threshold for vegetation, compare minimum distance, maximum likelihood, k-NN, random forest and a neural network on training and test pixels, and compute producer's and user's accuracy and kappa.

## Data

Sentinel-2 L2A `S2B_33UVQ_20230528_0_L2A` (28 May 2023) from the Earth Search catalogue on AWS, a 4 × 4 km window around Hluboká nad Vltavou and its fishponds; reference ESA WorldCover 10 m 2021 v200. About 20 MB is downloaded.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

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

Parameters the student changes:

- `n_train = 300`: number of training pixels per class

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
- `n_small = 30`: training pixels per class (a small sample overfits more easily)

**Task 5.** Try `hidden` 4, 64 and 256 and `n_small` 30 and 300. When does the network overfit (training rises, test falls or stalls)? What would help: more data, a smaller network or stopping earlier? Why is the training–test gap larger for the network than for maximum likelihood?

### 7. Result map

Loads the libraries and downloads the data.

**Task 6.** Find places where the map differs from WorldCover. Is the error always in the classification? Consider that WorldCover is from 2021 and has errors of its own, that a single image from one day cannot tell a meadow from a field of forage crops, nor green spring cereals from grass, and that a 10 m pixel at a forest edge is a mixture. How would you assess accuracy honestly?

**Extension (optional).** Compare your results with a classmate who has the notebook for another place (Roztoky, Brno, Hluboká nad Vltavou). Which classes are confused more elsewhere, and why (season of the image, type of landscape, field size)?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Copernicus Sentinel-2 data 2023, ESA (L2A, Sen2Cor); AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.
- Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Huete, A. R. (1988). A soil-adjusted vegetation index (SAVI). *Remote Sensing of Environment* 25, 295–309. https://doi.org/10.1016/0034-4257(88)90106-X
- Congalton, R. G., Green, K. (2019). *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices*, 3rd ed. CRC Press.
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
