import re

# místa, pro která se notebook staví: přípona souboru → letní a zimní scéna Landsatu 8, výřez, scéna Sentinelu-2 a popisy
VARIANTS = {
    "": dict(l8s="LC08_L1TP_191025_20190626_20190705_01_T1", l8w="LC08_L1TP_191025_20190218_20190222_01_T1", x0=452490, y0=5541690,
             els=60, elw=26, l8d_cs="26. 6. 2019", l8d_en="26 June 2019", l8wd_cs="18. 2. 2019", l8wd_en="18 Feb 2019",
             s2="S2B_33UVR_20190625_0_L2A", s2d_cs="25. 6. 2019", s2d_en="25 June 2019", s2rel_cs="o den dřív", s2rel_en="one day earlier",
             s2rel2_cs="snímek o den dřív a", s2rel2_en="an image taken one day earlier and",
             water_cs="Vltava a nádrže", water_en="The Vltava and reservoirs", over_cs="nad Prahou", over_en="Prague", win_cs="kolem centra Prahy", win_en="around central Prague"),
    "brno": dict(l8s="LC08_L1TP_190026_20200808_20200821_01_T1", l8w="LC08_L1TP_190026_20190227_20190309_01_T1", x0=607620, y0=5446530,
                 els=54, elw=30, l8d_cs="8. 8. 2020", l8d_en="8 Aug 2020", l8wd_cs="27. 2. 2019", l8wd_en="27 Feb 2019",
                 s2="S2B_33UXQ_20200808_0_L2A", s2d_cs="8. 8. 2020", s2d_en="8 Aug 2020", s2rel_cs="týž den", s2rel_en="the same day",
                 s2rel2_cs="snímek pořízený asi o 20 minut později a", s2rel2_en="an image taken about 20 minutes later and",
                 water_cs="Brněnská přehrada a Svratka", water_en="The Brno reservoir and the Svratka", over_cs="nad Brnem", over_en="Brno",
                 win_cs="od Brněnské přehrady k centru Brna", win_en="from the Brno reservoir to central Brno"),
    "hluboka": dict(l8s="LC08_L1TP_191026_20190626_20190705_01_T1", l8w="LC08_L1TP_191026_20190218_20190222_01_T1", x0=453090, y0=5427180,
                    els=61, elw=27, l8d_cs="26. 6. 2019", l8d_en="26 June 2019", l8wd_cs="18. 2. 2019", l8wd_en="18 Feb 2019",
                    s2="S2B_33UVQ_20190625_0_L2A", s2d_cs="25. 6. 2019", s2d_en="25 June 2019", s2rel_cs="o den dřív", s2rel_en="one day earlier",
                    s2rel2_cs="snímek o den dřív a", s2rel2_en="an image taken one day earlier and",
                    water_cs="Vltava a rybníky", water_en="The Vltava and the fishponds", over_cs="nad Hlubokou nad Vltavou", over_en="Hluboká nad Vltavou",
                    win_cs="kolem Hluboké nad Vltavou", win_en="around Hluboká nad Vltavou"),
}


