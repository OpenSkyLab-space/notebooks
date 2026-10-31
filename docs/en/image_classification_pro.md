# From pixel to class, advanced: time series, spatial validation and area estimates

Description of the notebook for the visual [From pixel to class](https://openskylab.space/edu_viz_image_classification.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/image_classification_pro_en.ipynb) · version 1.0 · about 75 min · five tasks

## What the notebook is about

The advanced version of the classification notebook. Instead of one image you work with three Sentinel-2 images from spring, summer and autumn 2024 near Roztoky, write the minimum distance classifier yourself, check accuracy with spatial validation and estimate class areas with their uncertainty, as is done in practice. Part of the code you write yourself.

## Goal

Build features from a time series, write and check your own classifier, compare random and spatial validation, measure what each image adds, and estimate class areas with a confidence interval following good practice (Olofsson et al. 2014).

## Data

Three Sentinel-2 L2A images of tile 33UVR (27 April, 21 July and 21 September 2024) from the Earth Search catalogue on AWS, a 4 × 4 km window around Roztoky and Suchdol; reference ESA WorldCover 10 m 2021 v200. About 60 MB is downloaded.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and three images

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

Parameters the student changes:

- `DATES = ["S2A_33UVR_20240427_0_L2A", "S2B_33UVR_20240721_0_L2A", "S2A_33UVR_20240921_0_L2A"]`: images of one year (spring, summer, autumn)
- `LON, LAT, HALF = 14.37, 50.14, 2000`: window centre and half width (m)

### 2. Features from a time series

From every image we take the reflectance of ten bands and three indices: NDVI (greenness), NDWI (water, McFeeters 1996) and NDMI (leaf moisture). With three images every pixel has 39 features. The indices are functions in the `INDICES` dictionary, and you can add your own.

Parameters the student changes:

- `INDICES = {`: indices computed from every image; add your own

**Task 1.** How does the median NDVI of grassland and cropland change between April, July and September, and why (sowing, harvest, mowing)? Why are several images better than one for telling cropland from grassland? Add your own index to `INDICES`, for example NDRE = (nir − rededge1) / (nir + rededge1), run the cells again and watch in step 5 whether it helped.

### 3. Your own minimum distance classifier

The minimum distance classifier assigns a pixel to the class whose centre (mean feature vector) is nearest. We write it in a few lines of numpy and check that it gives the same as `NearestCentroid` from scikit-learn. We train on the northern half of the window and test on the southern half. You write the branch for the Mahalanobis distance, which takes the spread and correlation of features within a class into account, yourself.

Parameters the student changes:

- `n_class = 600`: sample of pixels per class
- `metric = "euclid"`: "euclid", or "mahalanobis" once you have written it

**Task 2.** Write the `mahalanobis` branch in `min_distance` (covariance matrix of each class from the training pixels, `np.linalg.inv`, distance (x − μ)ᵀ Σ⁻¹ (x − μ)) and set `metric = "mahalanobis"`. How does the result compare with the Euclidean distance and with QDA? QDA is maximum likelihood: why does it still differ from your Mahalanobis distance (the ln |Σ| term and the prior probabilities)? Why is standardisation needed for the Euclidean distance? Try switching it off (`Xs = X`).

### 4. Random or spatial validation?

Neighbouring pixels are similar. If we split the sample into training and test pixels at random, a test pixel often has a neighbour in training and the accuracy comes out too good. Spatial validation splits the sample by squares: a whole square is either in training or in testing (Roberts et al. 2017). We compare a random split, squares, and a north–south split.

Parameters the student changes:

- `BLOCK_M = 500`: size of the squares for spatial validation (m)

**Task 3.** Why does the random split come out best and the north × south split worst? Set `BLOCK_M` to 200 and 1000 m: how do the mean and spread of accuracy change and why? Which number would you trust if the map were to be used in a neighbouring area, and which would you report?

### 5. What each image adds

The course over time separates classes that look alike at one moment. We compute the accuracy of a random forest (spatial validation by squares) for each image alone, for pairs and for all three, and the F1 score of each class for the summer image and for all three.

**Task 4.** Which single image is best, and which pair? How much did all three images help, and for which class most? Explain it with the NDVI plot from step 2. When would another image no longer help, and what would help more then (other features, a better reference, more training pixels)?

### 6. A map and area estimates with uncertainty

A class area counted from the map (number of pixels times pixel area) carries the classification errors. Good practice (Olofsson et al. 2014) is to estimate the area from a random sample of check pixels drawn separately in each map class (stratified sampling) and to report a confidence interval. We make the map from half of the squares and estimate areas on the rest of the area. The reference here is WorldCover, which we have for every pixel, so we can compare the estimate with the true total.

Parameters the student changes:

- `n_h = 100`: sample of check pixels in each map class

**Task 5.** Which classes does the map overestimate and which does it underestimate? Is the WorldCover total closer to the map area or to the sample estimate, and does it fall inside the ±95 % interval? Set `n_h` to 30 and 300: how does the interval change and why? In practice you do not have a reference for every pixel: why is the map area not enough then? And why is not even WorldCover the “truth” (its overall accuracy is about 77 %, Zanaga et al. 2022)?

**Extension (optional).** Try another place: find three cloud-free images of one year (spring, summer, autumn) in the Earth Search catalogue, change `DATES`, `LON` and `LAT`, and the WorldCover tile in the `WORLDCOVER` variable according to the location (3 × 3° tiles, e.g. N48E015 for Moravia). Do the conclusions of steps 4 to 6 hold?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.
- Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015
- Roberts, D. R. et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40, 913–929. https://doi.org/10.1111/ecog.02881
- Congalton, R. G., Green, K. (2019). *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices*, 3rd ed. CRC Press.
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
