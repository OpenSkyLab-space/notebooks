from _common import CUZK_HELPER

META = {
    "version": "1.0",
    "minutes": 50,
    "title": {"cs": "Lidar a fotogrammetrie v lese: mračna bodů a modely ČÚZK", "en": "Lidar and photogrammetry in a forest: ČÚZK point clouds and models"},
    "visual": {"cs": "LiDAR a fotogrammetrie v porostu", "en": "LiDAR vs photogrammetry under canopy"},
    "lead": {
        "cs": "Vizuál ukazuje, proč laserový pulz najde terén i pod korunami, zatímco fotogrammetrie vidí jen povrch. Tady to ověříš na skutečných datech ČÚZK z Roztockého háje u Suchdola: body terénu a povrchu z leteckého laserového skenování a povrch z obrazové korelace leteckých snímků.",
        "en": "The visual shows why a laser pulse finds the ground even under tree crowns while photogrammetry sees only the surface. Here you check it on real ČÚZK data from the Roztoky forest near Suchdol: ground and surface points from airborne laser scanning and a surface from image matching of aerial photographs.",
    },
    "goal": {
        "cs": "načíst a prohlédnout mračna bodů LAZ, zjistit, z kolikátého odrazu pocházejí body terénu v lese a na volné ploše, spočítat model výšky porostu CHM = DSM − DTM z lidaru i z fotogrammetrie, porovnat je v profilu, najít vrcholy stromů a vysvětlit rozdíly.",
        "en": "load and inspect LAZ point clouds, find out which return the ground points come from in the forest and in the open, compute the canopy height model CHM = DSM − DTM from lidar and from photogrammetry, compare them in a profile, find tree tops and explain the differences.",
    },
    "data": {
        "cs": "ČÚZK: DMR 5G (body terénu z leteckého laserového skenování, LAZ) a DMP 1G (body povrchu, LAZ) pro mapový list Kralupy nad Vltavou 7-7, rastry DMR 5G, DMP 1G a DMP OK (obrazová korelace) z obrazové služby ČÚZK; vše v S-JTSK (EPSG:5514), výšky Bpv. Data ČÚZK jsou otevřená (CC BY 4.0).",
        "en": "ČÚZK: DMR 5G (ground points from airborne laser scanning, LAZ) and DMP 1G (surface points, LAZ) for the map sheet Kralupy nad Vltavou 7-7, DMR 5G, DMP 1G and DMP OK (image matching) rasters from the ČÚZK image service; all in S-JTSK (EPSG:5514), heights in Bpv. ČÚZK data are open (CC BY 4.0).",
    },
    "sources": {
        "cs": [
            "ČÚZK: Digitální model reliéfu České republiky 5. generace (DMR 5G), úplná střední chyba výšky 0,18 m v odkrytém a 0,3 m v zalesněném terénu; Digitální model povrchu České republiky 1. generace (DMP 1G), úplná střední chyba výšky 0,4 m u budov a 0,7 m u vegetace; Digitální model povrchu z obrazové korelace (DMP OK). https://geoportal.cuzk.gov.cz",
            "Stahování LAZ: atomová služba ČÚZK, https://atom.cuzk.cz/DMR5G-SJTSK/DMR5G-SJTSK.xml a https://atom.cuzk.cz/DMP1G-SJTSK/DMP1G-SJTSK.xml; rastry: https://ags.cuzk.cz/arcgis2/rest/services",
            "ASPRS (2019). *LAS Specification 1.4 – R15* (třídy bodů, čísla odrazů, čas GPS).",
            "White, J. C., Wulder, M. A., Vastaranta, M. a kol. (2013). The utility of image-based point clouds for forest inventory: A comparison with airborne laser scanning. *Forests* 4(3), 518–536.",
        ],
        "en": [
            "ČÚZK: Digital Terrain Model of the Czech Republic of the 5th generation (DMR 5G), total root mean square height error 0.18 m in open and 0.3 m in forested terrain; Digital Surface Model of the Czech Republic of the 1st generation (DMP 1G), 0.4 m for buildings and 0.7 m for vegetation; Digital Surface Model from image matching (DMP OK). https://geoportal.cuzk.gov.cz",
            "LAZ download: ČÚZK Atom service, https://atom.cuzk.cz/DMR5G-SJTSK/DMR5G-SJTSK.xml and https://atom.cuzk.cz/DMP1G-SJTSK/DMP1G-SJTSK.xml; rasters: https://ags.cuzk.cz/arcgis2/rest/services",
            "ASPRS (2019). *LAS Specification 1.4 – R15* (point classes, return numbers, GPS time).",
            "White, J. C., Wulder, M. A., Vastaranta, M. et al. (2013). The utility of image-based point clouds for forest inventory: A comparison with airborne laser scanning. *Forests* 4(3), 518–536.",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a mračna bodů", "## 1. Setup and point clouds")),
        ("code", '%pip install -q "laspy[lazrs]" rasterio'),
        ("code", '''
import io, time, zipfile, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import laspy, rasterio
from scipy import ndimage as ndi
''' + t(CUZK_HELPER["cs"], CUZK_HELPER["en"]) + t('''
SHEET = "KRAV77"              # ◀ parametr: mapový list SM5 (názvy listů jsou v atomové službě ČÚZK)
X0, Y0, X1, Y1 = -744800, -1036000, -743800, -1035300   # ◀ parametr: výřez v S-JTSK (m), Roztocký háj a Tiché údolí

def laz(product, sheet, tries=4):
    for i in range(tries):
        try:
            r = requests.get(f"https://openzu.cuzk.gov.cz/opendata/{product}/epsg-5514/{sheet}.zip", timeout=180); r.raise_for_status(); break
        except requests.RequestException as e:
            print(product, type(e).__name__, "– zkusím znovu"); time.sleep(5 * (i + 1))
    z = zipfile.ZipFile(io.BytesIO(r.content))
    las = laspy.read(io.BytesIO(z.read(z.namelist()[0])))
    m = (las.x >= X0) & (las.x < X1) & (las.y >= Y0) & (las.y < Y1)
    return las.points[m]

ground = laz("DMR5G", SHEET)          # body terénu (klíčové body modelu reliéfu)
surface = laz("DMP1G", SHEET)         # body povrchu: 2 terén, 5 vysoká vegetace, 6 budovy
area = (X1 - X0) * (Y1 - Y0)
gps = np.median(np.asarray(ground.gps_time)) + 1e9          # „adjusted GPS time“ = sekundy od 6. 1. 1980 minus 10⁹
print(f"výřez {(X1 - X0) / 1000:.1f} × {(Y1 - Y0) / 1000:.1f} km, skenováno kolem {pd.Timestamp('1980-01-06') + pd.Timedelta(seconds=gps):%d. %m. %Y}")
CLS = {2: "terén", 5: "vysoká vegetace", 6: "budovy"}
tab = pd.DataFrame({"bodů": [len(ground)] + [int((surface.classification == c).sum()) for c in CLS]},
                   index=["DMR 5G: terén"] + [f"DMP 1G: {n}" for n in CLS.values()])
tab["bodů na m²"] = tab["bodů"] / area
print(tab.round(3))
fig, ax = plt.subplots(1, 2, figsize=(13, 4.8), sharey=True)
for c, col in zip(CLS, ["tab:brown", "tab:green", "tab:red"]):
    s = surface.classification == c
    ax[0].scatter(surface.x[s], surface.y[s], s=0.3, c=col, label=CLS[c])
ax[0].legend(markerscale=20); ax[0].set_title("DMP 1G podle tříd"); ax[0].set_aspect("equal")
sc = ax[1].scatter(ground.x, ground.y, s=0.3, c=ground.z, cmap="terrain"); ax[1].set_title("DMR 5G, výška (m)"); ax[1].set_aspect("equal")
plt.colorbar(sc, ax=ax[1]); plt.show()
''', '''
SHEET = "KRAV77"              # ◀ parameter: SM5 map sheet (sheet names are listed in the ČÚZK Atom service)
X0, Y0, X1, Y1 = -744800, -1036000, -743800, -1035300   # ◀ parameter: window in S-JTSK (m), the Roztoky forest and the Tiché údolí valley

def laz(product, sheet, tries=4):
    for i in range(tries):
        try:
            r = requests.get(f"https://openzu.cuzk.gov.cz/opendata/{product}/epsg-5514/{sheet}.zip", timeout=180); r.raise_for_status(); break
        except requests.RequestException as e:
            print(product, type(e).__name__, "– retrying"); time.sleep(5 * (i + 1))
    z = zipfile.ZipFile(io.BytesIO(r.content))
    las = laspy.read(io.BytesIO(z.read(z.namelist()[0])))
    m = (las.x >= X0) & (las.x < X1) & (las.y >= Y0) & (las.y < Y1)
    return las.points[m]

ground = laz("DMR5G", SHEET)          # ground points (key points of the terrain model)
surface = laz("DMP1G", SHEET)         # surface points: 2 ground, 5 high vegetation, 6 buildings
area = (X1 - X0) * (Y1 - Y0)
gps = np.median(np.asarray(ground.gps_time)) + 1e9          # "adjusted GPS time" = seconds since 6 Jan 1980 minus 10⁹
print(f"window {(X1 - X0) / 1000:.1f} × {(Y1 - Y0) / 1000:.1f} km, scanned around {pd.Timestamp('1980-01-06') + pd.Timedelta(seconds=gps):%d %b %Y}")
CLS = {2: "ground", 5: "high vegetation", 6: "buildings"}
tab = pd.DataFrame({"points": [len(ground)] + [int((surface.classification == c).sum()) for c in CLS]},
                   index=["DMR 5G: ground"] + [f"DMP 1G: {n}" for n in CLS.values()])
tab["points per m²"] = tab["points"] / area
print(tab.round(3))
fig, ax = plt.subplots(1, 2, figsize=(13, 4.8), sharey=True)
for c, col in zip(CLS, ["tab:brown", "tab:green", "tab:red"]):
    s = surface.classification == c
    ax[0].scatter(surface.x[s], surface.y[s], s=0.3, c=col, label=CLS[c])
ax[0].legend(markerscale=20); ax[0].set_title("DMP 1G by class"); ax[0].set_aspect("equal")
sc = ax[1].scatter(ground.x, ground.y, s=0.3, c=ground.z, cmap="terrain"); ax[1].set_title("DMR 5G, height (m)"); ax[1].set_aspect("equal")
plt.colorbar(sc, ax=ax[1]); plt.show()
''')),
        ("task", t(
            "Kolik bodů na m² mají DMR 5G a DMP 1G? Skener jich na zem poslal mnohem víc: proč ČÚZK zveřejňuje jen vybrané (klíčové) body a podle čeho je asi vybíral? Ve kterém měsíci se skenovalo? Jak ovlivní listí, kolik pulzů projde až na zem, a proč se lidar pro model terénu ideálně létá mimo vegetační sezónu?",
            "How many points per m² do DMR 5G and DMP 1G have? The scanner sent many more to the ground: why does ČÚZK publish only selected (key) points, and how might it have selected them? In which month was the scanning done? How do leaves affect how many pulses get through to the ground, and why is lidar for a terrain model ideally flown outside the growing season?")),
        ("md", t(
            "## 2. Z kolikátého odrazu je terén?\n\nKaždý bod nese číslo odrazu (return number) a počet odrazů pulzu (number of returns). Bod terénu s číslem odrazu 2 a víc znamená, že část pulzu se předtím odrazila od koruny a zbytek prošel mezerou až na zem. Les od volné plochy rozlišíme podle výšky povrchu nad terénem z rastrů DMP 1G a DMR 5G.",
            "## 2. Which return is the ground?\n\nEvery point carries a return number and the number of returns of its pulse. A ground point with return number 2 or more means that part of the pulse had been reflected by a crown and the rest passed through a gap down to the ground. We tell forest from open land by the height of the surface above the ground from the DMP 1G and DMR 5G rasters.")),
        ("code", t('''
RES = 2.0                     # ◀ parametr: velikost pixelu rastrů (m)
FOREST_H = 5                  # ◀ parametr: od jaké výšky povrchu nad terénem je to „les“ (m)
dtm, tf = cuzk_raster("dmr5g", X0, Y0, X1, Y1, RES)
dsm_l, _ = cuzk_raster("dmp1g", X0, Y0, X1, Y1, RES)
chm_l = dsm_l - dtm
r, c = rasterio.transform.rowcol(tf, np.asarray(ground.x), np.asarray(ground.y))
forest = chm_l[np.clip(r, 0, chm_l.shape[0] - 1), np.clip(c, 0, chm_l.shape[1] - 1)] > FOREST_H
rn = np.asarray(ground.return_number)
share = pd.DataFrame({"les": pd.Series(rn[forest]).value_counts(normalize=True), "volná plocha": pd.Series(rn[~forest]).value_counts(normalize=True)}).fillna(0) * 100
share.index.name = "číslo odrazu"
print(f"bodů terénu: v lese {forest.sum()} ({forest.sum() / ((chm_l > FOREST_H).sum() * RES**2):.3f}/m²), na volné ploše {(~forest).sum()} ({(~forest).sum() / ((chm_l <= FOREST_H).sum() * RES**2):.3f}/m²)")
print(share.round(1))
share.T.plot.bar(stacked=True, figsize=(6, 3.5), colormap="viridis", ylabel="% bodů terénu", rot=0); plt.legend(title="odraz", bbox_to_anchor=(1, 1)); plt.show()
''', '''
RES = 2.0                     # ◀ parameter: raster pixel size (m)
FOREST_H = 5                  # ◀ parameter: surface height above ground from which it counts as "forest" (m)
dtm, tf = cuzk_raster("dmr5g", X0, Y0, X1, Y1, RES)
dsm_l, _ = cuzk_raster("dmp1g", X0, Y0, X1, Y1, RES)
chm_l = dsm_l - dtm
r, c = rasterio.transform.rowcol(tf, np.asarray(ground.x), np.asarray(ground.y))
forest = chm_l[np.clip(r, 0, chm_l.shape[0] - 1), np.clip(c, 0, chm_l.shape[1] - 1)] > FOREST_H
rn = np.asarray(ground.return_number)
share = pd.DataFrame({"forest": pd.Series(rn[forest]).value_counts(normalize=True), "open land": pd.Series(rn[~forest]).value_counts(normalize=True)}).fillna(0) * 100
share.index.name = "return number"
print(f"ground points: in the forest {forest.sum()} ({forest.sum() / ((chm_l > FOREST_H).sum() * RES**2):.3f}/m²), in the open {(~forest).sum()} ({(~forest).sum() / ((chm_l <= FOREST_H).sum() * RES**2):.3f}/m²)")
print(share.round(1))
share.T.plot.bar(stacked=True, figsize=(6, 3.5), colormap="viridis", ylabel="% of ground points", rot=0); plt.legend(title="return", bbox_to_anchor=(1, 1)); plt.show()
''')),
        ("task", t(
            "Jaký podíl bodů terénu v lese pochází z 2. a dalšího odrazu a jaký na volné ploše? Proč není na volné ploše nula? Co by se stalo s modelem terénu pod lesem, kdyby skener zaznamenával jen první odraz? A proč fotogrammetrie (SfM) terén pod zapojeným porostem nenajde vůbec?",
            "What share of ground points in the forest comes from the 2nd or a later return, and what share in the open? Why is it not zero in the open? What would happen to the terrain model under the forest if the scanner recorded only the first return? And why does photogrammetry (SfM) not find the ground under a closed canopy at all?")),
        ("md", t(
            "## 3. CHM z lidaru a z fotogrammetrie\n\nCHM = DSM − DTM. DTM bereme vždy z lidaru (DMR 5G). DSM jednou z lidaru (DMP 1G), jednou z obrazové korelace leteckých měřických snímků (DMP OK), které ČÚZK pořídil později (letecké měřické snímkování probíhá obvykle od jara do léta). Obrazová korelace je stejný princip jako fotogrammetrie z dronu.",
            "## 3. CHM from lidar and from photogrammetry\n\nCHM = DSM − DTM. The DTM always comes from lidar (DMR 5G). The DSM comes once from lidar (DMP 1G) and once from image matching of aerial survey photographs (DMP OK), which ČÚZK took later (aerial survey photography usually takes place from spring to summer). Image matching is the same principle as drone photogrammetry.")),
        ("code", t('''
dsm_p, _ = cuzk_raster("dmp_obrazova_korelace", X0, Y0, X1, Y1, RES)
chm_p = dsm_p - dtm
ext = (X0, X1, Y0, Y1)
fig, ax = plt.subplots(1, 3, figsize=(16, 4.2))
for a, (name, v) in zip(ax, [("CHM lidar (DMP 1G − DMR 5G)", chm_l), ("CHM fotogrammetrie (DMP OK − DMR 5G)", chm_p)]):
    im = a.imshow(np.clip(v, 0, 35), extent=ext, cmap="viridis"); a.set_title(name); plt.colorbar(im, ax=a, label="m")
bins = np.arange(-2, 40, 1)
ax[2].hist(chm_l[chm_l > FOREST_H], bins, alpha=0.6, label="lidar"); ax[2].hist(chm_p[chm_l > FOREST_H], bins, alpha=0.6, label="fotogrammetrie")
ax[2].set_xlabel("výška porostu v lese (m)"); ax[2].legend(); plt.show()
fm = chm_l > FOREST_H
print(pd.DataFrame({"lidar": pd.Series(chm_l[fm]).describe(percentiles=[0.5, 0.95]), "fotogrammetrie": pd.Series(chm_p[fm]).describe(percentiles=[0.5, 0.95])}).loc[["mean", "50%", "95%", "max"]].round(1))
''', '''
dsm_p, _ = cuzk_raster("dmp_obrazova_korelace", X0, Y0, X1, Y1, RES)
chm_p = dsm_p - dtm
ext = (X0, X1, Y0, Y1)
fig, ax = plt.subplots(1, 3, figsize=(16, 4.2))
for a, (name, v) in zip(ax, [("CHM lidar (DMP 1G − DMR 5G)", chm_l), ("CHM photogrammetry (DMP OK − DMR 5G)", chm_p)]):
    im = a.imshow(np.clip(v, 0, 35), extent=ext, cmap="viridis"); a.set_title(name); plt.colorbar(im, ax=a, label="m")
bins = np.arange(-2, 40, 1)
ax[2].hist(chm_l[chm_l > FOREST_H], bins, alpha=0.6, label="lidar"); ax[2].hist(chm_p[chm_l > FOREST_H], bins, alpha=0.6, label="photogrammetry")
ax[2].set_xlabel("canopy height in the forest (m)"); ax[2].legend(); plt.show()
fm = chm_l > FOREST_H
print(pd.DataFrame({"lidar": pd.Series(chm_l[fm]).describe(percentiles=[0.5, 0.95]), "photogrammetry": pd.Series(chm_p[fm]).describe(percentiles=[0.5, 0.95])}).loc[["mean", "50%", "95%", "max"]].round(1))
''')),
        ("task", t(
            "Který CHM ukazuje v lese vyšší porost a o kolik (medián, 95. percentil)? Najdi aspoň tři důvody: roky mezi snímkováním, listí v létě a v době skenování, jak obrazová korelace „vyhlazuje“ mezery mezi korunami. Kde v mapě jsou rozdíly největší?",
            "Which CHM shows taller vegetation in the forest, and by how much (median, 95th percentile)? Find at least three reasons: the years between acquisitions, leaves in summer and at the time of scanning, how image matching \"smooths over\" gaps between crowns. Where in the map are the differences largest?")),
        ("md", t(
            "## 4. Profil porostem\n\nBody obou mračen v pásu podél zvolené čáry a profily tří povrchů.",
            "## 4. A profile through the forest\n\nPoints of both clouds in a strip along a chosen line, and profiles of the three surfaces.")),
        ("code", t('''
A_XY = (-744300, -1035950)    # ◀ parametr: začátek profilu (S-JTSK, m)
B_XY = (-744300, -1035350)    # ◀ parametr: konec profilu
HALF_W = 5                    # ◀ parametr: poloviční šířka pásu (m)
a, b = np.array(A_XY, float), np.array(B_XY, float); u = (b - a) / np.linalg.norm(b - a); n = np.array([-u[1], u[0]])
def strip(pts):
    d = np.c_[np.asarray(pts.x), np.asarray(pts.y)] - a
    s, o = d @ u, d @ n; m = (np.abs(o) <= HALF_W) & (s >= 0) & (s <= np.linalg.norm(b - a))
    return s[m], np.asarray(pts.z)[m], m
s_vals = np.arange(0, np.linalg.norm(b - a), RES / 2)
xy = a + np.outer(s_vals, u)
rr, cc = rasterio.transform.rowcol(tf, xy[:, 0], xy[:, 1])
fig, ax = plt.subplots(figsize=(13, 4.5))
for name, v, st in [("DTM lidar (DMR 5G)", dtm, "k-"), ("DSM lidar (DMP 1G)", dsm_l, "g-"), ("DSM fotogrammetrie (DMP OK)", dsm_p, "m-")]:
    ax.plot(s_vals, v[rr, cc], st, lw=1.2, label=name)
s, z, m = strip(surface)
for cl, col in zip(CLS, ["tab:brown", "tab:green", "tab:red"]):
    k = np.asarray(surface.classification)[m] == cl; ax.scatter(s[k], z[k], s=6, c=col, label=f"body DMP 1G: {CLS[cl]}")
s, z, m = strip(ground); k = np.asarray(ground.return_number)[m] > 1
ax.scatter(s[~k], z[~k], s=14, marker="^", c="k", label="body DMR 5G, 1. odraz"); ax.scatter(s[k], z[k], s=14, marker="^", facecolors="none", edgecolors="k", label="body DMR 5G, 2.+ odraz")
ax.set_xlabel("vzdálenost od začátku profilu (m)"); ax.set_ylabel("výška Bpv (m)"); ax.legend(fontsize=7, ncol=2); plt.show()
''', '''
A_XY = (-744300, -1035950)    # ◀ parameter: start of the profile (S-JTSK, m)
B_XY = (-744300, -1035350)    # ◀ parameter: end of the profile
HALF_W = 5                    # ◀ parameter: half-width of the strip (m)
a, b = np.array(A_XY, float), np.array(B_XY, float); u = (b - a) / np.linalg.norm(b - a); n = np.array([-u[1], u[0]])
def strip(pts):
    d = np.c_[np.asarray(pts.x), np.asarray(pts.y)] - a
    s, o = d @ u, d @ n; m = (np.abs(o) <= HALF_W) & (s >= 0) & (s <= np.linalg.norm(b - a))
    return s[m], np.asarray(pts.z)[m], m
s_vals = np.arange(0, np.linalg.norm(b - a), RES / 2)
xy = a + np.outer(s_vals, u)
rr, cc = rasterio.transform.rowcol(tf, xy[:, 0], xy[:, 1])
fig, ax = plt.subplots(figsize=(13, 4.5))
for name, v, st in [("DTM lidar (DMR 5G)", dtm, "k-"), ("DSM lidar (DMP 1G)", dsm_l, "g-"), ("DSM photogrammetry (DMP OK)", dsm_p, "m-")]:
    ax.plot(s_vals, v[rr, cc], st, lw=1.2, label=name)
s, z, m = strip(surface)
for cl, col in zip(CLS, ["tab:brown", "tab:green", "tab:red"]):
    k = np.asarray(surface.classification)[m] == cl; ax.scatter(s[k], z[k], s=6, c=col, label=f"DMP 1G points: {CLS[cl]}")
s, z, m = strip(ground); k = np.asarray(ground.return_number)[m] > 1
ax.scatter(s[~k], z[~k], s=14, marker="^", c="k", label="DMR 5G points, 1st return"); ax.scatter(s[k], z[k], s=14, marker="^", facecolors="none", edgecolors="k", label="DMR 5G points, 2nd+ return")
ax.set_xlabel("distance from the start of the profile (m)"); ax.set_ylabel("height Bpv (m)"); ax.legend(fontsize=7, ncol=2); plt.show()
''')),
        ("task", t(
            "Kde v profilu je les a kde volná plocha? Jak se liší DSM z lidaru a z fotogrammetrie na okraji lesa a v mezerách mezi korunami? Které body terénu jsou v lese z 2. a dalšího odrazu? Přesuň profil jinam (třeba přes údolí nebo budovy) a popiš, co vidíš.",
            "Where in the profile is the forest and where the open land? How do the lidar and photogrammetric DSMs differ at the forest edge and in gaps between crowns? Which ground points in the forest come from the 2nd or a later return? Move the profile elsewhere (e.g. across the valley or buildings) and describe what you see.")),
        ("md", t(
            "## 5. Vrcholy stromů\n\nVrchol stromu hledáme jako lokální maximum CHM v okně dané velikosti, které je vyšší než zvolená mez. Použijeme fotogrammetrický DSM v plném rozlišení 0,5 m.",
            "## 5. Tree tops\n\nWe look for a tree top as a local maximum of the CHM within a window of given size that is higher than a chosen limit. We use the photogrammetric DSM at its full resolution of 0.5 m.")),
        ("code", t('''
WIN = 5                       # ◀ parametr: velikost okna pro lokální maximum (m)
MIN_H = 10                    # ◀ parametr: minimální výška stromu (m)
SUB = (-744600, -1035900, -744300, -1035600)   # ◀ parametr: menší výřez v lese (S-JTSK, m)
d05, t05 = cuzk_raster("dmp_obrazova_korelace", *SUB, res=0.5)
g05, _ = cuzk_raster("dmr5g", *SUB, res=0.5)
chm05 = ndi.gaussian_filter(d05 - g05, 1)
k = max(3, int(round(WIN / 0.5)) | 1)
tops = (chm05 == ndi.maximum_filter(chm05, size=k)) & (chm05 > MIN_H)
rows_, cols_ = np.nonzero(tops)
ha = (SUB[2] - SUB[0]) * (SUB[3] - SUB[1]) / 1e4
print(f"okno {WIN} m, mez {MIN_H} m: {tops.sum()} vrcholů na {ha:.1f} ha = {tops.sum() / ha:.0f} stromů/ha, medián výšky {np.median(chm05[tops]):.1f} m")
fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.imshow(np.clip(chm05, 0, 35), cmap="viridis", extent=(SUB[0], SUB[2], SUB[1], SUB[3]))
xs, ys = rasterio.transform.xy(t05, rows_, cols_)
ax.scatter(xs, ys, s=8, c="r"); ax.set_title("CHM 0,5 m a nalezené vrcholy"); plt.show()
''', '''
WIN = 5                       # ◀ parameter: window size for the local maximum (m)
MIN_H = 10                    # ◀ parameter: minimum tree height (m)
SUB = (-744600, -1035900, -744300, -1035600)   # ◀ parameter: a smaller window in the forest (S-JTSK, m)
d05, t05 = cuzk_raster("dmp_obrazova_korelace", *SUB, res=0.5)
g05, _ = cuzk_raster("dmr5g", *SUB, res=0.5)
chm05 = ndi.gaussian_filter(d05 - g05, 1)
k = max(3, int(round(WIN / 0.5)) | 1)
tops = (chm05 == ndi.maximum_filter(chm05, size=k)) & (chm05 > MIN_H)
rows_, cols_ = np.nonzero(tops)
ha = (SUB[2] - SUB[0]) * (SUB[3] - SUB[1]) / 1e4
print(f"window {WIN} m, limit {MIN_H} m: {tops.sum()} tops on {ha:.1f} ha = {tops.sum() / ha:.0f} trees/ha, median height {np.median(chm05[tops]):.1f} m")
fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.imshow(np.clip(chm05, 0, 35), cmap="viridis", extent=(SUB[0], SUB[2], SUB[1], SUB[3]))
xs, ys = rasterio.transform.xy(t05, rows_, cols_)
ax.scatter(xs, ys, s=8, c="r"); ax.set_title("CHM 0.5 m and the tops found"); plt.show()
''')),
        ("task", t(
            "Kolik stromů na hektar najdeš s oknem 3 m, 5 m a 9 m? Které číslo je nejblíž skutečnosti, pokud mají koruny průměr kolem 8–12 m, a proč malé okno počet přeceňuje? Co by se stalo s počtem, kdybys použil CHM z lidaru s pixelem 2 m?",
            "How many trees per hectare do you find with a window of 3 m, 5 m and 9 m? Which number is closest to reality if the crowns are about 8–12 m across, and why does a small window overestimate the count? What would happen to the count if you used the lidar CHM with a 2 m pixel?")),
        ("md", t(
            "## 6. Co se mezi snímkováními změnilo\n\nRozdíl CHM z fotogrammetrie a z lidaru ukazuje růst porostu, těžbu i chyby obou metod. Přesnost udává ČÚZK jako úplnou střední chybu výšky: DMR 5G 0,18 m v odkrytém a 0,3 m v zalesněném terénu, DMP 1G 0,4 m u budov a 0,7 m u vegetace.",
            "## 6. What changed between the acquisitions\n\nThe difference between the photogrammetric and the lidar CHM shows forest growth, felling and the errors of both methods. ČÚZK gives the accuracy as the total root mean square height error: DMR 5G 0.18 m in open and 0.3 m in forested terrain, DMP 1G 0.4 m for buildings and 0.7 m for vegetation.")),
        ("code", t('''
CHANGE = 5                    # ◀ parametr: od jakého rozdílu výšky (m) to považujeme za změnu
diff = chm_p - chm_l
fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
im = ax[0].imshow(np.clip(diff, -15, 15), extent=ext, cmap="RdBu"); plt.colorbar(im, ax=ax[0], label="CHM fotogrammetrie − CHM lidar (m)")
ax[0].set_title("modře: vyšší ve fotogrammetrii, červeně: nižší")
ax[1].hist(diff[fm], np.arange(-20, 20, 0.5), color="gray"); ax[1].set_xlabel("rozdíl v lese (m)"); plt.show()
print(f"v lese: medián rozdílu {np.median(diff[fm]):+.1f} m; o víc než {CHANGE} m výš {100 * (diff[fm] > CHANGE).mean():.0f} %, o víc než {CHANGE} m níž {100 * (diff[fm] < -CHANGE).mean():.0f} % plochy")
''', '''
CHANGE = 5                    # ◀ parameter: height difference (m) from which we count it as a change
diff = chm_p - chm_l
fig, ax = plt.subplots(1, 2, figsize=(14, 4.5))
im = ax[0].imshow(np.clip(diff, -15, 15), extent=ext, cmap="RdBu"); plt.colorbar(im, ax=ax[0], label="CHM photogrammetry − CHM lidar (m)")
ax[0].set_title("blue: higher in photogrammetry, red: lower")
ax[1].hist(diff[fm], np.arange(-20, 20, 0.5), color="gray"); ax[1].set_xlabel("difference in the forest (m)"); plt.show()
print(f"in the forest: median difference {np.median(diff[fm]):+.1f} m; more than {CHANGE} m higher on {100 * (diff[fm] > CHANGE).mean():.0f} %, more than {CHANGE} m lower on {100 * (diff[fm] < -CHANGE).mean():.0f} % of the area")
''')),
        ("task", t(
            "Je medián rozdílu v lese větší, než vysvětlí udávaná přesnost obou modelů? Kolik by musel les za ta léta vyrůst a je to realistické (dohledej, jaký je typický roční výškový přírůst dospělého listnatého lesa)? Najdi v mapě místa, kde porost zmizel (těžba, polom) nebo přibyl. Proč nejde z jednoho fotogrammetrického DSM bez lidarového DTM výšku porostu vůbec spočítat?",
            "Is the median difference in the forest larger than the stated accuracy of both models explains? How much would the forest have had to grow over those years, and is that realistic (look up the typical annual height increment of a mature broadleaved forest)? Find places in the map where the forest disappeared (felling, windthrow) or appeared. Why can canopy height not be computed at all from a single photogrammetric DSM without a lidar DTM?")),
    ]
