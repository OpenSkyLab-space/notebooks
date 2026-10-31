# When to fly a thermal camera: surface temperatures from real weather

Description of the notebook for the visual [When to fly a thermal camera](https://openskylab.space/edu_viz_thermal_timing.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/thermal_timing_en.ipynb) · version 1.0 · about 45 min · six tasks

## What the notebook is about

The visual shows how water, meadow, asphalt, forest and photovoltaics warm up and cool down during the day, and when two surfaces merge in a thermal image. Here you drive the same kind of model (surface energy balance with heat conduction into the ground) with real hourly weather from the last months at Suchdol and look for the best flight time for a given task.

## Goal

Compute the daily course of surface temperatures from real radiation, temperature, humidity, cloud cover and wind, find the times when two surfaces cross over in temperature, compare a clear and an overcast day, show the effect of wind and of the emissivity set in the camera, and find the hours suitable for inspecting photovoltaics.

## Data

Hourly air temperature and humidity, global radiation on a horizontal and a tilted surface, cloud cover, wind at 10 m and soil surface temperature from Open-Meteo for the Suchdol campus, whatever the service returns for the last 92 days, usually two to three months (weather model, not an on-site measurement); thermal properties of materials from the literature.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and real weather

Loads the libraries and downloads the data.

Parameters the student changes:

- `LAT, LON = 50.130, 14.373`: site (Suchdol campus)
- `TILT, AZ = 35, 0`: tilt and azimuth of the PV panels (°; azimuth 0 = south, −90 = east, 90 = west)

### 2. The surface model and one clear day

For every surface the energy balance **Rn = H + LE + G** is solved every minute:

- Rn: absorbed solar radiation (1 − albedo) · S plus the long-wave balance ε (L↓ − σ T⁴). The sky L↓ comes from air temperature and humidity (Brutsaert 1975) and from cloud cover (Crawford and Duchon 1999).
- H: sensible heat to the air h · (T − Tₐ), h = 5.7 + 3.8 U, where U is the wind at 2 m (from the 10 m wind by a logarithmic profile, ×0.75).
- LE: evaporation ρ L (q*(T) − qₐ) / (rₐ + r_s); the stomatal resistance r_s is 70 s/m for the meadow and 100 s/m for the forest, water evaporates freely, asphalt and the panel not at all.
- G: heat into the ground. Asphalt and soil have 12 layers down to 1 m, the pond is a mixed water layer of 1 m, the forest canopy and the PV panel are a thin layer with no conduction into the ground.

Solar radiation, temperature, humidity, cloud cover and wind are real hourly values from Open-Meteo. The model runs from the start of the period; the first 14 days are spin-up.

Parameters the student changes:

- `DAY = SUNNY`: day, e.g. "2026-09-10"; the default is the sunniest day
- `A, B = "water", "meadow"`: pair of surfaces

**Task 1.** Read off the times of both crossovers of water and meadow. Why is water warmer than the meadow at night and colder at noon? Compare the modelled meadow with the soil surface temperature from Open-Meteo (dotted): where do they differ most and why might that be (it is a model too, not a measurement)? Try the pair asphalt × forest.

### 3. Clear or overcast?

We compare the sunniest and the most overcast day in the downloaded data. The amplitude is the difference between the daily maximum and minimum of surface temperature.

Parameters the student changes:

- `DAYS = [SUNNY, CLOUDY]`: days to compare (you can add a third one, e.g. "2026-09-20")

**Task 2.** By how much did the amplitude of asphalt and water shrink on the overcast day? What happened to the water − meadow difference at night? Explain the role of solar radiation during the day and of long-wave radiation from clouds at night.

### 4. Contrast calendar: when to fly

For every day and hour we compute the temperature difference of a pair of surfaces. White areas are crossovers, when the surfaces merge in a thermal image.

Parameters the student changes:

- `A, B = "water", "meadow"`: pair of surfaces
- `MIN_DT = 3`: contrast you can still reliably tell apart in a thermal image (K)

**Task 3.** In which hours is the contrast between water and meadow reliably large, and in which do the surfaces merge? How do the crossovers shift from summer to autumn and why? You are looking for wet spots in a meadow (pair meadow × water): when would you fly and why rather in the morning than at noon?

### 5. Wind

We compute the same weather again with weaker and stronger wind (we multiply the wind). Everything else stays real.

Parameters the student changes:

- `FACTORS = [0.5, 1, 2, 4]`: multiples of the real wind
- `DAY_W = SUNNY`: day

**Task 4.** How do the noon maximum of asphalt, the morning minimum of the meadow and the asphalt − meadow contrast change with stronger wind? Why does wind reduce contrasts in a thermal image? What wind limit would you recommend for a thermal flight?

### 6. Emissivity in the camera and photovoltaics

The camera measures the exitance W = ε σ T⁴ + (1 − ε) σ T_refl⁴, where the second term is the reflected surroundings. It computes temperature using the emissivity ε_c and the reflected temperature T_refl set in the camera. Simplification: we compute over the whole spectrum, not only the 8–14 µm band, and take the reflected surroundings to be the sky.

For inspecting PV plants an irradiance of at least 600 W/m² on the panel is recommended (IEA PVPS). The irradiance of the tilted surface comes from Open-Meteo.

Parameters the student changes:

- `EPS_CAM = 1.00`: emissivity set in the camera (try 0.95 and 0.85)
- `T_REFL = 20.0`: reflected temperature set in the camera (°C)
- `HOURS = ["05:00", "13:00"]`: times of the images
- `DAY_E = SUNNY`: day
- `THRESH = 600`: minimum panel irradiance for PV inspection (W/m²)

**Task 5.** With emissivity 1.00 in the camera: which surface differs most from its true temperature and why does the PV panel look colder than it is? Set 0.95 and then 0.85: which surface is now right and which are not? Why is the error at night different from the one at noon (think of the reflected sky)?

**Task 6.** In which months and hours was the panel irradiance at least 600 W/m²? In step 1 change the tilt to 60° and the azimuth to −90° (east) and run the cells again: how does the inspection window shift? Why is the contrast of a faulty or disconnected module small in weak sunlight?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744 (clear-sky long-wave radiation).
- Crawford, T. M., Duchon, C. E. (1999). An improved parameterization for estimating effective atmospheric emissivity. *Journal of Applied Meteorology* 38, 474–480 (effect of cloud cover).
- Oke, T. R. (1987). *Boundary Layer Climates*, 2nd ed. Routledge (thermal conductivity and heat capacity of asphalt and soil, albedos).
- Maes, W. H. (2025). Practical guidelines for performing UAV mapping flights with snapshot sensors. *Remote Sensing* 17(4), 606. https://doi.org/10.3390/rs17040606 (planning mapping flights, thermal included).
- IEA PVPS Task 13 (2018). *Review on Infrared and Electroluminescence Imaging for PV Field Applications*, Report IEA-PVPS T13-10:2018 (glass emissivity 0.85, irradiance ≥ 600 W/m²).
- Convective heat transfer h = 5.7 + 3.8 U (McAdams), saturation vapour pressure by the Magnus formula (WMO-No. 8, 2018).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
