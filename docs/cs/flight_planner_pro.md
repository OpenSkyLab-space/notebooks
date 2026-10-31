# Plánovač letu, pokročilá verze: pokrytí snímky, sledování terénu, vítr a baterie

Popis notebooku k vizuálu [Plánovač letu dronu](https://openskylab.space/edu_viz_flight_planner.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/flight_planner_pro_cs.ipynb) · verze 1.0 · asi 60 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku k plánování letu. Na zalesněném svahu údolí Vltavy u Roztok porovnáš tři způsoby, jak držet výšku: stálou nad místem vzletu, sledování terénu z DMR 5G a sledování povrchu korun z DMP 1G. Pro každý spočítáš, na kolika snímcích je každý bod vidět, jaký je odstup od stromů a jak rychle by dron musel stoupat. Pak podle dnešní předpovědi větru vybereš směr linek a rozdělíš misi na lety po jedné baterii.

## Cíl

Spočítat pokrytí území snímky a odstup od povrchu pro tři režimy výšky, určit potřebné vyhlazení výškového profilu podle rychlosti stoupání, najít nejrychlejší směr linek při skutečném větru a rozdělit misi na lety tak, aby na každý návrat zbyla energie.

## Data

DMR 5G (terén) a DMP 1G (povrch včetně vegetace a budov) z ČÚZK, služby ImageServer, buňka 2 m, území 1,2 × 0,8 km na levém svahu údolí Vltavy u Roztok; hodinová předpověď větru v 80 m z Open-Meteo na dnešní den; parametry dronu a kamery Mavic 3E z technického listu výrobce. DMP 1G vznikl z leteckého laserového skenování v letech 2009–2013, takže stromy od té doby mohly vyrůst nebo být pokáceny. Model pokrytí předpokládá kameru mířící kolmo dolů a nepočítá se zákryty (koruna zakryje terén pod sebou), čas otočky je orientační.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

### 2. Terén, povrch a plán linek

DMR 5G popisuje holý terén, DMP 1G povrch, který vidí kamera: koruny stromů a střechy. Jejich rozdíl je výška vegetace a budov. Plán je stejný jako v základní verzi: kamera Mavic 3E, linky východ–západ, místo vzletu na západním okraji.

Parametry, které student mění:

- `LON, LAT = 14.392, 50.152`: střed území (levý svah údolí Vltavy u Roztok)
- `HOME = (0.0, Hh / 2)`: poloha místa vzletu v území (x, y v m)
- `H0 = 80.0`: výška letu (m) nad místem vzletu, nad terénem nebo nad povrchem podle režimu
- `FO, SO = 0.80, 0.70`: podélný a příčný překryv
- `V = 8.0`: rychlost vůči vzduchu (m/s)
- `SMOOTH = 40`: délka vyhlazení výškového profilu linky (m) při sledování terénu a povrchu

### 3. Na kolika snímcích je každý bod vidět

Pro každý snímek spočítáme, které buňky povrchu leží v jeho záběru. Záběr se zvětšuje s výškou kamery nad tím, co vidí, takže koruny blíž ke kameře pokryje menší výřez. Porovnáme tři režimy: **stálá** výška H0 nad místem vzletu, **terén** (H0 nad DMR 5G) a **povrch** (H0 nad DMP 1G). U sledování se výškový profil linky vyhlazuje (`SMOOTH`).

**Úkol 1.** Na rovině by byl každý bod na tolika snímcích, kolik vypsala buňka s plánem. Proč při sledování terénu vychází medián menší a při stálé výšce a sledování povrchu větší? Kde v mapě stálé výšky jsou místa s nejmenším počtem snímků a proč? Pro fotogrammetrii lesa se obvykle doporučuje vyšší překryv: změň `FO` a `SO` a sleduj podíl bodů s méně než 9 snímky.

**Úkol 2.** Podívej se na nejmenší odstup od povrchu a rozsah GSD. Proč je při stálé výšce odstup nad nejvyššími korunami nejmenší a GSD nejvíc kolísá? Co by se stalo při sledování terénu, kdyby stromy od skenování v letech 2009–2013 vyrostly o 5 m nebo kdyby v území stál stožár, který DMP nezachytil? Nastav `H0 = 50` a porovnej.

### 4. Jak rychle by dron musel stoupat

Při sledování terénu nebo povrchu letí dron rychlostí V a výška se mění podle profilu linky. Svislá rychlost je V krát sklon profilu. Když přesáhne limit stoupání nebo klesání, musí dron zpomalit. Tabulka ukazuje různé délky vyhlazení: 2 m znamená bez vyhlazení.

Parametry, které student mění:

- `V_UP, V_DOWN = 6.0, 6.0`: nejvyšší rychlost stoupání a klesání (m/s), Mavic 3E v normálním režimu

**Úkol 3.** Proč je profil povrchu mnohem strmější než profil terénu, i když jde o stejné linky? Jakou nejkratší délku vyhlazení potřebuješ, aby dron při 8 m/s stačil s limitem 6 m/s, a co tím ztratíš (sloupce s tím, o kolik letí výš než H0)? Jak by se výsledek změnil při rychlosti 12 m/s?

### 5. Vítr a směr linek

Dron drží rychlost vůči vzduchu V. Na lince po větru se rychlost vůči zemi zvětší, proti větru zmenší a při bočním větru musí dron nadržovat, takže se zmenší v obou směrech. Spočítáme čas celé mise pro azimuty linek od 0° do 165° s dnešním větrem v 80 m. Linky pokrývají celý obdélník území, otočka stojí `T_TURN` sekund.

Parametry, které student mění:

- `WIND = float(met.wind_speed_80m.iloc[hour])`: rychlost větru (m/s); výchozí je největrnější hodina dneška mezi 6 a 20 h
- `WDIR = float(met.wind_direction_80m.iloc[hour])`: odkud vítr fouká (°, 0 = od severu)
- `T_TURN = 8.0`: čas na jednu otočku (s), orientačně

**Úkol 4.** Při jakém azimutu je dnes mise nejkratší a jak velký je rozdíl proti nejhoršímu? Proč jsou linky po větru a proti větru pomalejší než linky napříč větru, i když se zisk po větru a ztráta proti větru zdánlivě vyrovnají? Nastav `WIND = 2` a pak `WIND = 0`: který azimut vyhraje teď a proč (počet linek a otoček)? Co se stane, když `WIND` přesáhne `V`?

### 6. Rozdělení mise na baterie

Linky se přidávají do letu jedna po druhé, dokud po další lince zbývá energie na přímý návrat k místu vzletu. Pak dron přistane, vymění baterii a další let začne přeletem k následující lince.

Parametry, které student mění:

- `AZ = int(orient["čas (min)"].idxmin())`: azimut linek (°); výchozí je nejrychlejší z tabulky
- `E_BAT, TEMP, RESERVE = 77.0, 1.0, 0.20`: baterie (Wh), využitelná kapacita (v mrazu 0,7–0,8), rezerva při přistání

**Úkol 5.** Kolik letů mise potřebuje a proč mají lety různý počet linek? Přesuň místo vzletu `HOME` do středu území (600, 400) a spusť znovu buňky od načtení dat: ušetříš let? Nastav `TEMP = 0.75` jako v mrazu. Proč se při plánování počítá s návratem proti větru, i když vítr může během letu zeslábnout?

**Rozšíření (nepovinné).** Nastav `LON, LAT` na svah nad Brněnskou přehradou (16.4798, 49.2467) nebo na údolí u Hosína u Hluboké nad Vltavou (14.4769, 49.0452), kde stoupá terén také od východu k západu, a porovnej pokrytí, vyhlazení a počet letů s Roztoky.

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Digitální model reliéfu České republiky 5. generace (DMR 5G) a Digitální model povrchu České republiky 1. generace (DMP 1G), © ČÚZK, licence CC BY 4.0, služby https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer a https://ags.cuzk.cz/arcgis2/rest/services/dmp1g/ImageServer
- ČÚZK: *Technická zpráva k digitálnímu modelu povrchu České republiky 1. generace (DMP 1G)*, https://geoportal.cuzk.gov.cz/Dokumenty/TECHNICKA_ZPRAVA_DMP_1G.pdf (úplná střední chyba výšky 0,4 m pro budovy a 0,7 m pro vegetaci).
- Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- DJI: *Mavic 3 Enterprise, specifikace* (https://enterprise.dji.com/mavic-3-enterprise/specs): čip 4/3, 5280 × 3956 px, ohnisko 12,3 mm; stoupání 6 m/s a klesání 6 m/s v normálním režimu; výdrž 45 min; baterie 77 Wh.
- Výška letu v otevřené kategorii max. 120 m od nejbližšího bodu zemského povrchu: prováděcí nařízení Komise (EU) 2019/947, příloha, UAS.OPEN.010.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
