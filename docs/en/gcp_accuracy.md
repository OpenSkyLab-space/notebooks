# Ground control and check points: transformation accuracy on a real survey network

Description of the notebook for the visual [Ground control points and accuracy](https://openskylab.space/edu_viz_gcp_accuracy.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/gcp_accuracy_en.ipynb) · version 1.0 · about 45 min · four tasks

## What the notebook is about

The visual simulates how the layout of ground control points and the georeferencing method affect the accuracy of a drone map. Here you test the same principles on real points of the ČÚZK survey network: every point has GNSS coordinates in ETRS89 as well as coordinates in S-JTSK and an elevation in Bpv. You estimate the conversion between the systems from a few ground control points and measure its accuracy on the other, independent check points. It is the same task as georeferencing an image block, only over tens of kilometres.

## Goal

Estimate a similarity (Helmert) transformation from ground control points, compare residuals on control and check points for different layouts, convert ellipsoidal heights to Bpv, judge how many check points are needed, and show when a more complex transformation does harm.

## Data

ČÚZK trigonometric and densification points around Prague with S-JTSK coordinates, Bpv elevation and ETRS89 coordinates (B, L, ellipsoidal height) from static GNSS observations, BodovaPole service (layer 2).

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and survey points

Installs the libraries Colab lacks (`pyproj`) and downloads the data.

Parameters the student changes:

- `CX, CY = -742000, -1045000`: centre of the area in S-JTSK (EPSG:5514, m), Prague
- `HALF = 30000`: half the side of the area (m)

### 2. Helmert transformation from ground control points

A similarity transformation has 4 parameters (shift x, y, rotation, scale): x' = a·x − b·y + tₓ, y' = b·x + a·y + t_y. We estimate it by least squares from the ground control points and then apply it to all points. A residual on a control point only says how well the transformation adapted to those points. Accuracy is shown by check points that did not enter the computation. RMSE_H = √(mean(Δx² + Δy²)).

Note: S-JTSK has its own distortions and the scale of the Křovák projection changes with latitude, so even the best similarity transformation over such an area is not perfect. ČÚZK therefore converts with a transformation plus a correction grid. For us this is an advantage: there is a real error, unknown in advance, that the check points have to reveal.

Parameters the student changes:

- `LAYOUT = "cluster in a corner"`: one of the layouts above

**Task 1.** For the “cluster in a corner” compare RMSE_H on the control points and on the check points. Why are the residuals on the control points so small, and why can they not be reported as accuracy? Where on the map do the check point residuals grow? Then choose “corners + centre”: why is the residual on the control points now larger than on the check points?

### 3. Comparing layouts, position and height

GNSS gives the ellipsoidal height h, maps in Czechia use the normal height in Bpv: H = h − ζ, where ζ is the height anomaly (about 44–46 m around Prague). If we estimate ζ from the control points as a constant or as a plane, we get heights at the check points. RMSE_V = √(mean ΔH²).

A single control point can only give a shift in position. UTM and S-JTSK, however, are rotated relative to each other and have a different scale, so the error here comes out in kilometres. For an image block from RTK or PPK, rotation and scale are already set by the image positions.

**Task 2.** Which layout is best for position and which for height? Why do points “along a line only” still hold the position but fail to determine the plane of heights (the tilt)? What does a single point in the centre do, and what is it still good for when you have RTK or PPK? Why would mixing up ellipsoidal and normal height be an error of tens of metres in Czechia?

### 4. How many check points?

We estimate accuracy from a limited number of check points, so the RMSE itself is uncertain. We draw 12 or 30 check points at random many times and look at how much the estimate varies.

Parameters the student changes:

- `LAYOUT_N = "10 evenly"`: layout of the control points
- `COUNTS = [5, 12, 30]`: numbers of check points
- `DRAWS = 2000`: number of random draws

**Task 3.** How wide is the range of the RMSE_H estimate (5th to 95th percentile) with 5, 12 and 30 check points? Why does ASPRS require at least 30 check points? Why must the check points be spread over the whole area and not, say, only along a road?

### 5. More complex transformations and few points

The Helmert transformation has 4 parameters, the affine one 6 (two different scales and a shear on top) and a 2nd-degree polynomial 12. More parameters adapt better to the control points. Whether that also helps on the check points depends on whether the real difference between the systems has such a shape, and on how many control points there are. We draw the control points at random and look at the median and at the 90th percentile (an unlucky draw).

Parameters the student changes:

- `N_GCP = [3, 4, 6, 8, 12, 20, 40]`: numbers of control points
- `REPEAT = 200`: number of draws for each number

**Task 4.** Which transformation is best with 3–4 points and which with 40 points? Why is the affine transformation slightly worse than the Helmert one at every count, whereas the 2nd-degree polynomial is clearly better from 8 points on? What does that say about the shape of the real difference between S-JTSK and UTM? Compare the 90th percentile of the polynomial with 6 points with its median: how risky is a model with almost as many parameters as observations? How would you choose the transformation model, or the number of camera self-calibration parameters, in practice?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Survey control: © ČÚZK, service https://ags.cuzk.cz/arcgis/rest/services/BodovaPole/MapServer (CC BY 4.0); point descriptions at https://geoportal.cuzk.gov.cz
- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 1.0 (RMSE_H, RMSE_V, at least 30 check points).
- Sanz-Ablanedo, E., Chandler, J. H., Rodríguez-Pérez, J. R., Ordóñez, C. (2018). Accuracy of Unmanned Aerial Vehicle (UAV) and SfM Photogrammetry Survey as a Function of the Number and Location of Ground Control Points Used. *Remote Sensing* 10(10), 1606.
- Hofmann-Wellenhof, B., Lichtenegger, H., Wasle, E. (2008). *GNSS – Global Navigation Satellite Systems*. Springer (ellipsoidal and normal height, height anomaly).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
