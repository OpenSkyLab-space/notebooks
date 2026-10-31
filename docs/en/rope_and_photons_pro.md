# Rope and photons, advanced: how many photons a Sentinel-2 pixel and a drone pixel collect

Description of the notebook for the visual [Rope and photons](https://openskylab.space/edu_viz_rope_and_photons.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/rope_and_photons_pro_en.ipynb) · version 1.0 · about 60 min · five tasks

## What the notebook is about

The advanced version of the photons notebook. From a real Sentinel-2 scene over Roztoky you compute how many photons reach the detector in bands B02, B04, B08 and B11 during the time the satellite crosses one pixel, what signal-to-noise ratio follows from that and how the telescope size changes it. You then do the same calculation for a drone camera and find out why a small lens low above the ground collects about as many photons as a telescope in orbit.

## Goal

Compute radiance and the number of photoelectrons per pixel from L1C reflectance, derive the signal-to-noise ratio √N, simulate photon noise for different pupils, compare the satellite with a drone through the product A·Ω, and check how SNR grows when pixels are merged and how it relates to quantisation.

## Data

Copernicus Sentinel-2B L1C `S2B_MSIL1C_20240721T100559_N0510_R022_T33UVR_20240721T121133` (21 July 2024) from the Google Cloud public archive: the MTD_MSIL1C and MTD_TL metadata and 4 × 4 km windows of bands B02, B04, B08 and B11 around Roztoky, about 2 MB. The instrument parameters (150 mm pupil, 786 km orbit altitude) are taken from the MSI description. The efficiency ETA and the drone parameters are indicative estimates: the real instrument is more complex (detector types, several lines summed in some bands), so the numbers show the order of magnitude, not the exact SNR of Sentinel-2.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and the Sentinel-2 scene

From the top-of-atmosphere reflectance ρ we get radiance L = ρ · E0 · U · cos(θs) / π, where E0 is the solar irradiance in the band, U the Earth–Sun distance correction and θs the solar zenith angle. All three values are in the scene metadata.

Parameters the student changes:

- `LON, LAT, HALF = 14.375, 50.145, 2000`: window centre (near Roztoky) and half width (m)

### 2. The photon budget of a pixel

A telescope with pupil area A sees one pixel under the solid angle Ω = (pixel / height)². The energy arriving from the pixel in time t is L · A · Ω · Δλ · t; divided by the photon energy h·c/λ and multiplied by the efficiency ETA it gives the number of photoelectrons N. For t we take the time the satellite ground track needs to cross one pixel. Photons arrive at random (Poisson), so the noise is √N and the signal-to-noise ratio SNR = √N. Detector and electronics noise are neglected here.

Parameters the student changes:

- `D_PUPIL = 0.150`: telescope entrance pupil diameter (m); MSI has an equivalent of 150 mm
- `H_ORBIT = 786e3`: orbit altitude (m)
- `ETA = 0.3`: fraction of photons turned into electrons (optics transmission × quantum efficiency), an estimate

**Task 1.** Why does B11 have the most photoelectrons although the radiance in the shortwave infrared is lower than in the near infrared? Split the difference between B04 and B11 into the contributions of band width, wavelength (photon energy), pixel size and crossing time.

**Task 2.** Compare the SNR of dark (2 %) and bright (98 %) pixels in B04. Which surfaces in the window are they? Change `ETA` to 0.6 and then to 0.15: how does SNR change, and why only with the square root?

### 3. What photon noise looks like

We simulate the B04 image as pupils of different size would record it: instead of the expected count N we draw a random number from the Poisson distribution for each pixel. The terrain is the same in all three images, only the noise changes.

Parameters the student changes:

- `DIAMETERS = [0.150, 0.050, 0.015]`: pupil diameters to compare (m)

**Task 3.** The pupil shrinks three times (150 → 50 mm). By what factor does N drop, and by what factor SNR? At what pupil diameter would the median SNR in B04 fall below 10? Check by changing `DIAMETERS`.

### 4. Drone against satellite

For the drone we use the same band B04 and the same radiance, because the scene is the same. The exposure is the longest one that keeps the image from blurring by more than one pixel during flight (pixel / speed). The drone parameters are indicative and correspond to a small multispectral camera.

Parameters the student changes:

- `DRONE = dict(D=0.003, H=100.0, gsd=0.05, speed=8.0)`: drone: pupil (m), flight height (m), ground pixel (m), speed (m/s), indicative

**Task 4.** The drone pupil has about 2500 times smaller area than the MSI pupil, and yet the number of photoelectrons is comparable, even higher. Explain it with the product A·Ω and the exposure time. What happens to N when the drone flies twice as high with the same camera (the pixel doubles)?

### 5. Merging pixels and quantisation

Merging n × n pixels adds up the photoelectrons: the signal grows with n², the noise with n, so SNR grows with n. At the end we compare photon noise with the quantisation step: the L1C value is an integer (DN) and one DN step corresponds to a certain number of electrons.

**Task 5.** By what factor does SNR grow when 10 m pixels are merged into 60 m? What do you lose? Does L1C quantisation matter for the accuracy of the values, or does photon noise dominate? What would happen if reflectance were stored with only 8 bits (step 1/255)?

**Extension (optional).** Change `H_ORBIT` to 500 km and `D_PUPIL` so that SNR stays the same. Compare the result with smaller Earth observation satellites you know something about.

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Copernicus Sentinel-2 data 2024, ESA; L1C from the Google Cloud public archive (`gcp-public-data-sentinel-2`). Licence: [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice), free use with attribution.
- ESA: *Sentinel-2 MSI Instrument*, technical guide (https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-2-msi/msi-instrument).
- The multispectral instrument of the Sentinel2 program. *Proc. SPIE* 10566, 105660H (ICSO 2008). https://doi.org/10.1117/12.2308278
- Constants h and c: exactly defined SI values since 2019, taken from `scipy.constants`.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
