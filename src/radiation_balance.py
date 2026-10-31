import re

from _common import S2_HELPERS, OPEN_METEO_HELPER

# místa: přípona souboru → letní scéna, scéna se sněhem, souřadnice počasí a popisy
VARIANTS = {
    "": dict(item="S2B_33UVR_20240721_0_L2A", lon=14.375, lat=50.145, wc="N48E012", date_cs="21. 7. 2024", date_en="21 July 2024",
             place_cs="okolí Roztok u Prahy", place_en="near Roztoky u Prahy", around_cs="kolem Roztok", around_en="around Roztoky",
             snow_item="S2A_33UWS_20240308_0_L2A", snow_lon=15.70, snow_lat=50.735, snow_date_cs="8. 3. 2024", snow_date_en="8 March 2024",
             snow_cs="Krkonoše se sněhem", snow_en="snow in the Krkonoše mountains", snowfrom_cs="z Krkonoš", snowfrom_en="from the Krkonoše mountains",
             wlat=50.08, wlon=14.42, wx_cs="v Praze", wx_en="in Prague", wxg_cs="pro Prahu", wxg_en="for Prague", s2_years="2024",
             title_cs="Roztoky a Krkonoše", title_en="Roztoky and Krkonoše"),
    "brno": dict(item="S2B_33UXQ_20240814_0_L2A", lon=16.52, lat=49.23, wc="N48E015", date_cs="14. 8. 2024", date_en="14 August 2024",
                 place_cs="okolí Brněnské přehrady", place_en="near the Brno reservoir", around_cs="kolem Brněnské přehrady", around_en="around the Brno reservoir",
                 snow_item="S2B_33UXR_20240130_0_L2A", snow_lon=17.23, snow_lat=50.08, snow_date_cs="30. 1. 2024", snow_date_en="30 January 2024",
                 snow_cs="Hrubý Jeseník kolem Pradědu se sněhem", snow_en="snow in the Hrubý Jeseník mountains around Praděd",
                 snowfrom_cs="z okolí Pradědu", snowfrom_en="from around Praděd",
                 wlat=49.20, wlon=16.61, wx_cs="v Brně", wx_en="in Brno", wxg_cs="pro Brno", wxg_en="for Brno", s2_years="2024",
                 title_cs="Brno a Jeseníky", title_en="Brno and the Jeseníky"),
    "hluboka": dict(item="S2B_33UVQ_20240731_0_L2A", lon=14.44, lat=49.05, wc="N48E012", date_cs="31. 7. 2024", date_en="31 July 2024",
                    place_cs="okolí Hluboké nad Vltavou", place_en="near Hluboká nad Vltavou", around_cs="kolem Hluboké nad Vltavou", around_en="around Hluboká nad Vltavou",
                    snow_item="S2A_33UVQ_20230209_0_L2A", snow_lon=13.86, snow_lat=48.77, snow_date_cs="9. 2. 2023", snow_date_en="9 February 2023",
                    snow_cs="Šumava kolem Plechého se sněhem", snow_en="snow in the Šumava mountains around Plechý",
                    snowfrom_cs="ze Šumavy kolem Plechého", snowfrom_en="from the Šumava mountains around Plechý",
                    wlat=48.97, wlon=14.47, wx_cs="v Českých Budějovicích", wx_en="in České Budějovice", wxg_cs="pro České Budějovice", wxg_en="for České Budějovice",
                    s2_years="2023–2024", title_cs="Hluboká a Šumava", title_en="Hluboká and Šumava"),
}


