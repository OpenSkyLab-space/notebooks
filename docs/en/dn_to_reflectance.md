# From DN to reflectance: Landsat 8 over Prague

Description of the notebook for the visual [From DN to reflectance](https://openskylab.space/edu_viz_dn_to_reflectance.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/dn_to_reflectance_en.ipynb) · version 1.0 · about 45 min · five tasks

## What the notebook is about

The visual walks through the chain from digital number to radiance to top-of-atmosphere (TOA) and surface (BOA) reflectance and shows what dark object subtraction (DOS) and the empirical line correct. Here you compute the whole chain on two real Landsat 8 images of Prague and compare the result with Sentinel-2 L2A reflectance from the same week.

## Goal

Convert DN to radiance and TOA reflectance, show why DN from two days are not comparable, measure the atmospheric effect over water, and compare DOS and the empirical line with surface reflectance.

## Data

Landsat 8 OLI Collection 1 Level-1 from the Google Cloud public archive: `LC08_L1TP_191025_20190626_20190705_01_T1` (26 June 2019, sun elevation 60°) and `LC08_L1TP_191025_20190218_20190222_01_T1` (18 Feb 2019, sun elevation 26°), bands B1–B7, BQA and MTL. For comparison Sentinel-2 L2A `S2B_33UVR_20190625_0_L2A` (25 June 2019) from Earth Search. A 12 × 12 km window around central Prague, about 25 MB.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and data

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

### 2. From DN to radiance and TOA reflectance

Radiance: L = M_L · DN + A_L. TOA reflectance: ρ = (M_ρ · DN + A_ρ) / sin(sun elevation). The coefficients are in the MTL file; M_ρ already includes the Earth–Sun distance and the solar irradiance of the band.

**Task 1.** How much do the median DN differ between summer and winter, and how much the median TOA reflectance? How much of the DN difference is explained by sun elevation alone (compare the ratio of the sines)? Why does even TOA reflectance not agree completely between the dates (state of vegetation, possible snow, atmosphere)?

### 3. Surface reflectance from Sentinel-2 as a reference

Sentinel-2 L2A from 25 June 2019 (one day earlier) has BOA reflectance from the Sen2Cor model. We resample it to the Landsat grid (average into 30 m pixels) and pair bands of similar wavelength. Do not expect a perfect match: it is a different sensor with slightly different bands, an image taken one day earlier and from a different viewing angle.

**Task 2.** Compare the two images with the same colour stretch. Why does the TOA reflectance image look brighter, bluer and less contrasting? Which surfaces change most between TOA and BOA, dark or bright ones? Explain it with the additive contribution of the atmosphere.

### 4. Blue water above the atmosphere

The Vltava and reservoirs are almost black in the NIR. We compare their TOA and BOA reflectance in all bands: the difference is mainly light scattered by the atmosphere (path radiance).

**Task 3.** How does TOA − BOA over water change with wavelength? Compare the ratio between bands B1 and B4 with Rayleigh's law (scattering ∝ λ⁻⁴). Why is water blue above the atmosphere although it is dark in all bands at the surface?

### 5. Dark object subtraction (DOS)

We assume that the darkest pixels in the scene have almost zero surface reflectance (1 % is the usual choice, Chavez 1996). Whatever they have on top is path radiance, which we subtract from the whole scene. DOS corrects only the additive part of the atmosphere.

Parameters the student changes:

- `pct = 0.1`: percentile taken as the dark object (%)
- `rho_dark = 0.01`: assumed true reflectance of the dark object

**Task 4.** In which bands does DOS reduce the error against BOA and in which does it make it larger? Why is the DOS bias negative in all bands (what does DOS do with the multiplicative part, the atmospheric transmittance)? Set `pct = 2` and then `rho_dark = 0`: what happens? When does DOS fail completely (a winter scene with snow and no dark objects, haze over only part of the scene)?

### 6. Empirical line

In the field a dark and a bright panel with measured reflectance are placed in the image. Here the panels are dark and bright pixels whose surface reflectance we know from Sentinel-2. For each band we fit a line ρ_BOA = a · ρ_TOA + b: the offset b relates to path radiance and the slope a to atmospheric transmittance: for ρ_TOA ≈ ρ_path + T · ρ_BOA we get a ≈ 1/T and b ≈ −ρ_path/T.

Parameters the student changes:

- `n_panel = 300`: how many darkest and brightest pixels to use as panels

**Task 5.** Why does the empirical line have a negative offset and a slope different from 1 in the blue bands? What do they express physically? Which method did best and why can DOS not correct the slope? Set `n_panel = 20`: what happens to the reliability of the line? Why are two panels enough in the field, but must be in the same image and under the same illumination?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; Google Cloud public archive (`gcp-public-data-landsat`). USGS data have no use restrictions, attribution requested.
- USGS (2019). *Landsat 8 (L8) Data Users Handbook*, version 5.0, ch. 5 (DN to radiance and TOA reflectance).
- Copernicus Sentinel-2 data 2019, ESA (L2A, Sen2Cor), AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.
- Chavez, P. S. (1988). An improved dark-object subtraction technique for atmospheric scattering correction of multispectral data. *Remote Sensing of Environment* 24, 459–479. https://doi.org/10.1016/0034-4257(88)90019-3
- Chavez, P. S. (1996). Image-based atmospheric corrections – revisited and improved. *Photogrammetric Engineering and Remote Sensing* 62(9), 1025–1036.
- Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20, 2653–2662. https://doi.org/10.1080/014311699211994

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
