# Kdy letět s termokamerou, pokročilá verze: svahy, stíny a les na skutečném terénu

Popis notebooku k vizuálu [Kdy letět s termokamerou](https://openskylab.space/edu_viz_thermal_timing.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/thermal_timing_pro_cs.ipynb) · verze 1.0 · asi 55 min · čtyři úkolů

## O čem notebook je

Pokročilá verze notebooku o načasování termálního snímkování. Model povrchu ze základní verze tu běží pro každou čtyřmetrovou buňku skutečného svahu údolí Vltavy u Roztok: se sklonem a orientací z DMR 5G, se stíny terénu, s rozlišením lesa a louky z DMP 1G a se skutečným přímým a rozptýleným zářením z Open-Meteo. Zjistíš, kdy samotný terén vytváří v termosnímku největší a nejmenší rozdíly a kdy se les a louka teplotně překříží.

## Cíl

Spočítat polohu Slunce, osvit svahů a stíny terénu, spustit energetickou bilanci povrchu pro každou buňku území, porovnat teplotu luk podle orientace svahu během dne a najít denní dobu, kdy je teplota nejméně ovlivněná terénem, ve slunečném i zataženém dni.

## Data

DMR 5G (terén) a DMP 1G (povrch) z ČÚZK, buňka 4 m, území 1 × 0,7 km na levém svahu údolí Vltavy u Roztok; hodinová teplota, vlhkost, přímé (na kolmou plochu) a rozptýlené záření, oblačnost a vítr z Open-Meteo za posledních 92 dní (model počasí, ne měření na místě); tepelné vlastnosti louky a lesa stejné jako v základní verzi. Model nepočítá se stékáním studeného vzduchu do údolí v noci, s odraženým zářením z okolních svahů ani s vlhkostí půdy, která se mění; DMP 1G je z let 2009–2013.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava, terén a počasí

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

Parametry, které student mění:

- `LAT, LON = 50.152, 14.392`: střed území (levý svah údolí Vltavy u Roztok)
- `FOREST_H = 5.0`: od jaké výšky vegetace (m) počítáme buňku jako les
- `DAY, CLOUDY = days.idxmax().date(), days.idxmin().date()`: den k výpočtu (výchozí je nejslunečnější a nejzataženější)

### 2. Slunce, svahy a stíny

Přímé záření dopadá na svah úměrně cos i, kde i je úhel mezi paprskem a kolmicí ke svahu: cos i = cos z · cos s + sin z · sin s · cos(φ − A), z je zenitový úhel Slunce, φ jeho azimut, s sklon a A orientace svahu. Buňka je ve stínu, když terén ve směru Slunce stíní paprsek. Mapy ukazují cos i ve stínu nulové.

Parametry, které student mění:

- `hours = [7, 9, 13, 17]`: místní hodiny pro mapy

**Úkol 1.** Které části území jsou v 7 hodin ve stínu a proč právě ty? Proč jsou ráno nejvíc osvětlené svahy obrácené k východu a v 17 hodin k západu, i když Slunce je v obou časech podobně vysoko? Co to znamená pro termosnímek údolí pořízený brzy ráno?

### 3. Teplota povrchu každé buňky

Pro každou buňku běží stejná energetická bilance jako v základní verzi, jen pohlcené záření je přímé záření krát cos i (mimo stín) plus rozptýlené záření krát podíl oblohy, který buňka vidí. Louka má půdu s vedením tepla do hloubky, les je tenká vrstva korun. Model běží od tří dní před vybraným dnem, výpočet trvá asi minutu.

Parametry, které student mění:

- `MEADOW = dict(alb=0.20, eps=0.98, k=1.2, C=2.5e6, rs=70.0)`: louka (albedo, emisivita, vodivost, kapacita půdy, odpor průduchů)
- `FOREST = dict(alb=0.12, eps=0.98, rs=100.0, node=3.0e4, rough=3.0)`: les (koruny jako jedna tenká vrstva)

**Úkol 2.** O kolik stupňů se v 9 a ve 13 hodin liší louky na svazích obrácených k východu, jihu, západu a severu? Proč je ve 13 hodin nejteplejší jižní svah, ale v 17 hodin západní? Proč jsou rozdíly ve 21 hodin skoro pryč? Co by z toho plynulo pro hledání podmáčených míst na loukách podle teploty v poledne?

### 4. Kdy terén ruší nejméně

Rozptyl teploty mezi buňkami stejného povrchu (rozdíl 95. a 5. percentilu) ukazuje, jak velké rozdíly v termosnímku vytváří samotný terén, ne rozdíly v povrchu. Porovnáme nejslunečnější a nejzataženější den a sledujeme i rozdíl lesa a louky.

**Úkol 3.** Ve kterou denní dobu je rozptyl teploty louky nejmenší a jak dlouho po západu Slunce trvá, než rozdíly mezi svahy zmizí? Proč nezmizí hned? Změň v `MEADOW` tepelnou vodivost `k` na 0,6 (suchá půda) a sleduj, jak se to změní. Jak velký je rozptyl v zataženém dni a proč?

**Úkol 4.** Kdy se les a louka ve slunečném dni teplotně překříží a jak se to liší od zataženého dne? Model nepočítá se stékáním studeného vzduchu do údolí. Jak by skutečný termosnímek údolí před svítáním vypadal jinak než model a proč by pak nejmenší rozptyl nemusel být právě před svítáním?

**Rozšíření (nepovinné).** Nastav `LAT, LON` na svah nad Brněnskou přehradou (49.2467, 16.4798) nebo na údolí u Hosína u Hluboké nad Vltavou (49.0452, 14.4769) a porovnej stíny, rozdíly podle orientace svahů a čas nejmenšího rozptylu.

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Digitální model reliéfu ČR 5. generace (DMR 5G) a Digitální model povrchu ČR 1. generace (DMP 1G), © ČÚZK, licence CC BY 4.0, služby https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer a https://ags.cuzk.cz/arcgis2/rest/services/dmp1g/ImageServer
- Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- Poloha Slunce: NOAA Global Monitoring Laboratory, *General Solar Position Calculations* (vzorce pro deklinaci a časovou rovnici).
- Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744.
- Oke, T. R. (1987). *Boundary Layer Climates*, 2. vyd. Routledge (tepelné vlastnosti půdy, albeda, místní klima svahů).
- Maes, W. H. (2025). Practical guidelines for performing UAV mapping flights with snapshot sensors. *Remote Sensing* 17(4), 606. https://doi.org/10.3390/rs17040606

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
