# Where sunlight goes, advanced: the diurnal course of surface temperature

Description of the notebook for the visual [Where radiation goes](https://openskylab.space/edu_viz_radiation_balance.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/radiation_balance_pro_en.ipynb) · version 1.0 · about 60 min · five tasks

## What the notebook is about

The advanced version of the radiation balance notebook. Instead of an equilibrium in one hour you heat and cool the surface hour by hour under several days of real weather. Evaporation and heat flow into the ground join absorbed and emitted radiation, so you see why a forest is cooler than a field at noon and why a town stays warm at night.

## Goal

Build solar and longwave radiation from real weather, compute the diurnal course of surface temperature with a force-restore model, split net radiation into sensible heat, evaporation and ground heat flux, and explain the roles of albedo, water availability and thermal inertia.

## Data

Surface albedo from the Sentinel-2 L2A scene `S2B_33UVR_20240721_0_L2A` (21 July 2024, near Roztoky) and ESA WorldCover 2021 classes; hourly weather for Prague from Open-Meteo (last 92 days; the days around the sunniest one are simulated). About 5 MB is downloaded. The surface properties (water availability, thermal inertia) are indicative and the model is simplified: the results show relationships, they are not a forecast of the real temperature.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup and surface albedo

We compute the albedo of four surfaces as in the basic version (Liang 2001, Sentinel-2 bands). We leave water out: water mixes and stores heat at depth, which a single-layer surface model cannot describe.

### 2. Real weather as input

From Open-Meteo we take hourly global radiation, temperature, dew point, wind, cloud cover and pressure. Longwave sky radiation L↓ is computed from the clear-sky emissivity (Brutsaert 1975) and the cloud cover c is added in the form of Crawford and Duchon (1999): ε = ε_clear · (1 − c) + c. The cloud cover comes from the weather model here, not from measurements.

Parameters the student changes:

- `LAT, LON = 50.08, 14.42`: place for the weather (Prague)
- `N_DAYS = 4`: how many days to simulate (the sunniest day is in the middle)

**Task 1.** Find a night with clear and a night with overcast sky in the plots. How much does L↓ differ between them and why? What does that mean for the cooling of the surface at night?

### 3. The surface model

Net radiation Rn = (1 − albedo) · S + ε · L↓ − ε · σ · Ts⁴ splits into sensible heat H = h · (Ts − T_air), evaporation LE = β · (L_v/c_p) · h · (q_sat(Ts) − q_air) and ground heat flux G = Rn − H − LE. The surface temperature Ts is driven by G in the force-restore model (Noilhan and Planton 1989): dTs/dt = C_T · G − (2π/τ) · (Ts − T2), with C_T = 2√(π/τ)/P, where P is thermal inertia. β says how much water the surface has available (0 dry concrete, 1 wet surface).

Parameters the student changes:

- `SURF = pd.DataFrame({`: surface properties (indicative)
- `WIND = 0.75`: wind near the surface as a fraction of the 10 m wind

**Task 2.** Which surface is warmest at noon and which at night? Why is the built-up surface cooler than the field at noon although it hardly evaporates, and the warmest at night? At what time UTC does the surface reach its maximum, and why only after solar noon (in Prague around 11:00 UTC)?

### 4. Where the energy goes during the day

Loads the libraries and downloads the data.

**Task 3.** What percentage of net radiation does the forest spend on evaporation and what percentage the built-up surface? What does the Bowen ratio tell you and why is it below 1 for the forest? Why is the daily sum of G positive, i.e. what happens to the heat in the ground during sunny days?

### 5. Inertia and water

Loads the libraries and downloads the data.

Parameters the student changes:

- `TEST = "built-up"`: surface on which we try the properties

**Task 4.** How do the diurnal temperature range and the time of the maximum change with increasing thermal inertia P? And with water availability β? Which of the two measures would help more against overheating streets during the day and which at night (greenery and watering, or different materials)?

### 6. Comparison with the equilibrium from the basic version

Loads the libraries and downloads the data.

**Task 5.** How many degrees higher is the equilibrium temperature without evaporation and ground heat flux than the model temperature? Which two terms of the balance explain the difference, and for which surface is which more important? Why does a drone thermal camera at noon show a difference between forest and field from which water stress can be inferred?

**Extension (optional).** Change `LAT, LON` to another place (for example a mountain station) or `N_DAYS` to 10 and look at how night minima change under clear and overcast skies. Why are frost hollows coldest on clear and calm nights?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.
- Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Weather: Open-Meteo.com (CC BY 4.0). https://open-meteo.com
- Liang, S. (2001). Narrowband to broadband conversions of land surface albedo I: Algorithms. *Remote Sensing of Environment* 76, 213–238. https://doi.org/10.1016/S0034-4257(00)00205-4
- Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744. https://doi.org/10.1029/WR011i005p00742
- Crawford, T. M., Duchon, C. E. (1999). An improved parameterization for estimating effective atmospheric emissivity for use in calculating daytime downwelling longwave radiation. *Journal of Applied Meteorology* 38, 474–480.
- Noilhan, J., Planton, S. (1989). A simple parameterization of land surface processes for meteorological models. *Monthly Weather Review* 117, 536–549. https://doi.org/10.1175/1520-0493(1989)117<0536:ASPOLS>2.0.CO;2
- Oke, T. R., Mills, G., Christen, A., Voogt, J. A. (2017). *Urban Climates*. Cambridge University Press.

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
