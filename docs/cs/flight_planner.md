# Plán letu nad údolím Vltavy: GSD, překryvy, terén a vítr

Popis notebooku k vizuálu [Plánovač letu dronu](https://openskylab.space/edu_viz_flight_planner.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/flight_planner_cs.ipynb) · verze 1.0 · asi 50 min · pět úkolů

## O čem notebook je

Ve vizuálu jsi plánoval let nad rovinou a nad modelovým kopcem. Tady stejné vzorce použiješ na skutečný terén: svah údolí Vltavy u Roztok z digitálního modelu reliéfu ČÚZK DMR 5G (lidar, buňka 2 m) a na aktuální předpověď větru ve výšce letu.

## Cíl

Spočítat výšku letu pro cílové GSD, rozestup linek, interval a rychlost, rozmazání a zkosení, ukázat, jak terén mění výšku nad zemí a překryv, a naplánovat návrat proti větru.

## Data

DMR 5G (ČÚZK, služba ImageServer, výšky v Bpv, buňka 2 m) pro území 1,2 × 0,8 km na levém svahu údolí Vltavy u Roztok; hodinová předpověď větru ve 10, 80 a 120 m z Open-Meteo; parametry kamer z technických listů výrobců (stejné jako ve vizuálu).

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

### 2. Kamera, výška a GSD

GSD = H · p / f, kde p je velikost pixelu na čipu (šířka čipu / počet pixelů). Z cílového GSD tedy H = GSD · f / p.

Parametry, které student mění:

- `gsd_target = 1.5`: cílové GSD v cm/px

**Úkol 1.** Proč musí Mavic 3M pro stejné GSD letět mnohem níž než P1? Nastav `gsd_target` na 2 a pak na 4 cm/px. Pro které kamery a GSD by výška překročila 120 m, a tedy limit otevřené kategorie? Jaké má nízký let důsledky (počet snímků, čas, bezpečnost)?

### 3. Skutečný terén a plán linek

Načteme DMR 5G pro svah údolí Vltavy. Linky vedou ve směru východ–západ, tedy po spádnici dolů a zpět nahoru. Místo vzletu je na planině na západním okraji.

Parametry, které student mění:

- `cam = CAMERAS["Mavic 3E"]`: kamera
- `H0 = 80`: výška letu nad místem vzletu (m)
- `fo, so = 0.80, 0.70`: podélný a příčný překryv
- `v_air = 10.0`: rychlost vůči vzduchu (m/s)
- `long_across = True`: delší strana snímku napříč letem?

**Úkol 2.** Zvyšuj `v_air`, dokud se neobjeví upozornění, že kamera nestihne. Jaká je nejvyšší rychlost? Přepni `long_across = False`: jak se změní báze, nejvyšší rychlost, počet linek a čas letu? Proč otočený snímek dovolí rychlejší let, a přesto může let trvat déle? Nastav podélný překryv 0,85 jako pro vegetaci.

### 4. Stálá výška, nebo sledování terénu?

Při stálé výšce nad místem vzletu se výška nad zemí mění s terénem: H_AGL = H0 + z_vzlet − z. S ní se mění GSD i záběr, ale báze a rozestup linek zůstávají, takže se mění skutečný překryv.

Parametry, které student mění:

- `follow = False`: True = sledování terénu (stálá výška nad zemí H0)

**Úkol 3.** Při stálé výšce 80 m nad místem vzletu: jaký je rozsah GSD a překryvů? Kde je překryv nejmenší, nahoře u místa vzletu, nebo v nejnižších místech, a proč? Kolik území je výš než 120 m nad terénem? Přepni `follow = True`: co se zlepší a co k sledování terénu potřebuješ (model terénu, jeho přesnost, překážky)?

### 5. Skutečný vítr, rozmazání a postupná závěrka

Z Open-Meteo vezmeme předpověď větru pro toto území na dnešek. Rozmazání = rychlost vůči zemi · expozice / GSD; zkosení postupnou závěrkou = rychlost vůči zemi · doba vyčtení čipu / GSD. Zenmuse P1 a Mavic 3E mají mechanickou závěrku, takže u nich zkosení prakticky odpadá (t_read = 0); výchozích 30 ms je řádová hodnota pro elektronickou postupnou závěrku.

Parametry, které student mění:

- `hour = 6 + int(met.wind_speed_80m.values[6:21].argmax())`: hodina letu (místní čas); výchozí je největrnější hodina mezi 6 a 20 h
- `t_exp = 1 / 1000`: expoziční čas (s)
- `t_read = 0.030`: doba vyčtení čipu u postupné závěrky (s); 0 = globální závěrka

**Úkol 4.** Jaký vítr hlásí předpověď ve 10, 80 a 120 m a proč se liší? Jak se liší rozmazání a zkosení na lince po větru a proti větru? Proč zkosení nezmenší kratší expozice? Kdy bys linky raději otočil podél větru, nebo napříč?

### 6. Baterie a návrat domů

Mavic 3E má baterii 77 Wh a výrobce udává až 45 min letu bez větru, tedy průměrně asi 100 W. Spočítáme, kolik energie potřebuje návrat z nejvzdálenějšího bodu, když vítr fouká od místa vzletu.

Parametry, které student mění:

- `E_bat = 77.0`: energie baterie (Wh)
- `temp_factor = 1.0`: využitelná kapacita (1,0 při 20 °C; v mrazu zhruba 0,7–0,8)
- `reserve = 0.20`: rezerva při přistání

**Úkol 5.** Stačí jedna baterie? Nastav `temp_factor = 0.75` a pak zvyš vítr (`headwind = 8`). Proč je „tam po větru, zpátky proti větru“ past? Zkus také vyšší `v_air`: proč při silném větru pomáhá letět rychleji, i když výkon roste?

**Rozšíření (nepovinné).** Spolužáci mohou mít notebook pro jiné území (Roztoky, Brno-Bystrc, Hosín u Hluboké). Porovnejte převýšení, rozsah výšky nad zemí při stálé výšce 80 m nad místem vzletu a podíl území nad 120 m. Kde by stálá výška byla nejméně vhodná a kolik baterií by na území potřeboval každý z vás?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Digitální model reliéfu České republiky 5. generace (DMR 5G), © ČÚZK, licence CC BY 4.0, služba https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer
- Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- Parametry kamer: technické listy DJI Zenmuse P1, Mavic 3 Enterprise (3E, 3M) a obecná kamera 1″ 20 Mpx (u Mavic 3M a obecné kamery je nejkratší interval 2 s orientační hodnota); baterie Mavic 3 Enterprise 5000 mAh, 15,4 V (77 Wh).
- Výška letu v otevřené kategorii max. 120 m od nejbližšího bodu zemského povrchu: prováděcí nařízení Komise (EU) 2019/947, příloha, UAS.OPEN.010.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
