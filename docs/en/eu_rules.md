# Where may I fly: UAS geographical zones from ANS CR data

Description of the notebook for the visual [Where and how may I fly](https://openskylab.space/edu_viz_eu_rules.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/eu_rules_en.ipynb) · version 1.0 · about 45 min · five tasks

## What the notebook is about

The visual walks through the decision tree of the European drone rules. Here you go through one of its branches, UAS geographical zones, on real data: you download the current zones published by Air Navigation Services of the Czech Republic (ŘLP), find out which zones the planned flight sites fall into, how high you may fly near airports and how zones change over time. This is a teaching aid, not legal advice: before a flight always check the zones in the DroneMap app and the conditions in the CAA measures of general nature (OOP).

## Goal

Load the list of geographical zones and their GeoJSON files, determine the zones for given sites and for a whole mapping flight area, convert the vertical limits of zones (AGL, AMSL, FL) to metres above ground, read height restrictions from the grid around airports, and compare the current and the next release of the zones.

## Data

UAS geographical zones as GeoJSON (reference boundaries) from the ŘLP page https://aim.rlp.cz/?lang=cz&p=uas-gz, downloaded at run time; terrain elevation from Open-Meteo (Copernicus DEM 90 m).

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and the list of zones

Installs the libraries Colab lacks (`pyproj`, `shapely`) and downloads the data.

### 2. Which zones do the flight sites fall into?

We download zones up to a chosen file size (the largest layers, e.g. densely populated areas or class III roads, have hundreds of MB and would take long to download in Colab). For each site we find out which zones it lies in and what the vertical limit of the zone is.

Parameters the student changes:

- `MAX_MB = 20`: largest file to download (MB)
- `SITES = {`: flight sites (latitude, longitude)

**Task 1.** Which zones do the individual sites lie in? Which site is free of restrictions from the downloaded layers, and why does that still not mean you may fly there (which large layers did you not download, and what could they change)? Add a site where you want to fly yourself to SITES and compare the result with the DroneMap map.

### 3. Vertical limits of zones

A zone applies only between its lower and upper limit. Limits are given above ground (AGL), above mean sea level (AMSL) or as a flight level (FL, hundreds of feet at the standard pressure of 1013.25 hPa; here we treat it as an AMSL height for simplicity). 1 ft = 0.3048 m. Terrain elevation comes from Open-Meteo.

Parameters the student changes:

- `FLIGHT_AGL = 120`: planned flight height above ground (m)

**Task 2.** Both the outer and the inner zone of the Prague CTR (LKR314C and LKR314D) have an upper limit of 3500 ft AMSL: how many metres above ground is that in Suchdol? Why do some LKR320A airspace areas not concern a drone at 120 m at all? Why does terrain elevation matter for limits in AMSL or FL, and what does that mean for a flight in the mountains (Pec pod Sněžkou)?

### 4. The grid around controlled airports

Around controlled airports (CTR) ŘLP publishes a grid of 30″ × 30″ cells (about 600 × 900 m) where each cell states up to what height above ground flight is allowed without further approval. The conditions of using the grid are in the relevant OOP.

Parameters the student changes:

- `CENTER = (50.10, 14.30)`: centre of the map (latitude, longitude)
- `SPAN = 0.25`: half the extent of the map (°)

**Task 3.** Up to what height may you fly in Suchdol and in Kněževes according to the grid? How does the allowed height change towards the runway, and why? Move the map to another controlled airport (e.g. Brno 49.15° N, 16.69° E) and compare the shape of the grid. Why is a grid better than one large zone with a single height?

### 5. The whole area of a mapping flight

A mapping flight covers an area, not a point. We compute what share of a square around the site lies in each zone (in metres, in UTM 33N coordinates).

Parameters the student changes:

- `SITE = "Roztoky forest"`: a site from SITES
- `HALF_M = 1500`: half the side of the flight square (m)

**Task 4.** Which zones reach into the flight square even though the centre itself is not in them? How does the result change for a 0.5 km and a 3 km square? How would you split the mapping flight so that as much area as possible lies outside restrictions, and what would you have to arrange for the rest?

### 6. Zones change

Besides the current zones, ŘLP also publishes releases that will take effect in the future (following the AIRAC cycle). We compare layers that exist in both releases: the number of zones, their identifiers and the area added or removed.

**Task 5.** Which layers change in the next release, and how many zones and how much area are added or removed? Why must a drone have current data for its geo-awareness function, and why is it not enough to check the zones once when planning a project that lasts several weeks?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- UAS geographical zones: Air Navigation Services of the Czech Republic (ŘLP ČR), AIM, https://aim.rlp.cz/?lang=en&p=uas-gz; zone map: https://dronemap.gov.cz
- Commission Implementing Regulation (EU) 2019/947 on the rules and procedures for the operation of unmanned aircraft, Article 15 (UAS geographical zones); Delegated Regulation (EU) 2019/945.
- Civil Aviation Authority of the Czech Republic: measures of general nature on UAS geographical zones (LKR311 to LKR320), https://www.caa.gov.cz
- Terrain elevation: Open-Meteo Elevation API (Copernicus DEM GLO-90), https://open-meteo.com (CC BY 4.0).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
