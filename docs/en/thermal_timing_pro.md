# When to fly a thermal camera, advanced: slopes, shadows and forest on real terrain

Description of the notebook for the visual [When to fly a thermal camera](https://openskylab.space/edu_viz_thermal_timing.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/thermal_timing_pro_en.ipynb) · version 1.0 · about 55 min · four tasks

## What the notebook is about

The advanced version of the thermal timing notebook. The surface model from the basic version runs here for every four-metre cell of the real slope of the Vltava valley at Roztoky: with slope and aspect from DMR 5G, terrain shadows, forest and meadow from DMP 1G and the real direct and diffuse radiation from Open-Meteo. You find out when the terrain alone creates the largest and smallest differences in a thermal image and when forest and meadow cross over in temperature.

## Goal

Compute the Sun's position, the illumination of slopes and terrain shadows, run the surface energy balance for every cell of the area, compare meadow temperature by slope aspect during the day, and find the time of day when temperature is least affected by terrain, on a sunny and an overcast day.

## Data

DMR 5G (terrain) and DMP 1G (surface) from ČÚZK, 4 m cells, a 1 × 0.7 km area on the left slope of the Vltava valley at Roztoky; hourly temperature, humidity, direct (on a normal surface) and diffuse radiation, cloud cover and wind from Open-Meteo for the last 92 days (weather model, not on-site measurement); thermal properties of meadow and forest as in the basic version. The model ignores cold air draining into the valley at night, radiation reflected from neighbouring slopes and changing soil moisture; DMP 1G dates from 2009–2013.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup, terrain and weather

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

Parameters the student changes:

- `LAT, LON = 50.152, 14.392`: centre of the area (left slope of the Vltava valley at Roztoky)
- `FOREST_H = 5.0`: vegetation height (m) from which a cell counts as forest
- `DAY, CLOUDY = days.idxmax().date(), days.idxmin().date()`: day to compute (default is the sunniest and the most overcast)

### 2. Sun, slopes and shadows

Direct radiation falls on a slope in proportion to cos i, where i is the angle between the ray and the slope normal: cos i = cos z · cos s + sin z · sin s · cos(φ − A), z is the solar zenith angle, φ its azimuth, s the slope and A the slope aspect. A cell is in shadow when the terrain in the direction of the Sun blocks the ray. The maps show cos i, zero in shadow.

Parameters the student changes:

- `hours = [7, 9, 13, 17]`: local hours for the maps

**Task 1.** Which parts of the area are in shadow at 7 o'clock, and why those? Why are east-facing slopes the most illuminated in the morning and west-facing ones at 17 o'clock, although the Sun is at a similar height at both times? What does this mean for a thermal image of the valley taken early in the morning?

### 3. Surface temperature of every cell

The same energy balance as in the basic version runs for every cell, only the absorbed radiation is direct radiation times cos i (outside shadow) plus diffuse radiation times the fraction of the sky the cell sees. The meadow has soil with heat conduction into the depth, the forest is a thin layer of crowns. The model starts three days before the chosen day; the computation takes about a minute.

Parameters the student changes:

- `MEADOW = dict(alb=0.20, eps=0.98, k=1.2, C=2.5e6, rs=70.0)`: meadow (albedo, emissivity, conductivity, soil heat capacity, stomatal resistance)
- `FOREST = dict(alb=0.12, eps=0.98, rs=100.0, node=3.0e4, rough=3.0)`: forest (crowns as one thin layer)

**Task 2.** By how many degrees do meadows on east-, south-, west- and north-facing slopes differ at 9 and at 13 o'clock? Why is the south slope warmest at 13 o'clock but the west slope at 17 o'clock? Why have the differences almost gone at 21 o'clock? What would follow for finding waterlogged spots in meadows from midday temperature?

### 4. When the terrain interferes least

The spread of temperature between cells of the same surface (the difference between the 95th and 5th percentiles) shows how large differences in a thermal image the terrain alone creates, not differences in the surface. We compare the sunniest and the most overcast day and also follow the forest minus meadow difference.

**Task 3.** At what time of day is the meadow temperature spread smallest, and how long after sunset does it take for the differences between slopes to disappear? Why do they not disappear immediately? Change the thermal conductivity `k` in `MEADOW` to 0.6 (dry soil) and watch how this changes. How large is the spread on the overcast day, and why?

**Task 4.** When do forest and meadow cross over in temperature on the sunny day, and how does this differ from the overcast day? The model ignores cold air draining into the valley. How would a real pre-dawn thermal image of the valley look different from the model, and why might the smallest spread then not be just before dawn?

**Extension (optional).** Set `LAT, LON` to the slope above the Brno reservoir (49.2467, 16.4798) or to the valley near Hosín by Hluboká nad Vltavou (49.0452, 14.4769) and compare shadows, differences by slope aspect and the time of the smallest spread.

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Digital terrain model of the Czech Republic, 5th generation (DMR 5G) and digital surface model, 1st generation (DMP 1G), © ČÚZK, licence CC BY 4.0, services https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer and https://ags.cuzk.cz/arcgis2/rest/services/dmp1g/ImageServer
- Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- Solar position: NOAA Global Monitoring Laboratory, *General Solar Position Calculations* (formulas for declination and the equation of time).
- Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744.
- Oke, T. R. (1987). *Boundary Layer Climates*, 2nd ed. Routledge (thermal properties of soil, albedos, local climate of slopes).
- Maes, W. H. (2025). Practical guidelines for performing UAV mapping flights with snapshot sensors. *Remote Sensing* 17(4), 606. https://doi.org/10.3390/rs17040606

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
