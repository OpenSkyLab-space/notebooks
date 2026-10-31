from _common import S2_HELPERS, OPEN_METEO_HELPER

META = {
    "version": "1.0",
    "minutes": 60,
    "visual_stem": "radiation_balance",
    "title": {"cs": "Kam zmizí sluneční záření, pokročilá verze: denní chod teploty povrchu",
              "en": "Where sunlight goes, advanced: the diurnal course of surface temperature"},
    "visual": {"cs": "Kam zmizí záření", "en": "Where radiation goes"},
    "lead": {
        "cs": "Pokročilá verze notebooku k radiační bilanci. Místo rovnováhy v jedné hodině tu povrch ohříváš a ochlazuješ hodinu po hodině při skutečném počasí několika dní. K pohlcenému záření a vyzařování přibude výpar a tok tepla do země, takže uvidíš, proč je les v poledne chladnější než pole a proč město v noci zůstává teplé.",
        "en": "The advanced version of the radiation balance notebook. Instead of an equilibrium in one hour you heat and cool the surface hour by hour under several days of real weather. Evaporation and heat flow into the ground join absorbed and emitted radiation, so you see why a forest is cooler than a field at noon and why a town stays warm at night.",
    },
    "goal": {
        "cs": "sestavit z reálného počasí sluneční a dlouhovlnné záření, spočítat denní chod teploty povrchu modelem force-restore, rozdělit čistou radiaci na citelné teplo, výpar a tok do země a vysvětlit vliv albeda, dostupnosti vody a tepelné setrvačnosti.",
        "en": "build solar and longwave radiation from real weather, compute the diurnal course of surface temperature with a force-restore model, split net radiation into sensible heat, evaporation and ground heat flux, and explain the roles of albedo, water availability and thermal inertia.",
    },
    "data": {
        "cs": "Albedo povrchů ze scény Sentinel-2 L2A `S2B_33UVR_20240721_0_L2A` (21. 7. 2024, okolí Roztok) a tříd ESA WorldCover 2021; hodinové počasí pro Prahu z Open-Meteo (posledních 92 dní, simulují se dny kolem nejslunečnějšího z nich). Stahuje se asi 5 MB. Vlastnosti povrchů (dostupnost vody, tepelná setrvačnost) jsou orientační a model je zjednodušený: výsledky ukazují souvislosti, nejsou předpovědí skutečné teploty.",
        "en": "Surface albedo from the Sentinel-2 L2A scene `S2B_33UVR_20240721_0_L2A` (21 July 2024, near Roztoky) and ESA WorldCover 2021 classes; hourly weather for Prague from Open-Meteo (last 92 days; the days around the sunniest one are simulated). About 5 MB is downloaded. The surface properties (water availability, thermal inertia) are indicative and the model is simplified: the results show relationships, they are not a forecast of the real temperature.",
    },
    "sources": {
        "cs": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.",
            "Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Počasí: Open-Meteo.com (CC BY 4.0). https://open-meteo.com",
            "Liang, S. (2001). Narrowband to broadband conversions of land surface albedo I: Algorithms. *Remote Sensing of Environment* 76, 213–238. https://doi.org/10.1016/S0034-4257(00)00205-4",
            "Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744. https://doi.org/10.1029/WR011i005p00742",
            "Crawford, T. M., Duchon, C. E. (1999). An improved parameterization for estimating effective atmospheric emissivity for use in calculating daytime downwelling longwave radiation. *Journal of Applied Meteorology* 38, 474–480.",
            "Noilhan, J., Planton, S. (1989). A simple parameterization of land surface processes for meteorological models. *Monthly Weather Review* 117, 536–549. https://doi.org/10.1175/1520-0493(1989)117<0536:ASPOLS>2.0.CO;2",
            "Oke, T. R., Mills, G., Christen, A., Voogt, J. A. (2017). *Urban Climates*. Cambridge University Press.",
        ],
        "en": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.",
            "Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Weather: Open-Meteo.com (CC BY 4.0). https://open-meteo.com",
            "Liang, S. (2001). Narrowband to broadband conversions of land surface albedo I: Algorithms. *Remote Sensing of Environment* 76, 213–238. https://doi.org/10.1016/S0034-4257(00)00205-4",
            "Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744. https://doi.org/10.1029/WR011i005p00742",
            "Crawford, T. M., Duchon, C. E. (1999). An improved parameterization for estimating effective atmospheric emissivity for use in calculating daytime downwelling longwave radiation. *Journal of Applied Meteorology* 38, 474–480.",
            "Noilhan, J., Planton, S. (1989). A simple parameterization of land surface processes for meteorological models. *Monthly Weather Review* 117, 536–549. https://doi.org/10.1175/1520-0493(1989)117<0536:ASPOLS>2.0.CO;2",
            "Oke, T. R., Mills, G., Christen, A., Voogt, J. A. (2017). *Urban Climates*. Cambridge University Press.",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a albedo povrchů", "## 1. Setup and surface albedo")),
        ("code", "%pip install -q rasterio"),
        ("code", t('''
import time, requests, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
warnings.filterwarnings("ignore")
''' + S2_HELPERS["cs"] + OPEN_METEO_HELPER["cs"], '''
import time, requests, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
warnings.filterwarnings("ignore")
''' + S2_HELPERS["en"] + OPEN_METEO_HELPER["en"])),
        ("md", t("Albedo čtyř povrchů spočítáme stejně jako v základní verzi (Liang 2001, pásma Sentinelu-2). Vodu vynecháme: voda se promíchává a teplo ukládá do hloubky, což jednovrstvý model povrchu nepopíše.",
                 "We compute the albedo of four surfaces as in the basic version (Liang 2001, Sentinel-2 bands). We leave water out: water mixes and stores heat at depth, which a single-layer surface model cannot describe.")),
        ("code", t('''
refl, scl, wl, grid, item = s2_window("S2B_33UVR_20240721_0_L2A", 14.375, 50.145, 1500)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
clear = np.isin(scl, [4, 5, 6])
classes = {10: "les", 30: "louka", 40: "pole", 50: "zástavba"}
albedo = {}
for code, name in classes.items():
    m = clear & (wc == code)
    med = {b: float(np.median(refl[b][m])) for b in ["blue", "red", "nir", "swir16", "swir22"]}
    albedo[name] = 0.356 * med["blue"] + 0.130 * med["red"] + 0.373 * med["nir"] + 0.085 * med["swir16"] + 0.072 * med["swir22"] - 0.0018
print({k: round(v, 3) for k, v in albedo.items()})
''', '''
refl, scl, wl, grid, item = s2_window("S2B_33UVR_20240721_0_L2A", 14.375, 50.145, 1500)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
clear = np.isin(scl, [4, 5, 6])
classes = {10: "forest", 30: "meadow", 40: "field", 50: "built-up"}
albedo = {}
for code, name in classes.items():
    m = clear & (wc == code)
    med = {b: float(np.median(refl[b][m])) for b in ["blue", "red", "nir", "swir16", "swir22"]}
    albedo[name] = 0.356 * med["blue"] + 0.130 * med["red"] + 0.373 * med["nir"] + 0.085 * med["swir16"] + 0.072 * med["swir22"] - 0.0018
print({k: round(v, 3) for k, v in albedo.items()})
''')),
        ("md", t(
            "## 2. Skutečné počasí jako vstup\n\nZ Open-Meteo vezmeme hodinové globální záření, teplotu, rosný bod, vítr, oblačnost a tlak. Dlouhovlnné záření oblohy L↓ počítáme z emisivity jasné oblohy (Brutsaert 1975) a oblačnost c přičteme ve tvaru Crawforda a Duchona (1999): ε = ε_jasno · (1 − c) + c. Oblačnost tu bereme z modelu počasí, ne z měření.",
            "## 2. Real weather as input\n\nFrom Open-Meteo we take hourly global radiation, temperature, dew point, wind, cloud cover and pressure. Longwave sky radiation L↓ is computed from the clear-sky emissivity (Brutsaert 1975) and the cloud cover c is added in the form of Crawford and Duchon (1999): ε = ε_clear · (1 − c) + c. The cloud cover comes from the weather model here, not from measurements.")),
        ("code", t('''
LAT, LON = 50.08, 14.42                     # ◀ parametr: místo pro počasí (Praha)
w = open_meteo({"latitude": LAT, "longitude": LON, "past_days": 92, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "UTC",
                "hourly": "shortwave_radiation,temperature_2m,dew_point_2m,wind_speed_10m,cloud_cover,surface_pressure"})
met = pd.DataFrame(w["hourly"]).assign(time=lambda d: pd.to_datetime(d.time)).set_index("time").dropna()
daily = met.shortwave_radiation.resample("D").sum() * 3600 / 1e6            # MJ/m² za den
best = daily.idxmax()
N_DAYS = 4                                   # ◀ parametr: kolik dní simulovat (nejslunečnější den je uprostřed)
start = best - pd.Timedelta(days=N_DAYS // 2)
F = met.loc[start: start + pd.Timedelta(days=N_DAYS) - pd.Timedelta(hours=1)].copy()
SIGMA = 5.670374e-8
F["Ta"] = F.temperature_2m + 273.15
F["e_a"] = 6.112 * np.exp(17.62 * F.dew_point_2m / (243.12 + F.dew_point_2m))          # hPa
eps_clear = 1.24 * (F.e_a / F.Ta) ** (1 / 7)                                          # Brutsaert 1975
F["L_sky"] = (eps_clear * (1 - F.cloud_cover / 100) + F.cloud_cover / 100) * SIGMA * F.Ta ** 4
F["q_a"] = 0.622 * F.e_a / F.surface_pressure
print(f"nejslunečnější den {best.date()} ({daily.max():.1f} MJ/m²), simulace {F.index[0]} až {F.index[-1]} UTC")
fig, ax = plt.subplots(1, 2, figsize=(13, 3.6))
F[["shortwave_radiation", "L_sky"]].plot(ax=ax[0]); ax[0].set(ylabel="W/m²", title="sluneční a dlouhovlnné záření oblohy")
F[["temperature_2m", "dew_point_2m"]].plot(ax=ax[1]); (F.cloud_cover / 10).plot(ax=ax[1], ls=":", label="oblačnost / 10 (%)")
ax[1].set(ylabel="°C", title="teplota, rosný bod, oblačnost"); ax[1].legend(); plt.show()
''', '''
LAT, LON = 50.08, 14.42                     # ◀ parameter: place for the weather (Prague)
w = open_meteo({"latitude": LAT, "longitude": LON, "past_days": 92, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "UTC",
                "hourly": "shortwave_radiation,temperature_2m,dew_point_2m,wind_speed_10m,cloud_cover,surface_pressure"})
met = pd.DataFrame(w["hourly"]).assign(time=lambda d: pd.to_datetime(d.time)).set_index("time").dropna()
daily = met.shortwave_radiation.resample("D").sum() * 3600 / 1e6            # MJ/m² per day
best = daily.idxmax()
N_DAYS = 4                                   # ◀ parameter: how many days to simulate (the sunniest day is in the middle)
start = best - pd.Timedelta(days=N_DAYS // 2)
F = met.loc[start: start + pd.Timedelta(days=N_DAYS) - pd.Timedelta(hours=1)].copy()
SIGMA = 5.670374e-8
F["Ta"] = F.temperature_2m + 273.15
F["e_a"] = 6.112 * np.exp(17.62 * F.dew_point_2m / (243.12 + F.dew_point_2m))          # hPa
eps_clear = 1.24 * (F.e_a / F.Ta) ** (1 / 7)                                          # Brutsaert 1975
F["L_sky"] = (eps_clear * (1 - F.cloud_cover / 100) + F.cloud_cover / 100) * SIGMA * F.Ta ** 4
F["q_a"] = 0.622 * F.e_a / F.surface_pressure
print(f"sunniest day {best.date()} ({daily.max():.1f} MJ/m²), simulation {F.index[0]} to {F.index[-1]} UTC")
fig, ax = plt.subplots(1, 2, figsize=(13, 3.6))
F[["shortwave_radiation", "L_sky"]].plot(ax=ax[0]); ax[0].set(ylabel="W/m²", title="solar and longwave sky radiation")
F[["temperature_2m", "dew_point_2m"]].plot(ax=ax[1]); (F.cloud_cover / 10).plot(ax=ax[1], ls=":", label="cloud cover / 10 (%)")
ax[1].set(ylabel="°C", title="temperature, dew point, cloud cover"); ax[1].legend(); plt.show()
''')),
        ("task", t(
            "Najdi v grafech noc s jasnou a noc se zataženou oblohou. O kolik se v nich liší L↓ a proč? Co to znamená pro ochlazování povrchu v noci?",
            "Find a night with clear and a night with overcast sky in the plots. How much does L↓ differ between them and why? What does that mean for the cooling of the surface at night?")),
        ("md", t(
            "## 3. Model povrchu\n\nČistá radiace Rn = (1 − albedo) · S + ε · L↓ − ε · σ · Ts⁴ se dělí na citelné teplo H = h · (Ts − T_vzduch), výpar LE = β · (L_v/c_p) · h · (q_sat(Ts) − q_vzduch) a tok do země G = Rn − H − LE. Teplotu povrchu Ts posouvá G podle modelu force-restore (Noilhan a Planton 1989): dTs/dt = C_T · G − (2π/τ) · (Ts − T2), kde C_T = 2√(π/τ)/P a P je tepelná setrvačnost. β říká, kolik vody má povrch k dispozici (0 suchý beton, 1 mokrý povrch).",
            "## 3. The surface model\n\nNet radiation Rn = (1 − albedo) · S + ε · L↓ − ε · σ · Ts⁴ splits into sensible heat H = h · (Ts − T_air), evaporation LE = β · (L_v/c_p) · h · (q_sat(Ts) − q_air) and ground heat flux G = Rn − H − LE. The surface temperature Ts is driven by G in the force-restore model (Noilhan and Planton 1989): dTs/dt = C_T · G − (2π/τ) · (Ts − T2), with C_T = 2√(π/τ)/P, where P is thermal inertia. β says how much water the surface has available (0 dry concrete, 1 wet surface).")),
        ("code", t('''
SURF = pd.DataFrame({                                             # ◀ parametr: vlastnosti povrchů (orientační)
    "albedo": albedo,
    "ε":      {"les": 0.99, "louka": 0.98, "pole": 0.97, "zástavba": 0.93},
    "β":      {"les": 0.7, "louka": 0.5, "pole": 0.2, "zástavba": 0.05},          # dostupnost vody pro výpar (0–1)
    "P":      {"les": 800, "louka": 1200, "pole": 1000, "zástavba": 2000},        # tepelná setrvačnost (J·m⁻²·K⁻¹·s⁻½)
})
WIND = 0.75                                  # ◀ parametr: vítr u povrchu jako podíl větru v 10 m
TAU, LV, CP = 86400.0, 2.45e6, 1005.0

def q_sat(T, p):
    e = 6.112 * np.exp(17.62 * (T - 273.15) / (243.12 + T - 273.15))
    return 0.622 * e / p

def simulate(albedo, eps, beta, P, F=F, dt=60):
    """Model force-restore (Noilhan a Planton 1989): teplota povrchu Ts a hlubší vrstvy T2 při skutečném počasí."""
    CT = 2 * np.sqrt(np.pi / TAU) / P
    Ts = T2 = F.Ta.iloc[0]
    out = []
    for t, r in F.iterrows():
        h = 5.7 + 3.8 * r.wind_speed_10m * WIND
        for _ in range(int(3600 / dt)):
            Rn = (1 - albedo) * r.shortwave_radiation + eps * r.L_sky - eps * SIGMA * Ts ** 4
            H = h * (Ts - r.Ta)
            LE = beta * LV / CP * h * (q_sat(Ts, r.surface_pressure) - r.q_a)
            G = Rn - H - LE
            Ts, T2 = Ts + dt * (CT * G - 2 * np.pi / TAU * (Ts - T2)), T2 + dt * (Ts - T2) / TAU
        out.append({"time": t, "Ts": Ts - 273.15, "Rn": Rn, "H": H, "LE": LE, "G": G})
    return pd.DataFrame(out).set_index("time")

t0 = time.time()
runs = {name: simulate(s.albedo, s["ε"], s["β"], s.P) for name, s in SURF.iterrows()}
print(f"simulace {len(runs)} povrchů za {time.time() - t0:.0f} s")
fig, ax = plt.subplots(figsize=(12, 4))
for name, r in runs.items():
    r.Ts.plot(ax=ax, label=name)
F.temperature_2m.plot(ax=ax, color="k", ls="--", label="vzduch 2 m")
ax.set(ylabel="teplota povrchu (°C)", title="denní chod teploty povrchu"); ax.legend(); plt.show()
''', '''
SURF = pd.DataFrame({                                             # ◀ parameter: surface properties (indicative)
    "albedo": albedo,
    "ε":      {"forest": 0.99, "meadow": 0.98, "field": 0.97, "built-up": 0.93},
    "β":      {"forest": 0.7, "meadow": 0.5, "field": 0.2, "built-up": 0.05},          # water availability for evaporation (0–1)
    "P":      {"forest": 800, "meadow": 1200, "field": 1000, "built-up": 2000},        # thermal inertia (J·m⁻²·K⁻¹·s⁻½)
})
WIND = 0.75                                  # ◀ parameter: wind near the surface as a fraction of the 10 m wind
TAU, LV, CP = 86400.0, 2.45e6, 1005.0

def q_sat(T, p):
    e = 6.112 * np.exp(17.62 * (T - 273.15) / (243.12 + T - 273.15))
    return 0.622 * e / p

def simulate(albedo, eps, beta, P, F=F, dt=60):
    """Force-restore model (Noilhan and Planton 1989): temperature of the surface Ts and of a deeper layer T2 under real weather."""
    CT = 2 * np.sqrt(np.pi / TAU) / P
    Ts = T2 = F.Ta.iloc[0]
    out = []
    for t, r in F.iterrows():
        h = 5.7 + 3.8 * r.wind_speed_10m * WIND
        for _ in range(int(3600 / dt)):
            Rn = (1 - albedo) * r.shortwave_radiation + eps * r.L_sky - eps * SIGMA * Ts ** 4
            H = h * (Ts - r.Ta)
            LE = beta * LV / CP * h * (q_sat(Ts, r.surface_pressure) - r.q_a)
            G = Rn - H - LE
            Ts, T2 = Ts + dt * (CT * G - 2 * np.pi / TAU * (Ts - T2)), T2 + dt * (Ts - T2) / TAU
        out.append({"time": t, "Ts": Ts - 273.15, "Rn": Rn, "H": H, "LE": LE, "G": G})
    return pd.DataFrame(out).set_index("time")

t0 = time.time()
runs = {name: simulate(s.albedo, s["ε"], s["β"], s.P) for name, s in SURF.iterrows()}
print(f"simulation of {len(runs)} surfaces in {time.time() - t0:.0f} s")
fig, ax = plt.subplots(figsize=(12, 4))
for name, r in runs.items():
    r.Ts.plot(ax=ax, label=name)
F.temperature_2m.plot(ax=ax, color="k", ls="--", label="air 2 m")
ax.set(ylabel="surface temperature (°C)", title="diurnal course of surface temperature"); ax.legend(); plt.show()
''')),
        ("task", t(
            "Který povrch je nejteplejší v poledne a který v noci? Proč je zástavba v poledne chladnější než pole, i když skoro nic neodpařuje, a v noci naopak nejteplejší? V kolik hodin UTC má povrch maximum a proč až po slunečním poledni (v Praze kolem 11:00 UTC)?",
            "Which surface is warmest at noon and which at night? Why is the built-up surface cooler than the field at noon although it hardly evaporates, and the warmest at night? At what time UTC does the surface reach its maximum, and why only after solar noon (in Prague around 11:00 UTC)?")),
        ("md", t("## 4. Kam se energie během dne rozdělí", "## 4. Where the energy goes during the day")),
        ("code", t('''
day = F.index.normalize() == best
rows = {}
for name, r in runs.items():
    d = r[day]
    rows[name] = {"Rn (MJ/m²)": d.Rn.sum() * 3600 / 1e6, "H (MJ/m²)": d.H.sum() * 3600 / 1e6, "LE (MJ/m²)": d.LE.sum() * 3600 / 1e6,
                  "G (MJ/m²)": d.G.sum() * 3600 / 1e6, "Bowenův poměr H/LE": d.H.sum() / d.LE.sum(),
                  "max Ts (°C)": d.Ts.max(), "hodina max (UTC)": d.Ts.idxmax().hour, "min Ts noc (°C)": d.Ts.min()}
pd.DataFrame(rows).T.round(2)
''', '''
day = F.index.normalize() == best
rows = {}
for name, r in runs.items():
    d = r[day]
    rows[name] = {"Rn (MJ/m²)": d.Rn.sum() * 3600 / 1e6, "H (MJ/m²)": d.H.sum() * 3600 / 1e6, "LE (MJ/m²)": d.LE.sum() * 3600 / 1e6,
                  "G (MJ/m²)": d.G.sum() * 3600 / 1e6, "Bowen ratio H/LE": d.H.sum() / d.LE.sum(),
                  "max Ts (°C)": d.Ts.max(), "hour of max (UTC)": d.Ts.idxmax().hour, "min Ts night (°C)": d.Ts.min()}
pd.DataFrame(rows).T.round(2)
''')),
        ("task", t(
            "Kolik procent čisté radiace spotřebuje les na výpar a kolik zástavba? Co říká Bowenův poměr a proč u lesa vychází pod 1? Proč je denní součet G kladný, tj. co se během slunečných dní děje s teplem v zemi?",
            "What percentage of net radiation does the forest spend on evaporation and what percentage the built-up surface? What does the Bowen ratio tell you and why is it below 1 for the forest? Why is the daily sum of G positive, i.e. what happens to the heat in the ground during sunny days?")),
        ("md", t("## 5. Setrvačnost a voda", "## 5. Inertia and water")),
        ("code", t('''
TEST = "zástavba"                            # ◀ parametr: povrch, na kterém zkoušíme vlastnosti
s = SURF.loc[TEST]
fig, ax = plt.subplots(1, 2, figsize=(13, 3.8))
for P in [400, 1000, 2000, 3000]:
    simulate(s.albedo, s["ε"], s["β"], P).Ts.plot(ax=ax[0], label=f"P = {P}")
for beta in [0.0, 0.2, 0.5, 1.0]:
    simulate(s.albedo, s["ε"], beta, s.P).Ts.plot(ax=ax[1], label=f"β = {beta}")
ax[0].set(ylabel="Ts (°C)", title=f"{TEST}: tepelná setrvačnost"); ax[0].legend()
ax[1].set(ylabel="Ts (°C)", title=f"{TEST}: dostupnost vody"); ax[1].legend(); plt.show()
''', '''
TEST = "built-up"                            # ◀ parameter: surface on which we try the properties
s = SURF.loc[TEST]
fig, ax = plt.subplots(1, 2, figsize=(13, 3.8))
for P in [400, 1000, 2000, 3000]:
    simulate(s.albedo, s["ε"], s["β"], P).Ts.plot(ax=ax[0], label=f"P = {P}")
for beta in [0.0, 0.2, 0.5, 1.0]:
    simulate(s.albedo, s["ε"], beta, s.P).Ts.plot(ax=ax[1], label=f"β = {beta}")
ax[0].set(ylabel="Ts (°C)", title=f"{TEST}: thermal inertia"); ax[0].legend()
ax[1].set(ylabel="Ts (°C)", title=f"{TEST}: water availability"); ax[1].legend(); plt.show()
''')),
        ("task", t(
            "Jak se s rostoucí tepelnou setrvačností P mění denní rozkmit teploty a čas maxima? A jak s dostupností vody β? Který z obou zásahů by víc pomohl proti přehřívání ulic ve dne a který v noci (zeleň a zalévání, nebo jiné materiály)?",
            "How do the diurnal temperature range and the time of the maximum change with increasing thermal inertia P? And with water availability β? Which of the two measures would help more against overheating streets during the day and which at night (greenery and watering, or different materials)?")),
        ("md", t("## 6. Srovnání s rovnováhou ze základní verze", "## 6. Comparison with the equilibrium from the basic version")),
        ("code", t('''
from scipy.optimize import brentq
noon = runs["zástavba"][day].Ts.idxmax()
r = F.loc[noon]
h = 5.7 + 3.8 * r.wind_speed_10m * WIND
cmp = {}
for name, s in SURF.iterrows():
    f = lambda T: (1 - s.albedo) * r.shortwave_radiation + s["ε"] * r.L_sky - s["ε"] * SIGMA * T ** 4 - h * (T - r.Ta)
    cmp[name] = {"rovnováha bez výparu a země (°C)": brentq(f, 200, 400) - 273.15, "model force-restore (°C)": runs[name].Ts[noon]}
print(f"hodina {noon} UTC, S = {r.shortwave_radiation:.0f} W/m², vzduch {r.temperature_2m:.1f} °C")
pd.DataFrame(cmp).T.round(1)
''', '''
from scipy.optimize import brentq
noon = runs["built-up"][day].Ts.idxmax()
r = F.loc[noon]
h = 5.7 + 3.8 * r.wind_speed_10m * WIND
cmp = {}
for name, s in SURF.iterrows():
    f = lambda T: (1 - s.albedo) * r.shortwave_radiation + s["ε"] * r.L_sky - s["ε"] * SIGMA * T ** 4 - h * (T - r.Ta)
    cmp[name] = {"equilibrium without evaporation and ground (°C)": brentq(f, 200, 400) - 273.15, "force-restore model (°C)": runs[name].Ts[noon]}
print(f"hour {noon} UTC, S = {r.shortwave_radiation:.0f} W/m², air {r.temperature_2m:.1f} °C")
pd.DataFrame(cmp).T.round(1)
''')),
        ("task", t(
            "O kolik stupňů je rovnovážná teplota bez výparu a toku do země vyšší než teplota z modelu? Které dva členy bilance rozdíl vysvětlují a u kterého povrchu je který důležitější? Proč termokamera z dronu v poledne ukáže mezi lesem a polem rozdíl, ze kterého lze usuzovat na vodní stres?",
            "How many degrees higher is the equilibrium temperature without evaporation and ground heat flux than the model temperature? Which two terms of the balance explain the difference, and for which surface is which more important? Why does a drone thermal camera at noon show a difference between forest and field from which water stress can be inferred?")),
        ("task", t(
            "+ Změň `LAT, LON` na jiné místo (třeba horskou stanici) nebo `N_DAYS` na 10 a podívej se, jak se mění noční minima při jasné a zatažené obloze. Proč jsou mrazové kotliny nejchladnější za jasných a klidných nocí?",
            "+ Change `LAT, LON` to another place (for example a mountain station) or `N_DAYS` to 10 and look at how night minima change under clear and overcast skies. Why are frost hollows coldest on clear and calm nights?")),
    ]
