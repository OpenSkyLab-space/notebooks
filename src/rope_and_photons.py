META = {
    "version": "1.0",
    "minutes": 40,
    "title": {"cs": "Fotony v pásmech Sentinelu-2", "en": "Photons in the Sentinel-2 bands"},
    "visual": {"cs": "Švihadlo a fotony", "en": "Rope and photons"},
    "lead": {
        "cs": "Ve vizuálu jsi viděl, že u vlny na laně platí c = λ · f a že energii nese rozkmit i frekvence. U světla je to jinak: energii jednoho fotonu určuje jen frekvence, E = h · f, jas záření je počet fotonů. Tady to spočítáš pro skutečná pásma družice Sentinel-2.",
        "en": "In the visual you saw that a wave on a rope obeys c = λ · f and that both amplitude and frequency carry energy. Light is different: the energy of one photon depends only on frequency, E = h · f, and brightness is the number of photons. Here you compute it for the real bands of the Sentinel-2 satellite.",
    },
    "goal": {
        "cs": "z metadat skutečné scény Sentinel-2 spočítat frekvenci, energii fotonu a tok fotonů v každém pásmu a odvodit z nich, jaký detektor které pásmo potřebuje.",
        "en": "from the metadata of a real Sentinel-2 scene, compute the frequency, photon energy and photon flux in each band and work out which detector each band needs.",
    },
    "data": {
        "cs": "metadata produktu Sentinel-2B L1C, dlaždice 33UVR (okolí Prahy), 21. 7. 2024 (`MTD_MSIL1C.xml` z veřejného archivu Google Cloud): střední vlnové délky, spektrální citlivost pásem a sluneční ozáření nad atmosférou. Stahuje se asi 50 kB.",
        "en": "the product metadata of Sentinel-2B L1C, tile 33UVR (around Prague), 21 July 2024 (`MTD_MSIL1C.xml` from the Google Cloud public archive): central wavelengths, spectral response of the bands and top-of-atmosphere solar irradiance. About 50 kB is downloaded.",
    },
    "sources": {
        "cs": [
            "Copernicus Sentinel-2 data 2024, ESA; metadata L1C z veřejného archivu Google Cloud (`gcp-public-data-sentinel-2`). Licence: [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice), volné užití s uvedením zdroje.",
            "Konstanty h, c, e, k: v SI od roku 2019 přesně definované hodnoty, převzaté z `scipy.constants`.",
            "Šířka zakázaného pásu křemíku 1,12 eV při 300 K: Sze, S. M., Ng, K. K. (2007). *Physics of Semiconductor Devices*, 3. vyd. Wiley.",
            "Frekvence radaru Sentinel-1 (pásmo C) 5,405 GHz: ESA, Sentinel-1 User Handbook.",
        ],
        "en": [
            "Copernicus Sentinel-2 data 2024, ESA; L1C metadata from the Google Cloud public archive (`gcp-public-data-sentinel-2`). Licence: [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice), free use with attribution.",
            "Constants h, c, e, k: exactly defined SI values since 2019, taken from `scipy.constants`.",
            "Silicon band gap 1.12 eV at 300 K: Sze, S. M., Ng, K. K. (2007). *Physics of Semiconductor Devices*, 3rd ed. Wiley.",
            "Sentinel-1 radar frequency (C band) 5.405 GHz: ESA, Sentinel-1 User Handbook.",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a data", "## 1. Setup and data")),
        ("code", t('''
import re, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy.constants import h, c, e, k   # Planckova konstanta, rychlost světla, elementární náboj, Boltzmannova konstanta

# metadata jedné skutečné scény Sentinel-2B L1C (dlaždice 33UVR, 21. 7. 2024)
URL = ("https://storage.googleapis.com/gcp-public-data-sentinel-2/tiles/33/U/VR/"
       "S2B_MSIL1C_20240721T100559_N0510_R022_T33UVR_20240721T121133.SAFE/MTD_MSIL1C.xml")
xml = requests.get(URL, timeout=60).text
print(f"staženo {len(xml) / 1000:.0f} kB")
''', '''
import re, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy.constants import h, c, e, k   # Planck constant, speed of light, elementary charge, Boltzmann constant

# metadata of one real Sentinel-2B L1C scene (tile 33UVR, 21 July 2024)
URL = ("https://storage.googleapis.com/gcp-public-data-sentinel-2/tiles/33/U/VR/"
       "S2B_MSIL1C_20240721T100559_N0510_R022_T33UVR_20240721T121133.SAFE/MTD_MSIL1C.xml")
xml = requests.get(URL, timeout=60).text
print(f"downloaded {len(xml) / 1000:.0f} kB")
''')),
        ("code", t('''
# z XML vytáhneme pro každé pásmo: název, střední vlnovou délku, spektrální citlivost a sluneční ozáření E0
rows, srf = [], {}
for m in re.finditer(r'<Spectral_Information bandId="(\\d+)" physicalBand="(\\w+)">(.*?)</Spectral_Information>', xml, re.S):
    bid, name, body = int(m.group(1)), m.group(2), m.group(3)
    lmin = float(re.search(r'<MIN unit="nm">([\\d.]+)', body).group(1))
    vals = np.array(re.search(r"<VALUES>(.*?)</VALUES>", body).group(1).split(), float)
    srf[name] = (lmin + np.arange(len(vals)), vals)          # krok 1 nm
    e0 = float(re.search(rf'<SOLAR_IRRADIANCE bandId="{bid}"[^>]*>([\\d.]+)', xml).group(1))
    rows.append({"band": name,
                 "lambda_nm": float(re.search(r'<CENTRAL unit="nm">([\\d.]+)', body).group(1)),
                 "E0_W_m2_um": e0})
bands = pd.DataFrame(rows).set_index("band")
bands
''', '''
# from the XML we take for each band: name, central wavelength, spectral response and solar irradiance E0
rows, srf = [], {}
for m in re.finditer(r'<Spectral_Information bandId="(\\d+)" physicalBand="(\\w+)">(.*?)</Spectral_Information>', xml, re.S):
    bid, name, body = int(m.group(1)), m.group(2), m.group(3)
    lmin = float(re.search(r'<MIN unit="nm">([\\d.]+)', body).group(1))
    vals = np.array(re.search(r"<VALUES>(.*?)</VALUES>", body).group(1).split(), float)
    srf[name] = (lmin + np.arange(len(vals)), vals)          # 1 nm step
    e0 = float(re.search(rf'<SOLAR_IRRADIANCE bandId="{bid}"[^>]*>([\\d.]+)', xml).group(1))
    rows.append({"band": name,
                 "lambda_nm": float(re.search(r'<CENTRAL unit="nm">([\\d.]+)', body).group(1)),
                 "E0_W_m2_um": e0})
bands = pd.DataFrame(rows).set_index("band")
bands
''')),
        ("code", t('''
# spektrální citlivost pásem: jak silně detektor reaguje na jednotlivé vlnové délky
fig, ax = plt.subplots(figsize=(11, 3.2))
for name, (wl, r) in srf.items():
    ax.plot(wl, r, lw=1)
    ax.text(bands.lambda_nm[name], 1.03, name, ha="center", fontsize=8)
ax.set(xlabel="vlnová délka (nm)", ylabel="relativní citlivost", ylim=(0, 1.12), title="Sentinel-2B MSI: spektrální citlivost pásem")
plt.show()
''', '''
# spectral response of the bands: how strongly the detector responds to each wavelength
fig, ax = plt.subplots(figsize=(11, 3.2))
for name, (wl, r) in srf.items():
    ax.plot(wl, r, lw=1)
    ax.text(bands.lambda_nm[name], 1.03, name, ha="center", fontsize=8)
ax.set(xlabel="wavelength (nm)", ylabel="relative response", ylim=(0, 1.12), title="Sentinel-2B MSI: spectral response of the bands")
plt.show()
''')),
        ("md", t("## 2. Vlnová délka a frekvence", "## 2. Wavelength and frequency")),
        ("code", t('''
lam = bands.lambda_nm * 1e-9               # m
bands["f_THz"] = c / lam / 1e12            # f = c / λ
bands["lambda_x_f"] = lam * bands.f_THz * 1e12
bands[["lambda_nm", "f_THz", "lambda_x_f"]].round(1)
''', '''
lam = bands.lambda_nm * 1e-9               # m
bands["f_THz"] = c / lam / 1e12            # f = c / λ
bands["lambda_x_f"] = lam * bands.f_THz * 1e12
bands[["lambda_nm", "f_THz", "lambda_x_f"]].round(1)
''')),
        ("task", t(
            "Sloupec `lambda_x_f` je u všech pásem stejný. Co vyjadřuje a čemu odpovídá na laně ve vizuálu? Kolikrát vyšší frekvenci má pásmo B2 (modrá) než B12 (SWIR 2)?",
            "The `lambda_x_f` column is the same for every band. What does it express and what does it correspond to on the rope in the visual? How many times higher is the frequency of band B2 (blue) than of B12 (SWIR 2)?")),
        ("md", t("## 3. Energie jednoho fotonu", "## 3. Energy of one photon")),
        ("code", t('''
bands["E_photon_eV"] = h * c / lam / e     # E = h·f = h·c/λ, převedeno na elektronvolty
ax = bands.E_photon_eV.plot.bar(figsize=(9, 3), color="tab:purple")
ax.set(ylabel="energie fotonu (eV)", title="Energie jednoho fotonu ve středu pásma")
plt.show()
print(f"modrý (B2) / červený (B4) foton: {bands.E_photon_eV['B2'] / bands.E_photon_eV['B4']:.2f} ×")
''', '''
bands["E_photon_eV"] = h * c / lam / e     # E = h·f = h·c/λ, converted to electronvolts
ax = bands.E_photon_eV.plot.bar(figsize=(9, 3), color="tab:purple")
ax.set(ylabel="photon energy (eV)", title="Energy of one photon at the band centre")
plt.show()
print(f"blue (B2) / red (B4) photon: {bands.E_photon_eV['B2'] / bands.E_photon_eV['B4']:.2f} ×")
''')),
        ("task", t(
            "Ověř poměr energií modrého a červeného fotonu jen z vlnových délek, bez konstant. Proč stačí poměr λ? Jak se změní energie jednoho fotonu, když je modré světlo dvakrát jasnější?",
            "Check the energy ratio of the blue and red photon from the wavelengths alone, without constants. Why is the ratio of λ enough? How does the energy of one photon change when the blue light is twice as bright?")),
        ("md", t(
            "## 4. Jas je počet fotonů\n\nMetadata uvádějí pro každé pásmo sluneční ozáření nad atmosférou E0 ve W·m⁻²·µm⁻¹. Když ho vydělíme energií jednoho fotonu, dostaneme, kolik fotonů za sekundu dopadne na metr čtvereční v jednom mikrometru spektra.",
            "## 4. Brightness is the number of photons\n\nThe metadata give the top-of-atmosphere solar irradiance E0 in W·m⁻²·µm⁻¹ for each band. Dividing it by the energy of one photon gives the number of photons per second falling on one square metre within one micrometre of spectrum.")),
        ("code", t('''
bands["photons_per_s_m2_um"] = bands.E0_W_m2_um / (bands.E_photon_eV * e)
fig, ax1 = plt.subplots(figsize=(9, 3.2))
ax1.plot(bands.lambda_nm, bands.E0_W_m2_um, "o-", c="tab:orange", label="E0 (W·m⁻²·µm⁻¹)")
ax2 = ax1.twinx()
ax2.plot(bands.lambda_nm, bands.photons_per_s_m2_um / 1e21, "s--", c="tab:blue", label="fotony (10²¹ s⁻¹·m⁻²·µm⁻¹)")
ax1.set(xlabel="vlnová délka (nm)", ylabel="výkon"); ax2.set(ylabel="počet fotonů", ylim=(0, None)); ax1.set_ylim(0)
fig.legend(loc="lower left", bbox_to_anchor=(0.08, 0.15)); plt.show()
bands[["E0_W_m2_um", "E_photon_eV", "photons_per_s_m2_um"]].style.format("{:.3g}")
''', '''
bands["photons_per_s_m2_um"] = bands.E0_W_m2_um / (bands.E_photon_eV * e)
fig, ax1 = plt.subplots(figsize=(9, 3.2))
ax1.plot(bands.lambda_nm, bands.E0_W_m2_um, "o-", c="tab:orange", label="E0 (W·m⁻²·µm⁻¹)")
ax2 = ax1.twinx()
ax2.plot(bands.lambda_nm, bands.photons_per_s_m2_um / 1e21, "s--", c="tab:blue", label="photons (10²¹ s⁻¹·m⁻²·µm⁻¹)")
ax1.set(xlabel="wavelength (nm)", ylabel="power"); ax2.set(ylabel="number of photons", ylim=(0, None)); ax1.set_ylim(0)
fig.legend(loc="lower left", bbox_to_anchor=(0.08, 0.15)); plt.show()
bands[["E0_W_m2_um", "E_photon_eV", "photons_per_s_m2_um"]].style.format("{:.3g}")
''')),
        ("task", t(
            "Výkon E0 klesá od modré (B2) k SWIR 2 (B12) více než dvacetkrát. Klesá stejně i počet fotonů? Vysvětli rozdíl. V kterém pásmu dopadá na metr čtvereční nejvíc fotonů na mikrometr spektra a proč to není pásmo s nejvyšším E0?",
            "The power E0 falls more than twentyfold from blue (B2) to SWIR 2 (B12). Does the number of photons fall in the same way? Explain the difference. In which band does the most photons per micrometre fall on a square metre, and why is it not the band with the highest E0?")),
        ("md", t(
            "## 5. Které pásmo uvidí křemíkový čip\n\nFoton detektor uvolní elektron jen tehdy, když má aspoň energii zakázaného pásu materiálu. U křemíku je to asi 1,12 eV. Spočítáme mezní vlnovou délku a podíváme se, jak velká část citlivosti každého pásma leží pod ní.",
            "## 5. Which bands a silicon chip can see\n\nA photon frees an electron in a detector only if its energy is at least the band gap of the material. For silicon it is about 1.12 eV. We compute the cut-off wavelength and check how much of each band's response lies below it.")),
        ("code", t('''
Eg = 1.12          # ◀ parametr: šířka zakázaného pásu v eV (křemík 1,12; InGaAs asi 0,75; HgCdTe podle složení 0,1–0,5)
lam_cut = h * c / (Eg * e) * 1e9
print(f"mezní vlnová délka: {lam_cut:.0f} nm")
share = {name: r[wl <= lam_cut].sum() / r.sum() for name, (wl, r) in srf.items()}
bands["share_detectable"] = pd.Series(share)
bands[["lambda_nm", "E_photon_eV", "share_detectable"]].style.format({"lambda_nm": "{:.0f}", "E_photon_eV": "{:.2f}", "share_detectable": "{:.0%}"})
''', '''
Eg = 1.12          # ◀ parameter: band gap in eV (silicon 1.12; InGaAs about 0.75; HgCdTe 0.1–0.5 depending on composition)
lam_cut = h * c / (Eg * e) * 1e9
print(f"cut-off wavelength: {lam_cut:.0f} nm")
share = {name: r[wl <= lam_cut].sum() / r.sum() for name, (wl, r) in srf.items()}
bands["share_detectable"] = pd.Series(share)
bands[["lambda_nm", "E_photon_eV", "share_detectable"]].style.format({"lambda_nm": "{:.0f}", "E_photon_eV": "{:.2f}", "share_detectable": "{:.0%}"})
''')),
        ("task", t(
            "Která pásma Sentinelu-2 by křemíkový detektor zachytil celá, která jen zčásti a která vůbec? Nastav `Eg = 0.75` (InGaAs) a spusť buňku znovu. Co se změnilo? Sentinel-2 má pro pásma B10 až B12 detektory z HgCdTe: proč?",
            "Which Sentinel-2 bands would a silicon detector capture fully, partly and not at all? Set `Eg = 0.75` (InGaAs) and run the cell again. What changed? Sentinel-2 uses HgCdTe detectors for bands B10 to B12: why?")),
        ("md", t(
            "## 6. Termální záření a radar\n\nPorovnáme fotony z termálního pásma (10,9 µm, jako Landsat 8 TIRS) a z radaru Sentinel-1 (5,405 GHz) s typickou tepelnou energií kmitů v detektoru při pokojové teplotě, k · T.",
            "## 6. Thermal radiation and radar\n\nWe compare photons from a thermal band (10.9 µm, as in Landsat 8 TIRS) and from the Sentinel-1 radar (5.405 GHz) with the typical thermal energy in a detector at room temperature, k · T.")),
        ("code", t('''
T = 300            # ◀ parametr: teplota detektoru v kelvinech
kT = k * T / e
other = pd.DataFrame({
    "lambda_m": [h * c / (10 * e), 490e-9, 1610e-9, 10.9e-6, c / 5.405e9],
}, index=["ionizace (10 eV)", "B2 modrá", "B11 SWIR", "termální 10,9 µm", "radar C 5,405 GHz"])
other["E_eV"] = h * c / other.lambda_m / e
other["E_over_kT"] = other.E_eV / kT
print(f"k·T při {T} K = {kT * 1000:.1f} meV")
other.style.format({"lambda_m": "{:.3g}", "E_eV": "{:.3g}", "E_over_kT": "{:.3g}"})
''', '''
T = 300            # ◀ parameter: detector temperature in kelvin
kT = k * T / e
other = pd.DataFrame({
    "lambda_m": [h * c / (10 * e), 490e-9, 1610e-9, 10.9e-6, c / 5.405e9],
}, index=["ionisation (10 eV)", "B2 blue", "B11 SWIR", "thermal 10.9 µm", "radar C 5.405 GHz"])
other["E_eV"] = h * c / other.lambda_m / e
other["E_over_kT"] = other.E_eV / kT
print(f"k·T at {T} K = {kT * 1000:.1f} meV")
other.style.format({"lambda_m": "{:.3g}", "E_eV": "{:.3g}", "E_over_kT": "{:.3g}"})
''')),
        ("task", t(
            "Termální foton má energii jen asi čtyřikrát větší než k · T, radarový foton je víc než tisíckrát slabší než k · T. Proč proto termální kamery s fotonovými detektory chladí a proč mikrobolometr a radarová anténa neměří jednotlivé fotony, ale ohřev, resp. elektrické pole vlny? Nastav `T = 77` (kapalný dusík) a porovnej.",
            "A thermal photon has only about four times the energy of k · T, a radar photon is more than a thousand times weaker than k · T. Why are thermal cameras with photon detectors cooled, and why do a microbolometer and a radar antenna measure heating or the electric field of the wave rather than individual photons? Set `T = 77` (liquid nitrogen) and compare.")),
        ("task", t(
            "Na jaké vlnové délce má foton energii 10 eV (přibližná hranice ionizace)? Do které oblasti spektra patří? Chemické vazby v molekulách mají energii v řádu několika eV. Vysvětli, proč jediný foton UV záření může poškodit DNA, zatímco silný radarový signál nese celkem víc energie, a přesto žádnou vazbu nerozbije ani nic neionizuje.",
            "At what wavelength does a photon have an energy of 10 eV (the approximate ionisation threshold)? Which part of the spectrum is it? Chemical bonds in molecules have energies of a few eV. Explain why a single UV photon can damage DNA while a strong radar signal carries more energy in total and still breaks no bond and ionises nothing.")),
    ]
