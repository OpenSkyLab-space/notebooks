# A flight plan over the Vltava valley: GSD, overlaps, terrain and wind

Description of the notebook for the visual [Drone flight planner](https://openskylab.space/edu_viz_flight_planner.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/flight_planner_en.ipynb) · version 1.0 · about 50 min · five tasks

## What the notebook is about

In the visual you planned a flight over flat ground and over a model hill. Here you apply the same formulas to real terrain: the slope of the Vltava valley at Roztoky from the ČÚZK DMR 5G digital terrain model (lidar, 2 m cells), and to the current wind forecast at flight height.

## Goal

Compute flight height for a target GSD, line spacing, trigger interval and speed, motion blur and skew, show how terrain changes height above ground and overlap, and plan the return against the wind.

## Data

DMR 5G (ČÚZK, ImageServer, heights in Bpv, 2 m cells) for a 1.2 × 0.8 km area on the left slope of the Vltava valley at Roztoky; hourly wind forecast at 10, 80 and 120 m from Open-Meteo; camera parameters from manufacturers' data sheets (same as in the visual).

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

### 2. Camera, height and GSD

GSD = H · p / f, where p is the pixel pitch on the sensor (sensor width / pixel count). From a target GSD, H = GSD · f / p.

Parameters the student changes:

- `gsd_target = 1.5`: target GSD in cm/px

**Task 1.** Why does the Mavic 3M have to fly much lower than the P1 for the same GSD? Set `gsd_target` to 2 and then 4 cm/px. For which cameras and GSDs would the height exceed 120 m, the open-category limit? What are the consequences of flying low (number of images, time, safety)?

### 3. Real terrain and the line plan

We load DMR 5G for the slope of the Vltava valley. Lines run east–west, i.e. down the fall line into the valley and back. The take-off point is on the plateau at the western edge.

Parameters the student changes:

- `cam = CAMERAS["Mavic 3E"]`: camera
- `H0 = 80`: flight height above the take-off point (m)
- `fo, so = 0.80, 0.70`: forward and side overlap
- `v_air = 10.0`: airspeed (m/s)
- `long_across = True`: long side of the image across the flight direction?

**Task 2.** Increase `v_air` until the warning that the camera cannot keep up appears. What is the highest speed? Switch `long_across = False`: how do base, maximum speed, number of lines and flight time change? Why does a rotated image allow faster flight and yet the flight may take longer? Set the forward overlap to 0.85 as for vegetation.

### 4. Constant height or terrain following?

At a constant height above the take-off point, the height above ground changes with terrain: H_AGL = H0 + z_takeoff − z. GSD and footprint change with it, while base and line spacing stay fixed, so the actual overlap changes.

Parameters the student changes:

- `follow = False`: True = terrain following (constant height H0 above ground)

**Task 3.** At a constant 80 m above the plateau: what is the range of GSD and overlaps? Where is the overlap smallest, on the plateau or in the valley, and why? How much of the area is more than 120 m above the terrain? Switch to `follow = True`: what improves and what do you need for terrain following (terrain model, its accuracy, obstacles)?

### 5. Real wind, motion blur and rolling shutter

We take today's wind forecast for Roztoky from Open-Meteo. Blur = ground speed · exposure / GSD; rolling-shutter skew = ground speed · sensor readout time / GSD. The Zenmuse P1 and Mavic 3E have a mechanical shutter, so skew practically disappears for them (t_read = 0); the default 30 ms is an order-of-magnitude value for an electronic rolling shutter.

Parameters the student changes:

- `hour = 6 + int(met.wind_speed_80m.values[6:21].argmax())`: hour of the flight (local time); default is the windiest hour between 6 and 20 h
- `t_exp = 1 / 1000`: exposure time (s)
- `t_read = 0.030`: sensor readout time of a rolling shutter (s); 0 = global shutter

**Task 4.** What wind does the forecast give at 10, 80 and 120 m and why do they differ? How do blur and skew differ on the downwind and upwind legs? Why does a shorter exposure not reduce the skew? When would you rather orient the lines along or across the wind?

### 6. Battery and return to home

The Mavic 3E has a 77 Wh battery and the maker states up to 45 min of flight without wind, i.e. about 100 W on average. We compute how much energy a return from the farthest point needs when the wind blows away from the take-off point.

Parameters the student changes:

- `E_bat = 77.0`: battery energy (Wh)
- `temp_factor = 1.0`: usable capacity (1.0 at 20 °C; roughly 0.7–0.8 in frost)
- `reserve = 0.20`: landing reserve

**Task 5.** Is one battery enough? Set `temp_factor = 0.75` and then increase the wind (`headwind = 8`). Why is "downwind out, upwind back" a trap? Also try a higher `v_air`: why does flying faster help in strong wind even though power increases?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Digital terrain model of the Czech Republic, 5th generation (DMR 5G), © ČÚZK, licence CC BY 4.0, service https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer
- Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- Camera parameters: data sheets of DJI Zenmuse P1, Mavic 3 Enterprise (3E, 3M) and a generic 1″ 20 MP camera (the shortest interval of 2 s for the Mavic 3M and the generic camera is an indicative value); Mavic 3 Enterprise battery 5000 mAh, 15.4 V (77 Wh).
- Flight height in the open category max. 120 m from the closest point of the surface of the earth: Commission Implementing Regulation (EU) 2019/947, Annex, UAS.OPEN.010.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
