# Calibrating a multispectral camera: from DN to reflectance on real images

Description of the notebook for the visual [Calibrating a multispectral camera](https://openskylab.space/edu_viz_multispectral_calibration.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/multispectral_calibration_altum_pt_en.ipynb) · version 1.0 · about 45 min · five tasks

## What the notebook is about

The visual shows what a cloud, drone tilt, vignetting and a small panel do to reflectance. Here you go through the whole chain on real images from a MicaSense Altum-PT camera: an image of the calibration panel before the flight and an image from the flight over a road, an orchard, a dry meadow and a polytunnel. Everything you need (black level, vignetting, calibration coefficients, panel reflectance, readings of the DLS 2 light sensor) is stored directly in the TIFF files.

## Goal

Convert DN to radiance step by step, compute the calibration coefficient from the panel, compare reflectance from the panel only, from the DLS only and from both, show the effect of vignetting, saturation and DLS tilt, and compute NDVI from co-registered bands.

## Data

Two captures (5 multispectral bands) from a MicaSense Altum-PT camera with DLS 2 from the MicaSense sample data (repository micasense/imageprocessing, MIT licence): IMG_0000 (RP06 panel, 15 August 2022 19:16 UTC) and IMG_0010 (flight 3 minutes later about 97 m above ground), 48.51° N, 122.42° W. The Altum-PT also has a panchromatic band 6 and a thermal band 7, which this notebook does not use.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and images

Loads the libraries and downloads the data.

### 2. From DN to radiance

The MicaSense model (the same as in the library `micasense/image.py`):

L = V(r) · R(y) · (DN − black level) / (gain · exposure) · a₁ / 2¹⁶

- black level: the signal without light (BlackLevel tag),
- V(r) = 1 / (1 + k₀r + … + k₅r⁶): vignetting correction by the distance r from the vignetting centre (newer cameras store a 2D polynomial in x, y instead),
- R(y) = 1 / (1 + a₂ y / exposure − a₃ y): correction by row (the sensor is read out row by row),
- a₁: the factory radiometric calibration coefficient. The result is spectral radiance in W/m²/sr/nm.

Parameters the student changes:

- `BAND = 4`: band 1 blue, 2 green, 3 red, 4 NIR, 5 red edge

**Task 1.** Go through bands 1 to 5. By what percentage does the vignetting correction boost the signal in the corner of the image, and in which band most? What percentage of pixels is saturated and where in the image are they? Why can no calibration fix a saturated pixel, and what do you do about it during the flight?

### 3. The calibration panel

The metadata of the panel image contain an area in the middle of the panel that the camera software found in the image (ReflectArea, four corners in pixels), and its reflectance in the given band (Albedo) from the calibration sheet. The mean radiance of the panel L_p gives the coefficient k = ρ_panel / L_p and the reflectance of every pixel ρ = k · L.

Parameters the student changes:

- `SHRINK = 1.0`: shrink the area from the metadata (1 = the whole area, 0.3 = only the centre)
- `GROW_PX = 0`: enlarge the area by this many pixels instead (imitates a sloppily marked panel)

**Task 2.** Set GROW_PX to 30, 60 and 90 (look at the detail to see how far the area reaches): how do the mean panel radiance and the coefficient k change? By what percentage would that shift the reflectance of the whole map? Then set SHRINK = 0.2: what happens to the variability and why? Why are only pixels from the centre of the panel averaged, and why must the panel be large enough in the image (how many pixels does it have here)?

### 4. The DLS light sensor and its tilt

The DLS measures irradiance on its top surface. When the drone tilts towards the Sun, the sensor receives more direct radiation than the horizontal ground does. DLS 2 therefore splits irradiance into a direct and a diffuse component and converts it to a horizontal surface: E_hor = E_direct · sin(solar elevation) + E_diffuse.

Parameters the student changes:

- `TILT = 10`: tilt of the DLS sensor (°)

**Task 3.** By what percentage did the horizontal irradiance change between the panel image and the flight image (the first cell printed the image times)? How large a reflectance error does a tilt of 10° and 20° towards and away from the Sun cause? Why is the error larger with a low Sun, and why does a large diffuse component (overcast) help?

### 5. Three ways to calibrate

- **panel only:** ρ = k · L. Assumes the illumination has not changed since the panel image.
- **DLS only:** ρ = π · L / E_hor. Relies on the factory calibration of both the camera and the DLS.
- **panel + DLS:** ρ = k · L · E_hor(panel) / E_hor(image). The panel sets the absolute level, the DLS tracks changes in illumination.

Check: when we apply the “DLS only” method to the panel itself, we should get its known reflectance.

Parameters the student changes:

- `REGIONS = {"road": (slice(1140, 1260), slice(1570, 1650)), "dry meadow": (slice(100, 500), slice(1120, 1500)), "orchard": (slice(20, 640), slice(20, 560))}`: regions (rows, columns)

**Task 4.** What panel reflectance does the “DLS only” method give, and by what percentage does it differ from the calibration sheet? Which method is the most reliable here and why? How much do “panel only” and “panel + DLS” differ, and why (go back to step 4)? Do the curves of the road, dry meadow and orchard match what you know from spectral signatures?

### 6. NDVI and what calibration does to it

NDVI = (ρ_NIR − ρ_R) / (ρ_NIR + ρ_R). We compare NDVI from radiance (no calibration), from the “panel + DLS” calibration, and from a calibration without vignetting correction.

Parameters the student changes:

- `NDVI_MIN = 0.5`: NDVI threshold for “vegetation”

**Task 5.** Why does NDVI from radiance differ so much from NDVI from reflectance even though it is the same image? Why does skipping the vignetting correction hardly change NDVI while it does change reflectance in the corners (compare with step 2)? How would the vegetation share change if someone thresholded NDVI from radiance?

**Extension (optional).** Classmates may have the notebook for another camera (RedEdge-MX, Altum, Altum-PT). Compare the panel coefficient k, the change in irradiance between the panel and the flight, and the difference between the “DLS only” and “panel + DLS” methods. Do the cameras differ more, or the lighting conditions during the flight?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Images and the radiometric calibration procedure: MicaSense, Inc. (2017–2023). *imageprocessing* (MIT licence), https://github.com/micasense/imageprocessing, files data/ALTUM-PT/IMG_0000_*.tif and IMG_0010_*.tif and micasense/image.py (vignetting, radiance, reflectance).
- MicaSense: RedEdge Camera Radiometric Calibration Model; Use of Calibrated Reflectance Panels for MicaSense Data (MicaSense support).
- Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20(13), 2653–2662.
- Overview of UAV multispectral calibration: Aasen, H., Honkavaara, E., Lucieer, A., Zarco-Tejada, P. J. (2018). Quantitative remote sensing at ultra-high resolution with UAV spectroscopy. *Remote Sensing* 10(7), 1091.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
