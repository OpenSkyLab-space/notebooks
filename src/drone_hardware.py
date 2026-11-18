"""Notebook drone_hardware k laboratoři Dron jako měřicí přístroj (edu_viz_drone_hardware).
Data: odvozená tabulka letu Bahna 31. 10. 2025 (místní souřadnice, bez lat/lon a data), viz data/drone_hardware/README.md."""
from _drone_common import bi

META = {
    "version": "1.0",
    "minutes": 45,
    "title": {"cs": "Dron jako měřicí přístroj: časování, poloha a úhly na skutečném letu",
              "en": "The drone as a measuring instrument: timing, position and angles on a real flight"},
    "visual": {"cs": "Dron jako měřicí přístroj", "en": "The drone as a measuring instrument"},
    "lead": {
        "cs": "Laboratoř ukazuje, že dron je soustava přístrojů: přijímač GNSS, barometr, inerciální jednotka, gimbal a kamera, které měří každý trochu jinde a v trochu jiném okamžiku. Tady to ověříš na skutečném mapovacím letu nad Bahnami (DJI Mavic 2 Pro, bez RTK). Ke každému snímku máš polohu a výšky zapsané dronem, natočení těla a kamery a střed kamery spočtený z fotogrammetrie (SfM). Z jejich rozdílů zjistíš, jak rychle dron letěl, jak se naklání, o kolik se zpožďuje zápis polohy a jak moc se obraz rozmaže.",
        "en": "The lab shows that a drone is a set of instruments: a GNSS receiver, a barometer, an inertial unit, a gimbal and a camera, each measuring in a slightly different place and at a slightly different moment. Here you test this on a real mapping flight over Bahna (DJI Mavic 2 Pro, no RTK). For each image you have the position and heights recorded by the drone, the body and camera orientation and the camera centre computed by photogrammetry (SfM). From their differences you find how fast the drone flew, how it tilts, how much the position record lags and how much the image is blurred.",
    },
    "goal": {
        "cs": "z poloh a časů snímků určit řady, rychlost a rozestup snímků a najít chybějící snímky, porovnat náklon těla a kamery v řadách tam a zpět, oddělit zpoždění zápisu polohy od ramene páky antény, spočítat rozmazání pohybem a porovnat výšku z GNSS a z barometru.",
        "en": "determine the strips, speed and image spacing from image positions and times and find missing images, compare the body and camera tilt in strips flown in both directions, separate the position-record delay from the antenna lever arm, compute motion blur and compare the GNSS and barometric heights.",
    },
    "data": {
        "cs": "tabulka metadat 253 snímků letu nad Bahnami 31. 10. 2025 (EXIF a XMP od DJI) se středy kamer ze SfM, v místních souřadnicích (OpenSkyLab, CC BY 4.0).",
        "en": "a metadata table of 253 images of a flight over Bahna on 31 Oct 2025 (EXIF and DJI XMP) with SfM camera centres, in local coordinates (OpenSkyLab, CC BY 4.0).",
    },
    "sources": {
        "cs": [
            "Data letu: OpenSkyLab (2026), metadata letu Bahna 31. 10. 2025 odvozená ze snímků a z rekonstrukce SfM, licence CC BY 4.0, https://github.com/OpenSkyLab-space/notebooks/tree/main/data",
            "Pix4D: *How to correct for the rolling shutter effect* a *Time offset between GNSS and camera* (dokumentace Pix4Dmapper).",
            "Vautherin, J., Rutishauser, S., Schneider-Zapp, K., Choi, H. F., Chovancova, V., Glass, A., Strecha, C. (2016). Photogrammetric accuracy and modeling of rolling shutter cameras. *ISPRS Annals* III-3, 139–146.",
            "Groves, P. D. (2013). *Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems*, 2. vyd. Artech House (rameno páky, synchronizace senzorů).",
        ],
        "en": [
            "Flight data: OpenSkyLab (2026), metadata of the Bahna flight of 31 Oct 2025 derived from the images and the SfM reconstruction, licence CC BY 4.0, https://github.com/OpenSkyLab-space/notebooks/tree/main/data",
            "Pix4D: *How to correct for the rolling shutter effect* and *Time offset between GNSS and camera* (Pix4Dmapper documentation).",
            "Vautherin, J., Rutishauser, S., Schneider-Zapp, K., Choi, H. F., Chovancova, V., Glass, A., Strecha, C. (2016). Photogrammetric accuracy and modeling of rolling shutter cameras. *ISPRS Annals* III-3, 139–146.",
            "Groves, P. D. (2013). *Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems*, 2nd ed. Artech House (lever arm, sensor synchronisation).",
        ],
    },
}

