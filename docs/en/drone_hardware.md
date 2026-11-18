# The drone as a measuring instrument: timing, position and angles on a real flight

Description of the notebook for the lab [The drone as a measuring instrument](https://openskylab.space/edu_viz_drone_hardware.html). [Open in Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/drone_hardware_en.ipynb) · version 1.0 · about 45 min · five tasks

## What the notebook is about

The lab shows that a drone is a set of instruments: a GNSS receiver, a barometer, an inertial unit, a gimbal and a camera, each measuring in a slightly different place and at a slightly different moment. Here you test this on a real mapping flight over Bahna (DJI Mavic 2 Pro, no RTK). For each image you have the position and heights recorded by the drone, the body and camera orientation and the camera centre computed by photogrammetry (SfM). From their differences you find how fast the drone flew, how it tilts, how much the position record lags and how much the image is blurred.

## Goal

Determine the strips, speed and image spacing from image positions and times and find missing images, compare the body and camera tilt in strips flown in both directions, separate the position-record delay from the antenna lever arm, compute motion blur and compare the GNSS and barometric heights.

## Data

A metadata table of 253 images of a flight over Bahna on 31 Oct 2025 (EXIF and DJI XMP) with SfM camera centres, in local coordinates (OpenSkyLab, CC BY 4.0).

All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously.

## Step by step

### 1. Data and flight track

The table has one row per image. Positions are in a local plane in metres (east, north), heights above the take-off point. We split the mapping flight (`grid`) into strips by jumps in the north position and give each strip a direction.

### 2. Speed, spacing and missing images

The drone takes images at a regular interval. The speed in each strip is the slope of a line fitted to the east position against time. EXIF time has whole seconds only, hence a line rather than differences of neighbouring images.

**Task 1.** What are the speed, interval and image spacing? Do eastward and westward strips differ? Which images are missing and can you tell from the spacing where in a strip there is a hole?

### 3. Body and camera tilt

A multicopter flies forward by tilting, so that the rotor thrust gets a horizontal component. The gimbal is meant to cancel the body tilt so that the camera points straight down.

**Task 2.** Where does the drone's nose point in eastward and westward strips? What is the body pitch in both directions and why does it have opposite signs? Did the gimbal keep the camera pointing straight down? Why is the tilt not equally large eastwards and westwards?

### 4. Position-record delay and lever arm

The SfM camera centre is determined from the images, the EXIF position from GNSS. If the position is recorded dt after the exposure, it is shifted by v · dt in the flight direction, so it has opposite signs in strips flown back and forth. An antenna offset from the camera (lever arm) gives a shift that does not change with flight direction, because the drone's nose always points the same way. Note: SfM was fitted to the GNSS positions by a similarity transformation, so any constant shift of the whole block vanished and cannot be determined from the data.

Parameters the student changes:

- `SPEED = z_viz("speed", 8.0)`: flight speed in the lab (m/s)
- `DT = z_viz("dt", 0.24)`: position-record delay in the lab (s)
- `LEVER_X = z_viz("lever_x", 0.0)`: antenna ahead of the camera in the lab (m)
- `LEVER_Z = z_viz("lever_z", 0.2)`: antenna above the camera in the lab (m)

**Task 3.** What delay dt follows from the data and how does it agree with the lab? Why is the constant offset almost zero even if the antenna were ahead of the camera? How large a shift does the body tilt cause with the antenna 0.2 m above the camera, and can it be told apart from the delay?

### 5. Motion blur and shutter

During the exposure the drone moves by v · t_exp. If that is more than about half a ground pixel (GSD), the image is visibly blurred. The L1D-20c camera has no mechanical shutter: the sensor is read out row by row (rolling shutter) and during readout the drone moves by v · t_read.

Parameters the student changes:

- `T_EXP = z_viz("t_exp", 0.002)`: exposure time in the lab (s)
- `T_READ = z_viz("t_read", 0.03)`: sensor readout time in the lab (s), 0 = mechanical shutter

**Task 4.** Which exposure times did the camera use and how large is the blur in pixels? What is the longest time that would keep the blur below 0.5 px at this speed and height? What would you change in the flight plan if it were darker under clouds?

### 6. GNSS and barometric height

The drone measures height with a barometer (pressure difference to the take-off point) and with the GNSS receiver. `h_gnss` is the absolute altitude from XMP shifted so that it can be compared with `h_baro`.

**Task 5.** Which sensor keeps the height more stable and why? Does the difference h_gnss − h_baro have a trend in time? What can shift the barometer during the flight?

**Extension (optional).** The extra images (`set == 'extra'`) have a different camera tilt and height. Which of them were not registered in SfM and why?

## Requirements

A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks.

## Data sources and references

- Flight data: OpenSkyLab (2026), metadata of the Bahna flight of 31 Oct 2025 derived from the images and the SfM reconstruction, licence CC BY 4.0, https://github.com/OpenSkyLab-space/notebooks/tree/main/data
- Pix4D: *How to correct for the rolling shutter effect* and *Time offset between GNSS and camera* (Pix4Dmapper documentation).
- Vautherin, J., Rutishauser, S., Schneider-Zapp, K., Choi, H. F., Chovancova, V., Glass, A., Strecha, C. (2016). Photogrammetric accuracy and modeling of rolling shutter cameras. *ISPRS Annals* III-3, 139–146.
- Groves, P. D. (2013). *Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems*, 2nd ed. Artech House (lever arm, sensor synchronisation).

---

Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above).

*This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.*
