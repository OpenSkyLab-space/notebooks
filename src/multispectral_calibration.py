import re

# verze: přípona souboru → kamera a dvojice snímků z ukázkových dat MicaSense (panel před letem, snímek z letu)
VARIANTS = {
    "": dict(folder="REDEDGE-MX", panel="IMG_0001", flight="IMG_0020", cam="MicaSense RedEdge",
             scene_cs="nad silnicí, parkovištěm, trávníkem a stromy", scene_en="over a road, a car park, a lawn and trees",
             when_cs="IMG_0001 (panel RP06, 6. 4. 2022 18:50 UTC) a IMG_0020 (let o 7 minut později), 47,70° s. š., 122,14° z. d.",
             when_en="IMG_0001 (RP06 panel, 6 April 2022 18:50 UTC) and IMG_0020 (flight 7 minutes later), 47.70° N, 122.14° W.",
             regions_cs='{"silnice": (slice(250, 550), slice(365, 395)), "trávník": (slice(820, 920), slice(550, 850)), "stromy": (slice(150, 450), slice(650, 1000))}',
             regions_en='{"road": (slice(250, 550), slice(365, 395)), "lawn": (slice(820, 920), slice(550, 850)), "trees": (slice(150, 450), slice(650, 1000))}',
             regs_cs="silnice, trávníku a stromů", regs_en="road, lawn and trees"),
    "altum": dict(folder="ALTUM", panel="IMG_0000", flight="IMG_0021", cam="MicaSense Altum",
                  scene_cs="nad křižovatkou silnic, lesem, stromořadím a travnatým polem", scene_en="over a road junction, a forest, a row of trees and a grass field",
                  when_cs="IMG_0000 (panel RP06, 6. 4. 2022 20:00 UTC) a IMG_0021 (let o 2 minuty později asi 100 m nad terénem), 47,70° s. š., 122,14° z. d. Altum má i termální pásmo 6, které tento notebook nepoužívá.",
                  when_en="IMG_0000 (RP06 panel, 6 April 2022 20:00 UTC) and IMG_0021 (flight 2 minutes later about 100 m above ground), 47.70° N, 122.14° W. The Altum also has a thermal band 6, which this notebook does not use.",
                  regions_cs='{"silnice": (slice(500, 840), slice(660, 750)), "travnaté pole": (slice(200, 800), slice(1550, 1950)), "les": (slice(100, 800), slice(40, 500))}',
                  regions_en='{"road": (slice(500, 840), slice(660, 750)), "grass field": (slice(200, 800), slice(1550, 1950)), "forest": (slice(100, 800), slice(40, 500))}',
                  regs_cs="silnice, travnatého pole a lesa", regs_en="road, grass field and forest"),
    "altum_pt": dict(folder="ALTUM-PT", panel="IMG_0000", flight="IMG_0010", cam="MicaSense Altum-PT",
                     scene_cs="nad silnicí, ovocným sadem, suchou loukou a fóliovníkem", scene_en="over a road, an orchard, a dry meadow and a polytunnel",
                     when_cs="IMG_0000 (panel RP06, 15. 8. 2022 19:16 UTC) a IMG_0010 (let o 3 minuty později asi 97 m nad terénem), 48,51° s. š., 122,42° z. d. Altum-PT má i panchromatické pásmo 6 a termální pásmo 7, které tento notebook nepoužívá.",
                     when_en="IMG_0000 (RP06 panel, 15 August 2022 19:16 UTC) and IMG_0010 (flight 3 minutes later about 97 m above ground), 48.51° N, 122.42° W. The Altum-PT also has a panchromatic band 6 and a thermal band 7, which this notebook does not use.",
                     regions_cs='{"silnice": (slice(1140, 1260), slice(1570, 1650)), "suchá louka": (slice(100, 500), slice(1120, 1500)), "sad": (slice(20, 640), slice(20, 560))}',
                     regions_en='{"road": (slice(1140, 1260), slice(1570, 1650)), "dry meadow": (slice(100, 500), slice(1120, 1500)), "orchard": (slice(20, 640), slice(20, 560))}',
                     regs_cs="silnice, suché louky a sadu", regs_en="road, dry meadow and orchard"),
}