def meta(P):
    return {
        "version": "1.0",
        "minutes": 45,
        "title": {"cs": "Od DN k odrazivosti: Landsat 8 " + P["over_cs"], "en": "From DN to reflectance: Landsat 8 over " + P["over_en"]},
        "visual": {"cs": "Od DN k odrazivosti", "en": "From DN to reflectance"},
        "lead": {
            "cs": "Vizuál prochází řetězec od digitálního čísla přes zář k odrazivosti nad atmosférou (TOA) a na povrchu (BOA) a ukazuje, co opraví metoda tmavého objektu (DOS) a empirická přímka. Tady celý řetězec spočítáš na dvou skutečných snímcích Landsatu 8 " + P["over_cs"] + " a výsledek porovnáš s odrazivostí Sentinelu-2 L2A z téhož týdne.",
            "en": "The visual walks through the chain from digital number to radiance to top-of-atmosphere (TOA) and surface (BOA) reflectance and shows what dark object subtraction (DOS) and the empirical line correct. Here you compute the whole chain on two real Landsat 8 images of " + P["over_en"] + " and compare the result with Sentinel-2 L2A reflectance from the same week.",
        },
        "goal": {
            "cs": "převést DN na zář a odrazivost TOA, ukázat, proč DN ze dvou dnů nejsou srovnatelná, změřit vliv atmosféry na vodě a porovnat korekci DOS a empirickou přímku s odrazivostí na povrchu.",
            "en": "convert DN to radiance and TOA reflectance, show why DN from two days are not comparable, measure the atmospheric effect over water, and compare DOS and the empirical line with surface reflectance.",
        },
        "data": {
            "cs": f"Landsat 8 OLI Collection 1 Level-1 z veřejného archivu Google Cloud: `{P['l8s']}` ({P['l8d_cs']}, výška Slunce {P['els']}°) a `{P['l8w']}` ({P['l8wd_cs']}, výška Slunce {P['elw']}°), pásma B1–B7, BQA a MTL. Pro srovnání Sentinel-2 L2A `{P['s2']}` ({P['s2d_cs']}) z Earth Search. Výřez 12 × 12 km {P['win_cs']}, asi 25 MB.",
            "en": f"Landsat 8 OLI Collection 1 Level-1 from the Google Cloud public archive: `{P['l8s']}` ({P['l8d_en']}, sun elevation {P['els']}°) and `{P['l8w']}` ({P['l8wd_en']}, sun elevation {P['elw']}°), bands B1–B7, BQA and MTL. For comparison Sentinel-2 L2A `{P['s2']}` ({P['s2d_en']}) from Earth Search. A 12 × 12 km window {P['win_en']}, about 25 MB.",
        },
        "sources": {
            "cs": [
                "Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; veřejný archiv Google Cloud (`gcp-public-data-landsat`). Data USGS jsou bez omezení užití, s uvedením zdroje.",
                "USGS (2019). *Landsat 8 (L8) Data Users Handbook*, verze 5.0, kap. 5 (převod DN na zář a odrazivost TOA).",
                "Copernicus Sentinel-2 data " + P["s2d_en"][-4:] + ", ESA (L2A, Sen2Cor), registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.",
                "Chavez, P. S. (1988). An improved dark-object subtraction technique for atmospheric scattering correction of multispectral data. *Remote Sensing of Environment* 24, 459–479. https://doi.org/10.1016/0034-4257(88)90019-3",
                "Chavez, P. S. (1996). Image-based atmospheric corrections – revisited and improved. *Photogrammetric Engineering and Remote Sensing* 62(9), 1025–1036.",
                "Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20, 2653–2662. https://doi.org/10.1080/014311699211994",
            ],
            "en": [
                "Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; Google Cloud public archive (`gcp-public-data-landsat`). USGS data have no use restrictions, attribution requested.",
                "USGS (2019). *Landsat 8 (L8) Data Users Handbook*, version 5.0, ch. 5 (DN to radiance and TOA reflectance).",
                "Copernicus Sentinel-2 data " + P["s2d_en"][-4:] + ", ESA (L2A, Sen2Cor), AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.",
                "Chavez, P. S. (1988). An improved dark-object subtraction technique for atmospheric scattering correction of multispectral data. *Remote Sensing of Environment* 24, 459–479. https://doi.org/10.1016/0034-4257(88)90019-3",
                "Chavez, P. S. (1996). Image-based atmospheric corrections – revisited and improved. *Photogrammetric Engineering and Remote Sensing* 62(9), 1025–1036.",
                "Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20, 2653–2662. https://doi.org/10.1080/014311699211994",
            ],
        },
    }


