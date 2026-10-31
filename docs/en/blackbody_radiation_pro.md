# Blackbody radiation, advanced: surface temperature, heat island and drought from Landsat 8

Description of the notebook for the visual [Blackbody radiation](https://openskylab.space/edu_viz_blackbody_radiation.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/blackbody_radiation_pro_en.ipynb) · version 1.0 · about 65 min · four tasks

## What the notebook is about

The advanced version of the Planck's law notebook. Here you compute surface temperature from the Landsat 8 thermal band with the radiative transfer equation, i.e. with both emissivity and atmosphere, and find out which correction matters more. You then apply the result to the Prague urban heat island on two days and to the TVDI drought index from the temperature–NDVI space.

## Goal

Compute surface temperature from the radiative transfer equation and estimate the effect of emissivity and atmosphere, measure the surface urban heat island by land-cover class, and build the dry and wet edges and the TVDI index from the temperature–NDVI space.

## Data

Landsat 8 OLI/TIRS Collection 1 Level-1 from the Google Cloud public archive: `LC08_L1TP_191025_20190626_20190705_01_T1` (26 June 2019, heat wave) and `LC08_L1TP_191025_20170519_20170525_01_T1` (19 May 2017), bands B4, B5, B10, BQA and MTL; ESA WorldCover 2021 v200 classes. A 30 × 30 km window around Prague, about 25 MB. The atmospheric parameters (transmittance, upwelling and downwelling radiance) are not downloaded: they are given as indicative values that can be changed; real values for a given day and place come for instance from the NASA calculator (Barsi et al. 2005).

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and two scenes

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

Parameters the student changes:

- `SCENES = {"2019-06-26": "LC08_L1TP_191025_20190626_20190705_01_T1", "2017-05-19": "LC08_L1TP_191025_20170519_20170525_01_T1"}`: two scenes (heat wave, spring)
- `LON, LAT, HALF = 14.45, 50.08, 15000`: window centre and half width (m)

### 2. Surface temperature from the radiative transfer equation

The sensor above the atmosphere measures L = τ · [ε · B(Ts) + (1 − ε) · L↓] + L↑: the surface emission attenuated by the atmosphere, plus reflected sky radiation and the emission of the atmosphere itself. We solve the equation for Ts. Emissivity is estimated from NDVI as in the basic version; the atmospheric parameters τ, L↑ and L↓ are indicative values for a humid summer atmosphere.

Parameters the student changes:

- `TAU, L_UP, L_DOWN = 0.80, 1.6, 2.7`: atmospheric transmittance and upwelling and downwelling radiance (W·m⁻²·sr⁻¹·µm⁻¹), indicative summer values

**Task 1.** By how many degrees does the emissivity correction shift the temperature, and by how many the atmospheric correction? How much does the median temperature change when τ changes by 0.05? What does this mean for the accuracy of surface temperature when you do not know the atmospheric parameters for the day?

### 3. The surface urban heat island

We compare the surface temperature of built-up land with the surrounding farmland and forest on two days. The same atmospheric parameters are used for both days, which is a simplification: the atmosphere in May 2017 differed from the 2019 heat wave.

**Task 2.** On which day is the difference between built-up land and cropland larger, and why, given that the heat wave was in June 2019? Why does the built-up minus forest difference change less between the days? How would the heat island change at night (remember thermal inertia)?

### 4. Temperature–NDVI space and the TVDI drought index

In a plot of surface temperature against NDVI the pixels form a triangle or trapezoid. The upper, dry edge joins the warmest pixels at each NDVI (surfaces with no water to evaporate), the lower, wet edge the coolest. TVDI = (Ts − Ts_wet) / (Ts_dry(NDVI) − Ts_wet) lies between 0 (wet) and 1 (dry) (Sandholt et al. 2002). We compute it for grassland and cropland.

Parameters the student changes:

- `NBINS = 20`: number of NDVI bins for finding the dry edge

**Task 3.** Why does the dry edge have a negative slope, i.e. why are dry pixels with higher NDVI cooler? On which day does cropland come out drier, and does that match what you know about spring 2017 and the 2019 heat wave? Why can the TVDI of two days not be compared directly when the edges are computed for each image separately?

**Task 4.** Grassland comes out drier than cropland in TVDI. Look at the map to see where grassland lies according to WorldCover (urban lawns, dry slopes, edges of built-up areas). Which assumptions of the method (the same weather across the window, only differences in moisture, not in roughness or elevation) may not hold here? Change `NBINS` and watch how sensitive the dry edge is.

**Extension (optional).** Look up the atmospheric parameters for Prague and both days in the NASA calculator (atmcorr.gsfc.nasa.gov), put them in place of the indicative values (separately for each day) and compare the temperatures and the heat island.

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Landsat 8 OLI/TIRS Collection 1 Level-1, U.S. Geological Survey; Google Cloud public archive (`gcp-public-data-landsat`). USGS data have no use restrictions, attribution requested.
- Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- USGS (2019). *Landsat 8 (L8) Data Users Handbook*, version 5.0, ch. 5.
- Sobrino, J. A., Jiménez-Muñoz, J. C., Paolini, L. (2004). Land surface temperature retrieval from LANDSAT TM 5. *Remote Sensing of Environment* 90, 434–440. https://doi.org/10.1016/j.rse.2004.02.003
- Barsi, J. A., Schott, J. R., Palluconi, F. D., Hook, S. J. (2005). Validation of a web-based atmospheric correction tool for single thermal band instruments. *Proc. SPIE* 5882, 58820E. https://doi.org/10.1117/12.619990
- Sandholt, I., Rasmussen, K., Andersen, J. (2002). A simple interpretation of the surface temperature/vegetation index space for assessment of surface moisture status. *Remote Sensing of Environment* 79, 213–224. https://doi.org/10.1016/S0034-4257(01)00274-7

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
