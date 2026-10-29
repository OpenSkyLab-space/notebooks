from _common import S2_HELPERS

META = {
    "version": "1.0",
    "minutes": 45,
    "title": {"cs": "Spektrální signatury ze Sentinelu-2: les, pole, voda a sníh", "en": "Spectral signatures from Sentinel-2: forest, fields, water and snow"},
    "visual": {"cs": "Spektrální signatury", "en": "Spectral signatures"},
    "lead": {
        "cs": "Vizuál ukazuje, jak chlorofyl, voda v listech, sušina a LAI mění spektrální křivku vegetace a proč NDVI v hustém porostu přestává růst. Tady to ověříš na skutečných pixelech Sentinelu-2 od Roztok a na časové řadě jednoho pole během sezóny 2024.",
        "en": "The visual shows how chlorophyll, leaf water, dry matter and LAI shape the spectral curve of vegetation and why NDVI stops growing in dense canopies. Here you check it on real Sentinel-2 pixels near Roztoky and on a time series of one field over the 2024 season.",
    },
    "goal": {
        "cs": "porovnat skutečné spektrální křivky povrchů, najít polohu červené hrany, ukázat nasycení NDVI na časové řadě pole a vysvětlit, proč stejný index z jiných pásem dává jiné číslo.",
        "en": "compare real spectral curves of surfaces, locate the red edge, show NDVI saturation on a field time series, and explain why the same index from different bands gives a different number.",
    },
    "data": {
        "cs": "Sentinel-2 L2A z katalogu Earth Search na AWS: scéna `S2B_33UVR_20240721_0_L2A` (21. 7. 2024, okolí Roztok), bezoblačné scény dlaždice 33UVR z března až října 2024 pro časovou řadu a `S2A_33UWS_20240308_0_L2A` (Krkonoše se sněhem); třídy ESA WorldCover 2021. Stahuje se asi 30 MB, časová řada trvá 1 až 3 minuty.",
        "en": "Sentinel-2 L2A from the Earth Search catalogue on AWS: scene `S2B_33UVR_20240721_0_L2A` (21 July 2024, near Roztoky), cloud-free scenes of tile 33UVR from March to October 2024 for the time series, and `S2A_33UWS_20240308_0_L2A` (snow in the Krkonoše mountains); ESA WorldCover 2021 classes. About 30 MB is downloaded; the time series takes 1 to 3 minutes.",
    },
    "sources": {
        "cs": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); COG kopie v registru AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje podle [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).",
            "Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Poloha červené hrany lineární interpolací: Guyot, G., Baret, F. (1988). Utilisation de la haute résolution spectrale pour suivre l'état des couverts végétaux. *Proc. 4th Int. Colloquium on Spectral Signatures of Objects in Remote Sensing*, ESA SP-287, 279–286.",
            "Nasycení NDVI a indexy s červenou hranou: Gitelson, A. A., Merzlyak, M. N. (1994). Spectral reflectance changes associated with autumn senescence of *Aesculus hippocastanum* L. and *Acer platanoides* L. leaves. *Journal of Plant Physiology* 143, 286–292. https://doi.org/10.1016/S0176-1617(11)81633-0",
            "NDWI: McFeeters, S. K. (1996). The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. *International Journal of Remote Sensing* 17, 1425–1432. https://doi.org/10.1080/01431169608948714",
            "NDSI pro sníh: Hall, D. K., Riggs, G. A., Salomonson, V. V. (1995). Development of methods for mapping global snow cover using MODIS. *Remote Sensing of Environment* 54, 127–140. https://doi.org/10.1016/0034-4257(95)00137-P",
        ],
        "en": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); COG copy in the AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution under the [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).",
            "Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Red edge position by linear interpolation: Guyot, G., Baret, F. (1988). Utilisation de la haute résolution spectrale pour suivre l'état des couverts végétaux. *Proc. 4th Int. Colloquium on Spectral Signatures of Objects in Remote Sensing*, ESA SP-287, 279–286.",
            "NDVI saturation and red-edge indices: Gitelson, A. A., Merzlyak, M. N. (1994). Spectral reflectance changes associated with autumn senescence of *Aesculus hippocastanum* L. and *Acer platanoides* L. leaves. *Journal of Plant Physiology* 143, 286–292. https://doi.org/10.1016/S0176-1617(11)81633-0",
            "NDWI: McFeeters, S. K. (1996). The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. *International Journal of Remote Sensing* 17, 1425–1432. https://doi.org/10.1080/01431169608948714",
            "NDSI for snow: Hall, D. K., Riggs, G. A., Salomonson, V. V. (1995). Development of methods for mapping global snow cover using MODIS. *Remote Sensing of Environment* 54, 127–140. https://doi.org/10.1016/0034-4257(95)00137-P",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava", "## 1. Setup")),
        ("code", "%pip install -q rasterio"),
        ("code", '''
import requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling
from rasterio.windows import Window
from pyproj import Transformer
''' + t(S2_HELPERS["cs"], S2_HELPERS["en"])),
        ("md", t("## 2. Spektrální křivky skutečných povrchů", "## 2. Spectral curves of real surfaces")),
        ("code", t('''
refl, scl, wl, grid, item = s2_window("S2B_33UVR_20240721_0_L2A", 14.375, 50.145, 2000)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
clear = np.isin(scl, [4, 5, 6])
classes = {10: "les", 30: "louka", 40: "pole", 50: "zástavba", 80: "voda"}
lam = np.array([wl[b] for b in BANDS])
fig, ax = plt.subplots(figsize=(10, 4))
curves = {}
for code, name in classes.items():
    m = clear & (wc == code)
    stack = np.array([refl[b][m] for b in BANDS])
    q25, q50, q75 = np.percentile(stack, [25, 50, 75], axis=1)
    curves[name] = q50
    ax.plot(lam, q50, "o-", label=name); ax.fill_between(lam, q25, q75, alpha=0.15)
ax.set(xlabel="vlnová délka (µm)", ylabel="odrazivost", title="Medián a mezikvartilové rozpětí, Sentinel-2 L2A, 21. 7. 2024")
ax.legend(); plt.show()
''', '''
refl, scl, wl, grid, item = s2_window("S2B_33UVR_20240721_0_L2A", 14.375, 50.145, 2000)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
clear = np.isin(scl, [4, 5, 6])
classes = {10: "forest", 30: "meadow", 40: "field", 50: "built-up", 80: "water"}
lam = np.array([wl[b] for b in BANDS])
fig, ax = plt.subplots(figsize=(10, 4))
curves = {}
for code, name in classes.items():
    m = clear & (wc == code)
    stack = np.array([refl[b][m] for b in BANDS])
    q25, q50, q75 = np.percentile(stack, [25, 50, 75], axis=1)
    curves[name] = q50
    ax.plot(lam, q50, "o-", label=name); ax.fill_between(lam, q25, q75, alpha=0.15)
ax.set(xlabel="wavelength (µm)", ylabel="reflectance", title="Median and interquartile range, Sentinel-2 L2A, 21 July 2024")
ax.legend(); plt.show()
''')),
        ("task", t(
            "Popiš křivku lesa: proč je v modré a červené nízko, v zelené malé maximum a mezi 0,70 a 0,78 µm prudký nárůst? Proč má pole (koncem července často zralé obilí nebo strniště) v červené víc a v NIR méně než les? Proč je rozptyl u zástavby a pole tak velký?",
            "Describe the forest curve: why is it low in blue and red, with a small peak in green and a steep rise between 0.70 and 0.78 µm? Why does the field (in late July often ripe grain or stubble) have more red and less NIR than the forest? Why is the spread so large for built-up areas and fields?")),
        ("md", t(
            "## 3. Poloha červené hrany\n\nČervená hrana je strmý nárůst odrazivosti mezi červenou a NIR. Její polohu (REP) odhadneme lineární interpolací z pásem B4, B5, B6 a B7 (Guyot a Baret 1988). Víc chlorofylu posouvá hranu k delším vlnovým délkám.",
            "## 3. Red edge position\n\nThe red edge is the steep rise in reflectance between red and NIR. We estimate its position (REP) by linear interpolation from bands B4, B5, B6 and B7 (Guyot and Baret 1988). More chlorophyll shifts the edge to longer wavelengths.")),
        ("code", t('''
def rep(r4, r5, r6, r7):
    mid = (r4 + r7) / 2                                   # odrazivost v polovině hrany
    return 705 + 35 * (mid - r5) / (r6 - r5)             # nm (B5 = 705 nm, B6 = 740 nm)

REP = rep(refl["red"], refl["rededge1"], refl["rededge2"], refl["rededge3"])
for code, name in classes.items():
    m = clear & (wc == code)
    print(f"{name:9s}: REP medián {np.nanmedian(REP[m]):.1f} nm")
''', '''
def rep(r4, r5, r6, r7):
    mid = (r4 + r7) / 2                                   # reflectance halfway up the edge
    return 705 + 35 * (mid - r5) / (r6 - r5)             # nm (B5 = 705 nm, B6 = 740 nm)

REP = rep(refl["red"], refl["rededge1"], refl["rededge2"], refl["rededge3"])
for code, name in classes.items():
    m = clear & (wc == code)
    print(f"{name:9s}: REP median {np.nanmedian(REP[m]):.1f} nm")
''')),
        ("task", t(
            "Který povrch má červenou hranu nejdál a proč? Má smysl počítat REP u vody nebo zástavby? Podívej se, jaké hodnoty vyjdou, a vysvětli, proč index bez vegetace nedává fyzikální smysl, i když vrátí číslo.",
            "Which surface has the red edge furthest and why? Does it make sense to compute REP for water or built-up areas? Look at the values and explain why the index has no physical meaning without vegetation even though it returns a number.")),
        ("md", t(
            "## 4. Nasycení NDVI během sezóny\n\nVezmeme jeden pixel pole u Únětic a všechny bezoblačné snímky z roku 2024. Porovnáme NDVI = (NIR − R)/(NIR + R), NDRE = (NIR − RE1)/(NIR + RE1) a NDMI = (NIR − SWIR1)/(NIR + SWIR1).",
            "## 4. NDVI saturation during the season\n\nWe take one field pixel near Únětice and all cloud-free images from 2024. We compare NDVI = (NIR − R)/(NIR + R), NDRE = (NIR − RE1)/(NIR + RE1) and NDMI = (NIR − SWIR1)/(NIR + SWIR1).")),
        ("code", t('''
lon, lat = 14.3516, 50.1632          # ◀ parametr: bod (pole u Únětic); zkus i les, např. 14.366, 50.148
search = requests.post("https://earth-search.aws.element84.com/v1/search", json={
    "collections": ["sentinel-2-l2a"], "intersects": {"type": "Point", "coordinates": [lon, lat]},
    "datetime": "2024-03-01T00:00:00Z/2024-10-31T23:59:59Z", "limit": 100,
    "query": {"eo:cloud_cover": {"lt": 40}, "grid:code": {"eq": "MGRS-33UVR"}}}, timeout=60).json()
print("scén v katalogu:", len(search["features"]))

def pixel(item, key, x, y):
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2):
        with rasterio.open("/vsicurl/" + item["assets"][key]["href"]) as r:
            row, col = r.index(x, y)
            return float(r.read(1, window=Window(col - 1, row - 1, 3, 3)).mean() if key != "scl"
                         else r.read(1, window=Window(col, row, 1, 1))[0, 0])

rows = []
for it in sorted(search["features"], key=lambda f: f["properties"]["datetime"]):
    x, y = Transformer.from_crs(4326, 32633, always_xy=True).transform(lon, lat)
    if pixel(it, "scl", x, y) not in (4, 5):               # jen jasná vegetace nebo holá půda
        continue
    p = it["properties"]
    off = -1000 if float(p.get("s2:processing_baseline", "0")) >= 4 and not p.get("earthsearch:boa_offset_applied", False) else 0
    r = {k: (pixel(it, k, x, y) + off) / 10000 for k in ("red", "rededge1", "nir08", "nir", "swir16")}
    r["date"] = it["properties"]["datetime"][:10]
    rows.append(r)
ts = pd.DataFrame(rows).drop_duplicates("date").set_index("date")
ts["NDVI"] = (ts.nir - ts.red) / (ts.nir + ts.red)
ts["NDRE"] = (ts.nir - ts.rededge1) / (ts.nir + ts.rededge1)
ts["NDMI"] = (ts.nir08 - ts.swir16) / (ts.nir08 + ts.swir16)
ax = ts[["NDVI", "NDRE", "NDMI"]].plot(marker="o", figsize=(10, 3.8), rot=45)
ax.set(ylabel="index", title=f"Bod {lon}, {lat}: {len(ts)} jasných scén v roce 2024"); plt.show()
''', '''
lon, lat = 14.3516, 50.1632          # ◀ parameter: point (field near Únětice); also try forest, e.g. 14.366, 50.148
search = requests.post("https://earth-search.aws.element84.com/v1/search", json={
    "collections": ["sentinel-2-l2a"], "intersects": {"type": "Point", "coordinates": [lon, lat]},
    "datetime": "2024-03-01T00:00:00Z/2024-10-31T23:59:59Z", "limit": 100,
    "query": {"eo:cloud_cover": {"lt": 40}, "grid:code": {"eq": "MGRS-33UVR"}}}, timeout=60).json()
print("scenes in the catalogue:", len(search["features"]))

def pixel(item, key, x, y):
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2):
        with rasterio.open("/vsicurl/" + item["assets"][key]["href"]) as r:
            row, col = r.index(x, y)
            return float(r.read(1, window=Window(col - 1, row - 1, 3, 3)).mean() if key != "scl"
                         else r.read(1, window=Window(col, row, 1, 1))[0, 0])

rows = []
for it in sorted(search["features"], key=lambda f: f["properties"]["datetime"]):
    x, y = Transformer.from_crs(4326, 32633, always_xy=True).transform(lon, lat)
    if pixel(it, "scl", x, y) not in (4, 5):               # only clear vegetation or bare soil
        continue
    p = it["properties"]
    off = -1000 if float(p.get("s2:processing_baseline", "0")) >= 4 and not p.get("earthsearch:boa_offset_applied", False) else 0
    r = {k: (pixel(it, k, x, y) + off) / 10000 for k in ("red", "rededge1", "nir08", "nir", "swir16")}
    r["date"] = it["properties"]["datetime"][:10]
    rows.append(r)
ts = pd.DataFrame(rows).drop_duplicates("date").set_index("date")
ts["NDVI"] = (ts.nir - ts.red) / (ts.nir + ts.red)
ts["NDRE"] = (ts.nir - ts.rededge1) / (ts.nir + ts.rededge1)
ts["NDMI"] = (ts.nir08 - ts.swir16) / (ts.nir08 + ts.swir16)
ax = ts[["NDVI", "NDRE", "NDMI"]].plot(marker="o", figsize=(10, 3.8), rot=45)
ax.set(ylabel="index", title=f"Point {lon}, {lat}: {len(ts)} clear scenes in 2024"); plt.show()
''')),
        ("code", t('''
fig, ax = plt.subplots(figsize=(5, 4))
ax.scatter(ts.NDRE, ts.NDVI)
for d, r in ts.iterrows(): ax.annotate(d[5:], (r.NDRE, r.NDVI), fontsize=7)
ax.set(xlabel="NDRE", ylabel="NDVI", title="Stejné datum, dva indexy"); plt.show()
''', '''
fig, ax = plt.subplots(figsize=(5, 4))
ax.scatter(ts.NDRE, ts.NDVI)
for d, r in ts.iterrows(): ax.annotate(d[5:], (r.NDRE, r.NDVI), fontsize=7)
ax.set(xlabel="NDRE", ylabel="NDVI", title="Same date, two indices"); plt.show()
''')),
        ("task", t(
            "Kdy pole dosáhlo maxima a kdy byla sklizeň? V jakém rozsahu NDVI se graf NDVI–NDRE ohýbá, tj. NDVI už skoro neroste, ale NDRE ano? Vysvětli nasycení: proč červená při vysokém LAI už nemůže klesnout níž, ale červená hrana se ještě posouvá?",
            "When did the field reach its peak and when was it harvested? In what NDVI range does the NDVI–NDRE plot bend, i.e. NDVI hardly grows but NDRE still does? Explain the saturation: why can red not drop any lower at high LAI while the red edge still moves?")),
        ("task", t(
            "Jak se během sezóny chová NDMI a proč klesá dřív nebo rychleji než NDVI, když porost dozrává? Změň bod na les (`14.366, 50.148`) a porovnej: proč je u lesa řada mnohem plošší?",
            "How does NDMI behave during the season and why does it drop earlier or faster than NDVI as the crop ripens? Change the point to forest (`14.366, 50.148`) and compare: why is the forest series much flatter?")),
        ("md", t(
            "## 5. Voda a sníh\n\nNDWI (zelená a NIR, McFeeters 1996) zvýrazní vodu, NDSI (zelená a SWIR 1,6 µm) sníh. Sníh je ve viditelném jasný, ale v SWIR pohlcuje; oblaka odrážejí v obou.",
            "## 5. Water and snow\n\nNDWI (green and NIR, McFeeters 1996) highlights water, NDSI (green and SWIR 1.6 µm) highlights snow. Snow is bright in the visible but absorbs in the SWIR; clouds reflect in both.")),
        ("code", t('''
snow, snow_scl, *_ = s2_window("S2A_33UWS_20240308_0_L2A", 15.70, 50.735, 3000)
ndsi = (snow["green"] - snow["swir16"]) / (snow["green"] + snow["swir16"])
ndwi = (refl["green"] - refl["nir"]) / (refl["green"] + refl["nir"])
thr = 0.4                               # ◀ parametr: práh NDSI pro sníh (MODIS používá 0,4)
fig, ax = plt.subplots(1, 3, figsize=(14, 4.5))
rgb = np.dstack([snow["red"], snow["green"], snow["blue"]]); ax[0].imshow(np.clip(rgb / 1.0, 0, 1)); ax[0].set_title("Krkonoše 8. 3. 2024, barevně")
ax[1].imshow(ndsi > thr, cmap="Blues"); ax[1].set_title(f"NDSI > {thr}: {np.mean(ndsi > thr):.0%} plochy")
im = ax[2].imshow(ndwi, cmap="BrBG", vmin=-0.8, vmax=0.8); ax[2].set_title("NDWI u Roztok (Vltava)"); fig.colorbar(im, ax=ax[2])
for a in ax: a.axis("off")
plt.show()
print(f"shoda s maskou sněhu SCL: {np.mean((ndsi > thr) == (snow_scl == 11)):.1%} pixelů")
''', '''
snow, snow_scl, *_ = s2_window("S2A_33UWS_20240308_0_L2A", 15.70, 50.735, 3000)
ndsi = (snow["green"] - snow["swir16"]) / (snow["green"] + snow["swir16"])
ndwi = (refl["green"] - refl["nir"]) / (refl["green"] + refl["nir"])
thr = 0.4                               # ◀ parameter: NDSI threshold for snow (MODIS uses 0.4)
fig, ax = plt.subplots(1, 3, figsize=(14, 4.5))
rgb = np.dstack([snow["red"], snow["green"], snow["blue"]]); ax[0].imshow(np.clip(rgb / 1.0, 0, 1)); ax[0].set_title("Krkonoše 8 March 2024, true colour")
ax[1].imshow(ndsi > thr, cmap="Blues"); ax[1].set_title(f"NDSI > {thr}: {np.mean(ndsi > thr):.0%} of the area")
im = ax[2].imshow(ndwi, cmap="BrBG", vmin=-0.8, vmax=0.8); ax[2].set_title("NDWI near Roztoky (Vltava)"); fig.colorbar(im, ax=ax[2])
for a in ax: a.axis("off")
plt.show()
print(f"agreement with the SCL snow mask: {np.mean((ndsi > thr) == (snow_scl == 11)):.1%} of pixels")
''')),
        ("task", t(
            "Proč NDSI odliší sníh od oblaků, i když jsou ve viditelném oba bílé? Změň práh na 0,2 a 0,6: kde se maska mění nejvíc (les se sněhem, stíny, kosodřevina)? Proč je Vltava v NDWI kladná a vegetace záporná?",
            "Why does NDSI separate snow from clouds although both are white in the visible? Change the threshold to 0.2 and 0.6: where does the mask change most (snowy forest, shadows, dwarf pine)? Why is the Vltava positive in NDWI and vegetation negative?")),
        ("md", t(
            "## 6. Stejný index, jiné číslo\n\nNDVI lze ze Sentinelu-2 spočítat s širokým pásmem B8 (střed kolem 833 nm, šířka přes 100 nm, pixel 10 m) nebo s úzkým B8A (865 nm, šířka asi 21 nm, pixel 20 m). Dron s multispektrální kamerou nebo Landsat mají zase jiná pásma. Porovnáme obě varianty na stejných pixelech.",
            "## 6. Same index, different number\n\nNDVI can be computed from Sentinel-2 with the broad band B8 (centred near 833 nm, over 100 nm wide, 10 m pixel) or the narrow B8A (865 nm, about 21 nm wide, 20 m pixel). A drone multispectral camera or Landsat have different bands again. We compare both variants on the same pixels.")),
        ("code", t('''
ndvi_b8 = (refl["nir"] - refl["red"]) / (refl["nir"] + refl["red"])
ndvi_b8a = (refl["nir08"] - refl["red"]) / (refl["nir08"] + refl["red"])
m = clear & np.isin(wc, [10, 30, 40])
d = (ndvi_b8a - ndvi_b8)[m]
print(f"NDVI(B8A) − NDVI(B8) ve vegetaci: průměr {d.mean():+.3f}, 5.–95. percentil {np.percentile(d, 5):+.3f} až {np.percentile(d, 95):+.3f}")
fig, ax = plt.subplots(figsize=(5, 4.5))
ax.hexbin(ndvi_b8[m], ndvi_b8a[m], gridsize=60, bins="log", cmap="viridis"); ax.axline((0, 0), slope=1, color="r", lw=1)
ax.set(xlabel="NDVI s B8 (10 m)", ylabel="NDVI s B8A (20 m)"); plt.show()
''', '''
ndvi_b8 = (refl["nir"] - refl["red"]) / (refl["nir"] + refl["red"])
ndvi_b8a = (refl["nir08"] - refl["red"]) / (refl["nir08"] + refl["red"])
m = clear & np.isin(wc, [10, 30, 40])
d = (ndvi_b8a - ndvi_b8)[m]
print(f"NDVI(B8A) − NDVI(B8) in vegetation: mean {d.mean():+.3f}, 5th–95th percentile {np.percentile(d, 5):+.3f} to {np.percentile(d, 95):+.3f}")
fig, ax = plt.subplots(figsize=(5, 4.5))
ax.hexbin(ndvi_b8[m], ndvi_b8a[m], gridsize=60, bins="log", cmap="viridis"); ax.axline((0, 0), slope=1, color="r", lw=1)
ax.set(xlabel="NDVI with B8 (10 m)", ylabel="NDVI with B8A (20 m)"); plt.show()
''')),
        ("task", t(
            "O kolik se obě NDVI liší a kterým směrem? Navrhni dvě příčiny (poloha a šířka pásma, rozlišení 10 vs. 20 m). Co z toho plyne, když chceš porovnat NDVI z dronu s NDVI ze Sentinelu-2 nebo staré a nové mapy NDVI?",
            "How much do the two NDVIs differ and in which direction? Suggest two causes (band position and width, 10 vs 20 m resolution). What follows when you want to compare drone NDVI with Sentinel-2 NDVI, or old and new NDVI maps?")),
    ]
