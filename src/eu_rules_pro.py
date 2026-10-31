from _common import CUZK_HELPER

META = {
    "version": "1.0",
    "minutes": 60,
    "visual_stem": "eu_rules",
    "title": {"cs": "Kde smím létat, pokročilá verze: geometrie zón, mapa povolené výšky, letové hladiny a cyklus AIRAC",
              "en": "Where may I fly, advanced: zone geometry, a map of allowed height, flight levels and the AIRAC cycle"},
    "visual": {"cs": "Kde a jak smím létat", "en": "Where and how may I fly"},
    "lead": {
        "cs": "Pokročilá verze notebooku o zeměpisných zónách UAS. Na aktuálních datech ŘLP zjistíš, které zóny se dronu podle svislých hranic vůbec týkají, sestavíš mapu povolené výšky letu kolem Brna z gridových sítí, spočítáš ze zpráv METAR, jak vysoko ve skutečnosti leží letové hladiny, zkontroluješ data platnosti zón proti cyklu AIRAC a nakreslíš svislý řez zónami z Bystrce na letiště Tuřany nad skutečným terénem. Je to výuková pomůcka, ne právní posouzení: před letem vždy ověř zóny v aplikaci DroneMap a podmínky v opatřeních obecné povahy ÚCL.",
        "en": "The advanced version of the notebook on UAS geographical zones. On current ŘLP data you find out which zones concern a drone at all according to their vertical limits, build a map of allowed flight height around Brno from the grids, compute from METAR reports how high flight levels really are, check the effective dates of zones against the AIRAC cycle and draw a vertical cross-section of the zones from Bystrc to Tuřany airport over the real terrain. This is a teaching aid, not legal advice: before a flight always check the zones in the DroneMap app and the conditions in the CAA measures of general nature (OOP).",
    },
    "goal": {
        "cs": "roztřídit zóny podle dolní hranice a určit, kde se týkají dronu, spojit gridové sítě GRID_CTR a GRID_ATZ do mapy povolené výšky, převést letové hladiny na skutečnou nadmořskou výšku podle QNH a teploty, ověřit data platnosti proti cyklu AIRAC a sestavit svislý řez zónami nad terénem DMR 5G.",
        "en": "sort zones by their lower limit and determine where they concern a drone, combine the GRID_CTR and GRID_ATZ grids into a map of allowed height, convert flight levels to true altitude from QNH and temperature, check effective dates against the AIRAC cycle and build a vertical cross-section of the zones over the DMR 5G terrain.",
    },
    "data": {
        "cs": "zeměpisné zóny UAS ve formátu GeoJSON (referenční hranice) ze stránky ŘLP https://aim.rlp.cz/?lang=cz&p=uas-gz, stažené v okamžiku spuštění, kromě vrstev větších než zvolený limit; zprávy METAR letiště Brno-Tuřany (LKTB) za posledních 7 dní z Aviation Weather Center (NOAA); nadmořská výška terénu z Digitálního modelu reliéfu ČR 5. generace (DMR 5G, ČÚZK). Převod letové hladiny na skutečnou výšku používá standardní atmosféru ICAO s teplotou upravenou podle letiště, je to přiblížení.",
        "en": "UAS geographical zones as GeoJSON (reference boundaries) from the ŘLP page https://aim.rlp.cz/?lang=en&p=uas-gz, downloaded at run time, except layers larger than the chosen limit; METAR reports of Brno-Tuřany airport (LKTB) for the last 7 days from the Aviation Weather Center (NOAA); terrain elevation from the Digital terrain model of the Czech Republic, 5th generation (DMR 5G, ČÚZK). The conversion of a flight level to true altitude uses the ICAO standard atmosphere with the temperature adjusted to the airport; it is an approximation.",
    },
    "sources": {
        "cs": [
            "Zeměpisné zóny UAS: Řízení letového provozu České republiky, s. p., AIM, https://aim.rlp.cz/?lang=cz&p=uas-gz; mapa zón: https://dronemap.gov.cz",
            "Prováděcí nařízení Komise (EU) 2019/947 o pravidlech a postupech pro provoz bezpilotních letadel, čl. 15 (zeměpisné zóny UAS).",
            "Úřad pro civilní letectví: opatření obecné povahy k zeměpisným zónám UAS (LKR311 až LKR320), https://www.caa.gov.cz",
            "Zprávy METAR: NOAA Aviation Weather Center, Data API, https://aviationweather.gov/data/api/",
            "Výška terénu: Digitální model reliéfu ČR 5. generace (DMR 5G), © ČÚZK, licence CC BY 4.0, služba https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer",
            "ICAO (1993). *Manual of the ICAO Standard Atmosphere*, Doc 7488, 3. vyd. (tlaková výška).",
            "ICAO, Annex 15 k Úmluvě o mezinárodním civilním letectví, *Aeronautical Information Services* (systém AIRAC, 28denní cyklus).",
        ],
        "en": [
            "UAS geographical zones: Air Navigation Services of the Czech Republic (ŘLP ČR), AIM, https://aim.rlp.cz/?lang=en&p=uas-gz; zone map: https://dronemap.gov.cz",
            "Commission Implementing Regulation (EU) 2019/947 on the rules and procedures for the operation of unmanned aircraft, Article 15 (UAS geographical zones).",
            "Civil Aviation Authority of the Czech Republic: measures of general nature on UAS geographical zones (LKR311 to LKR320), https://www.caa.gov.cz",
            "METAR reports: NOAA Aviation Weather Center, Data API, https://aviationweather.gov/data/api/",
            "Terrain elevation: Digital terrain model of the Czech Republic, 5th generation (DMR 5G), © ČÚZK, licence CC BY 4.0, service https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer",
            "ICAO (1993). *Manual of the ICAO Standard Atmosphere*, Doc 7488, 3rd ed. (pressure altitude).",
            "ICAO, Annex 15 to the Convention on International Civil Aviation, *Aeronautical Information Services* (the AIRAC system, 28-day cycle).",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a zóny\n\nNačteme seznam aktuálních zón ze stránky ŘLP a stáhneme všechny vrstvy do zvoleného limitu velikosti a obě gridové sítě. Stahování trvá asi minutu.",
                 "## 1. Setup and zones\n\nWe load the list of current zones from the ŘLP page and download all layers up to the chosen size limit and both grids. Downloading takes about a minute.")),
        ("code", "%pip install -q shapely pyproj rasterio"),
        ("code", t('''
import re, html, time, datetime as dt, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import shape, Point, LineString, box
import shapely
from pyproj import Transformer
import rasterio
''' + CUZK_HELPER["cs"], '''
import re, html, time, datetime as dt, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import shape, Point, LineString, box
import shapely
from pyproj import Transformer
import rasterio
''' + CUZK_HELPER["en"])),
        ("code", t('''
AIM = "https://aim.rlp.cz"
def get(url, tries=4, **kw):
    for i in range(tries):
        try:
            r = requests.get(url, timeout=300, **kw); r.raise_for_status(); return r
        except requests.RequestException as e:
            print(url.split("/")[-1], type(e).__name__, "– zkusím znovu"); time.sleep(5 * (i + 1))
    raise RuntimeError(f"Nepodařilo se stáhnout {url}")

page = get(f"{AIM}/?lang=cz&p=uas-gz").content.decode("utf-8")
rows = []
for tr in re.findall(r"<tr.*?</tr>", page, re.S):
    href = re.search(r'href="(/data/uas/[^"]+\\.json)"', tr)
    cols = [re.sub(r"\\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
    if href and len(cols) >= 4 and "/actual/" in href.group(1):
        mb = re.search(r"([\\d.,]+)\\s*(kB|MB)", cols[3])
        rows.append({"code": cols[2].replace(".json", ""), "desc": cols[1], "MB": float(mb.group(1).replace(",", ".")) * (1e-3 if mb.group(2) == "kB" else 1), "url": AIM + href.group(1)})
zones = pd.DataFrame(rows).set_index("code")
MAX_MB = 20                   # ◀ parametr: největší stahovaný soubor (MB); obě gridové sítě se stáhnou vždy
T_UTM = Transformer.from_crs(4326, 32633, always_xy=True)
to_utm = lambda g: shapely.transform(g, lambda xy: np.column_stack(T_UTM.transform(xy[:, 0], xy[:, 1])))
layers = {}
for code, z in zones.iterrows():
    if z.MB <= MAX_MB or code in ("GRID_CTR", "GRID_ATZ"):
        feats = [f for f in get(z.url).json()["features"] if f.get("geometry")]
        layers[code] = pd.DataFrame({"geom": [shape(f["geometry"]) for f in feats], **{k: [f["properties"].get(k) for f in feats] for k in ("ident", "vertical_limit", "effective_date")}})
print(f"staženo {len(layers)} vrstev, {sum(len(v) for v in layers.values())} prvků; vynechané velké vrstvy:", ", ".join(c for c in zones.index if c not in layers))
''', '''
AIM = "https://aim.rlp.cz"
def get(url, tries=4, **kw):
    for i in range(tries):
        try:
            r = requests.get(url, timeout=300, **kw); r.raise_for_status(); return r
        except requests.RequestException as e:
            print(url.split("/")[-1], type(e).__name__, "– retrying"); time.sleep(5 * (i + 1))
    raise RuntimeError(f"Could not download {url}")

page = get(f"{AIM}/?lang=en&p=uas-gz").content.decode("utf-8")
rows = []
for tr in re.findall(r"<tr.*?</tr>", page, re.S):
    href = re.search(r'href="(/data/uas/[^"]+\\.json)"', tr)
    cols = [re.sub(r"\\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
    if href and len(cols) >= 4 and "/actual/" in href.group(1):
        mb = re.search(r"([\\d.,]+)\\s*(kB|MB)", cols[3])
        rows.append({"code": cols[2].replace(".json", ""), "desc": cols[1], "MB": float(mb.group(1).replace(",", ".")) * (1e-3 if mb.group(2) == "kB" else 1), "url": AIM + href.group(1)})
zones = pd.DataFrame(rows).set_index("code")
MAX_MB = 20                   # ◀ parameter: largest file to download (MB); both grids are always downloaded
T_UTM = Transformer.from_crs(4326, 32633, always_xy=True)
to_utm = lambda g: shapely.transform(g, lambda xy: np.column_stack(T_UTM.transform(xy[:, 0], xy[:, 1])))
layers = {}
for code, z in zones.iterrows():
    if z.MB <= MAX_MB or code in ("GRID_CTR", "GRID_ATZ"):
        feats = [f for f in get(z.url).json()["features"] if f.get("geometry")]
        layers[code] = pd.DataFrame({"geom": [shape(f["geometry"]) for f in feats], **{k: [f["properties"].get(k) for f in feats] for k in ("ident", "vertical_limit", "effective_date")}})
print(f"downloaded {len(layers)} layers, {sum(len(v) for v in layers.values())} features; large layers left out:", ", ".join(c for c in zones.index if c not in layers))
''')),
        ("md", t(
            "## 2. Které zóny se dronu vůbec týkají?\n\nKaždá zóna platí jen mezi dolní a horní hranicí. Dolní hranice může být u země (GND), ve výšce nad terénem (AGL), v nadmořské výšce (AMSL) nebo letová hladina (FL, zde přepočtená ve standardní atmosféře). U hranic v AMSL a FL záleží na terénu: rozhodneme, zda zóna zasahuje dron ve zvolené výšce všude v ČR, nikde, nebo jen nad určitou nadmořskou výškou terénu.",
            "## 2. Which zones concern a drone at all?\n\nEvery zone applies only between its lower and upper limit. The lower limit can be at the ground (GND), a height above ground (AGL), an altitude above sea level (AMSL) or a flight level (FL, here converted with the standard atmosphere). For limits in AMSL and FL the terrain matters: we decide whether the zone reaches a drone at the chosen height everywhere in Czechia, nowhere, or only above a certain terrain altitude.")),
        ("code", t('''
H_MIN, H_MAX = 115, 1603      # nejnižší a nejvyšší bod ČR (m n. m.): Labe u Hřenska a Sněžka
DRONE_AGL = 120               # ◀ parametr: výška letu nad terénem (m)
def lower_amsl(txt):
    """Dolní hranice zóny jako nadmořská výška (m); vrátí typ hranice a hodnotu."""
    s = txt.split("-", 1)[0].strip().upper().replace(" ", "")
    if s in ("GND", "SFC"): return "GND", 0.0
    if s.startswith("FL"): return "FL", float(s[2:]) * 100 * 0.3048
    m = re.match(r"([\\d.]+)(FT|M)(AGL|AMSL|MSL)", s)
    v = float(m.group(1)) * (0.3048 if m.group(2) == "FT" else 1)
    return ("AGL", v) if m.group(3) == "AGL" else ("AMSL", v)
rows = []
for code, df in layers.items():
    if code.startswith("GRID"): continue
    for vl, n in df.vertical_limit.value_counts().items():
        kind, v = lower_amsl(vl)
        if kind in ("GND", "AGL"):
            where = "všude" if v <= DRONE_AGL else "nikde"
        else:                                                    # AMSL nebo FL: záleží na terénu
            where = "nikde" if v > H_MAX + DRONE_AGL else ("všude" if v <= H_MIN + DRONE_AGL else f"kde je terén nad {v - DRONE_AGL:.0f} m n. m.")
        rows.append({"vrstva": code, "svislé hranice": vl, "prvků": n, "dolní hranice": kind,
                     "dolní hranice (m n. m.)": None if kind in ("GND", "AGL") else round(v), f"týká se dronu ve {DRONE_AGL} m": where})
lim = pd.DataFrame(rows)
pd.set_option("display.max_rows", 100)
print(lim.to_string(index=False))
print(lim.groupby("dolní hranice")["prvků"].sum().to_string())
''', '''
H_MIN, H_MAX = 115, 1603      # lowest and highest point of Czechia (m a.s.l.): the Elbe at Hřensko and Sněžka
DRONE_AGL = 120               # ◀ parameter: flight height above ground (m)
def lower_amsl(txt):
    """Lower limit of a zone as altitude (m); returns the type of limit and the value."""
    s = txt.split("-", 1)[0].strip().upper().replace(" ", "")
    if s in ("GND", "SFC"): return "GND", 0.0
    if s.startswith("FL"): return "FL", float(s[2:]) * 100 * 0.3048
    m = re.match(r"([\\d.]+)(FT|M)(AGL|AMSL|MSL)", s)
    v = float(m.group(1)) * (0.3048 if m.group(2) == "FT" else 1)
    return ("AGL", v) if m.group(3) == "AGL" else ("AMSL", v)
rows = []
for code, df in layers.items():
    if code.startswith("GRID"): continue
    for vl, n in df.vertical_limit.value_counts().items():
        kind, v = lower_amsl(vl)
        if kind in ("GND", "AGL"):
            where = "everywhere" if v <= DRONE_AGL else "nowhere"
        else:                                                    # AMSL or FL: depends on the terrain
            where = "nowhere" if v > H_MAX + DRONE_AGL else ("everywhere" if v <= H_MIN + DRONE_AGL else f"where the terrain is above {v - DRONE_AGL:.0f} m a.s.l.")
        rows.append({"layer": code, "vertical limits": vl, "features": n, "lower limit": kind,
                     "lower limit (m a.s.l.)": None if kind in ("GND", "AGL") else round(v), f"affects a drone at {DRONE_AGL} m": where})
lim = pd.DataFrame(rows)
pd.set_option("display.max_rows", 100)
print(lim.to_string(index=False))
print(lim.groupby("lower limit")["features"].sum().to_string())
''')),
        ("task", t(
            "Kolik prvků začíná u země a kolik až ve výšce? Které vrstvy začínají vysoko a proč se dronu ve 120 m v nížině netýkají? Najdi zóny, které dron zasáhnou jen na horách, a urči, nad jakou nadmořskou výškou terénu. Nastav DRONE_AGL na 50 m a 150 m: co se změní? Proč nestačí znát jen vodorovnou hranici zóny?",
            "How many features start at the ground and how many only at height? Which layers start high, and why do they not concern a drone at 120 m in the lowlands? Find the zones that reach a drone only in the mountains and determine above what terrain altitude. Set DRONE_AGL to 50 m and 150 m: what changes? Why is it not enough to know only the horizontal boundary of a zone?")),
        ("md", t(
            "## 3. Mapa povolené výšky kolem Brna\n\nGridové sítě GRID_CTR (kolem řízených letišť, buňky 30″) a GRID_ATZ (prostory neřízeného letového provozu, buňky 15″) udávají v každé buňce, do jaké výšky nad terénem je let povolen bez dalšího souhlasu. Území vzorkujeme po 7,5″, takže každý bod leží uvnitř jedné buňky. Vedle toho spočítáme, kolik zón od země (GND) se v bodě překrývá.",
            "## 3. A map of allowed height around Brno\n\nThe GRID_CTR grid (around controlled airports, 30″ cells) and the GRID_ATZ grid (areas of uncontrolled air traffic, 15″ cells) state in every cell up to what height above ground flight is allowed without further approval. We sample the area every 7.5″, so each point lies inside one cell. Besides that we count how many zones from the ground (GND) overlap at a point.")),
        ("code", t('''
BBOX = (16.45, 49.10, 16.80, 49.30)   # ◀ parametr: území (zem. délka a šířka: západ, jih, východ, sever)
STEP = 1 / 480                        # krok 7,5″: polovina buňky GRID_ATZ, čtvrtina buňky GRID_CTR
lon = np.arange(BBOX[0] + STEP / 2, BBOX[2], STEP); lat = np.arange(BBOX[1] + STEP / 2, BBOX[3], STEP)
LON, LAT = np.meshgrid(lon, lat)
hmax = lambda txt: float(re.search(r"-\\s*([\\d.]+)\\s*m\\s*AGL", txt).group(1))
allowed = np.full(LON.shape, np.nan)
for code in ("GRID_CTR", "GRID_ATZ"):
    for g, v in zip(layers[code].geom, layers[code].vertical_limit):
        if g.intersects(box(*BBOX)):
            inside = shapely.contains_xy(g, LON, LAT)
            allowed[inside] = np.fmin(allowed[inside], hmax(v))
restr = [c for c in layers if c.startswith(("LKR312", "LKR313", "LKR314", "LKR315", "LKR318", "LKR319"))]   # zóny od země (GND)
nzones = np.zeros(LON.shape, int)
for code in restr:
    for g in layers[code].geom:
        if g.intersects(box(*BBOX)):
            nzones += shapely.contains_xy(g, LON, LAT)
classes = pd.cut(pd.Series(allowed.ravel()), [-1, 0, 30, 60, 90, 119, 120], labels=["0 m", "1–30 m", "31–60 m", "61–90 m", "91–119 m", "120 m"])
share = (100 * classes.value_counts(normalize=False) / allowed.size).reindex(classes.cat.categories)
share["mimo síť"] = 100 * np.isnan(allowed).mean()
print("podíl území podle povolené výšky ze sítí GRID_CTR a GRID_ATZ (%):"); print(share.round(1).to_string())
print(f"podíl území v aspoň jedné zóně od země (vrstvy {', '.join(restr)}): {100 * (nzones > 0).mean():.0f} %")
fig, ax = plt.subplots(1, 2, figsize=(16, 5.5))
ext = (BBOX[0], BBOX[2], BBOX[1], BBOX[3]); asp = 1 / np.cos(np.radians(LAT.mean()))
im = ax[0].imshow(allowed, origin="lower", extent=ext, cmap="RdYlGn", vmin=0, vmax=120, aspect=asp); plt.colorbar(im, ax=ax[0], label="povolená výška (m AGL)")
ax[0].set_title("povolená výška podle gridových sítí (šedá = mimo síť)"); ax[0].set_facecolor("0.8")
im = ax[1].imshow(nzones, origin="lower", extent=ext, cmap="viridis", aspect=asp); plt.colorbar(im, ax=ax[1], label="počet zón")
ax[1].set_title("počet zón od země, které se v bodě překrývají")
plt.show()
''', '''
BBOX = (16.45, 49.10, 16.80, 49.30)   # ◀ parameter: area (longitude and latitude: west, south, east, north)
STEP = 1 / 480                        # 7.5″ step: half a GRID_ATZ cell, a quarter of a GRID_CTR cell
lon = np.arange(BBOX[0] + STEP / 2, BBOX[2], STEP); lat = np.arange(BBOX[1] + STEP / 2, BBOX[3], STEP)
LON, LAT = np.meshgrid(lon, lat)
hmax = lambda txt: float(re.search(r"-\\s*([\\d.]+)\\s*m\\s*AGL", txt).group(1))
allowed = np.full(LON.shape, np.nan)
for code in ("GRID_CTR", "GRID_ATZ"):
    for g, v in zip(layers[code].geom, layers[code].vertical_limit):
        if g.intersects(box(*BBOX)):
            inside = shapely.contains_xy(g, LON, LAT)
            allowed[inside] = np.fmin(allowed[inside], hmax(v))
restr = [c for c in layers if c.startswith(("LKR312", "LKR313", "LKR314", "LKR315", "LKR318", "LKR319"))]   # zones from the ground (GND)
nzones = np.zeros(LON.shape, int)
for code in restr:
    for g in layers[code].geom:
        if g.intersects(box(*BBOX)):
            nzones += shapely.contains_xy(g, LON, LAT)
classes = pd.cut(pd.Series(allowed.ravel()), [-1, 0, 30, 60, 90, 119, 120], labels=["0 m", "1–30 m", "31–60 m", "61–90 m", "91–119 m", "120 m"])
share = (100 * classes.value_counts(normalize=False) / allowed.size).reindex(classes.cat.categories)
share["outside the grid"] = 100 * np.isnan(allowed).mean()
print("share of the area by allowed height from GRID_CTR and GRID_ATZ (%):"); print(share.round(1).to_string())
print(f"share of the area in at least one zone from the ground (layers {', '.join(restr)}): {100 * (nzones > 0).mean():.0f} %")
fig, ax = plt.subplots(1, 2, figsize=(16, 5.5))
ext = (BBOX[0], BBOX[2], BBOX[1], BBOX[3]); asp = 1 / np.cos(np.radians(LAT.mean()))
im = ax[0].imshow(allowed, origin="lower", extent=ext, cmap="RdYlGn", vmin=0, vmax=120, aspect=asp); plt.colorbar(im, ax=ax[0], label="allowed height (m AGL)")
ax[0].set_title("allowed height from the grids (grey = outside the grid)"); ax[0].set_facecolor("0.8")
im = ax[1].imshow(nzones, origin="lower", extent=ext, cmap="viridis", aspect=asp); plt.colorbar(im, ax=ax[1], label="number of zones")
ax[1].set_title("number of zones from the ground overlapping at a point")
plt.show()
''')),
        ("task", t(
            "Jaký podíl území smíš podle sítí přeletět ve 120 m, jaký jen do 30 m a kde nesmíš vůbec? Kde je povolená výška 0 m a proč právě tam (porovnej s polohou letiště Tuřany, letiště Medlánky a heliportů v pravé mapě)? Znamená šedé území mimo síť, že tam smíš letět bez omezení? Vzpomeň na velké vrstvy, které jsme nestáhli.",
            "What share of the area may you fly over at 120 m according to the grids, what share only up to 30 m, and where may you not fly at all? Where is the allowed height 0 m, and why there (compare with the position of Tuřany airport, Medlánky airfield and the heliports in the right map)? Does the grey area outside the grid mean you may fly there without restrictions? Remember the large layers we did not download.")),
        ("md", t(
            "## 4. Jak vysoko je letová hladina?\n\nLetová hladina FL je tlaková výška ve stovkách stop při standardním tlaku 1013,25 hPa. Skutečná nadmořská výška hladiny závisí na tlaku u země (QNH) a na teplotě vzduchu: v teplém vzduchu leží výš, ve studeném níž. Vezmeme QNH a teplotu ze zpráv METAR za posledních 7 dní a spočítáme skutečnou výšku hladin, které jsou dolní hranicí prostorů LKR320A.",
            "## 4. How high is a flight level?\n\nA flight level FL is a pressure altitude in hundreds of feet at the standard pressure of 1013.25 hPa. The true altitude of the level depends on the pressure at the ground (QNH) and on the air temperature: in warm air it lies higher, in cold air lower. We take QNH and temperature from METAR reports for the last 7 days and compute the true altitude of the levels that are the lower limit of LKR320A areas.")),
        ("code", t('''
STATION = "LKTB"              # ◀ parametr: letiště, ze kterého vezmeme QNH a teplotu (zprávy METAR)
FLS = [65, 95]                # ◀ parametr: letové hladiny (např. dolní hranice prostorů LKR320A)
met = pd.DataFrame(get("https://aviationweather.gov/api/data/metar", params={"ids": STATION, "format": "json", "hours": 168}).json())
met["time"] = pd.to_datetime(met.reportTime); met = met.dropna(subset=["altim", "temp"]).sort_values("time").set_index("time")
h_s = float(met.elev.iloc[0])
pa = lambda p: 44330.77 * (1 - (p / 1013.25) ** 0.190263)                 # tlaková výška (m) v ISA
def true_alt(fl, qnh, t_s):
    """Skutečná nadmořská výška letové hladiny: nejdřív výška podle QNH, pak oprava na teplotu vrstvy mezi letištěm a hladinou."""
    z_q = fl * 100 * 0.3048 - pa(qnh)                                       # výška na výškoměru nastaveném na QNH
    t_isa = 288.15 - 0.0065 * (h_s + z_q) / 2                               # průměrná teplota vrstvy v ISA
    t_act = t_s + 273.15 - 0.0065 * (z_q - h_s) / 2                         # průměrná skutečná teplota vrstvy (pokles 6,5 K/km)
    return h_s + (z_q - h_s) * t_act / t_isa
fig, ax = plt.subplots(figsize=(12, 4))
rows = {}
for fl in FLS:
    z = true_alt(fl, met.altim, met.temp)
    ax.plot(z.index, z, label=f"FL{fl}"); ax.axhline(fl * 100 * 0.3048, color="k", lw=0.8, ls=":")
    rows[f"FL{fl}"] = {"FL × 100 ft (m)": fl * 100 * 0.3048, "min (m n. m.)": z.min(), "max (m n. m.)": z.max(), "rozpětí (m)": z.max() - z.min()}
print(f"{STATION}: {len(met)} zpráv METAR, QNH {met.altim.min():.0f}–{met.altim.max():.0f} hPa, teplota {met.temp.min():.0f}–{met.temp.max():.0f} °C, letiště {h_s:.0f} m n. m.")
print(pd.DataFrame(rows).T.to_string(float_format=lambda v: f"{v:.0f}"))
ax.set_ylabel("skutečná výška (m n. m.)"); ax.legend(); ax.grid(alpha=0.3); ax.set_title(f"skutečná výška letových hladin podle QNH a teploty na {STATION}")
plt.show()
''', '''
STATION = "LKTB"              # ◀ parameter: the airport whose QNH and temperature we use (METAR reports)
FLS = [65, 95]                # ◀ parameter: flight levels (e.g. lower limits of LKR320A areas)
met = pd.DataFrame(get("https://aviationweather.gov/api/data/metar", params={"ids": STATION, "format": "json", "hours": 168}).json())
met["time"] = pd.to_datetime(met.reportTime); met = met.dropna(subset=["altim", "temp"]).sort_values("time").set_index("time")
h_s = float(met.elev.iloc[0])
pa = lambda p: 44330.77 * (1 - (p / 1013.25) ** 0.190263)                 # pressure altitude (m) in ISA
def true_alt(fl, qnh, t_s):
    """True altitude of a flight level: first the altitude on QNH, then a correction for the temperature of the layer between the airport and the level."""
    z_q = fl * 100 * 0.3048 - pa(qnh)                                       # altitude on an altimeter set to QNH
    t_isa = 288.15 - 0.0065 * (h_s + z_q) / 2                               # mean temperature of the layer in ISA
    t_act = t_s + 273.15 - 0.0065 * (z_q - h_s) / 2                         # mean actual temperature of the layer (lapse 6.5 K/km)
    return h_s + (z_q - h_s) * t_act / t_isa
fig, ax = plt.subplots(figsize=(12, 4))
rows = {}
for fl in FLS:
    z = true_alt(fl, met.altim, met.temp)
    ax.plot(z.index, z, label=f"FL{fl}"); ax.axhline(fl * 100 * 0.3048, color="k", lw=0.8, ls=":")
    rows[f"FL{fl}"] = {"FL × 100 ft (m)": fl * 100 * 0.3048, "min (m a.s.l.)": z.min(), "max (m a.s.l.)": z.max(), "range (m)": z.max() - z.min()}
print(f"{STATION}: {len(met)} METAR reports, QNH {met.altim.min():.0f}–{met.altim.max():.0f} hPa, temperature {met.temp.min():.0f}–{met.temp.max():.0f} °C, airport {h_s:.0f} m a.s.l.")
print(pd.DataFrame(rows).T.to_string(float_format=lambda v: f"{v:.0f}"))
ax.set_ylabel("true altitude (m a.s.l.)"); ax.legend(); ax.grid(alpha=0.3); ax.set_title(f"true altitude of flight levels from QNH and temperature at {STATION}")
plt.show()
''')),
        ("task", t(
            "O kolik metrů se během týdne měnila skutečná výška FL65 a FL95? Co ji ovlivňuje víc, QNH, nebo teplota? Spočítej, kolik metrů výšky odpovídá změně QNH o 1 hPa. Jak vysoko nad Děvínem (asi 550 m n. m.) začíná prostor LKTB4 (FL65) v nejnižším a nejvyšším případě? Proč se v letectví vyšší hranice udávají letovými hladinami, i když jejich skutečná výška kolísá?",
            "By how many metres did the true altitude of FL65 and FL95 change during the week? What affects it more, QNH or temperature? Compute how many metres of height correspond to a change of QNH by 1 hPa. How high above Děvín (about 550 m a.s.l.) does the LKTB4 area (FL65) start in the lowest and the highest case? Why are higher limits in aviation given as flight levels, although their true altitude varies?")),
        ("md", t(
            "## 5. Kdy zóny platí: cyklus AIRAC\n\nZměny leteckých informací se zveřejňují k pevným datům cyklu AIRAC, která jdou po 28 dnech, a ŘLP aktualizuje data zón v návaznosti na tento cyklus. Každý prvek zóny má datum platnosti (effective_date). Zjistíme, která data platnosti jsou data AIRAC.",
            "## 5. When zones apply: the AIRAC cycle\n\nChanges to aeronautical information are published for the fixed dates of the AIRAC cycle, which follow every 28 days, and ŘLP updates the zone data in line with this cycle. Every zone feature has an effective date (effective_date). We find out which effective dates are AIRAC dates.")),
        ("code", t('''
AIRAC_REF = pd.Timestamp("2024-01-25", tz="UTC")     # známé datum AIRAC (cyklus 2401), cykly jdou po 28 dnech
eff = pd.concat([pd.DataFrame({"vrstva": c, "platí od": pd.to_datetime(d.effective_date)}) for c, d in layers.items()])
tab = eff.groupby("platí od")["vrstva"].agg(["count", lambda s: ", ".join(sorted(set(s)))])
tab.columns = ["prvků", "vrstvy"]
days = (tab.index - AIRAC_REF).days
tab["datum AIRAC"] = days % 28 == 0
tab["cyklus"] = [f"{(AIRAC_REF + pd.Timedelta(days=28 * (d // 28))).year % 100:02d}{1 + ((AIRAC_REF + pd.Timedelta(days=28 * (d // 28))) - pd.Timestamp(f'{(AIRAC_REF + pd.Timedelta(days=28 * (d // 28))).year}-01-01', tz='UTC')).days // 28:02d}" if d % 28 == 0 else "" for d in days]
pd.set_option("display.max_colwidth", 80)
print(tab.to_string())
today = pd.Timestamp.now(tz="UTC").normalize()
nxt = AIRAC_REF + pd.Timedelta(days=28 * ((today - AIRAC_REF).days // 28 + 1))
print(f"dnes {today:%Y-%m-%d}, příští datum AIRAC {nxt:%Y-%m-%d}")
''', '''
AIRAC_REF = pd.Timestamp("2024-01-25", tz="UTC")     # a known AIRAC date (cycle 2401), cycles follow every 28 days
eff = pd.concat([pd.DataFrame({"layer": c, "effective": pd.to_datetime(d.effective_date)}) for c, d in layers.items()])
tab = eff.groupby("effective")["layer"].agg(["count", lambda s: ", ".join(sorted(set(s)))])
tab.columns = ["features", "layers"]
days = (tab.index - AIRAC_REF).days
tab["AIRAC date"] = days % 28 == 0
tab["cycle"] = [f"{(AIRAC_REF + pd.Timedelta(days=28 * (d // 28))).year % 100:02d}{1 + ((AIRAC_REF + pd.Timedelta(days=28 * (d // 28))) - pd.Timestamp(f'{(AIRAC_REF + pd.Timedelta(days=28 * (d // 28))).year}-01-01', tz='UTC')).days // 28:02d}" if d % 28 == 0 else "" for d in days]
pd.set_option("display.max_colwidth", 80)
print(tab.to_string())
today = pd.Timestamp.now(tz="UTC").normalize()
nxt = AIRAC_REF + pd.Timedelta(days=28 * ((today - AIRAC_REF).days // 28 + 1))
print(f"today {today:%Y-%m-%d}, next AIRAC date {nxt:%Y-%m-%d}")
''')),
        ("task", t(
            "Která data platnosti odpovídají cyklu AIRAC a která ne? Které vrstvy se měnily nejčastěji a proč právě ty? Zóna OOPUAS-0055 má datum mimo cyklus: najdi na stránce ŘLP nebo v DroneMap, o jakou zónu jde, a vysvětli, proč může vzniknout mimo cyklus. Kdy je příští datum AIRAC a co uděláš před letem po tomto datu?",
            "Which effective dates match the AIRAC cycle and which do not? Which layers changed most often, and why those? The OOPUAS-0055 zone has a date outside the cycle: find on the ŘLP page or in DroneMap what zone it is, and explain why it can be created outside the cycle. When is the next AIRAC date, and what do you do before a flight after that date?")),
        ("md", t(
            "## 6. Svislý řez zónami\n\nNa přímce z Bystrce na letiště Brno-Tuřany navzorkujeme terén z DMR 5G po 25 m a pro každou zónu, kterou přímka protíná, převedeme dolní a horní hranici na nadmořskou výšku (AGL nad terénem, FL jako ve standardní atmosféře). Černá čára je terén plus povolená výška z gridových sítí.",
            "## 6. A vertical cross-section of the zones\n\nAlong the line from Bystrc to Brno-Tuřany airport we sample the terrain from DMR 5G every 25 m, and for every zone the line crosses we convert the lower and upper limit to altitude (AGL above the terrain, FL as in the standard atmosphere). The black line is the terrain plus the allowed height from the grids.")),
        ("code", t('''
A = (49.2467, 16.4798)        # ◀ parametr: začátek profilu (Bystrc, Kozí horka)
B = (49.1510, 16.6940)        # ◀ parametr: konec profilu (letiště Brno-Tuřany)
FLIGHT_AGL = 120              # ◀ parametr: plánovaná výška letu nad terénem (m)
T_JTSK = Transformer.from_crs(4326, 5514, always_xy=True)
(xa, xb), (ya, yb) = T_JTSK.transform([A[1], B[1]], [A[0], B[0]])
dem, tr = cuzk_raster("dmr5g", min(xa, xb) - 100, min(ya, yb) - 100, max(xa, xb) + 100, max(ya, yb) + 100, res=10.0)
n = int(np.hypot(xb - xa, yb - ya) // 25) + 1
d = np.linspace(0, np.hypot(xb - xa, yb - ya), n); xs = xa + (xb - xa) * d / d[-1]; ys = ya + (yb - ya) * d / d[-1]
col, row = ~tr * (xs, ys)
terr = dem[np.clip(row.astype(int), 0, dem.shape[0] - 1), np.clip(col.astype(int), 0, dem.shape[1] - 1)]
plon = np.linspace(A[1], B[1], n); plat = np.linspace(A[0], B[0], n)       # na 15 km stačí lineární interpolace v zem. souřadnicích
def amsl(txt, ground):
    s = txt.strip().upper().replace(" ", "")
    if s in ("GND", "SFC"): return ground
    if s.startswith("FL"): return np.full_like(ground, float(s[2:]) * 100 * 0.3048)
    m = re.match(r"([\\d.]+)(FT|M)(AGL|AMSL|MSL)", s)
    v = float(m.group(1)) * (0.3048 if m.group(2) == "FT" else 1)
    return ground + v if m.group(3) == "AGL" else np.full_like(ground, v)
line = LineString(zip(plon, plat))
fig, ax = plt.subplots(figsize=(15, 6))
ax.fill_between(d / 1000, 0, terr, color="0.55", zorder=3)
k = 0
for code, df in layers.items():
    if code.startswith("GRID"): continue
    for g, ident, vl in zip(df.geom, df.ident, df.vertical_limit):
        if not g.intersects(line): continue
        inside = shapely.contains_xy(g, plon, plat)
        lo, hi = vl.split("-", 1)
        ax.fill_between(d / 1000, amsl(lo, terr), amsl(hi, terr), where=inside, alpha=0.25, color=f"C{k % 10}", label=f"{code} {ident}: {vl}"); k += 1
grid_h = np.full(n, np.nan)
for code in ("GRID_CTR", "GRID_ATZ"):
    for g, v in zip(layers[code].geom, layers[code].vertical_limit):
        if g.intersects(line):
            inside = shapely.contains_xy(g, plon, plat); grid_h[inside] = np.fmin(grid_h[inside], hmax(v))
ax.plot(d / 1000, terr + grid_h, "k", lw=2, zorder=4, label="terén + povolená výška ze sítě")
ax.plot(d / 1000, terr + FLIGHT_AGL, "b--", zorder=4, label=f"let {FLIGHT_AGL} m nad terénem")
ax.set_ylim(0, 1300); ax.set_xlim(0, d[-1] / 1000)
ax.set_xlabel("vzdálenost od začátku profilu (km)"); ax.set_ylabel("nadmořská výška (m)")
ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1)); fig.subplots_adjust(right=0.72); ax.set_title("svislý řez zónami: dolní a horní hranice převedené na nadmořskou výšku (FL bráno jako ve standardní atmosféře)")
plt.show()
ok = np.nan_to_num(grid_h, nan=120) >= FLIGHT_AGL
print(f"let ve {FLIGHT_AGL} m nad terénem je podle sítí možný na {100 * ok.mean():.0f} % délky profilu; terén {terr.min():.0f}–{terr.max():.0f} m n. m.")
''', '''
A = (49.2467, 16.4798)        # ◀ parameter: start of the profile (Bystrc, Kozí horka)
B = (49.1510, 16.6940)        # ◀ parameter: end of the profile (Brno-Tuřany airport)
FLIGHT_AGL = 120              # ◀ parameter: planned flight height above ground (m)
T_JTSK = Transformer.from_crs(4326, 5514, always_xy=True)
(xa, xb), (ya, yb) = T_JTSK.transform([A[1], B[1]], [A[0], B[0]])
dem, tr = cuzk_raster("dmr5g", min(xa, xb) - 100, min(ya, yb) - 100, max(xa, xb) + 100, max(ya, yb) + 100, res=10.0)
n = int(np.hypot(xb - xa, yb - ya) // 25) + 1
d = np.linspace(0, np.hypot(xb - xa, yb - ya), n); xs = xa + (xb - xa) * d / d[-1]; ys = ya + (yb - ya) * d / d[-1]
col, row = ~tr * (xs, ys)
terr = dem[np.clip(row.astype(int), 0, dem.shape[0] - 1), np.clip(col.astype(int), 0, dem.shape[1] - 1)]
plon = np.linspace(A[1], B[1], n); plat = np.linspace(A[0], B[0], n)       # over 15 km a linear interpolation in geographic coordinates is enough
def amsl(txt, ground):
    s = txt.strip().upper().replace(" ", "")
    if s in ("GND", "SFC"): return ground
    if s.startswith("FL"): return np.full_like(ground, float(s[2:]) * 100 * 0.3048)
    m = re.match(r"([\\d.]+)(FT|M)(AGL|AMSL|MSL)", s)
    v = float(m.group(1)) * (0.3048 if m.group(2) == "FT" else 1)
    return ground + v if m.group(3) == "AGL" else np.full_like(ground, v)
line = LineString(zip(plon, plat))
fig, ax = plt.subplots(figsize=(15, 6))
ax.fill_between(d / 1000, 0, terr, color="0.55", zorder=3)
k = 0
for code, df in layers.items():
    if code.startswith("GRID"): continue
    for g, ident, vl in zip(df.geom, df.ident, df.vertical_limit):
        if not g.intersects(line): continue
        inside = shapely.contains_xy(g, plon, plat)
        lo, hi = vl.split("-", 1)
        ax.fill_between(d / 1000, amsl(lo, terr), amsl(hi, terr), where=inside, alpha=0.25, color=f"C{k % 10}", label=f"{code} {ident}: {vl}"); k += 1
grid_h = np.full(n, np.nan)
for code in ("GRID_CTR", "GRID_ATZ"):
    for g, v in zip(layers[code].geom, layers[code].vertical_limit):
        if g.intersects(line):
            inside = shapely.contains_xy(g, plon, plat); grid_h[inside] = np.fmin(grid_h[inside], hmax(v))
ax.plot(d / 1000, terr + grid_h, "k", lw=2, zorder=4, label="terrain + allowed height from the grid")
ax.plot(d / 1000, terr + FLIGHT_AGL, "b--", zorder=4, label=f"flight {FLIGHT_AGL} m above ground")
ax.set_ylim(0, 1300); ax.set_xlim(0, d[-1] / 1000)
ax.set_xlabel("distance from the start of the profile (km)"); ax.set_ylabel("altitude (m a.s.l.)")
ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1)); fig.subplots_adjust(right=0.72); ax.set_title("vertical cross-section of the zones: lower and upper limits converted to altitude (FL taken as in the standard atmosphere)")
plt.show()
ok = np.nan_to_num(grid_h, nan=120) >= FLIGHT_AGL
print(f"a flight at {FLIGHT_AGL} m above ground is possible according to the grids along {100 * ok.mean():.0f} % of the profile; terrain {terr.min():.0f}–{terr.max():.0f} m a.s.l.")
''')),
        ("task", t(
            "Na kolika procentech délky profilu smíš podle sítí letět ve 120 m nad terénem a kde povolená výška klesá k nule? Které zóny profil protíná od země a které začínají vysoko nad dronem? Nastav FLIGHT_AGL na 50 m: jak se výsledek změní? Proč pro let dronu nestačí znát jen zóny, do kterých padá místo startu?",
            "Along what percentage of the profile may you fly at 120 m above ground according to the grids, and where does the allowed height drop to zero? Which zones does the profile cross from the ground and which start high above the drone? Set FLIGHT_AGL to 50 m: how does the result change? Why is it not enough for a drone flight to know only the zones the take-off site falls into?")),
        ("task", t(
            "+ Nastav BBOX, A, B a STATION na okolí letiště Václava Havla (STATION = \"LKPR\", konec profilu 50,10° s. š., 14,26° v. d.) a porovnej mapu povolené výšky a svislý řez s Brnem.",
            "+ Set BBOX, A, B and STATION to the area around Václav Havel Airport (STATION = \"LKPR\", end of the profile 50.10° N, 14.26° E) and compare the map of allowed height and the cross-section with Brno.")),
    ]
