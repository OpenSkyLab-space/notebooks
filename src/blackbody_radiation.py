import re

# místa: přípona souboru → scéna Landsatu 8, střed výřezu a popisy
VARIANTS = {
    "": dict(scene="LC08_L1TP_191025_20190626_20190705_01_T1", lon=14.42, lat=50.08, date_cs="26. 6. 2019", date_en="26 June 2019", time="9:51", cc_cs="0,1", cc_en="0.1",
             place_cs="Praha", place_en="Prague", gen_cs="Prahy", win_cs="kolem centra Prahy", win_en="around central Prague",
             when_cs="z vlny veder 26. června 2019", when_en="from the heat wave of 26 June 2019",
             landmarks_cs="Vltavu, velké parky nebo lesy (Stromovka, Hvězda, Krč) a zastavěné plochy s halami",
             landmarks_en="the Vltava river, large parks or forests (Stromovka, Hvězda, Krč) and built-up areas with large halls"),
    "brno": dict(scene="LC08_L1TP_190026_20200808_20200821_01_T1", lon=16.61, lat=49.195, date_cs="8. 8. 2020", date_en="8 Aug 2020", time="9:45", cc_cs="2,5", cc_en="2.5",
                 place_cs="Brno", place_en="Brno", gen_cs="Brna", win_cs="kolem centra Brna", win_en="around central Brno",
                 when_cs="ze slunečného 8. srpna 2020", when_en="from the sunny 8 August 2020",
                 landmarks_cs="Svratku a Brněnskou přehradu, lesy (třeba kolem Kohoutovic) a zastavěné plochy s velkými halami (letiště Tuřany, průmyslové areály)",
                 landmarks_en="the Svratka river and the Brno reservoir, forests (for instance around Kohoutovice) and built-up areas with large halls (Tuřany airport, industrial estates)"),
    "hluboka": dict(scene="LC08_L1TP_191026_20190626_20190705_01_T1", lon=14.46, lat=49.01, date_cs="26. 6. 2019", date_en="26 June 2019", time="9:51", cc_cs="0,2", cc_en="0.2",
                    place_cs="České Budějovice a Hluboká", place_en="České Budějovice and Hluboká", gen_cs="Českých Budějovic a Hluboké",
                    win_cs="mezi Českými Budějovicemi a Hlubokou nad Vltavou", win_en="between České Budějovice and Hluboká nad Vltavou",
                    when_cs="z vlny veder 26. června 2019", when_en="from the heat wave of 26 June 2019",
                    landmarks_cs="Vltavu, Malši a rybníky u Hluboké, lesy a zastavěné plochy s velkými halami na okraji Českých Budějovic",
                    landmarks_en="the Vltava and Malše rivers and the fishponds near Hluboká, forests and built-up areas with large halls on the edge of České Budějovice"),
}


