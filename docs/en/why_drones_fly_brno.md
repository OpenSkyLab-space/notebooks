# Why a drone flies: lift, momentum and real air density

Description of the notebook for the visual [Why a drone flies](https://openskylab.space/edu_viz_why_drones_fly.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/why_drones_fly_brno_en.ipynb) · version 1.0 · about 45 min · five tasks

## What the notebook is about

The visual explains airfoil lift, the stall angle, rotor momentum theory and dangerous descent regimes. Here you apply momentum theory to real drones (DJI Mavic 3 Enterprise and Matrice 350 RTK) and to real air density computed from weather in the mountains and in the lowlands.

## Goal

Compute the lift of a thin airfoil and its limit, induced velocity and hover power, show how air density changes endurance, and estimate the descent rate at which the vortex ring state threatens.

## Data

Hourly temperature, pressure and humidity for the last 92 days from Open-Meteo for Brno, Praděd and Gerlachovský štít; mass, propeller diameter, battery and endurance of the drones from DJI data sheets.

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Setup

Loads the libraries and downloads the data.

### 2. Airfoil lift and stall

Thin airfoil theory says the lift coefficient grows linearly with angle of attack: c_L = 2π (α − α₀), where α₀ ≈ −2 · camber / chord (negative for a cambered airfoil). A real airfoil separates at about 12–16° and lift drops. Lift L = ½ ρ v² S c_L.

Parameters the student changes:

- `camber = 0.04`: airfoil camber (fraction of chord; 0 = symmetric, 0.04 = 4 %)
- `alpha_stall = 14`: stall angle (°), roughly 12–16° from measurements of real airfoils

**Task 1.** Why does a cambered airfoil lift even at 0° angle of attack and a symmetric one does not? Set `camber = 0`. At what angle would the wing carry 2.5 kg? Why does thin airfoil theory fail beyond the stall angle and what happens to the flow on the upper surface? (The curve beyond stall is only schematic.)

### 3. Two views of one force

A hovering rotor throws air downwards. Momentum theory: thrust T = ṁ · w, where w = 2 v_i is the air speed far below the rotor and ṁ = ρ A v_i the mass flow through the disc. Hence v_i = √(T / (2 ρ A)). The same thrust is also the pressure difference across the disc: Δp = T / A.

**Task 2.** Check that the ṁ · 2 v_i column gives the same number as the rotor thrust. Why are the pressure difference and the momentum of the air thrown down two descriptions of one force, not two forces that add up? Why does the Matrice 350 have a higher disc loading and induced velocity even though its propellers are much larger?

### 4. Real air density: lowland, mountains, warm and cold

Ideal hover power is P = T^(3/2) / √(2 ρ A), so it grows with 1/√ρ. We compute density from pressure, temperature and humidity over the last 92 days. The printed elevation is that of the Open-Meteo model point; for the peaks it is lower than the real summit (Gerlachovský štít is 2655 m a.s.l.).

Parameters the student changes:

- `FM, eta = 0.60, 0.80`: rotor efficiency (figure of merit) and motor + ESC efficiency

**Task 3.** By what percentage is the air on Gerlachovský štít thinner than in Brno, and how many per cent more power does the drone need to hover? Check that the power ratio is √(ρ_Brno / ρ_peak). What FM and η would make the hover-time estimate match the manufacturer's figure? Why do manufacturers state endurance under ideal conditions?

**Task 4.** Why do large slow propellers need less power to hover than small fast ones? Explain it from P = T · v_i: which of the two quantities does a larger disc change? Why then does a small drone not have huge propellers?

### 5. Descent and the vortex ring state

When a drone descends vertically at a speed comparable to the hover induced velocity v_h, the air the rotor pushes down recirculates back through the disc from above. According to Leishman (2006) the vortex ring region lies roughly between 0.5 v_h and 1.5 v_h (the exact boundary depends on the measurements).

Parameters the student changes:

- `site = "Praděd"`: site (density = 92-day median)

**Task 5.** At what vertical descent speed does the vortex ring state threaten the Mavic and the Matrice? Does the manufacturer's maximum descent speed lie in this region? Why is it safer to descend at an angle or with forward speed, and why is a fast vertical descent close to the ground dangerous when there is no room to recover?

**Extension (optional).** Classmates may have the notebook for other places (Prague, Sněžka and Lomnický štít; Brno, Praděd and Gerlachovský štít; České Budějovice, Plechý and Großglockner). Compare the thinnest air and the Mavic's hover time at the highest site. Why does the model point elevation differ from the real summit elevation, and how does that affect the result?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- DJI Mavic 3 Enterprise (3E): take-off weight 915 g, 9453F propellers (9.4″), 77 Wh battery, max. hover time 38 min, max. descent speed 6 m/s; DJI Matrice 350 RTK: weight with TB65 batteries 6.47 kg, max. take-off 9.2 kg, 21″ propellers, 2 × 263 Wh, max. descent speed 7 m/s (DJI data sheets).
- Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*, 2nd ed. Cambridge University Press (momentum theory, figure of merit, vortex ring state).
- Anderson, J. D. (2017). *Fundamentals of Aerodynamics*, 6th ed. McGraw-Hill (thin airfoil theory).
- Density of moist air via virtual temperature; saturation vapour pressure by the Magnus formula (WMO-No. 8, 2018).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
