# Spectral signatures, advanced: the PROSAIL model, index saturation and LAI retrieval

Description of the notebook for the visual [Spectral signatures](https://openskylab.space/edu_viz_spectral_signatures.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/spectral_signatures_pro_en.ipynb) · version 1.0 · about 75 min · five tasks

## What the notebook is about

The advanced version of the spectral signatures notebook. The curves from the visual are computed here by a real radiative transfer model, PROSAIL, which couples leaf optics (PROSPECT) with the canopy (SAIL). You use it to show why NDVI saturates, build a table of simulations and from it estimate LAI for every pixel of two Sentinel-2 images near Roztoky, with its uncertainty and the places where the model fails.

## Goal

Find out which bands carry information on chlorophyll, water, dry matter and LAI, compare the saturation of NDVI, NDRE and CIre in the model, understand why inverting the model is ambiguous, and estimate LAI by inverting a table of simulations while knowing its limits.

## Data

Two Sentinel-2 L2A images of tile 33UVR (14 May and 21 July 2024) from the Earth Search catalogue on AWS, a 4 × 4 km window around Roztoky and Únětice; ESA WorldCover 2021 v200 classes. The simulations are computed by the `prosail` package (PROSPECT-5 and 4SAIL) inside the notebook. About 40 MB is downloaded; the simulation table takes 1 to 3 minutes. No ground LAI measurements exist for the window, so the inversion results are model estimates, not validated values.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup, two images and the model

Installs the libraries Colab lacks (`prosail`, `rasterio`) and downloads the data.

Parameters the student changes:

- `DATES = ["S2A_33UVR_20240514_0_L2A", "S2B_33UVR_20240721_0_L2A"]`: two images of one season (spring, summer)
- `LON, LAT, HALF = 14.375, 50.155, 2000`: window centre and half width (m)

### 2. What the model does

PROSAIL computes canopy reflectance from leaf properties (chlorophyll `cab`, water `cw`, dry matter `cm`, structure `n`) and canopy properties (leaf area index `lai`, mean leaf angle `ala`, the soil below). The spectrum in 1 nm steps is converted to Sentinel-2 bands. The band spectral response is replaced here by a Gaussian, which is an approximation; ESA publishes the exact curves.

Parameters the student changes:

- `VAR, VALUES = "cab", [10, 30, 50, 70]`: variable (cab, cw, cm, lai, ala) and its values

**Task 1.** Run the cell for `cab`, `cw`, `cm`, `lai` and `ala`. From the plots and the sensitivity table, say which Sentinel-2 bands carry information on chlorophyll, leaf water and LAI. Which two variables change the red edge and NIR almost equally but with opposite sign, and what does this mean for estimating LAI from one image?

### 3. Index saturation in the model

We let LAI grow from 0 to 7 for three chlorophyll contents and follow NDVI, NDRE and CIre = NIR/RE1 − 1 (Gitelson et al. 2005). The table shows at what LAI the index reaches 90 % of the difference between bare soil and LAI 7, and how much a change in chlorophyll shifts the index, relative to that difference.

Parameters the student changes:

- `INDICES = {`: indices; add your own, e.g. MTCI

**Task 2.** At what LAI does NDVI saturate, and at what LAI NDRE and CIre? Why do red-edge indices saturate later? What price do they pay for it (last column)? Add your own index to `INDICES`, e.g. MTCI = (B6 − B5)/(B5 − B4), i.e. `(b["rededge2"] - b["rededge1"]) / (b["rededge1"] - b["red"])`, and place it among the others.

### 4. A table of simulations and one pixel

The model cannot run backwards. So we run thousands of simulations with random variable values within given ranges, and for a pixel we look for those whose bands are most similar to the measured ones (smallest RMSE). The ranges are prior knowledge: what we know about the canopy in advance. For each image the table is computed with its solar elevation.

Parameters the student changes:

- `N_LUT = 20000`: number of simulations in the table
- `"lai": (0, 7), "ala": (30, 80), "psoil": (0, 1), "rsoil": (0.5, 1.5)}`: variable ranges (prior knowledge)
- `K = 50`: how many best solutions from the table to keep
- `PLON, PLAT = 14.3516, 50.1632`: point (field near Únětice); try forest 14.366, 50.148

**Task 3.** How wide is the LAI range among the best solutions and how does it relate to leaf angle and chlorophyll (plots on the right)? Compare the coefficient of variation of `lai`, `cab` and their product `ccc` (canopy chlorophyll, µg per cm² of ground). Why is the product better determined than either part? Try `K = 10` and `K = 200` and a forest point.

### 5. LAI map and where the model does not fit

The same procedure for all pixels of the window. For each pixel we get the median LAI of the best solutions, their standard deviation as a measure of uncertainty, and the RMSE of the best simulation as a measure of how well the model explains the pixel at all.

**Task 4.** Where is the RMSE largest and why? Why does water get some LAI although there are no leaves, and why does built-up land fit almost as well as grassland? The forest comes out with LAI around 2, while a synthesis of ground measurements (Asner et al. 2003) gives a mean of 5.1 to 6.7 for temperate evergreen forests. Which assumptions of PROSAIL (one continuous layer of leaves, no trunks, gaps or crown shadows) contribute to the difference?

### 6. LAI, NDVI and uncertainty in real data

Loads the libraries and downloads the data.

**Task 5.** From what NDVI does the LAI uncertainty grow fastest, and how does this relate to the saturation in step 3? How did NDVI and LAI change between May and July on cropland, grassland and in the forest? Why would NDVI alone underestimate the difference between two dense canopies?

**Extension (optional).** Narrow the ranges in `RANGES` to what you know about the canopy (e.g. `ala` 50–65, `cab` 30–60) and run steps 4 to 6 again. How does the LAI uncertainty change? What happens when the prior knowledge is wrong, for example for a forest with a different leaf angle?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.
- Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Jacquemoud, S. et al. (2009). PROSPECT + SAIL models: A review of use for vegetation characterization. *Remote Sensing of Environment* 113, S56–S66. https://doi.org/10.1016/j.rse.2008.01.026
- Feret, J.-B. et al. (2008). PROSPECT-4 and 5: Advances in the leaf optical properties model separating photosynthetic pigments. *Remote Sensing of Environment* 112, 3030–3043. https://doi.org/10.1016/j.rse.2008.02.012
- Verhoef, W., Jia, L., Xiao, Q., Su, Z. (2007). Unified optical-thermal four-stream radiative transfer theory for homogeneous vegetation canopies. *IEEE Transactions on Geoscience and Remote Sensing* 45, 1808–1822. https://doi.org/10.1109/TGRS.2007.895844
- Gómez-Dans, J. *prosail*: Python bindings for PROSPECT and SAIL. https://github.com/jgomezdans/prosail
- Combal, B. et al. (2002). Retrieval of canopy biophysical variables from bidirectional reflectance using prior information to solve the ill-posed inverse problem. *Remote Sensing of Environment* 84, 1–15.
- Gitelson, A. A. et al. (2005). Remote estimation of canopy chlorophyll content in crops. *Geophysical Research Letters* 32, L08403. https://doi.org/10.1029/2005GL022688
- Asner, G. P., Scurlock, J. M. O., Hicke, J. A. (2003). Global synthesis of leaf area index observations: implications for ecological and remote sensing studies. *Global Ecology and Biogeography* 12, 191–205. https://doi.org/10.1046/j.1466-822X.2003.00026.x
- Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