def meta(P):
    return {
        "version": "1.0",
        "minutes": 45,
        "title": {"cs": "Kalibrace multispektrální kamery: od DN k odrazivosti na skutečných snímcích", "en": "Calibrating a multispectral camera: from DN to reflectance on real images"},
        "visual": {"cs": "Kalibrace multispektrální kamery", "en": "Calibrating a multispectral camera"},
        "lead": {
            "cs": "Vizuál ukazuje, co s odrazivostí udělá mrak, náklon dronu, vinětace a malý panel. Tady projdeš celý řetězec na skutečných snímcích kamery " + P["cam"] + ": snímek kalibračního panelu před letem a snímek z letu " + P["scene_cs"] + ". Všechny potřebné údaje (černá úroveň, vinětace, kalibrační koeficienty, odrazivost panelu, údaje senzoru osvětlení DLS 2) jsou uložené přímo v souborech TIFF.",
            "en": "The visual shows what a cloud, drone tilt, vignetting and a small panel do to reflectance. Here you go through the whole chain on real images from a " + P["cam"] + " camera: an image of the calibration panel before the flight and an image from the flight " + P["scene_en"] + ". Everything you need (black level, vignetting, calibration coefficients, panel reflectance, readings of the DLS 2 light sensor) is stored directly in the TIFF files.",
        },
        "goal": {
            "cs": "převést DN na radianci krok za krokem, z panelu spočítat kalibrační koeficient, porovnat odrazivost jen z panelu, jen z DLS a z obou dohromady, ukázat vliv vinětace, saturace a náklonu senzoru DLS a spočítat NDVI ze sesazených pásem.",
            "en": "convert DN to radiance step by step, compute the calibration coefficient from the panel, compare reflectance from the panel only, from the DLS only and from both, show the effect of vignetting, saturation and DLS tilt, and compute NDVI from co-registered bands.",
        },
        "data": {
            "cs": "dva snímky (5 multispektrálních pásem) kamery " + P["cam"] + " s DLS 2 z ukázkových dat MicaSense (repozitář micasense/imageprocessing, licence MIT): " + P["when_cs"],
            "en": "two captures (5 multispectral bands) from a " + P["cam"] + " camera with DLS 2 from the MicaSense sample data (repository micasense/imageprocessing, MIT licence): " + P["when_en"],
        },
        "sources": {
            "cs": [
                "Snímky a postup radiometrické kalibrace: MicaSense, Inc. (2017–2023). *imageprocessing* (licence MIT), https://github.com/micasense/imageprocessing, soubory data/" + P["folder"] + "/" + P["panel"] + "_*.tif a " + P["flight"] + "_*.tif a micasense/image.py (vinětace, radiance, odrazivost).",
                "MicaSense: RedEdge Camera Radiometric Calibration Model; Use of Calibrated Reflectance Panels for MicaSense Data (podpora MicaSense).",
                "Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20(13), 2653–2662.",
                "Přehled kalibrace multispektrálních a hyperspektrálních kamer na UAV: Aasen, H., Honkavaara, E., Lucieer, A., Zarco-Tejada, P. J. (2018). Quantitative remote sensing at ultra-high resolution with UAV spectroscopy. *Remote Sensing* 10(7), 1091.",
            ],
            "en": [
                "Images and the radiometric calibration procedure: MicaSense, Inc. (2017–2023). *imageprocessing* (MIT licence), https://github.com/micasense/imageprocessing, files data/" + P["folder"] + "/" + P["panel"] + "_*.tif and " + P["flight"] + "_*.tif and micasense/image.py (vignetting, radiance, reflectance).",
                "MicaSense: RedEdge Camera Radiometric Calibration Model; Use of Calibrated Reflectance Panels for MicaSense Data (MicaSense support).",
                "Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20(13), 2653–2662.",
                "Overview of UAV multispectral calibration: Aasen, H., Honkavaara, E., Lucieer, A., Zarco-Tejada, P. J. (2018). Quantitative remote sensing at ultra-high resolution with UAV spectroscopy. *Remote Sensing* 10(7), 1091.",
            ],
        },
    }


