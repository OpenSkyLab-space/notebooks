from _common import CUZK_HELPER, OPEN_METEO_HELPER

META = {
    "version": "1.0",
    "minutes": 50,
    "title": {"cs": "Plán letu nad údolím Vltavy: GSD, překryvy, terén a vítr", "en": "A flight plan over the Vltava valley: GSD, overlaps, terrain and wind"},
    "visual": {"cs": "Plánovač letu dronu", "en": "Drone flight planner"},
    "lead": {
        "cs": "Ve vizuálu jsi plánoval let nad rovinou a nad modelovým kopcem. Tady stejné vzorce použiješ na skutečný terén: svah údolí Vltavy u Roztok z digitálního modelu reliéfu ČÚZK DMR 5G (lidar, buňka 2 m) a na aktuální předpověď větru ve výšce letu.",
        "en": "In the visual you planned a flight over flat ground and over a model hill. Here you apply the same formulas to real terrain: the slope of the Vltava valley at Roztoky from the ČÚZK DMR 5G digital terrain model (lidar, 2 m cells), and to the current wind forecast at flight height.",
    },
    "goal": {
        "cs": "spočítat výšku letu pro cílové GSD, rozestup linek, interval a rychlost, rozmazání a zkosení, ukázat, jak terén mění výšku nad zemí a překryv, a naplánovat návrat proti větru.",
        "en": "compute flight height for a target GSD, line spacing, trigger interval and speed, motion blur and skew, show how terrain changes height above ground and overlap, and plan the return against the wind.",
    },
    "data": {
        "cs": "DMR 5G (ČÚZK, služba ImageServer, výšky v Bpv, buňka 2 m) pro území 1,2 × 0,8 km na levém svahu údolí Vltavy u Roztok; hodinová předpověď větru ve 10, 80 a 120 m z Open-Meteo; parametry kamer z technických listů výrobců (stejné jako ve vizuálu).",
        "en": "DMR 5G (ČÚZK, ImageServer, heights in Bpv, 2 m cells) for a 1.2 × 0.8 km area on the left slope of the Vltava valley at Roztoky; hourly wind forecast at 10, 80 and 120 m from Open-Meteo; camera parameters from manufacturers' data sheets (same as in the visual).",
    },
    "sources": {
        "cs": [
            "Digitální model reliéfu České republiky 5. generace (DMR 5G), © ČÚZK, licence CC BY 4.0, služba https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer",
            "Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "Parametry kamer: technické listy DJI Zenmuse P1, Mavic 3 Enterprise (3E, 3M) a obecná kamera 1″ 20 Mpx; baterie Mavic 3 Enterprise 5000 mAh, 15,4 V (77 Wh).",
            "Výška letu v otevřené kategorii max. 120 m od nejbližšího bodu zemského povrchu: prováděcí nařízení Komise (EU) 2019/947, příloha, UAS.OPEN.010.",
        ],
        "en": [
            "Digital terrain model of the Czech Republic, 5th generation (DMR 5G), © ČÚZK, licence CC BY 4.0, service https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer",
            "Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "Camera parameters: data sheets of DJI Zenmuse P1, Mavic 3 Enterprise (3E, 3M) and a generic 1″ 20 MP camera; Mavic 3 Enterprise battery 5000 mAh, 15.4 V (77 Wh).",
            "Flight height in the open category max. 120 m from the closest point of the surface of the earth: Commission Implementing Regulation (EU) 2019/947, Annex, UAS.OPEN.010.",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava", "## 1. Setup")),
        ("code", "%pip install -q rasterio"),
        ("code", '''
import time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import rasterio
from pyproj import Transformer
''' + t(CUZK_HELPER["cs"] + OPEN_METEO_HELPER["cs"], CUZK_HELPER["en"] + OPEN_METEO_HELPER["en"]) + t('''
# kamery: šířka a výška čipu (mm), počet pixelů, ohnisková vzdálenost (mm), nejkratší interval mezi snímky (s)
CAMERAS = {
    "P1 35 mm":        dict(sw=35.9, sh=24.0, pw=8192, ph=5460, f=35.0, tmin=0.7),
    "Mavic 3E":        dict(sw=17.3, sh=13.0, pw=5280, ph=3956, f=12.3, tmin=0.7),
    "Mavic 3M (MS)":   dict(sw=5.2,  sh=3.9,  pw=2592, ph=1944, f=4.34, tmin=2.0),
    "RGB 1″ 20 Mpx":   dict(sw=13.2, sh=8.8,  pw=5472, ph=3648, f=8.8,  tmin=2.0),
}
''', '''
# cameras: sensor width and height (mm), pixel count, focal length (mm), shortest interval between shots (s)
CAMERAS = {
    "P1 35 mm":        dict(sw=35.9, sh=24.0, pw=8192, ph=5460, f=35.0, tmin=0.7),
    "Mavic 3E":        dict(sw=17.3, sh=13.0, pw=5280, ph=3956, f=12.3, tmin=0.7),
    "Mavic 3M (MS)":   dict(sw=5.2,  sh=3.9,  pw=2592, ph=1944, f=4.34, tmin=2.0),
    "RGB 1″ 20 Mpx":   dict(sw=13.2, sh=8.8,  pw=5472, ph=3648, f=8.8,  tmin=2.0),
}
''')),
        ("md", t(
            "## 2. Kamera, výška a GSD\n\nGSD = H · p / f, kde p je velikost pixelu na čipu (šířka čipu / počet pixelů). Z cílového GSD tedy H = GSD · f / p.",
            "## 2. Camera, height and GSD\n\nGSD = H · p / f, where p is the pixel pitch on the sensor (sensor width / pixel count). From a target GSD, H = GSD · f / p.")),
        ("code", t('''
gsd_target = 1.5          # ◀ parametr: cílové GSD v cm/px
rows = []
for name, c in CAMERAS.items():
    p = c["sw"] / c["pw"]                       # mm
    H = gsd_target / 100 * c["f"] / p          # m
    rows.append({"kamera": name, "pixel na čipu (µm)": p * 1000, "výška letu (m)": H,
                 "záběr napříč (m)": c["pw"] * gsd_target / 100, "záběr podél (m)": c["ph"] * gsd_target / 100})
cam_tab = pd.DataFrame(rows).set_index("kamera")
cam_tab.round(1)
''', '''
gsd_target = 1.5          # ◀ parameter: target GSD in cm/px
rows = []
for name, c in CAMERAS.items():
    p = c["sw"] / c["pw"]                       # mm
    H = gsd_target / 100 * c["f"] / p          # m
    rows.append({"camera": name, "pixel pitch (µm)": p * 1000, "flight height (m)": H,
                 "footprint across (m)": c["pw"] * gsd_target / 100, "footprint along (m)": c["ph"] * gsd_target / 100})
cam_tab = pd.DataFrame(rows).set_index("camera")
cam_tab.round(1)
''')),
        ("task", t(
            "Proč musí Mavic 3M pro stejné GSD letět mnohem níž než P1? Nastav `gsd_target` na 2 a pak na 4 cm/px. Pro které kamery a GSD by výška překročila 120 m, a tedy limit otevřené kategorie? Jaké má nízký let důsledky (počet snímků, čas, bezpečnost)?",
            "Why does the Mavic 3M have to fly much lower than the P1 for the same GSD? Set `gsd_target` to 2 and then 4 cm/px. For which cameras and GSDs would the height exceed 120 m, the open-category limit? What are the consequences of flying low (number of images, time, safety)?")),
        ("md", t(
            "## 3. Skutečný terén a plán linek\n\nNačteme DMR 5G pro svah údolí Vltavy. Linky vedou ve směru východ–západ, tedy po spádnici dolů do údolí a zpět. Místo vzletu je na planině na západním okraji.",
            "## 3. Real terrain and the line plan\n\nWe load DMR 5G for the slope of the Vltava valley. Lines run east–west, i.e. down the fall line into the valley and back. The take-off point is on the plateau at the western edge.")),
        ("code", t('''
cx, cy = Transformer.from_crs(4326, 5514, always_xy=True).transform(14.392, 50.152)
W, Hh = 1200, 800                                  # území: šířka (V–Z) a výška (S–J) v m
dem, tr = cuzk_raster("dmr5g", cx - W / 2, cy - Hh / 2, cx + W / 2, cy + Hh / 2, res=2)
z_takeoff = float(np.median(dem[:, :10]))            # planina na západním okraji
print(f"terén {dem.min():.1f}–{dem.max():.1f} m n. m. (Bpv), místo vzletu {z_takeoff:.1f} m n. m.")
fig, ax = plt.subplots(figsize=(8, 5))
im = ax.imshow(dem, cmap="terrain", extent=(0, W, 0, Hh)); fig.colorbar(im, label="nadmořská výška (m, Bpv)")
ax.contour(np.flipud(dem), levels=np.arange(180, 300, 10), colors="k", linewidths=0.4, extent=(0, W, 0, Hh))
ax.set(xlabel="m (západ → východ)", ylabel="m", title="DMR 5G, levý svah údolí Vltavy u Roztok"); plt.show()
''', '''
cx, cy = Transformer.from_crs(4326, 5514, always_xy=True).transform(14.392, 50.152)
W, Hh = 1200, 800                                  # area: width (E–W) and height (N–S) in m
dem, tr = cuzk_raster("dmr5g", cx - W / 2, cy - Hh / 2, cx + W / 2, cy + Hh / 2, res=2)
z_takeoff = float(np.median(dem[:, :10]))            # plateau at the western edge
print(f"terrain {dem.min():.1f}–{dem.max():.1f} m a.s.l. (Bpv), take-off point {z_takeoff:.1f} m a.s.l.")
fig, ax = plt.subplots(figsize=(8, 5))
im = ax.imshow(dem, cmap="terrain", extent=(0, W, 0, Hh)); fig.colorbar(im, label="elevation (m, Bpv)")
ax.contour(np.flipud(dem), levels=np.arange(180, 300, 10), colors="k", linewidths=0.4, extent=(0, W, 0, Hh))
ax.set(xlabel="m (west → east)", ylabel="m", title="DMR 5G, left slope of the Vltava valley at Roztoky"); plt.show()
''')),
        ("code", t('''
cam = CAMERAS["Mavic 3E"]     # ◀ parametr: kamera
H0 = 80                       # ◀ parametr: výška letu nad místem vzletu (m)
fo, so = 0.80, 0.70           # ◀ parametr: podélný a příčný překryv
v_air = 10.0                  # ◀ parametr: rychlost vůči vzduchu (m/s)
long_across = True            # ◀ parametr: delší strana snímku napříč letem?

p = cam["sw"] / cam["pw"] / 1000                                   # m
n_across, n_along = (cam["pw"], cam["ph"]) if long_across else (cam["ph"], cam["pw"])
gsd0 = H0 * p / (cam["f"] / 1000)                                  # GSD nad místem vzletu
base = (1 - fo) * n_along * gsd0                                   # vzdálenost mezi snímky
spacing = (1 - so) * n_across * gsd0                               # rozestup linek
n_lines = int(np.ceil(Hh / spacing)) + 1
interval = base / v_air
photos = n_lines * (int(W / base) + 1)
t_flight = (n_lines * W + (n_lines - 1) * spacing) / v_air
print(f"GSD nad místem vzletu {gsd0 * 100:.2f} cm/px, báze {base:.1f} m, rozestup linek {spacing:.1f} m")
print(f"linek {n_lines}, snímků {photos}, interval {interval:.2f} s (kamera zvládne {cam['tmin']} s), čas letu {t_flight / 60:.1f} min bez otoček")
if interval < cam["tmin"]:
    print(f"POZOR: kamera nestihne; nejvyšší rychlost je {base / cam['tmin']:.1f} m/s")
''', '''
cam = CAMERAS["Mavic 3E"]     # ◀ parameter: camera
H0 = 80                       # ◀ parameter: flight height above the take-off point (m)
fo, so = 0.80, 0.70           # ◀ parameter: forward and side overlap
v_air = 10.0                  # ◀ parameter: airspeed (m/s)
long_across = True            # ◀ parameter: long side of the image across the flight direction?

p = cam["sw"] / cam["pw"] / 1000                                   # m
n_across, n_along = (cam["pw"], cam["ph"]) if long_across else (cam["ph"], cam["pw"])
gsd0 = H0 * p / (cam["f"] / 1000)                                  # GSD above the take-off point
base = (1 - fo) * n_along * gsd0                                   # distance between shots
spacing = (1 - so) * n_across * gsd0                               # line spacing
n_lines = int(np.ceil(Hh / spacing)) + 1
interval = base / v_air
photos = n_lines * (int(W / base) + 1)
t_flight = (n_lines * W + (n_lines - 1) * spacing) / v_air
print(f"GSD above take-off {gsd0 * 100:.2f} cm/px, base {base:.1f} m, line spacing {spacing:.1f} m")
print(f"lines {n_lines}, images {photos}, interval {interval:.2f} s (camera can do {cam['tmin']} s), flight time {t_flight / 60:.1f} min without turns")
if interval < cam["tmin"]:
    print(f"WARNING: the camera cannot keep up; the highest speed is {base / cam['tmin']:.1f} m/s")
''')),
        ("task", t(
            "Zvyšuj `v_air`, dokud se neobjeví upozornění, že kamera nestihne. Jaká je nejvyšší rychlost? Přepni `long_across = False`: jak se změní báze, nejvyšší rychlost, počet linek a čas letu? Proč otočený snímek dovolí rychlejší let, a přesto může let trvat déle? Nastav podélný překryv 0,85 jako pro vegetaci.",
            "Increase `v_air` until the warning that the camera cannot keep up appears. What is the highest speed? Switch `long_across = False`: how do base, maximum speed, number of lines and flight time change? Why does a rotated image allow faster flight and yet the flight may take longer? Set the forward overlap to 0.85 as for vegetation.")),
        ("md", t(
            "## 4. Stálá výška, nebo sledování terénu?\n\nPři stálé výšce nad místem vzletu se výška nad zemí mění s terénem: H_AGL = H0 + z_vzlet − z. S ní se mění GSD i záběr, ale báze a rozestup linek zůstávají, takže se mění skutečný překryv.",
            "## 4. Constant height or terrain following?\n\nAt a constant height above the take-off point, the height above ground changes with terrain: H_AGL = H0 + z_takeoff − z. GSD and footprint change with it, while base and line spacing stay fixed, so the actual overlap changes.")),
        ("code", t('''
follow = False                # ◀ parametr: True = sledování terénu (stálá výška nad zemí H0)
agl = np.full_like(dem, H0) if follow else H0 + z_takeoff - dem
gsd = agl * p / (cam["f"] / 1000)
fo_local = 1 - base / (n_along * gsd)
so_local = 1 - spacing / (n_across * gsd)
print(f"výška nad zemí {agl.min():.0f}–{agl.max():.0f} m, GSD {gsd.min() * 100:.2f}–{gsd.max() * 100:.2f} cm/px")
print(f"podélný překryv {fo_local.min():.0%}–{fo_local.max():.0%}, příčný {so_local.min():.0%}–{so_local.max():.0%}")
print(f"plocha nad 120 m nad terénem: {np.mean(agl > 120):.0%} území")
fig, ax = plt.subplots(1, 3, figsize=(15, 3.8))
for a, (arr, lbl, cm) in zip(ax, [(agl, "výška nad zemí (m)", "viridis"), (gsd * 100, "GSD (cm/px)", "magma"), (so_local * 100, "příčný překryv (%)", "RdYlGn")]):
    im = a.imshow(arr, cmap=cm, extent=(0, W, 0, Hh)); fig.colorbar(im, ax=a, label=lbl); a.set_xticks([]); a.set_yticks([])
ax[0].set_title("sledování terénu" if follow else f"stálá výška {H0} m nad místem vzletu"); plt.show()
''', '''
follow = False                # ◀ parameter: True = terrain following (constant height H0 above ground)
agl = np.full_like(dem, H0) if follow else H0 + z_takeoff - dem
gsd = agl * p / (cam["f"] / 1000)
fo_local = 1 - base / (n_along * gsd)
so_local = 1 - spacing / (n_across * gsd)
print(f"height above ground {agl.min():.0f}–{agl.max():.0f} m, GSD {gsd.min() * 100:.2f}–{gsd.max() * 100:.2f} cm/px")
print(f"forward overlap {fo_local.min():.0%}–{fo_local.max():.0%}, side overlap {so_local.min():.0%}–{so_local.max():.0%}")
print(f"area more than 120 m above terrain: {np.mean(agl > 120):.0%} of the area")
fig, ax = plt.subplots(1, 3, figsize=(15, 3.8))
for a, (arr, lbl, cm) in zip(ax, [(agl, "height above ground (m)", "viridis"), (gsd * 100, "GSD (cm/px)", "magma"), (so_local * 100, "side overlap (%)", "RdYlGn")]):
    im = a.imshow(arr, cmap=cm, extent=(0, W, 0, Hh)); fig.colorbar(im, ax=a, label=lbl); a.set_xticks([]); a.set_yticks([])
ax[0].set_title("terrain following" if follow else f"constant {H0} m above take-off"); plt.show()
''')),
        ("task", t(
            "Při stálé výšce 80 m nad planinou: jaký je rozsah GSD a překryvů? Kde je překryv nejmenší, na planině, nebo v údolí, a proč? Kolik území je výš než 120 m nad terénem? Přepni `follow = True`: co se zlepší a co k sledování terénu potřebuješ (model terénu, jeho přesnost, překážky)?",
            "At a constant 80 m above the plateau: what is the range of GSD and overlaps? Where is the overlap smallest, on the plateau or in the valley, and why? How much of the area is more than 120 m above the terrain? Switch to `follow = True`: what improves and what do you need for terrain following (terrain model, its accuracy, obstacles)?")),
        ("md", t(
            "## 5. Skutečný vítr, rozmazání a postupná závěrka\n\nZ Open-Meteo vezmeme předpověď větru pro Roztoky na dnešek. Rozmazání = rychlost vůči zemi · expozice / GSD; zkosení postupnou závěrkou = rychlost vůči zemi · doba vyčtení čipu / GSD.",
            "## 5. Real wind, motion blur and rolling shutter\n\nWe take today's wind forecast for Roztoky from Open-Meteo. Blur = ground speed · exposure / GSD; rolling-shutter skew = ground speed · sensor readout time / GSD.")),
        ("code", t('''
w = open_meteo({"latitude": 50.152, "longitude": 14.392, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "Europe/Prague",
                "hourly": "wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_direction_80m,wind_gusts_10m"})
met = pd.DataFrame(w["hourly"]).set_index("time")
print(met.iloc[6:20].to_string())
''', '''
w = open_meteo({"latitude": 50.152, "longitude": 14.392, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "Europe/Prague",
                "hourly": "wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_direction_80m,wind_gusts_10m"})
met = pd.DataFrame(w["hourly"]).set_index("time")
print(met.iloc[6:20].to_string())
''')),
        ("code", t('''
hour = int(met.wind_speed_80m.values[:24].argmax())   # ◀ parametr: hodina letu (místní čas); výchozí je největrnější hodina dne
t_exp = 1 / 1000               # ◀ parametr: expoziční čas (s)
t_read = 0.030                 # ◀ parametr: doba vyčtení čipu u postupné závěrky (s); 0 = globální závěrka
wind = met.wind_speed_80m.iloc[hour]
wdir = met.wind_direction_80m.iloc[hour]
# linky vedou V–Z; složka větru podél linek a napříč nimi
along = wind * np.cos(np.radians(wdir - 90)); cross = wind * np.sin(np.radians(wdir - 90))
for leg, sign in [("linka na východ", -1), ("linka na západ", +1)]:
    gs = np.sqrt(max(v_air**2 - cross**2, 0)) + sign * along      # rychlost vůči zemi (vítr odkud → znaménko)
    print(f"{leg}: vůči zemi {gs:4.1f} m/s, rozmazání {gs * t_exp / gsd0:.2f} px, zkosení {gs * t_read / gsd0:.1f} px")
print(f"{met.index[hour]}: vítr v 80 m: {wind:.1f} m/s od {wdir:.0f}°; složka k východu {-along:+.1f} m/s, k severu {cross:+.1f} m/s")
''', '''
hour = int(met.wind_speed_80m.values[:24].argmax())   # ◀ parameter: hour of the flight (local time); default is the windiest hour of the day
t_exp = 1 / 1000               # ◀ parameter: exposure time (s)
t_read = 0.030                 # ◀ parameter: sensor readout time of a rolling shutter (s); 0 = global shutter
wind = met.wind_speed_80m.iloc[hour]
wdir = met.wind_direction_80m.iloc[hour]
# lines run E–W; wind component along and across the lines
along = wind * np.cos(np.radians(wdir - 90)); cross = wind * np.sin(np.radians(wdir - 90))
for leg, sign in [("eastbound line", -1), ("westbound line", +1)]:
    gs = np.sqrt(max(v_air**2 - cross**2, 0)) + sign * along      # ground speed (wind is "from" → sign)
    print(f"{leg}: ground speed {gs:4.1f} m/s, blur {gs * t_exp / gsd0:.2f} px, skew {gs * t_read / gsd0:.1f} px")
print(f"{met.index[hour]}: wind at 80 m: {wind:.1f} m/s from {wdir:.0f}°; eastward component {-along:+.1f} m/s, northward {cross:+.1f} m/s")
''')),
        ("task", t(
            "Jaký vítr hlásí předpověď ve 10, 80 a 120 m a proč se liší? Jak se liší rozmazání a zkosení na lince po větru a proti větru? Proč zkosení nezmenší kratší expozice? Kdy bys linky raději otočil podél větru, nebo napříč?",
            "What wind does the forecast give at 10, 80 and 120 m and why do they differ? How do blur and skew differ on the downwind and upwind legs? Why does a shorter exposure not reduce the skew? When would you rather orient the lines along or across the wind?")),
        ("md", t(
            "## 6. Baterie a návrat domů\n\nMavic 3E má baterii 77 Wh a výrobce udává až 45 min letu bez větru, tedy průměrně asi 100 W. Spočítáme, kolik energie potřebuje návrat z nejvzdálenějšího bodu, když vítr fouká od místa vzletu.",
            "## 6. Battery and return to home\n\nThe Mavic 3E has a 77 Wh battery and the maker states up to 45 min of flight without wind, i.e. about 100 W on average. We compute how much energy a return from the farthest point needs when the wind blows away from the take-off point.")),
        ("code", t('''
E_bat = 77.0                  # ◀ parametr: energie baterie (Wh)
P = 77.0 / (45 / 60)          # průměrný výkon (W) z udávané výdrže
temp_factor = 1.0             # ◀ parametr: využitelná kapacita (1,0 při 20 °C; v mrazu zhruba 0,7–0,8)
reserve = 0.20                # ◀ parametr: rezerva při přistání
headwind = wind               # nejhorší případ: celý vítr proti návratu
d_home = np.hypot(W, Hh)      # nejvzdálenější roh území (m)
gs_home = v_air - headwind
E_mission = P * t_flight / 3600
E_return = P * d_home / max(gs_home, 0.1) / 3600
E_use = E_bat * temp_factor * (1 - reserve)
print(f"mise {E_mission:.1f} Wh + návrat {E_return:.1f} Wh (proti větru {headwind:.1f} m/s, vůči zemi {gs_home:.1f} m/s) = {E_mission + E_return:.1f} Wh")
print(f"využitelná energie {E_use:.1f} Wh → {'stačí' if E_mission + E_return <= E_use else 'NESTAČÍ, rozděl misi'}")
''', '''
E_bat = 77.0                  # ◀ parameter: battery energy (Wh)
P = 77.0 / (45 / 60)          # average power (W) from the stated endurance
temp_factor = 1.0             # ◀ parameter: usable capacity (1.0 at 20 °C; roughly 0.7–0.8 in frost)
reserve = 0.20                # ◀ parameter: landing reserve
headwind = wind               # worst case: all of the wind against the return
d_home = np.hypot(W, Hh)      # farthest corner of the area (m)
gs_home = v_air - headwind
E_mission = P * t_flight / 3600
E_return = P * d_home / max(gs_home, 0.1) / 3600
E_use = E_bat * temp_factor * (1 - reserve)
print(f"mission {E_mission:.1f} Wh + return {E_return:.1f} Wh (headwind {headwind:.1f} m/s, ground speed {gs_home:.1f} m/s) = {E_mission + E_return:.1f} Wh")
print(f"usable energy {E_use:.1f} Wh → {'enough' if E_mission + E_return <= E_use else 'NOT ENOUGH, split the mission'}")
''')),
        ("task", t(
            "Stačí jedna baterie? Nastav `temp_factor = 0.75` a pak zvyš vítr (`headwind = 8`). Proč je „tam po větru, zpátky proti větru“ past? Zkus také vyšší `v_air`: proč při silném větru pomáhá letět rychleji, i když výkon roste?",
            "Is one battery enough? Set `temp_factor = 0.75` and then increase the wind (`headwind = 8`). Why is \"downwind out, upwind back\" a trap? Also try a higher `v_air`: why does flying faster help in strong wind even though power increases?")),
    ]
