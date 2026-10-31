import re
from _common import CUZK_HELPER

# verze: přípona souboru → místa letu, gridová síť a texty úloh, které na místech závisí
VARIANTS = {
    "": dict(
        sites_cs="""SITES = {                     # ◀ parametr: místa letu (zeměpisná šířka, délka)
    "Suchdol, kampus":        (50.130, 14.373),
    "Roztocký háj":           (50.158, 14.385),
    "Kněževes u letiště":     (50.124, 14.262),
    "Letňany":                (50.131, 14.522),
    "Pec pod Sněžkou":        (50.692, 15.733),
    "Luční bouda, Krkonoše":  (50.735, 15.697),
}""",
        sites_en="""SITES = {                     # ◀ parameter: flight sites (latitude, longitude)
    "Suchdol, campus":        (50.130, 14.373),
    "Roztoky forest":         (50.158, 14.385),
    "Kněževes by the airport": (50.124, 14.262),
    "Letňany":                (50.131, 14.522),
    "Pec pod Sněžkou":        (50.692, 15.733),
    "Luční bouda, Krkonoše":  (50.735, 15.697),
}""",
        task3_cs="Vnější i vnitřní zóna CTR Praha (LKR314C a LKR314D) má horní hranici 3500 ft AMSL: kolik je to metrů nad terénem v Suchdole? Proč se některé letecké prostory LKR320A dronu ve 120 m vůbec netýkají? Proč u hranic v AMSL nebo FL záleží na výšce terénu, a co to znamená pro let na horách (Pec pod Sněžkou)?",
        task3_en="Both the outer and the inner zone of the Prague CTR (LKR314C and LKR314D) have an upper limit of 3500 ft AMSL: how many metres above ground is that in Suchdol? Why do some LKR320A airspace areas not concern a drone at 120 m at all? Why does terrain elevation matter for limits in AMSL or FL, and what does that mean for a flight in the mountains (Pec pod Sněžkou)?",
        grid="GRID_CTR", center="(50.10, 14.30)", span="0.25",
        grid_md_cs="## 4. Gridová síť kolem řízených letišť\n\nV okolí řízených letišť (CTR) ŘLP zveřejňuje síť buněk 30″ × 30″ (asi 600 × 900 m), kde každá buňka udává, do jaké výšky nad terénem je let povolen bez dalšího souhlasu. Podmínky použití sítě jsou v příslušném OOP.",
        grid_md_en="## 4. The grid around controlled airports\n\nAround controlled airports (CTR) ŘLP publishes a grid of 30″ × 30″ cells (about 600 × 900 m) where each cell states up to what height above ground flight is allowed without further approval. The conditions of using the grid are in the relevant OOP.",
        task4_cs="Do jaké výšky smíš podle sítě létat v Suchdole a v Kněževsi? Jak se povolená výška mění směrem k přistávací dráze a proč? Posuň mapu na jiné řízené letiště (např. Brno 49,15° s. š., 16,69° v. d.) a porovnej tvar sítě. Proč je síť výhodnější než jedna velká zóna s jedinou výškou?",
        task4_en="Up to what height may you fly in Suchdol and in Kněževes according to the grid? How does the allowed height change towards the runway, and why? Move the map to another controlled airport (e.g. Brno 49.15° N, 16.69° E) and compare the shape of the grid. Why is a grid better than one large zone with a single height?",
        site5_cs="Roztocký háj", site5_en="Roztoky forest",
        plus_cs="+ Spolužáci mohou mít notebook pro okolí Brna nebo Hluboké nad Vltavou. Porovnejte, jaké zóny a jaké povolené výšky ze sítě mají místa letu kolem letiště a mimo města, a čím se liší síť kolem řízeného a neřízeného letiště.",
        plus_en="+ Classmates may have the notebook for the Brno area or for Hluboká nad Vltavou. Compare which zones and which allowed heights from the grid the flight sites near the airport and outside towns have, and how the grid around a controlled and an uncontrolled airport differ."),
    "brno": dict(
        sites_cs="""SITES = {                     # ◀ parametr: místa letu (zeměpisná šířka, délka)
    "Bystrc, Kozí horka":                (49.2467, 16.4798),
    "Kraví hora, hvězdárna":             (49.2040, 16.5840),
    "Mendelova univerzita, Černá Pole":  (49.2105, 16.6150),
    "Chrlice u letiště Tuřany":          (49.1300, 16.6550),
    "Křtiny":                            (49.2970, 16.7440),
    "Pálava, Děvín":                     (48.8700, 16.6450),
}""",
        sites_en="""SITES = {                     # ◀ parameter: flight sites (latitude, longitude)
    "Bystrc, Kozí horka":                (49.2467, 16.4798),
    "Kraví hora, observatory":           (49.2040, 16.5840),
    "Mendel University, Černá Pole":     (49.2105, 16.6150),
    "Chrlice by Tuřany airport":         (49.1300, 16.6550),
    "Křtiny":                            (49.2970, 16.7440),
    "Pálava, Děvín":                     (48.8700, 16.6450),
}""",
        task3_cs="Omezený prostor kolem letiště Brno-Tuřany (zóna 9LKR314A) má horní hranici 2500 ft AMSL: kolik je to metrů nad terénem na Kraví hoře a v Chrlicích? Proč se některé letecké prostory LKR320A dronu ve 120 m vůbec netýkají? Proč u hranic v AMSL nebo FL záleží na výšce terénu a co to znamená na Děvíně, kde prostor LKTB4 začíná na FL65?",
        task3_en="The restricted area around Brno-Tuřany airport (zone 9LKR314A) has an upper limit of 2500 ft AMSL: how many metres above ground is that on Kraví hora and in Chrlice? Why do some LKR320A airspace areas not concern a drone at 120 m at all? Why does terrain elevation matter for limits in AMSL or FL, and what does that mean on Děvín, where the LKTB4 area starts at FL65?",
        grid="GRID_CTR", center="(49.17, 16.62)", span="0.15",
        grid_md_cs="## 4. Gridová síť kolem řízených letišť\n\nV okolí řízených letišť (CTR) ŘLP zveřejňuje síť buněk 30″ × 30″ (asi 600 × 900 m), kde každá buňka udává, do jaké výšky nad terénem je let povolen bez dalšího souhlasu. Podmínky použití sítě jsou v příslušném OOP.",
        grid_md_en="## 4. The grid around controlled airports\n\nAround controlled airports (CTR) ŘLP publishes a grid of 30″ × 30″ cells (about 600 × 900 m) where each cell states up to what height above ground flight is allowed without further approval. The conditions of using the grid are in the relevant OOP.",
        task4_cs="Do jaké výšky smíš podle sítě létat na Kraví hoře, u Mendelovy univerzity a v Chrlicích? Jak se povolená výška mění směrem k přistávací dráze letiště Brno-Tuřany a proč? Proč je Bystrc mimo tuto síť (najdi v seznamu zón soubor GRID_ATZ)? Proč je síť výhodnější než jedna velká zóna s jedinou výškou?",
        task4_en="Up to what height may you fly on Kraví hora, at Mendel University and in Chrlice according to the grid? How does the allowed height change towards the runway of Brno-Tuřany airport, and why? Why is Bystrc outside this grid (find the GRID_ATZ file in the list of zones)? Why is a grid better than one large zone with a single height?",
        site5_cs="Bystrc, Kozí horka", site5_en="Bystrc, Kozí horka",
        plus_cs="+ Spolužáci mohou mít notebook pro okolí Prahy nebo Hluboké nad Vltavou. Porovnejte, jaké zóny a jaké povolené výšky ze sítě mají místa letu kolem letiště a mimo města, a čím se liší síť kolem řízeného a neřízeného letiště.",
        plus_en="+ Classmates may have the notebook for the Prague area or for Hluboká nad Vltavou. Compare which zones and which allowed heights from the grid the flight sites near the airport and outside towns have, and how the grid around a controlled and an uncontrolled airport differ."),
    "hluboka": dict(
        sites_cs="""SITES = {                     # ◀ parametr: místa letu (zeměpisná šířka, délka)
    "Hluboká nad Vltavou, zámek":        (49.0517, 14.4400),
    "Hosín, údolí":                      (49.0452, 14.4769),
    "Jihočeská univerzita":              (48.9770, 14.4470),
    "u letiště České Budějovice":        (48.9445, 14.4302),
    "Třeboň, rybník Svět":               (48.9930, 14.7700),
    "Plechý, Šumava":                    (48.7713, 13.8580),
}""",
        sites_en="""SITES = {                     # ◀ parameter: flight sites (latitude, longitude)
    "Hluboká nad Vltavou, castle":       (49.0517, 14.4400),
    "Hosín, valley":                     (49.0452, 14.4769),
    "University of South Bohemia":       (48.9770, 14.4470),
    "by České Budějovice airport":       (48.9445, 14.4302),
    "Třeboň, Svět pond":                 (48.9930, 14.7700),
    "Plechý, Šumava":                    (48.7713, 13.8580),
}""",
        task3_cs="Omezený prostor kolem letiště České Budějovice (zóna 3LKR314A) má horní hranici 3500 ft AMSL: kolik je to metrů nad terénem u Jihočeské univerzity? Proč se některé letecké prostory LKR320A dronu ve 120 m vůbec netýkají? Proč u hranic v AMSL nebo FL záleží na výšce terénu? Co by stejná hranice 3500 ft AMSL znamenala, kdyby zóna sahala až na Kleť (1084 m n. m.)?",
        task3_en="The restricted area around České Budějovice airport (zone 3LKR314A) has an upper limit of 3500 ft AMSL: how many metres above ground is that at the University of South Bohemia? Why do some LKR320A airspace areas not concern a drone at 120 m at all? Why does terrain elevation matter for limits in AMSL or FL? What would the same 3500 ft AMSL limit mean if the zone reached as far as Kleť (1084 m a.s.l.)?",
        grid="GRID_ATZ", center="(49.00, 14.45)", span="0.10",
        grid_md_cs="## 4. Gridová síť kolem letišť\n\nV okolí letišť ŘLP zveřejňuje síť buněk, kde každá buňka udává, do jaké výšky nad terénem je let povolen bez dalšího souhlasu. Kolem řízených letišť (CTR) je to soubor GRID_CTR s buňkami 30″ × 30″, v prostorech neřízeného letového provozu soubor GRID_ATZ s buňkami 15″ × 15″ (asi 300 × 450 m). V okolí Českých Budějovic a Hluboké platí GRID_ATZ. Podmínky použití sítě jsou v příslušném OOP.",
        grid_md_en="## 4. The grid around airports\n\nAround airports ŘLP publishes a grid of cells where each cell states up to what height above ground flight is allowed without further approval. Around controlled airports (CTR) it is the GRID_CTR file with 30″ × 30″ cells, in areas of uncontrolled air traffic the GRID_ATZ file with 15″ × 15″ cells (about 300 × 450 m). Around České Budějovice and Hluboká GRID_ATZ applies. The conditions of using the grid are in the relevant OOP.",
        task4_cs="Do jaké výšky smíš podle sítě létat u Jihočeské univerzity, u zámku v Hluboké a v údolí u Hosína? Proč je u Hosína povolená výška 0 m nad terénem (podívej se, do které zóny LKR315A místo patří)? Jak se povolená výška mění směrem k letišti České Budějovice? Proč je síť výhodnější než jedna velká zóna s jedinou výškou?",
        task4_en="Up to what height may you fly at the University of South Bohemia, at Hluboká castle and in the valley near Hosín according to the grid? Why is the allowed height near Hosín 0 m above ground (look at which LKR315A zone the site belongs to)? How does the allowed height change towards České Budějovice airport? Why is a grid better than one large zone with a single height?",
        site5_cs="Hluboká nad Vltavou, zámek", site5_en="Hluboká nad Vltavou, castle",
        plus_cs="+ Spolužáci mohou mít notebook pro okolí Prahy nebo Brna. Porovnejte, jaké zóny a jaké povolené výšky ze sítě mají místa letu kolem letiště a mimo města, a čím se liší síť kolem řízeného a neřízeného letiště.",
        plus_en="+ Classmates may have the notebook for the Prague or the Brno area. Compare which zones and which allowed heights from the grid the flight sites near the airport and outside towns have, and how the grid around a controlled and an uncontrolled airport differ."),
}


