from _common import OPEN_METEO_HELPER

META = {
    "version": "1.0",
    "minutes": 45,
    "title": {"cs": "Můžu letět? Skutečné zprávy METAR a vítr ve výšce letu", "en": "Can I fly? Real METAR reports and wind at flight height"},
    "visual": {"cs": "Můžu letět? Počasí pro drony", "en": "Can I fly? Weather for drones"},
    "lead": {
        "cs": "Ve vizuálu jsi dekódoval ukázkové zprávy METAR, přepočítal vítr z letiště na místo a výšku letu a rozhodoval podle semaforu. Tady stáhneš skutečné zprávy METAR z českých letišť za posledních 24 hodin, sám je dekóduješ a výsledek porovnáš s modelovou předpovědí větru ve 80 a 120 m.",
        "en": "In the visual you decoded example METAR reports, converted the airport wind to the flight site and height and decided with a traffic light. Here you download real METAR reports from Czech airports for the last 24 hours, decode them yourself and compare the result with a model forecast of wind at 80 and 120 m.",
    },
    "goal": {
        "cs": "dekódovat METAR, spočítat relativní vlhkost a odhad základny oblačnosti, přepočítat vítr v 10 m na výšku letu nad jiným terénem, odhadnout návrat proti větru a rozhodnout o letu na příštích 24 hodin.",
        "en": "decode METAR, compute relative humidity and an estimate of the cloud base, convert the 10 m wind to flight height over different terrain, estimate the return against the wind, and decide about flying over the next 24 hours.",
    },
    "data": {
        "cs": "zprávy METAR a TAF z letišť Praha (LKPR), Brno (LKTB), Ostrava (LKMT) a Karlovy Vary (LKKV) ze služby NOAA Aviation Weather Center; hodinová předpověď z Open-Meteo pro Roztoky u Prahy. Data se mění každou půlhodinu, tvoje čísla budou jiná než v uloženém notebooku.",
        "en": "METAR and TAF reports from Prague (LKPR), Brno (LKTB), Ostrava (LKMT) and Karlovy Vary (LKKV) airports from the NOAA Aviation Weather Center; an hourly forecast from Open-Meteo for Roztoky u Prahy. The data change every half hour, so your numbers will differ from the stored notebook.",
    },
    "sources": {
        "cs": [
            "METAR a TAF: NOAA/NWS Aviation Weather Center, https://aviationweather.gov/data/api/ (veřejná data vlády USA).",
            "Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "Relativní vlhkost a tlak nasycených par (Magnusův vzorec): WMO (2018). *Guide to Instruments and Methods of Observation* (WMO-No. 8), příloha 4.B.",
            "Přenos větru přes výšku promíchání 60 m: Wieringa, J. (1986). Roughness-dependent geographical interpolation of surface wind speed averages. *Quarterly Journal of the Royal Meteorological Society* 112, 867–889; Verkaik, J. W. (2000). Evaluation of two gustiness models for exposure correction calculations. *Journal of Applied Meteorology* 39, 1613–1626.",
            "Klíč ke zprávám METAR: ICAO Annex 3 / WMO-No. 306, kód FM 15.",
            "Odolnost DJI Mavic 3 Enterprise vůči větru 12 m/s, max. rychlost 15 m/s v normálním režimu, 21 m/s ve sportovním (technický list DJI); odolnost DJI Mini 4 Pro vůči větru 10,7 m/s.",
        ],
        "en": [
            "METAR and TAF: NOAA/NWS Aviation Weather Center, https://aviationweather.gov/data/api/ (US government public data).",
            "Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "Relative humidity and saturation vapour pressure (Magnus formula): WMO (2018). *Guide to Instruments and Methods of Observation* (WMO-No. 8), annex 4.B.",
            "Wind transfer via a 60 m blending height: Wieringa, J. (1986). Roughness-dependent geographical interpolation of surface wind speed averages. *Quarterly Journal of the Royal Meteorological Society* 112, 867–889; Verkaik, J. W. (2000). Evaluation of two gustiness models for exposure correction calculations. *Journal of Applied Meteorology* 39, 1613–1626.",
            "METAR code: ICAO Annex 3 / WMO-No. 306, code FM 15.",
            "DJI Mavic 3 Enterprise wind resistance 12 m/s, max. speed 15 m/s in normal mode, 21 m/s in sport mode (DJI data sheet); DJI Mini 4 Pro wind resistance 10.7 m/s.",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a skutečné zprávy METAR", "## 1. Setup and real METAR reports")),
        ("code", '''
import re, time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
''' + t(OPEN_METEO_HELPER["cs"], OPEN_METEO_HELPER["en"])),
        ("code", t('''
STATIONS = "LKPR,LKTB,LKMT,LKKV"          # ◀ parametr: kódy letišť ICAO
raw = requests.get("https://aviationweather.gov/api/data/metar", params={"ids": STATIONS, "format": "raw", "hours": 24}, timeout=60).text.strip().splitlines()
taf = requests.get("https://aviationweather.gov/api/data/taf", params={"ids": "LKPR", "format": "raw"}, timeout=60).text.strip()
print(f"{len(raw)} zpráv; nejnovější:"); print("\\n".join(raw[:6])); print("\\nTAF Praha:\\n" + taf)
''', '''
STATIONS = "LKPR,LKTB,LKMT,LKKV"          # ◀ parameter: ICAO airport codes
raw = requests.get("https://aviationweather.gov/api/data/metar", params={"ids": STATIONS, "format": "raw", "hours": 24}, timeout=60).text.strip().splitlines()
taf = requests.get("https://aviationweather.gov/api/data/taf", params={"ids": "LKPR", "format": "raw"}, timeout=60).text.strip()
print(f"{len(raw)} reports; latest:"); print("\\n".join(raw[:6])); print("\\nTAF Prague:\\n" + taf)
''')),
        ("md", t(
            "## 2. Vlastní dekodér\n\nZpráva má pevné pořadí skupin: letiště, čas, vítr (směr, rychlost, nárazy G), dohlednost v metrech nebo CAVOK, jevy (RA déšť, SN sníh, BR kouřmo, FG mlha, - slabý, + silný), oblačnost (FEW, SCT, BKN, OVC a výška ve stovkách stop), teplota/rosný bod (M = minus) a tlak QNH. Část za TEMPO, BECMG nebo NOSIG je krátká předpověď a dekodér ji vynechá.",
            "## 2. Your own decoder\n\nA report has a fixed order of groups: airport, time, wind (direction, speed, gusts G), visibility in metres or CAVOK, weather (RA rain, SN snow, BR mist, FG fog, - light, + heavy), cloud (FEW, SCT, BKN, OVC and height in hundreds of feet), temperature/dew point (M = minus) and QNH pressure. The part after TEMPO, BECMG or NOSIG is a short trend forecast and the decoder skips it.")),
        ("code", t('''
KT = 0.514444
def decode(m):
    body = re.split(r"\\b(TEMPO|BECMG|NOSIG|RMK)\\b", m)[0]
    d = {"stanice": body.split()[1], "čas": re.search(r"\\b(\\d{6})Z\\b", body).group(1)}
    w = re.search(r"\\b(\\d{3}|VRB)(\\d{2,3})(?:G(\\d{2,3}))?(KT|MPS)\\b", body)
    if w:
        f = KT if w.group(4) == "KT" else 1.0
        d["směr"] = w.group(1); d["vítr m/s"] = int(w.group(2)) * f; d["nárazy m/s"] = int(w.group(3)) * f if w.group(3) else np.nan
    if "CAVOK" in body:
        d["dohlednost m"] = 10000
    else:
        v = re.search(r"(?<=KT )(\\d{4})\\b|(?<=MPS )(\\d{4})\\b|\\s(\\d{4})\\s", body)
        d["dohlednost m"] = int(next(g for g in v.groups() if g)) if v else np.nan
    d["jevy"] = " ".join(re.findall(r"(?<=\\s)([-+]?(?:VC)?(?:MI|BC|PR|DR|BL|SH|TS|FZ)?(?:DZ|RA|SN|SG|PL|GR|GS|BR|FG|FU|HZ|SQ)+)(?=\\s)", body + " "))
    clouds = re.findall(r"\\b(FEW|SCT|BKN|OVC|VV)(\\d{3})", body)
    d["oblačnost"] = " ".join(f"{c}{int(h) * 100}ft" for c, h in clouds)
    ceil = [int(h) * 100 * 0.3048 for c, h in clouds if c in ("BKN", "OVC", "VV")]
    d["základna BKN/OVC m"] = min(ceil) if ceil else np.nan
    tt = re.search(r"\\b(M?\\d{2})/(M?\\d{2})\\b", body)
    if tt:
        d["T °C"], d["Td °C"] = (int(x.replace("M", "-")) for x in tt.groups())
    return d

met = pd.DataFrame([decode(m) for m in raw])
met["RH %"] = 100 * np.exp(17.62 * met["Td °C"] / (243.12 + met["Td °C"])) / np.exp(17.62 * met["T °C"] / (243.12 + met["T °C"]))
met["odhad základny m"] = 125 * (met["T °C"] - met["Td °C"])
met.head(12).round(1)
''', '''
KT = 0.514444
def decode(m):
    body = re.split(r"\\b(TEMPO|BECMG|NOSIG|RMK)\\b", m)[0]
    d = {"station": body.split()[1], "time": re.search(r"\\b(\\d{6})Z\\b", body).group(1)}
    w = re.search(r"\\b(\\d{3}|VRB)(\\d{2,3})(?:G(\\d{2,3}))?(KT|MPS)\\b", body)
    if w:
        f = KT if w.group(4) == "KT" else 1.0
        d["dir"] = w.group(1); d["wind m/s"] = int(w.group(2)) * f; d["gusts m/s"] = int(w.group(3)) * f if w.group(3) else np.nan
    if "CAVOK" in body:
        d["visibility m"] = 10000
    else:
        v = re.search(r"(?<=KT )(\\d{4})\\b|(?<=MPS )(\\d{4})\\b|\\s(\\d{4})\\s", body)
        d["visibility m"] = int(next(g for g in v.groups() if g)) if v else np.nan
    d["weather"] = " ".join(re.findall(r"(?<=\\s)([-+]?(?:VC)?(?:MI|BC|PR|DR|BL|SH|TS|FZ)?(?:DZ|RA|SN|SG|PL|GR|GS|BR|FG|FU|HZ|SQ)+)(?=\\s)", body + " "))
    clouds = re.findall(r"\\b(FEW|SCT|BKN|OVC|VV)(\\d{3})", body)
    d["cloud"] = " ".join(f"{c}{int(h) * 100}ft" for c, h in clouds)
    ceil = [int(h) * 100 * 0.3048 for c, h in clouds if c in ("BKN", "OVC", "VV")]
    d["BKN/OVC base m"] = min(ceil) if ceil else np.nan
    tt = re.search(r"\\b(M?\\d{2})/(M?\\d{2})\\b", body)
    if tt:
        d["T °C"], d["Td °C"] = (int(x.replace("M", "-")) for x in tt.groups())
    return d

met = pd.DataFrame([decode(m) for m in raw])
met["RH %"] = 100 * np.exp(17.62 * met["Td °C"] / (243.12 + met["Td °C"])) / np.exp(17.62 * met["T °C"] / (243.12 + met["T °C"]))
met["estimated base m"] = 125 * (met["T °C"] - met["Td °C"])
met.head(12).round(1)
''')),
        ("task", t(
            "Vyber si jednu zprávu a dekóduj ji ručně skupinu po skupině; souhlasí s tabulkou? Které skupiny by samy o sobě vyloučily let VLOS (dohlednost, mlha, nízká oblačnost, srážky)? Proč je pro pilota důležitější rozdíl T − Td než samotná teplota?",
            "Pick one report and decode it by hand group by group; does it agree with the table? Which groups alone would rule out a VLOS flight (visibility, fog, low cloud, precipitation)? Why is the difference T − Td more important to a pilot than the temperature alone?")),
        ("code", t('''
c = met.dropna(subset=["základna BKN/OVC m"])
plt.figure(figsize=(5, 4.5))
plt.scatter(c["odhad základny m"], c["základna BKN/OVC m"])
plt.axline((0, 0), slope=1, color="gray", ls=":")
plt.xlabel("125 m · (T − Td)"); plt.ylabel("nahlášená základna BKN/OVC (m)"); plt.title(f"{len(c)} zpráv s oblačností BKN/OVC"); plt.show()
''', '''
c = met.dropna(subset=["BKN/OVC base m"])
plt.figure(figsize=(5, 4.5))
plt.scatter(c["estimated base m"], c["BKN/OVC base m"])
plt.axline((0, 0), slope=1, color="gray", ls=":")
plt.xlabel("125 m · (T − Td)"); plt.ylabel("reported BKN/OVC base (m)"); plt.title(f"{len(c)} reports with BKN/OVC cloud"); plt.show()
''')),
        ("task", t(
            "Jak dobře odhad 125 m · (T − Td) odpovídá skutečně nahlášené základně? Odhad platí pro kupovitou oblačnost v dobře promíchané vrstvě za dne. Najdi zprávy, kde selhává, a vysvětli proč (noc, vrstevnatá oblačnost, inverze, oblačnost z jiné vzduchové hmoty).",
            "How well does the estimate 125 m · (T − Td) match the reported cloud base? The estimate holds for cumulus in a well-mixed daytime layer. Find reports where it fails and explain why (night, stratiform cloud, inversion, cloud from another air mass).")),
        ("md", t(
            "## 3. Vítr ve výšce letu nad jiným terénem\n\nLetiště měří vítr v 10 m nad trávou (délka drsnosti z0 = 0,03 m). Ve výšce promíchání 60 m je vliv povrchu malý, tam vítr přeneseme na místo letu s jinou drsností z0 a posunutím nulové roviny d (Wieringa 1986). Platí pro neutrální zvrstvení (vítr, oblačno); za slunečného dne nebo v noci se profil liší.",
            "## 3. Wind at flight height over different terrain\n\nAirports measure wind 10 m above grass (roughness length z0 = 0.03 m). At a blending height of 60 m the surface hardly matters, so we transfer the wind there to the flight site with a different roughness z0 and zero-plane displacement d (Wieringa 1986). This holds for neutral stratification (windy, overcast); on a sunny day or at night the profile differs.")),
        ("code", t('''
def wind_at(z, u10, z0=0.03, d=0.0, zb=60.0):
    ub = u10 * np.log(zb / 0.03) / np.log(10 / 0.03)                    # vítr ve výšce promíchání nad letištěm
    z = np.asarray(z, float)
    site = ub * np.log(np.maximum(z - d, z0 * 1.01) / z0) / np.log((zb - d) / z0)
    above = ub * np.log(z / 0.03) / np.log(zb / 0.03)
    return np.where(z <= zb, site, above)

TERRAIN = {"voda": (0.0002, 0), "pole, tráva": (0.03, 0), "předměstí": (0.5, 6), "les 25 m": (2.5, 17)}
u10 = float(met[met["stanice"] == "LKPR"]["vítr m/s"].iloc[0])     # ◀ parametr: vítr v 10 m (výchozí je poslední METAR z Prahy)
z = np.linspace(1, 150, 300)
plt.figure(figsize=(6, 4.5))
for name, (z0, d) in TERRAIN.items():
    plt.plot(wind_at(z, u10, z0, d), z, label=f"{name} (z0 = {z0} m, d = {d} m)")
plt.axhline(60, color="gray", ls=":"); plt.xlabel("průměrný vítr (m/s)"); plt.ylabel("výška nad terénem (m)")
plt.title(f"vítr v 10 m na letišti {u10:.1f} m/s"); plt.legend(fontsize=8); plt.show()
for name, (z0, d) in TERRAIN.items():
    print(f"{name:12s}: 30 m {wind_at(30, u10, z0, d):4.1f} m/s, 100 m {wind_at(100, u10, z0, d):4.1f} m/s")
''', '''
def wind_at(z, u10, z0=0.03, d=0.0, zb=60.0):
    ub = u10 * np.log(zb / 0.03) / np.log(10 / 0.03)                    # wind at the blending height above the airport
    z = np.asarray(z, float)
    site = ub * np.log(np.maximum(z - d, z0 * 1.01) / z0) / np.log((zb - d) / z0)
    above = ub * np.log(z / 0.03) / np.log(zb / 0.03)
    return np.where(z <= zb, site, above)

TERRAIN = {"water": (0.0002, 0), "field, grass": (0.03, 0), "suburb": (0.5, 6), "forest 25 m": (2.5, 17)}
u10 = float(met[met["station"] == "LKPR"]["wind m/s"].iloc[0])     # ◀ parameter: wind at 10 m (default is the latest Prague METAR)
z = np.linspace(1, 150, 300)
plt.figure(figsize=(6, 4.5))
for name, (z0, d) in TERRAIN.items():
    plt.plot(wind_at(z, u10, z0, d), z, label=f"{name} (z0 = {z0} m, d = {d} m)")
plt.axhline(60, color="gray", ls=":"); plt.xlabel("mean wind (m/s)"); plt.ylabel("height above terrain (m)")
plt.title(f"10 m airport wind {u10:.1f} m/s"); plt.legend(fontsize=8); plt.show()
for name, (z0, d) in TERRAIN.items():
    print(f"{name:12s}: 30 m {wind_at(30, u10, z0, d):4.1f} m/s, 100 m {wind_at(100, u10, z0, d):4.1f} m/s")
''')),
        ("code", t('''
fc = open_meteo({"latitude": 50.152, "longitude": 14.392, "forecast_days": 2, "wind_speed_unit": "ms", "timezone": "Europe/Prague",
                 "hourly": "wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_gusts_10m,temperature_2m,dew_point_2m,visibility,precipitation"})
fc = pd.DataFrame(fc["hourly"]).set_index("time")
ratio80 = (fc.wind_speed_80m / fc.wind_speed_10m)[fc.wind_speed_10m > 2]
print(f"Open-Meteo pro Roztoky: poměr větru 80 m / 10 m medián {ratio80.median():.2f} (rozsah {ratio80.min():.2f}–{ratio80.max():.2f})")
print(f"náš profil nad polem: {wind_at(80, 1.0, 0.03, 0) / 1.0:.2f}, nad předměstím: {wind_at(80, 1.0, 0.5, 6) / wind_at(10, 1.0, 0.5, 6):.2f}")
''', '''
fc = open_meteo({"latitude": 50.152, "longitude": 14.392, "forecast_days": 2, "wind_speed_unit": "ms", "timezone": "Europe/Prague",
                 "hourly": "wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_gusts_10m,temperature_2m,dew_point_2m,visibility,precipitation"})
fc = pd.DataFrame(fc["hourly"]).set_index("time")
ratio80 = (fc.wind_speed_80m / fc.wind_speed_10m)[fc.wind_speed_10m > 2]
print(f"Open-Meteo for Roztoky: wind ratio 80 m / 10 m median {ratio80.median():.2f} (range {ratio80.min():.2f}–{ratio80.max():.2f})")
print(f"our profile over a field: {wind_at(80, 1.0, 0.03, 0) / 1.0:.2f}, over a suburb: {wind_at(80, 1.0, 0.5, 6) / wind_at(10, 1.0, 0.5, 6):.2f}")
''')),
        ("task", t(
            "Proč nad lesem vychází ve 30 m slabší průměrný vítr než nad vodou, ale ve 100 m skoro stejný? Kolega říká: „Letiště hlásí 6 m/s, dron snese 12 m/s, máme dvojnásobnou rezervu.“ Nastav `u10 = 6` a odpověz mu čísly pro výšku 100 m. Jak se poměr 80 m / 10 m z modelu Open-Meteo liší od našeho profilu a proč (zvrstvení během dne a noci)?",
            "Why is the mean wind at 30 m weaker over forest than over water, but almost the same at 100 m? A colleague says: \"The airport reports 6 m/s, the drone handles 12 m/s, we have a twofold margin.\" Set `u10 = 6` and answer with numbers for 100 m. How does the 80 m / 10 m ratio from the Open-Meteo model differ from our profile and why (stability during day and night)?")),
        ("md", t(
            "## 4. Cesta zpět proti větru\n\nDron letí vůči vzduchu rychlostí V, vítr ve výšce letu má rychlost U. Na trase D tam po větru a zpět proti větru trvá let t = D/(V + U) + D/(V − U).",
            "## 4. The way back against the wind\n\nThe drone flies at airspeed V, the wind at flight height is U. Over a distance D downwind out and upwind back the flight takes t = D/(V + U) + D/(V − U).")),
        ("code", t('''
V, D = 12.0, 800          # ◀ parametr: rychlost vůči vzduchu (m/s) a vzdálenost od pilota (m)
U = np.linspace(0, 11.5, 200)
t_rt = D / (V + U) + D / (V - U)
plt.figure(figsize=(7, 3.5)); plt.plot(U, t_rt / 60); plt.axhline(2 * D / V / 60 * 2, color="gray", ls=":", label="dvojnásobek času bez větru")
plt.xlabel("vítr ve výšce letu U (m/s)"); plt.ylabel("tam a zpět (min)"); plt.legend(); plt.show()
print(f"bez větru {2 * D / V / 60:.1f} min; dvojnásobek nastane při U = {V / np.sqrt(2):.1f} m/s")
''', '''
V, D = 12.0, 800          # ◀ parameter: airspeed (m/s) and distance from the pilot (m)
U = np.linspace(0, 11.5, 200)
t_rt = D / (V + U) + D / (V - U)
plt.figure(figsize=(7, 3.5)); plt.plot(U, t_rt / 60); plt.axhline(2 * D / V / 60 * 2, color="gray", ls=":", label="twice the no-wind time")
plt.xlabel("wind at flight height U (m/s)"); plt.ylabel("out and back (min)"); plt.legend(); plt.show()
print(f"no wind {2 * D / V / 60:.1f} min; doubled at U = {V / np.sqrt(2):.1f} m/s")
''')),
        ("task", t(
            "Odvoď ze vzorce, při jakém větru se čas tam a zpět zdvojnásobí (výsledek U = V/√2 vypisuje buňka). Proč nestačí, že průměrný vítr ve výšce letu je pod odolností dronu, když jsou nárazy (sloupec nárazy v METAR) o 30–50 % vyšší? Jak bys podle toho naplánoval trasu?",
            "Derive from the formula at what wind the round-trip time doubles (the cell prints U = V/√2). Why is it not enough that the mean wind at flight height is below the drone's wind resistance when gusts (the gust column in METAR) are 30–50 % higher? How would you plan the route accordingly?")),
        ("md", t(
            "## 5. Semafor na příštích 48 hodin\n\nPro každou hodinu předpovědi z Open-Meteo pro Roztoky rozhodneme: vítr ve 120 m a nárazy proti limitu dronu, srážky, dohlednost a riziko námrazy (teplota pod 1 °C a T − Td do 2 °C).",
            "## 5. A traffic light for the next 48 hours\n\nFor each hour of the Open-Meteo forecast for Roztoky we decide: wind at 120 m and gusts against the drone's limit, precipitation, visibility and icing risk (temperature below 1 °C and T − Td within 2 °C).")),
        ("code", t('''
limit = 12.0               # ◀ parametr: odolnost dronu vůči větru (m/s)
gust_factor = (fc.wind_gusts_10m / fc.wind_speed_10m.clip(lower=1)).clip(upper=2.5)
wind_fl = fc.wind_speed_120m
gust_fl = wind_fl * gust_factor
red = (gust_fl > limit) | (fc.precipitation > 0.5) | (fc.visibility < 1000)
icing = (fc.temperature_2m < 1) & (fc.temperature_2m - fc.dew_point_2m <= 2)
yellow = ~red & ((gust_fl > 0.75 * limit) | (fc.precipitation > 0) | (fc.visibility < 5000) | icing)
status = np.where(red, "NELETĚT", np.where(yellow, "pozor", "ok"))
out = pd.DataFrame({"vítr 120 m": wind_fl, "nárazy ~": gust_fl, "srážky mm": fc.precipitation, "dohlednost km": fc.visibility / 1000,
                    "T": fc.temperature_2m, "T−Td": fc.temperature_2m - fc.dew_point_2m, "verdikt": status}).round(1)
colors = {"ok": "#cfe8cf", "pozor": "#ffe7a3", "NELETĚT": "#f4b6b6"}
out.style.apply(lambda r: [f"background-color: {colors[r['verdikt']]}"] * len(r), axis=1)
''', '''
limit = 12.0               # ◀ parameter: drone wind resistance (m/s)
gust_factor = (fc.wind_gusts_10m / fc.wind_speed_10m.clip(lower=1)).clip(upper=2.5)
wind_fl = fc.wind_speed_120m
gust_fl = wind_fl * gust_factor
red = (gust_fl > limit) | (fc.precipitation > 0.5) | (fc.visibility < 1000)
icing = (fc.temperature_2m < 1) & (fc.temperature_2m - fc.dew_point_2m <= 2)
yellow = ~red & ((gust_fl > 0.75 * limit) | (fc.precipitation > 0) | (fc.visibility < 5000) | icing)
status = np.where(red, "NO GO", np.where(yellow, "caution", "ok"))
out = pd.DataFrame({"wind 120 m": wind_fl, "gusts ~": gust_fl, "precip. mm": fc.precipitation, "visibility km": fc.visibility / 1000,
                    "T": fc.temperature_2m, "T−Td": fc.temperature_2m - fc.dew_point_2m, "verdict": status}).round(1)
colors = {"ok": "#cfe8cf", "caution": "#ffe7a3", "NO GO": "#f4b6b6"}
out.style.apply(lambda r: [f"background-color: {colors[r['verdict']]}"] * len(r), axis=1)
''')),
        ("task", t(
            "Kdy bys v příštích 48 hodinách letěl a co v ostatních hodinách rozhoduje? Porovnej předpověď s posledním TAF pro Prahu: shodují se? Nárazy ve 120 m jsme odhadli poměrem nárazů a větru v 10 m; proč je to hrubé a proč je výsledek spíš na straně bezpečnosti, nebo naopak? Nastav `limit = 10.7` (odolnost malého dronu do 250 g, např. DJI Mini 4 Pro). Co se změní?",
            "When would you fly in the next 48 hours and what decides the other hours? Compare the forecast with the latest TAF for Prague: do they agree? We estimated gusts at 120 m from the gust-to-wind ratio at 10 m; why is that rough, and is the result on the safe side or not? Set `limit = 10.7` (wind resistance of a small sub-250 g drone such as the DJI Mini 4 Pro). What changes?")),
    ]
