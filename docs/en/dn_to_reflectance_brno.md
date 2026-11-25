# From DN to reflectance: Landsat 8 over Brno

Description of the notebook for the lab [From DN to reflectance](https://openskylab.space/edu_viz_dn_to_reflectance.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/dn_to_reflectance_brno_en.ipynb) · version 1.0 · about 45 min · five tasks

## What the notebook is about

The lab walks through the chain from digital number to radiance to top-of-atmosphere (TOA) and surface (BOA) reflectance and shows what dark object subtraction (DOS) and the empirical line correct. Here you compute the whole chain on two real Landsat 8 images of Brno and compare the result with Sentinel-2 L2A reflectance from the same week.

## Goal

Convert DN to radiance and TOA reflectance, show why DN from two days are not comparable, measure the atmospheric effect over water, and compare DOS and the empirical line with surface reflectance.

## Data

Landsat 8 OLI Collection 1 Level-1 from the Google Cloud public archive: `LC08_L1TP_190026_20200808_20200821_01_T1` (8 Aug 2020, sun elevation 54°) and `LC08_L1TP_190026_20190227_20190309_01_T1` (27 Feb 2019, sun elevation 30°), bands B1–B7, BQA and MTL. For comparison Sentinel-2 L2A `S2B_33UXQ_20200808_0_L2A` (8 Aug 2020) from Earth Search. A 12 × 12 km window from the Brno reservoir to central Brno, about 25 MB.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The notebook is stored without outputs; numbers and plots appear when it runs and may differ between runs where the data are updated continuously.

## Step by step

### 1. Setup and data

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

### 2. From DN to radiance and TOA reflectance

Radiance: L = M_L · DN + A_L. TOA reflectance: ρ = (M_ρ · DN + A_ρ) / sin(sun elevation). The coefficients are in the MTL file; M_ρ already includes the Earth–Sun distance and the solar irradiance of the band.

**Task 1.** How much do the median DN differ between summer and winter, and how much the median TOA reflectance? How much of the DN difference is explained by sun elevation alone (compare the ratio of the sines)? Why does even TOA reflectance not agree completely between the dates (state of vegetation, possible snow, atmosphere)?

### 3. Surface reflectance from Sentinel-2 as a reference

Sentinel-2 L2A from 8 Aug 2020 (the same day) has BOA reflectance from the Sen2Cor model. We resample it to the Landsat grid (average into 30 m pixels) and pair bands of similar wavelength. Do not expect a perfect match: it is a different sensor with slightly different bands, an image taken about 20 minutes later and from a different viewing angle.

**Task 2.** Compare the two images with the same colour stretch. Why does the TOA reflectance image look brighter, bluer and less contrasting? Which surfaces change most between TOA and BOA, dark or bright ones? Explain it with the additive contribution of the atmosphere.

### 4. Blue water above the atmosphere

The Brno reservoir and the Svratka are almost black in the NIR. We compare their TOA and BOA reflectance in all bands: the difference is mainly light scattered by the atmosphere (path radiance).

**Task 3.** How does TOA − BOA over water change with wavelength? Compare the ratio between bands B1 and B4 with Rayleigh's law (scattering ∝ λ⁻⁴). Why is water blue above the atmosphere although it is dark in all bands at the surface?

### 5. Dark object subtraction (DOS)

We assume that the darkest pixels in the scene have almost zero surface reflectance (1 % is the usual choice, Chavez 1996). Whatever they have on top is path radiance, which we subtract from the whole scene. DOS corrects only the additive part of the atmosphere.

Parameters the student changes:

- `pct = 0.1`: percentile taken as the dark object (%)
- `rho_dark = 0.01`: assumed true reflectance of the dark object

**Task 4.** In which bands does DOS reduce the error against BOA and in which does it make it larger? Why is the DOS bias negative in all bands (what does DOS do with the multiplicative part, the atmospheric transmittance)? Set `pct = 2` and then `rho_dark = 0`: what happens? When does DOS fail completely (a winter scene with snow and no dark objects, haze over only part of the scene)?

### 6. Empirical line

The empirical line corrects reflectance with a slope and an offset. In the field the
reference can be physical calibration panels with known reflectance.
In this exercise we use **reference pixels**: their reference reflectance
is taken from a Sentinel-2 L2A image.

For each band we look for a line between the Landsat TOA reflectance and the reference
BOA reflectance. We then correct the whole band with this line:

$$
\widehat{\rho}_{\mathrm{BOA}} = a\,\rho_{\mathrm{TOA}} + b.
$$

- $\rho_{\mathrm{TOA}}$ is the input top-of-atmosphere reflectance.
- $\widehat{\rho}_{\mathrm{BOA}}$ is our estimate of the surface reflectance.
- $a$ is the **slope** (`slope`): it scales the values.
- $b$ is the **offset** (`offset`): it adds the same correction to every value.

Reflectance, slope and offset are dimensionless. For a simplified model of the atmosphere

$$
\rho_{\mathrm{TOA}} \approx \rho_{\mathrm{path}} + T\,\rho_{\mathrm{BOA}}
\quad\Rightarrow\quad
a \approx \frac{1}{T},\qquad b \approx -\frac{\rho_{\mathrm{path}}}{T},
$$

where $T$ is the atmospheric transmittance and $\rho_{\mathrm{path}}$ the contribution of
atmospheric scattering expressed as reflectance. This physical reading is approximate:
here we compare two different sensors, and the reference BOA is itself a product of processing.

### 6.1 Select reference pixels and correct the image

In each band we select, according to Sentinel-2, the `n_reference` darkest and the same
number of brightest valid pixels. With `n_reference = 300` the line is therefore fitted
to **600 pairs of values**, not to two group means. Different bands
may select different pixels.

Indexing with `[valid]` picks the values at the valid locations shared by both images,
in the same order. `np.argsort` returns their indices from darkest to
brightest. `np.polyfit(..., deg=1)` computes the slope and offset of the line
from the selected pairs. We then apply the line to the whole Landsat band.

**After changing `n_reference`, run all three cells of this part again (6.1–6.3).**

### 6.2 Compare the errors of all three approaches

The table shows the slope and offset in each band and the RMSE of the original TOA reflectance,
of the DOS correction and of the empirical line against the Sentinel-2 BOA reference:

$$
\mathrm{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^{N}
\left(\rho_i^{\mathrm{estimate}}-\rho_i^{\mathrm{reference}}\right)^2}.
$$

$N$ is the number of all valid pixels and $i$ denotes one of them. A smaller RMSE
means better agreement with the reference. All methods are evaluated on the same pixels,
including those used to fit the line, so this is not an independent accuracy assessment.

### 6.3 Show the agreement with Sentinel-2

The horizontal axis shows the reference BOA, the vertical axis the reflectance from the given approach.
The black 1 : 1 line marks perfect agreement. Colours distinguish the blue band B2,
the red B4 and the near-infrared B5.

For clarity we plot only **4,000 randomly selected valid pixels**,
the same for all plots and bands. The fixed seed `0` makes the selection
repeatable. This sample is used only for plotting; it changes neither the calibration nor the RMSE.

Parameters the student changes:

- `n_reference = 300`: pixels in each group

**Task 5.** Why does the empirical line have a negative offset and a slope different from 1 in the blue bands? What do they express physically? Which method has the smallest RMSE in each band, and why can DOS not correct the slope? Set `n_reference = 20` and run cells 6.1–6.3 again: how do the slope, offset and RMSE change? Why are two calibration panels with different known reflectance enough to determine the line in the field, but must they be in the same image and under the same illumination?

**Extension (optional).** Compare your results with a classmate who ran the notebook for another place: did you get a similar TOA − BOA difference over water and a similar empirical line slope? What could make them differ (another day, other haze, another sun elevation)?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; Google Cloud public archive (`gcp-public-data-landsat`). USGS data have no use restrictions, attribution requested.
- USGS (2019). *Landsat 8 (L8) Data Users Handbook*, version 5.0, ch. 5 (DN to radiance and TOA reflectance).
- Copernicus Sentinel-2 data 2020, ESA (L2A, Sen2Cor), AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.
- Chavez, P. S. (1988). An improved dark-object subtraction technique for atmospheric scattering correction of multispectral data. *Remote Sensing of Environment* 24, 459–479. https://doi.org/10.1016/0034-4257(88)90019-3
- Chavez, P. S. (1996). Image-based atmospheric corrections – revisited and improved. *Photogrammetric Engineering and Remote Sensing* 62(9), 1025–1036.
- Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20, 2653–2662. https://doi.org/10.1080/014311699211994

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
