# Photons in the Sentinel-2A bands

Description of the notebook for the lab [Rope and photons](https://openskylab.space/edu_viz_rope_and_photons.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/rope_and_photons_hluboka_en.ipynb) · version 1.0 · about 40 min · six tasks

## What the notebook is about

In the lab you watched a wave on a rope. Its speed $v$, wavelength
$\lambda$ (the distance between neighbouring crests) and frequency $f$ (the number of
oscillations per second) are linked by

$$
v = \lambda f.
$$

**Light in vacuum obeys the same relation**, with the speed of light $c$. Light
carries energy in photons. From the wavelength we get the frequency and the energy
of one photon:

$$
f = \frac{c}{\lambda}, \qquad E = hf.
$$

$h$ is the Planck constant; we express energy in electronvolts (eV),
a unit of energy. **A shorter wavelength means a higher frequency and a larger photon
energy.** At the same frequency, more photons arriving on the same area per second
deliver more energy; the energy of each photon does not change.
Here you compute this for the real bands of the Sentinel-2A satellite.

## Goal

From the metadata of a real Sentinel-2 scene, compute the frequency, photon energy and photon flux in each band and work out which detector each band needs.

## Data

The product metadata of Sentinel-2A L1C, tile 33UVQ (around Hluboká nad Vltavou and České Budějovice), 5 January 2024 (`MTD_MSIL1C.xml` from the Google Cloud public archive): central wavelengths, spectral response of the bands and top-of-atmosphere solar spectral irradiance. About 50 kB is downloaded.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The notebook is stored without outputs; numbers and plots appear when it runs and may differ between runs where the data are updated continuously.

## Step by step

### 1. Setup and data

Loads the libraries and downloads the data.

### 2. Wavelength and frequency

Loads the libraries and downloads the data.

**Task 1.** The `lambda_x_f` column is the same for every band. What does it express and what does it correspond to on the rope in the lab? How many times higher is the frequency of band B2 (blue) than of B12 (SWIR 2)?

### 3. Energy of one photon

The energy of one photon is given by the Planck–Einstein relation:

$$
E = hf = \frac{hc}{\lambda}.
$$

We use $h \approx 6.626\times10^{-34}\ \mathrm{J\,s}$,
$c \approx 3.00\times10^8\ \mathrm{m\,s^{-1}}$ and the wavelength
$\lambda$ in metres, so the result comes out in joules.
Since $1\ \mathrm{eV} = 1.602\,176\,634\times10^{-19}\ \mathrm{J}$,
we convert the energy to eV by dividing by this value. In the code it is the
numerical value of `e`, the elementary charge in coulombs, from `scipy.constants`.

**Task 2.** Check the energy ratio of the blue and red photon from the wavelengths alone, without constants. Why is the ratio of λ enough? How does the energy of one photon change when the blue light is twice as bright?

### 4. From radiant energy to photon flux

The metadata give the top-of-atmosphere solar spectral irradiance $E_0$
in $\mathrm{W\,m^{-2}\,\mu m^{-1}}$. Dividing it by the energy of one photon
in joules gives the number of photons arriving per second on one square metre
per unit wavelength, here per micrometre:

$$
\Phi_\lambda = \frac{E_0}{E}.
$$

$\Phi_\lambda$ has the unit $\mathrm{s^{-1}\,m^{-2}\,\mu m^{-1}}$.
It is the spectral photon flux density, not the total number of photons in the band.

**Task 3.** The spectral irradiance E0 falls more than twentyfold from blue (B2) to SWIR 2 (B12). Does the spectral photon flux density fall in the same way? Explain the difference. In which band does the most photons per micrometre fall on a square metre, and why is it not the band with the highest E0?

### 5. Which bands a silicon chip can see

A photon frees an electron in a detector only if its energy is at least the band gap of the material. For silicon it is about 1.12 eV. We compute the cut-off wavelength and check how much of each band's response lies below it.

Parameters the student changes:

- `Eg = 1.12`: band gap in eV (silicon 1.12; InGaAs about 0.75; HgCdTe 0.1–0.5 depending on composition)

**Task 4.** Which Sentinel-2 bands would a silicon detector capture fully, partly and not at all? Set `Eg = 0.75` (InGaAs) and run the cell again. What changed? Sentinel-2 uses HgCdTe detectors for bands B10 to B12: why?

### 6. Thermal radiation and radar

We compare photons from a thermal band (10.9 µm, as in Landsat 8 TIRS) and from the Sentinel-1 radar (5.405 GHz) with the typical thermal energy in a detector at room temperature, k · T.

Parameters the student changes:

- `T = 300`: detector temperature in kelvin

**Task 5.** A thermal photon has only about four times the energy of k · T, a radar photon is more than a thousand times weaker than k · T. Why are thermal cameras with photon detectors cooled, and why do a microbolometer and a radar antenna measure heating or the electric field of the wave rather than individual photons? Set `T = 77` (liquid nitrogen) and compare.

**Task 6.** At what wavelength does a photon have an energy of 10 eV (the approximate ionisation threshold)? Which part of the spectrum is it? Chemical bonds in molecules have energies of a few eV. Explain why a single UV photon can damage DNA while a strong radar signal carries more energy in total and still breaks no bond and ionises nothing.

**Extension (optional).** Classmates may have the notebook for another Sentinel-2 satellite (2A, 2B or 2C). Compare the central wavelengths of the bands and the E0 values: by how many nanometres do bands of the same name differ, and why must anyone who builds a time series from several satellites take this into account?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Copernicus Sentinel-2 data 2024, ESA; L1C metadata from the Google Cloud public archive (`gcp-public-data-sentinel-2`). Licence: [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice), free use with attribution.
- Constants h, c, e, k: exactly defined SI values since 2019, taken from `scipy.constants`; CODATA 2022 overview: [NIST](https://physics.nist.gov/cuu/pdf/wall_2022.pdf).
- Silicon band gap 1.12 eV at 300 K: Sze, S. M., Ng, K. K. (2007). *Physics of Semiconductor Devices*, 3rd ed. Wiley.
- Sentinel-1 radar frequency (C band) 5.405 GHz: ESA, Sentinel-1 User Handbook.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
