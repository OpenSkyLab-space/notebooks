# Lidar and photogrammetry in a forest: ČÚZK point clouds and models

Description of the notebook for the visual [LiDAR vs photogrammetry under canopy](https://openskylab.space/edu_viz_lidar_canopy.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/lidar_canopy_en.ipynb) · version 1.0 · about 50 min · six tasks

## What the notebook is about

The visual shows why a laser pulse finds the ground even under tree crowns while photogrammetry sees only the surface. Here you check it on real ČÚZK data from the Roztoky forest near Suchdol: ground and surface points from airborne laser scanning and a surface from image matching of aerial photographs.

## Goal

Load and inspect LAZ point clouds, find out which return the ground points come from in the forest and in the open, compute the canopy height model CHM = DSM − DTM from lidar and from photogrammetry, compare them in a profile, find tree tops and explain the differences.

## Data

ČÚZK: DMR 5G (ground points from airborne laser scanning, LAZ) and DMP 1G (surface points, LAZ) for the map sheet Kralupy nad Vltavou 7-7, DMR 5G, DMP 1G and DMP OK (image matching) rasters from the ČÚZK image service; all in S-JTSK (EPSG:5514), heights in Bpv. ČÚZK data are open (CC BY 4.0).

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and point clouds

Installs the libraries Colab lacks (`laspy`, `rasterio`) and downloads the data.

Parameters the student changes:

- `SHEET = "KRAV77"`: SM5 map sheet (sheet names are listed in the ČÚZK Atom service)
- `X0, Y0, X1, Y1 = -744800, -1036000, -743800, -1035300`: window in S-JTSK (m), the Roztoky forest and the Tiché údolí valley

**Task 1.** How many points per m² do DMR 5G and DMP 1G have? The scanner sent many more to the ground: why does ČÚZK publish only selected (key) points, and how might it have selected them? In which month was the scanning done? How do leaves affect how many pulses get through to the ground, and why is lidar for a terrain model ideally flown outside the growing season?

### 2. Which return is the ground?

Every point carries a return number and the number of returns of its pulse. A ground point with return number 2 or more means that part of the pulse had been reflected by a crown and the rest passed through a gap down to the ground. We tell forest from open land by the height of the surface above the ground from the DMP 1G and DMR 5G rasters.

Parameters the student changes:

- `RES = 2.0`: raster pixel size (m)
- `FOREST_H = 5`: surface height above ground from which it counts as "forest" (m)

**Task 2.** What share of ground points in the forest comes from the 2nd or a later return, and what share in the open? Why is it not zero in the open? What would happen to the terrain model under the forest if the scanner recorded only the first return? And why does photogrammetry (SfM) not find the ground under a closed canopy at all?

### 3. CHM from lidar and from photogrammetry

CHM = DSM − DTM. The DTM always comes from lidar (DMR 5G). The DSM comes once from lidar (DMP 1G) and once from image matching of aerial survey photographs (DMP OK), which ČÚZK took later (aerial survey photography usually takes place from spring to summer). Image matching is the same principle as drone photogrammetry.

**Task 3.** Which CHM shows taller vegetation in the forest, and by how much (median, 95th percentile)? Find at least three reasons: the years between acquisitions, leaves in summer and at the time of scanning, how image matching "smooths over" gaps between crowns. Where in the map are the differences largest?

### 4. A profile through the forest

Points of both clouds in a strip along a chosen line, and profiles of the three surfaces.

Parameters the student changes:

- `A_XY = (-744300, -1035950)`: start of the profile (S-JTSK, m)
- `B_XY = (-744300, -1035350)`: end of the profile
- `HALF_W = 5`: half-width of the strip (m)

**Task 4.** Where in the profile is the forest and where the open land? How do the lidar and photogrammetric DSMs differ at the forest edge and in gaps between crowns? Which ground points in the forest come from the 2nd or a later return? Move the profile elsewhere (e.g. across the valley or buildings) and describe what you see.

### 5. Tree tops

We look for a tree top as a local maximum of the CHM within a window of given size that is higher than a chosen limit. We use the photogrammetric DSM at its full resolution of 0.5 m.

Parameters the student changes:

- `WIN = 5`: window size for the local maximum (m)
- `MIN_H = 10`: minimum tree height (m)
- `SUB = (-744600, -1035900, -744300, -1035600)`: a smaller window in the forest (S-JTSK, m)

**Task 5.** How many trees per hectare do you find with a window of 3 m, 5 m and 9 m? Which number is closest to reality if the crowns are about 8–12 m across, and why does a small window overestimate the count? What would happen to the count if you used the lidar CHM with a 2 m pixel?

### 6. What changed between the acquisitions

The difference between the photogrammetric and the lidar CHM shows forest growth, felling and the errors of both methods. ČÚZK gives the accuracy as the total root mean square height error: DMR 5G 0.18 m in open and 0.3 m in forested terrain, DMP 1G 0.4 m for buildings and 0.7 m for vegetation.

Parameters the student changes:

- `CHANGE = 5`: height difference (m) from which we count it as a change

**Task 6.** Is the median difference in the forest larger than the stated accuracy of both models explains? How much would the forest have had to grow over those years, and is that realistic (look up the typical annual height increment of a mature broadleaved forest)? Find places in the map where the forest disappeared (felling, windthrow) or appeared. Why can canopy height not be computed at all from a single photogrammetric DSM without a lidar DTM?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- ČÚZK: Digital Terrain Model of the Czech Republic of the 5th generation (DMR 5G), total root mean square height error 0.18 m in open and 0.3 m in forested terrain; Digital Surface Model of the Czech Republic of the 1st generation (DMP 1G), 0.4 m for buildings and 0.7 m for vegetation; Digital Surface Model from image matching (DMP OK). https://geoportal.cuzk.gov.cz
- LAZ download: ČÚZK Atom service, https://atom.cuzk.cz/DMR5G-SJTSK/DMR5G-SJTSK.xml and https://atom.cuzk.cz/DMP1G-SJTSK/DMP1G-SJTSK.xml; rasters: https://ags.cuzk.cz/arcgis2/rest/services
- ASPRS (2019). *LAS Specification 1.4 – R15* (point classes, return numbers, GPS time).
- White, J. C., Wulder, M. A., Vastaranta, M. et al. (2013). The utility of image-based point clouds for forest inventory: A comparison with airborne laser scanning. *Forests* 4(3), 518–536.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
