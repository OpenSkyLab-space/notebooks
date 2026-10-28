from _common import OPEN_METEO_HELPER

META = {
    "version": "1.0",
    "minutes": 45,
    "title": {"cs": "Proč dron letí: vztlak, hybnost a skutečná hustota vzduchu", "en": "Why a drone flies: lift, momentum and real air density"},
    "visual": {"cs": "Proč dron letí", "en": "Why a drone flies"},
    "lead": {
        "cs": "Vizuál vysvětluje vztlak profilu, pádový úhel, teorii hybnosti rotoru a nebezpečné režimy klesání. Tady teorii hybnosti použiješ na skutečné drony (DJI Mavic 3 Enterprise a Matrice 350 RTK) a na skutečnou hustotu vzduchu, kterou spočítáš z měřeného a modelovaného počasí na horách i v nížině.",
        "en": "The visual explains airfoil lift, the stall angle, rotor momentum theory and dangerous descent regimes. Here you apply momentum theory to real drones (DJI Mavic 3 Enterprise and Matrice 350 RTK) and to real air density computed from weather in the mountains and in the lowlands.",
    },
    "goal": {
        "cs": "spočítat vztlak tenkého profilu a jeho mez, indukovanou rychlost a výkon při visení, ukázat, jak hustota vzduchu mění výdrž, a odhadnout rychlost klesání, při které hrozí vírový prstenec.",
        "en": "compute the lift of a thin airfoil and its limit, induced velocity and hover power, show how air density changes endurance, and estimate the descent rate at which the vortex ring state threatens.",
    },
    "data": {
        "cs": "hodinová teplota, tlak a vlhkost za posledních 92 dní z Open-Meteo pro Prahu, Sněžku a Lomnický štít; hmotnost, průměr vrtulí, baterie a výdrž dronů z technických listů DJI.",
        "en": "hourly temperature, pressure and humidity for the last 92 days from Open-Meteo for Prague, Sněžka and Lomnický štít; mass, propeller diameter, battery and endurance of the drones from DJI data sheets.",
    },
    "sources": {
        "cs": [
            "Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "DJI Mavic 3 Enterprise (3E): vzletová hmotnost 915 g, vrtule 9453F (9,4″), baterie 77 Wh, max. doba visení 38 min, max. rychlost klesání 6 m/s; DJI Matrice 350 RTK: hmotnost s bateriemi TB65 6,47 kg, max. vzletová 9,2 kg, vrtule 21″, 2 × 263 Wh, max. rychlost klesání 7 m/s (technické listy DJI).",
            "Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*, 2. vyd. Cambridge University Press (teorie hybnosti, účinnost FM, vírový prstenec).",
            "Anderson, J. D. (2017). *Fundamentals of Aerodynamics*, 6. vyd. McGraw-Hill (teorie tenkého profilu).",
            "Hustota vlhkého vzduchu přes virtuální teplotu; tlak nasycených par Magnusovým vzorcem (WMO-No. 8, 2018).",
        ],
        "en": [
            "Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "DJI Mavic 3 Enterprise (3E): take-off weight 915 g, 9453F propellers (9.4″), 77 Wh battery, max. hover time 38 min, max. descent speed 6 m/s; DJI Matrice 350 RTK: weight with TB65 batteries 6.47 kg, max. take-off 9.2 kg, 21″ propellers, 2 × 263 Wh, max. descent speed 7 m/s (DJI data sheets).",
            "Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*, 2nd ed. Cambridge University Press (momentum theory, figure of merit, vortex ring state).",
            "Anderson, J. D. (2017). *Fundamentals of Aerodynamics*, 6th ed. McGraw-Hill (thin airfoil theory).",
            "Density of moist air via virtual temperature; saturation vapour pressure by the Magnus formula (WMO-No. 8, 2018).",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava", "## 1. Setup")),
        ("code", '''
import time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
''' + t(OPEN_METEO_HELPER["cs"], OPEN_METEO_HELPER["en"]) + t('''
g = 9.81
# drony z technických listů DJI: hmotnost (kg), počet rotorů, průměr vrtule (m), energie baterií (Wh), max. doba visení (min)
DRONES = {
    "Mavic 3E":     dict(m=0.915, n=4, D=9.4 * 0.0254, E=77, hover_min=38),
    "Matrice 350":  dict(m=6.47,  n=4, D=21 * 0.0254,  E=2 * 263, hover_min=None),
}
''', '''
g = 9.81
# drones from DJI data sheets: mass (kg), number of rotors, propeller diameter (m), battery energy (Wh), max. hover time (min)
DRONES = {
    "Mavic 3E":     dict(m=0.915, n=4, D=9.4 * 0.0254, E=77, hover_min=38),
    "Matrice 350":  dict(m=6.47,  n=4, D=21 * 0.0254,  E=2 * 263, hover_min=None),
}
''')),
        ("md", t(
            "## 2. Vztlak profilu a pád\n\nPodle teorie tenkého profilu roste součinitel vztlaku lineárně s úhlem náběhu: c_L = 2π (α − α₀), kde α₀ ≈ −2 · prohnutí / hloubka (záporné pro prohnutý profil). Skutečný profil se ale při úhlu kolem 12–16° odtrhne a vztlak spadne. Vztlak L = ½ ρ v² S c_L.",
            "## 2. Airfoil lift and stall\n\nThin airfoil theory says the lift coefficient grows linearly with angle of attack: c_L = 2π (α − α₀), where α₀ ≈ −2 · camber / chord (negative for a cambered airfoil). A real airfoil separates at about 12–16° and lift drops. Lift L = ½ ρ v² S c_L.")),
        ("code", t('''
camber = 0.04          # ◀ parametr: prohnutí profilu (podíl hloubky; 0 = souměrný, 0,04 = 4 %)
alpha_stall = 14       # ◀ parametr: pádový úhel (°), z měření skutečných profilů zhruba 12–16°
v, rho, S = 15, 1.2, 0.5     # rychlost (m/s), hustota (kg/m³), plocha křídla (m²): malý dron s pevným křídlem
alpha = np.linspace(-10, 25, 141)
a0 = -2 * camber
cl_theory = 2 * np.pi * (np.radians(alpha) - a0)
cl_real = np.where(alpha <= alpha_stall, cl_theory, 2 * np.pi * (np.radians(alpha_stall) - a0) * np.exp(-(alpha - alpha_stall) / 6) * 0.9)
plt.figure(figsize=(8, 3.5))
plt.plot(alpha, cl_theory, "--", label="tenký profil (teorie)"); plt.plot(alpha, cl_real, label="s odtržením proudění (schematicky)")
plt.axvline(alpha_stall, color="gray", ls=":"); plt.xlabel("úhel náběhu α (°)"); plt.ylabel("c_L"); plt.legend(); plt.show()
for a in (0, 5, 10):
    cl = 2 * np.pi * (np.radians(a) - a0)
    print(f"α = {a:2d}°: c_L = {cl:.2f}, vztlak {0.5 * rho * v**2 * S * cl:5.1f} N (unese {0.5 * rho * v**2 * S * cl / g:.2f} kg)")
''', '''
camber = 0.04          # ◀ parameter: airfoil camber (fraction of chord; 0 = symmetric, 0.04 = 4 %)
alpha_stall = 14       # ◀ parameter: stall angle (°), roughly 12–16° from measurements of real airfoils
v, rho, S = 15, 1.2, 0.5     # speed (m/s), density (kg/m³), wing area (m²): a small fixed-wing drone
alpha = np.linspace(-10, 25, 141)
a0 = -2 * camber
cl_theory = 2 * np.pi * (np.radians(alpha) - a0)
cl_real = np.where(alpha <= alpha_stall, cl_theory, 2 * np.pi * (np.radians(alpha_stall) - a0) * np.exp(-(alpha - alpha_stall) / 6) * 0.9)
plt.figure(figsize=(8, 3.5))
plt.plot(alpha, cl_theory, "--", label="thin airfoil (theory)"); plt.plot(alpha, cl_real, label="with flow separation (schematic)")
plt.axvline(alpha_stall, color="gray", ls=":"); plt.xlabel("angle of attack α (°)"); plt.ylabel("c_L"); plt.legend(); plt.show()
for a in (0, 5, 10):
    cl = 2 * np.pi * (np.radians(a) - a0)
    print(f"α = {a:2d}°: c_L = {cl:.2f}, lift {0.5 * rho * v**2 * S * cl:5.1f} N (carries {0.5 * rho * v**2 * S * cl / g:.2f} kg)")
''')),
        ("task", t(
            "Proč prohnutý profil nese i při úhlu náběhu 0° a souměrný ne? Nastav `camber = 0`. Při jakém úhlu by křídlo uneslo 2,5 kg? Proč teorie tenkého profilu nad pádovým úhlem neplatí a co se v tu chvíli děje s prouděním na horní straně? (Průběh za pádem je v grafu jen schematický.)",
            "Why does a cambered airfoil lift even at 0° angle of attack and a symmetric one does not? Set `camber = 0`. At what angle would the wing carry 2.5 kg? Why does thin airfoil theory fail beyond the stall angle and what happens to the flow on the upper surface? (The curve beyond stall is only schematic.)")),
        ("md", t(
            "## 3. Dva pohledy na jednu sílu\n\nRotor při visení vrhá vzduch dolů. Teorie hybnosti: tah T = ṁ · w, kde w = 2 v_i je rychlost vzduchu daleko pod rotorem a ṁ = ρ A v_i hmotnostní tok diskem. Odtud v_i = √(T / (2 ρ A)). Tentýž tah je i rozdíl tlaků nad a pod diskem: Δp = T / A.",
            "## 3. Two views of one force\n\nA hovering rotor throws air downwards. Momentum theory: thrust T = ṁ · w, where w = 2 v_i is the air speed far below the rotor and ṁ = ρ A v_i the mass flow through the disc. Hence v_i = √(T / (2 ρ A)). The same thrust is also the pressure difference across the disc: Δp = T / A.")),
        ("code", t('''
def hover(d, rho):
    T = d["m"] * g / d["n"]                 # tah jednoho rotoru (N)
    A = np.pi * d["D"] ** 2 / 4             # plocha disku (m²)
    vi = np.sqrt(T / (2 * rho * A))         # indukovaná rychlost (m/s)
    return dict(T=T, A=A, vi=vi, mdot=rho * A * vi, dp=T / A, P_ideal=d["n"] * T * vi)

rows = []
for name, d in DRONES.items():
    h = hover(d, 1.225)
    rows.append({"dron": name, "tah rotoru (N)": h["T"], "zatížení disku Δp (Pa)": h["dp"], "v_i (m/s)": h["vi"],
                 "ṁ (kg/s)": h["mdot"], "ṁ·2v_i (N)": h["mdot"] * 2 * h["vi"], "ideální výkon (W)": h["P_ideal"]})
pd.DataFrame(rows).set_index("dron").round(2)
''', '''
def hover(d, rho):
    T = d["m"] * g / d["n"]                 # thrust of one rotor (N)
    A = np.pi * d["D"] ** 2 / 4             # disc area (m²)
    vi = np.sqrt(T / (2 * rho * A))         # induced velocity (m/s)
    return dict(T=T, A=A, vi=vi, mdot=rho * A * vi, dp=T / A, P_ideal=d["n"] * T * vi)

rows = []
for name, d in DRONES.items():
    h = hover(d, 1.225)
    rows.append({"drone": name, "rotor thrust (N)": h["T"], "disc loading Δp (Pa)": h["dp"], "v_i (m/s)": h["vi"],
                 "ṁ (kg/s)": h["mdot"], "ṁ·2v_i (N)": h["mdot"] * 2 * h["vi"], "ideal power (W)": h["P_ideal"]})
pd.DataFrame(rows).set_index("drone").round(2)
''')),
        ("task", t(
            "Ověř, že sloupec ṁ · 2 v_i dává stejné číslo jako tah rotoru. Proč jsou rozdíl tlaků a hybnost vrženého vzduchu dva popisy téže síly, ne dvě síly, které se sčítají? Proč má Matrice 350 větší zatížení disku a vyšší indukovanou rychlost, i když má mnohem větší vrtule?",
            "Check that the ṁ · 2 v_i column gives the same number as the rotor thrust. Why are the pressure difference and the momentum of the air thrown down two descriptions of one force, not two forces that add up? Why does the Matrice 350 have a higher disc loading and induced velocity even though its propellers are much larger?")),
        ("md", t(
            "## 4. Skutečná hustota vzduchu: nížina, hory, léto a zima\n\nIdeální výkon při visení je P = T^(3/2) / √(2 ρ A), tedy roste s 1/√ρ. Hustotu spočítáme z tlaku, teploty a vlhkosti za posledních 92 dní.",
            "## 4. Real air density: lowland, mountains, summer and winter\n\nIdeal hover power is P = T^(3/2) / √(2 ρ A), so it grows with 1/√ρ. We compute density from pressure, temperature and humidity over the last 92 days.")),
        ("code", t('''
SITES = {"Praha": (50.08, 14.42), "Sněžka": (50.736, 15.740), "Lomnický štít": (49.195, 20.215)}
dens = {}
for name, (lat, lon) in SITES.items():
    w = open_meteo({"latitude": lat, "longitude": lon, "past_days": 92, "forecast_days": 1,
                    "hourly": "temperature_2m,relative_humidity_2m,surface_pressure", "timezone": "UTC"})
    df = pd.DataFrame(w["hourly"]).set_index("time")
    T = df.temperature_2m + 273.15
    e = df.relative_humidity_2m / 100 * 6.112 * np.exp(17.62 * df.temperature_2m / (243.12 + df.temperature_2m))
    Tv = T / (1 - 0.378 * e / df.surface_pressure)                    # virtuální teplota
    dens[name] = df.surface_pressure * 100 / (287.05 * Tv)
    print(f"{name:14s} {w['elevation']:5.0f} m n. m.: ρ {dens[name].min():.3f}–{dens[name].max():.3f} kg/m³, medián {dens[name].median():.3f}")
dens = pd.DataFrame(dens); dens.index = pd.to_datetime(dens.index)
ax = dens.plot(figsize=(10, 3.5)); ax.set(ylabel="hustota vzduchu (kg/m³)"); plt.show()
''', '''
SITES = {"Prague": (50.08, 14.42), "Sněžka": (50.736, 15.740), "Lomnický štít": (49.195, 20.215)}
dens = {}
for name, (lat, lon) in SITES.items():
    w = open_meteo({"latitude": lat, "longitude": lon, "past_days": 92, "forecast_days": 1,
                    "hourly": "temperature_2m,relative_humidity_2m,surface_pressure", "timezone": "UTC"})
    df = pd.DataFrame(w["hourly"]).set_index("time")
    T = df.temperature_2m + 273.15
    e = df.relative_humidity_2m / 100 * 6.112 * np.exp(17.62 * df.temperature_2m / (243.12 + df.temperature_2m))
    Tv = T / (1 - 0.378 * e / df.surface_pressure)                    # virtual temperature
    dens[name] = df.surface_pressure * 100 / (287.05 * Tv)
    print(f"{name:14s} {w['elevation']:5.0f} m a.s.l.: ρ {dens[name].min():.3f}–{dens[name].max():.3f} kg/m³, median {dens[name].median():.3f}")
dens = pd.DataFrame(dens); dens.index = pd.to_datetime(dens.index)
ax = dens.plot(figsize=(10, 3.5)); ax.set(ylabel="air density (kg/m³)"); plt.show()
''')),
        ("code", t('''
FM, eta = 0.60, 0.80     # ◀ parametr: účinnost rotoru (figure of merit) a účinnost motoru s regulátorem
d = DRONES["Mavic 3E"]
for name in dens:
    for label, rho_ in [("nejhustší", dens[name].max()), ("nejřidší", dens[name].min())]:
        P = hover(d, rho_)["P_ideal"] / (FM * eta)
        print(f"{name:14s} {label:9s} ρ = {rho_:.3f}: výkon {P:5.1f} W, visení {d['E'] / P * 60:4.1f} min")
print(f"výrobce udává max. dobu visení {d['hover_min']} min")
''', '''
FM, eta = 0.60, 0.80     # ◀ parameter: rotor efficiency (figure of merit) and motor + ESC efficiency
d = DRONES["Mavic 3E"]
for name in dens:
    for label, rho_ in [("densest", dens[name].max()), ("thinnest", dens[name].min())]:
        P = hover(d, rho_)["P_ideal"] / (FM * eta)
        print(f"{name:14s} {label:9s} ρ = {rho_:.3f}: power {P:5.1f} W, hover {d['E'] / P * 60:4.1f} min")
print(f"the manufacturer states a max. hover time of {d['hover_min']} min")
''')),
        ("task", t(
            "O kolik procent je vzduch na Lomnickém štítu řidší než v Praze a o kolik procent víc výkonu potřebuje dron k visení? Ověř, že poměr výkonů je √(ρ_Praha / ρ_štít). Jaké FM a η by musely platit, aby odhad doby visení odpovídal údaji výrobce? Proč výrobce udává výdrž za ideálních podmínek?",
            "By what percentage is the air on Lomnický štít thinner than in Prague, and how many per cent more power does the drone need to hover? Check that the power ratio is √(ρ_Prague / ρ_peak). What FM and η would make the hover-time estimate match the manufacturer's figure? Why do manufacturers state endurance under ideal conditions?")),
        ("code", t('''
D_list = np.linspace(0.15, 0.6, 40)
P_D = [hover(dict(DRONES["Mavic 3E"], D=D_), 1.225)["P_ideal"] / (FM * eta) for D_ in D_list]
plt.figure(figsize=(7, 3.3)); plt.plot(D_list * 100, P_D); plt.axvline(DRONES["Mavic 3E"]["D"] * 100, color="gray", ls=":")
plt.xlabel("průměr vrtule (cm)"); plt.ylabel("výkon při visení (W)"); plt.title("Mavic 3E se stejnou hmotností a jinými vrtulemi"); plt.show()
''', '''
D_list = np.linspace(0.15, 0.6, 40)
P_D = [hover(dict(DRONES["Mavic 3E"], D=D_), 1.225)["P_ideal"] / (FM * eta) for D_ in D_list]
plt.figure(figsize=(7, 3.3)); plt.plot(D_list * 100, P_D); plt.axvline(DRONES["Mavic 3E"]["D"] * 100, color="gray", ls=":")
plt.xlabel("propeller diameter (cm)"); plt.ylabel("hover power (W)"); plt.title("Mavic 3E with the same mass and other propellers"); plt.show()
''')),
        ("task", t(
            "Proč velké pomalé vrtule potřebují k visení méně výkonu než malé rychlé? Vysvětli to z P = T · v_i: kterou ze dvou veličin větší disk mění? Proč přesto nemá malý dron obří vrtule?",
            "Why do large slow propellers need less power to hover than small fast ones? Explain it from P = T · v_i: which of the two quantities does a larger disc change? Why then does a small drone not have huge propellers?")),
        ("md", t(
            "## 5. Klesání a vírový prstenec\n\nKdyž dron klesá svisle rychlostí srovnatelnou s indukovanou rychlostí při visení v_h, vzduch, který rotor tlačí dolů, se mu vrací shora skrz disk. Podle Leishmana (2006) je oblast vírového prstence zhruba mezi 0,5 v_h a 1,5 v_h (přesná mez závisí na měření).",
            "## 5. Descent and the vortex ring state\n\nWhen a drone descends vertically at a speed comparable to the hover induced velocity v_h, the air the rotor pushes down recirculates back through the disc from above. According to Leishman (2006) the vortex ring region lies roughly between 0.5 v_h and 1.5 v_h (the exact boundary depends on the measurements).")),
        ("code", t('''
v_desc = {"Mavic 3E": 6, "Matrice 350": 7}          # max. rychlost klesání z technických listů (m/s)
site = "Sněžka"                                       # ◀ parametr: místo (hustota = medián za 92 dní)
for name, d in DRONES.items():
    vh = hover(d, dens[site].median())["vi"]
    print(f"{name:12s}: v_h = {vh:.1f} m/s → vírový prstenec zhruba {0.5 * vh:.1f}–{1.5 * vh:.1f} m/s, "
          f"max. klesání výrobce {v_desc[name]} m/s ({v_desc[name] / vh:.1f} v_h)")
''', '''
v_desc = {"Mavic 3E": 6, "Matrice 350": 7}          # max. descent speed from the data sheets (m/s)
site = "Sněžka"                                       # ◀ parameter: site (density = 92-day median)
for name, d in DRONES.items():
    vh = hover(d, dens[site].median())["vi"]
    print(f"{name:12s}: v_h = {vh:.1f} m/s → vortex ring roughly {0.5 * vh:.1f}–{1.5 * vh:.1f} m/s, "
          f"manufacturer's max. descent {v_desc[name]} m/s ({v_desc[name] / vh:.1f} v_h)")
''')),
        ("task", t(
            "Při jaké svislé rychlosti klesání hrozí vírový prstenec u Mavicu a u Matrice? Leží maximální rychlost klesání od výrobce v této oblasti? Proč je bezpečnější klesat šikmo nebo s dopřednou rychlostí a proč je nebezpečné rychlé svislé klesání těsně nad zemí, kdy už není prostor na vybrání?",
            "At what vertical descent speed does the vortex ring state threaten the Mavic and the Matrice? Does the manufacturer's maximum descent speed lie in this region? Why is it safer to descend at an angle or with forward speed, and why is a fast vertical descent close to the ground dangerous when there is no room to recover?")),
    ]