LOAD = bi(r'''
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/OpenSkyLab-space/notebooks/main/data/drone_hardware_bahna_flight.csv"
d = pd.read_csv(URL)
g = d[d.set == "grid"].sort_values("t_s").reset_index(drop=True)      # {{mapovací let v řadách||the mapping flight in strips}}
# {{nová řada začíná, když se poloha na sever skokem změní o víc než 5 m (rozestup řad je asi 25 m)||a new strip starts when the north position jumps by more than 5 m (strips are about 25 m apart)}}
g["strip"] = (g.n_gnss.diff().abs() > 5).cumsum()
first, last = g.groupby("strip").e_gnss.first(), g.groupby("strip").e_gnss.last()
g["dir"] = g.strip.map(np.sign(last - first)).astype(int)              # {{+1 = na východ, −1 = na západ||+1 = eastwards, −1 = westwards}}
print(f"{{snímků||images}}: {len(d)} ({{mapovací let||mapping flight}} {len(g)}, {{doplňkové||extra}} {(d.set == 'extra').sum()}), {{řad||strips}}: {g.strip.nunique()}")
print(f"{{mapovací let trval||the mapping flight took}} {g.t_s.max() / 60:.1f} min, {{výška nad vzletem||height above take-off}} {g.h_baro.median():.1f} m")
fig, ax = plt.subplots(figsize=(8, 5))
for s, q in g.groupby("strip"):
    ax.plot(q.e_gnss, q.n_gnss, ".-", ms=4, lw=.6, c="tab:red" if q.dir.iloc[0] > 0 else "tab:blue")
ax.plot([], [], "r.-", label="{{na východ||eastwards}}"); ax.plot([], [], "b.-", label="{{na západ||westwards}}")
ax.set_aspect("equal"); ax.set_xlabel("E (m)"); ax.set_ylabel("N (m)"); ax.legend(); ax.set_title("{{Trasa letu podle GNSS dronu||Flight track from the drone GNSS}}")
plt.show()
''')

SPEED = bi(r'''
rows = []
for s, q in g.groupby("strip"):
    v = abs(np.polyfit(q.t_s, q.e_gnss, 1)[0])                           # {{rychlost = sklon přímky E(t)||speed = slope of the line E(t)}}
    rows.append({"{{řada||strip}}": s, "{{směr||direction}}": "E" if q.dir.iloc[0] > 0 else "W", "{{snímků||images}}": len(q),
                 "v (m/s)": round(v, 2), "{{interval (s)||interval (s)}}": q.t_s.diff().median(),
                 "{{rozestup (m)||spacing (m)}}": round(np.hypot(q.e_gnss.diff(), q.n_gnss.diff()).median(), 1)})
st = pd.DataFrame(rows)
display(st)
V_DATA = st["v (m/s)"].median()
print(f"{{medián rychlosti||median speed}} {V_DATA:.2f} m/s")
num = g.image.str.extract(r"_(\d{4})", expand=False).astype(int)
missing = sorted(set(range(num.min(), num.max() + 1)) - set(num))
print(f"{{chybějící čísla snímků||missing image numbers}}: {missing}")
step = np.hypot(g.e_gnss.diff(), g.n_gnss.diff())
same = g.strip.diff() == 0
big = g[same & (step > 1.5 * step[same].median())]
print("{{v řadě je rozestup větší než 1,5 × medián před snímky||within a strip the spacing exceeds 1.5 × median before images}}:", list(big.image))
''')

ATT = bi(r'''
att = g.groupby("dir")[["flight_pitch", "flight_roll", "flight_yaw", "gimbal_pitch", "gimbal_yaw"]].agg(["mean", "std"]).round(1)
att.index = att.index.map({1: "{{na východ||eastwards}}", -1: "{{na západ||westwards}}"})
display(att)
fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
ax[0].plot(g.t_s, g.flight_pitch, ".", ms=3, label="{{náklon těla (flight_pitch)||body pitch (flight_pitch)}}")
ax[0].plot(g.t_s, g.gimbal_pitch + 90, ".", ms=3, label="{{náklon kamery + 90° (gimbal_pitch + 90)||camera pitch + 90° (gimbal_pitch + 90)}}")
ax[0].axhline(0, c="k", lw=.5); ax[0].set_ylabel("°"); ax[0].legend(fontsize=8)
ax[1].plot(g.t_s, g.flight_yaw, ".", ms=3, label="{{kurz těla (flight_yaw)||body heading (flight_yaw)}}")
ax[1].plot(g.t_s, g.e_gnss.diff().apply(np.sign) * 45 + 90, "-", lw=.5, c="gray", label="{{směr letu (nahoře E, dole W)||flight direction (up E, down W)}}")
ax[1].set_ylabel("°"); ax[1].set_xlabel("{{čas od prvního snímku (s)||time since the first image (s)}}"); ax[1].legend(fontsize=8)
plt.show()
''')

