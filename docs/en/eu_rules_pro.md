# Where may I fly, advanced: zone geometry, a map of allowed height, flight levels and the AIRAC cycle

Description of the notebook for the visual [Where and how may I fly](https://openskylab.space/edu_viz_eu_rules.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/eu_rules_pro_en.ipynb) · version 1.0 · about 60 min · five tasks

## What the notebook is about

The advanced version of the notebook on UAS geographical zones. On current ŘLP data you check whether the geometry of zones matches their description, build a map of allowed flight height around Brno from the grids, compute from METAR reports how high flight levels really are, check the effective dates of zones against the AIRAC cycle and draw a vertical cross-section of the zones from Bystrc to Tuřany airport over the real terrain. This is a teaching aid, not legal advice: before a flight always check the zones in the DroneMap app and the conditions in the CAA measures of general nature (OOP).

## Goal

Measure the radii of circular zones and compare them with the description, combine the GRID_CTR and GRID_ATZ grids into a map of allowed height, convert flight levels to true altitude from QNH and temperature, check effective dates against the AIRAC cycle and build a vertical cross-section of the zones over the DMR 5G terrain.

## Data

UAS geographical zones as GeoJSON (reference boundaries) from the ŘLP page https://aim.rlp.cz/?lang=en&p=uas-gz, downloaded at run time, except layers larger than the chosen limit; METAR reports of Brno-Tuřany airport (LKTB) for the last 7 days from the Aviation Weather Center (NOAA); terrain elevation from the Digital terrain model of the Czech Republic, 5th generation (DMR 5G, ČÚZK). The conversion of a flight level to true altitude uses the ICAO standard atmosphere with the temperature adjusted to the airport; it is an approximation.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and zones

We load the list of current zones from the ŘLP page and download all layers up to the chosen size limit and both grids. Downloading takes about a minute.

Parameters the student changes:

- `MAX_MB = 20`: largest file to download (MB); both grids are always downloaded

### 2. Does the geometry of zones match the description?

For zones that the description defines by a distance from a point (aerodrome reference point ARP, heliport HRP), we measure the radius in the data: the radius of a circle with the same area as the outer boundary of the feature. The computation runs in metres in UTM 33N coordinates.

Parameters the student changes:

- `CHECK = {"LKR315A": [5500], "LKR315B": [1550], "LKR314D": [5500], "LKR315C": [3000, 1000, 200], "LKR315D": [3000, 1000, 200]}`: layer → radii according to the description on the ŘLP page (m)

**Task 1.** Which layers match the description and which do not? For LKR315A find features clearly smaller and larger than 5500 m and explain what may cause it (look at where they lie). For LKR315B, LKR315C and LKR315D compute by what percentage the radius in the data differs from the description on the ŘLP page. Find in the CAA measure of general nature for the LKR315 zones which distances apply, and decide what a pilot should follow: the description, or the zone boundary in DroneMap.

### 3. A map of allowed height around Brno

The GRID_CTR grid (around controlled airports, 30″ cells) and the GRID_ATZ grid (areas of uncontrolled air traffic, 15″ cells) state in every cell up to what height above ground flight is allowed without further approval. We sample the area every 7.5″, so each point lies inside one cell. Besides that we count how many zones from the ground (GND) overlap at a point.

Parameters the student changes:

- `BBOX = (16.45, 49.10, 16.80, 49.30)`: area (longitude and latitude: west, south, east, north)

**Task 2.** What share of the area may you fly over at 120 m according to the grids, what share only up to 30 m, and where may you not fly at all? Where is the allowed height 0 m, and why there (compare with the position of Tuřany airport, Medlánky airfield and the heliports in the right map)? Does the grey area outside the grid mean you may fly there without restrictions? Remember the large layers we did not download.

### 4. How high is a flight level?

A flight level FL is a pressure altitude in hundreds of feet at the standard pressure of 1013.25 hPa. The true altitude of the level depends on the pressure at the ground (QNH) and on the air temperature: in warm air it lies higher, in cold air lower. We take QNH and temperature from METAR reports for the last 7 days and compute the true altitude of the levels that are the lower limit of LKR320A areas.

Parameters the student changes:

- `STATION = "LKTB"`: the airport whose QNH and temperature we use (METAR reports)
- `FLS = [65, 95]`: flight levels (e.g. lower limits of LKR320A areas)

**Task 3.** By how many metres did the true altitude of FL65 and FL95 change during the week? What affects it more, QNH or temperature? Compute how many metres of height correspond to a change of QNH by 1 hPa. How high above Děvín (about 550 m a.s.l.) does the LKTB4 area (FL65) start in the lowest and the highest case? Why are higher limits in aviation given as flight levels, although their true altitude varies?

### 5. When zones apply: the AIRAC cycle

Changes to aeronautical information are published for the fixed dates of the AIRAC cycle, which follow every 28 days, and ŘLP updates the zone data in line with this cycle. Every zone feature has an effective date (effective_date). We find out which effective dates are AIRAC dates.

**Task 4.** Which effective dates match the AIRAC cycle and which do not? Which layers changed most often, and why those? The OOPUAS-0055 zone has a date outside the cycle: find on the ŘLP page or in DroneMap what zone it is, and explain why it can be created outside the cycle. When is the next AIRAC date, and what do you do before a flight after that date?

### 6. A vertical cross-section of the zones

Along the line from Bystrc to Brno-Tuřany airport we sample the terrain from DMR 5G every 25 m, and for every zone the line crosses we convert the lower and upper limit to altitude (AGL above the terrain, FL as in the standard atmosphere). The black line is the terrain plus the allowed height from the grids.

Parameters the student changes:

- `A = (49.2467, 16.4798)`: start of the profile (Bystrc, Kozí horka)
- `B = (49.1510, 16.6940)`: end of the profile (Brno-Tuřany airport)
- `FLIGHT_AGL = 120`: planned flight height above ground (m)

**Task 5.** Along what percentage of the profile may you fly at 120 m above ground according to the grids, and where does the allowed height drop to zero? Which zones does the profile cross from the ground and which start high above the drone? Set FLIGHT_AGL to 50 m: how does the result change? Why is it not enough for a drone flight to know only the zones the take-off site falls into?

**Extension (optional).** Set BBOX, A, B and STATION to the area around Václav Havel Airport (STATION = "LKPR", end of the profile 50.10° N, 14.26° E) and compare the map of allowed height and the cross-section with Brno.

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- UAS geographical zones: Air Navigation Services of the Czech Republic (ŘLP ČR), AIM, https://aim.rlp.cz/?lang=en&p=uas-gz; zone map: https://dronemap.gov.cz
- Commission Implementing Regulation (EU) 2019/947 on the rules and procedures for the operation of unmanned aircraft, Article 15 (UAS geographical zones).
- Civil Aviation Authority of the Czech Republic: measures of general nature on UAS geographical zones (LKR311 to LKR320), https://www.caa.gov.cz
- METAR reports: NOAA Aviation Weather Center, Data API, https://aviationweather.gov/data/api/
- Terrain elevation: Digital terrain model of the Czech Republic, 5th generation (DMR 5G), © ČÚZK, licence CC BY 4.0, service https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer
- ICAO (1993). *Manual of the ICAO Standard Atmosphere*, Doc 7488, 3rd ed. (pressure altitude).
- ICAO, Annex 15 to the Convention on International Civil Aviation, *Aeronautical Information Services* (the AIRAC system, 28-day cycle).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
