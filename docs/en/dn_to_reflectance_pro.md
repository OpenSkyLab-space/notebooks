# From DN to reflectance, advanced: topographic correction in the Krkonoše mountains

Description of the notebook for the visual [From DN to reflectance](https://openskylab.space/edu_viz_dn_to_reflectance.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/dn_to_reflectance_pro_en.ipynb) · version 1.0 · about 70 min · five tasks

## What the notebook is about

The advanced version of the DN-to-reflectance notebook. The TOA reflectance formula divides by the sine of the sun elevation, i.e. it assumes flat ground. In the mountains every slope gets different illumination. You compute it from a digital elevation model for two Landsat 8 scenes with different sun elevation, measure how strongly it changes forest reflectance, and compare five topographic corrections.

## Goal

Compute slope, aspect and the solar incidence angle from a DEM, measure the terrain effect on reflectance by band and season, compare the cosine, C, Minnaert and SCS+C corrections, and judge how to validate a correction fairly.

## Data

Landsat 8 OLI Collection 1 Level-1 from the Google Cloud public archive: `LC08_L1TP_191025_20190626_20190705_01_T1` (26 June 2019, sun elevation 60°) and `LC08_L1TP_191025_20181013_20181030_01_T1` (13 Oct 2018, sun elevation 31°), bands B2–B7, BQA and MTL; Copernicus DEM GLO-30 from the AWS Open Data registry; ESA WorldCover 2021 v200 classes. A 12 × 12 km window in the eastern Krkonoše mountains, about 25 MB.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and data

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

Parameters the student changes:

- `SCENES = {"summer": "LC08_L1TP_191025_20190626_20190705_01_T1", "autumn": "LC08_L1TP_191025_20181013_20181030_01_T1"}`: two scenes with different sun elevation
- `LON, LAT, SIZE = 15.70, 50.70, 12000`: window centre (Krkonoše) and its side (m)

### 2. Slope illumination from the terrain model

On flat ground direct sunlight arrives at the zenith angle θ_s, on a slope with gradient s and aspect a at the angle i: cos i = cos θ_s · cos s + sin θ_s · sin s · cos(φ_s − a), where φ_s is the sun azimuth. The direct irradiance of the slope is proportional to cos i; diffuse skylight arrives from all directions and depends much less on the slope aspect.

**Task 1.** Compare the cos i maps in summer and in autumn. Why do south- and north-facing slopes differ much more in autumn, and how many pixels are in self-shadow? Why does the TOA reflectance formula from the visual's notebook (dividing by the sine of the sun elevation) not give the true surface reflectance on a slope?

### 3. How strongly the terrain changes forest reflectance

We take forest pixels according to WorldCover and fit a line ρ = m · cos i + b. If the slope were lit only by direct sun and the forest reflected equally in all directions, reflectance would be proportional to cos i and the offset b would be zero. The ratio C = b/m is the basis of the C-correction (Teillet et al. 1982).

**Task 2.** In which band and season is the relationship with cos i strongest? Why does the blue band have a large C, i.e. a large offset compared with the slope, and SWIR almost zero? Relate it to the share of diffuse skylight at different wavelengths.

### 4. Five corrections

The cosine correction ρ · cos θ_s / cos i assumes direct light only. The C-correction adds C to both numerator and denominator, the Minnaert correction ρ · (cos θ_s / cos i)^k estimates the exponent k from the data, and SCS+C (Soenen et al. 2005) accounts for trees growing vertically, not perpendicular to the slope. We assess the correlation with cos i after correction, the spread of forest reflectance and the ratio of medians on steep south- and north-facing slopes (for the same forest it should be close to 1).

Parameters the student changes:

- `COSI_MIN = 0.15`: pixels with cos i below this value are not corrected (nearly in shadow)

**Task 3.** Which method overcorrects (negative r, south/north ratio below 1) and why most in the blue band and in autumn? Why does r come out almost exactly zero for C, Minnaert and SCS+C, and why does that alone not prove the correction works? Suggest a fairer check (e.g. estimating the parameters on one half of the window and assessing on the other).

### 5. Maps and the vegetation index

Loads the libraries and downloads the data.

Parameters the student changes:

- `SHOW, BAND = "autumn", 5`: season and band for the maps

**Task 4.** Where do errors remain in the corrected map (steep north-facing slopes, places below `COSI_MIN`)? Set `COSI_MIN` to 0.05 and 0.3 and describe the difference. Why does the cosine correction turn shaded slopes into the brightest places in the scene?

**Task 5.** In summer NDVI hardly correlates with cos i, in autumn it does. Why does a ratio index cancel the terrain effect only when the effect is purely multiplicative? Which two differences between red and NIR (share of diffuse light from step 3, path radiance) spoil this at low sun?

**Extension (optional).** Move the window to the Šumava mountains (the DEM and WorldCover tiles then have to change, and the Landsat scenes must cover the new place) or use grassland (`wc == 30`) instead of forest. Do the C and k parameters come out similar?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; Google Cloud public archive (`gcp-public-data-landsat`). USGS data have no use restrictions, attribution requested.
- Copernicus DEM GLO-30: produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. AWS Open Data registry (`copernicus-dem-30m`).
- Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Teillet, P. M., Guindon, B., Goodenough, D. G. (1982). On the slope-aspect correction of multispectral scanner data. *Canadian Journal of Remote Sensing* 8(2), 84–106.
- Minnaert, M. (1941). The reciprocity principle in lunar photometry. *Astrophysical Journal* 93, 403–410.
- Soenen, S. A., Peddle, D. R., Coburn, C. A. (2005). SCS+C: a modified sun-canopy-sensor topographic correction in forested terrain. *IEEE Transactions on Geoscience and Remote Sensing* 43, 2148–2159. https://doi.org/10.1109/TGRS.2005.852480

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