def cells(t, P):
    out = [
        ("md", t("## 1. Příprava a data", "## 1. Setup and data")),
        ("code", "%pip install -q rasterio"),
        ("code", t('''
import requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling

GCS = "https://storage.googleapis.com/gcp-public-data-landsat/LC08/01/@PATH@/@ROW@/"
SCENES = {"léto": "@L8S@", "zima": "@L8W@"}
X0, Y0, SIZE = @X0@, @Y0@, 12000          # levý dolní roh výřezu v UTM 33N (m) a jeho strana
BANDS = {1: "pobřežní 443", 2: "modrá 482", 3: "zelená 561", 4: "červená 655", 5: "NIR 865", 6: "SWIR1 1609", 7: "SWIR2 2201"}

def mtl(scene):
    txt = requests.get(f"{GCS}{scene}/{scene}_MTL.txt", timeout=60).text
    return {k.strip(): v.strip().strip('"') for k, v in (l.split(" = ") for l in txt.splitlines() if " = " in l)}

def read(scene, band):
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2):
        with rasterio.open(f"/vsicurl/{GCS}{scene}/{scene}_{band}.TIF") as r:
            w = rasterio.windows.from_bounds(X0, Y0, X0 + SIZE, Y0 + SIZE, r.transform).round_offsets().round_lengths()
            read.transform = r.window_transform(w)
            return r.read(1, window=w).astype(float)

L8 = {}
for season, scene in SCENES.items():
    meta = mtl(scene)
    dn = {b: read(scene, f"B{b}") for b in BANDS}
    L8_transform = read.transform
    qa = read(scene, "BQA").astype(int)
    ok = ((qa >> 4) & 1 == 0) & ((qa >> 7) & 3 < 3) & (dn[1] > 0)     # bez mraků a jistých stínů
    L8[season] = {"meta": meta, "dn": dn, "ok": ok, "transform": L8_transform}
    print(f"{season}: {scene}, výška Slunce {float(meta['SUN_ELEVATION']):.1f}°, vzdálenost Země–Slunce {meta['EARTH_SUN_DISTANCE']} AU, jasné pixely {ok.mean():.1%}")
''', '''
import requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling

GCS = "https://storage.googleapis.com/gcp-public-data-landsat/LC08/01/@PATH@/@ROW@/"
SCENES = {"summer": "@L8S@", "winter": "@L8W@"}
X0, Y0, SIZE = @X0@, @Y0@, 12000          # lower-left corner of the window in UTM 33N (m) and its side
BANDS = {1: "coastal 443", 2: "blue 482", 3: "green 561", 4: "red 655", 5: "NIR 865", 6: "SWIR1 1609", 7: "SWIR2 2201"}

def mtl(scene):
    txt = requests.get(f"{GCS}{scene}/{scene}_MTL.txt", timeout=60).text
    return {k.strip(): v.strip().strip('"') for k, v in (l.split(" = ") for l in txt.splitlines() if " = " in l)}

def read(scene, band):
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2):
        with rasterio.open(f"/vsicurl/{GCS}{scene}/{scene}_{band}.TIF") as r:
            w = rasterio.windows.from_bounds(X0, Y0, X0 + SIZE, Y0 + SIZE, r.transform).round_offsets().round_lengths()
            read.transform = r.window_transform(w)
            return r.read(1, window=w).astype(float)

L8 = {}
for season, scene in SCENES.items():
    meta = mtl(scene)
    dn = {b: read(scene, f"B{b}") for b in BANDS}
    L8_transform = read.transform
    qa = read(scene, "BQA").astype(int)
    ok = ((qa >> 4) & 1 == 0) & ((qa >> 7) & 3 < 3) & (dn[1] > 0)     # no clouds and no high-confidence shadows
    L8[season] = {"meta": meta, "dn": dn, "ok": ok, "transform": L8_transform}
    print(f"{season}: {scene}, sun elevation {float(meta['SUN_ELEVATION']):.1f}°, Earth–Sun distance {meta['EARTH_SUN_DISTANCE']} AU, clear pixels {ok.mean():.1%}")
''')),
        ("md", t(
            "## 2. Z DN na zář a odrazivost TOA\n\nZář: L = M_L · DN + A_L. Odrazivost TOA: ρ = (M_ρ · DN + A_ρ) / sin(výška Slunce). Koeficienty jsou v souboru MTL; v M_ρ je už započtena vzdálenost Země–Slunce i sluneční ozáření pásma.",
            "## 2. From DN to radiance and TOA reflectance\n\nRadiance: L = M_L · DN + A_L. TOA reflectance: ρ = (M_ρ · DN + A_ρ) / sin(sun elevation). The coefficients are in the MTL file; M_ρ already includes the Earth–Sun distance and the solar irradiance of the band.")),
        ("code", t('''
for s in L8.values():
    m, dn = s["meta"], s["dn"]
    sun = np.sin(np.radians(float(m["SUN_ELEVATION"])))
    s["rad"] = {b: float(m[f"RADIANCE_MULT_BAND_{b}"]) * dn[b] + float(m[f"RADIANCE_ADD_BAND_{b}"]) for b in BANDS}
    s["toa"] = {b: (float(m[f"REFLECTANCE_MULT_BAND_{b}"]) * dn[b] + float(m[f"REFLECTANCE_ADD_BAND_{b}"])) / sun for b in BANDS}

rows = []
for b, name in BANDS.items():
    r = {"pásmo": f"B{b} {name}"}
    for season, s in L8.items():
        ok = s["ok"]
        r[f"DN {season}"] = np.median(s["dn"][b][ok])
        r[f"zář {season}"] = np.median(s["rad"][b][ok])
        r[f"ρ TOA {season}"] = np.median(s["toa"][b][ok])
    rows.append(r)
tab = pd.DataFrame(rows).set_index("pásmo")
tab["poměr DN léto/zima"] = tab["DN léto"] / tab["DN zima"]
tab["poměr ρ léto/zima"] = tab["ρ TOA léto"] / tab["ρ TOA zima"]
tab.round(3)
''', '''
for s in L8.values():
    m, dn = s["meta"], s["dn"]
    sun = np.sin(np.radians(float(m["SUN_ELEVATION"])))
    s["rad"] = {b: float(m[f"RADIANCE_MULT_BAND_{b}"]) * dn[b] + float(m[f"RADIANCE_ADD_BAND_{b}"]) for b in BANDS}
    s["toa"] = {b: (float(m[f"REFLECTANCE_MULT_BAND_{b}"]) * dn[b] + float(m[f"REFLECTANCE_ADD_BAND_{b}"])) / sun for b in BANDS}

rows = []
for b, name in BANDS.items():
    r = {"band": f"B{b} {name}"}
    for season, s in L8.items():
        ok = s["ok"]
        r[f"DN {season}"] = np.median(s["dn"][b][ok])
        r[f"radiance {season}"] = np.median(s["rad"][b][ok])
        r[f"ρ TOA {season}"] = np.median(s["toa"][b][ok])
    rows.append(r)
tab = pd.DataFrame(rows).set_index("band")
tab["ratio DN summer/winter"] = tab["DN summer"] / tab["DN winter"]
tab["ratio ρ summer/winter"] = tab["ρ TOA summer"] / tab["ρ TOA winter"]
tab.round(3)
''')),
        ("task", t(
            "O kolik se mediány DN mezi létem a zimou liší a o kolik mediány odrazivosti TOA? Kolik z rozdílu DN vysvětlí jen výška Slunce (porovnej poměr sinů výšek)? Proč se ani odrazivost TOA mezi daty úplně neshoduje (stav porostu, případný sníh, atmosféra)?",
            "How much do the median DN differ between summer and winter, and how much the median TOA reflectance? How much of the DN difference is explained by sun elevation alone (compare the ratio of the sines)? Why does even TOA reflectance not agree completely between the dates (state of vegetation, possible snow, atmosphere)?")),
        ("md", t(
            "## 3. Odrazivost na povrchu ze Sentinelu-2 jako reference\n\nSentinel-2 L2A z @S2D_CS@ (@S2REL_CS@) má odrazivost BOA z modelu Sen2Cor. Převzorkujeme ho na mřížku Landsatu (průměr do pixelu 30 m) a přiřadíme si pásma s podobnou vlnovou délkou. Dokonalou shodu nečekej: jde o jiný senzor s trochu jinými pásmy, @S2REL2_CS@ z jiného úhlu pohledu.",
            "## 3. Surface reflectance from Sentinel-2 as a reference\n\nSentinel-2 L2A from @S2D_EN@ (@S2REL_EN@) has BOA reflectance from the Sen2Cor model. We resample it to the Landsat grid (average into 30 m pixels) and pair bands of similar wavelength. Do not expect a perfect match: it is a different sensor with slightly different bands, @S2REL2_EN@ from a different viewing angle.")),
        ("code", t('''
item = requests.get("https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/@S2@", timeout=60).json()
PAIR = {1: "coastal", 2: "blue", 3: "green", 4: "red", 5: "nir08", 6: "swir16", 7: "swir22"}
shape = L8["léto"]["dn"][1].shape
grid = L8["léto"]["transform"]
def s2(key, res=Resampling.average):
    out = np.zeros(shape, np.float32)
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2):
        with rasterio.open("/vsicurl/" + item["assets"][key]["href"]) as r:
            reproject(rasterio.band(r, 1), out, dst_transform=grid, dst_crs="EPSG:32633", resampling=res)
    return out
p = item["properties"]   # od základní linie zpracování 04.00 mají DN posun +1000, pokud ho katalog ještě neodečetl
off = -1000 if float(p.get("s2:processing_baseline", "0")) >= 4 and not p.get("earthsearch:boa_offset_applied", False) else 0
boa = {b: (s2(k) + off) / 10000 for b, k in PAIR.items()}
scl = s2("scl", Resampling.mode)
summer = L8["léto"]
valid = summer["ok"] & np.isin(scl, [4, 5, 6]) & (boa[1] > 0)
print(f"pixelů pro srovnání: {valid.sum()}")
fig, ax = plt.subplots(1, 2, figsize=(11, 5))
rgb = lambda d: np.clip(np.dstack([d[4], d[3], d[2]]) / 0.25, 0, 1)
ax[0].imshow(rgb(summer["toa"])); ax[0].set_title("Landsat 8, odrazivost TOA, @L8D_CS@")
ax[1].imshow(rgb(boa)); ax[1].set_title("Sentinel-2 L2A, odrazivost BOA, @S2D_CS@")
for a in ax: a.axis("off")
plt.show()
''', '''
item = requests.get("https://earth-search.aws.element84.com/v1/collections/sentinel-2-l2a/items/@S2@", timeout=60).json()
PAIR = {1: "coastal", 2: "blue", 3: "green", 4: "red", 5: "nir08", 6: "swir16", 7: "swir22"}
shape = L8["summer"]["dn"][1].shape
grid = L8["summer"]["transform"]
def s2(key, res=Resampling.average):
    out = np.zeros(shape, np.float32)
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2):
        with rasterio.open("/vsicurl/" + item["assets"][key]["href"]) as r:
            reproject(rasterio.band(r, 1), out, dst_transform=grid, dst_crs="EPSG:32633", resampling=res)
    return out
p = item["properties"]   # since processing baseline 04.00 DN carry a +1000 offset unless the catalogue has removed it
off = -1000 if float(p.get("s2:processing_baseline", "0")) >= 4 and not p.get("earthsearch:boa_offset_applied", False) else 0
boa = {b: (s2(k) + off) / 10000 for b, k in PAIR.items()}
scl = s2("scl", Resampling.mode)
summer = L8["summer"]
valid = summer["ok"] & np.isin(scl, [4, 5, 6]) & (boa[1] > 0)
print(f"pixels for comparison: {valid.sum()}")
fig, ax = plt.subplots(1, 2, figsize=(11, 5))
rgb = lambda d: np.clip(np.dstack([d[4], d[3], d[2]]) / 0.25, 0, 1)
ax[0].imshow(rgb(summer["toa"])); ax[0].set_title("Landsat 8, TOA reflectance, @L8D_EN@")
ax[1].imshow(rgb(boa)); ax[1].set_title("Sentinel-2 L2A, BOA reflectance, @S2D_EN@")
for a in ax: a.axis("off")
plt.show()
''')),
        ("task", t(
            "Porovnej oba obrázky se stejným roztažením barev. Proč působí snímek s odrazivostí TOA světleji, modřeji a méně kontrastně? Které povrchy se mezi TOA a BOA mění nejvíc, tmavé, nebo světlé? Vysvětli to aditivním příspěvkem atmosféry.",
            "Compare the two images with the same colour stretch. Why does the TOA reflectance image look brighter, bluer and less contrasting? Which surfaces change most between TOA and BOA, dark or bright ones? Explain it with the additive contribution of the atmosphere.")),
        ("md", t(
            "## 4. Modrá voda nad atmosférou\n\n@WATER_CS@ jsou v NIR skoro černé. Porovnáme jejich odrazivost TOA a BOA ve všech pásmech: rozdíl je hlavně světlo rozptýlené atmosférou (zář dráhy).",
            "## 4. Blue water above the atmosphere\n\n@WATER_EN@ are almost black in the NIR. We compare their TOA and BOA reflectance in all bands: the difference is mainly light scattered by the atmosphere (path radiance).")),
        ("code", t('''
ndwi = (boa[3] - boa[5]) / (boa[3] + boa[5])
water = valid & (ndwi > 0.3) & (scl == 6)
w = pd.DataFrame({"ρ TOA (Landsat)": [np.median(summer["toa"][b][water]) for b in BANDS],
                  "ρ BOA (Sentinel-2)": [np.median(boa[b][water]) for b in BANDS]}, index=[f"B{b} {n}" for b, n in BANDS.items()])
w["TOA − BOA"] = w.iloc[:, 0] - w.iloc[:, 1]
print(f"vodních pixelů: {water.sum()}")
w.round(4)
''', '''
ndwi = (boa[3] - boa[5]) / (boa[3] + boa[5])
water = valid & (ndwi > 0.3) & (scl == 6)
w = pd.DataFrame({"ρ TOA (Landsat)": [np.median(summer["toa"][b][water]) for b in BANDS],
                  "ρ BOA (Sentinel-2)": [np.median(boa[b][water]) for b in BANDS]}, index=[f"B{b} {n}" for b, n in BANDS.items()])
w["TOA − BOA"] = w.iloc[:, 0] - w.iloc[:, 1]
print(f"water pixels: {water.sum()}")
w.round(4)
''')),
        ("task", t(
            "Jak se rozdíl TOA − BOA nad vodou mění s vlnovou délkou? Porovnej poměr mezi pásmy B1 a B4 s Rayleighovým zákonem (rozptyl ∝ λ⁻⁴). Proč je voda nad atmosférou modrá, i když je na povrchu tmavá ve všech pásmech?",
            "How does TOA − BOA over water change with wavelength? Compare the ratio between bands B1 and B4 with Rayleigh's law (scattering ∝ λ⁻⁴). Why is water blue above the atmosphere although it is dark in all bands at the surface?")),
        ("md", t(
            "## 5. Metoda tmavého objektu (DOS)\n\nPředpokládáme, že nejtmavší pixely ve scéně mají na povrchu odrazivost skoro nulovou (běžně se bere 1 %, Chavez 1996). Co mají navíc, je zář dráhy, a tu odečteme od celé scény. DOS opraví jen aditivní část atmosféry.",
            "## 5. Dark object subtraction (DOS)\n\nWe assume that the darkest pixels in the scene have almost zero surface reflectance (1 % is the usual choice, Chavez 1996). Whatever they have on top is path radiance, which we subtract from the whole scene. DOS corrects only the additive part of the atmosphere.")),
        ("code", t('''
pct = 0.1          # ◀ parametr: percentil, který považujeme za tmavý objekt (%)
rho_dark = 0.01    # ◀ parametr: předpokládaná skutečná odrazivost tmavého objektu
dos = {b: summer["toa"][b] - (np.percentile(summer["toa"][b][summer["ok"]], pct) - rho_dark) for b in BANDS}

def rmse(a, b, m=valid): return float(np.sqrt(np.mean((a[m] - b[m]) ** 2)))
def bias(a, b, m=valid): return float(np.mean(a[m] - b[m]))
res = pd.DataFrame({
    "tmavý objekt ρ TOA": [np.percentile(summer["toa"][b][summer["ok"]], pct) for b in BANDS],
    "RMSE TOA": [rmse(summer["toa"][b], boa[b]) for b in BANDS],
    "RMSE DOS": [rmse(dos[b], boa[b]) for b in BANDS],
    "bias DOS": [bias(dos[b], boa[b]) for b in BANDS],
}, index=[f"B{b}" for b in BANDS])
res.round(4)
''', '''
pct = 0.1          # ◀ parameter: percentile taken as the dark object (%)
rho_dark = 0.01    # ◀ parameter: assumed true reflectance of the dark object
dos = {b: summer["toa"][b] - (np.percentile(summer["toa"][b][summer["ok"]], pct) - rho_dark) for b in BANDS}

def rmse(a, b, m=valid): return float(np.sqrt(np.mean((a[m] - b[m]) ** 2)))
def bias(a, b, m=valid): return float(np.mean(a[m] - b[m]))
res = pd.DataFrame({
    "dark object ρ TOA": [np.percentile(summer["toa"][b][summer["ok"]], pct) for b in BANDS],
    "RMSE TOA": [rmse(summer["toa"][b], boa[b]) for b in BANDS],
    "RMSE DOS": [rmse(dos[b], boa[b]) for b in BANDS],
    "bias DOS": [bias(dos[b], boa[b]) for b in BANDS],
}, index=[f"B{b}" for b in BANDS])
res.round(4)
''')),
        ("task", t(
            "Ve kterých pásmech DOS chybu proti BOA zmenší a ve kterých ji naopak zvětší? Proč je bias DOS ve všech pásmech záporný (co DOS dělá s násobnou složkou, propustností atmosféry)? Nastav `pct = 2` a pak `rho_dark = 0`: co se stane? Kdy DOS selže úplně (zimní scéna se sněhem bez tmavých objektů, opar jen nad částí scény)?",
            "In which bands does DOS reduce the error against BOA and in which does it make it larger? Why is the DOS bias negative in all bands (what does DOS do with the multiplicative part, the atmospheric transmittance)? Set `pct = 2` and then `rho_dark = 0`: what happens? When does DOS fail completely (a winter scene with snow and no dark objects, haze over only part of the scene)?")),
        ("md", t(
            "## 6. Empirická přímka\n\nV terénu se na snímek položí tmavý a světlý panel se změřenou odrazivostí. Tady jako panely poslouží tmavé a světlé pixely, jejichž odrazivost na povrchu známe ze Sentinelu-2. Pro každé pásmo proložíme přímku ρ_BOA = a · ρ_TOA + b: posun b souvisí se září dráhy a sklon s propustností atmosféry: pro ρ_TOA ≈ ρ_dráhy + T · ρ_BOA vychází a ≈ 1/T a b ≈ −ρ_dráhy/T.",
            "## 6. Empirical line\n\nIn the field a dark and a bright panel with measured reflectance are placed in the image. Here the panels are dark and bright pixels whose surface reflectance we know from Sentinel-2. For each band we fit a line ρ_BOA = a · ρ_TOA + b: the offset b relates to path radiance and the slope a to atmospheric transmittance: for ρ_TOA ≈ ρ_path + T · ρ_BOA we get a ≈ 1/T and b ≈ −ρ_path/T.")),
        ("code", t('''
n_panel = 300        # ◀ parametr: kolik nejtmavších a nejsvětlejších pixelů použít jako panely
rng = np.random.default_rng(0)
el, rows = {}, []
for b in BANDS:
    v = np.flatnonzero(valid.ravel())
    order = v[np.argsort(boa[b].ravel()[v])]
    panels = np.r_[order[:n_panel], order[-n_panel:]]               # tmavé a světlé „panely“
    a, c = np.polyfit(summer["toa"][b].ravel()[panels], boa[b].ravel()[panels], 1)
    el[b] = a * summer["toa"][b] + c
    rows.append({"pásmo": f"B{b}", "sklon a": a, "posun b": c, "RMSE TOA": rmse(summer["toa"][b], boa[b]),
                 "RMSE DOS": rmse(dos[b], boa[b]), "RMSE emp. přímka": rmse(el[b], boa[b])})
print(pd.DataFrame(rows).set_index("pásmo").round(4))
fig, ax = plt.subplots(1, 3, figsize=(13, 4))
sel = rng.choice(np.flatnonzero(valid.ravel()), 4000, replace=False)
for a_, (name, est) in zip(ax, [("TOA", summer["toa"]), ("DOS", dos), ("empirická přímka", el)]):
    for b, col in [(2, "tab:blue"), (4, "tab:red"), (5, "tab:purple")]:
        a_.scatter(boa[b].ravel()[sel], est[b].ravel()[sel], s=2, alpha=0.4, c=col, label=f"B{b}")
    a_.axline((0, 0), slope=1, color="k", lw=0.8); a_.set(xlim=(0, 0.5), ylim=(0, 0.5), xlabel="ρ BOA Sentinel-2", ylabel=name, title=name)
ax[0].legend(); plt.tight_layout(); plt.show()
''', '''
n_panel = 300        # ◀ parameter: how many darkest and brightest pixels to use as panels
rng = np.random.default_rng(0)
el, rows = {}, []
for b in BANDS:
    v = np.flatnonzero(valid.ravel())
    order = v[np.argsort(boa[b].ravel()[v])]
    panels = np.r_[order[:n_panel], order[-n_panel:]]               # dark and bright "panels"
    a, c = np.polyfit(summer["toa"][b].ravel()[panels], boa[b].ravel()[panels], 1)
    el[b] = a * summer["toa"][b] + c
    rows.append({"band": f"B{b}", "slope a": a, "offset b": c, "RMSE TOA": rmse(summer["toa"][b], boa[b]),
                 "RMSE DOS": rmse(dos[b], boa[b]), "RMSE emp. line": rmse(el[b], boa[b])})
print(pd.DataFrame(rows).set_index("band").round(4))
fig, ax = plt.subplots(1, 3, figsize=(13, 4))
sel = rng.choice(np.flatnonzero(valid.ravel()), 4000, replace=False)
for a_, (name, est) in zip(ax, [("TOA", summer["toa"]), ("DOS", dos), ("empirical line", el)]):
    for b, col in [(2, "tab:blue"), (4, "tab:red"), (5, "tab:purple")]:
        a_.scatter(boa[b].ravel()[sel], est[b].ravel()[sel], s=2, alpha=0.4, c=col, label=f"B{b}")
    a_.axline((0, 0), slope=1, color="k", lw=0.8); a_.set(xlim=(0, 0.5), ylim=(0, 0.5), xlabel="ρ BOA Sentinel-2", ylabel=name, title=name)
ax[0].legend(); plt.tight_layout(); plt.show()
''')),
        ("task", t(
            "Proč má empirická přímka v modrých pásmech záporný posun a sklon jiný než 1? Co fyzikálně vyjadřují? Která metoda dopadla nejlépe a proč DOS nemůže opravit sklon? Nastav `n_panel = 20`: co se stane se spolehlivostí přímky? Proč v terénu stačí dva panely, ale musí ležet ve stejném snímku a za stejného osvětlení?",
            "Why does the empirical line have a negative offset and a slope different from 1 in the blue bands? What do they express physically? Which method did best and why can DOS not correct the slope? Set `n_panel = 20`: what happens to the reliability of the line? Why are two panels enough in the field, but must be in the same image and under the same illumination?")),
        ("task", t(
        "+ Porovnej výsledky se spolužákem, který spustil notebook pro jiné místo: vyšel podobný rozdíl TOA − BOA nad vodou a podobný sklon empirické přímky? Čím se mohou lišit (jiný den, jiný opar, jiná výška Slunce)?",
        "+ Compare your results with a classmate who ran the notebook for another place: did you get a similar TOA − BOA difference over water and a similar empirical line slope? What could make them differ (another day, other haze, another sun elevation)?")),
    ]
    tokens = {"@PATH@": P["l8s"][10:13], "@ROW@": P["l8s"][13:16], "@L8S@": P["l8s"], "@L8W@": P["l8w"], "@X0@": str(P["x0"]), "@Y0@": str(P["y0"]),
              "@S2@": P["s2"], "@S2D_CS@": P["s2d_cs"], "@S2D_EN@": P["s2d_en"], "@L8D_CS@": P["l8d_cs"], "@L8D_EN@": P["l8d_en"],
              "@S2REL_CS@": P["s2rel_cs"], "@S2REL_EN@": P["s2rel_en"], "@S2REL2_CS@": P["s2rel2_cs"], "@S2REL2_EN@": P["s2rel2_en"],
              "@WATER_CS@": P["water_cs"], "@WATER_EN@": P["water_en"]}
    res = []
    for kind, text in out:
        for k, v in tokens.items():
            text = text.replace(k, v)
        assert not re.search(r"@[A-Z0-9_]+@", text), text[:80]
        res.append((kind, text))
    return res
