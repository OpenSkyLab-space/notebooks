# Drone flight planner, advanced: image coverage, terrain following, wind and batteries

Description of the notebook for the visual [Drone flight planner](https://openskylab.space/edu_viz_flight_planner.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/flight_planner_pro_en.ipynb) · version 1.0 · about 60 min · five tasks

## What the notebook is about

The advanced version of the flight planning notebook. On the wooded slope of the Vltava valley at Roztoky you compare three ways of holding height: constant above the take-off point, following the terrain from DMR 5G, and following the canopy surface from DMP 1G. For each you compute how many images see every point, the clearance above the trees and how fast the drone would have to climb. Then you choose the line direction from today's wind forecast and split the mission into flights of one battery each.

## Goal

Compute image coverage of the area and clearance above the surface for three height modes, find the smoothing of the height profile needed for the climb rate, find the fastest line direction in real wind, and split the mission into flights so that energy remains for every return.

## Data

DMR 5G (terrain) and DMP 1G (surface including vegetation and buildings) from ČÚZK, ImageServer services, 2 m cells, a 1.2 × 0.8 km area on the left slope of the Vltava valley at Roztoky; today's hourly wind forecast at 80 m from Open-Meteo; drone and camera parameters of the Mavic 3E from the manufacturer's data sheet. DMP 1G comes from airborne laser scanning in 2009–2013, so trees may have grown or been felled since. The coverage model assumes a camera pointing straight down and ignores occlusion (a crown hides the ground beneath it); the turn time is indicative.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

### 2. Terrain, surface and the line plan

DMR 5G describes the bare terrain, DMP 1G the surface the camera sees: tree crowns and roofs. Their difference is the height of vegetation and buildings. The plan is the same as in the basic version: a Mavic 3E camera, east–west lines, take-off at the western edge.

Parameters the student changes:

- `LON, LAT = 14.392, 50.152`: centre of the area (left slope of the Vltava valley at Roztoky)
- `HOME = (0.0, Hh / 2)`: position of the take-off point in the area (x, y in m)
- `H0 = 80.0`: flight height (m) above the take-off point, the terrain or the surface depending on the mode
- `FO, SO = 0.80, 0.70`: forward and side overlap
- `V = 8.0`: airspeed (m/s)
- `SMOOTH = 40`: smoothing length of the line height profile (m) for terrain and surface following

### 3. How many images see every point

For each image we compute which surface cells lie in its footprint. The footprint grows with the camera height above what it sees, so crowns closer to the camera are covered by a smaller patch. We compare three modes: **constant** height H0 above the take-off point, **terrain** (H0 above DMR 5G) and **surface** (H0 above DMP 1G). For following, the height profile of the line is smoothed (`SMOOTH`).

**Task 1.** On flat ground every point would be on as many images as the plan cell printed. Why is the median lower for terrain following and higher for constant height and surface following? Where in the constant-height map are the points with the fewest images, and why? Forest photogrammetry usually calls for higher overlap: change `FO` and `SO` and watch the share of points on fewer than 9 images.

**Task 2.** Look at the smallest clearance above the surface and the range of GSD. Why is the clearance above the tallest crowns smallest and GSD most variable at constant height? What would happen with terrain following if the trees had grown 5 m since the 2009–2013 scanning, or if there were a mast in the area that the DMP did not capture? Set `H0 = 50` and compare.

### 4. How fast the drone would have to climb

When following terrain or surface, the drone flies at speed V and its height follows the line profile. The vertical speed is V times the slope of the profile. When it exceeds the climb or descent limit, the drone has to slow down. The table shows different smoothing lengths: 2 m means no smoothing.

Parameters the student changes:

- `V_UP, V_DOWN = 6.0, 6.0`: maximum climb and descent rate (m/s), Mavic 3E in normal mode

**Task 3.** Why is the surface profile much steeper than the terrain profile, although the lines are the same? What is the shortest smoothing length that lets the drone keep within the 6 m/s limit at 8 m/s, and what do you lose (the columns showing how much higher than H0 it flies)? How would the result change at 12 m/s?

### 5. Wind and line direction

The drone keeps airspeed V. On a downwind line the ground speed increases, upwind it decreases, and in a crosswind the drone has to crab, so it decreases in both directions. We compute the time of the whole mission for line azimuths from 0° to 165° with today's wind at 80 m. The lines cover the whole rectangle of the area, a turn costs `T_TURN` seconds.

Parameters the student changes:

- `WIND = float(met.wind_speed_80m.iloc[hour])`: wind speed (m/s); default is today's windiest hour between 6 and 20 h
- `WDIR = float(met.wind_direction_80m.iloc[hour])`: direction the wind blows from (°, 0 = from the north)
- `T_TURN = 8.0`: time for one turn (s), indicative

**Task 4.** At which azimuth is today's mission shortest, and how big is the difference from the worst? Why are downwind and upwind lines slower than crosswind lines, although the gain downwind and the loss upwind seem to cancel out? Set `WIND = 2` and then `WIND = 0`: which azimuth wins now and why (number of lines and turns)? What happens when `WIND` exceeds `V`?

### 6. Splitting the mission into batteries

Lines are added to a flight one by one as long as energy for a direct return to the take-off point remains after the next line. Then the drone lands, the battery is swapped and the next flight starts with a transit to the following line.

Parameters the student changes:

- `AZ = int(orient["time (min)"].idxmin())`: line azimuth (°); default is the fastest in the table
- `E_BAT, TEMP, RESERVE = 77.0, 1.0, 0.20`: battery (Wh), usable capacity (0.7–0.8 in frost), landing reserve

**Task 5.** How many flights does the mission need, and why do the flights have different numbers of lines? Move the take-off point `HOME` to the centre of the area (600, 400) and rerun the cells from the data loading: do you save a flight? Set `TEMP = 0.75` as in frost. Why does planning count on returning against the wind, even though the wind may weaken during the flight?

**Extension (optional).** Set `LON, LAT` to the slope above the Brno reservoir (16.4798, 49.2467) or the valley near Hosín by Hluboká nad Vltavou (14.4769, 49.0452), where the terrain also rises from east to west, and compare coverage, smoothing and number of flights with Roztoky.

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Digital terrain model of the Czech Republic, 5th generation (DMR 5G) and digital surface model of the Czech Republic, 1st generation (DMP 1G), © ČÚZK, licence CC BY 4.0, services https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer and https://ags.cuzk.cz/arcgis2/rest/services/dmp1g/ImageServer
- ČÚZK: *Technical report on the digital surface model of the Czech Republic, 1st generation (DMP 1G)* (in Czech), https://geoportal.cuzk.gov.cz/Dokumenty/TECHNICKA_ZPRAVA_DMP_1G.pdf (total standard height error 0.4 m for buildings and 0.7 m for vegetation).
- Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- DJI: *Mavic 3 Enterprise, specs* (https://enterprise.dji.com/mavic-3-enterprise/specs): 4/3 sensor, 5280 × 3956 px, 12.3 mm focal length; climb 6 m/s and descent 6 m/s in normal mode; 45 min endurance; 77 Wh battery.
- Flight height in the open category max. 120 m from the closest point of the surface of the earth: Commission Implementing Regulation (EU) 2019/947, Annex, UAS.OPEN.010.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
