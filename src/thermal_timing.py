from _common import OPEN_METEO_HELPER

META = {
    "version": "1.0",
    "minutes": 45,
    "title": {"cs": "Kdy letět s termokamerou: teplota povrchů ze skutečného počasí", "en": "When to fly a thermal camera: surface temperatures from real weather"},
    "visual": {"cs": "Kdy letět s termokamerou", "en": "When to fly a thermal camera"},
    "lead": {
        "cs": "Vizuál ukazuje, jak se voda, louka, asfalt, les a fotovoltaika během dne ohřívají a chladnou a kdy se dva povrchy v termosnímku slijí. Tady stejný typ modelu (energetická bilance povrchu s vedením tepla do hloubky) poženeš skutečným hodinovým počasím za poslední měsíce v Suchdole a hledáš nejlepší čas letu podle úlohy.",
        "en": "The visual shows how water, meadow, asphalt, forest and photovoltaics warm up and cool down during the day, and when two surfaces merge in a thermal image. Here you drive the same kind of model (surface energy balance with heat conduction into the ground) with real hourly weather from the last months at Suchdol and look for the best flight time for a given task.",
    },
    "goal": {
        "cs": "spočítat denní chod teploty povrchů ze skutečného záření, teploty, vlhkosti, oblačnosti a větru, najít časy, kdy se dva povrchy teplotně překříží, porovnat jasný a zatažený den, ukázat vliv větru a emisivity nastavené v kameře a najít hodiny vhodné pro kontrolu fotovoltaiky.",
        "en": "compute the daily course of surface temperatures from real radiation, temperature, humidity, cloud cover and wind, find the times when two surfaces cross over in temperature, compare a clear and an overcast day, show the effect of wind and of the emissivity set in the camera, and find the hours suitable for inspecting photovoltaics.",
    },
    "data": {
        "cs": "hodinová teplota a vlhkost vzduchu, globální záření na vodorovnou i skloněnou plochu, oblačnost, vítr v 10 m a teplota povrchu půdy z Open-Meteo pro kampus v Suchdole, co služba vrátí za posledních 92 dní, obvykle dva až tři měsíce (model počasí, ne měření na místě); tepelné vlastnosti materiálů z literatury.",
        "en": "hourly air temperature and humidity, global radiation on a horizontal and a tilted surface, cloud cover, wind at 10 m and soil surface temperature from Open-Meteo for the Suchdol campus, whatever the service returns for the last 92 days, usually two to three months (weather model, not an on-site measurement); thermal properties of materials from the literature.",
    },
    "sources": {
        "cs": [
            "Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744 (dlouhovlnné záření jasné oblohy).",
            "Crawford, T. M., Duchon, C. E. (1999). An improved parameterization for estimating effective atmospheric emissivity. *Journal of Applied Meteorology* 38, 474–480 (vliv oblačnosti).",
            "Oke, T. R. (1987). *Boundary Layer Climates*, 2. vyd. Routledge (tepelná vodivost a kapacita asfaltu a půdy, albeda).",
            "Maes, W. H. (2025). Practical guidelines for performing UAV mapping flights with snapshot thermal cameras. *Remote Sensing of Environment* (načasování termálních letů).",
            "IEA PVPS Task 13 (2018). *Review on Infrared and Electroluminescence Imaging for PV Field Applications*, Report IEA-PVPS T13-10:2018 (emisivita skla 0,85, ozáření ≥ 600 W/m²).",
            "Přestup tepla prouděním h = 5,7 + 3,8 U (McAdams), tlak nasycených par Magnusovým vzorcem (WMO-No. 8, 2018).",
        ],
        "en": [
            "Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744 (clear-sky long-wave radiation).",
            "Crawford, T. M., Duchon, C. E. (1999). An improved parameterization for estimating effective atmospheric emissivity. *Journal of Applied Meteorology* 38, 474–480 (effect of cloud cover).",
            "Oke, T. R. (1987). *Boundary Layer Climates*, 2nd ed. Routledge (thermal conductivity and heat capacity of asphalt and soil, albedos).",
            "Maes, W. H. (2025). Practical guidelines for performing UAV mapping flights with snapshot thermal cameras. *Remote Sensing of Environment* (timing of thermal flights).",
            "IEA PVPS Task 13 (2018). *Review on Infrared and Electroluminescence Imaging for PV Field Applications*, Report IEA-PVPS T13-10:2018 (glass emissivity 0.85, irradiance ≥ 600 W/m²).",
            "Convective heat transfer h = 5.7 + 3.8 U (McAdams), saturation vapour pressure by the Magnus formula (WMO-No. 8, 2018).",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a skutečné počasí", "## 1. Setup and real weather")),
        ("code", '''
import time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
''' + t(OPEN_METEO_HELPER["cs"], OPEN_METEO_HELPER["en"]) + t('''
LAT, LON = 50.130, 14.373     # ◀ parametr: místo (kampus v Suchdole)
TILT, AZ = 35, 0              # ◀ parametr: sklon a azimut fotovoltaiky (°; azimut 0 = jih, −90 = východ, 90 = západ)

def weather(lat, lon, tilt, az):
    j = open_meteo({"latitude": lat, "longitude": lon, "past_days": 92, "forecast_days": 1,
                    "hourly": "temperature_2m,relative_humidity_2m,shortwave_radiation,global_tilted_irradiance,cloud_cover,wind_speed_10m,soil_temperature_0cm",
                    "tilt": tilt, "azimuth": az, "timezone": "Europe/Prague", "wind_speed_unit": "ms"})
    w = pd.DataFrame(j["hourly"]); w["time"] = pd.to_datetime(w.time)
    return w.set_index("time").dropna()

w = weather(LAT, LON, TILT, AZ)
days = w.shortwave_radiation.resample("D").sum() / 1000           # kWh/m² za den
days = days.iloc[14:-1]                                          # prvních 14 dní je rozběh modelu, poslední den je neúplný
SUNNY, CLOUDY = days.idxmax().date(), days.idxmin().date()
print(f"počasí {w.index[0]:%d. %m.} až {w.index[-1]:%d. %m. %Y}, {len(w)} hodin")
print(f"nejslunečnější den {SUNNY} ({days.max():.1f} kWh/m²), nejzataženější {CLOUDY} ({days.min():.1f} kWh/m²)")
w[["temperature_2m", "shortwave_radiation", "cloud_cover", "wind_speed_10m"]].plot(subplots=True, figsize=(10, 6), legend=True); plt.show()
''', '''
LAT, LON = 50.130, 14.373     # ◀ parameter: site (Suchdol campus)
TILT, AZ = 35, 0              # ◀ parameter: tilt and azimuth of the PV panels (°; azimuth 0 = south, −90 = east, 90 = west)

def weather(lat, lon, tilt, az):
    j = open_meteo({"latitude": lat, "longitude": lon, "past_days": 92, "forecast_days": 1,
                    "hourly": "temperature_2m,relative_humidity_2m,shortwave_radiation,global_tilted_irradiance,cloud_cover,wind_speed_10m,soil_temperature_0cm",
                    "tilt": tilt, "azimuth": az, "timezone": "Europe/Prague", "wind_speed_unit": "ms"})
    w = pd.DataFrame(j["hourly"]); w["time"] = pd.to_datetime(w.time)
    return w.set_index("time").dropna()

w = weather(LAT, LON, TILT, AZ)
days = w.shortwave_radiation.resample("D").sum() / 1000           # kWh/m² per day
days = days.iloc[14:-1]                                          # the first 14 days are model spin-up, the last day is incomplete
SUNNY, CLOUDY = days.idxmax().date(), days.idxmin().date()
print(f"weather {w.index[0]:%d %b} to {w.index[-1]:%d %b %Y}, {len(w)} hours")
print(f"sunniest day {SUNNY} ({days.max():.1f} kWh/m²), most overcast {CLOUDY} ({days.min():.1f} kWh/m²)")
w[["temperature_2m", "shortwave_radiation", "cloud_cover", "wind_speed_10m"]].plot(subplots=True, figsize=(10, 6), legend=True); plt.show()
''')),
        ("md", t(
            "## 2. Model povrchu a jeden jasný den\n\n"
            "Pro každý povrch se každou minutu řeší energetická bilance **Rn = H + LE + G**:\n\n"
            "- Rn: pohlcené sluneční záření (1 − albedo) · S plus dlouhovlnná bilance ε (L↓ − σ T⁴). L↓ z oblohy je z teploty a vlhkosti vzduchu (Brutsaert 1975) a z oblačnosti (Crawford a Duchon 1999).\n"
            "- H: citelné teplo do vzduchu h · (T − Tₐ), h = 5,7 + 3,8 U, kde U je vítr ve 2 m (z větru v 10 m logaritmickým profilem, ×0,75).\n"
            "- LE: výpar ρ L (q*(T) − qₐ) / (rₐ + r_s); odpor průduchů r_s je u louky 70 s/m, u lesa 100 s/m, voda se vypařuje volně, asfalt a panel vůbec.\n"
            "- G: teplo do hloubky. Asfalt a půda mají 12 vrstev do 1 m, rybník je promíchaná vrstva vody 1 m, koruny lesa a FV panel jsou tenká vrstva bez vedení do země.\n\n"
            "Sluneční záření, teplota, vlhkost, oblačnost a vítr jsou skutečné hodinové hodnoty z Open-Meteo. Model běží od začátku období, prvních 14 dní slouží k rozběhu.",
            "## 2. The surface model and one clear day\n\n"
            "For every surface the energy balance **Rn = H + LE + G** is solved every minute:\n\n"
            "- Rn: absorbed solar radiation (1 − albedo) · S plus the long-wave balance ε (L↓ − σ T⁴). The sky L↓ comes from air temperature and humidity (Brutsaert 1975) and from cloud cover (Crawford and Duchon 1999).\n"
            "- H: sensible heat to the air h · (T − Tₐ), h = 5.7 + 3.8 U, where U is the wind at 2 m (from the 10 m wind by a logarithmic profile, ×0.75).\n"
            "- LE: evaporation ρ L (q*(T) − qₐ) / (rₐ + r_s); the stomatal resistance r_s is 70 s/m for the meadow and 100 s/m for the forest, water evaporates freely, asphalt and the panel not at all.\n"
            "- G: heat into the ground. Asphalt and soil have 12 layers down to 1 m, the pond is a mixed water layer of 1 m, the forest canopy and the PV panel are a thin layer with no conduction into the ground.\n\n"
            "Solar radiation, temperature, humidity, cloud cover and wind are real hourly values from Open-Meteo. The model runs from the start of the period; the first 14 days are spin-up.")),
        ("code", t('''
SIG = 5.670e-8
# albedo, emisivita, tepelná vodivost k (W/m/K), objemová tepelná kapacita C (J/m³/K), odpor průduchů r_s (s/m; inf = bez výparu),
# node = tepelná kapacita jediné vrstvy (J/m²/K) u povrchů bez vedení do hloubky, rough = násobek přestupu tepla (drsnost), sides = ochlazování z obou stran
SURF = {
    "voda":     dict(alb=0.06, eps=0.99, k=0.0,  C=0.0,    rs=0.0,    node=4.18e6 * 1.0),
    "louka":    dict(alb=0.20, eps=0.98, k=1.2,  C=2.5e6,  rs=70.0),
    "asfalt":   dict(alb=0.08, eps=0.95, k=0.75, C=1.94e6, rs=np.inf),
    "les":      dict(alb=0.12, eps=0.98, k=0.0,  C=0.0,    rs=100.0,  node=3.0e4, rough=3),
    "FV panel": dict(alb=0.30, eps=0.85, k=0.0,  C=0.0,    rs=np.inf, node=1.5e4, sides=2, tilted=1),
}

def qsat(T):
    """Měrná vlhkost nasyceného vzduchu (kg/kg) při teplotě T v kelvinech (Magnus, 1013 hPa)."""
    return 0.622 * 610.94 * np.exp(17.625 * (T - 273.15) / (T - 30.11)) / 101325

def simulate(w, surf=SURF, wind_factor=1.0, dt=60, nl=12, depth=1.0):
    t = (w.index - w.index[0]).total_seconds().values
    ts = np.arange(0, t[-1], dt)
    Ta = np.interp(ts, t, w.temperature_2m.values) + 273.15
    RH = np.interp(ts, t, w.relative_humidity_2m.values) / 100
    S = np.interp(ts, t - 1800, w.shortwave_radiation.values)          # záření je průměr za předchozí hodinu
    S_tilt = np.interp(ts, t - 1800, w.global_tilted_irradiance.values)
    cc = np.interp(ts, t, w.cloud_cover.values) / 100
    U = np.maximum(np.interp(ts, t, w.wind_speed_10m.values) * 0.75 * wind_factor, 0.3)
    e = RH * 610.94 * np.exp(17.625 * (Ta - 273.15) / (Ta - 30.11))
    eps_sky = 1.24 * (e / 100 / Ta) ** (1 / 7) * (1 - cc) + cc
    Ld = eps_sky * SIG * Ta ** 4
    qa = RH * qsat(Ta)
    names = list(surf)
    p = {k: np.array([surf[n].get(k, d) for n in names], float) for k, d in
         [("alb", 0), ("eps", 1), ("k", 0), ("C", 0), ("rs", np.inf), ("node", 0), ("rough", 1), ("sides", 1), ("tilted", 0)]}
    r = 1.0
    while 0.01 * (r ** nl - 1) / (r - 1 + 1e-12) < depth: r += 0.001
    dz = 0.01 * r ** np.arange(nl)                                      # vrstvy od 1 cm, směrem dolů tlustší
    single = p["node"] > 0
    cap = np.outer(p["C"], dz); cap[single, 0] = p["node"][single]; cap[single, 1:] = 1
    kk = np.outer(p["k"], np.ones(nl - 1)) / ((dz[1:] + dz[:-1]) / 2)
    T = np.full((len(names), nl), Ta[: int(3 * 86400 / dt)].mean())
    out = np.empty((len(ts), len(names)))
    rho, cp, L = 1.2, 1005, 2.45e6
    for i in range(len(ts)):
        Ts = T[:, 0]
        h = (5.7 + 3.8 * U[i]) * p["rough"]
        sw = np.where(p["tilted"] > 0, S_tilt[i], S[i])
        Rn = (1 - p["alb"]) * sw + p["eps"] * (Ld[i] - SIG * Ts ** 4) + (p["sides"] - 1) * p["eps"] * SIG * (Ta[i] ** 4 - Ts ** 4)
        H = h * p["sides"] * (Ts - Ta[i])
        LE = np.where(np.isinf(p["rs"]), 0.0, rho * L * (qsat(Ts) - qa[i]) / (rho * cp / h + np.where(np.isinf(p["rs"]), 0, p["rs"])))
        flux = kk * (T[:, :-1] - T[:, 1:])
        dT = np.zeros_like(T)
        dT[:, 0] = Rn - H - LE - flux[:, 0]
        dT[:, 1:-1] = flux[:, :-1] - flux[:, 1:]
        dT[:, -1] = flux[:, -1]
        T += dt * dT / cap
        out[i] = T[:, 0]
    idx = w.index[0] + pd.to_timedelta(ts, "s")
    res = pd.DataFrame(out - 273.15, index=idx, columns=names)
    res.attrs["Ld"] = pd.Series(Ld, index=idx); res.attrs["Ta"] = pd.Series(Ta - 273.15, index=idx)
    return res

def crossings(a, b):
    """Časy, kdy rozdíl a − b mění znaménko (lineární interpolace mezi minutami)."""
    d = (a - b).values; i = np.where(np.sign(d[:-1]) * np.sign(d[1:]) < 0)[0]
    return [a.index[k] + (a.index[k + 1] - a.index[k]) * (d[k] / (d[k] - d[k + 1])) for k in i]

T = simulate(w)
DAY = SUNNY                   # ◀ parametr: den, např. "2026-09-10"; výchozí je nejslunečnější den
A, B = "voda", "louka"        # ◀ parametr: dvojice povrchů
d = T.loc[str(DAY)]
ax = d.plot(figsize=(10, 4.5))
T.attrs["Ta"].loc[str(DAY)].plot(ax=ax, color="k", ls="--", label="vzduch 2 m")
w.soil_temperature_0cm.loc[str(DAY)].plot(ax=ax, color="gray", ls=":", marker=".", label="povrch půdy podle Open-Meteo")
for c in crossings(d[A], d[B]):
    ax.axvline(c, color="gray", lw=0.8); print(f"{A} × {B}: překřížení v {c:%H:%M}")
ax.set_ylabel("teplota povrchu (°C)"); ax.set_xlabel(""); ax.set_title(f"{DAY}, Suchdol"); ax.legend(ncol=3, fontsize=8); plt.show()
print(d.resample("h").mean().iloc[[2, 5, 8, 11, 13, 16, 19, 22]].round(1))
''', '''
SIG = 5.670e-8
# albedo, emissivity, thermal conductivity k (W/m/K), volumetric heat capacity C (J/m³/K), stomatal resistance r_s (s/m; inf = no evaporation),
# node = heat capacity of a single layer (J/m²/K) for surfaces with no conduction into the ground, rough = multiple of heat transfer (roughness), sides = cooled from both sides
SURF = {
    "water":     dict(alb=0.06, eps=0.99, k=0.0,  C=0.0,    rs=0.0,    node=4.18e6 * 1.0),
    "meadow":    dict(alb=0.20, eps=0.98, k=1.2,  C=2.5e6,  rs=70.0),
    "asphalt":   dict(alb=0.08, eps=0.95, k=0.75, C=1.94e6, rs=np.inf),
    "forest":    dict(alb=0.12, eps=0.98, k=0.0,  C=0.0,    rs=100.0,  node=3.0e4, rough=3),
    "PV panel":  dict(alb=0.30, eps=0.85, k=0.0,  C=0.0,    rs=np.inf, node=1.5e4, sides=2, tilted=1),
}

def qsat(T):
    """Saturation specific humidity (kg/kg) at temperature T in kelvin (Magnus, 1013 hPa)."""
    return 0.622 * 610.94 * np.exp(17.625 * (T - 273.15) / (T - 30.11)) / 101325

def simulate(w, surf=SURF, wind_factor=1.0, dt=60, nl=12, depth=1.0):
    t = (w.index - w.index[0]).total_seconds().values
    ts = np.arange(0, t[-1], dt)
    Ta = np.interp(ts, t, w.temperature_2m.values) + 273.15
    RH = np.interp(ts, t, w.relative_humidity_2m.values) / 100
    S = np.interp(ts, t - 1800, w.shortwave_radiation.values)          # radiation is the mean over the preceding hour
    S_tilt = np.interp(ts, t - 1800, w.global_tilted_irradiance.values)
    cc = np.interp(ts, t, w.cloud_cover.values) / 100
    U = np.maximum(np.interp(ts, t, w.wind_speed_10m.values) * 0.75 * wind_factor, 0.3)
    e = RH * 610.94 * np.exp(17.625 * (Ta - 273.15) / (Ta - 30.11))
    eps_sky = 1.24 * (e / 100 / Ta) ** (1 / 7) * (1 - cc) + cc
    Ld = eps_sky * SIG * Ta ** 4
    qa = RH * qsat(Ta)
    names = list(surf)
    p = {k: np.array([surf[n].get(k, d) for n in names], float) for k, d in
         [("alb", 0), ("eps", 1), ("k", 0), ("C", 0), ("rs", np.inf), ("node", 0), ("rough", 1), ("sides", 1), ("tilted", 0)]}
    r = 1.0
    while 0.01 * (r ** nl - 1) / (r - 1 + 1e-12) < depth: r += 0.001
    dz = 0.01 * r ** np.arange(nl)                                      # layers from 1 cm, thicker with depth
    single = p["node"] > 0
    cap = np.outer(p["C"], dz); cap[single, 0] = p["node"][single]; cap[single, 1:] = 1
    kk = np.outer(p["k"], np.ones(nl - 1)) / ((dz[1:] + dz[:-1]) / 2)
    T = np.full((len(names), nl), Ta[: int(3 * 86400 / dt)].mean())
    out = np.empty((len(ts), len(names)))
    rho, cp, L = 1.2, 1005, 2.45e6
    for i in range(len(ts)):
        Ts = T[:, 0]
        h = (5.7 + 3.8 * U[i]) * p["rough"]
        sw = np.where(p["tilted"] > 0, S_tilt[i], S[i])
        Rn = (1 - p["alb"]) * sw + p["eps"] * (Ld[i] - SIG * Ts ** 4) + (p["sides"] - 1) * p["eps"] * SIG * (Ta[i] ** 4 - Ts ** 4)
        H = h * p["sides"] * (Ts - Ta[i])
        LE = np.where(np.isinf(p["rs"]), 0.0, rho * L * (qsat(Ts) - qa[i]) / (rho * cp / h + np.where(np.isinf(p["rs"]), 0, p["rs"])))
        flux = kk * (T[:, :-1] - T[:, 1:])
        dT = np.zeros_like(T)
        dT[:, 0] = Rn - H - LE - flux[:, 0]
        dT[:, 1:-1] = flux[:, :-1] - flux[:, 1:]
        dT[:, -1] = flux[:, -1]
        T += dt * dT / cap
        out[i] = T[:, 0]
    idx = w.index[0] + pd.to_timedelta(ts, "s")
    res = pd.DataFrame(out - 273.15, index=idx, columns=names)
    res.attrs["Ld"] = pd.Series(Ld, index=idx); res.attrs["Ta"] = pd.Series(Ta - 273.15, index=idx)
    return res

def crossings(a, b):
    """Times at which the difference a − b changes sign (linear interpolation between minutes)."""
    d = (a - b).values; i = np.where(np.sign(d[:-1]) * np.sign(d[1:]) < 0)[0]
    return [a.index[k] + (a.index[k + 1] - a.index[k]) * (d[k] / (d[k] - d[k + 1])) for k in i]

T = simulate(w)
DAY = SUNNY                   # ◀ parameter: day, e.g. "2026-09-10"; the default is the sunniest day
A, B = "water", "meadow"      # ◀ parameter: pair of surfaces
d = T.loc[str(DAY)]
ax = d.plot(figsize=(10, 4.5))
T.attrs["Ta"].loc[str(DAY)].plot(ax=ax, color="k", ls="--", label="air 2 m")
w.soil_temperature_0cm.loc[str(DAY)].plot(ax=ax, color="gray", ls=":", marker=".", label="soil surface from Open-Meteo")
for c in crossings(d[A], d[B]):
    ax.axvline(c, color="gray", lw=0.8); print(f"{A} × {B}: crossover at {c:%H:%M}")
ax.set_ylabel("surface temperature (°C)"); ax.set_xlabel(""); ax.set_title(f"{DAY}, Suchdol"); ax.legend(ncol=3, fontsize=8); plt.show()
print(d.resample("h").mean().iloc[[2, 5, 8, 11, 13, 16, 19, 22]].round(1))
''')),
        ("task", t(
            "Odečti časy obou překřížení vody a louky. Proč je voda v noci teplejší než louka a v poledne chladnější? Porovnej modelovanou louku s teplotou povrchu půdy z Open-Meteo (tečkovaně): kde se liší nejvíc a čím to může být (je to taky model, ne měření)? Zkus dvojici asfalt × les.",
            "Read off the times of both crossovers of water and meadow. Why is water warmer than the meadow at night and colder at noon? Compare the modelled meadow with the soil surface temperature from Open-Meteo (dotted): where do they differ most and why might that be (it is a model too, not a measurement)? Try the pair asphalt × forest.")),
        ("md", t(
            "## 3. Jasno, nebo zataženo?\n\nPorovnáme nejslunečnější a nejzataženější den ze stažených dat. Amplituda je rozdíl mezi denním maximem a minimem teploty povrchu.",
            "## 3. Clear or overcast?\n\nWe compare the sunniest and the most overcast day in the downloaded data. The amplitude is the difference between the daily maximum and minimum of surface temperature.")),
        ("code", t('''
DAYS = [SUNNY, CLOUDY]        # ◀ parametr: dny k porovnání (můžeš přidat třetí, např. "2026-09-20")
rows = {}
for day in DAYS:
    d = T.loc[str(day)]
    rows[f"{day}: amplituda"] = d.max() - d.min()
    rows[f"{day}: voda − louka ve 3:00"] = d.between_time("02:55", "03:05").mean()["voda"] - d.between_time("02:55", "03:05").mean()["louka"]
    print(f"{day}: záření {days.loc[pd.Timestamp(day)]:.1f} kWh/m², oblačnost {w.cloud_cover.loc[str(day)].mean():.0f} %, vítr {w.wind_speed_10m.loc[str(day)].mean():.1f} m/s")
print(pd.DataFrame({k: v for k, v in rows.items() if "amplituda" in k}).round(1))
print({k: round(float(v), 1) for k, v in rows.items() if "louka" in k})
fig, ax = plt.subplots(1, len(DAYS), figsize=(11, 3.5), sharey=True)
for a, day in zip(np.atleast_1d(ax), DAYS):
    T.loc[str(day)].plot(ax=a, legend=False); a.set_title(str(day))
np.atleast_1d(ax)[0].set_ylabel("°C"); np.atleast_1d(ax)[-1].legend(fontsize=8); plt.show()
''', '''
DAYS = [SUNNY, CLOUDY]        # ◀ parameter: days to compare (you can add a third one, e.g. "2026-09-20")
rows = {}
for day in DAYS:
    d = T.loc[str(day)]
    rows[f"{day}: amplitude"] = d.max() - d.min()
    rows[f"{day}: water − meadow at 3:00"] = d.between_time("02:55", "03:05").mean()["water"] - d.between_time("02:55", "03:05").mean()["meadow"]
    print(f"{day}: radiation {days.loc[pd.Timestamp(day)]:.1f} kWh/m², cloud cover {w.cloud_cover.loc[str(day)].mean():.0f} %, wind {w.wind_speed_10m.loc[str(day)].mean():.1f} m/s")
print(pd.DataFrame({k: v for k, v in rows.items() if "amplitude" in k}).round(1))
print({k: round(float(v), 1) for k, v in rows.items() if "meadow" in k})
fig, ax = plt.subplots(1, len(DAYS), figsize=(11, 3.5), sharey=True)
for a, day in zip(np.atleast_1d(ax), DAYS):
    T.loc[str(day)].plot(ax=a, legend=False); a.set_title(str(day))
np.atleast_1d(ax)[0].set_ylabel("°C"); np.atleast_1d(ax)[-1].legend(fontsize=8); plt.show()
''')),
        ("task", t(
            "O kolik se v zatažený den zmenšila amplituda asfaltu a vody? Co se stalo s rozdílem voda − louka v noci? Vysvětli roli slunečního záření ve dne a dlouhovlnného záření oblačnosti v noci.",
            "By how much did the amplitude of asphalt and water shrink on the overcast day? What happened to the water − meadow difference at night? Explain the role of solar radiation during the day and of long-wave radiation from clouds at night.")),
        ("md", t(
            "## 4. Kalendář kontrastu: kdy letět\n\nPro každý den a hodinu spočítáme rozdíl teplot dvojice povrchů. Bílá místa jsou překřížení, kdy se povrchy v termosnímku slijí.",
            "## 4. Contrast calendar: when to fly\n\nFor every day and hour we compute the temperature difference of a pair of surfaces. White areas are crossovers, when the surfaces merge in a thermal image.")),
        ("code", t('''
A, B = "voda", "louka"        # ◀ parametr: dvojice povrchů
MIN_DT = 3                    # ◀ parametr: kontrast, který ještě v termosnímku spolehlivě rozlišíš (K)
h = (T[A] - T[B]).iloc[14 * 1440:].resample("h").mean()
grid = h.to_frame("d").assign(den=h.index.date, hod=h.index.hour).pivot(index="hod", columns="den", values="d")
lim = np.nanpercentile(np.abs(grid.values), 98)
fig, ax = plt.subplots(figsize=(11, 4))
im = ax.pcolormesh(range(grid.shape[1] + 1), range(25), grid.values, cmap="RdBu_r", vmin=-lim, vmax=lim)
ax.set_yticks(range(0, 25, 3)); ax.set_ylabel("hodina (místní čas)")
ax.set_xticks(range(0, grid.shape[1], 7)); ax.set_xticklabels([str(c)[5:] for c in grid.columns[::7]], rotation=45)
plt.colorbar(im, label=f"{A} − {B} (K)"); plt.show()
ok = (grid.abs() >= MIN_DT).mean(axis=1) * 100
print(f"podíl dní, kdy je |{A} − {B}| ≥ {MIN_DT} K, podle hodiny (%):"); print(ok.round(0).to_frame("%").T.to_string())
''', '''
A, B = "water", "meadow"      # ◀ parameter: pair of surfaces
MIN_DT = 3                    # ◀ parameter: contrast you can still reliably tell apart in a thermal image (K)
h = (T[A] - T[B]).iloc[14 * 1440:].resample("h").mean()
grid = h.to_frame("d").assign(day=h.index.date, hour=h.index.hour).pivot(index="hour", columns="day", values="d")
lim = np.nanpercentile(np.abs(grid.values), 98)
fig, ax = plt.subplots(figsize=(11, 4))
im = ax.pcolormesh(range(grid.shape[1] + 1), range(25), grid.values, cmap="RdBu_r", vmin=-lim, vmax=lim)
ax.set_yticks(range(0, 25, 3)); ax.set_ylabel("hour (local time)")
ax.set_xticks(range(0, grid.shape[1], 7)); ax.set_xticklabels([str(c)[5:] for c in grid.columns[::7]], rotation=45)
plt.colorbar(im, label=f"{A} − {B} (K)"); plt.show()
ok = (grid.abs() >= MIN_DT).mean(axis=1) * 100
print(f"share of days with |{A} − {B}| ≥ {MIN_DT} K, by hour (%):"); print(ok.round(0).to_frame("%").T.to_string())
''')),
        ("task", t(
            "Ve kterých hodinách je kontrast vody a louky spolehlivě velký a ve kterých se povrchy slévají? Jak se překřížení posouvají od léta k podzimu a proč? Hledáš vlhká místa v louce (dvojice louka × voda): kdy bys letěl a proč spíš ráno než v poledne?",
            "In which hours is the contrast between water and meadow reliably large, and in which do the surfaces merge? How do the crossovers shift from summer to autumn and why? You are looking for wet spots in a meadow (pair meadow × water): when would you fly and why rather in the morning than at noon?")),
        ("md", t(
            "## 5. Vítr\n\nStejné počasí spočítáme ještě jednou se slabším a silnějším větrem (vítr vynásobíme). Ostatní veličiny zůstanou skutečné.",
            "## 5. Wind\n\nWe compute the same weather again with weaker and stronger wind (we multiply the wind). Everything else stays real.")),
        ("code", t('''
FACTORS = [0.5, 1, 2, 4]      # ◀ parametr: násobky skutečného větru
DAY_W = SUNNY                 # ◀ parametr: den
tab = {}
for f in FACTORS:
    d = simulate(w, wind_factor=f).loc[str(DAY_W)]
    tab[f"vítr ×{f}"] = {"asfalt max": d["asfalt"].max(), "louka min": d["louka"].min(), "asfalt − louka ve 13:00": (d["asfalt"] - d["louka"]).between_time("12:55", "13:05").mean()}
print(f"{DAY_W}: skutečný vítr v 10 m průměrně {w.wind_speed_10m.loc[str(DAY_W)].mean():.1f} m/s")
pd.DataFrame(tab).round(1)
''', '''
FACTORS = [0.5, 1, 2, 4]      # ◀ parameter: multiples of the real wind
DAY_W = SUNNY                 # ◀ parameter: day
tab = {}
for f in FACTORS:
    d = simulate(w, wind_factor=f).loc[str(DAY_W)]
    tab[f"wind ×{f}"] = {"asphalt max": d["asphalt"].max(), "meadow min": d["meadow"].min(), "asphalt − meadow at 13:00": (d["asphalt"] - d["meadow"]).between_time("12:55", "13:05").mean()}
print(f"{DAY_W}: real wind at 10 m averaged {w.wind_speed_10m.loc[str(DAY_W)].mean():.1f} m/s")
pd.DataFrame(tab).round(1)
''')),
        ("task", t(
            "Jak se se silnějším větrem změní polední maximum asfaltu, ranní minimum louky a kontrast asfalt − louka? Proč vítr kontrasty v termosnímku zmenšuje? Jaký limit větru bys pro termální let doporučil?",
            "How do the noon maximum of asphalt, the morning minimum of the meadow and the asphalt − meadow contrast change with stronger wind? Why does wind reduce contrasts in a thermal image? What wind limit would you recommend for a thermal flight?")),
        ("md", t(
            "## 6. Emisivita v kameře a fotovoltaika\n\n"
            "Kamera měří vyzařování W = ε σ T⁴ + (1 − ε) σ T_odr⁴, kde druhý člen je odražené okolí. Teplotu z něj počítá s emisivitou ε_k a odraženou teplotou T_odr, které nastavíš v kameře. Zjednodušení: počítáme v celém spektru, ne jen v pásmu 8–14 µm, a odražené okolí bereme jako oblohu.\n\n"
            "Pro kontrolu FV elektráren se doporučuje ozáření panelu aspoň 600 W/m² (IEA PVPS). Ozáření skloněné plochy máme z Open-Meteo.",
            "## 6. Emissivity in the camera and photovoltaics\n\n"
            "The camera measures the exitance W = ε σ T⁴ + (1 − ε) σ T_refl⁴, where the second term is the reflected surroundings. It computes temperature using the emissivity ε_c and the reflected temperature T_refl set in the camera. Simplification: we compute over the whole spectrum, not only the 8–14 µm band, and take the reflected surroundings to be the sky.\n\n"
            "For inspecting PV plants an irradiance of at least 600 W/m² on the panel is recommended (IEA PVPS). The irradiance of the tilted surface comes from Open-Meteo.")),
        ("code", t('''
EPS_CAM = 1.00                # ◀ parametr: emisivita nastavená v kameře (zkus 0,95 a 0,85)
T_REFL = 20.0                 # ◀ parametr: odražená teplota nastavená v kameře (°C)
HOURS = ["05:00", "13:00"]    # ◀ parametr: časy snímků
DAY_E = SUNNY                 # ◀ parametr: den
eps = pd.Series({n: v["eps"] for n, v in SURF.items()})
rows = {}
for hh in HOURS:
    tt = pd.Timestamp(f"{DAY_E} {hh}")
    Tk = T.loc[tt] + 273.15; Ld = T.attrs["Ld"].loc[tt]
    W = eps * SIG * Tk ** 4 + (1 - eps) * Ld
    Trad = ((W - (1 - EPS_CAM) * SIG * (T_REFL + 273.15) ** 4) / (EPS_CAM * SIG)) ** 0.25 - 273.15
    rows[f"{hh} skutečná"] = T.loc[tt]; rows[f"{hh} kamera"] = Trad; rows[f"{hh} chyba"] = Trad - T.loc[tt]
print(f"{DAY_E}, emisivita v kameře {EPS_CAM}, odražená teplota {T_REFL} °C")
print(pd.DataFrame(rows).round(1))

THRESH = 600                  # ◀ parametr: minimální ozáření panelu pro kontrolu FV (W/m²)
g = w.global_tilted_irradiance
ok = (g >= THRESH).groupby([g.index.to_period("M").rename("měsíc"), g.index.hour.rename("hodina")]).sum().unstack(fill_value=0)
print(f"\\nPočet hodin s ozářením panelu (sklon {TILT}°, azimut {AZ}°) ≥ {THRESH} W/m² podle měsíce a hodiny:")
print(ok.loc[:, ok.sum() > 0].to_string())
''', '''
EPS_CAM = 1.00                # ◀ parameter: emissivity set in the camera (try 0.95 and 0.85)
T_REFL = 20.0                 # ◀ parameter: reflected temperature set in the camera (°C)
HOURS = ["05:00", "13:00"]    # ◀ parameter: times of the images
DAY_E = SUNNY                 # ◀ parameter: day
eps = pd.Series({n: v["eps"] for n, v in SURF.items()})
rows = {}
for hh in HOURS:
    tt = pd.Timestamp(f"{DAY_E} {hh}")
    Tk = T.loc[tt] + 273.15; Ld = T.attrs["Ld"].loc[tt]
    W = eps * SIG * Tk ** 4 + (1 - eps) * Ld
    Trad = ((W - (1 - EPS_CAM) * SIG * (T_REFL + 273.15) ** 4) / (EPS_CAM * SIG)) ** 0.25 - 273.15
    rows[f"{hh} true"] = T.loc[tt]; rows[f"{hh} camera"] = Trad; rows[f"{hh} error"] = Trad - T.loc[tt]
print(f"{DAY_E}, emissivity in the camera {EPS_CAM}, reflected temperature {T_REFL} °C")
print(pd.DataFrame(rows).round(1))

THRESH = 600                  # ◀ parameter: minimum panel irradiance for PV inspection (W/m²)
g = w.global_tilted_irradiance
ok = (g >= THRESH).groupby([g.index.to_period("M").rename("month"), g.index.hour.rename("hour")]).sum().unstack(fill_value=0)
print(f"\\nNumber of hours with panel irradiance (tilt {TILT}°, azimuth {AZ}°) ≥ {THRESH} W/m² by month and hour:")
print(ok.loc[:, ok.sum() > 0].to_string())
''')),
        ("task", t(
            "S emisivitou 1,00 v kameře: který povrch se od své skutečné teploty liší nejvíc a proč FV panel vypadá chladnější, než je? Nastav 0,95 a pak 0,85: který povrch je teď správně a které ne? Proč je chyba v noci jiná než v poledne (uvaž odraženou oblohu)?",
            "With emissivity 1.00 in the camera: which surface differs most from its true temperature and why does the PV panel look colder than it is? Set 0.95 and then 0.85: which surface is now right and which are not? Why is the error at night different from the one at noon (think of the reflected sky)?")),
        ("task", t(
            "Ve kterých měsících a hodinách bylo ozáření panelů aspoň 600 W/m²? Změň v kroku 1 sklon na 60° a azimut na −90° (východ) a buňky spusť znovu: jak se okno pro kontrolu posune? Proč je kontrast vadného nebo odpojeného modulu při slabém slunci malý?",
            "In which months and hours was the panel irradiance at least 600 W/m²? In step 1 change the tilt to 60° and the azimuth to −90° (east) and run the cells again: how does the inspection window shift? Why is the contrast of a faulty or disconnected module small in weak sunlight?")),
    ]
