# Kde smím létat: zeměpisné zóny UAS z dat ŘLP

Popis notebooku k vizuálu [Kde a jak smím létat](https://openskylab.space/edu_viz_eu_rules.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/eu_rules_hluboka_cs.ipynb) · verze 1.0 · asi 45 min · pět úkolů

## O čem notebook je

Vizuál vede rozhodovacím stromem evropských pravidel pro drony. Jednu jeho větev, zeměpisné zóny UAS, tady projdeš na skutečných datech: stáhneš aktuální zóny, které zveřejňuje Řízení letového provozu ČR, zjistíš, do kterých zón padají plánovaná místa letu, jak vysoko se v okolí letišť smí létat a jak se zóny mění v čase. Je to výuková pomůcka, ne právní posouzení: před letem vždy ověř zóny v aplikaci DroneMap a podmínky v opatřeních obecné povahy ÚCL.

## Cíl

Načíst seznam zeměpisných zón a jejich soubory GeoJSON, určit zóny pro zadaná místa i pro celé území mapovacího letu, převést svislé hranice zón (AGL, AMSL, FL) na metry nad terénem, přečíst výškové omezení z gridové sítě kolem letišť a porovnat aktuální a budoucí vydání zón.

## Data

Zeměpisné zóny UAS ve formátu GeoJSON (referenční hranice) ze stránky ŘLP https://aim.rlp.cz/?lang=cz&p=uas-gz, stažené v okamžiku spuštění; nadmořská výška terénu z Digitálního modelu reliéfu ČR 5. generace (DMR 5G, ČÚZK).

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a seznam zón

Nainstaluje knihovny, které Colab nemá předem (`pyproj`, `rasterio`, `shapely`), a stáhne data.

### 2. Do kterých zón padají místa letu?

Stáhneme zóny do zvolené velikosti souboru (největší vrstvy, např. hustě osídlený prostor nebo silnice III. třídy, mají stovky MB a v Colabu by se stahovaly dlouho). Pro každé místo zjistíme, ve kterých zónách leží a jaká je svislá hranice zóny.

Parametry, které student mění:

- `MAX_MB = 20`: největší stahovaný soubor (MB)
- `SITES = {`: místa letu (zeměpisná šířka, délka)

**Úkol 1.** Ve kterých zónách leží jednotlivá místa? Které místo je bez omezení ze stažených vrstev a proč to ještě neznamená, že tam smíš létat (které velké vrstvy jsi nestáhl a co by mohly změnit)? Přidej do SITES místo, kde chceš sám létat, a výsledek porovnej s mapou DroneMap.

### 3. Svislé hranice zón

Zóna platí jen mezi svou dolní a horní hranicí. Hranice se udávají nad terénem (AGL), nad střední hladinou moře (AMSL) nebo jako letová hladina (FL, stovky stop při standardním tlaku 1013,25 hPa; zde ji pro jednoduchost bereme jako výšku AMSL). 1 ft = 0,3048 m. Nadmořskou výšku terénu vezmeme z digitálního modelu reliéfu DMR 5G (ČÚZK).

Parametry, které student mění:

- `FLIGHT_AGL = 120`: plánovaná výška letu nad terénem (m)

**Úkol 2.** Omezený prostor kolem letiště České Budějovice (zóna 3LKR314A) má horní hranici 3500 ft AMSL: kolik je to metrů nad terénem u Jihočeské univerzity? Proč se některé letecké prostory LKR320A dronu ve 120 m vůbec netýkají? Proč u hranic v AMSL nebo FL záleží na výšce terénu? Co by stejná hranice 3500 ft AMSL znamenala, kdyby zóna sahala až na Kleť (1084 m n. m.)?

### 4. Gridová síť kolem letišť

V okolí letišť ŘLP zveřejňuje síť buněk, kde každá buňka udává, do jaké výšky nad terénem je let povolen bez dalšího souhlasu. Kolem řízených letišť (CTR) je to soubor GRID_CTR s buňkami 30″ × 30″, v prostorech neřízeného letového provozu soubor GRID_ATZ s buňkami 15″ × 15″ (asi 300 × 450 m). V okolí Českých Budějovic a Hluboké platí GRID_ATZ. Podmínky použití sítě jsou v příslušném OOP.

Parametry, které student mění:

- `CENTER = (49.00, 14.45)`: střed mapy (šířka, délka)
- `SPAN = 0.10`: poloviční rozsah mapy (°)

**Úkol 3.** Do jaké výšky smíš podle sítě létat u Jihočeské univerzity, u zámku v Hluboké a v údolí u Hosína? Proč je u Hosína povolená výška 0 m nad terénem (podívej se, do které zóny LKR315A místo patří)? Jak se povolená výška mění směrem k letišti České Budějovice? Proč je síť výhodnější než jedna velká zóna s jedinou výškou?

### 5. Celé území mapovacího letu

Mapovací let nepokrývá bod, ale plochu. Spočítáme, jaký podíl čtverce kolem místa leží v jednotlivých zónách (v metrech, v souřadnicích UTM 33N).

Parametry, které student mění:

- `SITE = "Hluboká nad Vltavou, zámek"`: místo ze SITES
- `HALF_M = 1500`: polovina strany čtverce letu (m)

**Úkol 4.** Které zóny zasahují do čtverce letu, i když samotný střed v nich neleží? Jak se výsledek změní pro čtverec 0,5 km a 3 km? Jak bys mapovací let rozdělil, aby co nejvíc plochy leželo mimo omezení, a co bys musel vyřídit pro zbytek?

### 6. Zóny se mění

ŘLP zveřejňuje kromě aktuálních zón i vydání, která začnou platit v budoucnu (podle cyklu AIRAC). Porovnáme vrstvy, které mají obě vydání: počet zón, jejich identifikátory a plochu, která přibude nebo ubude.

**Úkol 5.** Které vrstvy se v příštím vydání mění, kolik zón a plochy přibude nebo ubude? Proč musí mít dron aktuální data pro funkci geografického povědomí (geo-awareness) a proč nestačí zóny zkontrolovat jednou při plánování projektu, který trvá několik týdnů?

**Rozšíření (nepovinné).** Spolužáci mohou mít notebook pro okolí Prahy nebo Brna. Porovnejte, jaké zóny a jaké povolené výšky ze sítě mají místa letu kolem letiště a mimo města, a čím se liší síť kolem řízeného a neřízeného letiště.

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Zeměpisné zóny UAS: Řízení letového provozu České republiky, s. p., AIM, https://aim.rlp.cz/?lang=cz&p=uas-gz; mapa zón: https://dronemap.gov.cz
- Prováděcí nařízení Komise (EU) 2019/947 o pravidlech a postupech pro provoz bezpilotních letadel, čl. 15 (zeměpisné zóny UAS); nařízení v přenesené pravomoci (EU) 2019/945.
- Úřad pro civilní letectví: opatření obecné povahy k zeměpisným zónám UAS (LKR311 až LKR320), https://www.caa.gov.cz
- Výška terénu: Digitální model reliéfu ČR 5. generace (DMR 5G), © ČÚZK, licence CC BY 4.0, služba https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
