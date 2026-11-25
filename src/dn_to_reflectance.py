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
            "cs": "Laboratoř prochází řetězec od digitálního čísla přes zář k odrazivosti nad atmosférou (TOA) a na povrchu (BOA) a ukazuje, co opraví metoda tmavého objektu (DOS) a empirická přímka. Tady celý řetězec spočítáš na dvou skutečných snímcích Landsatu 8 " + P["over_cs"] + " a výsledek porovnáš s odrazivostí Sentinelu-2 L2A z téhož týdne.",
            "en": "The lab walks through the chain from digital number to radiance to top-of-atmosphere (TOA) and surface (BOA) reflectance and shows what dark object subtraction (DOS) and the empirical line correct. Here you compute the whole chain on two real Landsat 8 images of " + P["over_en"] + " and compare the result with Sentinel-2 L2A reflectance from the same week.",
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
    return {k.strip(): v.strip().strip('"') for k, v in (line.split(" = ") for line in txt.splitlines() if " = " in line)}

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
    return {k.strip(): v.strip().strip('"') for k, v in (line.split(" = ") for line in txt.splitlines() if " = " in line)}

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
def rgb(d):
    return np.clip(np.dstack([d[4], d[3], d[2]]) / 0.25, 0, 1)
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
def rgb(d):
    return np.clip(np.dstack([d[4], d[3], d[2]]) / 0.25, 0, 1)
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
        ("md", t(r"""## 6. Empirická přímka

Empirická přímka opravuje odrazivost pomocí sklonu a posunu. V terénu mohou
jako reference sloužit fyzické kalibrační panely se známou odrazivostí.
V tomto cvičení použijeme **referenční pixely**: jejich referenční odrazivost
převezmeme ze snímku Sentinel-2 L2A.

Pro každé pásmo hledáme přímku mezi odrazivostí TOA Landsatu a referenční
odrazivostí BOA. Touto přímkou potom opravíme celé pásmo:

$$
\widehat{\rho}_{\mathrm{BOA}} = a\,\rho_{\mathrm{TOA}} + b.
$$

- $\rho_{\mathrm{TOA}}$ je vstupní odrazivost na horní hranici atmosféry.
- $\widehat{\rho}_{\mathrm{BOA}}$ je náš odhad odrazivosti na povrchu.
- $a$ je **sklon** (`slope`): mění měřítko hodnot.
- $b$ je **posun** (`offset`): ke každé hodnotě přičítá stejnou opravu.

Odrazivost, sklon i posun jsou bezrozměrné. Pro zjednodušený model atmosféry

$$
\rho_{\mathrm{TOA}} \approx \rho_{\mathrm{dráhy}} + T\,\rho_{\mathrm{BOA}}
\quad\Rightarrow\quad
a \approx \frac{1}{T},\qquad b \approx -\frac{\rho_{\mathrm{dráhy}}}{T},
$$

kde $T$ je propustnost atmosféry a $\rho_{\mathrm{dráhy}}$ příspěvek rozptylu
v atmosféře vyjádřený jako odrazivost. Tento fyzikální výklad je přibližný:
zde srovnáváme dva různé senzory a referenční BOA je sama výsledkem zpracování.""", r"""## 6. Empirical line

The empirical line corrects reflectance with a slope and an offset. In the field the
reference can be physical calibration panels with known reflectance.
In this exercise we use **reference pixels**: their reference reflectance
is taken from a Sentinel-2 L2A image.

For each band we look for a line between the Landsat TOA reflectance and the reference
BOA reflectance. We then correct the whole band with this line:

$$
\widehat{\rho}_{\mathrm{BOA}} = a\,\rho_{\mathrm{TOA}} + b.
$$

- $\rho_{\mathrm{TOA}}$ is the input top-of-atmosphere reflectance.
- $\widehat{\rho}_{\mathrm{BOA}}$ is our estimate of the surface reflectance.
- $a$ is the **slope** (`slope`): it scales the values.
- $b$ is the **offset** (`offset`): it adds the same correction to every value.

Reflectance, slope and offset are dimensionless. For a simplified model of the atmosphere

$$
\rho_{\mathrm{TOA}} \approx \rho_{\mathrm{path}} + T\,\rho_{\mathrm{BOA}}
\quad\Rightarrow\quad
a \approx \frac{1}{T},\qquad b \approx -\frac{\rho_{\mathrm{path}}}{T},
$$

where $T$ is the atmospheric transmittance and $\rho_{\mathrm{path}}$ the contribution of
atmospheric scattering expressed as reflectance. This physical reading is approximate:
here we compare two different sensors, and the reference BOA is itself a product of processing.""")),
        ("md", t(r"""### 6.1 Vyber referenční pixely a oprav snímek

V každém pásmu vybereme podle Sentinelu-2 `n_reference` nejtmavších a stejný
počet nejsvětlejších platných pixelů. Při `n_reference = 300` tedy přímku
prokládáme **600 dvojicemi hodnot**, ne dvěma průměry skupin. Různá pásma
mohou vybrat různé pixely.

Zápis `[valid]` vybere hodnoty na společných platných místech obou snímků
ve stejném pořadí. `np.argsort` vrátí jejich indexy od nejtmavších po
nejsvětlejší. `np.polyfit(..., deg=1)` z vybraných dvojic vypočítá sklon
a posun přímky. Tu pak použijeme na celé pásmo Landsatu.

**Po změně `n_reference` spusť znovu všechny tři buňky této části (6.1–6.3).**""", r"""### 6.1 Select reference pixels and correct the image

In each band we select, according to Sentinel-2, the `n_reference` darkest and the same
number of brightest valid pixels. With `n_reference = 300` the line is therefore fitted
to **600 pairs of values**, not to two group means. Different bands
may select different pixels.

Indexing with `[valid]` picks the values at the valid locations shared by both images,
in the same order. `np.argsort` returns their indices from darkest to
brightest. `np.polyfit(..., deg=1)` computes the slope and offset of the line
from the selected pairs. We then apply the line to the whole Landsat band.

**After changing `n_reference`, run all three cells of this part again (6.1–6.3).**""")),
        ("code", t("""
# Počet tmavých i světlých referenčních pixelů; celkem 2× tolik.
n_reference = 300  # ◀ parametr: pixelů v každé skupině
empirical = {}
coefficients = {}

for band in BANDS:
    toa_image = summer["toa"][band]
    toa_valid = toa_image[valid]
    boa_valid = boa[band][valid]

    sorted_indices = np.argsort(boa_valid)
    dark_indices = sorted_indices[:n_reference]
    bright_indices = sorted_indices[-n_reference:]
    reference_indices = np.concatenate((dark_indices, bright_indices))

    toa_reference = toa_valid[reference_indices]
    boa_reference = boa_valid[reference_indices]
    slope, offset = np.polyfit(toa_reference, boa_reference, deg=1)

    empirical[band] = slope * toa_image + offset
    coefficients[band] = (slope, offset)
""", """
# Number of dark and of bright reference pixels; twice as many in total.
n_reference = 300  # ◀ parameter: pixels in each group
empirical = {}
coefficients = {}

for band in BANDS:
    toa_image = summer["toa"][band]
    toa_valid = toa_image[valid]
    boa_valid = boa[band][valid]

    sorted_indices = np.argsort(boa_valid)
    dark_indices = sorted_indices[:n_reference]
    bright_indices = sorted_indices[-n_reference:]
    reference_indices = np.concatenate((dark_indices, bright_indices))

    toa_reference = toa_valid[reference_indices]
    boa_reference = boa_valid[reference_indices]
    slope, offset = np.polyfit(toa_reference, boa_reference, deg=1)

    empirical[band] = slope * toa_image + offset
    coefficients[band] = (slope, offset)
""")),
        ("md", t(r"""### 6.2 Porovnej chyby všech tří postupů

Tabulka ukáže sklon a posun v každém pásmu a RMSE původní odrazivosti TOA,
korekce DOS a empirické přímky proti referenci Sentinel-2 BOA:

$$
\mathrm{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^{N}
\left(\rho_i^{\mathrm{odhad}}-\rho_i^{\mathrm{reference}}\right)^2}.
$$

$N$ je počet všech platných pixelů a $i$ označuje jeden z nich. Menší RMSE
znamená lepší shodu s referencí. Všechny metody hodnotíme na stejných pixelech,
včetně těch použitých k proložení přímky; nejde tedy o nezávislé ověření přesnosti.""", r"""### 6.2 Compare the errors of all three approaches

The table shows the slope and offset in each band and the RMSE of the original TOA reflectance,
of the DOS correction and of the empirical line against the Sentinel-2 BOA reference:

$$
\mathrm{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^{N}
\left(\rho_i^{\mathrm{estimate}}-\rho_i^{\mathrm{reference}}\right)^2}.
$$

$N$ is the number of all valid pixels and $i$ denotes one of them. A smaller RMSE
means better agreement with the reference. All methods are evaluated on the same pixels,
including those used to fit the line, so this is not an independent accuracy assessment.""")),
        ("code", t("""
rows = []
for band in BANDS:
    slope, offset = coefficients[band]
    rows.append(
        {
            "pásmo": f"B{band}",
            "sklon a": slope,
            "posun b": offset,
            "RMSE TOA": rmse(summer["toa"][band], boa[band]),
            "RMSE DOS": rmse(dos[band], boa[band]),
            "RMSE emp. přímka": rmse(empirical[band], boa[band]),
        }
    )

comparison = pd.DataFrame(rows).set_index("pásmo")
print(comparison.round(4))
""", """
rows = []
for band in BANDS:
    slope, offset = coefficients[band]
    rows.append(
        {
            "band": f"B{band}",
            "slope a": slope,
            "offset b": offset,
            "RMSE TOA": rmse(summer["toa"][band], boa[band]),
            "RMSE DOS": rmse(dos[band], boa[band]),
            "RMSE emp. line": rmse(empirical[band], boa[band]),
        }
    )

comparison = pd.DataFrame(rows).set_index("band")
print(comparison.round(4))
""")),
        ("md", t(r"""### 6.3 Zobraz shodu se Sentinelem-2

Na vodorovné ose je referenční BOA, na svislé ose odrazivost daného postupu.
Černá přímka 1 : 1 označuje úplnou shodu. Barvy rozlišují modré pásmo B2,
červené B4 a blízké infračervené B5.

Pro přehlednost vykreslíme jen **4 000 náhodně vybraných platných pixelů**,
stejných pro všechny grafy i pásma. Pevné semínko `0` zajistí opakovatelný
výběr. Tento vzorek slouží pouze ke kreslení; kalibraci ani RMSE nemění.""", r"""### 6.3 Show the agreement with Sentinel-2

The horizontal axis shows the reference BOA, the vertical axis the reflectance from the given approach.
The black 1 : 1 line marks perfect agreement. Colours distinguish the blue band B2,
the red B4 and the near-infrared B5.

For clarity we plot only **4,000 randomly selected valid pixels**,
the same for all plots and bands. The fixed seed `0` makes the selection
repeatable. This sample is used only for plotting; it changes neither the calibration nor the RMSE.""")),
        ("code", t("""
rng = np.random.default_rng(0)
n_valid = np.count_nonzero(valid)
plot_indices = rng.choice(n_valid, size=4000, replace=False)

methods = [("TOA", summer["toa"]), ("DOS", dos), ("empirická přímka", empirical)]
band_colors = {2: "tab:blue", 4: "tab:red", 5: "tab:purple"}
fig, axes = plt.subplots(1, 3, figsize=(13, 4))

for axis, (name, estimates) in zip(axes, methods):
    for band, color in band_colors.items():
        reference_values = boa[band][valid]
        estimated_values = estimates[band][valid]
        axis.scatter(
            reference_values[plot_indices],
            estimated_values[plot_indices],
            s=2,
            alpha=0.4,
            c=color,
            label=f"B{band}",
        )
    axis.axline((0, 0), slope=1, color="k", lw=0.8)
    axis.set(xlim=(0, 0.5), ylim=(0, 0.5), xlabel="ρ BOA Sentinel-2", ylabel=name, title=name)

axes[0].legend()
plt.tight_layout()
plt.show()
""", """
rng = np.random.default_rng(0)
n_valid = np.count_nonzero(valid)
plot_indices = rng.choice(n_valid, size=4000, replace=False)

methods = [("TOA", summer["toa"]), ("DOS", dos), ("empirical line", empirical)]
band_colors = {2: "tab:blue", 4: "tab:red", 5: "tab:purple"}
fig, axes = plt.subplots(1, 3, figsize=(13, 4))

for axis, (name, estimates) in zip(axes, methods):
    for band, color in band_colors.items():
        reference_values = boa[band][valid]
        estimated_values = estimates[band][valid]
        axis.scatter(
            reference_values[plot_indices],
            estimated_values[plot_indices],
            s=2,
            alpha=0.4,
            c=color,
            label=f"B{band}",
        )
    axis.axline((0, 0), slope=1, color="k", lw=0.8)
    axis.set(xlim=(0, 0.5), ylim=(0, 0.5), xlabel="ρ BOA Sentinel-2", ylabel=name, title=name)

axes[0].legend()
plt.tight_layout()
plt.show()
""")),
        ("task", t(
            "Proč má empirická přímka v modrých pásmech záporný posun a sklon jiný než 1? Co fyzikálně vyjadřují? Která metoda má nejmenší RMSE v jednotlivých pásmech a proč DOS nemůže opravit sklon? Nastav `n_reference = 20` a znovu spusť buňky 6.1–6.3: jak se změní sklon, posun a RMSE? Proč v terénu stačí k určení přímky dva kalibrační panely s různou známou odrazivostí, ale musí ležet ve stejném snímku a za stejného osvětlení?",
            "Why does the empirical line have a negative offset and a slope different from 1 in the blue bands? What do they express physically? Which method has the smallest RMSE in each band, and why can DOS not correct the slope? Set `n_reference = 20` and run cells 6.1–6.3 again: how do the slope, offset and RMSE change? Why are two calibration panels with different known reflectance enough to determine the line in the field, but must they be in the same image and under the same illumination?")),
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