TIMING = bi(r'''
SPEED = z_viz("speed", 8.0)        # ◀ {{parametr: rychlost letu v laboratoři (m/s)||parameter: flight speed in the lab (m/s)}}
DT = z_viz("dt", 0.24)             # ◀ {{parametr: zpoždění zápisu polohy v laboratoři (s)||parameter: position-record delay in the lab (s)}}
LEVER_X = z_viz("lever_x", 0.0)    # ◀ {{parametr: anténa před kamerou v laboratoři (m)||parameter: antenna ahead of the camera in the lab (m)}}
LEVER_Z = z_viz("lever_z", 0.2)    # ◀ {{parametr: anténa nad kamerou v laboratoři (m)||parameter: antenna above the camera in the lab (m)}}
ok = g.e_sfm.notna()
g["dE"] = g.e_gnss - g.e_sfm                                             # {{GNSS minus střed kamery ze SfM, východ||GNSS minus SfM camera centre, east}}
g["dN"] = g.n_gnss - g.n_sfm
m = g[ok].groupby("dir")[["dE", "dN"]].agg(["mean", "std", "size"]).round(2)
m.index = m.index.map({1: "{{na východ||eastwards}}", -1: "{{na západ||westwards}}"})
display(m)
dE_e, dE_w = g[ok & (g.dir > 0)].dE.mean(), g[ok & (g.dir < 0)].dE.mean()
# {{model: dE = směr · v · dt + stálý posun (rameno páky; nos dronu míří stále na východ)||model: dE = direction · v · dt + constant offset (lever arm; the drone nose always points east)}}
vdt = (dE_e - dE_w) / 2
const = (dE_e + dE_w) / 2
print(f"{{posun ve směru letu||shift in the flight direction}} v·dt = {vdt:.2f} m  →  dt = {vdt / V_DATA:.3f} s {{při||at}} v = {V_DATA:.2f} m/s")
print(f"{{laboratoř||lab}}: v·dt = {SPEED * DT:.2f} m (v = {SPEED} m/s, dt = {DT} s)")
print(f"{{stálý posun na východ||constant offset to the east}}: {const:+.2f} m")
print(f"{{laboratoř: anténa {LEVER_X:.2f} m před kamerou by dala stálý posun||lab: an antenna {LEVER_X:.2f} m ahead of the camera would give a constant offset}} {LEVER_X:+.2f} m {{na východ (nos míří na východ)||to the east (the nose points east)}}")
tilt = LEVER_Z * np.sin(np.radians(g.groupby("dir").flight_pitch.mean().abs().mean()))
print(f"{{posun antény náklonem těla (lever_z · sin|pitch|)||antenna shift from body tilt (lever_z · sin|pitch|)}}: {tilt:.3f} m")
fig, ax = plt.subplots(figsize=(8, 4))
for s_, c, lab in ((1, "tab:red", "{{na východ||eastwards}}"), (-1, "tab:blue", "{{na západ||westwards}}")):
    ax.hist(g[ok & (g.dir == s_)].dE, bins=30, alpha=.6, color=c, label=lab)
ax.axvline(0, c="k", lw=.5); ax.set_xlabel("E_GNSS − E_SfM (m)"); ax.legend(); plt.show()
''')

