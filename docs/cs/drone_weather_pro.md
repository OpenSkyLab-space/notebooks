# Můžu letět?, pokročilá verze: jak přesný je model, profil větru a létavé hodiny

Popis notebooku k vizuálu [Můžu letět? Počasí pro drony](https://openskylab.space/edu_viz_drone_weather.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/drone_weather_pro_cs.ipynb) · verze 1.0 · asi 50 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku o počasí pro drony. Modelovou předpověď Open-Meteo porovnáš s týdnem skutečných zpráv METAR ze čtyř českých letišť a spočítáš, jak moc se model plete ve větru, teplotě a rosném bodu. Pak z tří měsíců modelových dat pro Roztoky zjistíš, jak se mění profil větru se stabilitou ovzduší během dne a ve kterých hodinách se dalo létat nejčastěji.

## Cíl

Dekódovat týden zpráv METAR, ověřit proti nim model (odchylka, RMSE, korelace), spočítat exponent profilu větru a jeho závislost na teplotním zvrstvení a sestavit denní chod podílu hodin vhodných k letu podle větru, nárazů, srážek, dohlednosti a námrazy.

## Data

Zprávy METAR za posledních 7 dní z letišť Praha (LKPR), Brno (LKTB), Ostrava (LKMT) a Karlovy Vary (LKKV) ze služby NOAA Aviation Weather Center; hodinová data Open-Meteo za stejných 7 dní pro souřadnice letišť a za 92 dní pro Roztoky (vítr v 10, 80 a 120 m, nárazy, teplota ve 2 a 120 m, rosný bod, srážky, dohlednost). Hodnoty Open-Meteo pro minulé dny jsou uložené krátkodobé předpovědi modelů, ne měření. Data se průběžně mění, tvoje čísla budou jiná než v uloženém notebooku.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava

Načte knihovny a stáhne data.

### 2. Týden zpráv METAR

Stáhneme zprávy za 7 dní, dekódujeme vítr, nárazy, teplotu, rosný bod, dohlednost a základnu oblačnosti a ponecháme jednu zprávu na hodinu. Zpráva nese jen den v měsíci, měsíc a rok doplníme podle dnešního data.

Parametry, které student mění:

- `AIRPORTS = {"LKPR": (50.1008, 14.2600), "LKTB": (49.1513, 16.6944), "LKMT": (49.6963, 18.1111), "LKKV": (50.2030, 12.9150)}`: letiště a souřadnice

### 3. Ověření modelu

Pro každé letiště stáhneme z Open-Meteo hodinová data za stejných 7 dní a spárujeme je se zprávami. **Odchylka** je průměr rozdílu model − pozorování (systematická chyba), **RMSE** odmocnina průměru čtverců rozdílu (celková chyba), **korelace** říká, jak dobře model zachytil průběh.

**Úkol 1.** Podhodnocuje model vítr, nebo ho nadhodnocuje? Jak velká je RMSE ve srovnání s typickou rychlostí větru na letišti? Na kterém letišti model sedí nejhůř a čím to může být (terén v okolí, údolí, rozlišení modelu)? Proč METAR udává vítr v celých uzlech a jakou chybu to samo o sobě přináší?

**Úkol 2.** Jak přesně model trefuje teplotu a rosný bod? Odhad základny oblačnosti je 125 m na každý stupeň rozdílu T − Td: o kolik metrů se odhad posune, když se rosný bod splete o 1 °C? Co z toho plyne pro rozhodování o mlze, nízké oblačnosti a námraze podle modelu?

### 4. Profil větru a stabilita ovzduší

Vítr s výškou roste přibližně podle u(z) = u(10 m) · (z / 10)^α. Exponent α spočítáme z větru v 10 a 120 m pro každou hodinu za 92 dní a porovnáme ho s rozdílem teploty ve 120 a 2 m. Klesá-li teplota s výškou rychleji než o 1 °C na 100 m, je ovzduší labilní a promíchává se; roste-li s výškou (inverze), je stabilní.

Parametry, které student mění:

- `LAT, LON = 50.152, 14.392`: místo letu (Roztoky)

**Úkol 3.** Proč je α v noci a ráno velké a přes den malé? Proč je při inverzi u země téměř bezvětří, zatímco ve 120 m fouká? Co to znamená, když ráno před vzletem změříš vítr ručním anemometrem a podle něj odhaduješ vítr ve výšce letu? V kolik hodin se inverze typicky rozpouští?

### 5. Létavé hodiny za poslední tři měsíce

Pro každou hodinu za 92 dní vyhodnotíme podmínky jako semafor v základní verzi: vítr ve 120 m, odhad nárazů ve 120 m, srážky, dohlednost a riziko námrazy. Nárazy ve 120 m model nedává, proto je odhadneme ze 10 m dvěma způsoby (`GUSTS`).

Parametry, které student mění:

- `LIM_WIND, LIM_GUST = 10.0, 12.0`: limit větru ve 120 m a nárazů (m/s)
- `LIM_VIS = 5000`: nejmenší dohlednost (m)
- `GUSTS = "poměr"`: odhad nárazů ve 120 m: "poměr" (stejný poměr nárazy/vítr jako v 10 m) nebo "přírůstek" (stejný rozdíl)

**Úkol 4.** Která podmínka v posledních třech měsících omezovala létání nejčastěji a ve kterou denní dobu byla šance na let nejlepší? Přepni `GUSTS` na druhý způsob odhadu nárazů: o kolik se změní podíl létavých hodin? Který odhad je podle tebe bližší skutečnosti a proč (jak se poryvy mění s výškou)?

**Úkol 5.** Nastav limity pro menší dron (`LIM_WIND = 8`, `LIM_GUST = 10.7` jako odolnost DJI Mini 4 Pro) a pak pro přísnější provoz se snímkováním (dohlednost 8 km). Jak se změní podíl létavých hodin a jejich denní chod? Proč by tento výpočet pro zimní měsíce vyšel jinak?

**Rozšíření (nepovinné).** Přidej do `AIRPORTS` letiště Linec (`"LOWL": (48.2332, 14.1875)`) nebo jiné a porovnej přesnost modelu. Změň `LAT, LON` na jiné místo letu (třeba Brno-Bystrc 49.2467, 16.4798) a porovnej profil větru a létavé hodiny.

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- METAR: NOAA/NWS Aviation Weather Center, https://aviationweather.gov/data/api/ (veřejná data vlády USA).
- Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- Klíč ke zprávám METAR: ICAO Annex 3 / WMO-No. 306, kód FM 15.
- Stull, R. B. (1988). *An Introduction to Boundary Layer Meteorology*. Kluwer (denní chod mezní vrstvy, stabilita, profil větru).
- Odolnost DJI Mavic 3 Enterprise vůči větru 12 m/s a DJI Mini 4 Pro 10,7 m/s (technické listy DJI).

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