def meta(P):
    return {
        "version": "1.0",
        "minutes": 45,
        "title": {"cs": "Kde smím létat: zeměpisné zóny UAS z dat ŘLP", "en": "Where may I fly: UAS geographical zones from ANS CR data"},
        "visual": {"cs": "Kde a jak smím létat", "en": "Where and how may I fly"},
        "lead": {
            "cs": "Vizuál vede rozhodovacím stromem evropských pravidel pro drony. Jednu jeho větev, zeměpisné zóny UAS, tady projdeš na skutečných datech: stáhneš aktuální zóny, které zveřejňuje Řízení letového provozu ČR, zjistíš, do kterých zón padají plánovaná místa letu, jak vysoko se v okolí letišť smí létat a jak se zóny mění v čase. Je to výuková pomůcka, ne právní posouzení: před letem vždy ověř zóny v aplikaci DroneMap a podmínky v opatřeních obecné povahy ÚCL.",
            "en": "The visual walks through the decision tree of the European drone rules. Here you go through one of its branches, UAS geographical zones, on real data: you download the current zones published by Air Navigation Services of the Czech Republic (ŘLP), find out which zones the planned flight sites fall into, how high you may fly near airports and how zones change over time. This is a teaching aid, not legal advice: before a flight always check the zones in the DroneMap app and the conditions in the CAA measures of general nature (OOP).",
        },
        "goal": {
            "cs": "načíst seznam zeměpisných zón a jejich soubory GeoJSON, určit zóny pro zadaná místa i pro celé území mapovacího letu, převést svislé hranice zón (AGL, AMSL, FL) na metry nad terénem, přečíst výškové omezení z gridové sítě kolem letišť a porovnat aktuální a budoucí vydání zón.",
            "en": "load the list of geographical zones and their GeoJSON files, determine the zones for given sites and for a whole mapping flight area, convert the vertical limits of zones (AGL, AMSL, FL) to metres above ground, read height restrictions from the grid around airports, and compare the current and the next release of the zones.",
        },
        "data": {
            "cs": "zeměpisné zóny UAS ve formátu GeoJSON (referenční hranice) ze stránky ŘLP https://aim.rlp.cz/?lang=cz&p=uas-gz, stažené v okamžiku spuštění; nadmořská výška terénu z Digitálního modelu reliéfu ČR 5. generace (DMR 5G, ČÚZK).",
            "en": "UAS geographical zones as GeoJSON (reference boundaries) from the ŘLP page https://aim.rlp.cz/?lang=cz&p=uas-gz, downloaded at run time; terrain elevation from the Digital terrain model of the Czech Republic, 5th generation (DMR 5G, ČÚZK).",
        },
        "sources": {
            "cs": [
                "Zeměpisné zóny UAS: Řízení letového provozu České republiky, s. p., AIM, https://aim.rlp.cz/?lang=cz&p=uas-gz; mapa zón: https://dronemap.gov.cz",
                "Prováděcí nařízení Komise (EU) 2019/947 o pravidlech a postupech pro provoz bezpilotních letadel, čl. 15 (zeměpisné zóny UAS); nařízení v přenesené pravomoci (EU) 2019/945.",
                "Úřad pro civilní letectví: opatření obecné povahy k zeměpisným zónám UAS (LKR311 až LKR320), https://www.caa.gov.cz",
                "Výška terénu: Digitální model reliéfu ČR 5. generace (DMR 5G), © ČÚZK, licence CC BY 4.0, služba https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer",
            ],
            "en": [
                "UAS geographical zones: Air Navigation Services of the Czech Republic (ŘLP ČR), AIM, https://aim.rlp.cz/?lang=en&p=uas-gz; zone map: https://dronemap.gov.cz",
                "Commission Implementing Regulation (EU) 2019/947 on the rules and procedures for the operation of unmanned aircraft, Article 15 (UAS geographical zones); Delegated Regulation (EU) 2019/945.",
                "Civil Aviation Authority of the Czech Republic: measures of general nature on UAS geographical zones (LKR311 to LKR320), https://www.caa.gov.cz",
                "Terrain elevation: Digital terrain model of the Czech Republic, 5th generation (DMR 5G), © ČÚZK, licence CC BY 4.0, service https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer",
            ],
        },
    }



