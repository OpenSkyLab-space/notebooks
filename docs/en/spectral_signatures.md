# Spectral signatures from Sentinel-2: forest, fields, water and snow

Description of the notebook for the visual [Spectral signatures](https://openskylab.space/edu_viz_spectral_signatures.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/spectral_signatures_en.ipynb) · version 1.0 · about 45 min · six tasks

## What the notebook is about

The visual shows how chlorophyll, leaf water, dry matter and LAI shape the spectral curve of vegetation and why NDVI stops growing in dense canopies. Here you check it on real Sentinel-2 pixels near Roztoky and on a time series of one field over the 2024 season.

## Goal

Compare real spectral curves of surfaces, locate the red edge, show NDVI saturation on a field time series, and explain why the same index from different bands gives a different number.

## Data

Sentinel-2 L2A from the Earth Search catalogue on AWS: scene `S2B_33UVR_20240721_0_L2A` (21 July 2024, near Roztoky), cloud-free scenes of tile 33UVR from March to October 2024 for the time series, and `S2A_33UWS_20240308_0_L2A` (snow in the Krkonoše mountains); ESA WorldCover 2021 classes. About 30 MB is downloaded; the time series takes 1 to 3 minutes.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

### 2. Spectral curves of real surfaces

Loads the libraries and downloads the data.

**Task 1.** Describe the forest curve: why is it low in blue and red, with a small peak in green and a steep rise between 0.70 and 0.78 µm? Why does the field (in late July often ripe grain or stubble) have more red and less NIR than the forest? Why is the spread so large for built-up areas and fields?

### 3. Red edge position

The red edge is the steep rise in reflectance between red and NIR. We estimate its position (REP) by linear interpolation from bands B4, B5, B6 and B7 (Guyot and Baret 1988). More chlorophyll shifts the edge to longer wavelengths.

**Task 2.** Which surface has the red edge furthest and why? Does it make sense to compute REP for water or built-up areas? Look at the values and explain why the index has no physical meaning without vegetation even though it returns a number.

### 4. NDVI saturation during the season

We take one field pixel near Únětice and all cloud-free images from 2024. We compare NDVI = (NIR − R)/(NIR + R), NDRE = (NIR − RE1)/(NIR + RE1) and NDMI = (NIR − SWIR1)/(NIR + SWIR1).

Parameters the student changes:

- `lon, lat = 14.3516, 50.1632`: point (field near Únětice); also try forest, e.g. 14.366, 50.148

**Task 3.** When did the field reach its peak and when was it harvested? In what NDVI range does the NDVI–NDRE plot bend, i.e. NDVI hardly grows but NDRE still does? Explain the saturation: why can red not drop any lower at high LAI while the red edge still moves?

**Task 4.** How does NDMI behave during the season and why does it drop earlier or faster than NDVI as the crop ripens? Change the point to forest (`14.366, 50.148`) and compare: why is the forest series much flatter?

### 5. Water and snow

NDWI (green and NIR, McFeeters 1996) highlights water, NDSI (green and SWIR 1.6 µm) highlights snow. Snow is bright in the visible but absorbs in the SWIR; clouds reflect in both.

Parameters the student changes:

- `thr = 0.4`: NDSI threshold for snow (MODIS uses 0.4)

**Task 5.** Why does NDSI separate snow from clouds although both are white in the visible? Change the threshold to 0.2 and 0.6: where does the mask change most (snowy forest, shadows, dwarf pine)? Why is the Vltava positive in NDWI and vegetation negative?

### 6. Same index, different number

NDVI can be computed from Sentinel-2 with the broad band B8 (centred near 833 nm, over 100 nm wide, 10 m pixel) or the narrow B8A (865 nm, about 21 nm wide, 20 m pixel). A drone multispectral camera or Landsat have different bands again. We compare both variants on the same pixels.

**Task 6.** How much do the two NDVIs differ and in which direction? Suggest two causes (band position and width, 10 vs 20 m resolution). What follows when you want to compare drone NDVI with Sentinel-2 NDVI, or old and new NDVI maps?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); COG copy in the AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution under the [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).
- Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Red edge position by linear interpolation: Guyot, G., Baret, F. (1988). Utilisation de la haute résolution spectrale pour suivre l'état des couverts végétaux. *Proc. 4th Int. Colloquium on Spectral Signatures of Objects in Remote Sensing*, ESA SP-287, 279–286.
- NDVI saturation and red-edge indices: Gitelson, A. A., Merzlyak, M. N. (1994). Spectral reflectance changes associated with autumn senescence of *Aesculus hippocastanum* L. and *Acer platanoides* L. leaves. *Journal of Plant Physiology* 143, 286–292. https://doi.org/10.1016/S0176-1617(11)81633-0
- NDWI: McFeeters, S. K. (1996). The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. *International Journal of Remote Sensing* 17, 1425–1432. https://doi.org/10.1080/01431169608948714
- NDSI for snow: Hall, D. K., Riggs, G. A., Salomonson, V. V. (1995). Development of methods for mapping global snow cover using MODIS. *Remote Sensing of Environment* 54, 127–140. https://doi.org/10.1016/0034-4257(95)00137-P

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
