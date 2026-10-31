META = {
    "version": "1.0",
    "minutes": 70,
    "visual_stem": "dn_to_reflectance",
    "title": {"cs": "Od DN k odrazivosti, pokročilá verze: topografická korekce v Krkonoších",
              "en": "From DN to reflectance, advanced: topographic correction in the Krkonoše mountains"},
    "visual": {"cs": "Od DN k odrazivosti", "en": "From DN to reflectance"},
    "lead": {
        "cs": "Pokročilá verze notebooku k převodu DN na odrazivost. Vzorec pro odrazivost TOA dělí sinem výšky Slunce, tedy předpokládá rovinu. V horách ale každý svah dostává jiné osvětlení. Spočítáš ho z digitálního modelu terénu pro dvě scény Landsatu 8 s různou výškou Slunce, změříš, jak silně mění odrazivost lesa, a porovnáš pět topografických korekcí.",
        "en": "The advanced version of the DN-to-reflectance notebook. The TOA reflectance formula divides by the sine of the sun elevation, i.e. it assumes flat ground. In the mountains every slope gets different illumination. You compute it from a digital elevation model for two Landsat 8 scenes with different sun elevation, measure how strongly it changes forest reflectance, and compare five topographic corrections.",
    },
    "goal": {
        "cs": "spočítat sklon, orientaci a úhel dopadu slunečního záření z DEM, změřit vliv terénu na odrazivost v jednotlivých pásmech a ročních obdobích, porovnat kosinovou korekci, C-korekci, Minnaertovu korekci a SCS+C a posoudit, jak korekci poctivě ověřit.",
        "en": "compute slope, aspect and the solar incidence angle from a DEM, measure the terrain effect on reflectance by band and season, compare the cosine, C, Minnaert and SCS+C corrections, and judge how to validate a correction fairly.",
    },
    "data": {
        "cs": "Landsat 8 OLI Collection 1 Level-1 z veřejného archivu Google Cloud: `LC08_L1TP_191025_20190626_20190705_01_T1` (26. 6. 2019, výška Slunce 60°) a `LC08_L1TP_191025_20181013_20181030_01_T1` (13. 10. 2018, výška Slunce 31°), pásma B2–B7, BQA a MTL; Copernicus DEM GLO-30 z registru AWS Open Data; třídy ESA WorldCover 2021 v200. Výřez 12 × 12 km ve východních Krkonoších, asi 25 MB.",
        "en": "Landsat 8 OLI Collection 1 Level-1 from the Google Cloud public archive: `LC08_L1TP_191025_20190626_20190705_01_T1` (26 June 2019, sun elevation 60°) and `LC08_L1TP_191025_20181013_20181030_01_T1` (13 Oct 2018, sun elevation 31°), bands B2–B7, BQA and MTL; Copernicus DEM GLO-30 from the AWS Open Data registry; ESA WorldCover 2021 v200 classes. A 12 × 12 km window in the eastern Krkonoše mountains, about 25 MB.",
    },
    "sources": {
        "cs": [
            "Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; veřejný archiv Google Cloud (`gcp-public-data-landsat`). Data USGS jsou bez omezení užití, s uvedením zdroje.",
            "Copernicus DEM GLO-30: produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. Registr AWS Open Data (`copernicus-dem-30m`).",
            "Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Teillet, P. M., Guindon, B., Goodenough, D. G. (1982). On the slope-aspect correction of multispectral scanner data. *Canadian Journal of Remote Sensing* 8(2), 84–106.",
            "Minnaert, M. (1941). The reciprocity principle in lunar photometry. *Astrophysical Journal* 93, 403–410.",
            "Soenen, S. A., Peddle, D. R., Coburn, C. A. (2005). SCS+C: a modified sun-canopy-sensor topographic correction in forested terrain. *IEEE Transactions on Geoscience and Remote Sensing* 43, 2148–2159. https://doi.org/10.1109/TGRS.2005.852480",
        ],
        "en": [
            "Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; Google Cloud public archive (`gcp-public-data-landsat`). USGS data have no use restrictions, attribution requested.",
            "Copernicus DEM GLO-30: produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. AWS Open Data registry (`copernicus-dem-30m`).",
            "Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Teillet, P. M., Guindon, B., Goodenough, D. G. (1982). On the slope-aspect correction of multispectral scanner data. *Canadian Journal of Remote Sensing* 8(2), 84–106.",
            "Minnaert, M. (1941). The reciprocity principle in lunar photometry. *Astrophysical Journal* 93, 403–410.",
            "Soenen, S. A., Peddle, D. R., Coburn, C. A. (2005). SCS+C: a modified sun-canopy-sensor topographic correction in forested terrain. *IEEE Transactions on Geoscience and Remote Sensing* 43, 2148–2159. https://doi.org/10.1109/TGRS.2005.852480",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a data", "## 1. Setup and data")),
        ("code", "%pip install -q rasterio"),
        ("code", t('''
import requests, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
warnings.filterwarnings("ignore")
''', '''
import requests, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
warnings.filterwarnings("ignore")
''')),
        ("code", t('''
GCS = "https://storage.googleapis.com/gcp-public-data-landsat/LC08/01/191/025/"
SCENES = {"léto": "LC08_L1TP_191025_20190626_20190705_01_T1", "podzim": "LC08_L1TP_191025_20181013_20181030_01_T1"}   # ◀ parametr: dvě scény s různou výškou Slunce
LON, LAT, SIZE = 15.70, 50.70, 12000               # ◀ parametr: střed výřezu (Krkonoše) a jeho strana (m)
x, y = Transformer.from_crs(4326, 32633, always_xy=True).transform(LON, LAT)
X0, Y0 = round((x - SIZE / 2) / 30) * 30, round((y - SIZE / 2) / 30) * 30
BANDS = {2: "modrá", 3: "zelená", 4: "červená", 5: "NIR", 6: "SWIR1", 7: "SWIR2"}
DEM = "https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N50_00_E015_00_DEM/Copernicus_DSM_COG_10_N50_00_E015_00_DEM.tif"
WORLDCOVER = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N48E015_Map.tif"
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2)

def mtl(scene):
    txt = requests.get(f"{GCS}{scene}/{scene}_MTL.txt", timeout=60).text
    return {k.strip(): v.strip().strip('"') for k, v in (l.split(" = ") for l in txt.splitlines() if " = " in l)}

def read(scene, band):
    with rasterio.Env(**ENV), rasterio.open(f"/vsicurl/{GCS}{scene}/{scene}_{band}.TIF") as r:
        w = rasterio.windows.from_bounds(X0, Y0, X0 + SIZE, Y0 + SIZE, r.transform).round_offsets().round_lengths()
        read.transform = r.window_transform(w)
        return r.read(1, window=w).astype(float)

def on_grid(url, shape, resampling=Resampling.bilinear, dtype=np.float32):
    out = np.zeros(shape, dtype)
    with rasterio.Env(**ENV), rasterio.open("/vsicurl/" + url) as r:
        reproject(rasterio.band(r, 1), out, dst_transform=read.transform, dst_crs="EPSG:32633", resampling=resampling)
    return out

L8 = {}
for season, scene in SCENES.items():
    m = mtl(scene)
    el, az = float(m["SUN_ELEVATION"]), float(m["SUN_AZIMUTH"])
    toa = {b: (float(m[f"REFLECTANCE_MULT_BAND_{b}"]) * read(scene, f"B{b}") + float(m[f"REFLECTANCE_ADD_BAND_{b}"])) / np.sin(np.radians(el)) for b in BANDS}
    qa = read(scene, "BQA").astype(int)
    ok = ((qa >> 4) & 1 == 0) & ((qa >> 7) & 3 < 3) & (qa > 1)
    L8[season] = dict(toa=toa, el=el, az=az, ok=ok)
    print(f"{season}: {scene}, výška Slunce {el:.1f}°, azimut {az:.1f}°, jasné pixely {ok.mean():.1%}")
shape = L8["léto"]["toa"][2].shape
dem = on_grid(DEM, shape)
wc = on_grid(WORLDCOVER, shape, Resampling.mode, np.uint8)
print(f"výšky {dem.min():.0f}–{dem.max():.0f} m, les podle WorldCoveru {np.mean(wc == 10):.0%} výřezu")
''', '''
GCS = "https://storage.googleapis.com/gcp-public-data-landsat/LC08/01/191/025/"
SCENES = {"summer": "LC08_L1TP_191025_20190626_20190705_01_T1", "autumn": "LC08_L1TP_191025_20181013_20181030_01_T1"}   # ◀ parameter: two scenes with different sun elevation
LON, LAT, SIZE = 15.70, 50.70, 12000               # ◀ parameter: window centre (Krkonoše) and its side (m)
x, y = Transformer.from_crs(4326, 32633, always_xy=True).transform(LON, LAT)
X0, Y0 = round((x - SIZE / 2) / 30) * 30, round((y - SIZE / 2) / 30) * 30
BANDS = {2: "blue", 3: "green", 4: "red", 5: "NIR", 6: "SWIR1", 7: "SWIR2"}
DEM = "https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N50_00_E015_00_DEM/Copernicus_DSM_COG_10_N50_00_E015_00_DEM.tif"
WORLDCOVER = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_N48E015_Map.tif"
ENV = dict(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2)

def mtl(scene):
    txt = requests.get(f"{GCS}{scene}/{scene}_MTL.txt", timeout=60).text
    return {k.strip(): v.strip().strip('"') for k, v in (l.split(" = ") for l in txt.splitlines() if " = " in l)}

def read(scene, band):
    with rasterio.Env(**ENV), rasterio.open(f"/vsicurl/{GCS}{scene}/{scene}_{band}.TIF") as r:
        w = rasterio.windows.from_bounds(X0, Y0, X0 + SIZE, Y0 + SIZE, r.transform).round_offsets().round_lengths()
        read.transform = r.window_transform(w)
        return r.read(1, window=w).astype(float)

def on_grid(url, shape, resampling=Resampling.bilinear, dtype=np.float32):
    out = np.zeros(shape, dtype)
    with rasterio.Env(**ENV), rasterio.open("/vsicurl/" + url) as r:
        reproject(rasterio.band(r, 1), out, dst_transform=read.transform, dst_crs="EPSG:32633", resampling=resampling)
    return out

L8 = {}
for season, scene in SCENES.items():
    m = mtl(scene)
    el, az = float(m["SUN_ELEVATION"]), float(m["SUN_AZIMUTH"])
    toa = {b: (float(m[f"REFLECTANCE_MULT_BAND_{b}"]) * read(scene, f"B{b}") + float(m[f"REFLECTANCE_ADD_BAND_{b}"])) / np.sin(np.radians(el)) for b in BANDS}
    qa = read(scene, "BQA").astype(int)
    ok = ((qa >> 4) & 1 == 0) & ((qa >> 7) & 3 < 3) & (qa > 1)
    L8[season] = dict(toa=toa, el=el, az=az, ok=ok)
    print(f"{season}: {scene}, sun elevation {el:.1f}°, azimuth {az:.1f}°, clear pixels {ok.mean():.1%}")
shape = L8["summer"]["toa"][2].shape
dem = on_grid(DEM, shape)
wc = on_grid(WORLDCOVER, shape, Resampling.mode, np.uint8)
print(f"heights {dem.min():.0f}–{dem.max():.0f} m, forest according to WorldCover {np.mean(wc == 10):.0%} of the window")
''')),
        ("md", t(
            "## 2. Osvětlení svahu z modelu terénu\n\nNa rovině dopadá přímé sluneční záření pod zenitovým úhlem θ_s, na svahu se sklonem s a orientací a pod úhlem i: cos i = cos θ_s · cos s + sin θ_s · sin s · cos(φ_s − a), kde φ_s je azimut Slunce. Přímé ozáření svahu je úměrné cos i; difuzní světlo oblohy dopadá ze všech směrů a na orientaci svahu závisí mnohem méně.",
            "## 2. Slope illumination from the terrain model\n\nOn flat ground direct sunlight arrives at the zenith angle θ_s, on a slope with gradient s and aspect a at the angle i: cos i = cos θ_s · cos s + sin θ_s · sin s · cos(φ_s − a), where φ_s is the sun azimuth. The direct irradiance of the slope is proportional to cos i; diffuse skylight arrives from all directions and depends much less on the slope aspect.")),
        ("code", t('''
dzdy, dzdx = np.gradient(dem, 30)                  # řádky jdou k jihu, sloupce k východu
dzdE, dzdN = dzdx, -dzdy
slope = np.arctan(np.hypot(dzdE, dzdN))
aspect = np.arctan2(-dzdE, -dzdN) % (2 * np.pi)    # kam svah hledí, ve stupních od severu po směru hodin
for s in L8.values():
    zs, az = np.radians(90 - s["el"]), np.radians(s["az"])
    s["cosi"] = np.cos(zs) * np.cos(slope) + np.sin(zs) * np.sin(slope) * np.cos(az - aspect)
    s["cosz"] = np.cos(zs)
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
im = ax[0].imshow(dem, cmap="terrain"); ax[0].set_title("Copernicus DEM (m)"); fig.colorbar(im, ax=ax[0], shrink=0.8)
for a, (season, s) in zip(ax[1:], L8.items()):
    im = a.imshow(s["cosi"], cmap="gray", vmin=0, vmax=1); a.set_title(f"cos i, {season} (Slunce {s['el']:.0f}°)"); fig.colorbar(im, ax=a, shrink=0.8)
for a in ax: a.axis("off")
plt.show()
for season, s in L8.items():
    print(f"{season}: cos i na rovině {s['cosz']:.2f}, ve výřezu 1.–99. percentil {np.percentile(s['cosi'], 1):.2f} až {np.percentile(s['cosi'], 99):.2f}, "
          f"ve vlastním stínu (cos i < 0) {np.mean(s['cosi'] < 0):.1%} pixelů")
''', '''
dzdy, dzdx = np.gradient(dem, 30)                  # rows run south, columns run east
dzdE, dzdN = dzdx, -dzdy
slope = np.arctan(np.hypot(dzdE, dzdN))
aspect = np.arctan2(-dzdE, -dzdN) % (2 * np.pi)    # where the slope faces, clockwise from north
for s in L8.values():
    zs, az = np.radians(90 - s["el"]), np.radians(s["az"])
    s["cosi"] = np.cos(zs) * np.cos(slope) + np.sin(zs) * np.sin(slope) * np.cos(az - aspect)
    s["cosz"] = np.cos(zs)
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
im = ax[0].imshow(dem, cmap="terrain"); ax[0].set_title("Copernicus DEM (m)"); fig.colorbar(im, ax=ax[0], shrink=0.8)
for a, (season, s) in zip(ax[1:], L8.items()):
    im = a.imshow(s["cosi"], cmap="gray", vmin=0, vmax=1); a.set_title(f"cos i, {season} (sun {s['el']:.0f}°)"); fig.colorbar(im, ax=a, shrink=0.8)
for a in ax: a.axis("off")
plt.show()
for season, s in L8.items():
    print(f"{season}: cos i on flat ground {s['cosz']:.2f}, in the window 1st–99th percentile {np.percentile(s['cosi'], 1):.2f} to {np.percentile(s['cosi'], 99):.2f}, "
          f"in self-shadow (cos i < 0) {np.mean(s['cosi'] < 0):.1%} of pixels")
''')),
        ("task", t(
            "Porovnej mapy cos i v létě a na podzim. Proč se na podzim osvětlení jižních a severních svahů liší mnohem víc a kolik pixelů je ve vlastním stínu? Proč vzorec odrazivosti TOA z notebooku k vizuálu (dělení sinem výšky Slunce) na svahu nedává skutečnou odrazivost povrchu?",
            "Compare the cos i maps in summer and in autumn. Why do south- and north-facing slopes differ much more in autumn, and how many pixels are in self-shadow? Why does the TOA reflectance formula from the visual's notebook (dividing by the sine of the sun elevation) not give the true surface reflectance on a slope?")),
        ("md", t(
            "## 3. Jak silně terén mění odrazivost lesa\n\nVezmeme lesní pixely podle WorldCoveru a proložíme přímku ρ = m · cos i + b. Kdyby svah osvětlovalo jen přímé Slunce a les odrážel stejně do všech směrů, byla by odrazivost úměrná cos i a posun b by byl nulový. Poměr C = b/m je základem C-korekce (Teillet a kol. 1982).",
            "## 3. How strongly the terrain changes forest reflectance\n\nWe take forest pixels according to WorldCover and fit a line ρ = m · cos i + b. If the slope were lit only by direct sun and the forest reflected equally in all directions, reflectance would be proportional to cos i and the offset b would be zero. The ratio C = b/m is the basis of the C-correction (Teillet et al. 1982).")),
        ("code", t('''
forest = (wc == 10) & (slope > np.radians(2))
rows, rng = [], np.random.default_rng(0)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
for a, (season, s) in zip(ax, L8.items()):
    f = forest & s["ok"]
    sel = rng.choice(np.flatnonzero(f.ravel()), 5000, replace=False)
    for b, col in [(2, "tab:blue"), (4, "tab:red"), (5, "tab:purple")]:
        a.scatter(s["cosi"].ravel()[sel], s["toa"][b].ravel()[sel], s=2, alpha=0.3, c=col, label=f"B{b} {BANDS[b]}")
    a.axvline(s["cosz"], color="k", lw=0.8, ls="--")
    a.set(xlabel="cos i", ylabel="ρ TOA", title=f"les, {season} (čárkovaně: rovina)"); a.legend(markerscale=5)
    for b in BANDS:
        k, q = np.polyfit(s["cosi"][f], s["toa"][b][f], 1)
        rows.append({"období": season, "pásmo": f"B{b} {BANDS[b]}", "r": np.corrcoef(s["cosi"][f], s["toa"][b][f])[0, 1],
                     "sklon m": k, "posun b": q, "C = b/m": q / k})
plt.show()
pd.DataFrame(rows).set_index(["období", "pásmo"]).round(3)
''', '''
forest = (wc == 10) & (slope > np.radians(2))
rows, rng = [], np.random.default_rng(0)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
for a, (season, s) in zip(ax, L8.items()):
    f = forest & s["ok"]
    sel = rng.choice(np.flatnonzero(f.ravel()), 5000, replace=False)
    for b, col in [(2, "tab:blue"), (4, "tab:red"), (5, "tab:purple")]:
        a.scatter(s["cosi"].ravel()[sel], s["toa"][b].ravel()[sel], s=2, alpha=0.3, c=col, label=f"B{b} {BANDS[b]}")
    a.axvline(s["cosz"], color="k", lw=0.8, ls="--")
    a.set(xlabel="cos i", ylabel="ρ TOA", title=f"forest, {season} (dashed: flat ground)"); a.legend(markerscale=5)
    for b in BANDS:
        k, q = np.polyfit(s["cosi"][f], s["toa"][b][f], 1)
        rows.append({"season": season, "band": f"B{b} {BANDS[b]}", "r": np.corrcoef(s["cosi"][f], s["toa"][b][f])[0, 1],
                     "slope m": k, "offset b": q, "C = b/m": q / k})
plt.show()
pd.DataFrame(rows).set_index(["season", "band"]).round(3)
''')),
        ("task", t(
            "Ve kterém pásmu a období je vztah s cos i nejsilnější? Proč má modrá pásmo velké C, tedy velký posun ve srovnání se sklonem, a SWIR skoro nulové? Spoj to s podílem difuzního světla oblohy v jednotlivých vlnových délkách.",
            "In which band and season is the relationship with cos i strongest? Why does the blue band have a large C, i.e. a large offset compared with the slope, and SWIR almost zero? Relate it to the share of diffuse skylight at different wavelengths.")),
        ("md", t(
            "## 4. Pět korekcí\n\nKosinová korekce ρ · cos θ_s / cos i předpokládá jen přímé světlo. C-korekce přidá C do čitatele i jmenovatele, Minnaertova korekce ρ · (cos θ_s / cos i)^k odhadne exponent k z dat a SCS+C (Soenen a kol. 2005) bere v úvahu, že stromy rostou svisle, ne kolmo ke svahu. Hodnotíme korelaci s cos i po korekci, rozptyl odrazivosti lesa a poměr mediánů na strmých jižních a severních svazích (u stejného lesa by měl být blízko 1).",
            "## 4. Five corrections\n\nThe cosine correction ρ · cos θ_s / cos i assumes direct light only. The C-correction adds C to both numerator and denominator, the Minnaert correction ρ · (cos θ_s / cos i)^k estimates the exponent k from the data, and SCS+C (Soenen et al. 2005) accounts for trees growing vertically, not perpendicular to the slope. We assess the correlation with cos i after correction, the spread of forest reflectance and the ratio of medians on steep south- and north-facing slopes (for the same forest it should be close to 1).")),
        ("code", t('''
COSI_MIN = 0.15        # ◀ parametr: pixely s cos i pod touto hodnotou se neopravují (skoro ve stínu)

def correct(rho, cosi, cosz, slope, method, f):
    """Topografická korekce odrazivosti rho; parametry metod (C, k) se odhadují na pixelech f."""
    if method == "žádná":
        return rho
    if method == "kosinová":
        return rho * cosz / cosi
    if method == "C":
        m, b = np.polyfit(cosi[f], rho[f], 1)
        return rho * (cosz + b / m) / (cosi + b / m)
    if method == "Minnaert":
        k = np.polyfit(np.log(cosi[f] / cosz), np.log(rho[f]), 1)[0]
        return rho * (cosz / cosi) ** k
    if method == "SCS+C":
        m, b = np.polyfit(cosi[f], rho[f], 1)
        return rho * (np.cos(slope) * cosz + b / m) / (cosi + b / m)
    raise ValueError(method)

METHODS = ["žádná", "kosinová", "C", "Minnaert", "SCS+C"]
sunny, shady = (np.degrees(aspect) > 135) & (np.degrees(aspect) < 225), (np.degrees(aspect) < 45) | (np.degrees(aspect) > 315)
rows = []
for season, s in L8.items():
    f = forest & s["ok"] & (s["cosi"] > COSI_MIN)
    steep = f & (slope > np.radians(15))
    for b in [2, 4, 5, 6]:
        for meth in METHODS:
            c = correct(s["toa"][b], s["cosi"], s["cosz"], slope, meth, f)
            q25, q50, q75 = np.percentile(c[f], [25, 50, 75])
            rows.append({"období": season, "pásmo": f"B{b}", "metoda": meth, "r s cos i": np.corrcoef(s["cosi"][f], c[f])[0, 1],
                         "rozptyl (IQR/medián)": (q75 - q25) / q50,
                         "jižní/severní svahy": np.median(c[steep & sunny]) / np.median(c[steep & shady])})
res = pd.DataFrame(rows).set_index(["období", "pásmo", "metoda"])
res.round(3)
''', '''
COSI_MIN = 0.15        # ◀ parameter: pixels with cos i below this value are not corrected (nearly in shadow)

def correct(rho, cosi, cosz, slope, method, f):
    """Topographic correction of reflectance rho; method parameters (C, k) are estimated on pixels f."""
    if method == "none":
        return rho
    if method == "cosine":
        return rho * cosz / cosi
    if method == "C":
        m, b = np.polyfit(cosi[f], rho[f], 1)
        return rho * (cosz + b / m) / (cosi + b / m)
    if method == "Minnaert":
        k = np.polyfit(np.log(cosi[f] / cosz), np.log(rho[f]), 1)[0]
        return rho * (cosz / cosi) ** k
    if method == "SCS+C":
        m, b = np.polyfit(cosi[f], rho[f], 1)
        return rho * (np.cos(slope) * cosz + b / m) / (cosi + b / m)
    raise ValueError(method)

METHODS = ["none", "cosine", "C", "Minnaert", "SCS+C"]
sunny, shady = (np.degrees(aspect) > 135) & (np.degrees(aspect) < 225), (np.degrees(aspect) < 45) | (np.degrees(aspect) > 315)
rows = []
for season, s in L8.items():
    f = forest & s["ok"] & (s["cosi"] > COSI_MIN)
    steep = f & (slope > np.radians(15))
    for b in [2, 4, 5, 6]:
        for meth in METHODS:
            c = correct(s["toa"][b], s["cosi"], s["cosz"], slope, meth, f)
            q25, q50, q75 = np.percentile(c[f], [25, 50, 75])
            rows.append({"season": season, "band": f"B{b}", "method": meth, "r with cos i": np.corrcoef(s["cosi"][f], c[f])[0, 1],
                         "spread (IQR/median)": (q75 - q25) / q50,
                         "south/north slopes": np.median(c[steep & sunny]) / np.median(c[steep & shady])})
res = pd.DataFrame(rows).set_index(["season", "band", "method"])
res.round(3)
''')),
        ("task", t(
            "Která metoda překorigovává (záporné r, poměr jižních a severních svahů pod 1) a proč nejvíc v modré a na podzim? Proč u C, Minnaertovy korekce a SCS+C vychází r skoro přesně nula a proč to samo o sobě nedokazuje, že korekce funguje? Navrhni poctivější ověření (např. odhad parametrů na jedné polovině výřezu a hodnocení na druhé).",
            "Which method overcorrects (negative r, south/north ratio below 1) and why most in the blue band and in autumn? Why does r come out almost exactly zero for C, Minnaert and SCS+C, and why does that alone not prove the correction works? Suggest a fairer check (e.g. estimating the parameters on one half of the window and assessing on the other).")),
        ("md", t(
            "## 5. Mapy a vegetační index",
            "## 5. Maps and the vegetation index")),
        ("code", t('''
SHOW, BAND = "podzim", 5           # ◀ parametr: období a pásmo pro mapy
s = L8[SHOW]
f = forest & s["ok"] & (s["cosi"] > COSI_MIN)
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
for a, meth in zip(ax, ["žádná", "kosinová", "SCS+C"]):
    c = np.where(s["cosi"] > COSI_MIN, correct(s["toa"][BAND], s["cosi"], s["cosz"], slope, meth, f), np.nan)
    a.imshow(c, cmap="gray", vmin=0, vmax=np.nanpercentile(s["toa"][BAND], 99)); a.set_title(f"B{BAND}, {SHOW}, korekce: {meth}"); a.axis("off")
plt.show()
ndvi = {season: (v["toa"][5] - v["toa"][4]) / (v["toa"][5] + v["toa"][4]) for season, v in L8.items()}
for season, v in L8.items():
    fs = forest & v["ok"]
    print(f"{season}: korelace s cos i v lese: NIR {np.corrcoef(v['cosi'][fs], v['toa'][5][fs])[0, 1]:.2f}, "
          f"červená {np.corrcoef(v['cosi'][fs], v['toa'][4][fs])[0, 1]:.2f}, NDVI {np.corrcoef(v['cosi'][fs], ndvi[season][fs])[0, 1]:.2f}")
''', '''
SHOW, BAND = "autumn", 5           # ◀ parameter: season and band for the maps
s = L8[SHOW]
f = forest & s["ok"] & (s["cosi"] > COSI_MIN)
fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
for a, meth in zip(ax, ["none", "cosine", "SCS+C"]):
    c = np.where(s["cosi"] > COSI_MIN, correct(s["toa"][BAND], s["cosi"], s["cosz"], slope, meth, f), np.nan)
    a.imshow(c, cmap="gray", vmin=0, vmax=np.nanpercentile(s["toa"][BAND], 99)); a.set_title(f"B{BAND}, {SHOW}, correction: {meth}"); a.axis("off")
plt.show()
ndvi = {season: (v["toa"][5] - v["toa"][4]) / (v["toa"][5] + v["toa"][4]) for season, v in L8.items()}
for season, v in L8.items():
    fs = forest & v["ok"]
    print(f"{season}: correlation with cos i in forest: NIR {np.corrcoef(v['cosi'][fs], v['toa'][5][fs])[0, 1]:.2f}, "
          f"red {np.corrcoef(v['cosi'][fs], v['toa'][4][fs])[0, 1]:.2f}, NDVI {np.corrcoef(v['cosi'][fs], ndvi[season][fs])[0, 1]:.2f}")
''')),
        ("task", t(
            "Kde v opravené mapě zůstávají chyby (strmé severní svahy, místa pod `COSI_MIN`)? Nastav `COSI_MIN` na 0,05 a na 0,3 a popiš rozdíl. Proč kosinová korekce dělá ze stinných svahů nejjasnější místa scény?",
            "Where do errors remain in the corrected map (steep north-facing slopes, places below `COSI_MIN`)? Set `COSI_MIN` to 0.05 and 0.3 and describe the difference. Why does the cosine correction turn shaded slopes into the brightest places in the scene?")),
        ("task", t(
            "V létě NDVI s cos i skoro nekoreluje, na podzim ano. Proč poměrový index vliv terénu vyruší jen tehdy, když je efekt čistě násobný? Které dva rozdíly mezi červenou a NIR (podíl difuzního světla z kroku 3, zář dráhy) to při nízkém Slunci kazí?",
            "In summer NDVI hardly correlates with cos i, in autumn it does. Why does a ratio index cancel the terrain effect only when the effect is purely multiplicative? Which two differences between red and NIR (share of diffuse light from step 3, path radiance) spoil this at low sun?")),
        ("task", t(
            "+ Přesuň výřez do Šumavy (dlaždici DEM a WorldCoveru je pak třeba změnit, scény Landsatu musí pokrývat nové místo) nebo použij místo lesa louky (`wc == 30`). Vyjdou parametry C a k podobně?",
            "+ Move the window to the Šumava mountains (the DEM and WorldCover tiles then have to change, and the Landsat scenes must cover the new place) or use grassland (`wc == 30`) instead of forest. Do the C and k parameters come out similar?")),
    ]
