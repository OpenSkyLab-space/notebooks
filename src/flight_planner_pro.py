from _common import CUZK_HELPER, OPEN_METEO_HELPER

META = {
    "version": "1.0",
    "minutes": 60,
    "visual_stem": "flight_planner",
    "title": {"cs": "Plánovač letu, pokročilá verze: pokrytí snímky, sledování terénu, vítr a baterie",
              "en": "Drone flight planner, advanced: image coverage, terrain following, wind and batteries"},
    "visual": {"cs": "Plánovač letu dronu", "en": "Drone flight planner"},
    "lead": {
        "cs": "Pokročilá verze notebooku k plánování letu. Na zalesněném svahu údolí Vltavy u Roztok porovnáš tři způsoby, jak držet výšku: stálou nad místem vzletu, sledování terénu z DMR 5G a sledování povrchu korun z DMP 1G. Pro každý spočítáš, na kolika snímcích je každý bod vidět, jaký je odstup od stromů a jak rychle by dron musel stoupat. Pak podle dnešní předpovědi větru vybereš směr linek a rozdělíš misi na lety po jedné baterii.",
        "en": "The advanced version of the flight planning notebook. On the wooded slope of the Vltava valley at Roztoky you compare three ways of holding height: constant above the take-off point, following the terrain from DMR 5G, and following the canopy surface from DMP 1G. For each you compute how many images see every point, the clearance above the trees and how fast the drone would have to climb. Then you choose the line direction from today's wind forecast and split the mission into flights of one battery each.",
    },
    "goal": {
        "cs": "spočítat pokrytí území snímky a odstup od povrchu pro tři režimy výšky, určit potřebné vyhlazení výškového profilu podle rychlosti stoupání, najít nejrychlejší směr linek při skutečném větru a rozdělit misi na lety tak, aby na každý návrat zbyla energie.",
        "en": "compute image coverage of the area and clearance above the surface for three height modes, find the smoothing of the height profile needed for the climb rate, find the fastest line direction in real wind, and split the mission into flights so that energy remains for every return.",
    },
    "data": {
        "cs": "DMR 5G (terén) a DMP 1G (povrch včetně vegetace a budov) z ČÚZK, služby ImageServer, buňka 2 m, území 1,2 × 0,8 km na levém svahu údolí Vltavy u Roztok; hodinová předpověď větru v 80 m z Open-Meteo na dnešní den; parametry dronu a kamery Mavic 3E z technického listu výrobce. DMP 1G vznikl z leteckého laserového skenování v letech 2009–2013, takže stromy od té doby mohly vyrůst nebo být pokáceny. Model pokrytí předpokládá kameru mířící kolmo dolů a nepočítá se zákryty (koruna zakryje terén pod sebou), čas otočky je orientační.",
        "en": "DMR 5G (terrain) and DMP 1G (surface including vegetation and buildings) from ČÚZK, ImageServer services, 2 m cells, a 1.2 × 0.8 km area on the left slope of the Vltava valley at Roztoky; today's hourly wind forecast at 80 m from Open-Meteo; drone and camera parameters of the Mavic 3E from the manufacturer's data sheet. DMP 1G comes from airborne laser scanning in 2009–2013, so trees may have grown or been felled since. The coverage model assumes a camera pointing straight down and ignores occlusion (a crown hides the ground beneath it); the turn time is indicative.",
    },
    "sources": {
        "cs": [
            "Digitální model reliéfu České republiky 5. generace (DMR 5G) a Digitální model povrchu České republiky 1. generace (DMP 1G), © ČÚZK, licence CC BY 4.0, služby https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer a https://ags.cuzk.cz/arcgis2/rest/services/dmp1g/ImageServer",
            "ČÚZK: *Technická zpráva k digitálnímu modelu povrchu České republiky 1. generace (DMP 1G)*, https://geoportal.cuzk.gov.cz/Dokumenty/TECHNICKA_ZPRAVA_DMP_1G.pdf (úplná střední chyba výšky 0,4 m pro budovy a 0,7 m pro vegetaci).",
            "Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "DJI: *Mavic 3 Enterprise, specifikace* (https://enterprise.dji.com/mavic-3-enterprise/specs): čip 4/3, 5280 × 3956 px, ohnisko 12,3 mm; stoupání 6 m/s a klesání 6 m/s v normálním režimu; výdrž 45 min; baterie 77 Wh.",
            "Výška letu v otevřené kategorii max. 120 m od nejbližšího bodu zemského povrchu: prováděcí nařízení Komise (EU) 2019/947, příloha, UAS.OPEN.010.",
        ],
        "en": [
            "Digital terrain model of the Czech Republic, 5th generation (DMR 5G) and digital surface model of the Czech Republic, 1st generation (DMP 1G), © ČÚZK, licence CC BY 4.0, services https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer and https://ags.cuzk.cz/arcgis2/rest/services/dmp1g/ImageServer",
            "ČÚZK: *Technical report on the digital surface model of the Czech Republic, 1st generation (DMP 1G)* (in Czech), https://geoportal.cuzk.gov.cz/Dokumenty/TECHNICKA_ZPRAVA_DMP_1G.pdf (total standard height error 0.4 m for buildings and 0.7 m for vegetation).",
            "Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "DJI: *Mavic 3 Enterprise, specs* (https://enterprise.dji.com/mavic-3-enterprise/specs): 4/3 sensor, 5280 × 3956 px, 12.3 mm focal length; climb 6 m/s and descent 6 m/s in normal mode; 45 min endurance; 77 Wh battery.",
            "Flight height in the open category max. 120 m from the closest point of the surface of the earth: Commission Implementing Regulation (EU) 2019/947, Annex, UAS.OPEN.010.",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava", "## 1. Setup")),
        ("code", "%pip install -q rasterio"),
        ("code", t('''
import time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from pyproj import Transformer
from scipy.ndimage import maximum_filter, uniform_filter1d
''' + CUZK_HELPER["cs"] + OPEN_METEO_HELPER["cs"], '''
import time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from pyproj import Transformer
from scipy.ndimage import maximum_filter, uniform_filter1d
''' + CUZK_HELPER["en"] + OPEN_METEO_HELPER["en"])),
        ("md", t(
            "## 2. Terén, povrch a plán linek\n\nDMR 5G popisuje holý terén, DMP 1G povrch, který vidí kamera: koruny stromů a střechy. Jejich rozdíl je výška vegetace a budov. Plán je stejný jako v základní verzi: kamera Mavic 3E, linky východ–západ, místo vzletu na západním okraji.",
            "## 2. Terrain, surface and the line plan\n\nDMR 5G describes the bare terrain, DMP 1G the surface the camera sees: tree crowns and roofs. Their difference is the height of vegetation and buildings. The plan is the same as in the basic version: a Mavic 3E camera, east–west lines, take-off at the western edge.")),
        ("code", t('''
LON, LAT = 14.392, 50.152            # ◀ parametr: střed území (levý svah údolí Vltavy u Roztok)
W, Hh, RES = 1200, 800, 2.0          # šířka (V–Z) a výška (S–J) území v m, buňka 2 m
cx, cy = Transformer.from_crs(4326, 5514, always_xy=True).transform(LON, LAT)
box = (cx - W / 2, cy - Hh / 2, cx + W / 2, cy + Hh / 2)
dmr, _ = cuzk_raster("dmr5g", *box, res=RES)       # terén
dmp, _ = cuzk_raster("dmp1g", *box, res=RES)       # povrch včetně stromů a budov
veg = np.clip(dmp - dmr, 0, None)                   # výška vegetace a budov nad terénem
z_takeoff = float(np.median(dmr[:, :10]))           # místo vzletu na západním okraji
HOME = (0.0, Hh / 2)                                # ◀ parametr: poloha místa vzletu v území (x, y v m)
xs = np.arange(dmr.shape[1]) * RES + RES / 2        # souřadnice středů buněk (x na východ, y na sever)
ys = Hh - np.arange(dmr.shape[0]) * RES - RES / 2
print(f"terén {dmr.min():.0f}–{dmr.max():.0f} m n. m., povrch {dmp.min():.0f}–{dmp.max():.0f} m n. m., místo vzletu {z_takeoff:.0f} m n. m.")
print(f"vegetace nebo budovy vyšší než 2 m na {np.mean(veg > 2):.0%} území, medián jejich výšky {np.median(veg[veg > 2]):.1f} m, 99. percentil {np.percentile(veg, 99):.1f} m")
fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
for a, arr, lbl, cm in [(ax[0], dmr, "terén DMR 5G (m n. m.)", "terrain"), (ax[1], veg, "povrch − terén (m)", "Greens")]:
    im = a.imshow(arr, cmap=cm, extent=(0, W, 0, Hh)); fig.colorbar(im, ax=a, label=lbl)
ax[0].plot(*HOME, "r^", ms=10); plt.show()
''', '''
LON, LAT = 14.392, 50.152            # ◀ parameter: centre of the area (left slope of the Vltava valley at Roztoky)
W, Hh, RES = 1200, 800, 2.0          # width (E–W) and height (N–S) of the area in m, 2 m cells
cx, cy = Transformer.from_crs(4326, 5514, always_xy=True).transform(LON, LAT)
box = (cx - W / 2, cy - Hh / 2, cx + W / 2, cy + Hh / 2)
dmr, _ = cuzk_raster("dmr5g", *box, res=RES)       # terrain
dmp, _ = cuzk_raster("dmp1g", *box, res=RES)       # surface including trees and buildings
veg = np.clip(dmp - dmr, 0, None)                   # height of vegetation and buildings above the terrain
z_takeoff = float(np.median(dmr[:, :10]))           # take-off point at the western edge
HOME = (0.0, Hh / 2)                                # ◀ parameter: position of the take-off point in the area (x, y in m)
xs = np.arange(dmr.shape[1]) * RES + RES / 2        # coordinates of cell centres (x east, y north)
ys = Hh - np.arange(dmr.shape[0]) * RES - RES / 2
print(f"terrain {dmr.min():.0f}–{dmr.max():.0f} m a.s.l., surface {dmp.min():.0f}–{dmp.max():.0f} m a.s.l., take-off {z_takeoff:.0f} m a.s.l.")
print(f"vegetation or buildings taller than 2 m on {np.mean(veg > 2):.0%} of the area, median height {np.median(veg[veg > 2]):.1f} m, 99th percentile {np.percentile(veg, 99):.1f} m")
fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
for a, arr, lbl, cm in [(ax[0], dmr, "terrain DMR 5G (m a.s.l.)", "terrain"), (ax[1], veg, "surface − terrain (m)", "Greens")]:
    im = a.imshow(arr, cmap=cm, extent=(0, W, 0, Hh)); fig.colorbar(im, ax=a, label=lbl)
ax[0].plot(*HOME, "r^", ms=10); plt.show()
''')),
        ("code", t('''
CAM = dict(sw=17.3, sh=13.0, pw=5280, ph=3956, f=12.3)   # Mavic 3E: čip (mm), pixely, ohnisko (mm)
H0 = 80.0             # ◀ parametr: výška letu (m) nad místem vzletu, nad terénem nebo nad povrchem podle režimu
FO, SO = 0.80, 0.70   # ◀ parametr: podélný a příčný překryv
V = 8.0               # ◀ parametr: rychlost vůči vzduchu (m/s)
SMOOTH = 40           # ◀ parametr: délka vyhlazení výškového profilu linky (m) při sledování terénu a povrchu
p, f = CAM["sw"] / CAM["pw"] / 1000, CAM["f"] / 1000
gsd0 = H0 * p / f
base = (1 - FO) * CAM["ph"] * gsd0                  # vzdálenost snímků podél linky (krátká strana snímku podél)
spacing = (1 - SO) * CAM["pw"] * gsd0               # rozestup linek (dlouhá strana napříč)
line_y = np.arange(0, Hh + spacing / 2, spacing)    # linky V–Z
shot_x = np.arange(0, W + base / 2, base)
xline = np.arange(0, W + RES / 2, RES)

def sample(arr, x, y):
    i = np.clip(((Hh - y) / RES).astype(int), 0, arr.shape[0] - 1)
    j = np.clip((x / RES).astype(int), 0, arr.shape[1] - 1)
    return arr[i, j]

def altitude(mode, y, smooth=SMOOTH):
    """Nadmořská výška dronu podél linky y v bodech xline."""
    if mode == "stálá":
        return np.full_like(xline, z_takeoff + H0)
    ref = sample(dmr if mode == "terén" else dmp, xline, np.full_like(xline, y))
    n = max(int(smooth / RES), 1)
    if n > 1:                                         # nejdřív maximum (aby dron nepodletěl vrchol), pak průměr
        ref = uniform_filter1d(maximum_filter(ref, size=n, mode="nearest"), size=n, mode="nearest")
    return ref + H0

print(f"GSD při výšce {H0:.0f} m: {gsd0 * 100:.2f} cm/px, báze {base:.1f} m, rozestup linek {spacing:.1f} m, {len(line_y)} linek × {len(shot_x)} snímků")
print(f"teoreticky na rovině: každý bod na {1 / ((1 - FO) * (1 - SO)):.1f} snímcích")
''', '''
CAM = dict(sw=17.3, sh=13.0, pw=5280, ph=3956, f=12.3)   # Mavic 3E: sensor (mm), pixels, focal length (mm)
H0 = 80.0             # ◀ parameter: flight height (m) above the take-off point, the terrain or the surface depending on the mode
FO, SO = 0.80, 0.70   # ◀ parameter: forward and side overlap
V = 8.0               # ◀ parameter: airspeed (m/s)
SMOOTH = 40           # ◀ parameter: smoothing length of the line height profile (m) for terrain and surface following
p, f = CAM["sw"] / CAM["pw"] / 1000, CAM["f"] / 1000
gsd0 = H0 * p / f
base = (1 - FO) * CAM["ph"] * gsd0                  # distance between shots along the line (short side of the image along)
spacing = (1 - SO) * CAM["pw"] * gsd0               # line spacing (long side across)
line_y = np.arange(0, Hh + spacing / 2, spacing)    # E–W lines
shot_x = np.arange(0, W + base / 2, base)
xline = np.arange(0, W + RES / 2, RES)

def sample(arr, x, y):
    i = np.clip(((Hh - y) / RES).astype(int), 0, arr.shape[0] - 1)
    j = np.clip((x / RES).astype(int), 0, arr.shape[1] - 1)
    return arr[i, j]

def altitude(mode, y, smooth=SMOOTH):
    """Altitude of the drone along line y at the points xline."""
    if mode == "constant":
        return np.full_like(xline, z_takeoff + H0)
    ref = sample(dmr if mode == "terrain" else dmp, xline, np.full_like(xline, y))
    n = max(int(smooth / RES), 1)
    if n > 1:                                         # maximum first (so the drone does not undercut a peak), then the mean
        ref = uniform_filter1d(maximum_filter(ref, size=n, mode="nearest"), size=n, mode="nearest")
    return ref + H0

print(f"GSD at {H0:.0f} m: {gsd0 * 100:.2f} cm/px, base {base:.1f} m, line spacing {spacing:.1f} m, {len(line_y)} lines × {len(shot_x)} shots")
print(f"in theory on flat ground: every point on {1 / ((1 - FO) * (1 - SO)):.1f} images")
''')),
        ("md", t(
            "## 3. Na kolika snímcích je každý bod vidět\n\nPro každý snímek spočítáme, které buňky povrchu leží v jeho záběru. Záběr se zvětšuje s výškou kamery nad tím, co vidí, takže koruny blíž ke kameře pokryje menší výřez. Porovnáme tři režimy: **stálá** výška H0 nad místem vzletu, **terén** (H0 nad DMR 5G) a **povrch** (H0 nad DMP 1G). U sledování se výškový profil linky vyhlazuje (`SMOOTH`).",
            "## 3. How many images see every point\n\nFor each image we compute which surface cells lie in its footprint. The footprint grows with the camera height above what it sees, so crowns closer to the camera are covered by a smaller patch. We compare three modes: **constant** height H0 above the take-off point, **terrain** (H0 above DMR 5G) and **surface** (H0 above DMP 1G). For following, the height profile of the line is smoothed (`SMOOTH`).")),
        ("code", t('''
MODES = ["stálá", "terén", "povrch"]   # stálá výška nad místem vzletu, sledování DMR 5G, sledování DMP 1G
hx, hy = CAM["sh"] / CAM["f"] / 2, CAM["sw"] / CAM["f"] / 2   # poloviční záběr na 1 m výšky: podél linky (x), napříč (y)
cov, rows = {}, {}
for mode in MODES:
    cnt = np.zeros(dmr.shape, dtype=np.int16)
    agl_all, clear = [], np.inf
    for y in line_y:
        zl = altitude(mode, y)
        surf = sample(dmp, xline, np.full_like(xline, y))
        agl_all.append(zl - surf); clear = min(clear, float((zl - surf).min()))
        for x in shot_x:
            zc = float(np.interp(x, xline, zl))
            ext = zc - dmp.min()
            i0, i1 = int(max((Hh - y - ext * hy) / RES, 0)), int(min((Hh - y + ext * hy) / RES + 1, dmr.shape[0]))
            j0, j1 = int(max((x - ext * hx) / RES, 0)), int(min((x + ext * hx) / RES + 1, dmr.shape[1]))
            h = zc - dmp[i0:i1, j0:j1]                 # výška kamery nad viděným povrchem
            cnt[i0:i1, j0:j1] += (np.abs(xs[j0:j1][None, :] - x) <= h * hx) & (np.abs(ys[i0:i1][:, None] - y) <= h * hy) & (h > 0)
    cov[mode] = cnt
    inner = cnt[20:-20, 20:-20]                        # bez okrajového pásu 40 m
    agl_all = np.concatenate(agl_all)
    rows[mode] = {"medián snímků na bod": np.median(inner), "podíl bodů s < 9 snímky": np.mean(inner < 9),
                  "GSD na povrchu 5 % (cm)": np.percentile(agl_all, 5) * p / f * 100, "GSD na povrchu 95 % (cm)": np.percentile(agl_all, 95) * p / f * 100,
                  "nejmenší odstup od povrchu (m)": clear}
fig, ax = plt.subplots(1, 3, figsize=(16, 4))
for a, mode in zip(ax, MODES):
    im = a.imshow(cov[mode], cmap="viridis", vmin=0, vmax=30, extent=(0, W, 0, Hh)); a.set_title(mode); a.set_xticks([]); a.set_yticks([])
fig.colorbar(im, ax=ax, label="počet snímků, na kterých je bod vidět"); plt.show()
pd.DataFrame(rows).T.round(2)
''', '''
MODES = ["constant", "terrain", "surface"]   # constant height above take-off, following DMR 5G, following DMP 1G
hx, hy = CAM["sh"] / CAM["f"] / 2, CAM["sw"] / CAM["f"] / 2   # half footprint per 1 m of height: along the line (x), across (y)
cov, rows = {}, {}
for mode in MODES:
    cnt = np.zeros(dmr.shape, dtype=np.int16)
    agl_all, clear = [], np.inf
    for y in line_y:
        zl = altitude(mode, y)
        surf = sample(dmp, xline, np.full_like(xline, y))
        agl_all.append(zl - surf); clear = min(clear, float((zl - surf).min()))
        for x in shot_x:
            zc = float(np.interp(x, xline, zl))
            ext = zc - dmp.min()
            i0, i1 = int(max((Hh - y - ext * hy) / RES, 0)), int(min((Hh - y + ext * hy) / RES + 1, dmr.shape[0]))
            j0, j1 = int(max((x - ext * hx) / RES, 0)), int(min((x + ext * hx) / RES + 1, dmr.shape[1]))
            h = zc - dmp[i0:i1, j0:j1]                 # camera height above the surface it sees
            cnt[i0:i1, j0:j1] += (np.abs(xs[j0:j1][None, :] - x) <= h * hx) & (np.abs(ys[i0:i1][:, None] - y) <= h * hy) & (h > 0)
    cov[mode] = cnt
    inner = cnt[20:-20, 20:-20]                        # without the 40 m edge strip
    agl_all = np.concatenate(agl_all)
    rows[mode] = {"median images per point": np.median(inner), "share of points on < 9 images": np.mean(inner < 9),
                  "GSD on the surface 5 % (cm)": np.percentile(agl_all, 5) * p / f * 100, "GSD on the surface 95 % (cm)": np.percentile(agl_all, 95) * p / f * 100,
                  "smallest clearance above the surface (m)": clear}
fig, ax = plt.subplots(1, 3, figsize=(16, 4))
for a, mode in zip(ax, MODES):
    im = a.imshow(cov[mode], cmap="viridis", vmin=0, vmax=30, extent=(0, W, 0, Hh)); a.set_title(mode); a.set_xticks([]); a.set_yticks([])
fig.colorbar(im, ax=ax, label="number of images in which the point is visible"); plt.show()
pd.DataFrame(rows).T.round(2)
''')),
        ("task", t(
            "Na rovině by byl každý bod na tolika snímcích, kolik vypsala buňka s plánem. Proč při sledování terénu vychází medián menší a při stálé výšce a sledování povrchu větší? Kde v mapě stálé výšky jsou místa s nejmenším počtem snímků a proč? Pro fotogrammetrii lesa se obvykle doporučuje vyšší překryv: změň `FO` a `SO` a sleduj podíl bodů s méně než 9 snímky.",
            "On flat ground every point would be on as many images as the plan cell printed. Why is the median lower for terrain following and higher for constant height and surface following? Where in the constant-height map are the points with the fewest images, and why? Forest photogrammetry usually calls for higher overlap: change `FO` and `SO` and watch the share of points on fewer than 9 images.")),
        ("task", t(
            "Podívej se na nejmenší odstup od povrchu a rozsah GSD. Proč je při stálé výšce odstup nad nejvyššími korunami nejmenší a GSD nejvíc kolísá? Co by se stalo při sledování terénu, kdyby stromy od skenování v letech 2009–2013 vyrostly o 5 m nebo kdyby v území stál stožár, který DMP nezachytil? Nastav `H0 = 50` a porovnej.",
            "Look at the smallest clearance above the surface and the range of GSD. Why is the clearance above the tallest crowns smallest and GSD most variable at constant height? What would happen with terrain following if the trees had grown 5 m since the 2009–2013 scanning, or if there were a mast in the area that the DMP did not capture? Set `H0 = 50` and compare.")),
        ("md", t(
            "## 4. Jak rychle by dron musel stoupat\n\nPři sledování terénu nebo povrchu letí dron rychlostí V a výška se mění podle profilu linky. Svislá rychlost je V krát sklon profilu. Když přesáhne limit stoupání nebo klesání, musí dron zpomalit. Tabulka ukazuje různé délky vyhlazení: 2 m znamená bez vyhlazení.",
            "## 4. How fast the drone would have to climb\n\nWhen following terrain or surface, the drone flies at speed V and its height follows the line profile. The vertical speed is V times the slope of the profile. When it exceeds the climb or descent limit, the drone has to slow down. The table shows different smoothing lengths: 2 m means no smoothing.")),
        ("code", t('''
V_UP, V_DOWN = 6.0, 6.0      # ◀ parametr: nejvyšší rychlost stoupání a klesání (m/s), Mavic 3E v normálním režimu
rows = {}
for mode in ["terén", "povrch"]:
    for sm in [2, 20, 60, 100]:
        vz = np.concatenate([np.diff(altitude(mode, y, sm)[::d]) / RES * V for y in line_y for d in (1, -1)])
        top = V * min(V_UP / vz.max(), V_DOWN / -vz.min(), 1.0)
        dev = np.concatenate([altitude(mode, y, sm) - altitude(mode, y, 2) for y in line_y])
        rows[(mode, sm)] = {"největší stoupání (m/s)": vz.max(), "podíl úseků nad limitem": np.mean((vz > V_UP) | (vz < -V_DOWN)),
                            "rychlost, aby stačil (m/s)": top, "dron výš než H0 o (m, medián)": np.median(dev), "max (m)": dev.max()}
pd.DataFrame(rows).T.round(2)
''', '''
V_UP, V_DOWN = 6.0, 6.0      # ◀ parameter: maximum climb and descent rate (m/s), Mavic 3E in normal mode
rows = {}
for mode in ["terrain", "surface"]:
    for sm in [2, 20, 60, 100]:
        vz = np.concatenate([np.diff(altitude(mode, y, sm)[::d]) / RES * V for y in line_y for d in (1, -1)])
        top = V * min(V_UP / vz.max(), V_DOWN / -vz.min(), 1.0)
        dev = np.concatenate([altitude(mode, y, sm) - altitude(mode, y, 2) for y in line_y])
        rows[(mode, sm)] = {"largest climb rate (m/s)": vz.max(), "share of segments over the limit": np.mean((vz > V_UP) | (vz < -V_DOWN)),
                            "speed to keep up (m/s)": top, "drone higher than H0 by (m, median)": np.median(dev), "max (m)": dev.max()}
pd.DataFrame(rows).T.round(2)
''')),
        ("task", t(
            "Proč je profil povrchu mnohem strmější než profil terénu, i když jde o stejné linky? Jakou nejkratší délku vyhlazení potřebuješ, aby dron při 8 m/s stačil s limitem 6 m/s, a co tím ztratíš (sloupce s tím, o kolik letí výš než H0)? Jak by se výsledek změnil při rychlosti 12 m/s?",
            "Why is the surface profile much steeper than the terrain profile, although the lines are the same? What is the shortest smoothing length that lets the drone keep within the 6 m/s limit at 8 m/s, and what do you lose (the columns showing how much higher than H0 it flies)? How would the result change at 12 m/s?")),
        ("md", t(
            "## 5. Vítr a směr linek\n\nDron drží rychlost vůči vzduchu V. Na lince po větru se rychlost vůči zemi zvětší, proti větru zmenší a při bočním větru musí dron nadržovat, takže se zmenší v obou směrech. Spočítáme čas celé mise pro azimuty linek od 0° do 165° s dnešním větrem v 80 m. Linky pokrývají celý obdélník území, otočka stojí `T_TURN` sekund.",
            "## 5. Wind and line direction\n\nThe drone keeps airspeed V. On a downwind line the ground speed increases, upwind it decreases, and in a crosswind the drone has to crab, so it decreases in both directions. We compute the time of the whole mission for line azimuths from 0° to 165° with today's wind at 80 m. The lines cover the whole rectangle of the area, a turn costs `T_TURN` seconds.")),
        ("code", t('''
w = open_meteo({"latitude": LAT, "longitude": LON, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "Europe/Prague",
                "hourly": "wind_speed_80m,wind_direction_80m"})
met = pd.DataFrame(w["hourly"]).set_index("time")
hour = 6 + int(met.wind_speed_80m.values[6:21].argmax())
WIND = float(met.wind_speed_80m.iloc[hour])    # ◀ parametr: rychlost větru (m/s); výchozí je největrnější hodina dneška mezi 6 a 20 h
WDIR = float(met.wind_direction_80m.iloc[hour]) # ◀ parametr: odkud vítr fouká (°, 0 = od severu)
T_TURN = 8.0                                    # ◀ parametr: čas na jednu otočku (s), orientačně
P_AVG = 77.0 / (45 / 60)                        # průměrný výkon (W) z udávané výdrže 45 min s baterií 77 Wh
to = np.radians(WDIR + 180)
wvec = WIND * np.array([np.sin(to), np.cos(to)])  # vektor větru (kam fouká), složky na východ a na sever
print(f"{met.index[hour]}: vítr v 80 m {WIND:.1f} m/s od {WDIR:.0f}°")

def leg_time(a, b, v=V):
    """Čas přeletu z a do b (s); dron drží rychlost v vůči vzduchu a nadržuje proti bočnímu větru."""
    d = np.subtract(b, a); L = np.hypot(*d)
    if L < 1e-6:
        return 0.0
    e = d / L
    along, cross = wvec @ e, wvec @ np.array([-e[1], e[0]])
    gs = np.sqrt(max(v ** 2 - cross ** 2, 0)) + along
    return L / gs if gs > 0.3 else np.inf

gy, gx = np.mgrid[RES / 2:Hh:RES, RES / 2:W:RES]
def plan(az):
    """Linky pod azimutem az (° od severu) přes celé území, v pořadí letu (had)."""
    a = np.radians(az); ux, uy = np.sin(a), np.cos(a)
    u, v = gx * ux + gy * uy, -gx * uy + gy * ux
    lines = []
    for k, vk in enumerate(np.arange(v.min(), v.max() + spacing / 2, spacing)):
        sel = np.abs(v - vk) <= RES
        if sel.any():
            u0, u1 = u[sel].min(), u[sel].max()
            ends = ((u0 * ux - vk * uy, u0 * uy + vk * ux), (u1 * ux - vk * uy, u1 * uy + vk * ux))
            lines.append(ends if k % 2 == 0 else ends[::-1])
    return lines

def mission_time(lines):
    t = sum(leg_time(a, b) for a, b in lines)
    t += sum(leg_time(lines[i][1], lines[i + 1][0]) for i in range(len(lines) - 1)) + 2 * T_TURN * (len(lines) - 1)
    return t

rows = []
for az in range(0, 180, 15):
    L = plan(az); t = mission_time(L)
    rows.append({"azimut linek (°)": az, "linek": len(L), "délka linek (km)": sum(np.hypot(*np.subtract(b, a)) for a, b in L) / 1000,
                 "čas (min)": t / 60, "energie (Wh)": P_AVG * t / 3600})
orient = pd.DataFrame(rows).set_index("azimut linek (°)")
orient.round(1)
''', '''
w = open_meteo({"latitude": LAT, "longitude": LON, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "Europe/Prague",
                "hourly": "wind_speed_80m,wind_direction_80m"})
met = pd.DataFrame(w["hourly"]).set_index("time")
hour = 6 + int(met.wind_speed_80m.values[6:21].argmax())
WIND = float(met.wind_speed_80m.iloc[hour])    # ◀ parameter: wind speed (m/s); default is today's windiest hour between 6 and 20 h
WDIR = float(met.wind_direction_80m.iloc[hour]) # ◀ parameter: direction the wind blows from (°, 0 = from the north)
T_TURN = 8.0                                    # ◀ parameter: time for one turn (s), indicative
P_AVG = 77.0 / (45 / 60)                        # average power (W) from the stated endurance of 45 min with a 77 Wh battery
to = np.radians(WDIR + 180)
wvec = WIND * np.array([np.sin(to), np.cos(to)])  # wind vector (where it blows to), east and north components
print(f"{met.index[hour]}: wind at 80 m {WIND:.1f} m/s from {WDIR:.0f}°")

def leg_time(a, b, v=V):
    """Time to fly from a to b (s); the drone keeps airspeed v and crabs into the crosswind."""
    d = np.subtract(b, a); L = np.hypot(*d)
    if L < 1e-6:
        return 0.0
    e = d / L
    along, cross = wvec @ e, wvec @ np.array([-e[1], e[0]])
    gs = np.sqrt(max(v ** 2 - cross ** 2, 0)) + along
    return L / gs if gs > 0.3 else np.inf

gy, gx = np.mgrid[RES / 2:Hh:RES, RES / 2:W:RES]
def plan(az):
    """Lines at azimuth az (° from north) across the whole area, in flight order (lawnmower)."""
    a = np.radians(az); ux, uy = np.sin(a), np.cos(a)
    u, v = gx * ux + gy * uy, -gx * uy + gy * ux
    lines = []
    for k, vk in enumerate(np.arange(v.min(), v.max() + spacing / 2, spacing)):
        sel = np.abs(v - vk) <= RES
        if sel.any():
            u0, u1 = u[sel].min(), u[sel].max()
            ends = ((u0 * ux - vk * uy, u0 * uy + vk * ux), (u1 * ux - vk * uy, u1 * uy + vk * ux))
            lines.append(ends if k % 2 == 0 else ends[::-1])
    return lines

def mission_time(lines):
    t = sum(leg_time(a, b) for a, b in lines)
    t += sum(leg_time(lines[i][1], lines[i + 1][0]) for i in range(len(lines) - 1)) + 2 * T_TURN * (len(lines) - 1)
    return t

rows = []
for az in range(0, 180, 15):
    L = plan(az); t = mission_time(L)
    rows.append({"line azimuth (°)": az, "lines": len(L), "line length (km)": sum(np.hypot(*np.subtract(b, a)) for a, b in L) / 1000,
                 "time (min)": t / 60, "energy (Wh)": P_AVG * t / 3600})
orient = pd.DataFrame(rows).set_index("line azimuth (°)")
orient.round(1)
''')),
        ("task", t(
            "Při jakém azimutu je dnes mise nejkratší a jak velký je rozdíl proti nejhoršímu? Proč jsou linky po větru a proti větru pomalejší než linky napříč větru, i když se zisk po větru a ztráta proti větru zdánlivě vyrovnají? Nastav `WIND = 2` a pak `WIND = 0`: který azimut vyhraje teď a proč (počet linek a otoček)? Co se stane, když `WIND` přesáhne `V`?",
            "At which azimuth is today's mission shortest, and how big is the difference from the worst? Why are downwind and upwind lines slower than crosswind lines, although the gain downwind and the loss upwind seem to cancel out? Set `WIND = 2` and then `WIND = 0`: which azimuth wins now and why (number of lines and turns)? What happens when `WIND` exceeds `V`?")),
        ("md", t(
            "## 6. Rozdělení mise na baterie\n\nLinky se přidávají do letu jedna po druhé, dokud po další lince zbývá energie na přímý návrat k místu vzletu. Pak dron přistane, vymění baterii a další let začne přeletem k následující lince.",
            "## 6. Splitting the mission into batteries\n\nLines are added to a flight one by one as long as energy for a direct return to the take-off point remains after the next line. Then the drone lands, the battery is swapped and the next flight starts with a transit to the following line.")),
        ("code", t('''
AZ = int(orient["čas (min)"].idxmin())   # ◀ parametr: azimut linek (°); výchozí je nejrychlejší z tabulky
E_BAT, TEMP, RESERVE = 77.0, 1.0, 0.20     # ◀ parametr: baterie (Wh), využitelná kapacita (v mrazu 0,7–0,8), rezerva při přistání
E_USE = E_BAT * TEMP * (1 - RESERVE)

def split(lines):
    """Rozdělí linky na lety: další linku přidá, jen když po ní zbude energie na návrat domů."""
    flights, cur, e, pos = [], [], 0.0, HOME
    for a, b in lines:
        need = (leg_time(pos, a) + leg_time(a, b) + 2 * T_TURN) * P_AVG / 3600
        if cur and e + need + leg_time(b, HOME) * P_AVG / 3600 > E_USE:
            flights.append((cur, e + leg_time(pos, HOME) * P_AVG / 3600))
            cur, e, pos = [], 0.0, HOME
            need = (leg_time(pos, a) + leg_time(a, b) + 2 * T_TURN) * P_AVG / 3600
        cur.append((a, b)); e += need; pos = b
    flights.append((cur, e + leg_time(pos, HOME) * P_AVG / 3600))
    return flights

fl = split(plan(AZ))
print(f"azimut {AZ}°, využitelná energie baterie {E_USE:.1f} Wh: {len(fl)} letů")
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.imshow(dmr, cmap="Greys", extent=(0, W, 0, Hh), alpha=0.5)
for k, (lines, e) in enumerate(fl):
    col = plt.cm.tab10(k % 10)
    for a, b in lines:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=1.5)
    print(f"let {k + 1}: {len(lines)} linek, {e:.1f} Wh")
ax.plot(*HOME, "r^", ms=12); ax.arrow(W - 120, Hh - 120, wvec[0] * 12, wvec[1] * 12, width=6, color="k")
ax.set(xlim=(-20, W + 20), ylim=(-20, Hh + 20), title=f"lety po baterii, vítr {WIND:.1f} m/s od {WDIR:.0f}° (šipka)"); plt.show()
''', '''
AZ = int(orient["time (min)"].idxmin())   # ◀ parameter: line azimuth (°); default is the fastest in the table
E_BAT, TEMP, RESERVE = 77.0, 1.0, 0.20     # ◀ parameter: battery (Wh), usable capacity (0.7–0.8 in frost), landing reserve
E_USE = E_BAT * TEMP * (1 - RESERVE)

def split(lines):
    """Split the lines into flights: add the next line only if energy for the return home remains after it."""
    flights, cur, e, pos = [], [], 0.0, HOME
    for a, b in lines:
        need = (leg_time(pos, a) + leg_time(a, b) + 2 * T_TURN) * P_AVG / 3600
        if cur and e + need + leg_time(b, HOME) * P_AVG / 3600 > E_USE:
            flights.append((cur, e + leg_time(pos, HOME) * P_AVG / 3600))
            cur, e, pos = [], 0.0, HOME
            need = (leg_time(pos, a) + leg_time(a, b) + 2 * T_TURN) * P_AVG / 3600
        cur.append((a, b)); e += need; pos = b
    flights.append((cur, e + leg_time(pos, HOME) * P_AVG / 3600))
    return flights

fl = split(plan(AZ))
print(f"azimuth {AZ}°, usable battery energy {E_USE:.1f} Wh: {len(fl)} flights")
fig, ax = plt.subplots(figsize=(8, 5.5))
ax.imshow(dmr, cmap="Greys", extent=(0, W, 0, Hh), alpha=0.5)
for k, (lines, e) in enumerate(fl):
    col = plt.cm.tab10(k % 10)
    for a, b in lines:
        ax.plot([a[0], b[0]], [a[1], b[1]], color=col, lw=1.5)
    print(f"flight {k + 1}: {len(lines)} lines, {e:.1f} Wh")
ax.plot(*HOME, "r^", ms=12); ax.arrow(W - 120, Hh - 120, wvec[0] * 12, wvec[1] * 12, width=6, color="k")
ax.set(xlim=(-20, W + 20), ylim=(-20, Hh + 20), title=f"flights per battery, wind {WIND:.1f} m/s from {WDIR:.0f}° (arrow)"); plt.show()
''')),
        ("task", t(
            "Kolik letů mise potřebuje a proč mají lety různý počet linek? Přesuň místo vzletu `HOME` do středu území (600, 400) a spusť znovu buňky od načtení dat: ušetříš let? Nastav `TEMP = 0.75` jako v mrazu. Proč se při plánování počítá s návratem proti větru, i když vítr může během letu zeslábnout?",
            "How many flights does the mission need, and why do the flights have different numbers of lines? Move the take-off point `HOME` to the centre of the area (600, 400) and rerun the cells from the data loading: do you save a flight? Set `TEMP = 0.75` as in frost. Why does planning count on returning against the wind, even though the wind may weaken during the flight?")),
        ("task", t(
            "+ Nastav `LON, LAT` na svah nad Brněnskou přehradou (16.4798, 49.2467) nebo na údolí u Hosína u Hluboké nad Vltavou (14.4769, 49.0452), kde stoupá terén také od východu k západu, a porovnej pokrytí, vyhlazení a počet letů s Roztoky.",
            "+ Set `LON, LAT` to the slope above the Brno reservoir (16.4798, 49.2467) or the valley near Hosín by Hluboká nad Vltavou (14.4769, 49.0452), where the terrain also rises from east to west, and compare coverage, smoothing and number of flights with Roztoky.")),
    ]
