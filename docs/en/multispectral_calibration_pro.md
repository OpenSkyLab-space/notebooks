# Calibrating a multispectral camera, advanced: band geometry, NDVI errors, thermal and panchromatic bands

Description of the notebook for the visual [Calibrating a multispectral camera](https://openskylab.space/edu_viz_multispectral_calibration.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/multispectral_calibration_pro_en.ipynb) · version 1.0 · about 60 min · five tasks

## What the notebook is about

The advanced version of the multispectral calibration notebook. The MicaSense Altum-PT camera has seven separate lenses: five multispectral, one panchromatic and one thermal. On a real flight image you find out how the bands shift, rotate and differ in scale against each other and what this does to NDVI, how a calibration error in one band propagates into indices, how surface temperature relates to vegetation, and what sharpening with the panchromatic band can and cannot do.

## Goal

Measure the parallax between bands and from it the camera's distance from the panel, register the bands with an affine transform and compare it with the rig metadata, derive the sensitivity of NDVI to a calibration error, move NDVI onto the thermal grid and compare it with surface temperature, and sharpen the bands with the panchromatic image.

## Data

Two captures (all 7 bands) from a MicaSense Altum-PT camera with DLS 2 from the MicaSense sample data (repository micasense/imageprocessing, MIT licence): IMG_0000 (RP06 panel, 15 August 2022 19:16 UTC) and IMG_0010 (flight 3 minutes later, about 97 m above ground), 48.51° N, 122.42° W. The five multispectral bands have 2064 × 1544 pixels, the panchromatic band 4112 × 3008 and the thermal band 320 × 256. The thermal band is in centikelvin and the camera assumes an emissivity of 1.0 (accuracy ±5 K according to the manufacturer).

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and images

We load all seven bands of the flight capture and the five bands of the panel capture. The table shows that every band has its own lens with a slightly different focal length and that the lenses are offset from each other by centimetres (RigTranslations in the metadata, relative to the green band).

### 2. Parallax between bands

Two lenses a distance T apart see the same point at a distance H shifted by Δ = T · f / (H · p) pixels, where f is the focal length and p the sensor pixel size. From 100 m this is about one pixel, from a metre above the ground over a hundred. Part of the shift does not depend on the distance (the lenses are not exactly parallel), so we compare the shift in the panel image and in the flight image: the difference is almost pure parallax of the panel image.

**Task 1.** Why does the band shift in the panel image differ from the shift in the flight image by tens of pixels, although it is the same camera? From what distance was the panel photographed, and what flight height above ground does this give? Compute the parallax of the blue band against the green one for a flight at 30 m and for a flight at 40 m over a forest with 20 m tall crowns (for the crowns and for the ground). Why is one shift for the whole image then not enough to register the bands?

### 3. Scale and rotation of the bands

We measure the shift separately in each 256 × 256 pixel tile and fit it with an affine transform d = t + A · (x, y): t is the shift at the centre, the matrix A gives the difference in scale and the rotation. The scale difference should match the ratio of the focal lengths, the rotation the third RigRelatives angle (in degrees in the metadata).

Parameters the student changes:

- `TILE = 256`: tile size (px)
- `BAND = 3`: band for the shift map (1 blue, 3 red, 4 NIR, 5 red edge)

**Task 2.** Why does the band shift change across the image (look at the arrows for the red band and then for NIR)? Does the scale agree with the ratio of the focal lengths and the rotation with RigRelatives? By how many pixels does the real shift in the corner of the image differ from the shift at the centre? Where in the image and on which objects does NDVI from a whole-pixel shift (as in the basic version) differ most from the affine registration, and why there?

### 4. How a calibration error propagates into NDVI

When NIR has a relative error e_NIR and the red band e_Red, NDVI changes by approximately ΔNDVI ≈ (1 − NDVI²) / 2 · (e_NIR − e_Red). A common error of both bands cancels out. We compare the formula with the computation on the image and look at what calibration from the DLS alone, without the panel, does to the indices.

Parameters the student changes:

- `REGIONS = {"road": (slice(1140, 1260), slice(1570, 1650)), "dry meadow": (slice(100, 500), slice(1120, 1500)), "orchard": (slice(20, 640), slice(20, 560))}`: regions (rows, columns)
- `ERR_RED, ERR_NIR = 0.00, 0.05`: relative calibration error of the red and NIR band (0.05 = +5 %)

**Task 3.** Set ERR_NIR = 0.05 and ERR_RED = 0: why does NDVI of the road and the meadow shift more than NDVI of the orchard? Check the formula for ERR_RED = 0.05 and for ERR_RED = ERR_NIR. Calibration from the DLS alone gives reflectance in the individual bands that differs by several to tens of percent (the ratio was printed), yet NDVI changes only by hundredths. Why? For which tasks is the DLS without a panel enough, and for which is it not?

### 5. The thermal band and vegetation

The thermal band stores temperature in centikelvin, computed with an emissivity of 1.0. A real surface has a lower emissivity, and part of the radiation the camera sees is reflected sky. In the grey-body approximation σT_b⁴ = ε σT⁴ + (1 − ε) σT_sky⁴. The thermal camera has a coarser pixel and a different focal length, so we average NDVI to the size of a thermal pixel, convert via the principal points of the lenses and find the remaining shift so that the correlation of NDVI and temperature is strongest.

Parameters the student changes:

- `EPS = 0.95`: surface emissivity for the correction (the camera assumes 1.0)
- `T_SKY = -30.0`: sky brightness temperature (°C), an assumption for a clear sky

**Task 4.** How large is a thermal pixel on the ground, and how many multispectral pixels fall into it? How warm are the road, the dry meadow and the orchard, and what explains that the orchard is so much cooler? Find the points with NDVI below zero and low temperature in the plot and on the maps: what are they? Set EPS to 0.97 (vegetation) and 0.92 (dry soil) and T_SKY to −10 °C (cloudy): by how much does the temperature change, and is that more or less than the accuracy of the camera?

### 6. Sharpening with the panchromatic band

The panchromatic band captures a wide range of wavelengths (the centre and width are in the table in step 1) with a pixel half the size. The HPM method (high-pass modulation) multiplies each resampled band by the ratio pan / pan blurred to the MS resolution. We first register pan to the mean of bands 1–4 in the same way as in step 3.

Parameters the student changes:

- `CROP = (slice(1000, 1400), slice(1400, 1850))`: crop in MS pixels (rows, columns)

**Task 5.** How many times finer is the panchromatic pixel, and by how much did the share of fine detail in the red band increase? Why is NDVI from the sharpened bands the same as from the unsharpened ones (the difference is at the level of rounding)? Why does sharpening not change the mean reflectance? Pan also covers part of NIR: is the sharpened red band as trustworthy for vegetation as the sharpened green one? Consider how vegetation looks in pan and how in the red band.

**Extension (optional).** From the GSD table compute at what height a thermal pixel would be 10 cm and what pixel the multispectral bands would then have. How many times more flight lines would that mean, with the same side overlap, compared with the flight at 97 m? Check it in the Drone flight planner notebook.

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Images: MicaSense, Inc. (2017–2023). *imageprocessing* (MIT licence), https://github.com/micasense/imageprocessing, files data/ALTUM-PT/IMG_0000_*.tif and IMG_0010_*.tif and micasense/image.py (radiance, vignetting, thermal band).
- MicaSense: Altum and Altum-PT Thermal Band – FAQ, https://support.micasense.com/hc/en-us/articles/360036377834 (centikelvin, emissivity 1.0, accuracy ±5 K).
- Zitová, B., Flusser, J. (2003). Image registration methods: a survey. *Image and Vision Computing* 21(11), 977–1000.
- Kuglin, C. D., Hines, D. C. (1975). The phase correlation image alignment method. *Proceedings of the IEEE International Conference on Cybernetics and Society*, 163–165.
- Vivone, G. et al. (2015). A critical comparison among pansharpening algorithms. *IEEE Transactions on Geoscience and Remote Sensing* 53(5), 2565–2586.
- Norman, J. M., Becker, F. (1995). Terminology in thermal infrared remote sensing of natural surfaces. *Agricultural and Forest Meteorology* 77, 153–166.
- Carlson, T. N., Gillies, R. R., Perry, E. M. (1994). A method to make use of thermal infrared temperature and NDVI measurements to infer surface soil water content and fractional vegetation cover. *Remote Sensing Reviews* 9, 161–173.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
