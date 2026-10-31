# The temperature of Prague from Landsat 8: Planck's law in practice

Description of the notebook for the visual [Blackbody radiation](https://openskylab.space/edu_viz_blackbody_radiation.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/blackbody_radiation_en.ipynb) · version 1.0 · about 45 min · five tasks

## What the notebook is about

The visual shows Planck's law, Wien's shift, the fourth power of the Stefan–Boltzmann law and the role of emissivity. Here you apply the same formulas to a real Landsat 8 thermal image from the heat wave of 26 June 2019 and turn digital numbers into the surface temperature of Prague.

## Goal

Convert the Landsat 8 thermal band from DN to radiance and brightness temperature, correct it for emissivity, estimate the error from a wrong emissivity and from sky reflection, and show why satellites look for small fires at 3.9 µm.

## Data

Landsat 8 OLI/TIRS, Collection 1 Level-1, scene `LC08_L1TP_191025_20190626_20190705_01_T1` (26 June 2019, 9:51 UTC, cloud cover 0.1 %), bands B4, B5 and B10 and the MTL file with calibration constants from the Google Cloud public archive. Only a 16 × 16 km window around central Prague is read (about 3 MB).

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

### 2. Planck's law, Wien and the fourth power

Loads the libraries and downloads the data.

Parameters the student changes:

- `T_list = [300, 600, 900, 5772]`: temperatures in K (landscape, stove, fire, solar surface)

**Task 1.** How many times do the total exitance and the radiance at 10.9 µm increase when you double the temperature from 300 to 600 K? Why do the two numbers differ? Also compute how many per cent more asphalt at 45 °C emits than grass at 25 °C.

### 3. A real scene: from DN to brightness temperature

Band B10 (10.6–11.2 µm) stores digital numbers (DN). The MTL file holds the linear conversion to radiance, L = M · DN + A, and the constants K1, K2 that turn radiance into brightness temperature, T = K2 / ln(K1 / L + 1). It is Planck's law simplified for one band.

Parameters the student changes:

- `lon, lat, half = 14.42, 50.08, 8000`: window centre (°) and half-width (m)

**Task 2.** Find the Vltava river, large parks or forests (Stromovka, Hvězda, Krč) and built-up areas with large halls on the map. What brightness temperatures do they have? Why is the difference between the water and hall roofs so large around noon? Why is brightness temperature not the same as surface temperature?

### 4. Emissivity

Real surfaces emit less than a blackbody: L = ε · B(T). We estimate emissivity from NDVI with a simplified threshold method after Sobrino et al. (2004): bare surface 0.97, full vegetation 0.99, in between according to the vegetation fraction with a correction for multiple scattering between plants and soil. Water (NDVI < 0) gets a typical value of 0.991. Sky reflection and the atmosphere are ignored for now.

Parameters the student changes:

- `eps_soil, eps_veg, eps_water = 0.97, 0.99, 0.991`: emissivities
- `T_true = 273.15 + 40`: true surface temperature in K

**Task 3.** Where is the emissivity correction largest and why? Roughly how many kelvin is the sensor off for each hundredth of emissivity? Change `eps_soil` to 0.95 (concrete, asphalt) and watch how the correction changes in built-up areas.

### 5. Sky reflection

A surface with emissivity ε reflects 1 − ε of the longwave radiation coming from the sky. A clear sky is very cold at 10 µm, an overcast sky has roughly the temperature of the cloud base. The sensor receives L = ε · B(T) + (1 − ε) · B(T_sky).

Parameters the student changes:

- `T_surf = 273.15 + 27`: surface temperature

**Task 4.** Why does polished sheet metal under a clear sky look freezing cold in a thermal camera although it is at 27 °C? Why does emissivity not matter at all when the sky is as warm as the surface? In what weather would you therefore plan thermal imaging of roofs?

### 6. A fire smaller than a pixel

A pixel is a mixture: a fraction p burns at the fire temperature, the rest has the background temperature. As background we take the median real brightness temperature of the window (Prague) and compare the 3.9 µm band (the fire bands of MODIS and VIIRS lie between 3.7 and 4.1 µm) with the 10.9 µm band.

Parameters the student changes:

- `T_fire = 900`: fire temperature in K

**Task 5.** At what fire fraction does the pixel warm by 10 K at 3.9 µm and at 10.9 µm? What area is that within a 1 × 1 km MODIS pixel? Explain the difference with Wien's law. Why do daytime algorithms also watch for reflected sunlight at 3.9 µm?

**Extension (optional).** Compare with a classmate who ran the notebook for another place and day: what range of brightness temperatures did they get? How much of the difference can be due to another day and hour, another sun elevation and a different landscape?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Landsat 8 OLI/TIRS Collection 1 Level-1, U.S. Geological Survey; Google Cloud public archive (`gcp-public-data-landsat`). USGS data are free of use restrictions (public domain), with attribution.
- DN to radiance and brightness temperature: USGS (2019). *Landsat 8 (L8) Data Users Handbook*, version 5.0, ch. 5.
- Emissivity from NDVI: Sobrino, J. A., Jiménez-Muñoz, J. C., Paolini, L. (2004). Land surface temperature retrieval from LANDSAT TM 5. *Remote Sensing of Environment* 90, 434–440. https://doi.org/10.1016/j.rse.2004.02.003
- Fire detection at 3.9 and 11 µm: Giglio, L., Schroeder, W., Justice, C. O. (2016). The collection 6 MODIS active fire detection algorithm and fire products. *Remote Sensing of Environment* 178, 31–41. https://doi.org/10.1016/j.rse.2016.02.054

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