BLUR = bi(r'''
F_MM, PIX_UM = 10.26, 2.41        # {{ohnisko a velikost pixelu Hasselblad L1D-20c (EXIF snímků: f = 10,26 mm, ekvivalent 28 mm, 5472 px)||focal length and pixel size of the Hasselblad L1D-20c (image EXIF: f = 10.26 mm, 28 mm equivalent, 5472 px)}}
T_EXP = z_viz("t_exp", 0.002)      # ◀ {{parametr: expoziční čas v laboratoři (s)||parameter: exposure time in the lab (s)}}
T_READ = z_viz("t_read", 0.03)     # ◀ {{parametr: doba vyčtení čipu v laboratoři (s), 0 = mechanická závěrka||parameter: sensor readout time in the lab (s), 0 = mechanical shutter}}
g["gsd_cm"] = g.h_baro * PIX_UM * 1e-6 / (F_MM * 1e-3) * 100
g["v"] = g.strip.map(dict(zip(st.iloc[:, 0], st["v (m/s)"])))
g["blur_cm"] = g.v * g.exposure_s * 100
g["blur_px"] = g.blur_cm / g.gsd_cm
tab = g.groupby("exposure_s").agg(n=("image", "size"), gsd_cm=("gsd_cm", "median"), blur_cm=("blur_cm", "median"), blur_px=("blur_px", "median")).round(2)
tab.index = [f"1/{1 / e:.0f} s" for e in tab.index]
display(tab)
print(f"{{laboratoř||lab}}: t_exp = 1/{1 / T_EXP:.0f} s → {{rozmazání||blur}} {SPEED * T_EXP * 100:.1f} cm = {SPEED * T_EXP * 100 / g.gsd_cm.median():.2f} px")
print(f"{{posun během vyčtení čipu (t_read = {T_READ} s)||shift during sensor readout (t_read = {T_READ} s)}}: {V_DATA * T_READ * 100:.0f} cm = {V_DATA * T_READ * 100 / g.gsd_cm.median():.0f} px {{mezi první a poslední řádkou snímku||between the first and last row of the image}}")
''')

HEIGHT = bi(r'''
g["dh"] = g.h_gnss - g.h_baro
print(f"h_gnss − h_baro: {{průměr||mean}} {g.dh.mean():+.2f} m, {{směrodatná odchylka||standard deviation}} {g.dh.std():.2f} m, {{rozsah||range}} {g.dh.min():+.2f} … {g.dh.max():+.2f} m")
k = np.polyfit(g.t_s, g.dh, 1)[0] * 60
print(f"{{trend||trend}} h_gnss − h_baro: {k:+.3f} m/min")
okh = g.h_sfm.notna()
print(f"h_sfm − h_baro: {{směrodatná odchylka||standard deviation}} {(g.h_sfm - g.h_baro)[okh].std():.2f} m;  h_sfm − h_gnss: {(g.h_sfm - g.h_gnss)[okh].std():.2f} m")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(g.t_s, g.h_baro, ".", ms=3, label="h_baro ({{barometr||barometer}})")
ax.plot(g.t_s, g.h_gnss, ".", ms=3, label="h_gnss (GNSS)")
ax.plot(g.t_s[okh], g.h_sfm[okh], ".", ms=3, label="h_sfm (SfM)")
ax.set_xlabel("{{čas od prvního snímku (s)||time since the first image (s)}}"); ax.set_ylabel("{{výška nad vzletem (m)||height above take-off (m)}}"); ax.legend()
plt.show()
''')


