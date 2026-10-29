# GNSS under the sky: real satellites, DOP, terrain and Bpv heights

Description of the notebook for the visual [GNSS under the sky](https://openskylab.space/edu_viz_gnss_sky.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/gnss_sky_en.ipynb) · version 1.0 · about 50 min · five tasks

## What the notebook is about

The visual shows how the number and layout of satellites set the DOP, what obstacles and the elevation mask do and why GNSS height is less accurate than position. Here you compute the positions of real GPS, Galileo, GLONASS and BeiDou satellites from broadcast ephemerides, the real horizon in the Vltava valley from the ČÚZK terrain model, and the conversion from ellipsoidal height to Bpv height from survey control points.

## Goal

Draw the real GNSS sky over Suchdol, compute HDOP, VDOP and PDOP over a day, assess the effect of a forest and a deep valley, find the nearest CZEPOS reference station and convert an RTK height to Bpv.

## Data

broadcast ephemerides of GPS, Galileo, GLONASS and BeiDou satellites for one day (RINEX navigation file merged by the IGS, BKG archive, about 1.3 MB); DMR 5G (ČÚZK) for the valley horizon; CZEPOS network stations and densification survey points with both Bpv height and ETRS89 ellipsoidal height from the ČÚZK BodovaPole service.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and satellite orbits

Installs the libraries Colab lacks (`rasterio`) and downloads the data.

Parameters the student changes:

- `DAY = (datetime.now(timezone.utc) - timedelta(days=1)).date()`: day (UTC), default is yesterday; try e.g. date(2026, 9, 1)

### 2. From an ephemeris to a satellite position

Every satellite broadcasts its ephemeris: GPS, Galileo and BeiDou send Keplerian orbital elements with corrections (semi-major axis, eccentricity, inclination, node longitude, argument of latitude and their rates), GLONASS sends position, velocity and acceleration at one instant, from which the orbit is computed by numerical integration. The receiver computes the satellite position from them, and its own position from that. An ephemeris is valid only for a few hours around its reference time, so new ones are broadcast: GPS about every 2 h, BeiDou every hour, GLONASS every 30 min, Galileo even more often. The computation following the GPS interface specification (IS-GPS-200) and the GLONASS ICD gives the position in Earth-fixed coordinates (ECEF).

Parameters the student changes:

- `HOUR = 12`: hour of the check (UTC)
- `RANK = 1`: which further ephemeris to compare with (1 = neighbouring, 3 = three further)
- `LAT, LON = 50.130, 14.373`: site (Suchdol campus)
- `T_SKY = T0 + timedelta(hours=12)`: time of the sky plot (UTC)
- `mask = 10`: elevation mask (°)

**Task 1.** How far from Earth's centre do the satellites of each system orbit? Why does BeiDou also have satellites much higher (geostationary and on inclined geosynchronous orbits)? By how many metres does the position of the same satellite differ between two neighbouring ephemerides? Set `RANK = 3` and then 6 and watch the age of the compared ephemeris and the position difference. Why is the compared ephemeris much older for GPS than for Galileo at the same `RANK`? How does the difference grow with age, and why does it grow faster for GLONASS than for GPS (a broadcast state and integration, or orbital elements with corrections)? Why must ephemerides be broadcast again and again?

### 3. DOP over a day

We compute DOP from geometry: each satellite gives a row of the matrix G with the unit direction vector (east, north, up) and a one for the receiver clock (each system has its own clock offset). Q = (GᵀG)⁻¹, HDOP = √(Q_EE + Q_NN), VDOP = √Q_UU, PDOP = √(Q_EE + Q_NN + Q_UU).

**Task 2.** Why is VDOP larger than HDOP all day? Explain it by where the satellites are in the sky and where they cannot be. How many satellites does a four-system receiver see and how many with GPS only, and how does that affect PDOP? Set the mask to 20° and then 5°.

### 4. Forest to the south or to the north?

A forest edge blocks the sky up to about 35° on one side. The orbits of GPS (inclination 55°) and Galileo (56°) never go beyond 55–56° latitude, so in central Europe there is a region without satellites in the northern sky at medium elevations. Low above the northern horizon, however, we see satellites passing “beyond the pole”. Which side of the forest hurts more is therefore not obvious and depends on the height of the forest.

Parameters the student changes:

- `forest_el = 35`: height of the forest edge above the horizon (°)

**Task 3.** Where is the “hole” without satellites in the sky from step 2, and why? Try forest_el 20°, 35° and 60°: does a forest to the north or to the south hurt more? Does the common advice “there is a hole in the north, so a forest to the north does not matter” hold? Explain the result by the elevations at which the northern sky has the hole and those at which it has satellites “beyond the pole” (the sky plot from step 2 at other hours helps; change `T_SKY`). Where would you set up a base station or survey a ground control point?

### 5. A deep valley: the real horizon from DMR 5G

For a point by the Vltava in Roztoky we compute the horizon elevation in every azimuth from the terrain model and use it to select visible satellites.

Parameters the student changes:

- `VLAT, VLON = 50.1588, 14.3985`: point in the valley (by the Vltava in Roztoky)

**Task 4.** Which directions does the valley block most and why? How high does the horizon reach, and is the valley really “deep” for a four-system GNSS receiver? Try `mask = 20` or a point below a rock face. At which hours of the selected day (UTC) would you survey ground control points in the valley? Why does the terrain model not capture everything that actually blocks or reflects the signal (trees, buildings, rock faces)?

### 6. CZEPOS reference stations

RTK accuracy decreases with distance from the reference station because ionospheric, tropospheric and orbit effects decorrelate. Manufacturers usually state accuracy as 1 cm + 1 ppm (1 mm per km).

### 7. Ellipsoidal height or Bpv?

RTK gives height above the GRS80 ellipsoid (ETRS89). Maps and projects in Czechia use normal height in Bpv. The difference is the height anomaly ζ = h − H. We take densification survey points nearby that have both heights.

Parameters the student changes:

- `half = 15000`: half-width of the surroundings (m)

**Task 5.** What is the height anomaly around Suchdol and how much does it change over 30 km? What happens to a terrain model or to ground control points if you store RTK heights as Bpv without conversion? Why is subtracting one constant for the whole country not enough, and what should you use (quasigeoid model, ČÚZK transformation service)? How far is the nearest CZEPOS station and what RTK error do you expect from that?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Broadcast ephemerides: International GNSS Service (IGS), daily merged navigation file BRDC00IGS_R, BKG archive https://igs.bkg.bund.de/root_ftp/IGS/BRDC/ (IGS data are freely available with attribution). Johnston, G., Riddell, A., Hausler, G. (2017). The International GNSS Service. In *Springer Handbook of Global Navigation Satellite Systems*, 967–982.
- Satellite position computation: IS-GPS-200 (GPS interface, sec. 20.3.3.4.3), Galileo OS SIS ICD, BeiDou ICD B1I (geostationary satellites), GLONASS ICD (integration of motion, appendix J); RINEX 3.05 format (IGS/RTCM).
- Survey control and CZEPOS stations: © ČÚZK, service https://ags.cuzk.cz/arcgis/rest/services/BodovaPole/MapServer (CC BY 4.0).
- DMR 5G: © ČÚZK, CC BY 4.0, https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer
- Hofmann-Wellenhof, B., Lichtenegger, H., Wasle, E. (2008). *GNSS – Global Navigation Satellite Systems*. Springer (DOP, multi-GNSS, RTK).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