def meta(P):
    return {
        "version": "1.0",
        "minutes": 45,
        "title": {"cs": "Teplota " + P["gen_cs"] + " z Landsatu 8: Planckův zákon v praxi", "en": "The temperature of " + P["place_en"] + " from Landsat 8: Planck's law in practice"},
        "visual": {"cs": "Záření černého tělesa", "en": "Blackbody radiation"},
        "lead": {
            "cs": "Vizuál ukazuje Planckův zákon, Wienův posun, čtvrtou mocninu Stefanova–Boltzmannova zákona a vliv emisivity. Tady stejné vzorce použiješ na skutečný termální snímek Landsatu 8 " + P["when_cs"] + " a z digitálních čísel spočítáš teplotu povrchu " + P["gen_cs"] + ".",
            "en": "The visual shows Planck's law, Wien's shift, the fourth power of the Stefan–Boltzmann law and the role of emissivity. Here you apply the same formulas to a real Landsat 8 thermal image " + P["when_en"] + " and turn digital numbers into the surface temperature of " + P["place_en"] + ".",
        },
        "goal": {
            "cs": "převést termální pásmo Landsatu 8 z DN na zář a jasovou teplotu, opravit ji o emisivitu, odhadnout chybu ze špatné emisivity a odrazu oblohy a ukázat, proč družice hledají malé požáry ve 3,9 µm.",
            "en": "convert the Landsat 8 thermal band from DN to radiance and brightness temperature, correct it for emissivity, estimate the error from a wrong emissivity and from sky reflection, and show why satellites look for small fires at 3.9 µm.",
        },
        "data": {
            "cs": f"Landsat 8 OLI/TIRS, Collection 1 Level-1, scéna `{P['scene']}` ({P['date_cs']}, {P['time']} UTC, oblačnost {P['cc_cs']} %), pásma B4, B5 a B10 a soubor MTL s kalibračními konstantami z veřejného archivu Google Cloud. Čte se jen výřez 16 × 16 km {P['win_cs']} (asi 3 MB).",
            "en": f"Landsat 8 OLI/TIRS, Collection 1 Level-1, scene `{P['scene']}` ({P['date_en']}, {P['time']} UTC, cloud cover {P['cc_en']} %), bands B4, B5 and B10 and the MTL file with calibration constants from the Google Cloud public archive. Only a 16 × 16 km window {P['win_en']} is read (about 3 MB).",
        },
        "sources": {
            "cs": [
                "Landsat 8 OLI/TIRS Collection 1 Level-1, U.S. Geological Survey; veřejný archiv Google Cloud (`gcp-public-data-landsat`). Data USGS jsou volná bez omezení užití (public domain), s uvedením zdroje.",
                "Převod DN na zář a jasovou teplotu: USGS (2019). *Landsat 8 (L8) Data Users Handbook*, verze 5.0, kap. 5.",
                "Emisivita z NDVI: Sobrino, J. A., Jiménez-Muñoz, J. C., Paolini, L. (2004). Land surface temperature retrieval from LANDSAT TM 5. *Remote Sensing of Environment* 90, 434–440. https://doi.org/10.1016/j.rse.2004.02.003",
                "Detekce požárů ve 3,9 a 11 µm: Giglio, L., Schroeder, W., Justice, C. O. (2016). The collection 6 MODIS active fire detection algorithm and fire products. *Remote Sensing of Environment* 178, 31–41. https://doi.org/10.1016/j.rse.2016.02.054",
            ],
            "en": [
                "Landsat 8 OLI/TIRS Collection 1 Level-1, U.S. Geological Survey; Google Cloud public archive (`gcp-public-data-landsat`). USGS data are free of use restrictions (public domain), with attribution.",
                "DN to radiance and brightness temperature: USGS (2019). *Landsat 8 (L8) Data Users Handbook*, version 5.0, ch. 5.",
                "Emissivity from NDVI: Sobrino, J. A., Jiménez-Muñoz, J. C., Paolini, L. (2004). Land surface temperature retrieval from LANDSAT TM 5. *Remote Sensing of Environment* 90, 434–440. https://doi.org/10.1016/j.rse.2004.02.003",
                "Fire detection at 3.9 and 11 µm: Giglio, L., Schroeder, W., Justice, C. O. (2016). The collection 6 MODIS active fire detection algorithm and fire products. *Remote Sensing of Environment* 178, 31–41. https://doi.org/10.1016/j.rse.2016.02.054",
            ],
        },
    }


