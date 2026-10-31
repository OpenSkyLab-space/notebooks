# Can I fly?, advanced: how accurate the model is, the wind profile and flyable hours

Description of the notebook for the visual [Can I fly? Weather for drones](https://openskylab.space/edu_viz_drone_weather.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/drone_weather_pro_en.ipynb) · version 1.0 · about 50 min · five tasks

## What the notebook is about

The advanced version of the drone weather notebook. You compare the Open-Meteo model with a week of real METAR reports from four Czech airports and compute how much the model errs in wind, temperature and dew point. Then, from three months of model data for Roztoky, you find out how the wind profile changes with atmospheric stability during the day and in which hours flying was possible most often.

## Goal

Decode a week of METAR reports, verify the model against them (bias, RMSE, correlation), compute the wind profile exponent and its dependence on temperature stratification, and build the daily cycle of the share of hours suitable for flying by wind, gusts, precipitation, visibility and icing.

## Data

METAR reports for the last 7 days from Prague (LKPR), Brno (LKTB), Ostrava (LKMT) and Karlovy Vary (LKKV) airports from the NOAA Aviation Weather Center; hourly Open-Meteo data for the same 7 days at the airport coordinates and for 92 days for Roztoky (wind at 10, 80 and 120 m, gusts, temperature at 2 and 120 m, dew point, precipitation, visibility). Open-Meteo values for past days are stored short-range model forecasts, not measurements. The data change continuously, so your numbers will differ from the stored notebook.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup

Loads the libraries and downloads the data.

### 2. A week of METAR reports

We download the reports for 7 days, decode wind, gusts, temperature, dew point, visibility and cloud base and keep one report per hour. A report only carries the day of the month; month and year are taken from today's date.

Parameters the student changes:

- `AIRPORTS = {"LKPR": (50.1008, 14.2600), "LKTB": (49.1513, 16.6944), "LKMT": (49.6963, 18.1111), "LKKV": (50.2030, 12.9150)}`: airports and coordinates

### 3. Verifying the model

For each airport we download hourly Open-Meteo data for the same 7 days and pair them with the reports. **Bias** is the mean of model − observation (systematic error), **RMSE** the root mean square of the difference (total error), **correlation** tells how well the model caught the course.

**Task 1.** Does the model underestimate or overestimate the wind? How large is the RMSE compared with the typical wind speed at the airport? At which airport does the model fit worst, and what may cause it (surrounding terrain, a valley, model resolution)? Why does METAR give wind in whole knots, and what error does that alone introduce?

**Task 2.** How accurately does the model hit temperature and dew point? The cloud base estimate is 125 m per degree of T − Td: by how many metres does the estimate shift when the dew point is off by 1 °C? What follows for deciding about fog, low cloud and icing from the model?

### 4. Wind profile and atmospheric stability

Wind grows with height approximately as u(z) = u(10 m) · (z / 10)^α. We compute the exponent α from the wind at 10 and 120 m for every hour over 92 days and compare it with the temperature difference between 120 and 2 m. If temperature falls with height faster than 1 °C per 100 m, the air is unstable and mixes; if it rises with height (an inversion), it is stable.

Parameters the student changes:

- `LAT, LON = 50.152, 14.392`: flight site (Roztoky)

**Task 3.** Why is α large at night and in the morning and small during the day? Why is there almost no wind at the ground in an inversion while it blows at 120 m? What does it mean when you measure the wind with a hand anemometer before a morning take-off and estimate the wind at flight height from it? At what time does the inversion typically break up?

### 5. Flyable hours over the last three months

For each hour over 92 days we evaluate the conditions like the traffic light in the basic version: wind at 120 m, estimated gusts at 120 m, precipitation, visibility and icing risk. The model does not give gusts at 120 m, so we estimate them from 10 m in two ways (`GUSTS`).

Parameters the student changes:

- `LIM_WIND, LIM_GUST = 10.0, 12.0`: limit for wind at 120 m and for gusts (m/s)
- `LIM_VIS = 5000`: minimum visibility (m)
- `GUSTS = "ratio"`: estimate of gusts at 120 m: "ratio" (the same gust/wind ratio as at 10 m) or "excess" (the same difference)

**Task 4.** Which condition limited flying most often over the last three months, and at what time of day was the chance to fly best? Switch `GUSTS` to the other gust estimate: by how much does the share of flyable hours change? Which estimate do you think is closer to reality, and why (how do gusts change with height)?

**Task 5.** Set the limits for a smaller drone (`LIM_WIND = 8`, `LIM_GUST = 10.7` as the wind resistance of the DJI Mini 4 Pro) and then for stricter operation with imaging (visibility 8 km). How do the share of flyable hours and its daily cycle change? Why would this calculation turn out differently for the winter months?

**Extension (optional).** Add Linz airport (`"LOWL": (48.2332, 14.1875)`) or another to `AIRPORTS` and compare the model accuracy. Change `LAT, LON` to another flight site (for example Brno-Bystrc 49.2467, 16.4798) and compare the wind profile and flyable hours.

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- METAR: NOAA/NWS Aviation Weather Center, https://aviationweather.gov/data/api/ (US government public data).
- Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- METAR code: ICAO Annex 3 / WMO-No. 306, code FM 15.
- Stull, R. B. (1988). *An Introduction to Boundary Layer Meteorology*. Kluwer (daily cycle of the boundary layer, stability, wind profile).
- Wind resistance of the DJI Mavic 3 Enterprise 12 m/s and of the DJI Mini 4 Pro 10.7 m/s (DJI data sheets).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
