from _common import OPEN_METEO_HELPER

META = {
    "version": "1.0",
    "minutes": 55,
    "visual_stem": "why_drones_fly",
    "title": {"cs": "Proč dron letí, pokročilá verze: výkon v dopředném letu, vítr, hustota vzduchu a vliv země",
              "en": "Why a drone flies, advanced: power in forward flight, wind, air density and ground effect"},
    "visual": {"cs": "Proč dron letí", "en": "Why a drone flies"},
    "lead": {
        "cs": "Pokročilá verze notebooku o letu dronu. Mavic 3E podle výrobce visí 38 minut, ale stálou rychlostí 32,4 km/h letí 45 minut: v dopředném letu tedy potřebuje méně výkonu než na místě. Sestavíš model výkonu z teorie hybnosti, nakalibruješ ho na tyto dva údaje a použiješ ho na nejlepší rychlost pro výdrž a dolet, na skutečný vítr ve 120 m za poslední tři měsíce, na hustotu vzduchu a na let těsně nad zemí.",
        "en": "The advanced version of the drone flight notebook. According to the manufacturer the Mavic 3E hovers for 38 minutes but flies for 45 minutes at a constant 32.4 km/h, so it needs less power in forward flight than on the spot. You build a power model from momentum theory, calibrate it to these two figures and use it for the best speed for endurance and range, for the real wind at 120 m over the last three months, for air density and for flight close to the ground.",
    },
    "goal": {
        "cs": "rozložit výkon dronu na indukovaný, profilový a škodlivý, nakalibrovat model na údaje výrobce, najít rychlost nejdelší výdrže a největšího doletu i s protivětrem, vyhodnotit skutečný vítr a hustotu vzduchu za 92 dní a odhadnout vliv země při visení nízko.",
        "en": "split drone power into induced, profile and parasite parts, calibrate the model to the manufacturer's figures, find the speed for maximum endurance and maximum range including headwind, evaluate the real wind and air density over 92 days, and estimate ground effect when hovering low.",
    },
    "data": {
        "cs": "hodinový vítr v 10 a 120 m, teplota, vlhkost a tlak za posledních 92 dní z Open-Meteo pro Roztoky (modelová data, ne měření); hmotnost, vrtule, baterie a výdrž Mavicu 3E z technického listu DJI (45 min letu stálou rychlostí 32,4 km/h bez větru u hladiny moře do vybití, 38 min visení). Účinnost rotoru FM, indukční ztráty a obvodová rychlost listu jsou odhady; účinnost pohonu a plochu odporu notebook dopočítá kalibrací, takže v nich jsou schované i všechny ostatní ztráty (elektronika, kamera, baterie).",
        "en": "hourly wind at 10 and 120 m, temperature, humidity and pressure for the last 92 days from Open-Meteo for Roztoky (model data, not measurements); mass, propellers, battery and endurance of the Mavic 3E from the DJI data sheet (45 min of flight at a constant 32.4 km/h without wind at sea level until empty, 38 min of hover). The rotor figure of merit FM, the induced losses and the blade tip speed are estimates; the drive efficiency and drag area are calibrated by the notebook, so they also absorb all other losses (electronics, camera, battery).",
    },
    "sources": {
        "cs": [
            "Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "DJI: *Mavic 3 Enterprise, specifikace* (https://enterprise.dji.com/mavic-3-enterprise/specs): vzletová hmotnost 915 g, baterie 77 Wh, max. doba letu 45 min a max. doba visení 38 min bez větru, odolnost vůči větru 12 m/s, max. rychlost 15 m/s v normálním a 21 m/s ve sportovním režimu. Podmínky měření 45 min (stálá rychlost 32,4 km/h u hladiny moře do vybití) uvádějí technické listy prodejců.",
            "Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*, 2. vyd. Cambridge University Press (teorie hybnosti v dopředném letu, rozklad výkonu, K ≈ 4,65).",
            "Glauert, H. (1926). A general theory of the autogyro. *ARC R&M* 1111 (indukovaná rychlost v dopředném letu).",
            "Cheeseman, I. C., Bennett, W. E. (1955). The effect of the ground on a helicopter rotor in forward flight. *ARC R&M* 3021.",
            "Hustota vlhkého vzduchu přes virtuální teplotu; tlak nasycených par Magnusovým vzorcem (WMO-No. 8, 2018).",
        ],
        "en": [
            "Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "DJI: *Mavic 3 Enterprise, specs* (https://enterprise.dji.com/mavic-3-enterprise/specs): take-off weight 915 g, 77 Wh battery, max. flight time 45 min and max. hover time 38 min without wind, wind resistance 12 m/s, max. speed 15 m/s in normal and 21 m/s in sport mode. The measurement conditions for 45 min (constant 32.4 km/h at sea level until empty) are given in resellers' data sheets.",
            "Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*, 2nd ed. Cambridge University Press (momentum theory in forward flight, power breakdown, K ≈ 4.65).",
            "Glauert, H. (1926). A general theory of the autogyro. *ARC R&M* 1111 (induced velocity in forward flight).",
            "Cheeseman, I. C., Bennett, W. E. (1955). The effect of the ground on a helicopter rotor in forward flight. *ARC R&M* 3021.",
            "Density of moist air via virtual temperature; saturation vapour pressure by the Magnus formula (WMO-No. 8, 2018).",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava", "## 1. Setup")),
        ("code", t('''
import time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq
''' + OPEN_METEO_HELPER["cs"], '''
import time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq
''' + OPEN_METEO_HELPER["en"])),
        ("md", t(
            "## 2. Model výkonu a jeho kalibrace\n\nVýkon rozložíme na tři části. **Indukovaný** výkon jde na urychlení vzduchu dolů; v dopředném letu proudí diskem víc vzduchu, takže stačí menší indukovaná rychlost (Glauert). **Profilový** výkon spotřebuje odpor listů vrtule a s rychlostí mírně roste. **Škodlivý** výkon překonává odpor trupu a roste s třetí mocninou rychlosti. Dvě neznámé, účinnost pohonu η a ekvivalentní plochu odporu f, určíme z výdrže při visení a při letu 9 m/s.",
            "## 2. The power model and its calibration\n\nWe split power into three parts. **Induced** power accelerates air downwards; in forward flight more air passes through the disc, so a smaller induced velocity is enough (Glauert). **Profile** power is used by the drag of the propeller blades and grows slightly with speed. **Parasite** power overcomes the drag of the airframe and grows with the cube of speed. Two unknowns, the drive efficiency η and the equivalent drag area f, are set from the endurance in hover and in flight at 9 m/s.")),
        ("code", t('''
g = 9.81
# Mavic 3E z technického listu DJI: vzletová hmotnost, vrtule 9,4″, baterie, výdrž
m, n_rot, R, E_BAT = 0.915, 4, 9.4 * 0.0254 / 2, 77.0
T_HOVER, T_FLIGHT, V_TEST = 38, 45, 32.4 / 3.6     # min visení; min letu stálou rychlostí 32,4 km/h; ta rychlost v m/s
A = n_rot * np.pi * R ** 2                          # plocha všech disků
W = m * g
RHO0 = 1.225                                        # hustota standardní atmosféry u hladiny moře (kg/m³)
KAPPA = 1.15     # ◀ parametr: indukční ztráty proti ideálnímu disku (nerovnoměrný tok, konec listu)
FM = 0.60        # ◀ parametr: účinnost rotoru při visení (figure of merit)
V_TIP = 90.0     # ◀ parametr: obvodová rychlost konce listu (m/s), odhad
K_P = 4.65       # nárůst profilového výkonu s dopřednou rychlostí (Leishman 2006)

def induced_velocity(T, V, alpha, rho):
    """Indukovaná rychlost v dopředném letu podle Glauerta (rotor skloněný o alpha)."""
    vh = np.sqrt(T / (2 * rho * A))
    return brentq(lambda v: v - vh ** 2 / np.hypot(V * np.cos(alpha), V * np.sin(alpha) + v), 1e-6, 2 * vh)

def power(V, rho, fA, eta, mass=m):
    """Elektrický výkon (W) při vodorovném letu rychlostí V vůči vzduchu: indukovaný, profilový, škodlivý."""
    Wt = mass * g
    D = 0.5 * rho * V ** 2 * fA                     # odpor trupu
    T = np.hypot(Wt, D); alpha = np.arctan2(D, Wt)  # tah a náklon
    Pi_h = Wt * np.sqrt(Wt / (2 * rho * A))         # ideální výkon při visení
    Pi = KAPPA * T * induced_velocity(T, V, alpha, rho)
    P0 = (1 / FM - KAPPA) * Pi_h * (1 + K_P * (V / V_TIP) ** 2)
    Pp = D * V
    return np.array([Pi, P0, Pp]) / eta

# kalibrace na údaje výrobce: výkon při visení určí účinnost pohonu, výkon při 9 m/s plochu odporu
P_hover, P_test = E_BAT / (T_HOVER / 60), E_BAT / (T_FLIGHT / 60)
eta = W * np.sqrt(W / (2 * RHO0 * A)) / FM / P_hover
fA = brentq(lambda f: power(V_TEST, RHO0, f, eta).sum() - P_test, 1e-5, 0.5)
print(f"výkon z výdrže: visení {P_hover:.1f} W, let {V_TEST:.0f} m/s {P_test:.1f} W")
print(f"kalibrace: účinnost pohonu a elektroniky η = {eta:.2f}, ekvivalentní plocha odporu f = Cd·S = {fA * 1e4:.0f} cm²")
''', '''
g = 9.81
# Mavic 3E from the DJI data sheet: take-off mass, 9.4″ propellers, battery, endurance
m, n_rot, R, E_BAT = 0.915, 4, 9.4 * 0.0254 / 2, 77.0
T_HOVER, T_FLIGHT, V_TEST = 38, 45, 32.4 / 3.6     # min hover; min of flight at a constant 32.4 km/h; that speed in m/s
A = n_rot * np.pi * R ** 2                          # area of all discs
W = m * g
RHO0 = 1.225                                        # standard atmosphere density at sea level (kg/m³)
KAPPA = 1.15     # ◀ parameter: induced losses relative to an ideal disc (non-uniform inflow, tip losses)
FM = 0.60        # ◀ parameter: rotor efficiency in hover (figure of merit)
V_TIP = 90.0     # ◀ parameter: blade tip speed (m/s), an estimate
K_P = 4.65       # growth of profile power with forward speed (Leishman 2006)

def induced_velocity(T, V, alpha, rho):
    """Induced velocity in forward flight after Glauert (rotor tilted by alpha)."""
    vh = np.sqrt(T / (2 * rho * A))
    return brentq(lambda v: v - vh ** 2 / np.hypot(V * np.cos(alpha), V * np.sin(alpha) + v), 1e-6, 2 * vh)

def power(V, rho, fA, eta, mass=m):
    """Electrical power (W) in level flight at airspeed V: induced, profile, parasite."""
    Wt = mass * g
    D = 0.5 * rho * V ** 2 * fA                     # drag of the airframe
    T = np.hypot(Wt, D); alpha = np.arctan2(D, Wt)  # thrust and tilt
    Pi_h = Wt * np.sqrt(Wt / (2 * rho * A))         # ideal hover power
    Pi = KAPPA * T * induced_velocity(T, V, alpha, rho)
    P0 = (1 / FM - KAPPA) * Pi_h * (1 + K_P * (V / V_TIP) ** 2)
    Pp = D * V
    return np.array([Pi, P0, Pp]) / eta

# calibration to the manufacturer's figures: hover power sets the drive efficiency, power at 9 m/s the drag area
P_hover, P_test = E_BAT / (T_HOVER / 60), E_BAT / (T_FLIGHT / 60)
eta = W * np.sqrt(W / (2 * RHO0 * A)) / FM / P_hover
fA = brentq(lambda f: power(V_TEST, RHO0, f, eta).sum() - P_test, 1e-5, 0.5)
print(f"power from endurance: hover {P_hover:.1f} W, flight at {V_TEST:.0f} m/s {P_test:.1f} W")
print(f"calibration: drive and electronics efficiency η = {eta:.2f}, equivalent drag area f = Cd·S = {fA * 1e4:.0f} cm²")
''')),
        ("code", t('''
Vs = np.arange(0, 21.5, 0.5)
curve = pd.DataFrame([power(V, RHO0, fA, eta) for V in Vs], index=Vs, columns=["indukovaný", "profilový", "škodlivý"])
curve["celkem"] = curve.sum(axis=1)
V_end = curve["celkem"].idxmin()
V_rng = (curve["celkem"] / curve.index.to_series().replace(0, np.nan)).idxmin()
ax = curve.plot(figsize=(9, 4)); ax.axvline(V_TEST, color="gray", ls=":")
ax.set(xlabel="rychlost vůči vzduchu (m/s)", ylabel="elektrický výkon (W)", title="Mavic 3E, ρ = 1,225 kg/m³"); plt.show()
print(f"nejmenší výkon {curve['celkem'].min():.0f} W při {V_end:.1f} m/s → výdrž {E_BAT / curve['celkem'].min() * 60:.0f} min")
print(f"nejmenší energie na km {curve['celkem'][V_rng] / V_rng / 3.6:.2f} Wh/km při {V_rng:.1f} m/s → dolet {E_BAT / (curve['celkem'][V_rng] / V_rng / 3.6):.1f} km")
curve.iloc[::4].round(1)
''', '''
Vs = np.arange(0, 21.5, 0.5)
curve = pd.DataFrame([power(V, RHO0, fA, eta) for V in Vs], index=Vs, columns=["induced", "profile", "parasite"])
curve["total"] = curve.sum(axis=1)
V_end = curve["total"].idxmin()
V_rng = (curve["total"] / curve.index.to_series().replace(0, np.nan)).idxmin()
ax = curve.plot(figsize=(9, 4)); ax.axvline(V_TEST, color="gray", ls=":")
ax.set(xlabel="airspeed (m/s)", ylabel="electrical power (W)", title="Mavic 3E, ρ = 1.225 kg/m³"); plt.show()
print(f"minimum power {curve['total'].min():.0f} W at {V_end:.1f} m/s → endurance {E_BAT / curve['total'].min() * 60:.0f} min")
print(f"minimum energy per km {curve['total'][V_rng] / V_rng / 3.6:.2f} Wh/km at {V_rng:.1f} m/s → range {E_BAT / (curve['total'][V_rng] / V_rng / 3.6):.1f} km")
curve.iloc[::4].round(1)
''')),
        ("task", t(
            "Proč indukovaný výkon s rychlostí klesá a škodlivý roste? Při jaké rychlosti má dron nejdelší výdrž a při jaké největší dolet, a proč to nejsou stejné rychlosti? Je ekvivalentní plocha odporu f věrohodná pro dron velikosti Mavicu (odhadni čelní plochu trupu a součinitel odporu kolem 1)? Změň `FM` na 0,5 a 0,7: jak se změní kalibrace a výsledné rychlosti?",
            "Why does induced power decrease with speed and parasite power increase? At what speed does the drone have the longest endurance and at what speed the greatest range, and why are these not the same speed? Is the equivalent drag area f plausible for a drone the size of a Mavic (estimate the frontal area of the airframe and a drag coefficient of about 1)? Change `FM` to 0.5 and 0.7: how do the calibration and the resulting speeds change?")),
        ("md", t(
            "## 3. Let proti větru\n\nPři protivětru se počítá energie na kilometr vůči zemi: výkon dělený rychlostí vůči zemi (V − vítr). Tabulka ukazuje nejlepší rychlost vůči vzduchu pro různý protivítr a srovnání se stálými 9 m/s.",
            "## 3. Flying against the wind\n\nWith a headwind what counts is the energy per kilometre over the ground: power divided by the ground speed (V − wind). The table shows the best airspeed for different headwinds and a comparison with a constant 9 m/s.")),
        ("code", t('''
rows = []
for wind in [0, 3, 6, 9, 12]:                      # vítr proti směru letu (m/s)
    Vv = Vs[Vs > wind + 0.5]
    e = np.array([power(V, RHO0, fA, eta).sum() / (V - wind) / 3.6 for V in Vv])   # Wh na km vůči zemi
    k = e.argmin()
    rows.append({"protivítr (m/s)": wind, "nejlepší rychlost vůči vzduchu (m/s)": Vv[k], "rychlost vůči zemi (m/s)": Vv[k] - wind,
                 "energie (Wh/km)": e[k], "při stálých 9 m/s (Wh/km)": power(9, RHO0, fA, eta).sum() / (9 - wind) / 3.6 if wind < 9 else np.inf})
pd.DataFrame(rows).set_index("protivítr (m/s)").round(2)
''', '''
rows = []
for wind in [0, 3, 6, 9, 12]:                      # wind against the flight direction (m/s)
    Vv = Vs[Vs > wind + 0.5]
    e = np.array([power(V, RHO0, fA, eta).sum() / (V - wind) / 3.6 for V in Vv])   # Wh per km over the ground
    k = e.argmin()
    rows.append({"headwind (m/s)": wind, "best airspeed (m/s)": Vv[k], "ground speed (m/s)": Vv[k] - wind,
                 "energy (Wh/km)": e[k], "at a constant 9 m/s (Wh/km)": power(9, RHO0, fA, eta).sum() / (9 - wind) / 3.6 if wind < 9 else np.inf})
pd.DataFrame(rows).set_index("headwind (m/s)").round(2)
''')),
        ("task", t(
            "Proč má dron při protivětru letět rychleji vůči vzduchu, i když tím roste výkon? Kolikrát víc energie na kilometr spotřebuje návrat proti větru 6 m/s, když letí optimální rychlostí, a kolikrát, když drží 9 m/s? Při jakém větru přestane stačit normální režim s rychlostí 15 m/s?",
            "Why should the drone fly faster through the air in a headwind, although power increases? How many times more energy per kilometre does a return against a 6 m/s wind use at the optimum speed, and how many times at a constant 9 m/s? At what wind does the normal mode with 15 m/s stop being enough?")),
        ("md", t(
            "## 4. Skutečný vítr za poslední tři měsíce\n\nZ Open-Meteo stáhneme hodinový vítr v 10 a 120 m a počasí za 92 dní pro Roztoky a vybereme denní hodiny 8–18 h. Pro každou hodinu spočítáme energii na kilometr návratu, kdyby celý vítr ve 120 m foukal proti.",
            "## 4. Real wind over the last three months\n\nFrom Open-Meteo we download the hourly wind at 10 and 120 m and the weather for 92 days for Roztoky and keep the daytime hours 8–18 h. For each hour we compute the energy per kilometre of a return if all of the wind at 120 m blew against it.")),
        ("code", t('''
LAT, LON = 50.152, 14.392           # ◀ parametr: místo (Roztoky)
w = open_meteo({"latitude": LAT, "longitude": LON, "past_days": 92, "forecast_days": 1, "wind_speed_unit": "ms",
                "hourly": "wind_speed_10m,wind_speed_120m,temperature_2m,relative_humidity_2m,surface_pressure", "timezone": "Europe/Prague"})
met = pd.DataFrame(w["hourly"]).set_index("time"); met.index = pd.to_datetime(met.index)
day = met[(met.index.hour >= 8) & (met.index.hour <= 18)].dropna()   # jen hodiny, kdy se obvykle létá
WIND_LIMIT = 12.0                   # ◀ parametr: odolnost vůči větru podle výrobce (m/s)
print(f"{len(day)} denních hodin s daty za 92 dní, vítr ve 120 m: medián {day.wind_speed_120m.median():.1f} m/s, 90. percentil {day.wind_speed_120m.quantile(0.9):.1f} m/s")
for thr in [6, 9, WIND_LIMIT]:
    print(f"  vítr ve 120 m nad {thr:4.1f} m/s: {np.mean(day.wind_speed_120m > thr):5.1%} hodin, v 10 m: {np.mean(day.wind_speed_10m > thr):5.1%}")
best = {wv: min(power(V, RHO0, fA, eta).sum() / (V - wv) / 3.6 for V in Vs[Vs > wv + 0.5]) for wv in np.arange(0, 16, 0.5)}
e_back = np.interp(day.wind_speed_120m, list(best), list(best.values()))
print(f"energie na km návratu proti větru ve 120 m: medián {np.median(e_back):.2f} Wh/km, 90. percentil {np.percentile(e_back, 90):.2f} Wh/km (bez větru {best[0]:.2f})")
plt.figure(figsize=(9, 3.2)); plt.hist([day.wind_speed_10m, day.wind_speed_120m], bins=np.arange(0, 20, 1), label=["10 m", "120 m"])
plt.axvline(WIND_LIMIT, color="r", ls=":"); plt.xlabel("rychlost větru (m/s)"); plt.ylabel("hodin"); plt.legend(); plt.show()
''', '''
LAT, LON = 50.152, 14.392           # ◀ parameter: site (Roztoky)
w = open_meteo({"latitude": LAT, "longitude": LON, "past_days": 92, "forecast_days": 1, "wind_speed_unit": "ms",
                "hourly": "wind_speed_10m,wind_speed_120m,temperature_2m,relative_humidity_2m,surface_pressure", "timezone": "Europe/Prague"})
met = pd.DataFrame(w["hourly"]).set_index("time"); met.index = pd.to_datetime(met.index)
day = met[(met.index.hour >= 8) & (met.index.hour <= 18)].dropna()   # only the hours when people usually fly
WIND_LIMIT = 12.0                   # ◀ parameter: wind resistance according to the manufacturer (m/s)
print(f"{len(day)} daytime hours with data in 92 days, wind at 120 m: median {day.wind_speed_120m.median():.1f} m/s, 90th percentile {day.wind_speed_120m.quantile(0.9):.1f} m/s")
for thr in [6, 9, WIND_LIMIT]:
    print(f"  wind at 120 m above {thr:4.1f} m/s: {np.mean(day.wind_speed_120m > thr):5.1%} of hours, at 10 m: {np.mean(day.wind_speed_10m > thr):5.1%}")
best = {wv: min(power(V, RHO0, fA, eta).sum() / (V - wv) / 3.6 for V in Vs[Vs > wv + 0.5]) for wv in np.arange(0, 16, 0.5)}
e_back = np.interp(day.wind_speed_120m, list(best), list(best.values()))
print(f"energy per km of a return against the wind at 120 m: median {np.median(e_back):.2f} Wh/km, 90th percentile {np.percentile(e_back, 90):.2f} Wh/km (no wind {best[0]:.2f})")
plt.figure(figsize=(9, 3.2)); plt.hist([day.wind_speed_10m, day.wind_speed_120m], bins=np.arange(0, 20, 1), label=["10 m", "120 m"])
plt.axvline(WIND_LIMIT, color="r", ls=":"); plt.xlabel("wind speed (m/s)"); plt.ylabel("hours"); plt.legend(); plt.show()
''')),
        ("task", t(
            "Jak se liší vítr v 10 a ve 120 m a co to znamená, když vítr odhaduješ u země před vzletem? V kolika procentech denních hodin by vítr ve 120 m překročil odolnost dronu? O kolik procent víc energie na kilometr spotřebuje typický návrat proti větru proti bezvětří a co z toho plyne pro rezervu baterie?",
            "How does the wind at 10 m differ from the wind at 120 m, and what does that mean when you judge the wind on the ground before take-off? In what percentage of daytime hours would the wind at 120 m exceed the drone's wind resistance? How many per cent more energy per kilometre does a typical return against the wind use compared with calm air, and what follows for the battery reserve?")),
        ("md", t(
            "## 5. Hustota vzduchu\n\nZ tlaku, teploty a vlhkosti spočítáme hustotu vzduchu v Roztokách za stejných 92 dní a přidáme hustotu pro vysoké hory. Předpokládáme, že účinnost rotoru FM a pohonu η se s hustotou nemění.",
            "## 5. Air density\n\nFrom pressure, temperature and humidity we compute the air density at Roztoky over the same 92 days and add a density for high mountains. We assume that the rotor figure of merit FM and the drive efficiency η do not change with density.")),
        ("code", t('''
met = met.dropna()
T = met.temperature_2m + 273.15
e_v = met.relative_humidity_2m / 100 * 6.112 * np.exp(17.62 * met.temperature_2m / (243.12 + met.temperature_2m))
rho = met.surface_pressure * 100 / (287.05 * T / (1 - 0.378 * e_v / met.surface_pressure))
RHO_MOUNTAIN = 0.90                 # ◀ parametr: hustota pro vysoké hory (kg/m³), zhruba 2600 m n. m.
cases = {"nejhustší (Roztoky)": rho.max(), "nejřidší (Roztoky)": rho.min(), "hory": RHO_MOUNTAIN}
rows = {}
for name, r in cases.items():
    P = np.array([power(V, r, fA, eta).sum() for V in Vs])
    k_end, k_rng = P.argmin(), (P[1:] / Vs[1:]).argmin() + 1
    rows[name] = {"ρ (kg/m³)": r, "visení (W)": P[0], "visení (min)": E_BAT / P[0] * 60, "nejmenší výkon (W)": P[k_end],
                  "rychlost nejdelší výdrže (m/s)": Vs[k_end], "rychlost největšího doletu (m/s)": Vs[k_rng], "dolet (km)": E_BAT / (P[k_rng] / Vs[k_rng] / 3.6)}
pd.DataFrame(rows).T.round(2)
''', '''
met = met.dropna()
T = met.temperature_2m + 273.15
e_v = met.relative_humidity_2m / 100 * 6.112 * np.exp(17.62 * met.temperature_2m / (243.12 + met.temperature_2m))
rho = met.surface_pressure * 100 / (287.05 * T / (1 - 0.378 * e_v / met.surface_pressure))
RHO_MOUNTAIN = 0.90                 # ◀ parameter: density for high mountains (kg/m³), roughly 2600 m a.s.l.
cases = {"densest (Roztoky)": rho.max(), "thinnest (Roztoky)": rho.min(), "mountains": RHO_MOUNTAIN}
rows = {}
for name, r in cases.items():
    P = np.array([power(V, r, fA, eta).sum() for V in Vs])
    k_end, k_rng = P.argmin(), (P[1:] / Vs[1:]).argmin() + 1
    rows[name] = {"ρ (kg/m³)": r, "hover (W)": P[0], "hover (min)": E_BAT / P[0] * 60, "minimum power (W)": P[k_end],
                  "max-endurance speed (m/s)": Vs[k_end], "max-range speed (m/s)": Vs[k_rng], "range (km)": E_BAT / (P[k_rng] / Vs[k_rng] / 3.6)}
pd.DataFrame(rows).T.round(2)
''')),
        ("task", t(
            "O kolik se v řidším vzduchu zkrátí doba visení a jak se posunou rychlosti nejdelší výdrže a největšího doletu? Proč se dolet v horách téměř nemění, i když výkon roste? (Porovnej, jak na hustotě závisí indukovaný a škodlivý výkon.) Co by se stalo, kdyby dron ve stejných horách nesl náklad, který zvýší hmotnost o 20 %? Zkus `m` v buňce modelu.",
            "By how much does hover time shorten in thinner air, and how do the speeds for maximum endurance and maximum range shift? Why does the range in the mountains hardly change although power increases? (Compare how induced and parasite power depend on density.) What would happen if the drone carried a payload in the same mountains that increased its mass by 20 %? Try `m` in the model cell.")),
        ("md", t(
            "## 6. Visení těsně nad zemí\n\nBlízko země se proud pod rotorem nemůže volně rozšířit, indukovaná rychlost klesne a stejný tah stojí méně výkonu. Cheeseman a Bennett (1955) to popsali vztahem v_IGE / v_OGE = 1 − (R / 4z)², kde z je výška rotoru nad zemí. Vztah platí pro jeden rotor; u kvadrokoptéry se proudy čtyř vrtulí navíc ovlivňují.",
            "## 6. Hovering close to the ground\n\nClose to the ground the wake under the rotor cannot expand freely, the induced velocity drops and the same thrust needs less power. Cheeseman and Bennett (1955) described this as v_IGE / v_OGE = 1 − (R / 4z)², where z is the rotor height above the ground. The relation holds for a single rotor; with a quadcopter the wakes of the four propellers also interact.")),
        ("code", t('''
def ground_factor(z):
    """Cheeseman a Bennett (1955): poměr indukované rychlosti v blízkosti země a mimo ni při stejném tahu."""
    return np.clip(1 - (R / (4 * z)) ** 2, 0, 1)

rows = []
Pi_h, P0_h, _ = power(0, RHO0, fA, eta)
for zR in [0.5, 0.75, 1, 1.5, 2, 3, 5]:          # výška rotoru nad zemí v poloměrech
    k = ground_factor(zR * R)
    P = Pi_h * k + P0_h
    rows.append({"z / R": zR, "z (cm)": zR * R * 100, "indukovaná rychlost (% mimo zem)": k * 100, "výkon (W)": P, "úspora výkonu (%)": (1 - P / (Pi_h + P0_h)) * 100})
pd.DataFrame(rows).set_index("z / R").round(1)
''', '''
def ground_factor(z):
    """Cheeseman and Bennett (1955): ratio of induced velocity near the ground to that out of ground effect at equal thrust."""
    return np.clip(1 - (R / (4 * z)) ** 2, 0, 1)

rows = []
Pi_h, P0_h, _ = power(0, RHO0, fA, eta)
for zR in [0.5, 0.75, 1, 1.5, 2, 3, 5]:          # rotor height above the ground in radii
    k = ground_factor(zR * R)
    P = Pi_h * k + P0_h
    rows.append({"z / R": zR, "z (cm)": zR * R * 100, "induced velocity (% of free air)": k * 100, "power (W)": P, "power saving (%)": (1 - P / (Pi_h + P0_h)) * 100})
pd.DataFrame(rows).set_index("z / R").round(1)
''')),
        ("task", t(
            "Do jaké výšky nad zemí je vliv země u Mavicu znatelný (úspora výkonu nad 2 %)? Proč dron při přistání těsně nad zemí „plave“ a proč je to u velkých vrtulí výraznější v metrech? Proč ti vliv země nepomůže při letu nad vysokou vegetací nebo nad vodou se zvlněnou hladinou stejně jako nad betonem?",
            "Up to what height above the ground is ground effect noticeable for the Mavic (power saving above 2 %)? Why does the drone \"float\" just above the ground when landing, and why is this more pronounced in metres for large propellers? Why does ground effect not help you over tall vegetation or over rippled water as much as over concrete?")),
        ("task", t(
            "+ Uprav model na Matrice 350 RTK (hmotnost 6,47 kg, vrtule 21″, baterie 2 × 263 Wh). Výrobce udává 55 min letu bez nákladu; doplň `T_FLIGHT`, odhadni `T_HOVER` a sleduj, jak výdrž klesá s nákladem až do maximální vzletové hmotnosti 9,2 kg.",
            "+ Adapt the model to the Matrice 350 RTK (mass 6.47 kg, 21″ propellers, battery 2 × 263 Wh). The manufacturer states 55 min of flight without payload; fill in `T_FLIGHT`, estimate `T_HOVER` and watch how endurance falls with payload up to the maximum take-off mass of 9.2 kg.")),
    ]
