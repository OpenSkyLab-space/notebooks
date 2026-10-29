META = {
    "version": "1.0",
    "minutes": 45,
    "title": {"cs": "Vlícovací a kontrolní body: přesnost transformace na skutečném bodovém poli", "en": "Ground control and check points: transformation accuracy on a real survey network"},
    "visual": {"cs": "Vlícovací body a přesnost", "en": "Ground control points and accuracy"},
    "lead": {
        "cs": "Vizuál simuluje, jak rozmístění vlícovacích bodů a způsob georeferencování ovlivní přesnost mapy z dronu. Tady stejné principy ověříš na skutečných bodech bodového pole ČÚZK: každý bod má souřadnice z GNSS v ETRS89 a zároveň souřadnice v S-JTSK a nadmořskou výšku v Bpv. Převod mezi systémy odhadneš z několika vlícovacích bodů a jeho přesnost změříš na ostatních, nezávislých kontrolních bodech. Je to stejná úloha jako georeferencování bloku snímků, jen na území desítek kilometrů.",
        "en": "The visual simulates how the layout of ground control points and the georeferencing method affect the accuracy of a drone map. Here you test the same principles on real points of the ČÚZK survey network: every point has GNSS coordinates in ETRS89 as well as coordinates in S-JTSK and an elevation in Bpv. You estimate the conversion between the systems from a few ground control points and measure its accuracy on the other, independent check points. It is the same task as georeferencing an image block, only over tens of kilometres.",
    },
    "goal": {
        "cs": "odhadnout podobnostní (Helmertovu) transformaci z vlícovacích bodů, porovnat odchylky na vlícovacích a kontrolních bodech pro různé rozmístění, převést elipsoidické výšky na Bpv, posoudit, kolik kontrolních bodů je potřeba, a ukázat, kdy složitější transformace škodí.",
        "en": "estimate a similarity (Helmert) transformation from ground control points, compare residuals on control and check points for different layouts, convert ellipsoidal heights to Bpv, judge how many check points are needed, and show when a more complex transformation does harm.",
    },
    "data": {
        "cs": "trigonometrické a zhušťovací body ČÚZK v okolí Prahy se souřadnicemi S-JTSK, výškou Bpv a souřadnicemi ETRS89 (B, L, elipsoidická výška) ze statického měření GNSS, služba BodovaPole (vrstva 2).",
        "en": "ČÚZK trigonometric and densification points around Prague with S-JTSK coordinates, Bpv elevation and ETRS89 coordinates (B, L, ellipsoidal height) from static GNSS observations, BodovaPole service (layer 2).",
    },
    "sources": {
        "cs": [
            "Bodová pole: © ČÚZK, služba https://ags.cuzk.cz/arcgis/rest/services/BodovaPole/MapServer (CC BY 4.0); geodetické údaje bodů na https://geoportal.cuzk.gov.cz",
            "ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 1.0 (RMSE_H, RMSE_V, nejméně 30 kontrolních bodů).",
            "Sanz-Ablanedo, E., Chandler, J. H., Rodríguez-Pérez, J. R., Ordóñez, C. (2018). Accuracy of Unmanned Aerial Vehicle (UAV) and SfM Photogrammetry Survey as a Function of the Number and Location of Ground Control Points Used. *Remote Sensing* 10(10), 1606.",
            "Hofmann-Wellenhof, B., Lichtenegger, H., Wasle, E. (2008). *GNSS – Global Navigation Satellite Systems*. Springer (elipsoidická a normální výška, výšková anomálie).",
        ],
        "en": [
            "Survey control: © ČÚZK, service https://ags.cuzk.cz/arcgis/rest/services/BodovaPole/MapServer (CC BY 4.0); point descriptions at https://geoportal.cuzk.gov.cz",
            "ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 1.0 (RMSE_H, RMSE_V, at least 30 check points).",
            "Sanz-Ablanedo, E., Chandler, J. H., Rodríguez-Pérez, J. R., Ordóñez, C. (2018). Accuracy of Unmanned Aerial Vehicle (UAV) and SfM Photogrammetry Survey as a Function of the Number and Location of Ground Control Points Used. *Remote Sensing* 10(10), 1606.",
            "Hofmann-Wellenhof, B., Lichtenegger, H., Wasle, E. (2008). *GNSS – Global Navigation Satellite Systems*. Springer (ellipsoidal and normal height, height anomaly).",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a body bodového pole", "## 1. Setup and survey points")),
        ("code", "%pip install -q pyproj"),
        ("code", t('''
import requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from pyproj import Transformer

CX, CY = -742000, -1045000    # ◀ parametr: střed území v S-JTSK (EPSG:5514, m), Praha
HALF = 30000                  # ◀ parametr: polovina strany území (m)
q = requests.get("https://ags.cuzk.cz/arcgis/rest/services/BodovaPole/MapServer/2/query",
                 params={"geometry": f"{CX - HALF},{CY - HALF},{CX + HALF},{CY + HALF}", "geometryType": "esriGeometryEnvelope", "inSR": 5514,
                         "outFields": "CISLO_SMO5,CISLO,NAZEV_KU,Y,X,VYSKA,B,L,HEL", "returnGeometry": "false", "f": "json"}, timeout=120).json()
p = pd.DataFrame([f["attributes"] for f in q["features"]])
for k in ["Y", "X", "VYSKA", "B", "L", "HEL"]:
    p[k] = pd.to_numeric(p[k], errors="coerce")
p = p.dropna(subset=["Y", "X", "VYSKA", "B", "L", "HEL"]).reset_index(drop=True)
# „mapa“: polohy z GNSS v ETRS89 převedené do UTM 33N; „skutečnost“: S-JTSK (osy EPSG:5514: x = −Y, y = −X)
p["E"], p["N"] = Transformer.from_crs(4258, 32633, always_xy=True).transform(p.L.values, p.B.values)
p["sx"], p["sy"] = -p.Y, -p.X
SRC, DST = p[["E", "N"]].values, p[["sx", "sy"]].values
C0 = SRC.mean(axis=0)
print(f"bodů: {len(p)} na území {2 * HALF / 1000:.0f} × {2 * HALF / 1000:.0f} km")
p[["CISLO_SMO5", "CISLO", "NAZEV_KU", "Y", "X", "VYSKA", "B", "L", "HEL"]].head()
''', '''
import requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from pyproj import Transformer

CX, CY = -742000, -1045000    # ◀ parameter: centre of the area in S-JTSK (EPSG:5514, m), Prague
HALF = 30000                  # ◀ parameter: half the side of the area (m)
q = requests.get("https://ags.cuzk.cz/arcgis/rest/services/BodovaPole/MapServer/2/query",
                 params={"geometry": f"{CX - HALF},{CY - HALF},{CX + HALF},{CY + HALF}", "geometryType": "esriGeometryEnvelope", "inSR": 5514,
                         "outFields": "CISLO_SMO5,CISLO,NAZEV_KU,Y,X,VYSKA,B,L,HEL", "returnGeometry": "false", "f": "json"}, timeout=120).json()
p = pd.DataFrame([f["attributes"] for f in q["features"]])
for k in ["Y", "X", "VYSKA", "B", "L", "HEL"]:
    p[k] = pd.to_numeric(p[k], errors="coerce")
p = p.dropna(subset=["Y", "X", "VYSKA", "B", "L", "HEL"]).reset_index(drop=True)
# "map": GNSS positions in ETRS89 converted to UTM 33N; "truth": S-JTSK (EPSG:5514 axes: x = −Y, y = −X)
p["E"], p["N"] = Transformer.from_crs(4258, 32633, always_xy=True).transform(p.L.values, p.B.values)
p["sx"], p["sy"] = -p.Y, -p.X
SRC, DST = p[["E", "N"]].values, p[["sx", "sy"]].values
C0 = SRC.mean(axis=0)
print(f"points: {len(p)} in an area of {2 * HALF / 1000:.0f} × {2 * HALF / 1000:.0f} km")
p[["CISLO_SMO5", "CISLO", "NAZEV_KU", "Y", "X", "VYSKA", "B", "L", "HEL"]].head()
''')),
        ("md", t(
            "## 2. Helmertova transformace z vlícovacích bodů\n\n"
            "Podobnostní transformace má 4 parametry (posun x, y, otočení, měřítko): x' = a·x − b·y + tₓ, y' = b·x + a·y + t_y. Odhadneme ji metodou nejmenších čtverců z vlícovacích bodů a pak ji použijeme na všechny body. "
            "Odchylka na vlícovacím bodě říká jen, jak dobře se transformace k těmto bodům přizpůsobila. Přesnost ukážou až kontrolní body, které do výpočtu nevstoupily. RMSE_H = √(průměr(Δx² + Δy²)).\n\n"
            "Pozor: S-JTSK má vlastní deformace a měřítko Křovákova zobrazení se mění se zeměpisnou šířkou, takže ani nejlepší podobnostní transformace na takovém území není dokonalá. ČÚZK proto pro převod používá transformaci s opravnou sítí. Pro nás je to výhoda: je tu skutečná, předem neznámá chyba, kterou musí odhalit kontrolní body.",
            "## 2. Helmert transformation from ground control points\n\n"
            "A similarity transformation has 4 parameters (shift x, y, rotation, scale): x' = a·x − b·y + tₓ, y' = b·x + a·y + t_y. We estimate it by least squares from the ground control points and then apply it to all points. "
            "A residual on a control point only says how well the transformation adapted to those points. Accuracy is shown by check points that did not enter the computation. RMSE_H = √(mean(Δx² + Δy²)).\n\n"
            "Note: S-JTSK has its own distortions and the scale of the Křovák projection changes with latitude, so even the best similarity transformation over such an area is not perfect. ČÚZK therefore converts with a transformation plus a correction grid. For us this is an advantage: there is a real error, unknown in advance, that the check points have to reveal.")),
        ("code", t('''
def fit(src, dst, kind="helmert"):
    """Parametry transformace src → dst nejmenšími čtverci (souřadnice vztažené ke středu C0)."""
    x, y = (src - C0).T
    if kind == "helmert":
        A = np.zeros((2 * len(x), 4)); A[0::2] = np.c_[x, -y, np.ones_like(x), 0 * x]; A[1::2] = np.c_[y, x, 0 * x, np.ones_like(x)]
        return kind, np.linalg.lstsq(A, dst.ravel(), rcond=None)[0]
    cols = {"afinní": [1, x, y], "affine": [1, x, y], "polynom 2": [1, x, y, x * x, x * y, y * y], "polynomial 2": [1, x, y, x * x, x * y, y * y]}[kind]
    B = np.c_[tuple(np.broadcast_to(c, x.shape) for c in cols)]
    return kind, np.linalg.lstsq(B, dst, rcond=None)[0]

def apply(model, src):
    kind, par = model; x, y = (src - C0).T
    if kind == "helmert":
        a, b, tx, ty = par; return np.c_[a * x - b * y + tx, b * x + a * y + ty]
    cols = [1, x, y] if kind in ("afinní", "affine") else [1, x, y, x * x, x * y, y * y]
    return np.c_[tuple(np.broadcast_to(c, x.shape) for c in cols)] @ par

def pick(targets):
    """Pro každý cílový bod (podíl šířky a výšky území) najde nejbližší skutečný bod."""
    x0, y0 = SRC.min(axis=0); x1, y1 = SRC.max(axis=0)
    idx = [int(np.argmin(np.hypot(SRC[:, 0] - (x0 + fx * (x1 - x0)), SRC[:, 1] - (y0 + fy * (y1 - y0))))) for fx, fy in targets]
    return np.array(list(dict.fromkeys(idx)))

LAYOUTS = {
    "rohy + střed":        pick([(0, 0), (0, 1), (1, 0), (1, 1), (0.5, 0.5)]),
    "1 ve středu":         pick([(0.5, 0.5)]),
    "shluk v rohu":        np.argsort(np.hypot(*(SRC - SRC.min(axis=0)).T))[:5],
    "jen podél linie":     pick([(f, 0.5) for f in np.linspace(0, 1, 5)]),
    "10 rovnoměrně":       pick([(fx, fy) for fx in (0.1, 0.5, 0.9) for fy in (0.1, 0.5, 0.9)] + [(0.3, 0.3)]),
}
LAYOUT = "shluk v rohu"       # ◀ parametr: jedno z rozmístění výše
gcp = LAYOUTS[LAYOUT]; chk = np.setdiff1d(np.arange(len(p)), gcp)
model = fit(SRC[gcp], DST[gcp], "helmert") if len(gcp) >= 2 else None
pred = apply(model, SRC) if model else SRC - SRC[gcp].mean(axis=0) + DST[gcp].mean(axis=0)   # jeden bod: jen posun
res = pred - DST
rmse = lambda r: np.sqrt((r ** 2).sum(axis=1).mean())
print(f"{LAYOUT}: {len(gcp)} vlícovacích, {len(chk)} kontrolních bodů")
print(f"RMSE_H na vlícovacích bodech {rmse(res[gcp]):.3f} m, na kontrolních {rmse(res[chk]):.3f} m, největší odchylka kontrolního bodu {np.hypot(*res[chk].T).max():.2f} m")
fig, ax = plt.subplots(figsize=(7, 6.5))
q_ = ax.quiver(p.sx[chk], p.sy[chk], res[chk, 0], res[chk, 1], np.hypot(*res[chk].T), cmap="viridis", scale=15, scale_units="width")
ax.scatter(p.sx[gcp], p.sy[gcp], marker="^", s=120, c="r", label="vlícovací body"); ax.quiverkey(q_, 0.85, 1.03, 1, "1 m", labelpos="E")
ax.set_aspect("equal"); ax.legend(loc="lower right"); ax.set_title("odchylky na kontrolních bodech (šipky)"); plt.colorbar(q_, label="m", shrink=0.7); plt.show()
''', '''
def fit(src, dst, kind="helmert"):
    """Least-squares transformation parameters src → dst (coordinates relative to the centre C0)."""
    x, y = (src - C0).T
    if kind == "helmert":
        A = np.zeros((2 * len(x), 4)); A[0::2] = np.c_[x, -y, np.ones_like(x), 0 * x]; A[1::2] = np.c_[y, x, 0 * x, np.ones_like(x)]
        return kind, np.linalg.lstsq(A, dst.ravel(), rcond=None)[0]
    cols = {"affine": [1, x, y], "polynomial 2": [1, x, y, x * x, x * y, y * y]}[kind]
    B = np.c_[tuple(np.broadcast_to(c, x.shape) for c in cols)]
    return kind, np.linalg.lstsq(B, dst, rcond=None)[0]

def apply(model, src):
    kind, par = model; x, y = (src - C0).T
    if kind == "helmert":
        a, b, tx, ty = par; return np.c_[a * x - b * y + tx, b * x + a * y + ty]
    cols = [1, x, y] if kind == "affine" else [1, x, y, x * x, x * y, y * y]
    return np.c_[tuple(np.broadcast_to(c, x.shape) for c in cols)] @ par

def pick(targets):
    """For each target (fraction of the area's width and height) find the nearest real point."""
    x0, y0 = SRC.min(axis=0); x1, y1 = SRC.max(axis=0)
    idx = [int(np.argmin(np.hypot(SRC[:, 0] - (x0 + fx * (x1 - x0)), SRC[:, 1] - (y0 + fy * (y1 - y0))))) for fx, fy in targets]
    return np.array(list(dict.fromkeys(idx)))

LAYOUTS = {
    "corners + centre":    pick([(0, 0), (0, 1), (1, 0), (1, 1), (0.5, 0.5)]),
    "1 in the centre":     pick([(0.5, 0.5)]),
    "cluster in a corner": np.argsort(np.hypot(*(SRC - SRC.min(axis=0)).T))[:5],
    "along a line only":   pick([(f, 0.5) for f in np.linspace(0, 1, 5)]),
    "10 evenly":           pick([(fx, fy) for fx in (0.1, 0.5, 0.9) for fy in (0.1, 0.5, 0.9)] + [(0.3, 0.3)]),
}
LAYOUT = "cluster in a corner"   # ◀ parameter: one of the layouts above
gcp = LAYOUTS[LAYOUT]; chk = np.setdiff1d(np.arange(len(p)), gcp)
model = fit(SRC[gcp], DST[gcp], "helmert") if len(gcp) >= 2 else None
pred = apply(model, SRC) if model else SRC - SRC[gcp].mean(axis=0) + DST[gcp].mean(axis=0)   # one point: shift only
res = pred - DST
rmse = lambda r: np.sqrt((r ** 2).sum(axis=1).mean())
print(f"{LAYOUT}: {len(gcp)} control points, {len(chk)} check points")
print(f"RMSE_H on control points {rmse(res[gcp]):.3f} m, on check points {rmse(res[chk]):.3f} m, largest check point residual {np.hypot(*res[chk].T).max():.2f} m")
fig, ax = plt.subplots(figsize=(7, 6.5))
q_ = ax.quiver(p.sx[chk], p.sy[chk], res[chk, 0], res[chk, 1], np.hypot(*res[chk].T), cmap="viridis", scale=15, scale_units="width")
ax.scatter(p.sx[gcp], p.sy[gcp], marker="^", s=120, c="r", label="ground control points"); ax.quiverkey(q_, 0.85, 1.03, 1, "1 m", labelpos="E")
ax.set_aspect("equal"); ax.legend(loc="lower right"); ax.set_title("residuals on check points (arrows)"); plt.colorbar(q_, label="m", shrink=0.7); plt.show()
''')),
        ("task", t(
            "Pro „shluk v rohu“ porovnej RMSE_H na vlícovacích a na kontrolních bodech. Proč jsou odchylky na vlícovacích bodech tak malé a proč z nich nelze vykázat přesnost? Kde na mapě rostou odchylky kontrolních bodů? Pak zvol „rohy + střed“: proč je teď odchylka na vlícovacích bodech větší než na kontrolních?",
            "For the “cluster in a corner” compare RMSE_H on the control points and on the check points. Why are the residuals on the control points so small, and why can they not be reported as accuracy? Where on the map do the check point residuals grow? Then choose “corners + centre”: why is the residual on the control points now larger than on the check points?")),
        ("md", t(
            "## 3. Porovnání rozmístění, polohy i výšky\n\n"
            "GNSS dává elipsoidickou výšku h, mapy v ČR používají nadmořskou (normální) výšku v Bpv: H = h − ζ, kde ζ je výšková anomálie (v okolí Prahy kolem 44–46 m). Když z vlícovacích bodů odhadneme ζ jako konstantu, nebo jako rovinu, dostaneme výšky na kontrolních bodech. RMSE_V = √(průměr ΔH²).\n\nZ jediného vlícovacího bodu lze polohově odhadnout jen posun. UTM a S-JTSK jsou ale vůči sobě pootočené a mají jiné měřítko, proto tu chyba vyjde v kilometrech. U bloku snímků z RTK nebo PPK je natočení i měřítko dané už polohami snímků.",
            "## 3. Comparing layouts, position and height\n\n"
            "GNSS gives the ellipsoidal height h, maps in Czechia use the normal height in Bpv: H = h − ζ, where ζ is the height anomaly (about 44–46 m around Prague). If we estimate ζ from the control points as a constant or as a plane, we get heights at the check points. RMSE_V = √(mean ΔH²).\n\nA single control point can only give a shift in position. UTM and S-JTSK, however, are rotated relative to each other and have a different scale, so the error here comes out in kilometres. For an image block from RTK or PPK, rotation and scale are already set by the image positions.")),
        ("code", t('''
zeta = (p.HEL - p.VYSKA).values
x, y = (SRC - C0).T
rows = {}
for name, g in LAYOUTS.items():
    c = np.setdiff1d(np.arange(len(p)), g)
    r = (apply(fit(SRC[g], DST[g]), SRC) if len(g) >= 2 else SRC - SRC[g].mean(axis=0) + DST[g].mean(axis=0)) - DST
    const = zeta[g].mean()
    plane = np.linalg.lstsq(np.c_[np.ones(len(g)), x[g], y[g]], zeta[g], rcond=None)[0] if len(g) >= 3 else None
    rows[name] = {"vlícovacích": len(g), "RMSE_H vlíc. (m)": rmse(r[g]), "RMSE_H kontr. (m)": rmse(r[c]),
                  "RMSE_V ζ konstanta (m)": np.sqrt(((const - zeta[c]) ** 2).mean()),
                  "RMSE_V ζ rovina (m)": np.sqrt(((np.c_[np.ones(len(c)), x[c], y[c]] @ plane - zeta[c]) ** 2).mean()) if plane is not None else np.nan}
print(pd.DataFrame(rows).T.round(3))
print(f"\\nζ na území: {zeta.min():.2f} až {zeta.max():.2f} m. Kdo zapomene ζ odečíst, má výšky o {zeta.mean():.1f} m vedle.")
fig, ax = plt.subplots(figsize=(7, 6)); sc = ax.scatter(p.sx, p.sy, c=zeta, cmap="viridis"); plt.colorbar(sc, label="ζ = h − H (m)"); ax.set_aspect("equal"); ax.set_title("výšková anomálie na bodech"); plt.show()
''', '''
zeta = (p.HEL - p.VYSKA).values
x, y = (SRC - C0).T
rows = {}
for name, g in LAYOUTS.items():
    c = np.setdiff1d(np.arange(len(p)), g)
    r = (apply(fit(SRC[g], DST[g]), SRC) if len(g) >= 2 else SRC - SRC[g].mean(axis=0) + DST[g].mean(axis=0)) - DST
    const = zeta[g].mean()
    plane = np.linalg.lstsq(np.c_[np.ones(len(g)), x[g], y[g]], zeta[g], rcond=None)[0] if len(g) >= 3 else None
    rows[name] = {"control": len(g), "RMSE_H control (m)": rmse(r[g]), "RMSE_H check (m)": rmse(r[c]),
                  "RMSE_V ζ constant (m)": np.sqrt(((const - zeta[c]) ** 2).mean()),
                  "RMSE_V ζ plane (m)": np.sqrt(((np.c_[np.ones(len(c)), x[c], y[c]] @ plane - zeta[c]) ** 2).mean()) if plane is not None else np.nan}
print(pd.DataFrame(rows).T.round(3))
print(f"\\nζ over the area: {zeta.min():.2f} to {zeta.max():.2f} m. Whoever forgets to subtract ζ has heights off by {zeta.mean():.1f} m.")
fig, ax = plt.subplots(figsize=(7, 6)); sc = ax.scatter(p.sx, p.sy, c=zeta, cmap="viridis"); plt.colorbar(sc, label="ζ = h − H (m)"); ax.set_aspect("equal"); ax.set_title("height anomaly at the points"); plt.show()
''')),
        ("task", t(
            "Které rozmístění je nejlepší polohově a které výškově? Proč body „jen podél linie“ polohu ještě drží, ale rovinu výšek (náklon) neurčí? Co dělá jediný bod ve středu a k čemu se přesto hodí, když máš RTK nebo PPK? Proč by záměna elipsoidické a nadmořské výšky byla v ČR chyba desítek metrů?",
            "Which layout is best for position and which for height? Why do points “along a line only” still hold the position but fail to determine the plane of heights (the tilt)? What does a single point in the centre do, and what is it still good for when you have RTK or PPK? Why would mixing up ellipsoidal and normal height be an error of tens of metres in Czechia?")),
        ("md", t(
            "## 4. Kolik kontrolních bodů?\n\nPřesnost odhadujeme z omezeného počtu kontrolních bodů, takže i samotné RMSE má nejistotu. Vybereme náhodně 12 nebo 30 kontrolních bodů mnohokrát po sobě a podíváme se, jak moc se odhad mění.",
            "## 4. How many check points?\n\nWe estimate accuracy from a limited number of check points, so the RMSE itself is uncertain. We draw 12 or 30 check points at random many times and look at how much the estimate varies.")),
        ("code", t('''
LAYOUT_N = "10 rovnoměrně"    # ◀ parametr: rozmístění vlícovacích bodů
COUNTS = [5, 12, 30]          # ◀ parametr: počty kontrolních bodů
DRAWS = 2000                  # ◀ parametr: počet náhodných výběrů
g = LAYOUTS[LAYOUT_N]; c = np.setdiff1d(np.arange(len(p)), g)
r = np.hypot(*(apply(fit(SRC[g], DST[g]), SRC) - DST).T)[c]
rng = np.random.default_rng(1)
est = {n: np.array([np.sqrt((rng.choice(r, n, replace=False) ** 2).mean()) for _ in range(DRAWS)]) for n in COUNTS if n <= len(r)}
plt.figure(figsize=(8, 3.5))
for n, e in est.items():
    plt.hist(e, 40, alpha=0.5, label=f"{n} kontrolních bodů")
plt.axvline(np.sqrt((r ** 2).mean()), color="k", label=f"všech {len(r)} bodů"); plt.xlabel("odhad RMSE_H (m)"); plt.legend(); plt.show()
print(pd.DataFrame({f"{n} bodů": {"5. percentil": np.percentile(e, 5), "medián": np.median(e), "95. percentil": np.percentile(e, 95)} for n, e in est.items()}).round(3))
''', '''
LAYOUT_N = "10 evenly"        # ◀ parameter: layout of the control points
COUNTS = [5, 12, 30]          # ◀ parameter: numbers of check points
DRAWS = 2000                  # ◀ parameter: number of random draws
g = LAYOUTS[LAYOUT_N]; c = np.setdiff1d(np.arange(len(p)), g)
r = np.hypot(*(apply(fit(SRC[g], DST[g]), SRC) - DST).T)[c]
rng = np.random.default_rng(1)
est = {n: np.array([np.sqrt((rng.choice(r, n, replace=False) ** 2).mean()) for _ in range(DRAWS)]) for n in COUNTS if n <= len(r)}
plt.figure(figsize=(8, 3.5))
for n, e in est.items():
    plt.hist(e, 40, alpha=0.5, label=f"{n} check points")
plt.axvline(np.sqrt((r ** 2).mean()), color="k", label=f"all {len(r)} points"); plt.xlabel("RMSE_H estimate (m)"); plt.legend(); plt.show()
print(pd.DataFrame({f"{n} points": {"5th percentile": np.percentile(e, 5), "median": np.median(e), "95th percentile": np.percentile(e, 95)} for n, e in est.items()}).round(3))
''')),
        ("task", t(
            "Jak široké je rozmezí odhadu RMSE_H (5. až 95. percentil) s 5, 12 a 30 kontrolními body? Proč ASPRS požaduje aspoň 30 kontrolních bodů? Proč musí být kontrolní body rozmístěné po celém území a ne třeba jen u silnice?",
            "How wide is the range of the RMSE_H estimate (5th to 95th percentile) with 5, 12 and 30 check points? Why does ASPRS require at least 30 check points? Why must the check points be spread over the whole area and not, say, only along a road?")),
        ("md", t(
            "## 5. Složitější transformace a málo bodů\n\nHelmertova transformace má 4 parametry, afinní 6 (navíc dvě různá měřítka a zkosení) a polynom 2. stupně 12. Víc parametrů se k vlícovacím bodům přizpůsobí lépe. Jestli to pomůže i na kontrolních bodech, záleží na tom, jestli skutečný rozdíl mezi systémy takový tvar má, a na tom, kolik je vlícovacích bodů. Vlícovací body losujeme náhodně a díváme se na medián i na 90. percentil (nepříznivé losování).",
            "## 5. More complex transformations and few points\n\nThe Helmert transformation has 4 parameters, the affine one 6 (two different scales and a shear on top) and a 2nd-degree polynomial 12. More parameters adapt better to the control points. Whether that also helps on the check points depends on whether the real difference between the systems has such a shape, and on how many control points there are. We draw the control points at random and look at the median and at the 90th percentile (an unlucky draw).")),
        ("code", t('''
KINDS = ["helmert", "afinní", "polynom 2"]
N_GCP = [3, 4, 6, 8, 12, 20, 40]   # ◀ parametr: počty vlícovacích bodů
REPEAT = 200                  # ◀ parametr: počet losování pro každý počet
need = {"helmert": 2, "afinní": 3, "polynom 2": 6}
out = {k: [] for k in KINDS}
for n in N_GCP:
    for k in KINDS:
        vals = []
        for _ in range(REPEAT):
            g = rng.choice(len(p), n, replace=False); c = np.setdiff1d(np.arange(len(p)), g)
            if n < need[k]: break
            vals.append(rmse(apply(fit(SRC[g], DST[g], k), SRC[c]) - DST[c]))
        out[k].append((np.median(vals), np.percentile(vals, 90)) if vals else (np.nan, np.nan))
tab = pd.DataFrame({k: [v[0] for v in out[k]] for k in KINDS}, index=pd.Index(N_GCP, name="vlícovacích bodů"))
p90 = pd.DataFrame({k: [v[1] for v in out[k]] for k in KINDS}, index=tab.index)
print("RMSE_H na kontrolních bodech (m), medián:"); print(tab.round(3)); print("90. percentil:"); print(p90.round(3))
tab.plot(marker="o", logy=True, figsize=(7, 3.8), ylabel="RMSE_H kontrolní body (m)"); plt.show()
''', '''
KINDS = ["helmert", "affine", "polynomial 2"]
N_GCP = [3, 4, 6, 8, 12, 20, 40]   # ◀ parameter: numbers of control points
REPEAT = 200                  # ◀ parameter: number of draws for each number
need = {"helmert": 2, "affine": 3, "polynomial 2": 6}
out = {k: [] for k in KINDS}
for n in N_GCP:
    for k in KINDS:
        vals = []
        for _ in range(REPEAT):
            g = rng.choice(len(p), n, replace=False); c = np.setdiff1d(np.arange(len(p)), g)
            if n < need[k]: break
            vals.append(rmse(apply(fit(SRC[g], DST[g], k), SRC[c]) - DST[c]))
        out[k].append((np.median(vals), np.percentile(vals, 90)) if vals else (np.nan, np.nan))
tab = pd.DataFrame({k: [v[0] for v in out[k]] for k in KINDS}, index=pd.Index(N_GCP, name="control points"))
p90 = pd.DataFrame({k: [v[1] for v in out[k]] for k in KINDS}, index=tab.index)
print("RMSE_H on check points (m), median:"); print(tab.round(3)); print("90th percentile:"); print(p90.round(3))
tab.plot(marker="o", logy=True, figsize=(7, 3.8), ylabel="RMSE_H check points (m)"); plt.show()
''')),
        ("task", t(
            "Která transformace je nejlepší se 3–4 body a která se 40 body? Proč je afinní transformace při všech počtech o něco horší než Helmertova, kdežto polynom 2. stupně je od 8 bodů výrazně lepší? Co to říká o tvaru skutečného rozdílu mezi S-JTSK a UTM? Porovnej 90. percentil polynomu se 6 body s mediánem: jak riskantní je model, který má skoro tolik parametrů jako podmínek? Podle čeho bys v praxi volil model transformace nebo počet parametrů autokalibrace kamery?",
            "Which transformation is best with 3–4 points and which with 40 points? Why is the affine transformation slightly worse than the Helmert one at every count, whereas the 2nd-degree polynomial is clearly better from 8 points on? What does that say about the shape of the real difference between S-JTSK and UTM? Compare the 90th percentile of the polynomial with 6 points with its median: how risky is a model with almost as many parameters as observations? How would you choose the transformation model, or the number of camera self-calibration parameters, in practice?")),
    ]