def cells(t):
    return [
        ("md", t("## 1. Data a trasa letu", "## 1. Data and flight track")),
        ("md", t("Tabulka má jeden řádek na snímek. Polohy jsou v místní rovině v metrech (východ, sever), výšky nad místem vzletu. Mapovací let (`grid`) rozdělíme na řady podle skoků v poloze na sever a každé řadě určíme směr.",
                 "The table has one row per image. Positions are in a local plane in metres (east, north), heights above the take-off point. We split the mapping flight (`grid`) into strips by jumps in the north position and give each strip a direction.")),
        ("code", t(*LOAD)),
        ("md", t("## 2. Rychlost, rozestup a chybějící snímky", "## 2. Speed, spacing and missing images")),
        ("md", t("Dron snímá v pravidelném intervalu. Rychlost v každé řadě je sklon přímky proložené polohou na východ v závislosti na čase. Čas je v EXIF jen na celé sekundy, proto přímka a ne rozdíly sousedních snímků.",
                 "The drone takes images at a regular interval. The speed in each strip is the slope of a line fitted to the east position against time. EXIF time has whole seconds only, hence a line rather than differences of neighbouring images.")),
        ("code", t(*SPEED)),
        ("task", t("Jaká je rychlost, interval a rozestup snímků? Liší se řady na východ a na západ? Které snímky chybějí a dá se z rozestupů poznat, kde v řadě je díra?",
                   "What are the speed, interval and image spacing? Do eastward and westward strips differ? Which images are missing and can you tell from the spacing where in a strip there is a hole?")),
        ("md", t("## 3. Náklon těla a kamery", "## 3. Body and camera tilt")),
        ("md", t("Multikoptéra letí dopředu tak, že se nakloní: tah rotorů pak má vodorovnou složku. Gimbal má náklon těla vyrovnat, aby kamera mířila kolmo dolů.",
                 "A multicopter flies forward by tilting, so that the rotor thrust gets a horizontal component. The gimbal is meant to cancel the body tilt so that the camera points straight down.")),
        ("code", t(*ATT)),
        ("task", t("Kam míří nos dronu v řadách na východ a na západ? Jaký je náklon těla v obou směrech a proč má opačné znaménko? Udržel gimbal kameru kolmo dolů? Proč náklon na východ a na západ není stejně velký?",
                   "Where does the drone's nose point in eastward and westward strips? What is the body pitch in both directions and why does it have opposite signs? Did the gimbal keep the camera pointing straight down? Why is the tilt not equally large eastwards and westwards?")),
        ("md", t("## 4. Zpoždění zápisu polohy a rameno páky", "## 4. Position-record delay and lever arm")),
        ("md", t("Střed kamery ze SfM je určený ze snímků, poloha v EXIF z GNSS. Když se poloha zapíše o dt později než expozice, je posunutá o v · dt ve směru letu, takže v řadách tam a zpět má opačné znaménko. Anténa posunutá vůči kameře (rameno páky) dá posun, který se se směrem letu nemění, protože nos dronu míří stále stejně. Pozor: SfM bylo na polohy GNSS přiloženo podobnostní transformací, takže stálý posun celého bloku tím zmizel a z dat ho určit nejde.",
                 "The SfM camera centre is determined from the images, the EXIF position from GNSS. If the position is recorded dt after the exposure, it is shifted by v · dt in the flight direction, so it has opposite signs in strips flown back and forth. An antenna offset from the camera (lever arm) gives a shift that does not change with flight direction, because the drone's nose always points the same way. Note: SfM was fitted to the GNSS positions by a similarity transformation, so any constant shift of the whole block vanished and cannot be determined from the data.")),
        ("code", t(*TIMING)),
        ("task", t("Jaké zpoždění dt vychází z dat a jak se shoduje s laboratoří? Proč stálý posun vychází skoro nulový, i kdyby anténa byla před kamerou? Jak velký posun způsobí náklon těla s anténou 0,2 m nad kamerou a dá se odlišit od zpoždění?",
                   "What delay dt follows from the data and how does it agree with the lab? Why is the constant offset almost zero even if the antenna were ahead of the camera? How large a shift does the body tilt cause with the antenna 0.2 m above the camera, and can it be told apart from the delay?")),
        ("md", t("## 5. Rozmazání pohybem a závěrka", "## 5. Motion blur and shutter")),
        ("md", t("Během expozice se dron posune o v · t_exp. Když je to víc než asi polovina pixelu na zemi (GSD), snímek se viditelně rozmaže. Kamera L1D-20c nemá mechanickou závěrku: čip se vyčítá po řádcích (rolling shutter) a během vyčtení se dron posune o v · t_read.",
                 "During the exposure the drone moves by v · t_exp. If that is more than about half a ground pixel (GSD), the image is visibly blurred. The L1D-20c camera has no mechanical shutter: the sensor is read out row by row (rolling shutter) and during readout the drone moves by v · t_read.")),
        ("code", t(*BLUR)),
        ("task", t("Jaké expoziční časy kamera použila a jak velké je rozmazání v pixelech? Jaký nejdelší čas by při této rychlosti a výšce dal rozmazání pod 0,5 px? Co bys změnil v plánu letu, kdyby bylo pod mrakem tmavěji?",
                   "Which exposure times did the camera use and how large is the blur in pixels? What is the longest time that would keep the blur below 0.5 px at this speed and height? What would you change in the flight plan if it were darker under clouds?")),
        ("md", t("## 6. Výška z GNSS a z barometru", "## 6. GNSS and barometric height")),
        ("md", t("Dron měří výšku barometrem (rozdíl tlaku proti místu vzletu) a přijímačem GNSS. `h_gnss` je absolutní výška z XMP posunutá tak, aby šla porovnat s `h_baro`.",
                 "The drone measures height with a barometer (pressure difference to the take-off point) and with the GNSS receiver. `h_gnss` is the absolute altitude from XMP shifted so that it can be compared with `h_baro`.")),
        ("code", t(*HEIGHT)),
        ("task", t("Který senzor drží výšku stabilněji a proč? Má rozdíl h_gnss − h_baro trend v čase? Čím se může barometr během letu posunout?",
                   "Which sensor keeps the height more stable and why? Does the difference h_gnss − h_baro have a trend in time? What can shift the barometer during the flight?")),
        ("task", t("+ Doplňkové snímky (`set == 'extra'`) mají jiný náklon kamery a výšku. Které z nich se v SfM neregistrovaly a proč?",
                   "+ The extra images (`set == 'extra'`) have a different camera tilt and height. Which of them were not registered in SfM and why?")),
    ]