def cells(t, P):
    out = [
        ("md", t("## 1. Příprava a snímky", "## 1. Setup and images")),
        ("code", t('''
import re, io, time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage as ndi
from matplotlib.path import Path

BASE = "https://media.githubusercontent.com/media/micasense/imageprocessing/master/data/@FOLDER@/"
def fetch(name, tries=5):
    for i in range(tries):
        try:
            r = requests.get(BASE + name, timeout=120); r.raise_for_status(); return r.content
        except requests.RequestException as e:
            print(name, type(e).__name__, "– zkusím znovu"); time.sleep(3 * (i + 1))
    raise RuntimeError("Snímky se nepodařilo stáhnout.")

def xmp_reader(raw):
    x = raw[raw.find(b"<x:xmpmeta"): raw.find(b"</x:xmpmeta>")].decode()
    def get(tag):
        m = re.search(rf"<{tag}>(.*?)</{tag}>", x, re.S)
        if not m: return None
        v = m.group(1)
        if "<rdf:li>" in v:
            return [float(s) for li in re.findall(r"<rdf:li>\\s*([^<]+?)\\s*</rdf:li>", v) for s in li.split(",")]
        try: return float(v)
        except ValueError: return v.strip()
    return get

def load(name):
    """Načte jedno pásmo: pole DN a slovník metadat z EXIF a XMP."""
    raw = fetch(name); im = Image.open(io.BytesIO(raw)); ex = im.getexif(); sub = ex.get_ifd(0x8769); g = xmp_reader(raw)
    m = dict(band=g("Camera:BandName"), wl=g("Camera:CentralWavelength"), exposure=float(sub[33434]), gain=sub.get(34867, 100) / 100,
             black=float(np.mean(ex[50714])), bits=ex[258], cal=g("MicaSense:RadiometricCalibration"),
             vig_c=g("Camera:VignettingCenter"), vig_p=g("Camera:VignettingPolynomial"),
             vig_2d=g("Camera:VignettingPolynomial2D"), vig_e=g("Camera:VignettingPolynomial2DName"),
             albedo=g("Camera:Albedo"), area=g("Camera:ReflectArea"), time=ex[306],
             E_h=g("DLS:HorizontalIrradiance"), E_sensor=g("DLS:SpectralIrradiance"), E_dir=g("DLS:DirectIrradiance"),
             E_sc=g("DLS:ScatteredIrradiance"), sun_el=g("DLS:SolarElevation"), sun_az=g("DLS:SolarAzimuth"),
             pitch=g("DLS:Pitch"), roll=g("DLS:Roll"))
    for k in ("E_h", "E_sensor", "E_dir", "E_sc"):
        m[k] = m[k] * 0.01            # DLS 2 ukládá µW/cm²/nm, převod na W/m²/nm (faktor 0,01 jako v knihovně MicaSense)
    return np.array(im).astype(float), m

def vig_factor(m, shape):
    """Násobek korekce vinětace V pro každý pixel: radiální polynom, nebo u novějších kamer 2D polynom (jako micasense/image.py)."""
    y, x = np.indices(shape)
    if m["vig_c"] is not None:
        return 1 / np.polyval(list(m["vig_p"])[::-1] + [1.0], np.hypot(x - m["vig_c"][0], y - m["vig_c"][1]))
    xv, yv = x / shape[1], y / shape[0]
    return 1 / sum(c * xv ** m["vig_e"][2 * i] * yv ** m["vig_e"][2 * i + 1] for i, c in enumerate(m["vig_2d"]))

def panel_shift(a, c):
    """Celopixelový posun snímku c proti a fázovou korelací."""
    f = np.fft.fft2(a - a.mean()) * np.conj(np.fft.fft2(c - c.mean())); cc = np.abs(np.fft.ifft2(f / (np.abs(f) + 1e-9)))
    dy, dx = np.unravel_index(cc.argmax(), cc.shape)
    return (dy - a.shape[0] if dy > a.shape[0] // 2 else dy, dx - a.shape[1] if dx > a.shape[1] // 2 else dx)

PANEL = {b: load(f"@PANEL@_{b}.tif") for b in range(1, 6)}
FLIGHT = {b: load(f"@FLIGHT@_{b}.tif") for b in range(1, 6)}
for b in PANEL:                     # když software kamery panel v některém pásmu nenašel, posuneme oblast z pásma 1
    if PANEL[b][1]["area"] is None:
        dy, dx = panel_shift(PANEL[1][0], PANEL[b][0])
        PANEL[b][1]["area"] = list((np.array(PANEL[1][1]["area"]).reshape(-1, 2) - [dx, dy]).ravel())
        print(f"pásmo {b}: oblast panelu chybí v metadatech, odvozena z pásma 1 posunem o {dx}, {dy} px")
    if PANEL[b][1]["albedo"] is None:          # chybí i odrazivost panelu: odhad interpolací podle vlnové délky z ostatních pásem
        known = sorted((PANEL[k][1]["wl"], PANEL[k][1]["albedo"]) for k in PANEL if PANEL[k][1]["albedo"] is not None)
        PANEL[b][1]["albedo"] = float(np.interp(PANEL[b][1]["wl"], *zip(*known)))
        print(f"pásmo {b}: odrazivost panelu chybí v metadatech, odhad interpolací {PANEL[b][1]['albedo']:.3f}")
print(pd.DataFrame({PANEL[b][1]["band"]: {"λ (nm)": PANEL[b][1]["wl"], "expozice panel (ms)": 1000 * PANEL[b][1]["exposure"],
      "expozice let (ms)": 1000 * FLIGHT[b][1]["exposure"], "odrazivost panelu": PANEL[b][1]["albedo"]} for b in PANEL}).round(3))
print("panel:", PANEL[1][1]["time"], " let:", FLIGHT[1][1]["time"], " (UTC)")
''', '''
import re, io, time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from scipy import ndimage as ndi
from matplotlib.path import Path

BASE = "https://media.githubusercontent.com/media/micasense/imageprocessing/master/data/@FOLDER@/"
def fetch(name, tries=5):
    for i in range(tries):
        try:
            r = requests.get(BASE + name, timeout=120); r.raise_for_status(); return r.content
        except requests.RequestException as e:
            print(name, type(e).__name__, "– retrying"); time.sleep(3 * (i + 1))
    raise RuntimeError("Could not download the images.")

def xmp_reader(raw):
    x = raw[raw.find(b"<x:xmpmeta"): raw.find(b"</x:xmpmeta>")].decode()
    def get(tag):
        m = re.search(rf"<{tag}>(.*?)</{tag}>", x, re.S)
        if not m: return None
        v = m.group(1)
        if "<rdf:li>" in v:
            return [float(s) for li in re.findall(r"<rdf:li>\\s*([^<]+?)\\s*</rdf:li>", v) for s in li.split(",")]
        try: return float(v)
        except ValueError: return v.strip()
    return get

def load(name):
    """Load one band: the DN array and a dictionary of EXIF and XMP metadata."""
    raw = fetch(name); im = Image.open(io.BytesIO(raw)); ex = im.getexif(); sub = ex.get_ifd(0x8769); g = xmp_reader(raw)
    m = dict(band=g("Camera:BandName"), wl=g("Camera:CentralWavelength"), exposure=float(sub[33434]), gain=sub.get(34867, 100) / 100,
             black=float(np.mean(ex[50714])), bits=ex[258], cal=g("MicaSense:RadiometricCalibration"),
             vig_c=g("Camera:VignettingCenter"), vig_p=g("Camera:VignettingPolynomial"),
             vig_2d=g("Camera:VignettingPolynomial2D"), vig_e=g("Camera:VignettingPolynomial2DName"),
             albedo=g("Camera:Albedo"), area=g("Camera:ReflectArea"), time=ex[306],
             E_h=g("DLS:HorizontalIrradiance"), E_sensor=g("DLS:SpectralIrradiance"), E_dir=g("DLS:DirectIrradiance"),
             E_sc=g("DLS:ScatteredIrradiance"), sun_el=g("DLS:SolarElevation"), sun_az=g("DLS:SolarAzimuth"),
             pitch=g("DLS:Pitch"), roll=g("DLS:Roll"))
    for k in ("E_h", "E_sensor", "E_dir", "E_sc"):
        m[k] = m[k] * 0.01            # DLS 2 stores µW/cm²/nm; convert to W/m²/nm (factor 0.01 as in the MicaSense library)
    return np.array(im).astype(float), m

def vig_factor(m, shape):
    """Vignetting correction factor V for every pixel: a radial polynomial or, for newer cameras, a 2D polynomial (as in micasense/image.py)."""
    y, x = np.indices(shape)
    if m["vig_c"] is not None:
        return 1 / np.polyval(list(m["vig_p"])[::-1] + [1.0], np.hypot(x - m["vig_c"][0], y - m["vig_c"][1]))
    xv, yv = x / shape[1], y / shape[0]
    return 1 / sum(c * xv ** m["vig_e"][2 * i] * yv ** m["vig_e"][2 * i + 1] for i, c in enumerate(m["vig_2d"]))

def panel_shift(a, c):
    """Whole-pixel shift of image c relative to a by phase correlation."""
    f = np.fft.fft2(a - a.mean()) * np.conj(np.fft.fft2(c - c.mean())); cc = np.abs(np.fft.ifft2(f / (np.abs(f) + 1e-9)))
    dy, dx = np.unravel_index(cc.argmax(), cc.shape)
    return (dy - a.shape[0] if dy > a.shape[0] // 2 else dy, dx - a.shape[1] if dx > a.shape[1] // 2 else dx)

PANEL = {b: load(f"@PANEL@_{b}.tif") for b in range(1, 6)}
FLIGHT = {b: load(f"@FLIGHT@_{b}.tif") for b in range(1, 6)}
for b in PANEL:                     # if the camera software did not find the panel in some band, shift the area from band 1
    if PANEL[b][1]["area"] is None:
        dy, dx = panel_shift(PANEL[1][0], PANEL[b][0])
        PANEL[b][1]["area"] = list((np.array(PANEL[1][1]["area"]).reshape(-1, 2) - [dx, dy]).ravel())
        print(f"band {b}: panel area missing in the metadata, derived from band 1 by a shift of {dx}, {dy} px")
    if PANEL[b][1]["albedo"] is None:          # the panel reflectance is missing too: estimate by interpolation in wavelength from the other bands
        known = sorted((PANEL[k][1]["wl"], PANEL[k][1]["albedo"]) for k in PANEL if PANEL[k][1]["albedo"] is not None)
        PANEL[b][1]["albedo"] = float(np.interp(PANEL[b][1]["wl"], *zip(*known)))
        print(f"band {b}: panel reflectance missing in the metadata, interpolated estimate {PANEL[b][1]['albedo']:.3f}")
print(pd.DataFrame({PANEL[b][1]["band"]: {"λ (nm)": PANEL[b][1]["wl"], "exposure panel (ms)": 1000 * PANEL[b][1]["exposure"],
      "exposure flight (ms)": 1000 * FLIGHT[b][1]["exposure"], "panel reflectance": PANEL[b][1]["albedo"]} for b in PANEL}).round(3))
print("panel:", PANEL[1][1]["time"], " flight:", FLIGHT[1][1]["time"], " (UTC)")
''')),
        ("md", t(
            "## 2. Od DN k radianci\n\n"
            "Model MicaSense (stejný jako v knihovně `micasense/image.py`):\n\n"
            "L = V(r) · R(y) · (DN − černá úroveň) / (zisk · expozice) · a₁ / 2¹⁶\n\n"
            "- černá úroveň: signál bez světla (tag BlackLevel),\n"
            "- V(r) = 1 / (1 + k₀r + … + k₅r⁶): korekce vinětace podle vzdálenosti r od středu vinětace (novější kamery ukládají místo toho 2D polynom v souřadnicích x, y),\n"
            "- R(y) = 1 / (1 + a₂ y / expozice − a₃ y): korekce podle řádku (snímač se čte po řádcích),\n"
            "- a₁: radiometrický kalibrační koeficient z výroby. Výsledek je spektrální radiance ve W/m²/sr/nm.",
            "## 2. From DN to radiance\n\n"
            "The MicaSense model (the same as in the library `micasense/image.py`):\n\n"
            "L = V(r) · R(y) · (DN − black level) / (gain · exposure) · a₁ / 2¹⁶\n\n"
            "- black level: the signal without light (BlackLevel tag),\n"
            "- V(r) = 1 / (1 + k₀r + … + k₅r⁶): vignetting correction by the distance r from the vignetting centre (newer cameras store a 2D polynomial in x, y instead),\n"
            "- R(y) = 1 / (1 + a₂ y / exposure − a₃ y): correction by row (the sensor is read out row by row),\n"
            "- a₁: the factory radiometric calibration coefficient. The result is spectral radiance in W/m²/sr/nm.")),
        ("code", t('''
def radiance(dn, m, vignette=True):
    y, x = np.indices(dn.shape)
    a1, a2, a3 = m["cal"]
    V = vig_factor(m, dn.shape) if vignette else 1.0
    R = 1 / (1 + a2 * y / m["exposure"] - a3 * y)
    return np.clip(V * R * (dn - m["black"]), 0, None) / (m["gain"] * m["exposure"]) * a1 / 2 ** m["bits"]

BAND = 4                      # ◀ parametr: pásmo 1 modré, 2 zelené, 3 červené, 4 NIR, 5 red edge
dn, m = FLIGHT[BAND]
y, x = np.indices(dn.shape)
V = vig_factor(m, dn.shape)
fig, ax = plt.subplots(1, 3, figsize=(14, 3.6))
ax[0].imshow(dn, cmap="gray"); ax[0].set_title(f"DN, {m['band']}")
im = ax[1].imshow(V, cmap="magma"); plt.colorbar(im, ax=ax[1]); ax[1].set_title("násobek vinětace V")
im = ax[2].imshow(radiance(dn, m), cmap="gray"); plt.colorbar(im, ax=ax[2]); ax[2].set_title("radiance (W/m²/sr/nm)")
for a in ax: a.axis("off")
plt.show()
sat = (dn >= 2 ** m["bits"] - 16).mean() * 100
print(f"{m['band']}: černá úroveň {m['black']:.0f} DN, expozice {m['exposure'] * 1000:.2f} ms, zisk {m['gain']:.0f}×")
print(f"vinětace: střed ×{V.min():.2f}, roh ×{V[0, 0]:.2f};  saturovaných pixelů {sat:.2f} %")
''', '''
def radiance(dn, m, vignette=True):
    y, x = np.indices(dn.shape)
    a1, a2, a3 = m["cal"]
    V = vig_factor(m, dn.shape) if vignette else 1.0
    R = 1 / (1 + a2 * y / m["exposure"] - a3 * y)
    return np.clip(V * R * (dn - m["black"]), 0, None) / (m["gain"] * m["exposure"]) * a1 / 2 ** m["bits"]

BAND = 4                      # ◀ parameter: band 1 blue, 2 green, 3 red, 4 NIR, 5 red edge
dn, m = FLIGHT[BAND]
y, x = np.indices(dn.shape)
V = vig_factor(m, dn.shape)
fig, ax = plt.subplots(1, 3, figsize=(14, 3.6))
ax[0].imshow(dn, cmap="gray"); ax[0].set_title(f"DN, {m['band']}")
im = ax[1].imshow(V, cmap="magma"); plt.colorbar(im, ax=ax[1]); ax[1].set_title("vignetting factor V")
im = ax[2].imshow(radiance(dn, m), cmap="gray"); plt.colorbar(im, ax=ax[2]); ax[2].set_title("radiance (W/m²/sr/nm)")
for a in ax: a.axis("off")
plt.show()
sat = (dn >= 2 ** m["bits"] - 16).mean() * 100
print(f"{m['band']}: black level {m['black']:.0f} DN, exposure {m['exposure'] * 1000:.2f} ms, gain {m['gain']:.0f}×")
print(f"vignetting: centre ×{V.min():.2f}, corner ×{V[0, 0]:.2f};  saturated pixels {sat:.2f} %")
''')),
        ("task", t(
            "Projdi pásma 1 až 5. O kolik procent zesiluje korekce vinětace signál v rohu snímku a ve kterém pásmu nejvíc? Kolik procent pixelů je saturovaných a kde ve snímku jsou? Proč saturovaný pixel nejde opravit žádnou kalibrací a co s tím při letu uděláš?",
            "Go through bands 1 to 5. By what percentage does the vignetting correction boost the signal in the corner of the image, and in which band most? What percentage of pixels is saturated and where in the image are they? Why can no calibration fix a saturated pixel, and what do you do about it during the flight?")),
        ("md", t(
            "## 3. Kalibrační panel\n\nV metadatech snímku panelu je oblast uprostřed panelu, kterou na snímku našel software kamery (ReflectArea, čtyři rohy v pixelech), a jeho odrazivost v daném pásmu (Albedo) z kalibračního listu. Z průměrné radiance panelu L_p plyne koeficient k = ρ_panel / L_p a odrazivost každého pixelu ρ = k · L.",
            "## 3. The calibration panel\n\nThe metadata of the panel image contain an area in the middle of the panel that the camera software found in the image (ReflectArea, four corners in pixels), and its reflectance in the given band (Albedo) from the calibration sheet. The mean radiance of the panel L_p gives the coefficient k = ρ_panel / L_p and the reflectance of every pixel ρ = k · L.")),
        ("code", t('''
SHRINK = 1.0                  # ◀ parametr: zmenšení oblasti z metadat (1 = celá oblast, 0,3 = jen střed)
GROW_PX = 0                   # ◀ parametr: oblast naopak zvětšit o tolik pixelů (napodobí nepřesné vyznačení panelu)

def panel_mask(m, shrink=SHRINK, grow=GROW_PX):
    xy = np.array(m["area"]).reshape(-1, 2); c = xy.mean(axis=0)
    xy = c + (xy - c) * shrink + np.sign(xy - c) * grow
    yy, xx = np.indices(PANEL[1][0].shape)
    return Path(xy).contains_points(np.c_[xx.ravel(), yy.ravel()]).reshape(PANEL[1][0].shape)

rows = {}
for b, (dn, m) in PANEL.items():
    L = radiance(dn, m); msk = panel_mask(m)
    rows[m["band"]] = {"pixelů": msk.sum(), "L_p": L[msk].mean(), "variabilita (%)": 100 * L[msk].std() / L[msk].mean(),
                       "ρ_panel": m["albedo"], "k = ρ/L_p": m["albedo"] / L[msk].mean()}
panel_tab = pd.DataFrame(rows).T
print(panel_tab.round(4))
dn, m = PANEL[3]
xy = np.array(m["area"]).reshape(-1, 2)
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].imshow(radiance(dn, m), cmap="gray"); ax[0].contour(panel_mask(m), [0.5], colors="r"); ax[0].set_title("snímek panelu, červené pásmo")
ax[1].imshow(radiance(dn, m), cmap="gray"); ax[1].contour(panel_mask(m), [0.5], colors="r")
ax[1].set_xlim(xy[:, 0].min() - 60, xy[:, 0].max() + 60); ax[1].set_ylim(xy[:, 1].max() + 60, xy[:, 1].min() - 60); ax[1].set_title("detail")
plt.show()
''', '''
SHRINK = 1.0                  # ◀ parameter: shrink the area from the metadata (1 = the whole area, 0.3 = only the centre)
GROW_PX = 0                   # ◀ parameter: enlarge the area by this many pixels instead (imitates a sloppily marked panel)

def panel_mask(m, shrink=SHRINK, grow=GROW_PX):
    xy = np.array(m["area"]).reshape(-1, 2); c = xy.mean(axis=0)
    xy = c + (xy - c) * shrink + np.sign(xy - c) * grow
    yy, xx = np.indices(PANEL[1][0].shape)
    return Path(xy).contains_points(np.c_[xx.ravel(), yy.ravel()]).reshape(PANEL[1][0].shape)

rows = {}
for b, (dn, m) in PANEL.items():
    L = radiance(dn, m); msk = panel_mask(m)
    rows[m["band"]] = {"pixels": msk.sum(), "L_p": L[msk].mean(), "variability (%)": 100 * L[msk].std() / L[msk].mean(),
                       "ρ_panel": m["albedo"], "k = ρ/L_p": m["albedo"] / L[msk].mean()}
panel_tab = pd.DataFrame(rows).T
print(panel_tab.round(4))
dn, m = PANEL[3]
xy = np.array(m["area"]).reshape(-1, 2)
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].imshow(radiance(dn, m), cmap="gray"); ax[0].contour(panel_mask(m), [0.5], colors="r"); ax[0].set_title("panel image, red band")
ax[1].imshow(radiance(dn, m), cmap="gray"); ax[1].contour(panel_mask(m), [0.5], colors="r")
ax[1].set_xlim(xy[:, 0].min() - 60, xy[:, 0].max() + 60); ax[1].set_ylim(xy[:, 1].max() + 60, xy[:, 1].min() - 60); ax[1].set_title("detail")
plt.show()
''')),
        ("task", t(
            "Nastav GROW_PX na 30, 60 a 90 (podívej se na detail, kam oblast sahá): jak se změní průměrná radiance panelu a koeficient k? O kolik procent by se tím posunula odrazivost celé mapy? Pak nastav SHRINK = 0,2: co se stane s variabilitou a proč? Proč se do průměru berou jen pixely ze středu panelu a proč musí být panel na snímku dost velký (kolik pixelů tu má)?",
            "Set GROW_PX to 30, 60 and 90 (look at the detail to see how far the area reaches): how do the mean panel radiance and the coefficient k change? By what percentage would that shift the reflectance of the whole map? Then set SHRINK = 0.2: what happens to the variability and why? Why are only pixels from the centre of the panel averaged, and why must the panel be large enough in the image (how many pixels does it have here)?")),
        ("md", t(
            "## 4. Senzor osvětlení DLS a jeho náklon\n\n"
            "DLS měří ozáření na svou horní plochu. Když se dron nakloní ke Slunci, dopadá na senzor víc přímého záření, než kolik dopadá na vodorovný terén. DLS 2 proto rozkládá ozáření na přímou a rozptýlenou složku a přepočítává ho na vodorovnou plochu: E_vod = E_přímé · sin(výška Slunce) + E_rozptýlené.",
            "## 4. The DLS light sensor and its tilt\n\n"
            "The DLS measures irradiance on its top surface. When the drone tilts towards the Sun, the sensor receives more direct radiation than the horizontal ground does. DLS 2 therefore splits irradiance into a direct and a diffuse component and converts it to a horizontal surface: E_hor = E_direct · sin(solar elevation) + E_diffuse.")),
        ("code", t('''
TILT = 10                     # ◀ parametr: náklon senzoru DLS (°)
rows = {}
for b in range(1, 6):
    for name, (dn, m) in [("panel", PANEL[b]), ("let", FLIGHT[b])]:
        rows[(m["band"], name)] = {"E senzor": m["E_sensor"], "E vodorovné": m["E_h"], "přímé·sin(h)+rozptýlené": m["E_dir"] * np.sin(m["sun_el"]) + m["E_sc"],
                                   "náklon (°)": np.degrees(np.hypot(m["pitch"], m["roll"]))}
print(pd.DataFrame(rows).T.round(3))
m = FLIGHT[3][1]; el = m["sun_el"]
for direction, sign in [("ke Slunci", 1), ("od Slunce", -1)]:
    cos_g = np.sin(el) * np.cos(np.radians(TILT)) + sign * np.cos(el) * np.sin(np.radians(TILT))
    E_tilt = m["E_dir"] * cos_g + m["E_sc"]
    print(f"výška Slunce {np.degrees(el):.1f}°, náklon {TILT}° {direction}: senzor změří {E_tilt / m['E_h']:.3f}× vodorovné ozáření (bez korekce chyba odrazivosti {100 * (m['E_h'] / E_tilt - 1):+.1f} %)")
''', '''
TILT = 10                     # ◀ parameter: tilt of the DLS sensor (°)
rows = {}
for b in range(1, 6):
    for name, (dn, m) in [("panel", PANEL[b]), ("flight", FLIGHT[b])]:
        rows[(m["band"], name)] = {"E sensor": m["E_sensor"], "E horizontal": m["E_h"], "direct·sin(h)+diffuse": m["E_dir"] * np.sin(m["sun_el"]) + m["E_sc"],
                                   "tilt (°)": np.degrees(np.hypot(m["pitch"], m["roll"]))}
print(pd.DataFrame(rows).T.round(3))
m = FLIGHT[3][1]; el = m["sun_el"]
for direction, sign in [("towards the Sun", 1), ("away from the Sun", -1)]:
    cos_g = np.sin(el) * np.cos(np.radians(TILT)) + sign * np.cos(el) * np.sin(np.radians(TILT))
    E_tilt = m["E_dir"] * cos_g + m["E_sc"]
    print(f"solar elevation {np.degrees(el):.1f}°, tilt {TILT}° {direction}: the sensor measures {E_tilt / m['E_h']:.3f}× the horizontal irradiance (without correction a reflectance error of {100 * (m['E_h'] / E_tilt - 1):+.1f} %)")
''')),
        ("task", t(
            "O kolik procent se mezi snímkem panelu a snímkem z letu změnilo vodorovné ozáření (časy snímků vypsala první buňka)? Jak velkou chybu odrazivosti způsobí náklon 10° a 20° ke Slunci a od Slunce? Proč je chyba při nízkém Slunci větší a proč pomáhá, když je rozptýlené složky hodně (zataženo)?",
            "By what percentage did the horizontal irradiance change between the panel image and the flight image (the first cell printed the image times)? How large a reflectance error does a tilt of 10° and 20° towards and away from the Sun cause? Why is the error larger with a low Sun, and why does a large diffuse component (overcast) help?")),
        ("md", t(
            "## 5. Tři způsoby kalibrace\n\n"
            "- **jen panel:** ρ = k · L. Předpokládá, že se osvětlení od snímku panelu nezměnilo.\n"
            "- **jen DLS:** ρ = π · L / E_vod. Spoléhá na tovární kalibraci kamery i DLS.\n"
            "- **panel + DLS:** ρ = k · L · E_vod(panel) / E_vod(snímek). Panel určí absolutní úroveň, DLS sleduje změny osvětlení.\n\n"
            "Kontrola: když metodu „jen DLS“ použijeme na samotný panel, měli bychom dostat jeho známou odrazivost.",
            "## 5. Three ways to calibrate\n\n"
            "- **panel only:** ρ = k · L. Assumes the illumination has not changed since the panel image.\n"
            "- **DLS only:** ρ = π · L / E_hor. Relies on the factory calibration of both the camera and the DLS.\n"
            "- **panel + DLS:** ρ = k · L · E_hor(panel) / E_hor(image). The panel sets the absolute level, the DLS tracks changes in illumination.\n\n"
            "Check: when we apply the “DLS only” method to the panel itself, we should get its known reflectance.")),
        ("code", t('''
def shift_to(ref, img):
    """Celopixelový posun img vůči ref fázovou korelací gradientů (pásma má každé svůj objektiv)."""
    g = lambda a: np.hypot(*np.gradient(ndi.gaussian_filter(a, 1.5)))
    F = np.fft.fft2(g(ref)) * np.conj(np.fft.fft2(g(img))); c = np.fft.ifft2(F / (np.abs(F) + 1e-12)).real
    dy, dx = np.unravel_index(c.argmax(), c.shape)
    return (dy - c.shape[0] if dy > c.shape[0] // 2 else dy, dx - c.shape[1] if dx > c.shape[1] // 2 else dx)

L_fl = {b: radiance(*FLIGHT[b]) for b in FLIGHT}
shifts = {b: shift_to(L_fl[3], L_fl[b]) for b in FLIGHT}
L_al = {b: ndi.shift(L_fl[b], shifts[b], order=0, mode="nearest") for b in FLIGHT}
REGIONS = @REGIONS_CS@  # ◀ parametr: oblasti (řádky, sloupce)
res = {}
for b in FLIGHT:
    mp, mf = PANEL[b][1], FLIGHT[b][1]; k = panel_tab.loc[mp["band"], "k = ρ/L_p"]
    methods = {"jen panel": k * L_al[b], "jen DLS": np.pi * L_al[b] / mf["E_h"], "panel + DLS": k * L_al[b] * mp["E_h"] / mf["E_h"]}
    for meth, rho in methods.items():
        for reg, (r, c) in REGIONS.items():
            res[(reg, meth, mp["band"])] = np.median(rho[r, c])
    res[("panel (kontrola)", "jen DLS", mp["band"])] = np.pi * panel_tab.loc[mp["band"], "L_p"] / mp["E_h"]
RHO = pd.Series(res).unstack()[["Blue", "Green", "Red", "Red edge", "NIR"]]
print(RHO.round(3))
fig, ax = plt.subplots(figsize=(11, 4.5))
rgb = np.dstack([L_al[3], L_al[2], L_al[1]]); ax.imshow(np.clip(rgb / np.percentile(rgb, 99), 0, 1))
for reg, (r, c) in REGIONS.items():
    ax.add_patch(plt.Rectangle((c.start, r.start), c.stop - c.start, r.stop - r.start, fill=False, color="yellow")); ax.text(c.start, r.start - 8, reg, color="yellow")
ax.set_title("snímek z letu (sesazená pásma), oblasti pro porovnání"); ax.axis("off"); plt.show()
''', '''
def shift_to(ref, img):
    """Whole-pixel shift of img relative to ref by phase correlation of gradients (each band has its own lens)."""
    g = lambda a: np.hypot(*np.gradient(ndi.gaussian_filter(a, 1.5)))
    F = np.fft.fft2(g(ref)) * np.conj(np.fft.fft2(g(img))); c = np.fft.ifft2(F / (np.abs(F) + 1e-12)).real
    dy, dx = np.unravel_index(c.argmax(), c.shape)
    return (dy - c.shape[0] if dy > c.shape[0] // 2 else dy, dx - c.shape[1] if dx > c.shape[1] // 2 else dx)

L_fl = {b: radiance(*FLIGHT[b]) for b in FLIGHT}
shifts = {b: shift_to(L_fl[3], L_fl[b]) for b in FLIGHT}
L_al = {b: ndi.shift(L_fl[b], shifts[b], order=0, mode="nearest") for b in FLIGHT}
REGIONS = @REGIONS_EN@  # ◀ parameter: regions (rows, columns)
res = {}
for b in FLIGHT:
    mp, mf = PANEL[b][1], FLIGHT[b][1]; k = panel_tab.loc[mp["band"], "k = ρ/L_p"]
    methods = {"panel only": k * L_al[b], "DLS only": np.pi * L_al[b] / mf["E_h"], "panel + DLS": k * L_al[b] * mp["E_h"] / mf["E_h"]}
    for meth, rho in methods.items():
        for reg, (r, c) in REGIONS.items():
            res[(reg, meth, mp["band"])] = np.median(rho[r, c])
    res[("panel (check)", "DLS only", mp["band"])] = np.pi * panel_tab.loc[mp["band"], "L_p"] / mp["E_h"]
RHO = pd.Series(res).unstack()[["Blue", "Green", "Red", "Red edge", "NIR"]]
print(RHO.round(3))
fig, ax = plt.subplots(figsize=(11, 4.5))
rgb = np.dstack([L_al[3], L_al[2], L_al[1]]); ax.imshow(np.clip(rgb / np.percentile(rgb, 99), 0, 1))
for reg, (r, c) in REGIONS.items():
    ax.add_patch(plt.Rectangle((c.start, r.start), c.stop - c.start, r.stop - r.start, fill=False, color="yellow")); ax.text(c.start, r.start - 8, reg, color="yellow")
ax.set_title("flight image (co-registered bands), regions for comparison"); ax.axis("off"); plt.show()
''')),
        ("task", t(
            "Jakou odrazivost panelu dá metoda „jen DLS“ a o kolik procent se liší od kalibračního listu? Která metoda je tu nejspolehlivější a proč? O kolik se liší „jen panel“ a „panel + DLS“ a čím to je (vrať se ke kroku 4)? Odpovídají křivky @REGS_CS@ tomu, co znáš ze spektrálních signatur?",
            "What panel reflectance does the “DLS only” method give, and by what percentage does it differ from the calibration sheet? Which method is the most reliable here and why? How much do “panel only” and “panel + DLS” differ, and why (go back to step 4)? Do the curves of the @REGS_EN@ match what you know from spectral signatures?")),
        ("md", t(
            "## 6. NDVI a co s ním dělá kalibrace\n\nNDVI = (ρ_NIR − ρ_R) / (ρ_NIR + ρ_R). Porovnáme NDVI z radiance (bez kalibrace), z kalibrace „panel + DLS“ a z kalibrace bez korekce vinětace.",
            "## 6. NDVI and what calibration does to it\n\nNDVI = (ρ_NIR − ρ_R) / (ρ_NIR + ρ_R). We compare NDVI from radiance (no calibration), from the “panel + DLS” calibration, and from a calibration without vignetting correction.")),
        ("code", t('''
NDVI_MIN = 0.5                # ◀ parametr: práh NDVI pro „vegetaci“
def calibrated(b, vignette=True):
    mp, mf = PANEL[b][1], FLIGHT[b][1]; k = panel_tab.loc[mp["band"], "k = ρ/L_p"]
    L = ndi.shift(radiance(*FLIGHT[b], vignette=vignette), shifts[b], order=0, mode="nearest")
    return k * L * mp["E_h"] / mf["E_h"]
nd = lambda nir, red: (nir - red) / (nir + red + 1e-9)
variants = {"z radiance": nd(L_al[4], L_al[3]), "panel + DLS": nd(calibrated(4), calibrated(3)),
            "panel + DLS bez vinětace": nd(calibrated(4, False), calibrated(3, False))}
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
for a, (name, v) in zip(ax, variants.items()):
    im = a.imshow(v, cmap="RdYlGn", vmin=-0.2, vmax=0.95); a.set_title(name); a.axis("off")
plt.colorbar(im, ax=ax, shrink=0.8); plt.show()
print(pd.DataFrame({name: {**{reg: np.median(v[r, c]) for reg, (r, c) in REGIONS.items()}, f"podíl NDVI ≥ {NDVI_MIN} (%)": 100 * (v >= NDVI_MIN).mean()}
                    for name, v in variants.items()}).round(3))
''', '''
NDVI_MIN = 0.5                # ◀ parameter: NDVI threshold for “vegetation”
def calibrated(b, vignette=True):
    mp, mf = PANEL[b][1], FLIGHT[b][1]; k = panel_tab.loc[mp["band"], "k = ρ/L_p"]
    L = ndi.shift(radiance(*FLIGHT[b], vignette=vignette), shifts[b], order=0, mode="nearest")
    return k * L * mp["E_h"] / mf["E_h"]
nd = lambda nir, red: (nir - red) / (nir + red + 1e-9)
variants = {"from radiance": nd(L_al[4], L_al[3]), "panel + DLS": nd(calibrated(4), calibrated(3)),
            "panel + DLS without vignetting": nd(calibrated(4, False), calibrated(3, False))}
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
for a, (name, v) in zip(ax, variants.items()):
    im = a.imshow(v, cmap="RdYlGn", vmin=-0.2, vmax=0.95); a.set_title(name); a.axis("off")
plt.colorbar(im, ax=ax, shrink=0.8); plt.show()
print(pd.DataFrame({name: {**{reg: np.median(v[r, c]) for reg, (r, c) in REGIONS.items()}, f"share NDVI ≥ {NDVI_MIN} (%)": 100 * (v >= NDVI_MIN).mean()}
                    for name, v in variants.items()}).round(3))
''')),
        ("task", t(
            "Proč se NDVI z radiance tolik liší od NDVI z odrazivosti, i když jde o stejný snímek? Proč vynechání korekce vinětace NDVI skoro nezmění, ale odrazivost v rozích ano (srovnej s krokem 2)? Jak by se změnil podíl vegetace, kdyby někdo prahoval NDVI z radiance?",
            "Why does NDVI from radiance differ so much from NDVI from reflectance even though it is the same image? Why does skipping the vignetting correction hardly change NDVI while it does change reflectance in the corners (compare with step 2)? How would the vegetation share change if someone thresholded NDVI from radiance?")),
        ("task", t(
            "+ Spolužáci mohou mít notebook pro jinou kameru (RedEdge-MX, Altum, Altum-PT). Porovnejte koeficient k z panelu, změnu ozáření mezi panelem a letem a rozdíl metod „jen DLS“ a „panel + DLS“. Liší se víc kamery, nebo podmínky osvětlení při letu?",
            "+ Classmates may have the notebook for another camera (RedEdge-MX, Altum, Altum-PT). Compare the panel coefficient k, the change in irradiance between the panel and the flight, and the difference between the “DLS only” and “panel + DLS” methods. Do the cameras differ more, or the lighting conditions during the flight?")),
    ]
    tokens = {"@FOLDER@": P["folder"], "@PANEL@": P["panel"], "@FLIGHT@": P["flight"], "@REGIONS_CS@": P["regions_cs"], "@REGIONS_EN@": P["regions_en"],
              "@REGS_CS@": P["regs_cs"], "@REGS_EN@": P["regs_en"]}
    res = []
    for kind, text in out:
        for k, v in tokens.items():
            text = text.replace(k, v)
        assert not re.search(r"@[A-Z0-9_]+@", text), text[:80]
        res.append((kind, text))
    return res
