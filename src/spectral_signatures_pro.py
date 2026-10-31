from _common import S2_HELPERS

META = {
    "version": "1.0",
    "minutes": 75,
    "visual_stem": "spectral_signatures",
    "title": {"cs": "Spektrální signatury, pokročilá verze: model PROSAIL, nasycení indexů a odhad LAI",
              "en": "Spectral signatures, advanced: the PROSAIL model, index saturation and LAI retrieval"},
    "visual": {"cs": "Spektrální signatury", "en": "Spectral signatures"},
    "lead": {
        "cs": "Pokročilá verze notebooku ke spektrálním signaturám. Křivky z vizuálu tu počítá skutečný model přenosu záření PROSAIL, který spojuje optiku listu (PROSPECT) s porostem (SAIL). Ukážeš v něm, proč se NDVI nasycuje, sestavíš tabulku simulací a z ní odhadneš LAI pro každý pixel dvou snímků Sentinel-2 u Roztok, včetně nejistoty a míst, kde model selhává.",
        "en": "The advanced version of the spectral signatures notebook. The curves from the visual are computed here by a real radiative transfer model, PROSAIL, which couples leaf optics (PROSPECT) with the canopy (SAIL). You use it to show why NDVI saturates, build a table of simulations and from it estimate LAI for every pixel of two Sentinel-2 images near Roztoky, with its uncertainty and the places where the model fails.",
    },
    "goal": {
        "cs": "zjistit, která pásma nesou informaci o chlorofylu, vodě, sušině a LAI, porovnat nasycení NDVI, NDRE a CIre v modelu, pochopit, proč je inverze modelu nejednoznačná, a odhadnout LAI z inverze tabulkou simulací se znalostí jejích mezí.",
        "en": "find out which bands carry information on chlorophyll, water, dry matter and LAI, compare the saturation of NDVI, NDRE and CIre in the model, understand why inverting the model is ambiguous, and estimate LAI by inverting a table of simulations while knowing its limits.",
    },
    "data": {
        "cs": "dva snímky Sentinel-2 L2A dlaždice 33UVR (14. 5. a 21. 7. 2024) z katalogu Earth Search na AWS, výřez 4 × 4 km kolem Roztok a Únětic; třídy ESA WorldCover 2021 v200. Simulace počítá balíček `prosail` (PROSPECT-5 a 4SAIL) přímo v notebooku. Stahuje se asi 40 MB, tabulka simulací trvá 1 až 3 minuty. Pozemní měření LAI k výřezu nejsou k dispozici, takže výsledky inverze jsou odhady modelu, ne ověřené hodnoty.",
        "en": "two Sentinel-2 L2A images of tile 33UVR (14 May and 21 July 2024) from the Earth Search catalogue on AWS, a 4 × 4 km window around Roztoky and Únětice; ESA WorldCover 2021 v200 classes. The simulations are computed by the `prosail` package (PROSPECT-5 and 4SAIL) inside the notebook. About 40 MB is downloaded; the simulation table takes 1 to 3 minutes. No ground LAI measurements exist for the window, so the inversion results are model estimates, not validated values.",
    },
    "sources": {
        "cs": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.",
            "Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Jacquemoud, S. a kol. (2009). PROSPECT + SAIL models: A review of use for vegetation characterization. *Remote Sensing of Environment* 113, S56–S66. https://doi.org/10.1016/j.rse.2008.01.026",
            "Feret, J.-B. a kol. (2008). PROSPECT-4 and 5: Advances in the leaf optical properties model separating photosynthetic pigments. *Remote Sensing of Environment* 112, 3030–3043. https://doi.org/10.1016/j.rse.2008.02.012",
            "Verhoef, W., Jia, L., Xiao, Q., Su, Z. (2007). Unified optical-thermal four-stream radiative transfer theory for homogeneous vegetation canopies. *IEEE Transactions on Geoscience and Remote Sensing* 45, 1808–1822. https://doi.org/10.1109/TGRS.2007.895844",
            "Gómez-Dans, J. *prosail*: Python bindings for PROSPECT and SAIL. https://github.com/jgomezdans/prosail",
            "Combal, B. a kol. (2002). Retrieval of canopy biophysical variables from bidirectional reflectance using prior information to solve the ill-posed inverse problem. *Remote Sensing of Environment* 84, 1–15.",
            "Gitelson, A. A. a kol. (2005). Remote estimation of canopy chlorophyll content in crops. *Geophysical Research Letters* 32, L08403. https://doi.org/10.1029/2005GL022688",
            "Asner, G. P., Scurlock, J. M. O., Hicke, J. A. (2003). Global synthesis of leaf area index observations: implications for ecological and remote sensing studies. *Global Ecology and Biogeography* 12, 191–205. https://doi.org/10.1046/j.1466-822X.2003.00026.x",
            "Pedregosa, F. a kol. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.",
        ],
        "en": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.",
            "Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Jacquemoud, S. et al. (2009). PROSPECT + SAIL models: A review of use for vegetation characterization. *Remote Sensing of Environment* 113, S56–S66. https://doi.org/10.1016/j.rse.2008.01.026",
            "Feret, J.-B. et al. (2008). PROSPECT-4 and 5: Advances in the leaf optical properties model separating photosynthetic pigments. *Remote Sensing of Environment* 112, 3030–3043. https://doi.org/10.1016/j.rse.2008.02.012",
            "Verhoef, W., Jia, L., Xiao, Q., Su, Z. (2007). Unified optical-thermal four-stream radiative transfer theory for homogeneous vegetation canopies. *IEEE Transactions on Geoscience and Remote Sensing* 45, 1808–1822. https://doi.org/10.1109/TGRS.2007.895844",
            "Gómez-Dans, J. *prosail*: Python bindings for PROSPECT and SAIL. https://github.com/jgomezdans/prosail",
            "Combal, B. et al. (2002). Retrieval of canopy biophysical variables from bidirectional reflectance using prior information to solve the ill-posed inverse problem. *Remote Sensing of Environment* 84, 1–15.",
            "Gitelson, A. A. et al. (2005). Remote estimation of canopy chlorophyll content in crops. *Geophysical Research Letters* 32, L08403. https://doi.org/10.1029/2005GL022688",
            "Asner, G. P., Scurlock, J. M. O., Hicke, J. A. (2003). Global synthesis of leaf area index observations: implications for ecological and remote sensing studies. *Global Ecology and Biogeography* 12, 191–205. https://doi.org/10.1046/j.1466-822X.2003.00026.x",
            "Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava, dva snímky a model", "## 1. Setup, two images and the model")),
        ("code", "%pip install -q rasterio prosail"),
        ("code", t('''
import requests, time, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio, prosail
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
from sklearn.neighbors import NearestNeighbors
warnings.filterwarnings("ignore")
''' + S2_HELPERS["cs"], '''
import requests, time, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio, prosail
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
from sklearn.neighbors import NearestNeighbors
warnings.filterwarnings("ignore")
''' + S2_HELPERS["en"])),
        ("code", t('''
DATES = ["S2A_33UVR_20240514_0_L2A", "S2B_33UVR_20240721_0_L2A"]   # ◀ parametr: dva snímky jedné sezóny (jaro, léto)
LON, LAT, HALF = 14.375, 50.155, 2000                              # ◀ parametr: střed výřezu a jeho poloviční šířka (m)
scenes = {}
for item_id in DATES:
    refl, scl, wl, grid, item = s2_window(item_id, LON, LAT, HALF)
    day = item["properties"]["datetime"][:10]
    scenes[day] = dict(refl=refl, clear=np.isin(scl, [4, 5, 6]), sza=90 - item["properties"]["view:sun_elevation"])
    print(f"{item_id}: bez mraků {scenes[day]['clear'].mean():.1%} výřezu, zenitový úhel Slunce {scenes[day]['sza']:.1f}°")
DAYS = list(scenes)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
CLASSES = {10: "les", 30: "louka", 40: "pole", 50: "zástavba", 80: "voda"}

# pásma pro model a jejich spektrální citlivost, přibližně Gaussovou křivkou podle středu a pološířky z katalogu
INV = ["blue", "green", "red", "rededge1", "rededge2", "rededge3", "nir", "nir08", "swir16", "swir22"]
cwl = np.array([item["assets"][b]["eo:bands"][0]["center_wavelength"] for b in INV]) * 1000
fwhm = np.array([item["assets"][b]["eo:bands"][0]["full_width_half_max"] for b in INV]) * 1000
WL = np.arange(400, 2501)
SRF = np.exp(-0.5 * ((WL[None] - cwl[:, None]) / (fwhm[:, None] / 2.355)) ** 2)
SRF /= SRF.sum(1, keepdims=True)

def prosail_s2(cab=40, cw=0.012, cm=0.008, lai=3, ala=57, n=1.5, psoil=0.5, rsoil=1.0, sza=32, full=False):
    """Odrazivost porostu z PROSAIL (PROSPECT-5 + 4SAIL): celé spektrum 400–2500 nm (full=True), nebo pásma Sentinelu-2.
    cab chlorofyl (µg/cm²), cw voda v listu (cm), cm sušina (g/cm²), lai index listové plochy, ala průměrný úhel listů (°),
    n struktura listu, psoil podíl suché půdy, rsoil jas půdy; karotenoidy = cab/4, pohled kolmo dolů."""
    r = prosail.run_prosail(n, cab, cab / 4, 0.0, cw, cm, lai=lai, lidfa=ala, hspot=0.01, tts=sza, tto=0.0, psi=0.0,
                            typelidf=2, rsoil=rsoil, psoil=psoil, factor="SDR")
    return r if full else SRF @ r
''', '''
DATES = ["S2A_33UVR_20240514_0_L2A", "S2B_33UVR_20240721_0_L2A"]   # ◀ parameter: two images of one season (spring, summer)
LON, LAT, HALF = 14.375, 50.155, 2000                              # ◀ parameter: window centre and half width (m)
scenes = {}
for item_id in DATES:
    refl, scl, wl, grid, item = s2_window(item_id, LON, LAT, HALF)
    day = item["properties"]["datetime"][:10]
    scenes[day] = dict(refl=refl, clear=np.isin(scl, [4, 5, 6]), sza=90 - item["properties"]["view:sun_elevation"])
    print(f"{item_id}: cloud-free {scenes[day]['clear'].mean():.1%} of the window, solar zenith angle {scenes[day]['sza']:.1f}°")
DAYS = list(scenes)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
CLASSES = {10: "forest", 30: "grassland", 40: "cropland", 50: "built-up", 80: "water"}

# bands for the model and their spectral response, approximated by a Gaussian from the centre and FWHM in the catalogue
INV = ["blue", "green", "red", "rededge1", "rededge2", "rededge3", "nir", "nir08", "swir16", "swir22"]
cwl = np.array([item["assets"][b]["eo:bands"][0]["center_wavelength"] for b in INV]) * 1000
fwhm = np.array([item["assets"][b]["eo:bands"][0]["full_width_half_max"] for b in INV]) * 1000
WL = np.arange(400, 2501)
SRF = np.exp(-0.5 * ((WL[None] - cwl[:, None]) / (fwhm[:, None] / 2.355)) ** 2)
SRF /= SRF.sum(1, keepdims=True)

def prosail_s2(cab=40, cw=0.012, cm=0.008, lai=3, ala=57, n=1.5, psoil=0.5, rsoil=1.0, sza=32, full=False):
    """Canopy reflectance from PROSAIL (PROSPECT-5 + 4SAIL): the full 400–2500 nm spectrum (full=True) or the Sentinel-2 bands.
    cab chlorophyll (µg/cm²), cw leaf water (cm), cm dry matter (g/cm²), lai leaf area index, ala mean leaf angle (°),
    n leaf structure, psoil fraction of dry soil, rsoil soil brightness; carotenoids = cab/4, view straight down."""
    r = prosail.run_prosail(n, cab, cab / 4, 0.0, cw, cm, lai=lai, lidfa=ala, hspot=0.01, tts=sza, tto=0.0, psi=0.0,
                            typelidf=2, rsoil=rsoil, psoil=psoil, factor="SDR")
    return r if full else SRF @ r
''')),
        ("md", t(
            "## 2. Co model umí\n\nPROSAIL počítá odrazivost porostu z vlastností listů (chlorofyl `cab`, voda `cw`, sušina `cm`, struktura `n`) a porostu (index listové plochy `lai`, průměrný úhel listů `ala`, půda pod porostem). Spektrum v krocích 1 nm převedeme na pásma Sentinelu-2. Spektrální citlivost pásem tu nahrazujeme Gaussovou křivkou, což je přiblížení; přesné křivky zveřejňuje ESA.",
            "## 2. What the model does\n\nPROSAIL computes canopy reflectance from leaf properties (chlorophyll `cab`, water `cw`, dry matter `cm`, structure `n`) and canopy properties (leaf area index `lai`, mean leaf angle `ala`, the soil below). The spectrum in 1 nm steps is converted to Sentinel-2 bands. The band spectral response is replaced here by a Gaussian, which is an approximation; ESA publishes the exact curves.")),
        ("code", t('''
VAR, VALUES = "cab", [10, 30, 50, 70]      # ◀ parametr: proměnná (cab, cw, cm, lai, ala) a její hodnoty
UNITS = {"cab": "µg/cm²", "cw": "cm", "cm": "g/cm²", "lai": "m²/m²", "ala": "°"}
fig, ax = plt.subplots(figsize=(11, 4))
for v in VALUES:
    r = prosail_s2(**{VAR: v}, full=True)
    line, = ax.plot(WL / 1000, r, lw=1, label=f"{VAR} = {v} {UNITS[VAR]}")
    ax.plot(cwl / 1000, SRF @ r, "o", color=line.get_color())
ax.set(xlabel="vlnová délka (µm)", ylabel="odrazivost", title="PROSAIL: čára = celé spektrum, body = pásma Sentinelu-2"); ax.legend(); plt.show()

# citlivost: změna odrazivosti v pásmu, když proměnná přejde z nižší na vyšší hodnotu (ostatní výchozí)
STEPS = {"cab": (20, 60), "cw": (0.005, 0.03), "cm": (0.004, 0.012), "lai": (1, 5), "ala": (40, 70)}
sens = pd.DataFrame({k: prosail_s2(**{k: hi}) - prosail_s2(**{k: lo}) for k, (lo, hi) in STEPS.items()}, index=INV).T
sens.index = [f"{k} {lo}→{hi}" for k, (lo, hi) in STEPS.items()]
sens.round(3)
''', '''
VAR, VALUES = "cab", [10, 30, 50, 70]      # ◀ parameter: variable (cab, cw, cm, lai, ala) and its values
UNITS = {"cab": "µg/cm²", "cw": "cm", "cm": "g/cm²", "lai": "m²/m²", "ala": "°"}
fig, ax = plt.subplots(figsize=(11, 4))
for v in VALUES:
    r = prosail_s2(**{VAR: v}, full=True)
    line, = ax.plot(WL / 1000, r, lw=1, label=f"{VAR} = {v} {UNITS[VAR]}")
    ax.plot(cwl / 1000, SRF @ r, "o", color=line.get_color())
ax.set(xlabel="wavelength (µm)", ylabel="reflectance", title="PROSAIL: line = full spectrum, dots = Sentinel-2 bands"); ax.legend(); plt.show()

# sensitivity: change in band reflectance when the variable goes from the lower to the higher value (others at default)
STEPS = {"cab": (20, 60), "cw": (0.005, 0.03), "cm": (0.004, 0.012), "lai": (1, 5), "ala": (40, 70)}
sens = pd.DataFrame({k: prosail_s2(**{k: hi}) - prosail_s2(**{k: lo}) for k, (lo, hi) in STEPS.items()}, index=INV).T
sens.index = [f"{k} {lo}→{hi}" for k, (lo, hi) in STEPS.items()]
sens.round(3)
''')),
        ("task", t(
            "Spusť buňku pro `cab`, `cw`, `cm`, `lai` a `ala`. Podle grafů a tabulky citlivosti řekni, která pásma Sentinelu-2 nesou informaci o chlorofylu, o vodě v listech a o LAI. Které dvě proměnné mění red edge a NIR skoro stejně, jen s opačným znaménkem, a co to znamená pro odhad LAI z jednoho snímku?",
            "Run the cell for `cab`, `cw`, `cm`, `lai` and `ala`. From the plots and the sensitivity table, say which Sentinel-2 bands carry information on chlorophyll, leaf water and LAI. Which two variables change the red edge and NIR almost equally but with opposite sign, and what does this mean for estimating LAI from one image?")),
        ("md", t(
            "## 3. Nasycení indexů v modelu\n\nNecháme LAI růst od 0 do 7 pro tři obsahy chlorofylu a sledujeme NDVI, NDRE a CIre = NIR/RE1 − 1 (Gitelson a kol. 2005). Tabulka ukazuje, při jakém LAI index dosáhne 90 % rozdílu mezi holou půdou a LAI 7, a jak moc index posune změna chlorofylu, vztaženo k tomuto rozdílu.",
            "## 3. Index saturation in the model\n\nWe let LAI grow from 0 to 7 for three chlorophyll contents and follow NDVI, NDRE and CIre = NIR/RE1 − 1 (Gitelson et al. 2005). The table shows at what LAI the index reaches 90 % of the difference between bare soil and LAI 7, and how much a change in chlorophyll shifts the index, relative to that difference.")),
        ("code", t('''
INDICES = {                                                            # ◀ parametr: indexy; přidej vlastní, např. MTCI
    "NDVI": lambda b: (b["nir"] - b["red"]) / (b["nir"] + b["red"]),
    "NDRE": lambda b: (b["nir"] - b["rededge1"]) / (b["nir"] + b["rededge1"]),
    "CIre": lambda b: b["nir"] / b["rededge1"] - 1,
}
LAIS = np.arange(0, 7.01, 0.25)
CABS = [20, 40, 60]
sim = {cab: [dict(zip(INV, prosail_s2(cab=cab, lai=l))) for l in LAIS] for cab in CABS}
fig, ax = plt.subplots(1, len(INDICES), figsize=(4.2 * len(INDICES), 3.6))
rows = {}
for a, (name, f) in zip(ax, INDICES.items()):
    curves = {cab: np.array([f(b) for b in sim[cab]]) for cab in CABS}
    for cab, v in curves.items():
        a.plot(LAIS, v, label=f"cab {cab}")
        rel = (v - v[0]) / (v[-1] - v[0])                            # 0 = holá půda, 1 = LAI 7
        rows.setdefault(name, {})[f"LAI na 90 % (cab {cab})"] = LAIS[np.argmax(rel >= 0.9)]
    i3, v40 = list(LAIS).index(3.0), curves[40]
    rows[name]["vliv cab 20–60 při LAI 3"] = (curves[60][i3] - curves[20][i3]) / (v40[-1] - v40[0])
    a.set(xlabel="LAI", title=name); a.legend()
plt.tight_layout(); plt.show()
pd.DataFrame(rows).T.round(2)
''', '''
INDICES = {                                                            # ◀ parameter: indices; add your own, e.g. MTCI
    "NDVI": lambda b: (b["nir"] - b["red"]) / (b["nir"] + b["red"]),
    "NDRE": lambda b: (b["nir"] - b["rededge1"]) / (b["nir"] + b["rededge1"]),
    "CIre": lambda b: b["nir"] / b["rededge1"] - 1,
}
LAIS = np.arange(0, 7.01, 0.25)
CABS = [20, 40, 60]
sim = {cab: [dict(zip(INV, prosail_s2(cab=cab, lai=l))) for l in LAIS] for cab in CABS}
fig, ax = plt.subplots(1, len(INDICES), figsize=(4.2 * len(INDICES), 3.6))
rows = {}
for a, (name, f) in zip(ax, INDICES.items()):
    curves = {cab: np.array([f(b) for b in sim[cab]]) for cab in CABS}
    for cab, v in curves.items():
        a.plot(LAIS, v, label=f"cab {cab}")
        rel = (v - v[0]) / (v[-1] - v[0])                            # 0 = bare soil, 1 = LAI 7
        rows.setdefault(name, {})[f"LAI at 90 % (cab {cab})"] = LAIS[np.argmax(rel >= 0.9)]
    i3, v40 = list(LAIS).index(3.0), curves[40]
    rows[name]["effect of cab 20–60 at LAI 3"] = (curves[60][i3] - curves[20][i3]) / (v40[-1] - v40[0])
    a.set(xlabel="LAI", title=name); a.legend()
plt.tight_layout(); plt.show()
pd.DataFrame(rows).T.round(2)
''')),
        ("task", t(
            "Při jakém LAI se nasytí NDVI a při jakém NDRE a CIre? Proč se indexy s červenou hranou nasycují později? Jakou cenu za to platí (poslední sloupec)? Přidej do `INDICES` vlastní index, např. MTCI = (B6 − B5)/(B5 − B4), tj. `(b[\"rededge2\"] - b[\"rededge1\"]) / (b[\"rededge1\"] - b[\"red\"])`, a zařaď ho mezi ostatní.",
            "At what LAI does NDVI saturate, and at what LAI NDRE and CIre? Why do red-edge indices saturate later? What price do they pay for it (last column)? Add your own index to `INDICES`, e.g. MTCI = (B6 − B5)/(B5 − B4), i.e. `(b[\"rededge2\"] - b[\"rededge1\"]) / (b[\"rededge1\"] - b[\"red\"])`, and place it among the others.")),
        ("md", t(
            "## 4. Tabulka simulací a jeden pixel\n\nModel neumí počítat pozpátku. Proto spustíme tisíce simulací s náhodnými hodnotami proměnných v zadaných rozsazích a pro pixel hledáme ty, jejichž pásma se nejvíc podobají naměřeným (nejmenší RMSE). Rozsahy jsou apriorní znalost: co o porostu víme předem. Pro každý snímek se tabulka počítá s jeho výškou Slunce.",
            "## 4. A table of simulations and one pixel\n\nThe model cannot run backwards. So we run thousands of simulations with random variable values within given ranges, and for a pixel we look for those whose bands are most similar to the measured ones (smallest RMSE). The ranges are prior knowledge: what we know about the canopy in advance. For each image the table is computed with its solar elevation.")),
        ("code", t('''
N_LUT = 20000                                                          # ◀ parametr: počet simulací v tabulce
RANGES = {"n": (1.2, 2.2), "cab": (10, 80), "cw": (0.002, 0.04), "cm": (0.002, 0.015),
          "lai": (0, 7), "ala": (30, 80), "psoil": (0, 1), "rsoil": (0.5, 1.5)}   # ◀ parametr: rozsahy proměnných (apriorní znalost)
rng = np.random.default_rng(0)
lut = pd.DataFrame({k: rng.uniform(lo, hi, N_LUT) for k, (lo, hi) in RANGES.items()})
t0 = time.time()
LUT = {day: np.array([prosail_s2(sza=s["sza"], **p) for p in lut.to_dict("records")]) for day, s in scenes.items()}
print(f"{N_LUT} simulací pro {len(DAYS)} snímky za {time.time() - t0:.0f} s")
''', '''
N_LUT = 20000                                                          # ◀ parameter: number of simulations in the table
RANGES = {"n": (1.2, 2.2), "cab": (10, 80), "cw": (0.002, 0.04), "cm": (0.002, 0.015),
          "lai": (0, 7), "ala": (30, 80), "psoil": (0, 1), "rsoil": (0.5, 1.5)}   # ◀ parameter: variable ranges (prior knowledge)
rng = np.random.default_rng(0)
lut = pd.DataFrame({k: rng.uniform(lo, hi, N_LUT) for k, (lo, hi) in RANGES.items()})
t0 = time.time()
LUT = {day: np.array([prosail_s2(sza=s["sza"], **p) for p in lut.to_dict("records")]) for day, s in scenes.items()}
print(f"{N_LUT} simulations for {len(DAYS)} images in {time.time() - t0:.0f} s")
''')),
        ("code", t('''
K = 50                                     # ◀ parametr: kolik nejlepších řešení z tabulky vzít
PLON, PLAT = 14.3516, 50.1632              # ◀ parametr: bod (pole u Únětic); zkus les 14.366, 50.148
day = DAYS[0]
x, y = Transformer.from_crs(4326, grid[1], always_xy=True).transform(PLON, PLAT)
col, row = [int(v) for v in ~grid[0] * (x, y)]
obs = np.array([scenes[day]["refl"][b][row, col] for b in INV])
rmse = np.sqrt(((LUT[day] - obs) ** 2).mean(1))
best = np.argsort(rmse)[:K]
sol = lut.iloc[best].assign(ccc=lambda d: d.lai * d.cab, rmse=rmse[best])
print(f"{day}, bod {PLON}, {PLAT}: NDVI {(obs[6] - obs[2]) / (obs[6] + obs[2]):.2f}, nejlepší shoda RMSE {rmse[best[0]]:.4f}")
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
for i in best[:10]:
    ax[0].plot(cwl / 1000, LUT[day][i], color="0.7", lw=1)
ax[0].plot(cwl / 1000, obs, "ko-", label="Sentinel-2"); ax[0].set(xlabel="vlnová délka (µm)", ylabel="odrazivost", title="pixel a 10 nejlepších simulací"); ax[0].legend()
for a, v in zip(ax[1:], ["ala", "cab"]):
    s = a.scatter(sol[v], sol.lai, c=sol.rmse, cmap="viridis_r"); a.set(xlabel=v, ylabel="LAI", title=f"{K} nejlepších řešení")
fig.colorbar(s, ax=ax[2], label="RMSE"); plt.show()
summary = sol[["lai", "cab", "ccc", "ala", "cw"]].describe(percentiles=[0.05, 0.5, 0.95]).T[["5%", "50%", "95%"]]
summary["variační koeficient"] = sol[["lai", "cab", "ccc", "ala", "cw"]].std() / sol[["lai", "cab", "ccc", "ala", "cw"]].mean()
summary.round(3)
''', '''
K = 50                                     # ◀ parameter: how many best solutions from the table to keep
PLON, PLAT = 14.3516, 50.1632              # ◀ parameter: point (field near Únětice); try forest 14.366, 50.148
day = DAYS[0]
x, y = Transformer.from_crs(4326, grid[1], always_xy=True).transform(PLON, PLAT)
col, row = [int(v) for v in ~grid[0] * (x, y)]
obs = np.array([scenes[day]["refl"][b][row, col] for b in INV])
rmse = np.sqrt(((LUT[day] - obs) ** 2).mean(1))
best = np.argsort(rmse)[:K]
sol = lut.iloc[best].assign(ccc=lambda d: d.lai * d.cab, rmse=rmse[best])
print(f"{day}, point {PLON}, {PLAT}: NDVI {(obs[6] - obs[2]) / (obs[6] + obs[2]):.2f}, best match RMSE {rmse[best[0]]:.4f}")
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
for i in best[:10]:
    ax[0].plot(cwl / 1000, LUT[day][i], color="0.7", lw=1)
ax[0].plot(cwl / 1000, obs, "ko-", label="Sentinel-2"); ax[0].set(xlabel="wavelength (µm)", ylabel="reflectance", title="pixel and the 10 best simulations"); ax[0].legend()
for a, v in zip(ax[1:], ["ala", "cab"]):
    s = a.scatter(sol[v], sol.lai, c=sol.rmse, cmap="viridis_r"); a.set(xlabel=v, ylabel="LAI", title=f"{K} best solutions")
fig.colorbar(s, ax=ax[2], label="RMSE"); plt.show()
summary = sol[["lai", "cab", "ccc", "ala", "cw"]].describe(percentiles=[0.05, 0.5, 0.95]).T[["5%", "50%", "95%"]]
summary["coefficient of variation"] = sol[["lai", "cab", "ccc", "ala", "cw"]].std() / sol[["lai", "cab", "ccc", "ala", "cw"]].mean()
summary.round(3)
''')),
        ("task", t(
            "Jak široké je rozpětí LAI mezi nejlepšími řešeními a jak souvisí s úhlem listů a chlorofylem (grafy vpravo)? Porovnej variační koeficient `lai`, `cab` a jejich součinu `ccc` (chlorofyl v porostu, µg na cm² půdy). Proč je součin určen lépe než každá složka zvlášť? Zkus `K = 10` a `K = 200` a bod v lese.",
            "How wide is the LAI range among the best solutions and how does it relate to leaf angle and chlorophyll (plots on the right)? Compare the coefficient of variation of `lai`, `cab` and their product `ccc` (canopy chlorophyll, µg per cm² of ground). Why is the product better determined than either part? Try `K = 10` and `K = 200` and a forest point.")),
        ("md", t(
            "## 5. Mapa LAI a kde model nesedí\n\nStejný postup pro všechny pixely výřezu. Pro každý pixel dostaneme medián LAI z nejlepších řešení, jejich směrodatnou odchylku jako míru nejistoty a RMSE nejlepší simulace jako míru, jak dobře model pixel vůbec vysvětlí.",
            "## 5. LAI map and where the model does not fit\n\nThe same procedure for all pixels of the window. For each pixel we get the median LAI of the best solutions, their standard deviation as a measure of uncertainty, and the RMSE of the best simulation as a measure of how well the model explains the pixel at all.")),
        ("code", t('''
def invert(day, k=K):
    """Pro každý pixel najde k simulací nejbližších v odrazivosti (nejmenší RMSE) a vrátí medián LAI, jeho rozptyl, obsah chlorofylu v porostu a RMSE."""
    X = np.dstack([scenes[day]["refl"][b] for b in INV]).reshape(-1, len(INV))
    d, idx = NearestNeighbors(n_neighbors=k).fit(LUT[day]).kneighbors(X)
    lai, cab = lut.lai.values[idx], lut.cab.values[idx]
    sh = wc.shape
    return dict(lai=np.median(lai, 1).reshape(sh), lai_sd=lai.std(1).reshape(sh),
                ccc=np.median(lai * cab, 1).reshape(sh), rmse=(d[:, 0] / np.sqrt(len(INV))).reshape(sh))

t0 = time.time()
inv = {day: invert(day) for day in DAYS}
print(f"inverze {wc.size} pixelů × {len(DAYS)} snímky za {time.time() - t0:.0f} s")
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
for a, day in zip(ax, DAYS):
    im = a.imshow(np.where(scenes[day]["clear"], inv[day]["lai"], np.nan), cmap="YlGn", vmin=0, vmax=5); a.set_title(f"LAI {day}"); fig.colorbar(im, ax=a, shrink=0.8)
im = ax[2].imshow(inv[DAYS[-1]]["rmse"], cmap="magma", vmin=0, vmax=0.03); ax[2].set_title(f"RMSE nejlepší simulace {DAYS[-1]}"); fig.colorbar(im, ax=ax[2], shrink=0.8)
for a in ax: a.axis("off")
plt.show()
tab = pd.DataFrame({(day, q): {name: np.median(inv[day][q][scenes[day]["clear"] & (wc == code)]) for code, name in CLASSES.items()}
                    for day in DAYS for q in ["lai", "lai_sd", "rmse"]})
tab.round(3)
''', '''
def invert(day, k=K):
    """For every pixel find the k simulations closest in reflectance (smallest RMSE) and return the median LAI, its spread, canopy chlorophyll content and RMSE."""
    X = np.dstack([scenes[day]["refl"][b] for b in INV]).reshape(-1, len(INV))
    d, idx = NearestNeighbors(n_neighbors=k).fit(LUT[day]).kneighbors(X)
    lai, cab = lut.lai.values[idx], lut.cab.values[idx]
    sh = wc.shape
    return dict(lai=np.median(lai, 1).reshape(sh), lai_sd=lai.std(1).reshape(sh),
                ccc=np.median(lai * cab, 1).reshape(sh), rmse=(d[:, 0] / np.sqrt(len(INV))).reshape(sh))

t0 = time.time()
inv = {day: invert(day) for day in DAYS}
print(f"inversion of {wc.size} pixels × {len(DAYS)} images in {time.time() - t0:.0f} s")
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
for a, day in zip(ax, DAYS):
    im = a.imshow(np.where(scenes[day]["clear"], inv[day]["lai"], np.nan), cmap="YlGn", vmin=0, vmax=5); a.set_title(f"LAI {day}"); fig.colorbar(im, ax=a, shrink=0.8)
im = ax[2].imshow(inv[DAYS[-1]]["rmse"], cmap="magma", vmin=0, vmax=0.03); ax[2].set_title(f"RMSE of the best simulation {DAYS[-1]}"); fig.colorbar(im, ax=ax[2], shrink=0.8)
for a in ax: a.axis("off")
plt.show()
tab = pd.DataFrame({(day, q): {name: np.median(inv[day][q][scenes[day]["clear"] & (wc == code)]) for code, name in CLASSES.items()}
                    for day in DAYS for q in ["lai", "lai_sd", "rmse"]})
tab.round(3)
''')),
        ("task", t(
            "Kde je RMSE největší a proč? Proč u vody vyjde nějaké LAI, i když tam žádné listy nejsou, a proč zástavba sedí skoro stejně dobře jako louka? Les tu vychází s LAI kolem 2, zatímco souhrn pozemních měření (Asner a kol. 2003) uvádí pro stálezelené lesy mírného pásu průměr 5,1 až 6,7. Které předpoklady PROSAILu (jedna souvislá vrstva listů, žádné kmeny, mezery ani stíny korun) k rozdílu přispívají?",
            "Where is the RMSE largest and why? Why does water get some LAI although there are no leaves, and why does built-up land fit almost as well as grassland? The forest comes out with LAI around 2, while a synthesis of ground measurements (Asner et al. 2003) gives a mean of 5.1 to 6.7 for temperate evergreen forests. Which assumptions of PROSAIL (one continuous layer of leaves, no trunks, gaps or crown shadows) contribute to the difference?")),
        ("md", t(
            "## 6. LAI, NDVI a nejistota na skutečných datech",
            "## 6. LAI, NDVI and uncertainty in real data")),
        ("code", t('''
veg = np.isin(wc, [10, 30, 40])
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
for day in DAYS:
    r = scenes[day]["refl"]; m = veg & scenes[day]["clear"]
    ndvi = ((r["nir"] - r["red"]) / (r["nir"] + r["red"]))[m]
    lai, sd = inv[day]["lai"][m], inv[day]["lai_sd"][m]
    bins = np.arange(0.2, 0.96, 0.05); k = np.digitize(ndvi, bins)
    mid = [(bins[i - 1] + bins[i]) / 2 for i in range(1, len(bins)) if (k == i).sum() > 50]
    ax[0].plot(mid, [np.median(lai[k == i]) for i in range(1, len(bins)) if (k == i).sum() > 50], "o-", label=day)
    ax[1].plot(mid, [np.median(sd[k == i]) for i in range(1, len(bins)) if (k == i).sum() > 50], "o-", label=day)
ax[0].set(xlabel="NDVI", ylabel="medián LAI z inverze", title="LAI podle NDVI (les, louky, pole)"); ax[0].legend()
ax[1].set(xlabel="NDVI", ylabel="medián směrodatné odchylky LAI", title="nejistota LAI podle NDVI"); ax[1].legend()
plt.show()
r0, r1 = scenes[DAYS[0]]["refl"], scenes[DAYS[1]]["refl"]
ndvi0, ndvi1 = [(r["nir"] - r["red"]) / (r["nir"] + r["red"]) for r in (r0, r1)]
both = scenes[DAYS[0]]["clear"] & scenes[DAYS[1]]["clear"]
pd.DataFrame({name: {"NDVI " + DAYS[0]: np.median(ndvi0[both & (wc == c)]), "NDVI " + DAYS[1]: np.median(ndvi1[both & (wc == c)]),
                     "LAI " + DAYS[0]: np.median(inv[DAYS[0]]["lai"][both & (wc == c)]), "LAI " + DAYS[1]: np.median(inv[DAYS[1]]["lai"][both & (wc == c)])}
              for c, name in CLASSES.items() if c in (10, 30, 40)}).T.round(2)
''', '''
veg = np.isin(wc, [10, 30, 40])
fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
for day in DAYS:
    r = scenes[day]["refl"]; m = veg & scenes[day]["clear"]
    ndvi = ((r["nir"] - r["red"]) / (r["nir"] + r["red"]))[m]
    lai, sd = inv[day]["lai"][m], inv[day]["lai_sd"][m]
    bins = np.arange(0.2, 0.96, 0.05); k = np.digitize(ndvi, bins)
    mid = [(bins[i - 1] + bins[i]) / 2 for i in range(1, len(bins)) if (k == i).sum() > 50]
    ax[0].plot(mid, [np.median(lai[k == i]) for i in range(1, len(bins)) if (k == i).sum() > 50], "o-", label=day)
    ax[1].plot(mid, [np.median(sd[k == i]) for i in range(1, len(bins)) if (k == i).sum() > 50], "o-", label=day)
ax[0].set(xlabel="NDVI", ylabel="median LAI from the inversion", title="LAI by NDVI (forest, grassland, cropland)"); ax[0].legend()
ax[1].set(xlabel="NDVI", ylabel="median standard deviation of LAI", title="LAI uncertainty by NDVI"); ax[1].legend()
plt.show()
r0, r1 = scenes[DAYS[0]]["refl"], scenes[DAYS[1]]["refl"]
ndvi0, ndvi1 = [(r["nir"] - r["red"]) / (r["nir"] + r["red"]) for r in (r0, r1)]
both = scenes[DAYS[0]]["clear"] & scenes[DAYS[1]]["clear"]
pd.DataFrame({name: {"NDVI " + DAYS[0]: np.median(ndvi0[both & (wc == c)]), "NDVI " + DAYS[1]: np.median(ndvi1[both & (wc == c)]),
                     "LAI " + DAYS[0]: np.median(inv[DAYS[0]]["lai"][both & (wc == c)]), "LAI " + DAYS[1]: np.median(inv[DAYS[1]]["lai"][both & (wc == c)])}
              for c, name in CLASSES.items() if c in (10, 30, 40)}).T.round(2)
''')),
        ("task", t(
            "Od jakého NDVI roste nejistota LAI nejrychleji a jak to souvisí s nasycením z kroku 3? Jak se mezi květnem a červencem změnilo NDVI a LAI na polích, loukách a v lese? Proč by samotné NDVI podcenilo rozdíl mezi dvěma hustými porosty?",
            "From what NDVI does the LAI uncertainty grow fastest, and how does this relate to the saturation in step 3? How did NDVI and LAI change between May and July on cropland, grassland and in the forest? Why would NDVI alone underestimate the difference between two dense canopies?")),
        ("task", t(
            "+ Zužte rozsahy v `RANGES` podle toho, co o porostu víš (např. `ala` 50–65, `cab` 30–60), a spusť kroky 4 až 6 znovu. Jak se změní nejistota LAI? Co se stane, když apriorní znalost neplatí, třeba pro les s jiným úhlem listů?",
            "+ Narrow the ranges in `RANGES` to what you know about the canopy (e.g. `ala` 50–65, `cab` 30–60) and run steps 4 to 6 again. How does the LAI uncertainty change? What happens when the prior knowledge is wrong, for example for a forest with a different leaf angle?")),
    ]