def meta(P):
    return {
        "version": "1.0",
        "minutes": 40,
        "title": {"cs": "Kam zmizí sluneční záření: bilance povrchů ze Sentinelu-2 (" + P["title_cs"] + ")", "en": "Where sunlight goes: surface balance from Sentinel-2 (" + P["title_en"] + ")"},
        "visual": {"cs": "Kam zmizí záření", "en": "Where radiation goes"},
        "lead": {
            "cs": "Ve vizuálu se dopadající záření dělí na odražené, pohlcené a prošlé, ρ + α + τ = 1, a podle Kirchhoffova zákona platí ε = α. Tady odrazivost změříš na skutečných pixelech Sentinelu-2 (les, louka, pole, zástavba, voda a sníh), spočítáš, kolik záření povrchy pohltí za skutečného počasí, a odhadneš, jak se ohřejí.",
            "en": "In the visual, incoming radiation splits into reflected, absorbed and transmitted parts, ρ + α + τ = 1, and Kirchhoff's law gives ε = α. Here you measure reflectance on real Sentinel-2 pixels (forest, meadow, field, built-up area, water and snow), compute how much radiation the surfaces absorb in real weather and estimate how warm they get.",
        },
        "goal": {
            "cs": "ze skutečné odrazivosti spočítat pohltivost a albedo povrchů, použít Kirchhoffův zákon na sníh a kovy a z energetické bilance s aktuálním počasím odhadnout rovnovážnou teplotu povrchu a navrhnout chladnou střechu.",
            "en": "compute absorptance and albedo of surfaces from real reflectance, apply Kirchhoff's law to snow and metals, and estimate the equilibrium surface temperature from an energy balance with current weather, then design a cool roof.",
        },
        "data": {
            "cs": f"Sentinel-2 L2A (odrazivost na povrchu) z katalogu Earth Search na AWS: scéna `{P['item']}` ({P['date_cs']}, {P['place_cs']}) a `{P['snow_item']}` ({P['snow_date_cs']}, {P['snow_cs']}); třídy pokryvu ESA WorldCover 2021; hodinové počasí {P['wxg_cs']} z Open-Meteo (posledních 92 dní). Stahuje se asi 15 MB.",
            "en": f"Sentinel-2 L2A (surface reflectance) from the Earth Search catalogue on AWS: scene `{P['item']}` ({P['date_en']}, {P['place_en']}) and `{P['snow_item']}` ({P['snow_date_en']}, {P['snow_en']}); land-cover classes from ESA WorldCover 2021; hourly weather {P['wxg_en']} from Open-Meteo (last 92 days). About 15 MB is downloaded.",
        },
        "sources": {
            "cs": [
                "Copernicus Sentinel-2 data " + P["s2_years"] + ", ESA, zpracováno ESA (L2A, Sen2Cor); COG kopie v registru AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje podle [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).",
                "Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. Zenodo. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
                "Počasí: Open-Meteo.com, model ICON/ECMWF podle dostupnosti (CC BY 4.0). https://open-meteo.com",
                "Albedo z úzkých pásem: Liang, S. (2001). Narrowband to broadband conversions of land surface albedo I: Algorithms. *Remote Sensing of Environment* 76, 213–238. https://doi.org/10.1016/S0034-4257(00)00205-4",
                "Dlouhovlnné záření jasné oblohy: Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744. https://doi.org/10.1029/WR011i005p00742",
                "Součinitel přestupu tepla prouděním h = 5,7 + 3,8 · u: McAdams, W. H. (1954). *Heat Transmission*, 3. vyd. McGraw-Hill (převzato v Duffie, J. A., Beckman, W. A., *Solar Engineering of Thermal Processes*).",
            ],
            "en": [
                "Copernicus Sentinel-2 data " + P["s2_years"] + ", ESA, processed by ESA (L2A, Sen2Cor); COG copy in the AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution under the [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).",
                "Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. Zenodo. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
                "Weather: Open-Meteo.com, ICON/ECMWF models as available (CC BY 4.0). https://open-meteo.com",
                "Narrowband to broadband albedo: Liang, S. (2001). Narrowband to broadband conversions of land surface albedo I: Algorithms. *Remote Sensing of Environment* 76, 213–238. https://doi.org/10.1016/S0034-4257(00)00205-4",
                "Clear-sky longwave radiation: Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744. https://doi.org/10.1029/WR011i005p00742",
                "Convective heat transfer coefficient h = 5.7 + 3.8 · u: McAdams, W. H. (1954). *Heat Transmission*, 3rd ed. McGraw-Hill (as given in Duffie, J. A., Beckman, W. A., *Solar Engineering of Thermal Processes*).",
            ],
        },
    }


