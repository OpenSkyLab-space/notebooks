from _common import OPEN_METEO_HELPER

META = {
    "version": "1.0",
    "minutes": 50,
    "visual_stem": "drone_weather",
    "title": {"cs": "Můžu letět?, pokročilá verze: jak přesný je model, profil větru a létavé hodiny",
              "en": "Can I fly?, advanced: how accurate the model is, the wind profile and flyable hours"},
    "visual": {"cs": "Můžu letět? Počasí pro drony", "en": "Can I fly? Weather for drones"},
    "lead": {
        "cs": "Pokročilá verze notebooku o počasí pro drony. Modelovou předpověď Open-Meteo porovnáš s týdnem skutečných zpráv METAR ze čtyř českých letišť a spočítáš, jak moc se model plete ve větru, teplotě a rosném bodu. Pak z tří měsíců modelových dat pro Roztoky zjistíš, jak se mění profil větru se stabilitou ovzduší během dne a ve kterých hodinách se dalo létat nejčastěji.",
        "en": "The advanced version of the drone weather notebook. You compare the Open-Meteo model with a week of real METAR reports from four Czech airports and compute how much the model errs in wind, temperature and dew point. Then, from three months of model data for Roztoky, you find out how the wind profile changes with atmospheric stability during the day and in which hours flying was possible most often.",
    },
    "goal": {
        "cs": "dekódovat týden zpráv METAR, ověřit proti nim model (odchylka, RMSE, korelace), spočítat exponent profilu větru a jeho závislost na teplotním zvrstvení a sestavit denní chod podílu hodin vhodných k letu podle větru, nárazů, srážek, dohlednosti a námrazy.",
        "en": "decode a week of METAR reports, verify the model against them (bias, RMSE, correlation), compute the wind profile exponent and its dependence on temperature stratification, and build the daily cycle of the share of hours suitable for flying by wind, gusts, precipitation, visibility and icing.",
    },
    "data": {
        "cs": "zprávy METAR za posledních 7 dní z letišť Praha (LKPR), Brno (LKTB), Ostrava (LKMT) a Karlovy Vary (LKKV) ze služby NOAA Aviation Weather Center; hodinová data Open-Meteo za stejných 7 dní pro souřadnice letišť a za 92 dní pro Roztoky (vítr v 10, 80 a 120 m, nárazy, teplota ve 2 a 120 m, rosný bod, srážky, dohlednost). Hodnoty Open-Meteo pro minulé dny jsou uložené krátkodobé předpovědi modelů, ne měření. Data se průběžně mění, tvoje čísla budou jiná než v uloženém notebooku.",
        "en": "METAR reports for the last 7 days from Prague (LKPR), Brno (LKTB), Ostrava (LKMT) and Karlovy Vary (LKKV) airports from the NOAA Aviation Weather Center; hourly Open-Meteo data for the same 7 days at the airport coordinates and for 92 days for Roztoky (wind at 10, 80 and 120 m, gusts, temperature at 2 and 120 m, dew point, precipitation, visibility). Open-Meteo values for past days are stored short-range model forecasts, not measurements. The data change continuously, so your numbers will differ from the stored notebook.",
    },
    "sources": {
        "cs": [
            "METAR: NOAA/NWS Aviation Weather Center, https://aviationweather.gov/data/api/ (veřejná data vlády USA).",
            "Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "Klíč ke zprávám METAR: ICAO Annex 3 / WMO-No. 306, kód FM 15.",
            "Stull, R. B. (1988). *An Introduction to Boundary Layer Meteorology*. Kluwer (denní chod mezní vrstvy, stabilita, profil větru).",
            "Odolnost DJI Mavic 3 Enterprise vůči větru 12 m/s a DJI Mini 4 Pro 10,7 m/s (technické listy DJI).",
        ],
        "en": [
            "METAR: NOAA/NWS Aviation Weather Center, https://aviationweather.gov/data/api/ (US government public data).",
            "Weather: Open-Meteo.com (CC BY 4.0), https://open-meteo.com",
            "METAR code: ICAO Annex 3 / WMO-No. 306, code FM 15.",
            "Stull, R. B. (1988). *An Introduction to Boundary Layer Meteorology*. Kluwer (daily cycle of the boundary layer, stability, wind profile).",
            "Wind resistance of the DJI Mavic 3 Enterprise 12 m/s and of the DJI Mini 4 Pro 10.7 m/s (DJI data sheets).",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava", "## 1. Setup")),
        ("code", t('''
import re, time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
''' + OPEN_METEO_HELPER["cs"], '''
import re, time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
''' + OPEN_METEO_HELPER["en"])),
        ("md", t(
            "## 2. Týden zpráv METAR\n\nStáhneme zprávy za 7 dní, dekódujeme vítr, nárazy, teplotu, rosný bod, dohlednost a základnu oblačnosti a ponecháme jednu zprávu na hodinu. Zpráva nese jen den v měsíci, měsíc a rok doplníme podle dnešního data.",
            "## 2. A week of METAR reports\n\nWe download the reports for 7 days, decode wind, gusts, temperature, dew point, visibility and cloud base and keep one report per hour. A report only carries the day of the month; month and year are taken from today's date.")),
        ("code", t('''
AIRPORTS = {"LKPR": (50.1008, 14.2600), "LKTB": (49.1513, 16.6944), "LKMT": (49.6963, 18.1111), "LKKV": (50.2030, 12.9150)}  # ◀ parametr: letiště a souřadnice
raw = []
for code in AIRPORTS:                 # po jednom letišti, služba vrací v jednom dotazu nejvýš kolem 400 zpráv
    raw += requests.get("https://aviationweather.gov/api/data/metar", params={"ids": code, "format": "raw", "hours": 168}, timeout=60).text.strip().splitlines()
now = pd.Timestamp.now(tz="UTC").tz_localize(None)
KT = 0.514444

def decode(m):
    body = re.split(r"\\b(TEMPO|BECMG|NOSIG|RMK)\\b", m)[0]
    dd, hh, mm = (int(x) for x in re.search(r"\\b(\\d{2})(\\d{2})(\\d{2})Z\\b", body).groups())
    ts = now.replace(day=1, hour=hh, minute=mm, second=0, microsecond=0, nanosecond=0)
    ts = ts.replace(day=dd) if dd <= now.day else (ts - pd.DateOffset(months=1)).replace(day=dd)   # zpráva z minulého měsíce
    d = {"stanice": body.split()[1], "čas": ts}
    w = re.search(r"\\b(\\d{3}|VRB)(\\d{2,3})(?:G(\\d{2,3}))?KT\\b", body)
    if w:
        d["vítr"] = int(w.group(2)) * KT; d["nárazy"] = int(w.group(3)) * KT if w.group(3) else np.nan
    tt = re.search(r"\\b(M?\\d{2})/(M?\\d{2})\\b", body)
    if tt:
        d["T"], d["Td"] = (int(x.replace("M", "-")) for x in tt.groups())
    v = re.search(r"\\s(\\d{4})\\s", body)
    d["dohlednost"] = 10000 if "CAVOK" in body else (int(v.group(1)) if v else np.nan)
    ceil = [int(h) * 30.48 for c, h in re.findall(r"\\b(BKN|OVC|VV)(\\d{3})", body)]
    d["základna"] = min(ceil) if ceil else np.nan
    d["srážky"] = bool(re.search(r"(?<=\\s)[-+]?(?:VC)?(?:SH|TS|FZ)?(?:DZ|RA|SN|SG|PL|GR|GS)", body + " "))
    return d

obs = pd.DataFrame([decode(m) for m in raw]).dropna(subset=["vítr", "T"])
obs["hodina"] = obs["čas"].dt.round("h")
obs = obs.sort_values("čas").groupby(["stanice", "hodina"]).last().reset_index()   # jedna zpráva na hodinu
print(f"{len(raw)} zpráv METAR, {len(obs)} hodin s pozorováním; od {obs['hodina'].min()} do {obs['hodina'].max()} UTC")
obs.groupby("stanice")[["vítr", "nárazy", "T", "Td"]].describe().loc[:, (slice(None), ["count", "mean", "max"])].round(1)
''', '''
AIRPORTS = {"LKPR": (50.1008, 14.2600), "LKTB": (49.1513, 16.6944), "LKMT": (49.6963, 18.1111), "LKKV": (50.2030, 12.9150)}  # ◀ parameter: airports and coordinates
raw = []
for code in AIRPORTS:                 # one airport at a time, the service returns at most about 400 reports per query
    raw += requests.get("https://aviationweather.gov/api/data/metar", params={"ids": code, "format": "raw", "hours": 168}, timeout=60).text.strip().splitlines()
now = pd.Timestamp.now(tz="UTC").tz_localize(None)
KT = 0.514444

def decode(m):
    body = re.split(r"\\b(TEMPO|BECMG|NOSIG|RMK)\\b", m)[0]
    dd, hh, mm = (int(x) for x in re.search(r"\\b(\\d{2})(\\d{2})(\\d{2})Z\\b", body).groups())
    ts = now.replace(day=1, hour=hh, minute=mm, second=0, microsecond=0, nanosecond=0)
    ts = ts.replace(day=dd) if dd <= now.day else (ts - pd.DateOffset(months=1)).replace(day=dd)   # report from the previous month
    d = {"station": body.split()[1], "time": ts}
    w = re.search(r"\\b(\\d{3}|VRB)(\\d{2,3})(?:G(\\d{2,3}))?KT\\b", body)
    if w:
        d["wind"] = int(w.group(2)) * KT; d["gusts"] = int(w.group(3)) * KT if w.group(3) else np.nan
    tt = re.search(r"\\b(M?\\d{2})/(M?\\d{2})\\b", body)
    if tt:
        d["T"], d["Td"] = (int(x.replace("M", "-")) for x in tt.groups())
    v = re.search(r"\\s(\\d{4})\\s", body)
    d["visibility"] = 10000 if "CAVOK" in body else (int(v.group(1)) if v else np.nan)
    ceil = [int(h) * 30.48 for c, h in re.findall(r"\\b(BKN|OVC|VV)(\\d{3})", body)]
    d["ceiling"] = min(ceil) if ceil else np.nan
    d["precip"] = bool(re.search(r"(?<=\\s)[-+]?(?:VC)?(?:SH|TS|FZ)?(?:DZ|RA|SN|SG|PL|GR|GS)", body + " "))
    return d

obs = pd.DataFrame([decode(m) for m in raw]).dropna(subset=["wind", "T"])
obs["hour"] = obs["time"].dt.round("h")
obs = obs.sort_values("time").groupby(["station", "hour"]).last().reset_index()   # one report per hour
print(f"{len(raw)} METAR reports, {len(obs)} hours with observations; from {obs['hour'].min()} to {obs['hour'].max()} UTC")
obs.groupby("station")[["wind", "gusts", "T", "Td"]].describe().loc[:, (slice(None), ["count", "mean", "max"])].round(1)
''')),
        ("md", t(
            "## 3. Ověření modelu\n\nPro každé letiště stáhneme z Open-Meteo hodinová data za stejných 7 dní a spárujeme je se zprávami. **Odchylka** je průměr rozdílu model − pozorování (systematická chyba), **RMSE** odmocnina průměru čtverců rozdílu (celková chyba), **korelace** říká, jak dobře model zachytil průběh.",
            "## 3. Verifying the model\n\nFor each airport we download hourly Open-Meteo data for the same 7 days and pair them with the reports. **Bias** is the mean of model − observation (systematic error), **RMSE** the root mean square of the difference (total error), **correlation** tells how well the model caught the course.")),
        ("code", t('''
lats = ",".join(str(v[0]) for v in AIRPORTS.values()); lons = ",".join(str(v[1]) for v in AIRPORTS.values())
w = open_meteo({"latitude": lats, "longitude": lons, "past_days": 7, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "UTC",
                "hourly": "wind_speed_10m,wind_gusts_10m,temperature_2m,dew_point_2m"})
mod = pd.concat([pd.DataFrame(r["hourly"]).assign(stanice=k) for k, r in zip(AIRPORTS, w)])
mod["hodina"] = pd.to_datetime(mod["time"])
cmp = obs.merge(mod, on=["stanice", "hodina"])
rows = {}
for k, g in cmp.groupby("stanice"):
    rows[k] = {"hodin": len(g),
               "vítr: odchylka modelu (m/s)": (g.wind_speed_10m - g["vítr"]).mean(), "vítr: RMSE (m/s)": np.sqrt(((g.wind_speed_10m - g["vítr"]) ** 2).mean()),
               "vítr: korelace": g.wind_speed_10m.corr(g["vítr"]),
               "T: odchylka (°C)": (g.temperature_2m - g["T"]).mean(), "T: RMSE (°C)": np.sqrt(((g.temperature_2m - g["T"]) ** 2).mean()),
               "Td: odchylka (°C)": (g.dew_point_2m - g["Td"]).mean()}
k0 = list(AIRPORTS)[0]
g = cmp[cmp.stanice == k0]
fig, ax = plt.subplots(figsize=(11, 3.5))
ax.plot(g.hodina, g["vítr"], ".", label="METAR"); ax.plot(g.hodina, g.wind_speed_10m, "-", label="Open-Meteo")
ax.set(ylabel="vítr v 10 m (m/s)", title=k0); ax.legend(); plt.show()
pd.DataFrame(rows).T.round(2)
''', '''
lats = ",".join(str(v[0]) for v in AIRPORTS.values()); lons = ",".join(str(v[1]) for v in AIRPORTS.values())
w = open_meteo({"latitude": lats, "longitude": lons, "past_days": 7, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "UTC",
                "hourly": "wind_speed_10m,wind_gusts_10m,temperature_2m,dew_point_2m"})
mod = pd.concat([pd.DataFrame(r["hourly"]).assign(station=k) for k, r in zip(AIRPORTS, w)])
mod["hour"] = pd.to_datetime(mod["time"])
cmp = obs.merge(mod, on=["station", "hour"])
rows = {}
for k, g in cmp.groupby("station"):
    rows[k] = {"hours": len(g),
               "wind: model bias (m/s)": (g.wind_speed_10m - g["wind"]).mean(), "wind: RMSE (m/s)": np.sqrt(((g.wind_speed_10m - g["wind"]) ** 2).mean()),
               "wind: correlation": g.wind_speed_10m.corr(g["wind"]),
               "T: bias (°C)": (g.temperature_2m - g["T"]).mean(), "T: RMSE (°C)": np.sqrt(((g.temperature_2m - g["T"]) ** 2).mean()),
               "Td: bias (°C)": (g.dew_point_2m - g["Td"]).mean()}
k0 = list(AIRPORTS)[0]
g = cmp[cmp.station == k0]
fig, ax = plt.subplots(figsize=(11, 3.5))
ax.plot(g.hour, g["wind"], ".", label="METAR"); ax.plot(g.hour, g.wind_speed_10m, "-", label="Open-Meteo")
ax.set(ylabel="wind at 10 m (m/s)", title=k0); ax.legend(); plt.show()
pd.DataFrame(rows).T.round(2)
''')),
        ("task", t(
            "Podhodnocuje model vítr, nebo ho nadhodnocuje? Jak velká je RMSE ve srovnání s typickou rychlostí větru na letišti? Na kterém letišti model sedí nejhůř a čím to může být (terén v okolí, údolí, rozlišení modelu)? Proč METAR udává vítr v celých uzlech a jakou chybu to samo o sobě přináší?",
            "Does the model underestimate or overestimate the wind? How large is the RMSE compared with the typical wind speed at the airport? At which airport does the model fit worst, and what may cause it (surrounding terrain, a valley, model resolution)? Why does METAR give wind in whole knots, and what error does that alone introduce?")),
        ("task", t(
            "Jak přesně model trefuje teplotu a rosný bod? Odhad základny oblačnosti je 125 m na každý stupeň rozdílu T − Td: o kolik metrů se odhad posune, když se rosný bod splete o 1 °C? Co z toho plyne pro rozhodování o mlze, nízké oblačnosti a námraze podle modelu?",
            "How accurately does the model hit temperature and dew point? The cloud base estimate is 125 m per degree of T − Td: by how many metres does the estimate shift when the dew point is off by 1 °C? What follows for deciding about fog, low cloud and icing from the model?")),
        ("md", t(
            "## 4. Profil větru a stabilita ovzduší\n\nVítr s výškou roste přibližně podle u(z) = u(10 m) · (z / 10)^α. Exponent α spočítáme z větru v 10 a 120 m pro každou hodinu za 92 dní a porovnáme ho s rozdílem teploty ve 120 a 2 m. Klesá-li teplota s výškou rychleji než o 1 °C na 100 m, je ovzduší labilní a promíchává se; roste-li s výškou (inverze), je stabilní.",
            "## 4. Wind profile and atmospheric stability\n\nWind grows with height approximately as u(z) = u(10 m) · (z / 10)^α. We compute the exponent α from the wind at 10 and 120 m for every hour over 92 days and compare it with the temperature difference between 120 and 2 m. If temperature falls with height faster than 1 °C per 100 m, the air is unstable and mixes; if it rises with height (an inversion), it is stable.")),
        ("code", t('''
LAT, LON = 50.152, 14.392            # ◀ parametr: místo letu (Roztoky)
w = open_meteo({"latitude": LAT, "longitude": LON, "past_days": 92, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "Europe/Prague",
                "hourly": "wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_gusts_10m,temperature_2m,temperature_120m,dew_point_2m,precipitation,visibility"})
loc = pd.DataFrame(w["hourly"]); loc["time"] = pd.to_datetime(loc["time"]); loc = loc.set_index("time").dropna()
loc["alfa"] = np.log(loc.wind_speed_120m / loc.wind_speed_10m.clip(lower=0.5)) / np.log(120 / 10)   # exponent mocninného profilu
loc["dT"] = loc.temperature_120m - loc.temperature_2m                                               # teplota 120 m − 2 m
loc["stabilita"] = pd.cut(loc.dT, [-10, -1.0, 0.0, 1.0, 20], labels=["labilní (< −1 °C)", "slabě labilní", "slabě stabilní", "inverze (> +1 °C)"])
fig, ax = plt.subplots(1, 2, figsize=(14, 4))
by_h = loc.groupby(loc.index.hour)
ax[0].plot(by_h.alfa.median(), "o-", label="exponent α"); ax2 = ax[0].twinx(); ax2.plot(by_h.dT.median(), "s--", color="C3", label="T(120 m) − T(2 m)")
ax[0].set(xlabel="hodina (místní čas)", ylabel="medián α"); ax2.set_ylabel("medián rozdílu teplot (°C)", color="C3")
ax[1].scatter(loc.dT, loc.alfa, s=3, alpha=0.3); ax[1].set(xlabel="T(120 m) − T(2 m) (°C)", ylabel="α", ylim=(-0.2, 1.2)); plt.tight_layout(); plt.show()
print(f"{len(loc)} hodin; suchoadiabatický pokles na 118 m je −1,15 °C")
loc.groupby("stabilita", observed=True).agg(hodin=("alfa", "size"), alfa=("alfa", "median"), vitr10=("wind_speed_10m", "median"), vitr120=("wind_speed_120m", "median")).round(2)
''', '''
LAT, LON = 50.152, 14.392            # ◀ parameter: flight site (Roztoky)
w = open_meteo({"latitude": LAT, "longitude": LON, "past_days": 92, "forecast_days": 1, "wind_speed_unit": "ms", "timezone": "Europe/Prague",
                "hourly": "wind_speed_10m,wind_speed_80m,wind_speed_120m,wind_gusts_10m,temperature_2m,temperature_120m,dew_point_2m,precipitation,visibility"})
loc = pd.DataFrame(w["hourly"]); loc["time"] = pd.to_datetime(loc["time"]); loc = loc.set_index("time").dropna()
loc["alpha"] = np.log(loc.wind_speed_120m / loc.wind_speed_10m.clip(lower=0.5)) / np.log(120 / 10)   # exponent of the power-law profile
loc["dT"] = loc.temperature_120m - loc.temperature_2m                                               # temperature 120 m − 2 m
loc["stability"] = pd.cut(loc.dT, [-10, -1.0, 0.0, 1.0, 20], labels=["unstable (< −1 °C)", "weakly unstable", "weakly stable", "inversion (> +1 °C)"])
fig, ax = plt.subplots(1, 2, figsize=(14, 4))
by_h = loc.groupby(loc.index.hour)
ax[0].plot(by_h.alpha.median(), "o-", label="exponent α"); ax2 = ax[0].twinx(); ax2.plot(by_h.dT.median(), "s--", color="C3", label="T(120 m) − T(2 m)")
ax[0].set(xlabel="hour (local time)", ylabel="median α"); ax2.set_ylabel("median temperature difference (°C)", color="C3")
ax[1].scatter(loc.dT, loc.alpha, s=3, alpha=0.3); ax[1].set(xlabel="T(120 m) − T(2 m) (°C)", ylabel="α", ylim=(-0.2, 1.2)); plt.tight_layout(); plt.show()
print(f"{len(loc)} hours; the dry adiabatic drop over 118 m is −1.15 °C")
loc.groupby("stability", observed=True).agg(hours=("alpha", "size"), alpha=("alpha", "median"), wind10=("wind_speed_10m", "median"), wind120=("wind_speed_120m", "median")).round(2)
''')),
        ("task", t(
            "Proč je α v noci a ráno velké a přes den malé? Proč je při inverzi u země téměř bezvětří, zatímco ve 120 m fouká? Co to znamená, když ráno před vzletem změříš vítr ručním anemometrem a podle něj odhaduješ vítr ve výšce letu? V kolik hodin se inverze typicky rozpouští?",
            "Why is α large at night and in the morning and small during the day? Why is there almost no wind at the ground in an inversion while it blows at 120 m? What does it mean when you measure the wind with a hand anemometer before a morning take-off and estimate the wind at flight height from it? At what time does the inversion typically break up?")),
        ("md", t(
            "## 5. Létavé hodiny za poslední tři měsíce\n\nPro každou hodinu za 92 dní vyhodnotíme podmínky jako semafor v základní verzi: vítr ve 120 m, odhad nárazů ve 120 m, srážky, dohlednost a riziko námrazy. Nárazy ve 120 m model nedává, proto je odhadneme ze 10 m dvěma způsoby (`GUSTS`).",
            "## 5. Flyable hours over the last three months\n\nFor each hour over 92 days we evaluate the conditions like the traffic light in the basic version: wind at 120 m, estimated gusts at 120 m, precipitation, visibility and icing risk. The model does not give gusts at 120 m, so we estimate them from 10 m in two ways (`GUSTS`).")),
        ("code", t('''
LIM_WIND, LIM_GUST = 10.0, 12.0      # ◀ parametr: limit větru ve 120 m a nárazů (m/s)
LIM_VIS = 5000                        # ◀ parametr: nejmenší dohlednost (m)
GUSTS = "poměr"                       # ◀ parametr: odhad nárazů ve 120 m: "poměr" (stejný poměr nárazy/vítr jako v 10 m) nebo "přírůstek" (stejný rozdíl)
if GUSTS == "poměr":
    gust120 = loc.wind_gusts_10m * loc.wind_speed_120m / loc.wind_speed_10m.clip(lower=0.5)
else:
    gust120 = loc.wind_speed_120m + (loc.wind_gusts_10m - loc.wind_speed_10m)
ok = pd.DataFrame({"vítr 120 m": loc.wind_speed_120m <= LIM_WIND, "nárazy": gust120 <= LIM_GUST, "bez srážek": loc.precipitation < 0.1,
                   "dohlednost": loc.visibility >= LIM_VIS, "bez námrazy": ~((loc.temperature_2m < 1) & (loc.temperature_2m - loc.dew_point_2m < 2))})
ok["létat"] = ok.all(axis=1)
day = ok[(ok.index.hour >= 6) & (ok.index.hour <= 20)]
print("podíl denních hodin (6–20 h), kdy je podmínka splněna:"); print((day.mean() * 100).round(1).to_string())
fig, ax = plt.subplots(figsize=(10, 3.5))
(ok.groupby(ok.index.hour).mean() * 100)[["vítr 120 m", "nárazy", "bez srážek", "dohlednost", "létat"]].plot(ax=ax, marker=".")
ax.set(xlabel="hodina (místní čas)", ylabel="% hodin", ylim=(0, 105)); plt.show()
''', '''
LIM_WIND, LIM_GUST = 10.0, 12.0      # ◀ parameter: limit for wind at 120 m and for gusts (m/s)
LIM_VIS = 5000                        # ◀ parameter: minimum visibility (m)
GUSTS = "ratio"                       # ◀ parameter: estimate of gusts at 120 m: "ratio" (the same gust/wind ratio as at 10 m) or "excess" (the same difference)
if GUSTS == "ratio":
    gust120 = loc.wind_gusts_10m * loc.wind_speed_120m / loc.wind_speed_10m.clip(lower=0.5)
else:
    gust120 = loc.wind_speed_120m + (loc.wind_gusts_10m - loc.wind_speed_10m)
ok = pd.DataFrame({"wind 120 m": loc.wind_speed_120m <= LIM_WIND, "gusts": gust120 <= LIM_GUST, "no precipitation": loc.precipitation < 0.1,
                   "visibility": loc.visibility >= LIM_VIS, "no icing": ~((loc.temperature_2m < 1) & (loc.temperature_2m - loc.dew_point_2m < 2))})
ok["fly"] = ok.all(axis=1)
day = ok[(ok.index.hour >= 6) & (ok.index.hour <= 20)]
print("share of daytime hours (6–20 h) when the condition is met:"); print((day.mean() * 100).round(1).to_string())
fig, ax = plt.subplots(figsize=(10, 3.5))
(ok.groupby(ok.index.hour).mean() * 100)[["wind 120 m", "gusts", "no precipitation", "visibility", "fly"]].plot(ax=ax, marker=".")
ax.set(xlabel="hour (local time)", ylabel="% of hours", ylim=(0, 105)); plt.show()
''')),
        ("task", t(
            "Která podmínka v posledních třech měsících omezovala létání nejčastěji a ve kterou denní dobu byla šance na let nejlepší? Přepni `GUSTS` na druhý způsob odhadu nárazů: o kolik se změní podíl létavých hodin? Který odhad je podle tebe bližší skutečnosti a proč (jak se poryvy mění s výškou)?",
            "Which condition limited flying most often over the last three months, and at what time of day was the chance to fly best? Switch `GUSTS` to the other gust estimate: by how much does the share of flyable hours change? Which estimate do you think is closer to reality, and why (how do gusts change with height)?")),
        ("task", t(
            "Nastav limity pro menší dron (`LIM_WIND = 8`, `LIM_GUST = 10.7` jako odolnost DJI Mini 4 Pro) a pak pro přísnější provoz se snímkováním (dohlednost 8 km). Jak se změní podíl létavých hodin a jejich denní chod? Proč by tento výpočet pro zimní měsíce vyšel jinak?",
            "Set the limits for a smaller drone (`LIM_WIND = 8`, `LIM_GUST = 10.7` as the wind resistance of the DJI Mini 4 Pro) and then for stricter operation with imaging (visibility 8 km). How do the share of flyable hours and its daily cycle change? Why would this calculation turn out differently for the winter months?")),
        ("task", t(
            "+ Přidej do `AIRPORTS` letiště Linec (`\"LOWL\": (48.2332, 14.1875)`) nebo jiné a porovnej přesnost modelu. Změň `LAT, LON` na jiné místo letu (třeba Brno-Bystrc 49.2467, 16.4798) a porovnej profil větru a létavé hodiny.",
            "+ Add Linz airport (`\"LOWL\": (48.2332, 14.1875)`) or another to `AIRPORTS` and compare the model accuracy. Change `LAT, LON` to another flight site (for example Brno-Bystrc 49.2467, 16.4798) and compare the wind profile and flyable hours.")),
    ]