def cells(t, P):
    out = [
        ("md", t("## 1. Příprava", "## 1. Setup")),
        ("code", t('''
%pip install -q rasterio
''', '''
%pip install -q rasterio
''')),
        ("code", t('''
import numpy as np, requests
import matplotlib.pyplot as plt
import rasterio
from rasterio.windows import from_bounds
from pyproj import Transformer
from scipy.constants import h, c, k, sigma

def planck(lam_um, T):
    """Spektrální zář černého tělesa ve W·m⁻²·sr⁻¹·µm⁻¹ pro vlnovou délku v µm a teplotu v K."""
    lam = np.asarray(lam_um) * 1e-6
    return 2 * h * c**2 / lam**5 / np.expm1(h * c / (lam * k * T)) * 1e-6

def planck_inv(lam_um, L):
    """Jasová teplota (K): teplota černého tělesa, které by mělo zář L na vlnové délce lam_um."""
    lam = lam_um * 1e-6
    return h * c / (lam * k) / np.log1p(2 * h * c**2 / lam**5 / (np.asarray(L) * 1e6))
''', '''
import numpy as np, requests
import matplotlib.pyplot as plt
import rasterio
from rasterio.windows import from_bounds
from pyproj import Transformer
from scipy.constants import h, c, k, sigma

def planck(lam_um, T):
    """Blackbody spectral radiance in W·m⁻²·sr⁻¹·µm⁻¹ for wavelength in µm and temperature in K."""
    lam = np.asarray(lam_um) * 1e-6
    return 2 * h * c**2 / lam**5 / np.expm1(h * c / (lam * k * T)) * 1e-6

def planck_inv(lam_um, L):
    """Brightness temperature (K): the temperature of a blackbody with radiance L at wavelength lam_um."""
    lam = lam_um * 1e-6
    return h * c / (lam * k) / np.log1p(2 * h * c**2 / lam**5 / (np.asarray(L) * 1e6))
''')),
        ("md", t(
            "## 2. Planckův zákon, Wien a čtvrtá mocnina",
            "## 2. Planck's law, Wien and the fourth power")),
        ("code", t('''
T_list = [300, 600, 900, 5772]      # ◀ parametr: teploty v K (krajina, kamna, požár, povrch Slunce)
lam = np.logspace(-1, 2, 2000)      # 0,1 až 100 µm
fig, ax = plt.subplots(figsize=(9, 4))
for T in T_list:
    L = planck(lam, T)
    ax.loglog(lam, L, label=f"{T} K")
    lmax = 2897.77 / T                                   # Wienův posunovací zákon, µm
    M = np.trapezoid(L, lam) * np.pi                     # zář → zářivý tok z plochy (W·m⁻²)
    print(f"{T:5d} K: maximum {lmax:6.2f} µm, tok {M:10.4g} W/m² (σT⁴ = {sigma * T**4:10.4g}), "
          f"zář v 10,9 µm {planck(10.9, T):8.3g} W·m⁻²·sr⁻¹·µm⁻¹")
ax.axvspan(8, 14, color="tab:red", alpha=0.08, label="termální okno 8–14 µm")
ax.set(xlabel="vlnová délka (µm)", ylabel="spektrální zář (W·m⁻²·sr⁻¹·µm⁻¹)", ylim=(1e-4, 1e8))
ax.legend(); plt.show()
''', '''
T_list = [300, 600, 900, 5772]      # ◀ parameter: temperatures in K (landscape, stove, fire, solar surface)
lam = np.logspace(-1, 2, 2000)      # 0.1 to 100 µm
fig, ax = plt.subplots(figsize=(9, 4))
for T in T_list:
    L = planck(lam, T)
    ax.loglog(lam, L, label=f"{T} K")
    lmax = 2897.77 / T                                   # Wien's displacement law, µm
    M = np.trapezoid(L, lam) * np.pi                     # radiance → radiant exitance (W·m⁻²)
    print(f"{T:5d} K: peak {lmax:6.2f} µm, exitance {M:10.4g} W/m² (σT⁴ = {sigma * T**4:10.4g}), "
          f"radiance at 10.9 µm {planck(10.9, T):8.3g} W·m⁻²·sr⁻¹·µm⁻¹")
ax.axvspan(8, 14, color="tab:red", alpha=0.08, label="thermal window 8–14 µm")
ax.set(xlabel="wavelength (µm)", ylabel="spectral radiance (W·m⁻²·sr⁻¹·µm⁻¹)", ylim=(1e-4, 1e8))
ax.legend(); plt.show()
''')),
        ("task", t(
            "Kolikrát vzroste celkový tok a kolikrát zář v 10,9 µm, když teplotu zdvojnásobíš z 300 na 600 K? Proč se obě čísla liší? Spočítej také, o kolik procent víc vyzáří asfalt o 45 °C než tráva o 25 °C.",
            "How many times do the total exitance and the radiance at 10.9 µm increase when you double the temperature from 300 to 600 K? Why do the two numbers differ? Also compute how many per cent more asphalt at 45 °C emits than grass at 25 °C.")),
        ("md", t(
            "## 3. Skutečná scéna: z DN na jasovou teplotu\n\nPásmo B10 (10,6–11,2 µm) ukládá digitální čísla (DN). Soubor MTL obsahuje lineární převod na zář, L = M · DN + A, a konstanty K1, K2, kterými se zář převede na jasovou teplotu, T = K2 / ln(K1 / L + 1). Je to Planckův zákon zjednodušený na jedno pásmo.",
            "## 3. A real scene: from DN to brightness temperature\n\nBand B10 (10.6–11.2 µm) stores digital numbers (DN). The MTL file holds the linear conversion to radiance, L = M · DN + A, and the constants K1, K2 that turn radiance into brightness temperature, T = K2 / ln(K1 / L + 1). It is Planck's law simplified for one band.")),
        ("code", t('''
SCENE = "@SCENE@"
BASE = f"https://storage.googleapis.com/gcp-public-data-landsat/LC08/01/@PATH@/@ROW@/{SCENE}/{SCENE}"
mtl = dict(l.strip().split(" = ") for l in requests.get(BASE + "_MTL.txt", timeout=60).text.splitlines() if " = " in l)
num = lambda key: float(mtl[key])

lon, lat, half = @LON@, @LAT@, 8000      # ◀ parametr: střed výřezu (°) a poloviční šířka (m)

def read_band(b):
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2):
        with rasterio.open(f"/vsicurl/{BASE}_B{b}.TIF") as r:
            x, y = Transformer.from_crs(4326, r.crs, always_xy=True).transform(lon, lat)
            return r.read(1, window=from_bounds(x - half, y - half, x + half, y + half, r.transform)).astype(float)

dn10 = read_band(10)
L10 = num("RADIANCE_MULT_BAND_10") * dn10 + num("RADIANCE_ADD_BAND_10")
BT = num("K2_CONSTANT_BAND_10") / np.log(num("K1_CONSTANT_BAND_10") / L10 + 1)
print("datum a čas:", mtl["DATE_ACQUIRED"], mtl["SCENE_CENTER_TIME"].strip('"'), "| výška Slunce", mtl["SUN_ELEVATION"], "°")
print(f"DN {dn10.min():.0f}–{dn10.max():.0f} → zář {L10.min():.2f}–{L10.max():.2f} W·m⁻²·sr⁻¹·µm⁻¹ → "
      f"jasová teplota {BT.min() - 273.15:.1f} až {BT.max() - 273.15:.1f} °C")
print(f"kontrola Planckem pro 10,9 µm: {planck_inv(10.9, np.median(L10)) - 273.15:.1f} °C vs. K1/K2: {np.median(BT) - 273.15:.1f} °C")
''', '''
SCENE = "@SCENE@"
BASE = f"https://storage.googleapis.com/gcp-public-data-landsat/LC08/01/@PATH@/@ROW@/{SCENE}/{SCENE}"
mtl = dict(l.strip().split(" = ") for l in requests.get(BASE + "_MTL.txt", timeout=60).text.splitlines() if " = " in l)
num = lambda key: float(mtl[key])

lon, lat, half = @LON@, @LAT@, 8000      # ◀ parameter: window centre (°) and half-width (m)

def read_band(b):
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", GDAL_HTTP_MAX_RETRY=5, GDAL_HTTP_RETRY_DELAY=2):
        with rasterio.open(f"/vsicurl/{BASE}_B{b}.TIF") as r:
            x, y = Transformer.from_crs(4326, r.crs, always_xy=True).transform(lon, lat)
            return r.read(1, window=from_bounds(x - half, y - half, x + half, y + half, r.transform)).astype(float)

dn10 = read_band(10)
L10 = num("RADIANCE_MULT_BAND_10") * dn10 + num("RADIANCE_ADD_BAND_10")
BT = num("K2_CONSTANT_BAND_10") / np.log(num("K1_CONSTANT_BAND_10") / L10 + 1)
print("date and time:", mtl["DATE_ACQUIRED"], mtl["SCENE_CENTER_TIME"].strip('"'), "| sun elevation", mtl["SUN_ELEVATION"], "°")
print(f"DN {dn10.min():.0f}–{dn10.max():.0f} → radiance {L10.min():.2f}–{L10.max():.2f} W·m⁻²·sr⁻¹·µm⁻¹ → "
      f"brightness temperature {BT.min() - 273.15:.1f} to {BT.max() - 273.15:.1f} °C")
print(f"check with Planck at 10.9 µm: {planck_inv(10.9, np.median(L10)) - 273.15:.1f} °C vs. K1/K2: {np.median(BT) - 273.15:.1f} °C")
''')),
        ("code", t('''
fig, ax = plt.subplots(figsize=(7.5, 6.5))
im = ax.imshow(BT - 273.15, cmap="inferno")
fig.colorbar(im, ax=ax, label="jasová teplota B10 (°C)")
ax.set_title(f"@PLACE_CS@, {mtl['DATE_ACQUIRED']}, Landsat 8 B10\\n(pixel 30 m, převzorkováno ze 100 m)")
ax.axis("off"); plt.show()
''', '''
fig, ax = plt.subplots(figsize=(7.5, 6.5))
im = ax.imshow(BT - 273.15, cmap="inferno")
fig.colorbar(im, ax=ax, label="B10 brightness temperature (°C)")
ax.set_title(f"@PLACE_EN@, {mtl['DATE_ACQUIRED']}, Landsat 8 B10\\n(30 m pixel, resampled from 100 m)")
ax.axis("off"); plt.show()
''')),
        ("task", t(
            "Najdi na mapě @LANDMARKS_CS@. Jaké jasové teploty mají? Proč je rozdíl mezi vodou a střechami hal kolem poledne tak velký? Proč není jasová teplota totéž co teplota povrchu?",
            "Find @LANDMARKS_EN@ on the map. What brightness temperatures do they have? Why is the difference between the water and hall roofs so large around noon? Why is brightness temperature not the same as surface temperature?")),
        ("md", t(
            "## 4. Emisivita\n\nReálné povrchy vyzařují méně než černé těleso: L = ε · B(T). Emisivitu odhadneme z NDVI zjednodušenou metodou prahů podle Sobrina a kol. (2004): holý povrch 0,97, plná vegetace 0,99, mezi tím podle podílu vegetace s opravou na vícenásobné odrazy mezi rostlinami a půdou. Vodě (NDVI < 0) dáme typickou hodnotu 0,991. Odraz oblohy a atmosféru zatím zanedbáme.",
            "## 4. Emissivity\n\nReal surfaces emit less than a blackbody: L = ε · B(T). We estimate emissivity from NDVI with a simplified threshold method after Sobrino et al. (2004): bare surface 0.97, full vegetation 0.99, in between according to the vegetation fraction with a correction for multiple scattering between plants and soil. Water (NDVI < 0) gets a typical value of 0.991. Sky reflection and the atmosphere are ignored for now.")),
        ("code", t('''
sun = np.sin(np.radians(num("SUN_ELEVATION")))
refl = lambda b: (num(f"REFLECTANCE_MULT_BAND_{b}") * read_band(b) + num(f"REFLECTANCE_ADD_BAND_{b}")) / sun
red, nir = refl(4), refl(5)
ndvi = (nir - red) / (nir + red)

eps_soil, eps_veg, eps_water = 0.97, 0.99, 0.991     # ◀ parametr: emisivity
ndvi_s, ndvi_v = 0.2, 0.5
pv = np.clip((ndvi - ndvi_s) / (ndvi_v - ndvi_s), 0, 1) ** 2          # podíl vegetace v pixelu
# poslední člen: dutinový efekt (vícenásobné odrazy mezi rostlinami a půdou), tvarový faktor 0,55
eps = np.where(ndvi < 0, eps_water, np.where(ndvi < ndvi_s, eps_soil, eps_veg * pv + eps_soil * (1 - pv) + (1 - eps_soil) * (1 - pv) * 0.55 * eps_veg))
LST = planck_inv(10.9, L10 / eps)            # teplota tělesa, které by s emisivitou ε mělo naměřenou zář
d = LST - BT
print(f"emisivita {eps.min():.3f}–{eps.max():.3f}; oprava LST − BT: medián {np.median(d):.2f} K, rozsah {d.min():.2f} až {d.max():.2f} K")
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
a = ax[0].imshow(ndvi, cmap="RdYlGn", vmin=-0.2, vmax=0.8); fig.colorbar(a, ax=ax[0], label="NDVI")
b = ax[1].imshow(d, cmap="viridis"); fig.colorbar(b, ax=ax[1], label="LST − BT (K)")
for x in ax: x.axis("off")
plt.show()
''', '''
sun = np.sin(np.radians(num("SUN_ELEVATION")))
refl = lambda b: (num(f"REFLECTANCE_MULT_BAND_{b}") * read_band(b) + num(f"REFLECTANCE_ADD_BAND_{b}")) / sun
red, nir = refl(4), refl(5)
ndvi = (nir - red) / (nir + red)

eps_soil, eps_veg, eps_water = 0.97, 0.99, 0.991     # ◀ parameter: emissivities
ndvi_s, ndvi_v = 0.2, 0.5
pv = np.clip((ndvi - ndvi_s) / (ndvi_v - ndvi_s), 0, 1) ** 2          # vegetation fraction of the pixel
# last term: cavity effect (multiple scattering between plants and soil), shape factor 0.55
eps = np.where(ndvi < 0, eps_water, np.where(ndvi < ndvi_s, eps_soil, eps_veg * pv + eps_soil * (1 - pv) + (1 - eps_soil) * (1 - pv) * 0.55 * eps_veg))
LST = planck_inv(10.9, L10 / eps)            # temperature of a body that would give the measured radiance with emissivity ε
d = LST - BT
print(f"emissivity {eps.min():.3f}–{eps.max():.3f}; correction LST − BT: median {np.median(d):.2f} K, range {d.min():.2f} to {d.max():.2f} K")
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
a = ax[0].imshow(ndvi, cmap="RdYlGn", vmin=-0.2, vmax=0.8); fig.colorbar(a, ax=ax[0], label="NDVI")
b = ax[1].imshow(d, cmap="viridis"); fig.colorbar(b, ax=ax[1], label="LST − BT (K)")
for x in ax: x.axis("off")
plt.show()
''')),
        ("code", t('''
# o kolik se splete senzor, když povrch s naměřenou zář má jinou emisivitu, než předpokládáme
T_true = 273.15 + 40          # ◀ parametr: skutečná teplota povrchu v K
for eps_true in (0.98, 0.95, 0.92, 0.85):
    L = eps_true * planck(10.9, T_true)
    print(f"ε = {eps_true:.2f}: jasová teplota {planck_inv(10.9, L) - 273.15:5.1f} °C, chyba {planck_inv(10.9, L) - T_true:+5.2f} K")
''', '''
# how far off the sensor is when a surface has a different emissivity than assumed
T_true = 273.15 + 40          # ◀ parameter: true surface temperature in K
for eps_true in (0.98, 0.95, 0.92, 0.85):
    L = eps_true * planck(10.9, T_true)
    print(f"ε = {eps_true:.2f}: brightness temperature {planck_inv(10.9, L) - 273.15:5.1f} °C, error {planck_inv(10.9, L) - T_true:+5.2f} K")
''')),
        ("task", t(
            "Kde je oprava o emisivitu největší a proč? Zhruba o kolik kelvinů se senzor splete na každou setinu emisivity? Změň `eps_soil` na 0,95 (beton, asfalt) a sleduj, jak se změní oprava v zastavěných plochách.",
            "Where is the emissivity correction largest and why? Roughly how many kelvin is the sensor off for each hundredth of emissivity? Change `eps_soil` to 0.95 (concrete, asphalt) and watch how the correction changes in built-up areas.")),
        ("md", t(
            "## 5. Odraz oblohy\n\nPovrch s emisivitou ε odráží 1 − ε dlouhovlnného záření, které na něj svítí z oblohy. Jasná obloha je v 10 µm velmi studená, zatažená má zhruba teplotu základny oblačnosti. Senzor dostane L = ε · B(T) + (1 − ε) · B(T_obloha).",
            "## 5. Sky reflection\n\nA surface with emissivity ε reflects 1 − ε of the longwave radiation coming from the sky. A clear sky is very cold at 10 µm, an overcast sky has roughly the temperature of the cloud base. The sensor receives L = ε · B(T) + (1 − ε) · B(T_sky).")),
        ("code", t('''
T_surf = 273.15 + 27           # ◀ parametr: teplota povrchu
for name, eps_m in [("tráva", 0.98), ("beton", 0.92), ("zoxidovaný plech", 0.6), ("lesklý hliník", 0.05)]:
    row = []
    for T_sky_c in (-40, -10, 10, 27):       # jasná obloha … nízká oblačnost … obloha teplá jako povrch
        L = eps_m * planck(10.9, T_surf) + (1 - eps_m) * planck(10.9, 273.15 + T_sky_c)
        row.append(f"{planck_inv(10.9, L) - 273.15:6.1f}")
    print(f"{name:18s} ε={eps_m:.2f}: jasová teplota při obloze −40/−10/+10/+27 °C:", " ".join(row), "°C")
''', '''
T_surf = 273.15 + 27           # ◀ parameter: surface temperature
for name, eps_m in [("grass", 0.98), ("concrete", 0.92), ("oxidised sheet metal", 0.6), ("polished aluminium", 0.05)]:
    row = []
    for T_sky_c in (-40, -10, 10, 27):       # clear sky … low cloud … sky as warm as the surface
        L = eps_m * planck(10.9, T_surf) + (1 - eps_m) * planck(10.9, 273.15 + T_sky_c)
        row.append(f"{planck_inv(10.9, L) - 273.15:6.1f}")
    print(f"{name:20s} ε={eps_m:.2f}: brightness temperature with sky −40/−10/+10/+27 °C:", " ".join(row), "°C")
''')),
        ("task", t(
            "Proč lesklý plech pod jasnou oblohou vypadá v termokameře mrazivě studený, i když má 27 °C? Proč při obloze stejně teplé jako povrch nehraje emisivita žádnou roli? Za jakého počasí bys proto plánoval termální snímkování střech?",
            "Why does polished sheet metal under a clear sky look freezing cold in a thermal camera although it is at 27 °C? Why does emissivity not matter at all when the sky is as warm as the surface? In what weather would you therefore plan thermal imaging of roofs?")),
        ("md", t(
            "## 6. Požár menší než pixel\n\nPixel je směs: podíl p hoří při teplotě požáru, zbytek má teplotu pozadí. Jako pozadí vezmeme medián skutečné jasové teploty z výřezu (@PLACE_CS@) a porovnáme pásmo 3,9 µm (požárová pásma MODIS a VIIRS leží mezi 3,7 a 4,1 µm) s pásmem 10,9 µm.",
            "## 6. A fire smaller than a pixel\n\nA pixel is a mixture: a fraction p burns at the fire temperature, the rest has the background temperature. As background we take the median real brightness temperature of the window (@PLACE_EN@) and compare the 3.9 µm band (the fire bands of MODIS and VIIRS lie between 3.7 and 4.1 µm) with the 10.9 µm band.")),
        ("code", t('''
T_fire = 900                     # ◀ parametr: teplota požáru v K
T_bg = float(np.median(BT))
p = np.logspace(-5, -1, 200)     # podíl požáru v pixelu
fig, ax = plt.subplots(figsize=(8, 3.8))
for lam_b in (3.9, 10.9):
    L = p * planck(lam_b, T_fire) + (1 - p) * planck(lam_b, T_bg)
    ax.semilogx(p * 100, planck_inv(lam_b, L) - T_bg, label=f"{lam_b} µm")
ax.axhline(10, color="gray", ls=":")
ax.set(xlabel="podíl požáru v pixelu (%)", ylabel="zvýšení jasové teploty (K)", title=f"pozadí {T_bg - 273.15:.1f} °C, požár {T_fire} K")
ax.legend(); plt.show()
for lam_b in (3.9, 10.9):
    L = p * planck(lam_b, T_fire) + (1 - p) * planck(lam_b, T_bg)
    p10 = p[np.argmax(planck_inv(lam_b, L) - T_bg > 10)]
    print(f"{lam_b} µm: o 10 K teplejší pixel už při podílu {p10 * 100:.3f} % = {p10 * 1e6:.0f} m² z pixelu 1 × 1 km")
''', '''
T_fire = 900                     # ◀ parameter: fire temperature in K
T_bg = float(np.median(BT))
p = np.logspace(-5, -1, 200)     # fire fraction of the pixel
fig, ax = plt.subplots(figsize=(8, 3.8))
for lam_b in (3.9, 10.9):
    L = p * planck(lam_b, T_fire) + (1 - p) * planck(lam_b, T_bg)
    ax.semilogx(p * 100, planck_inv(lam_b, L) - T_bg, label=f"{lam_b} µm")
ax.axhline(10, color="gray", ls=":")
ax.set(xlabel="fire fraction of the pixel (%)", ylabel="brightness temperature increase (K)", title=f"background {T_bg - 273.15:.1f} °C, fire {T_fire} K")
ax.legend(); plt.show()
for lam_b in (3.9, 10.9):
    L = p * planck(lam_b, T_fire) + (1 - p) * planck(lam_b, T_bg)
    p10 = p[np.argmax(planck_inv(lam_b, L) - T_bg > 10)]
    print(f"{lam_b} µm: a pixel 10 K warmer already at a fraction of {p10 * 100:.3f} % = {p10 * 1e6:.0f} m² of a 1 × 1 km pixel")
''')),
        ("task", t(
            "Při jakém podílu požáru se pixel ohřeje o 10 K ve 3,9 µm a při jakém v 10,9 µm? Jakou plochu to je v pixelu MODIS 1 × 1 km? Vysvětli rozdíl Wienovým zákonem. Proč algoritmy ve dne hlídají i odražené Slunce ve 3,9 µm?",
            "At what fire fraction does the pixel warm by 10 K at 3.9 µm and at 10.9 µm? What area is that within a 1 × 1 km MODIS pixel? Explain the difference with Wien's law. Why do daytime algorithms also watch for reflected sunlight at 3.9 µm?")),
        ("task", t(
        "+ Porovnej se spolužákem, který spustil notebook pro jiné místo a den: jaký rozsah jasových teplot vyšel jemu? Kolik z rozdílu může jít na vrub jiného dne a hodiny, jiné výšky Slunce a jiného složení krajiny?",
        "+ Compare with a classmate who ran the notebook for another place and day: what range of brightness temperatures did they get? How much of the difference can be due to another day and hour, another sun elevation and a different landscape?")),
    ]
    tokens = {"@SCENE@": P["scene"], "@PATH@": P["scene"][10:13], "@ROW@": P["scene"][13:16], "@LON@": str(P["lon"]), "@LAT@": str(P["lat"]),
              "@PLACE_CS@": P["place_cs"], "@PLACE_EN@": P["place_en"], "@LANDMARKS_CS@": P["landmarks_cs"], "@LANDMARKS_EN@": P["landmarks_en"]}
    res = []
    for kind, text in out:
        for k, v in tokens.items():
            text = text.replace(k, v)
        assert not re.search(r"@[A-Z0-9_]+@", text), text[:80]
        res.append((kind, text))
    return res
