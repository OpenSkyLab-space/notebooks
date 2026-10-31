# Can I fly? Real METAR reports and wind at flight height

Description of the notebook for the visual [Can I fly? Weather for drones](https://openskylab.space/edu_viz_drone_weather.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/drone_weather_hluboka_en.ipynb) · version 1.0 · about 45 min · five tasks

## What the notebook is about

In the visual you decoded example METAR reports, converted the airport wind to the flight site and height and decided with a traffic light. Here you download real METAR reports from Czech airports for the last 24 hours, decode them yourself and compare the result with a model forecast of wind at 80 and 120 m.

## Goal

Decode METAR, compute relative humidity and an estimate of the cloud base, convert the 10 m wind to flight height over different terrain, estimate the return against the wind, and decide about flying over the next 24 hours.

## Data

METAR and TAF reports from Linz (LOWL, the nearest airport with regular reports; České Budějovice LKCS was not sending METAR reports to the service in October 2026), Prague (LKPR), Brno (LKTB) and Karlovy Vary (LKKV) airports from the NOAA Aviation Weather Center; an hourly forecast from Open-Meteo for Hluboká nad Vltavou. The data change every half hour, so your numbers will differ from the stored notebook.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and real METAR reports

Loads the libraries and downloads the data.

Parameters the student changes:

- `STATIONS = "LOWL,LKPR,LKTB,LKKV"`: ICAO airport codes

### 2. Your own decoder

A report has a fixed order of groups: airport, time, wind (direction, speed, gusts G), visibility in metres or CAVOK, weather (RA rain, SN snow, BR mist, FG fog, - light, + heavy), cloud (FEW, SCT, BKN, OVC and height in hundreds of feet), temperature/dew point (M = minus) and QNH pressure. The part after TEMPO, BECMG or NOSIG is a short trend forecast and the decoder skips it.

**Task 1.** Pick one report and decode it by hand group by group; does it agree with the table? Which groups alone would rule out a VLOS flight (visibility, fog, low cloud, precipitation)? Why is the difference T − Td more important to a pilot than the temperature alone?

**Task 2.** How well does the estimate 125 m · (T − Td) match the reported cloud base? The estimate holds for cumulus in a well-mixed daytime layer. Find reports where it fails and explain why (night, stratiform cloud, inversion, cloud from another air mass).

### 3. Wind at flight height over different terrain

Airports measure wind 10 m above grass (roughness length z0 = 0.03 m). At a blending height of 60 m the surface hardly matters, so we transfer the wind there to the flight site with a different roughness z0 and zero-plane displacement d (Wieringa 1986). This holds for neutral stratification (windy, overcast); on a sunny day or at night the profile differs.

Parameters the student changes:

- `u10 = float(met[met["station"] == "LOWL"]["wind m/s"].iloc[0])`: wind at 10 m (default is the latest Linz METAR)

**Task 3.** Why is the mean wind at 30 m weaker over forest than over water, but almost the same at 100 m? A colleague says: "The airport reports 6 m/s, the drone handles 12 m/s, we have a twofold margin." Set `u10 = 6` and answer with numbers for 100 m. How does the 80 m / 10 m ratio from the Open-Meteo model differ from our profile and why (stability during day and night)?

### 4. The way back against the wind

The drone flies at airspeed V, the wind at flight height is U. Over a distance D downwind out and upwind back the flight takes t = D/(V + U) + D/(V − U).

Parameters the student changes:

- `V, D = 12.0, 800`: airspeed (m/s) and distance from the pilot (m)

**Task 4.** Derive from the formula at what wind the round-trip time doubles (the cell prints U = V/√2). Why is it not enough that the mean wind at flight height is below the drone's wind resistance when gusts (the gust column in METAR) are 30–50 % higher? How would you plan the route accordingly?

### 5. A traffic light for the next 48 hours

For each hour of the Open-Meteo forecast for the flight site we decide: wind at 120 m and gusts against the drone's limit, precipitation, visibility and icing risk (temperature below 1 °C and T − Td within 2 °C).

Parameters the student changes:

- `limit = 12.0`: drone wind resistance (m/s)

**Task 5.** When would you fly in the next 48 hours and what decides the other hours? Compare the forecast with the latest TAF for Linz: do they agree? We estimated gusts at 120 m from the gust-to-wind ratio at 10 m; why is that rough, and is the result on the safe side or not? Set `limit = 10.7` (wind resistance of a small sub-250 g drone such as the DJI Mini 4 Pro). What changes?

**Extension (optional).** Classmates may have the notebook for another site and other airports (Roztoky and Prague; Brno-Bystrc and Brno-Tuřany; Hluboká and Linz). Compare, for the same hour, the METAR wind, the 80 m / 10 m wind ratio from Open-Meteo and the traffic-light result. Why does the ratio differ with site and terrain?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- METAR and TAF: NOAA/NWS Aviation Weather Center, https://aviationweather.gov/data/api/ (US government public data).
- Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- Relative humidity and saturation vapour pressure (Magnus formula): WMO (2018). *Guide to Instruments and Methods of Observation* (WMO-No. 8), annex 4.B.
- Wind transfer via a 60 m blending height: Wieringa, J. (1986). Roughness-dependent geographical interpolation of surface wind speed averages. *Quarterly Journal of the Royal Meteorological Society* 112, 867–889; Verkaik, J. W. (2000). Evaluation of two gustiness models for exposure correction calculations. *Journal of Applied Meteorology* 39, 1613–1626.
- METAR code: ICAO Annex 3 / WMO-No. 306, code FM 15.
- DJI Mavic 3 Enterprise wind resistance 12 m/s, max. speed 15 m/s in normal mode, 21 m/s in sport mode (DJI data sheet); DJI Mini 4 Pro wind resistance 10.7 m/s.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
