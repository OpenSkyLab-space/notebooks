# Od DN k odrazivosti, pokročilá verze: topografická korekce v Krkonoších

Popis notebooku k vizuálu [Od DN k odrazivosti](https://openskylab.space/edu_viz_dn_to_reflectance.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/dn_to_reflectance_pro_cs.ipynb) · verze 1.0 · asi 70 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku k převodu DN na odrazivost. Vzorec pro odrazivost TOA dělí sinem výšky Slunce, tedy předpokládá rovinu. V horách ale každý svah dostává jiné osvětlení. Spočítáš ho z digitálního modelu terénu pro dvě scény Landsatu 8 s různou výškou Slunce, změříš, jak silně mění odrazivost lesa, a porovnáš pět topografických korekcí.

## Cíl

Spočítat sklon, orientaci a úhel dopadu slunečního záření z DEM, změřit vliv terénu na odrazivost v jednotlivých pásmech a ročních obdobích, porovnat kosinovou korekci, C-korekci, Minnaertovu korekci a SCS+C a posoudit, jak korekci poctivě ověřit.

## Data

Landsat 8 OLI Collection 1 Level-1 z veřejného archivu Google Cloud: `LC08_L1TP_191025_20190626_20190705_01_T1` (26. 6. 2019, výška Slunce 60°) a `LC08_L1TP_191025_20181013_20181030_01_T1` (13. 10. 2018, výška Slunce 31°), pásma B2–B7, BQA a MTL; Copernicus DEM GLO-30 z registru AWS Open Data; třídy ESA WorldCover 2021 v200. Výřez 12 × 12 km ve východních Krkonoších, asi 25 MB.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a data

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

Parametry, které student mění:

- `SCENES = {"léto": "LC08_L1TP_191025_20190626_20190705_01_T1", "podzim": "LC08_L1TP_191025_20181013_20181030_01_T1"}`: dvě scény s různou výškou Slunce
- `LON, LAT, SIZE = 15.70, 50.70, 12000`: střed výřezu (Krkonoše) a jeho strana (m)

### 2. Osvětlení svahu z modelu terénu

Na rovině dopadá přímé sluneční záření pod zenitovým úhlem θ_s, na svahu se sklonem s a orientací a pod úhlem i: cos i = cos θ_s · cos s + sin θ_s · sin s · cos(φ_s − a), kde φ_s je azimut Slunce. Přímé ozáření svahu je úměrné cos i; difuzní světlo oblohy dopadá ze všech směrů a na orientaci svahu závisí mnohem méně.

**Úkol 1.** Porovnej mapy cos i v létě a na podzim. Proč se na podzim osvětlení jižních a severních svahů liší mnohem víc a kolik pixelů je ve vlastním stínu? Proč vzorec odrazivosti TOA z notebooku k vizuálu (dělení sinem výšky Slunce) na svahu nedává skutečnou odrazivost povrchu?

### 3. Jak silně terén mění odrazivost lesa

Vezmeme lesní pixely podle WorldCoveru a proložíme přímku ρ = m · cos i + b. Kdyby svah osvětlovalo jen přímé Slunce a les odrážel stejně do všech směrů, byla by odrazivost úměrná cos i a posun b by byl nulový. Poměr C = b/m je základem C-korekce (Teillet a kol. 1982).

**Úkol 2.** Ve kterém pásmu a období je vztah s cos i nejsilnější? Proč má modrá pásmo velké C, tedy velký posun ve srovnání se sklonem, a SWIR skoro nulové? Spoj to s podílem difuzního světla oblohy v jednotlivých vlnových délkách.

### 4. Pět korekcí

Kosinová korekce ρ · cos θ_s / cos i předpokládá jen přímé světlo. C-korekce přidá C do čitatele i jmenovatele, Minnaertova korekce ρ · (cos θ_s / cos i)^k odhadne exponent k z dat a SCS+C (Soenen a kol. 2005) bere v úvahu, že stromy rostou svisle, ne kolmo ke svahu. Hodnotíme korelaci s cos i po korekci, rozptyl odrazivosti lesa a poměr mediánů na strmých jižních a severních svazích (u stejného lesa by měl být blízko 1).

Parametry, které student mění:

- `COSI_MIN = 0.15`: pixely s cos i pod touto hodnotou se neopravují (skoro ve stínu)

**Úkol 3.** Která metoda překorigovává (záporné r, poměr jižních a severních svahů pod 1) a proč nejvíc v modré a na podzim? Proč u C, Minnaertovy korekce a SCS+C vychází r skoro přesně nula a proč to samo o sobě nedokazuje, že korekce funguje? Navrhni poctivější ověření (např. odhad parametrů na jedné polovině výřezu a hodnocení na druhé).

### 5. Mapy a vegetační index

Načte knihovny a stáhne data.

Parametry, které student mění:

- `SHOW, BAND = "podzim", 5`: období a pásmo pro mapy

**Úkol 4.** Kde v opravené mapě zůstávají chyby (strmé severní svahy, místa pod `COSI_MIN`)? Nastav `COSI_MIN` na 0,05 a na 0,3 a popiš rozdíl. Proč kosinová korekce dělá ze stinných svahů nejjasnější místa scény?

**Úkol 5.** V létě NDVI s cos i skoro nekoreluje, na podzim ano. Proč poměrový index vliv terénu vyruší jen tehdy, když je efekt čistě násobný? Které dva rozdíly mezi červenou a NIR (podíl difuzního světla z kroku 3, zář dráhy) to při nízkém Slunci kazí?

**Rozšíření (nepovinné).** Přesuň výřez do Šumavy (dlaždici DEM a WorldCoveru je pak třeba změnit, scény Landsatu musí pokrývat nové místo) nebo použij místo lesa louky (`wc == 30`). Vyjdou parametry C a k podobně?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; veřejný archiv Google Cloud (`gcp-public-data-landsat`). Data USGS jsou bez omezení užití, s uvedením zdroje.
- Copernicus DEM GLO-30: produced using Copernicus WorldDEM-30 © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. Registr AWS Open Data (`copernicus-dem-30m`).
- Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Teillet, P. M., Guindon, B., Goodenough, D. G. (1982). On the slope-aspect correction of multispectral scanner data. *Canadian Journal of Remote Sensing* 8(2), 84–106.
- Minnaert, M. (1941). The reciprocity principle in lunar photometry. *Astrophysical Journal* 93, 403–410.
- Soenen, S. A., Peddle, D. R., Coburn, C. A. (2005). SCS+C: a modified sun-canopy-sensor topographic correction in forested terrain. *IEEE Transactions on Geoscience and Remote Sensing* 43, 2148–2159. https://doi.org/10.1109/TGRS.2005.852480

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
