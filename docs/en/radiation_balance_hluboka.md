# Where sunlight goes: surface balance from Sentinel-2 (Hluboká and Šumava)

Description of the notebook for the visual [Where radiation goes](https://openskylab.space/edu_viz_radiation_balance.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/radiation_balance_hluboka_en.ipynb) · version 1.0 · about 40 min · six tasks

## What the notebook is about

In the visual, incoming radiation splits into reflected, absorbed and transmitted parts, ρ + α + τ = 1, and Kirchhoff's law gives ε = α. Here you measure reflectance on real Sentinel-2 pixels (forest, meadow, field, built-up area, water and snow), compute how much radiation the surfaces absorb in real weather and estimate how warm they get.

## Goal

Compute absorptance and albedo of surfaces from real reflectance, apply Kirchhoff's law to snow and metals, and estimate the equilibrium surface temperature from an energy balance with current weather, then design a cool roof.

## Data

Sentinel-2 L2A (surface reflectance) from the Earth Search catalogue on AWS: scene `S2B_33UVQ_20240731_0_L2A` (31 July 2024, near Hluboká nad Vltavou) and `S2A_33UVQ_20230209_0_L2A` (9 February 2023, snow in the Šumava mountains around Plechý); land-cover classes from ESA WorldCover 2021; hourly weather for České Budějovice from Open-Meteo (last 92 days). About 15 MB is downloaded.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

### 2. Reflectance of real surfaces

We load a 3 × 3 km window around Hluboká nad Vltavou and for each ESA WorldCover class take the median reflectance of clear pixels (no clouds or shadows according to the SCL mask). We add snow from the Šumava mountains around Plechý; to get open snow without trees, we take only snow pixels with green reflectance above 0.5.

### 3. Absorptance: α = 1 − ρ − τ

For the satellite a pixel is opaque: whatever is not reflected back is absorbed by the canopy, the soil or the water below. For the whole pixel α = 1 − ρ. (For a single leaf, τ in the NIR is about as large as ρ; inside a canopy the transmitted light is reflected and absorbed further.)

**Task 1.** Where do forest and meadow absorb most and least? Why is it useful for a plant to absorb almost no NIR? Why does water absorb almost everything that enters it in the NIR?

**Task 2.** Snow is white in visible light. What is its absorptance at 1.6 µm (B11)? Kirchhoff's law gives ε = α at the same wavelength. Sentinel-2 has no thermal band (10 µm), but the trend from visible to SWIR hints at how snow behaves further on. Why is snow almost a blackbody in the thermal range (ε ≈ 0.99) and what does that mean for measuring its temperature with a thermal camera?

### 4. Albedo: how much sunlight a surface reflects in total

Albedo is reflectance weighted by the solar spectrum. Liang (2001) derived it for Landsat bands as a linear combination; we use the corresponding Sentinel-2 bands (B2, B4, B8, B11, B12), so the result is approximate.

### 5. Real weather and the energy balance

From Open-Meteo we take the sunniest hour of the last 92 days in České Budějovice: global radiation S, air temperature, dew point and wind. A surface in equilibrium (no evaporation and no conduction into the ground) satisfies

(1 − albedo) · S + ε · L↓ = ε · σ · T⁴ + h · (T − T_air),

where L↓ is the longwave radiation of the sky (Brutsaert 1975, clear sky) and h = 5.7 + 3.8 · u is convective heat transfer.

Parameters the student changes:

- `u = row.wind_speed_10m * 0.75`: wind near the surface (about 3/4 of the 10 m wind)

**Task 3.** Rank the surfaces by absorbed radiation and by equilibrium temperature. A real sunlit forest or meadow is usually only a few degrees warmer than the air. Which term of the balance is missing from the model? How is this used when looking for water stress in crops with a thermal camera on a drone? Why does the model fail completely for water?

**Task 4.** Change `u` to 0.5 and then to 6 m/s. How does the equilibrium temperature of the built-up area change? Why does wind reduce the temperature differences between surfaces?

### 6. Design a cool roof

We vary the albedo and emissivity of a roof under the same real weather. Polished metal reflects a lot of sunlight but hardly emits in the thermal range (ε ≈ 0.1); white paint reflects sunlight and emits as well (ε ≈ 0.9).

Parameters the student changes:

- `for eps in (0.05, 0.3, 0.6, 0.9):`: roof emissivities

**Task 5.** What temperature would a roof with the albedo of the built-up area in your window have, and a white roof (albedo 0.8, ε 0.9)? Why is polished sheet metal with albedo 0.6 (ε 0.05) so much warmer than a coating with the same albedo and emissivity 0.9? What properties should an ideal coating have at 0.3–2.5 µm and at 8–13 µm?

**Task 6.** Pick another hour from the `met` table, for instance the warmest one, and put it in place of `row` (e.g. `row = met.loc[met.temperature_2m.idxmax()]` for the warmest hour). How do the ranking and the temperatures of the surfaces change? The model gives snow a temperature above 0 °C: why is that impossible in reality, and what does the surplus energy go into? Why does snow still not melt immediately in spring sunshine even though S is high?

**Extension (optional).** Compare your results with a classmate who ran the notebook for another place: do the albedos of built-up land, fields and snow differ? Did the sunniest hour fall on another day and with another S?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Copernicus Sentinel-2 data 2023–2024, ESA, processed by ESA (L2A, Sen2Cor); COG copy in the AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution under the [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).
- Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. Zenodo. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Weather: Open-Meteo.com, ICON/ECMWF models as available (CC BY 4.0). https://open-meteo.com
- Narrowband to broadband albedo: Liang, S. (2001). Narrowband to broadband conversions of land surface albedo I: Algorithms. *Remote Sensing of Environment* 76, 213–238. https://doi.org/10.1016/S0034-4257(00)00205-4
- Clear-sky longwave radiation: Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744. https://doi.org/10.1029/WR011i005p00742
- Convective heat transfer coefficient h = 5.7 + 3.8 · u: McAdams, W. H. (1954). *Heat Transmission*, 3rd ed. McGraw-Hill (as given in Duffie, J. A., Beckman, W. A., *Solar Engineering of Thermal Processes*).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
