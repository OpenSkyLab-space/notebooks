# Why a drone flies, advanced: power in forward flight, wind, air density and ground effect

Description of the notebook for the visual [Why a drone flies](https://openskylab.space/edu_viz_why_drones_fly.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/why_drones_fly_pro_en.ipynb) · version 1.0 · about 55 min · five tasks

## What the notebook is about

The advanced version of the drone flight notebook. According to the manufacturer the Mavic 3E hovers for 38 minutes but flies for 45 minutes at a constant 32.4 km/h, so it needs less power in forward flight than on the spot. You build a power model from momentum theory, calibrate it to these two figures and use it for the best speed for endurance and range, for the real wind at 120 m over the last three months, for air density and for flight close to the ground.

## Goal

Split drone power into induced, profile and parasite parts, calibrate the model to the manufacturer's figures, find the speed for maximum endurance and maximum range including headwind, evaluate the real wind and air density over 92 days, and estimate ground effect when hovering low.

## Data

Hourly wind at 10 and 120 m, temperature, humidity and pressure for the last 92 days from Open-Meteo for Roztoky (model data, not measurements); mass, propellers, battery and endurance of the Mavic 3E from the DJI data sheet (45 min of flight at a constant 32.4 km/h without wind at sea level until empty, 38 min of hover). The rotor figure of merit FM, the induced losses and the blade tip speed are estimates; the drive efficiency and drag area are calibrated by the notebook, so they also absorb all other losses (electronics, camera, battery).

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup

Loads the libraries and downloads the data.

### 2. The power model and its calibration

We split power into three parts. **Induced** power accelerates air downwards; in forward flight more air passes through the disc, so a smaller induced velocity is enough (Glauert). **Profile** power is used by the drag of the propeller blades and grows slightly with speed. **Parasite** power overcomes the drag of the airframe and grows with the cube of speed. Two unknowns, the drive efficiency η and the equivalent drag area f, are set from the endurance in hover and in flight at 9 m/s.

Parameters the student changes:

- `KAPPA = 1.15`: induced losses relative to an ideal disc (non-uniform inflow, tip losses)
- `FM = 0.60`: rotor efficiency in hover (figure of merit)
- `V_TIP = 90.0`: blade tip speed (m/s), an estimate

**Task 1.** Why does induced power decrease with speed and parasite power increase? At what speed does the drone have the longest endurance and at what speed the greatest range, and why are these not the same speed? Is the equivalent drag area f plausible for a drone the size of a Mavic (estimate the frontal area of the airframe and a drag coefficient of about 1)? Change `FM` to 0.5 and 0.7: how do the calibration and the resulting speeds change?

### 3. Flying against the wind

With a headwind what counts is the energy per kilometre over the ground: power divided by the ground speed (V − wind). The table shows the best airspeed for different headwinds and a comparison with a constant 9 m/s.

**Task 2.** Why should the drone fly faster through the air in a headwind, although power increases? How many times more energy per kilometre does a return against a 6 m/s wind use at the optimum speed, and how many times at a constant 9 m/s? At what wind does the normal mode with 15 m/s stop being enough?

### 4. Real wind over the last three months

From Open-Meteo we download the hourly wind at 10 and 120 m and the weather for 92 days for Roztoky and keep the daytime hours 8–18 h. For each hour we compute the energy per kilometre of a return if all of the wind at 120 m blew against it.

Parameters the student changes:

- `LAT, LON = 50.152, 14.392`: site (Roztoky)
- `WIND_LIMIT = 12.0`: wind resistance according to the manufacturer (m/s)

**Task 3.** How does the wind at 10 m differ from the wind at 120 m, and what does that mean when you judge the wind on the ground before take-off? In what percentage of daytime hours would the wind at 120 m exceed the drone's wind resistance? How many per cent more energy per kilometre does a typical return against the wind use compared with calm air, and what follows for the battery reserve?

### 5. Air density

From pressure, temperature and humidity we compute the air density at Roztoky over the same 92 days and add a density for high mountains. We assume that the rotor figure of merit FM and the drive efficiency η do not change with density.

Parameters the student changes:

- `RHO_MOUNTAIN = 0.90`: density for high mountains (kg/m³), roughly 2600 m a.s.l.

**Task 4.** By how much does hover time shorten in thinner air, and how do the speeds for maximum endurance and maximum range shift? Why does the range in the mountains hardly change although power increases? (Compare how induced and parasite power depend on density.) What would happen if the drone carried a payload in the same mountains that increased its mass by 20 %? Try `m` in the model cell.

### 6. Hovering close to the ground

Close to the ground the wake under the rotor cannot expand freely, the induced velocity drops and the same thrust needs less power. Cheeseman and Bennett (1955) described this as v_IGE / v_OGE = 1 − (R / 4z)², where z is the rotor height above the ground. The relation holds for a single rotor; with a quadcopter the wakes of the four propellers also interact.

**Task 5.** Up to what height above the ground is ground effect noticeable for the Mavic (power saving above 2 %)? Why does the drone "float" just above the ground when landing, and why is this more pronounced in metres for large propellers? Why does ground effect not help you over tall vegetation or over rippled water as much as over concrete?

**Extension (optional).** Adapt the model to the Matrice 350 RTK (mass 6.47 kg, 21″ propellers, battery 2 × 263 Wh). The manufacturer states 55 min of flight without payload; fill in `T_FLIGHT`, estimate `T_HOVER` and watch how endurance falls with payload up to the maximum take-off mass of 9.2 kg.

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- DJI: *Mavic 3 Enterprise, specs* (https://enterprise.dji.com/mavic-3-enterprise/specs): take-off weight 915 g, 77 Wh battery, max. flight time 45 min and max. hover time 38 min without wind, wind resistance 12 m/s, max. speed 15 m/s in normal and 21 m/s in sport mode. The measurement conditions for 45 min (constant 32.4 km/h at sea level until empty) are given in resellers' data sheets.
- Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*, 2nd ed. Cambridge University Press (momentum theory in forward flight, power breakdown, K ≈ 4.65).
- Glauert, H. (1926). A general theory of the autogyro. *ARC R&M* 1111 (induced velocity in forward flight).
- Cheeseman, I. C., Bennett, W. E. (1955). The effect of the ground on a helicopter rotor in forward flight. *ARC R&M* 3021.
- Density of moist air via virtual temperature; saturation vapour pressure by the Magnus formula (WMO-No. 8, 2018).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