def cells(t, P):
    out = [
        ("md", t("## 1. Příprava", "## 1. Setup")),
        ("code", "%pip install -q rasterio"),
        ("code", '''
import time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
from scipy.optimize import brentq
''' + t(S2_HELPERS["cs"] + OPEN_METEO_HELPER["cs"], S2_HELPERS["en"] + OPEN_METEO_HELPER["en"])),
        ("md", t(
            "## 2. Odrazivost skutečných povrchů\n\nNačteme výřez 3 × 3 km @AROUND_CS@ a pro každou třídu ESA WorldCover vezmeme medián odrazivosti čistých pixelů (bez mraků a stínů podle masky SCL). Přidáme sníh @SNOWFROM_CS@; aby šlo o otevřený sníh bez stromů, bereme jen sněhové pixely se zelenou odrazivostí nad 0,5.",
            "## 2. Reflectance of real surfaces\n\nWe load a 3 × 3 km window @AROUND_EN@ and for each ESA WorldCover class take the median reflectance of clear pixels (no clouds or shadows according to the SCL mask). We add snow @SNOWFROM_EN@; to get open snow without trees, we take only snow pixels with green reflectance above 0.5.")),
        ("code", t('''
refl, scl, wl, grid, item = s2_window("@ITEM@", @LON@, @LAT@, 1500)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
clear = np.isin(scl, [4, 5, 6])                     # 4 vegetace, 5 holý povrch, 6 voda
classes = {10: "les", 30: "louka", 40: "pole", 50: "zástavba", 80: "voda"}
spectra = {}
for code, name in classes.items():
    m = clear & (wc == code)
    spectra[name] = [float(np.median(refl[b][m])) for b in BANDS]
    print(f"{name:9s}: {m.sum():6d} pixelů")

snow_refl, snow_scl, *_ = s2_window("@SNOW_ITEM@", @SNOW_LON@, @SNOW_LAT@, 1500)
m = (snow_scl == 11) & (snow_refl["green"] > 0.5)    # 11 = sníh a led; jen otevřený sníh
spectra["sníh"] = [float(np.median(snow_refl[b][m])) for b in BANDS]
print(f"sníh     : {m.sum():6d} pixelů")
R = pd.DataFrame(spectra, index=pd.Index([wl[b] for b in BANDS], name="λ (µm)"))
R.round(3)
''', '''
refl, scl, wl, grid, item = s2_window("@ITEM@", @LON@, @LAT@, 1500)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
clear = np.isin(scl, [4, 5, 6])                     # 4 vegetation, 5 bare surface, 6 water
classes = {10: "forest", 30: "meadow", 40: "field", 50: "built-up", 80: "water"}
spectra = {}
for code, name in classes.items():
    m = clear & (wc == code)
    spectra[name] = [float(np.median(refl[b][m])) for b in BANDS]
    print(f"{name:9s}: {m.sum():6d} pixels")

snow_refl, snow_scl, *_ = s2_window("@SNOW_ITEM@", @SNOW_LON@, @SNOW_LAT@, 1500)
m = (snow_scl == 11) & (snow_refl["green"] > 0.5)    # 11 = snow and ice; open snow only
spectra["snow"] = [float(np.median(snow_refl[b][m])) for b in BANDS]
print(f"snow     : {m.sum():6d} pixels")
R = pd.DataFrame(spectra, index=pd.Index([wl[b] for b in BANDS], name="λ (µm)"))
R.round(3)
''')),
        ("md", t(
            "## 3. Pohltivost: α = 1 − ρ − τ\n\nPixel je pro družici neprůhledný: co neodrazí zpět, pohltí porost, půda nebo voda pod ním. Pro celý pixel proto platí α = 1 − ρ. (U jednoho listu je τ v NIR asi stejně velké jako ρ; uvnitř porostu se ale prošlé záření dál odráží a pohlcuje.)",
            "## 3. Absorptance: α = 1 − ρ − τ\n\nFor the satellite a pixel is opaque: whatever is not reflected back is absorbed by the canopy, the soil or the water below. For the whole pixel α = 1 − ρ. (For a single leaf, τ in the NIR is about as large as ρ; inside a canopy the transmitted light is reflected and absorbed further.)")),
        ("code", t('''
A = 1 - R
fig, ax = plt.subplots(1, 2, figsize=(12, 3.8), sharex=True)
R.plot(ax=ax[0], marker="o"); ax[0].set(ylabel="odrazivost ρ", title="Odrazivost (Sentinel-2 L2A)")
A.plot(ax=ax[1], marker="o", legend=False); ax[1].set(ylabel="pohltivost α = 1 − ρ", title="Pohltivost celého pixelu")
plt.show()
''', '''
A = 1 - R
fig, ax = plt.subplots(1, 2, figsize=(12, 3.8), sharex=True)
R.plot(ax=ax[0], marker="o"); ax[0].set(ylabel="reflectance ρ", title="Reflectance (Sentinel-2 L2A)")
A.plot(ax=ax[1], marker="o", legend=False); ax[1].set(ylabel="absorptance α = 1 − ρ", title="Absorptance of the whole pixel")
plt.show()
''')),
        ("task", t(
            "Kde les a louka pohlcují nejvíc a kde nejmíň? Proč je pro rostlinu výhodné NIR skoro nepohlcovat? Proč voda v NIR pohltí téměř vše, co do ní pronikne?",
            "Where do forest and meadow absorb most and least? Why is it useful for a plant to absorb almost no NIR? Why does water absorb almost everything that enters it in the NIR?")),
        ("task", t(
            "Sníh je ve viditelném světle bílý. Jakou má pohltivost v pásmu 1,6 µm (B11)? Podle Kirchhoffova zákona je při stejné vlnové délce ε = α. Termální pásmo (10 µm) Sentinel-2 nemá, ale trend od viditelného k SWIR naznačuje, jak se sníh chová dál. Proč je sníh v termální oblasti skoro černé těleso (ε ≈ 0,99) a co z toho plyne pro měření jeho teploty termokamerou?",
            "Snow is white in visible light. What is its absorptance at 1.6 µm (B11)? Kirchhoff's law gives ε = α at the same wavelength. Sentinel-2 has no thermal band (10 µm), but the trend from visible to SWIR hints at how snow behaves further on. Why is snow almost a blackbody in the thermal range (ε ≈ 0.99) and what does that mean for measuring its temperature with a thermal camera?")),
        ("md", t(
            "## 4. Albedo: kolik slunečního záření povrch odrazí celkem\n\nAlbedo je odrazivost vážená spektrem Slunce. Liang (2001) ho pro pásma Landsatu odvodil jako lineární kombinaci; použijeme odpovídající pásma Sentinelu-2 (B2, B4, B8, B11, B12), takže výsledek je přibližný.",
            "## 4. Albedo: how much sunlight a surface reflects in total\n\nAlbedo is reflectance weighted by the solar spectrum. Liang (2001) derived it for Landsat bands as a linear combination; we use the corresponding Sentinel-2 bands (B2, B4, B8, B11, B12), so the result is approximate.")),
        ("code", t('''
pick = lambda name, b: R[name].iloc[BANDS.index(b)]
albedo = pd.Series({name: 0.356 * pick(name, "blue") + 0.130 * pick(name, "red") + 0.373 * pick(name, "nir")
                         + 0.085 * pick(name, "swir16") + 0.072 * pick(name, "swir22") - 0.0018 for name in R.columns})
print(albedo.round(3).to_string())
''', '''
pick = lambda name, b: R[name].iloc[BANDS.index(b)]
albedo = pd.Series({name: 0.356 * pick(name, "blue") + 0.130 * pick(name, "red") + 0.373 * pick(name, "nir")
                         + 0.085 * pick(name, "swir16") + 0.072 * pick(name, "swir22") - 0.0018 for name in R.columns})
print(albedo.round(3).to_string())
''')),
        ("md", t(
            "## 5. Skutečné počasí a energetická bilance\n\nZ Open-Meteo vezmeme nejslunečnější hodinu posledních 92 dní @WX_CS@: globální záření S, teplotu vzduchu, rosný bod a vítr. Povrch v rovnováze (bez vypařování a vedení do země) splní\n\n(1 − albedo) · S + ε · L↓ = ε · σ · T⁴ + h · (T − T_vzduch),\n\nkde L↓ je dlouhovlnné záření oblohy (Brutsaert 1975, jasná obloha) a h = 5,7 + 3,8 · u je přestup tepla prouděním.",
            "## 5. Real weather and the energy balance\n\nFrom Open-Meteo we take the sunniest hour of the last 92 days @WX_EN@: global radiation S, air temperature, dew point and wind. A surface in equilibrium (no evaporation and no conduction into the ground) satisfies\n\n(1 − albedo) · S + ε · L↓ = ε · σ · T⁴ + h · (T − T_air),\n\nwhere L↓ is the longwave radiation of the sky (Brutsaert 1975, clear sky) and h = 5.7 + 3.8 · u is convective heat transfer.")),
        ("code", t('''
w = open_meteo({"latitude": @WLAT@, "longitude": @WLON@, "past_days": 92, "forecast_days": 1, "wind_speed_unit": "ms",
                "hourly": "shortwave_radiation,temperature_2m,dew_point_2m,wind_speed_10m,cloud_cover", "timezone": "UTC"})
met = pd.DataFrame(w["hourly"]).set_index("time")
row = met.loc[met.shortwave_radiation.idxmax()]
print("nejslunečnější hodina:", row.name, "UTC"); print(row.to_string())
''', '''
w = open_meteo({"latitude": @WLAT@, "longitude": @WLON@, "past_days": 92, "forecast_days": 1, "wind_speed_unit": "ms",
                "hourly": "shortwave_radiation,temperature_2m,dew_point_2m,wind_speed_10m,cloud_cover", "timezone": "UTC"})
met = pd.DataFrame(w["hourly"]).set_index("time")
row = met.loc[met.shortwave_radiation.idxmax()]
print("sunniest hour:", row.name, "UTC"); print(row.to_string())
''')),
        ("code", t('''
SIGMA = 5.670374e-8
S, Ta, Td = row.shortwave_radiation, row.temperature_2m + 273.15, row.dew_point_2m
u = row.wind_speed_10m * 0.75          # ◀ parametr: vítr u povrchu (zhruba 3/4 větru v 10 m)
e_a = 6.112 * np.exp(17.62 * Td / (243.12 + Td))                  # tlak vodní páry (hPa), Magnusův vzorec
L_sky = 1.24 * (e_a / Ta) ** (1 / 7) * SIGMA * Ta**4               # Brutsaert, jasná obloha
h_c = 5.7 + 3.8 * u

def t_equilibrium(albedo, eps, S=S, Ta=Ta, L_sky=L_sky, h_c=h_c):
    f = lambda T: (1 - albedo) * S + eps * L_sky - eps * SIGMA * T**4 - h_c * (T - Ta)
    return brentq(f, 200, 400) - 273.15

eps_surface = {"les": 0.99, "louka": 0.98, "pole": 0.97, "zástavba": 0.93, "voda": 0.99, "sníh": 0.99}
tab = pd.DataFrame({"albedo": albedo, "ε": pd.Series(eps_surface)})
tab["pohlceno (W/m²)"] = (1 - tab.albedo) * S
tab["T rovnováha (°C)"] = [t_equilibrium(a, e) for a, e in zip(tab.albedo, tab["ε"])]
print(f"S = {S:.0f} W/m², vzduch {Ta - 273.15:.1f} °C, L↓ = {L_sky:.0f} W/m², h = {h_c:.1f} W·m⁻²·K⁻¹")
tab.round(2)
''', '''
SIGMA = 5.670374e-8
S, Ta, Td = row.shortwave_radiation, row.temperature_2m + 273.15, row.dew_point_2m
u = row.wind_speed_10m * 0.75          # ◀ parameter: wind near the surface (about 3/4 of the 10 m wind)
e_a = 6.112 * np.exp(17.62 * Td / (243.12 + Td))                  # water vapour pressure (hPa), Magnus formula
L_sky = 1.24 * (e_a / Ta) ** (1 / 7) * SIGMA * Ta**4               # Brutsaert, clear sky
h_c = 5.7 + 3.8 * u

def t_equilibrium(albedo, eps, S=S, Ta=Ta, L_sky=L_sky, h_c=h_c):
    f = lambda T: (1 - albedo) * S + eps * L_sky - eps * SIGMA * T**4 - h_c * (T - Ta)
    return brentq(f, 200, 400) - 273.15

eps_surface = {"forest": 0.99, "meadow": 0.98, "field": 0.97, "built-up": 0.93, "water": 0.99, "snow": 0.99}
tab = pd.DataFrame({"albedo": albedo, "ε": pd.Series(eps_surface)})
tab["absorbed (W/m²)"] = (1 - tab.albedo) * S
tab["T equilibrium (°C)"] = [t_equilibrium(a, e) for a, e in zip(tab.albedo, tab["ε"])]
print(f"S = {S:.0f} W/m², air {Ta - 273.15:.1f} °C, L↓ = {L_sky:.0f} W/m², h = {h_c:.1f} W·m⁻²·K⁻¹")
tab.round(2)
''')),
        ("task", t(
            "Seřaď povrchy podle pohlceného záření a podle rovnovážné teploty. Skutečný osluněný les nebo louka bývají jen o pár stupňů teplejší než vzduch. Který člen bilance v modelu chybí? Jak se toho využívá při hledání vodního stresu porostu termokamerou z dronu? Proč model u vody selže úplně?",
            "Rank the surfaces by absorbed radiation and by equilibrium temperature. A real sunlit forest or meadow is usually only a few degrees warmer than the air. Which term of the balance is missing from the model? How is this used when looking for water stress in crops with a thermal camera on a drone? Why does the model fail completely for water?")),
        ("task", t(
            "Změň `u` na 0,5 a pak na 6 m/s. Jak se změní rovnovážná teplota zástavby? Proč vítr teplotní rozdíly mezi povrchy zmenšuje?",
            "Change `u` to 0.5 and then to 6 m/s. How does the equilibrium temperature of the built-up area change? Why does wind reduce the temperature differences between surfaces?")),
        ("md", t(
            "## 6. Navrhni chladnou střechu\n\nMěníme albedo a emisivitu střechy při stejném skutečném počasí. Lesklý kov odráží hodně slunce, ale v termální oblasti skoro nevyzařuje (ε ≈ 0,1); bílý nátěr odráží slunce a zároveň vyzařuje (ε ≈ 0,9).",
            "## 6. Design a cool roof\n\nWe vary the albedo and emissivity of a roof under the same real weather. Polished metal reflects a lot of sunlight but hardly emits in the thermal range (ε ≈ 0.1); white paint reflects sunlight and emits as well (ε ≈ 0.9).")),
        ("code", t('''
albedos = np.linspace(0.05, 0.9, 18)
fig, ax = plt.subplots(figsize=(8, 3.8))
for eps in (0.05, 0.3, 0.6, 0.9):          # ◀ parametr: emisivity střechy
    ax.plot(albedos, [t_equilibrium(a, eps) for a in albedos], label=f"ε = {eps}")
ax.axhline(Ta - 273.15, color="gray", ls=":", label="vzduch")
ax.set(xlabel="albedo střechy", ylabel="rovnovážná teplota (°C)"); ax.legend(); plt.show()
''', '''
albedos = np.linspace(0.05, 0.9, 18)
fig, ax = plt.subplots(figsize=(8, 3.8))
for eps in (0.05, 0.3, 0.6, 0.9):          # ◀ parameter: roof emissivities
    ax.plot(albedos, [t_equilibrium(a, eps) for a in albedos], label=f"ε = {eps}")
ax.axhline(Ta - 273.15, color="gray", ls=":", label="air")
ax.set(xlabel="roof albedo", ylabel="equilibrium temperature (°C)"); ax.legend(); plt.show()
''')),
        ("task", t(
            "Jakou teplotu by měla střecha s albedem zástavby z tvého výřezu a jakou bílá střecha (albedo 0,8, ε 0,9)? Proč je lesklý plech s albedem 0,6 (ε 0,05) o tolik teplejší než nátěr se stejným albedem a emisivitou 0,9? Jaké vlastnosti má mít ideální nátěr v pásmu 0,3–2,5 µm a jaké v 8–13 µm?",
            "What temperature would a roof with the albedo of the built-up area in your window have, and a white roof (albedo 0.8, ε 0.9)? Why is polished sheet metal with albedo 0.6 (ε 0.05) so much warmer than a coating with the same albedo and emissivity 0.9? What properties should an ideal coating have at 0.3–2.5 µm and at 8–13 µm?")),
        ("task", t(
            "Vyber z tabulky `met` jinou hodinu, třeba nejteplejší, a vlož ji místo `row` (např. `row = met.loc[met.temperature_2m.idxmax()]` pro nejteplejší hodinu). Jak se změní pořadí a teploty povrchů? Model dává sněhu teplotu nad 0 °C: proč to ve skutečnosti nejde a na co se přebytek energie spotřebuje? Proč na jaře sníh na slunci přesto neroztaje hned, i když S je vysoké?",
            "Pick another hour from the `met` table, for instance the warmest one, and put it in place of `row` (e.g. `row = met.loc[met.temperature_2m.idxmax()]` for the warmest hour). How do the ranking and the temperatures of the surfaces change? The model gives snow a temperature above 0 °C: why is that impossible in reality, and what does the surplus energy go into? Why does snow still not melt immediately in spring sunshine even though S is high?")),
        ("task", t(
        "+ Porovnej výsledky se spolužákem, který spustil notebook pro jiné místo: liší se albedo zástavby, pole a sněhu? Vyšla nejslunečnější hodina v jiný den a s jiným S?",
        "+ Compare your results with a classmate who ran the notebook for another place: do the albedos of built-up land, fields and snow differ? Did the sunniest hour fall on another day and with another S?")),
    ]
    tokens = {"@ITEM@": P["item"], "@LON@": str(P["lon"]), "@LAT@": str(P["lat"]), "@SNOW_ITEM@": P["snow_item"], "@SNOW_LON@": str(P["snow_lon"]),
              "@SNOW_LAT@": str(P["snow_lat"]), "@AROUND_CS@": P["around_cs"], "@AROUND_EN@": P["around_en"], "@SNOWFROM_CS@": P["snowfrom_cs"],
              "@SNOWFROM_EN@": P["snowfrom_en"], "@WX_CS@": P["wx_cs"], "@WX_EN@": P["wx_en"], "@WLAT@": str(P["wlat"]), "@WLON@": str(P["wlon"]),
              "_N48E012_Map": f"_{P['wc']}_Map"}
    res = []
    for kind, text in out:
        for k, v in tokens.items():
            text = text.replace(k, v)
        assert not re.search(r"@[A-Z0-9_]+@", text), text[:80]
        res.append((kind, text))
    return res