def cells(t, P):
    out = [
        ("md", t("## 1. Příprava a seznam zón", "## 1. Setup and the list of zones")),
        ("code", "%pip install -q shapely pyproj rasterio"),
        ("code", t('''
import re, html, json, time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import shape, Point, box
import shapely
from pyproj import Transformer
import rasterio

AIM = "https://aim.rlp.cz"
def get(url, tries=4, **kw):
    for i in range(tries):
        try:
            r = requests.get(url, timeout=180, **kw); r.raise_for_status(); return r
        except requests.RequestException as e:
            print(url.split("/")[-1], type(e).__name__, "– zkusím znovu"); time.sleep(5 * (i + 1))
    raise RuntimeError(f"Nepodařilo se stáhnout {url}")

page = get(f"{AIM}/?lang=cz&p=uas-gz").content.decode("utf-8")
rows = []
for tr in re.findall(r"<tr.*?</tr>", page, re.S):
    href = re.search(r'href="(/data/uas/[^"]+\\.json)"', tr)
    cols = [re.sub(r"\\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
    if href and len(cols) >= 4:
        url = AIM + href.group(1)
        rows.append({"zóna": cols[0], "popis": cols[1], "soubor": cols[2], "velikost": cols[3],
                     "vydání": "aktuální" if "/actual/" in url else url.split("/")[-2], "url": url})
zones = pd.DataFrame(rows)
mb = zones.velikost.str.replace(",", ".").str.extract(r"([\\d.]+)\\s*(kB|MB)")
zones["MB"] = mb[0].astype(float) * np.where(mb[1] == "kB", 1e-3, 1)
pd.set_option("display.max_colwidth", 70)
zones[zones.vydání == "aktuální"][["zóna", "popis", "MB"]]
''', '''
import re, html, json, time, requests
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import shape, Point, box
import shapely
from pyproj import Transformer
import rasterio

AIM = "https://aim.rlp.cz"
def get(url, tries=4, **kw):
    for i in range(tries):
        try:
            r = requests.get(url, timeout=180, **kw); r.raise_for_status(); return r
        except requests.RequestException as e:
            print(url.split("/")[-1], type(e).__name__, "– retrying"); time.sleep(5 * (i + 1))
    raise RuntimeError(f"Could not download {url}")

page = get(f"{AIM}/?lang=en&p=uas-gz").content.decode("utf-8")
rows = []
for tr in re.findall(r"<tr.*?</tr>", page, re.S):
    href = re.search(r'href="(/data/uas/[^"]+\\.json)"', tr)
    cols = [re.sub(r"\\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip() for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
    if href and len(cols) >= 4:
        url = AIM + href.group(1)
        rows.append({"zone": cols[0], "description": cols[1], "file": cols[2], "size": cols[3],
                     "release": "current" if "/actual/" in url else url.split("/")[-2], "url": url})
zones = pd.DataFrame(rows)
mb = zones["size"].str.replace(",", ".").str.extract(r"([\\d.]+)\\s*(kB|MB)")
zones["MB"] = mb[0].astype(float) * np.where(mb[1] == "kB", 1e-3, 1)
pd.set_option("display.max_colwidth", 70)
zones[zones.release == "current"][["zone", "description", "MB"]]
''')),
        ("md", t(
            "## 2. Do kterých zón padají místa letu?\n\nStáhneme zóny do zvolené velikosti souboru (největší vrstvy, např. hustě osídlený prostor nebo silnice III. třídy, mají stovky MB a v Colabu by se stahovaly dlouho). Pro každé místo zjistíme, ve kterých zónách leží a jaká je svislá hranice zóny.",
            "## 2. Which zones do the flight sites fall into?\n\nWe download zones up to a chosen file size (the largest layers, e.g. densely populated areas or class III roads, have hundreds of MB and would take long to download in Colab). For each site we find out which zones it lies in and what the vertical limit of the zone is.")),
        ("code", t('''
MAX_MB = 20                   # ◀ parametr: největší stahovaný soubor (MB)
@SITES_CS@
current = zones[(zones.vydání == "aktuální") & (zones.MB <= MAX_MB) & ~zones.soubor.str.startswith("GRID")]
layers = {}
for _, z in current.iterrows():
    gj = get(z.url).json()
    layers[z.soubor.replace(".json", "")] = [(shape(f["geometry"]), f.get("properties") or {}) for f in gj["features"] if f.get("geometry")]
print(f"staženo {len(layers)} vrstev, {sum(len(v) for v in layers.values())} polygonů; nestaženo (velké): {', '.join(zones[(zones.vydání == 'aktuální') & (zones.MB > MAX_MB)].soubor)}")
hits = []
for site, (lat, lon) in SITES.items():
    pt = Point(lon, lat)
    for code, feats in layers.items():
        for geom, prop in feats:
            if geom.contains(pt):
                hits.append({"místo": site, "vrstva": code, "zóna": prop.get("ident"), "svislé hranice": prop.get("vertical_limit"),
                             "popis": current.set_index(current.soubor.str.replace(".json", "")).loc[code, "popis"]})
hits = pd.DataFrame(hits)
hits if len(hits) else print("žádné místo neleží ve stažené zóně")
''', '''
MAX_MB = 20                   # ◀ parameter: largest file to download (MB)
@SITES_EN@
current = zones[(zones.release == "current") & (zones.MB <= MAX_MB) & ~zones.file.str.startswith("GRID")]
layers = {}
for _, z in current.iterrows():
    gj = get(z.url).json()
    layers[z.file.replace(".json", "")] = [(shape(f["geometry"]), f.get("properties") or {}) for f in gj["features"] if f.get("geometry")]
print(f"downloaded {len(layers)} layers, {sum(len(v) for v in layers.values())} polygons; not downloaded (large): {', '.join(zones[(zones.release == 'current') & (zones.MB > MAX_MB)].file)}")
hits = []
for site, (lat, lon) in SITES.items():
    pt = Point(lon, lat)
    for code, feats in layers.items():
        for geom, prop in feats:
            if geom.contains(pt):
                hits.append({"site": site, "layer": code, "zone": prop.get("ident"), "vertical limits": prop.get("vertical_limit"),
                             "description": current.set_index(current.file.str.replace(".json", "")).loc[code, "description"]})
hits = pd.DataFrame(hits)
hits if len(hits) else print("no site lies in a downloaded zone")
''')),
        ("task", t(
            "Ve kterých zónách leží jednotlivá místa? Které místo je bez omezení ze stažených vrstev a proč to ještě neznamená, že tam smíš létat (které velké vrstvy jsi nestáhl a co by mohly změnit)? Přidej do SITES místo, kde chceš sám létat, a výsledek porovnej s mapou DroneMap.",
            "Which zones do the individual sites lie in? Which site is free of restrictions from the downloaded layers, and why does that still not mean you may fly there (which large layers did you not download, and what could they change)? Add a site where you want to fly yourself to SITES and compare the result with the DroneMap map.")),
        ("md", t(
            "## 3. Svislé hranice zón\n\nZóna platí jen mezi svou dolní a horní hranicí. Hranice se udávají nad terénem (AGL), nad střední hladinou moře (AMSL) nebo jako letová hladina (FL, stovky stop při standardním tlaku 1013,25 hPa; zde ji pro jednoduchost bereme jako výšku AMSL). 1 ft = 0,3048 m. Nadmořskou výšku terénu vezmeme z digitálního modelu reliéfu DMR 5G (ČÚZK).",
            "## 3. Vertical limits of zones\n\nA zone applies only between its lower and upper limit. Limits are given above ground (AGL), above mean sea level (AMSL) or as a flight level (FL, hundreds of feet at the standard pressure of 1013.25 hPa; here we treat it as an AMSL height for simplicity). 1 ft = 0.3048 m. Terrain elevation comes from the DMR 5G digital terrain model (ČÚZK).")),
        ("code", t(CUZK_HELPER["cs"] + '''
FLIGHT_AGL = 120              # ◀ parametr: plánovaná výška letu nad terénem (m)
def level(txt, ground):
    """Převede jednu hranici (např. 'GND', '3500 ft AMSL', '120 m AGL', 'FL95') na metry nad terénem."""
    s = txt.strip().upper().replace(" ", "")
    if s in ("GND", "SFC"): return 0.0
    if s.startswith("FL"): return float(s[2:]) * 100 * 0.3048 - ground
    m = re.match(r"([\\d.]+)(FT|M)(AGL|AMSL|MSL)", s)
    v = float(m.group(1)) * (0.3048 if m.group(2) == "FT" else 1)
    return v if m.group(3) == "AGL" else v - ground

T_JTSK = Transformer.from_crs(4326, 5514, always_xy=True)
def terrain(lat, lon):
    """Nadmořská výška terénu (m) z DMR 5G v bodě: střed malého výřezu 20 × 20 m."""
    x, y = T_JTSK.transform(lon, lat)
    z, _ = cuzk_raster("dmr5g", x - 10, y - 10, x + 10, y + 10, res=2.0)
    return float(z[z.shape[0] // 2, z.shape[1] // 2])
ground = {site: terrain(lat, lon) for site, (lat, lon) in SITES.items()}
if len(hits):
    lim = hits["svislé hranice"].str.split("-", n=1, expand=True)
    hits["terén (m n. m.)"] = hits["místo"].map(ground)
    hits["dolní (m AGL)"] = [level(a, g) for a, g in zip(lim[0], hits["terén (m n. m.)"])]
    hits["horní (m AGL)"] = [level(b, g) for b, g in zip(lim[1], hits["terén (m n. m.)"])]
    hits[f"let v {FLIGHT_AGL} m je v zóně"] = (hits["dolní (m AGL)"] <= FLIGHT_AGL) & (FLIGHT_AGL <= hits["horní (m AGL)"])
    print(hits[["místo", "zóna", "svislé hranice", "terén (m n. m.)", "dolní (m AGL)", "horní (m AGL)", f"let v {FLIGHT_AGL} m je v zóně"]].round(0).to_string())
airspace = pd.DataFrame([{"prostor": p.get("ident"), "svislé hranice": p.get("vertical_limit")} for _, p in layers.get("LKR320A", [])])
print("\\nLetecké prostory LKR320A podle svislých hranic:"); print(airspace["svislé hranice"].value_counts().head(10).to_string())
''', CUZK_HELPER["en"] + '''
FLIGHT_AGL = 120              # ◀ parameter: planned flight height above ground (m)
def level(txt, ground):
    """Convert one limit (e.g. 'GND', '3500 ft AMSL', '120 m AGL', 'FL95') to metres above ground."""
    s = txt.strip().upper().replace(" ", "")
    if s in ("GND", "SFC"): return 0.0
    if s.startswith("FL"): return float(s[2:]) * 100 * 0.3048 - ground
    m = re.match(r"([\\d.]+)(FT|M)(AGL|AMSL|MSL)", s)
    v = float(m.group(1)) * (0.3048 if m.group(2) == "FT" else 1)
    return v if m.group(3) == "AGL" else v - ground

T_JTSK = Transformer.from_crs(4326, 5514, always_xy=True)
def terrain(lat, lon):
    """Terrain elevation (m a.s.l.) from DMR 5G at a point: the centre of a small 20 × 20 m window."""
    x, y = T_JTSK.transform(lon, lat)
    z, _ = cuzk_raster("dmr5g", x - 10, y - 10, x + 10, y + 10, res=2.0)
    return float(z[z.shape[0] // 2, z.shape[1] // 2])
ground = {site: terrain(lat, lon) for site, (lat, lon) in SITES.items()}
if len(hits):
    lim = hits["vertical limits"].str.split("-", n=1, expand=True)
    hits["terrain (m AMSL)"] = hits["site"].map(ground)
    hits["lower (m AGL)"] = [level(a, g) for a, g in zip(lim[0], hits["terrain (m AMSL)"])]
    hits["upper (m AGL)"] = [level(b, g) for b, g in zip(lim[1], hits["terrain (m AMSL)"])]
    hits[f"flight at {FLIGHT_AGL} m is in the zone"] = (hits["lower (m AGL)"] <= FLIGHT_AGL) & (FLIGHT_AGL <= hits["upper (m AGL)"])
    print(hits[["site", "zone", "vertical limits", "terrain (m AMSL)", "lower (m AGL)", "upper (m AGL)", f"flight at {FLIGHT_AGL} m is in the zone"]].round(0).to_string())
airspace = pd.DataFrame([{"area": p.get("ident"), "vertical limits": p.get("vertical_limit")} for _, p in layers.get("LKR320A", [])])
print("\\nAirspace areas LKR320A by vertical limits:"); print(airspace["vertical limits"].value_counts().head(10).to_string())
''')),
        ("task", t(
            "@TASK3_CS@",
            "@TASK3_EN@")),
        ("md", t(
            "@GRIDMD_CS@",
            "@GRIDMD_EN@")),
        ("code", t('''
CENTER = @CENTER@       # ◀ parametr: střed mapy (šířka, délka)
SPAN = @SPAN@                   # ◀ parametr: poloviční rozsah mapy (°)
grid_url = zones[(zones.vydání == "aktuální") & (zones.soubor == "@GRID@.json")].url.iloc[0]
grid = [(shape(f["geometry"]), f["properties"]["vertical_limit"]) for f in get(grid_url).json()["features"]]
hmax = lambda txt: float(re.search(r"-\\s*([\\d.]+)\\s*m\\s*AGL", txt).group(1))
fig, ax = plt.subplots(figsize=(9, 7))
view = box(CENTER[1] - SPAN * 1.6, CENTER[0] - SPAN, CENTER[1] + SPAN * 1.6, CENTER[0] + SPAN)
cmap = plt.get_cmap("RdYlGn")
for g, v in grid:
    if g.intersects(view):
        x, y = g.exterior.xy; ax.fill(x, y, color=cmap(hmax(v) / 120), lw=0)
for site, (lat, lon) in SITES.items():
    ax.plot(lon, lat, "k^"); ax.annotate(site, (lon, lat), xytext=(4, 4), textcoords="offset points", fontsize=8)
ax.set_xlim(view.bounds[0], view.bounds[2]); ax.set_ylim(view.bounds[1], view.bounds[3]); ax.set_aspect(1 / np.cos(np.radians(CENTER[0])))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 120)); plt.colorbar(sm, ax=ax, label="povolená výška (m AGL)")
ax.set_title("gridová síť @GRID@"); plt.show()
for site, (lat, lon) in SITES.items():
    v = [hmax(lim) for g, lim in grid if g.contains(Point(lon, lat))]
    print(f"{site}: {'mimo síť' if not v else f'do {v[0]:.0f} m nad terénem'}")
''', '''
CENTER = @CENTER@       # ◀ parameter: centre of the map (latitude, longitude)
SPAN = @SPAN@                   # ◀ parameter: half the extent of the map (°)
grid_url = zones[(zones.release == "current") & (zones.file == "@GRID@.json")].url.iloc[0]
grid = [(shape(f["geometry"]), f["properties"]["vertical_limit"]) for f in get(grid_url).json()["features"]]
hmax = lambda txt: float(re.search(r"-\\s*([\\d.]+)\\s*m\\s*AGL", txt).group(1))
fig, ax = plt.subplots(figsize=(9, 7))
view = box(CENTER[1] - SPAN * 1.6, CENTER[0] - SPAN, CENTER[1] + SPAN * 1.6, CENTER[0] + SPAN)
cmap = plt.get_cmap("RdYlGn")
for g, v in grid:
    if g.intersects(view):
        x, y = g.exterior.xy; ax.fill(x, y, color=cmap(hmax(v) / 120), lw=0)
for site, (lat, lon) in SITES.items():
    ax.plot(lon, lat, "k^"); ax.annotate(site, (lon, lat), xytext=(4, 4), textcoords="offset points", fontsize=8)
ax.set_xlim(view.bounds[0], view.bounds[2]); ax.set_ylim(view.bounds[1], view.bounds[3]); ax.set_aspect(1 / np.cos(np.radians(CENTER[0])))
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(0, 120)); plt.colorbar(sm, ax=ax, label="allowed height (m AGL)")
ax.set_title("@GRID@ grid"); plt.show()
for site, (lat, lon) in SITES.items():
    v = [hmax(lim) for g, lim in grid if g.contains(Point(lon, lat))]
    print(f"{site}: {'outside the grid' if not v else f'up to {v[0]:.0f} m above ground'}")
''')),
        ("task", t(
            "@TASK4_CS@",
            "@TASK4_EN@")),
        ("md", t(
            "## 5. Celé území mapovacího letu\n\nMapovací let nepokrývá bod, ale plochu. Spočítáme, jaký podíl čtverce kolem místa leží v jednotlivých zónách (v metrech, v souřadnicích UTM 33N).",
            "## 5. The whole area of a mapping flight\n\nA mapping flight covers an area, not a point. We compute what share of a square around the site lies in each zone (in metres, in UTM 33N coordinates).")),
        ("code", t('''
SITE = "@SITE5_CS@"         # ◀ parametr: místo ze SITES
HALF_M = 1500                 # ◀ parametr: polovina strany čtverce letu (m)
T_UTM = Transformer.from_crs(4326, 32633, always_xy=True)
to_utm = lambda g: shapely.transform(g, lambda xy: np.column_stack(T_UTM.transform(xy[:, 0], xy[:, 1])))
lat, lon = SITES[SITE]; cx, cy = T_UTM.transform(lon, lat)
area = box(cx - HALF_M, cy - HALF_M, cx + HALF_M, cy + HALF_M)
share = []
for code, feats in layers.items():
    for geom, prop in feats:
        g = to_utm(geom)
        if g.intersects(area):
            share.append({"vrstva": code, "zóna": prop.get("ident"), "svislé hranice": prop.get("vertical_limit"), "podíl území (%)": 100 * g.intersection(area).area / area.area})
for g, v in grid:
    gu = to_utm(g)
    if gu.intersects(area):
        share.append({"vrstva": "@GRID@", "zóna": v, "svislé hranice": v, "podíl území (%)": 100 * gu.intersection(area).area / area.area})
share = pd.DataFrame(share)
print(f"{SITE}: čtverec {2 * HALF_M / 1000:.1f} × {2 * HALF_M / 1000:.1f} km")
share.groupby(["vrstva", "svislé hranice"])["podíl území (%)"].sum().round(1).to_frame() if len(share) else print("území neleží v žádné stažené zóně")
''', '''
SITE = "@SITE5_EN@"       # ◀ parameter: a site from SITES
HALF_M = 1500                 # ◀ parameter: half the side of the flight square (m)
T_UTM = Transformer.from_crs(4326, 32633, always_xy=True)
to_utm = lambda g: shapely.transform(g, lambda xy: np.column_stack(T_UTM.transform(xy[:, 0], xy[:, 1])))
lat, lon = SITES[SITE]; cx, cy = T_UTM.transform(lon, lat)
area = box(cx - HALF_M, cy - HALF_M, cx + HALF_M, cy + HALF_M)
share = []
for code, feats in layers.items():
    for geom, prop in feats:
        g = to_utm(geom)
        if g.intersects(area):
            share.append({"layer": code, "zone": prop.get("ident"), "vertical limits": prop.get("vertical_limit"), "share of area (%)": 100 * g.intersection(area).area / area.area})
for g, v in grid:
    gu = to_utm(g)
    if gu.intersects(area):
        share.append({"layer": "@GRID@", "zone": v, "vertical limits": v, "share of area (%)": 100 * gu.intersection(area).area / area.area})
share = pd.DataFrame(share)
print(f"{SITE}: square {2 * HALF_M / 1000:.1f} × {2 * HALF_M / 1000:.1f} km")
share.groupby(["layer", "vertical limits"])["share of area (%)"].sum().round(1).to_frame() if len(share) else print("the area does not lie in any downloaded zone")
''')),
        ("task", t(
            "Které zóny zasahují do čtverce letu, i když samotný střed v nich neleží? Jak se výsledek změní pro čtverec 0,5 km a 3 km? Jak bys mapovací let rozdělil, aby co nejvíc plochy leželo mimo omezení, a co bys musel vyřídit pro zbytek?",
            "Which zones reach into the flight square even though the centre itself is not in them? How does the result change for a 0.5 km and a 3 km square? How would you split the mapping flight so that as much area as possible lies outside restrictions, and what would you have to arrange for the rest?")),
        ("md", t(
            "## 6. Zóny se mění\n\nŘLP zveřejňuje kromě aktuálních zón i vydání, která začnou platit v budoucnu (podle cyklu AIRAC). Porovnáme vrstvy, které mají obě vydání: počet zón, jejich identifikátory a plochu, která přibude nebo ubude.",
            "## 6. Zones change\n\nBesides the current zones, ŘLP also publishes releases that will take effect in the future (following the AIRAC cycle). We compare layers that exist in both releases: the number of zones, their identifiers and the area added or removed.")),
        ("code", t('''
future = zones[(zones.vydání != "aktuální") & (zones.MB <= MAX_MB)]
if future.empty:
    print("ŘLP teď nezveřejňuje žádné budoucí vydání stažitelné velikosti.")
def load_layer(url):
    feats = [f for f in get(url).json()["features"] if f.get("geometry")]
    geoms = [shapely.make_valid(to_utm(shape(f["geometry"]))) for f in feats]
    return {f["properties"]["ident"] for f in feats}, shapely.union_all(geoms), len(feats)
for _, z in future.iterrows():
    ids0, u0, n0 = load_layer(zones[(zones.vydání == "aktuální") & (zones.soubor == z.soubor)].url.iloc[0])
    ids1, u1, n1 = load_layer(z.url)
    added, removed = sorted(ids1 - ids0), sorted(ids0 - ids1)
    print(f"{z.soubor} (vydání {z.vydání}): zón {n0} → {n1}, plocha {u0.area / 1e6:.2f} → {u1.area / 1e6:.2f} km², "
          f"přibude {u1.difference(u0).area / 1e6:.2f} km², ubude {u0.difference(u1).area / 1e6:.2f} km²")
    for name, lst in [("nové identifikátory", added), ("zrušené identifikátory", removed)]:
        if lst: print(f"   {name}: {', '.join(lst[:12])}{' …' if len(lst) > 12 else ''}")
''', '''
future = zones[(zones.release != "current") & (zones.MB <= MAX_MB)]
if future.empty:
    print("ŘLP is not publishing any future release of downloadable size right now.")
def load_layer(url):
    feats = [f for f in get(url).json()["features"] if f.get("geometry")]
    geoms = [shapely.make_valid(to_utm(shape(f["geometry"]))) for f in feats]
    return {f["properties"]["ident"] for f in feats}, shapely.union_all(geoms), len(feats)
for _, z in future.iterrows():
    ids0, u0, n0 = load_layer(zones[(zones.release == "current") & (zones.file == z.file)].url.iloc[0])
    ids1, u1, n1 = load_layer(z.url)
    added, removed = sorted(ids1 - ids0), sorted(ids0 - ids1)
    print(f"{z.file} (release {z.release}): zones {n0} → {n1}, area {u0.area / 1e6:.2f} → {u1.area / 1e6:.2f} km², "
          f"{u1.difference(u0).area / 1e6:.2f} km² added, {u0.difference(u1).area / 1e6:.2f} km² removed")
    for name, lst in [("new identifiers", added), ("withdrawn identifiers", removed)]:
        if lst: print(f"   {name}: {', '.join(lst[:12])}{' …' if len(lst) > 12 else ''}")
''')),
        ("task", t(
            "Které vrstvy se v příštím vydání mění, kolik zón a plochy přibude nebo ubude? Proč musí mít dron aktuální data pro funkci geografického povědomí (geo-awareness) a proč nestačí zóny zkontrolovat jednou při plánování projektu, který trvá několik týdnů?",
            "Which layers change in the next release, and how many zones and how much area are added or removed? Why must a drone have current data for its geo-awareness function, and why is it not enough to check the zones once when planning a project that lasts several weeks?")),
        ("task", t("@PLUS_CS@", "@PLUS_EN@")),
    ]
    tokens = {"@SITES_CS@": P["sites_cs"], "@SITES_EN@": P["sites_en"], "@TASK3_CS@": P["task3_cs"], "@TASK3_EN@": P["task3_en"],
              "@GRIDMD_CS@": P["grid_md_cs"], "@GRIDMD_EN@": P["grid_md_en"],
              "@TASK4_CS@": P["task4_cs"], "@TASK4_EN@": P["task4_en"], "@GRID@": P["grid"], "@CENTER@": P["center"], "@SPAN@": P["span"],
              "@SITE5_CS@": P["site5_cs"], "@SITE5_EN@": P["site5_en"], "@PLUS_CS@": P["plus_cs"], "@PLUS_EN@": P["plus_en"]}
    res = []
    for kind, text in out:
        for k, v in tokens.items():
            text = text.replace(k, v)
        assert not re.search(r"@[A-Z0-9_]+@", text), text[:200]
        res.append((kind, text))
    return res
