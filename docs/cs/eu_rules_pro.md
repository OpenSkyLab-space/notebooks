# Kde smím létat, pokročilá verze: geometrie zón, mapa povolené výšky, letové hladiny a cyklus AIRAC

Popis notebooku k vizuálu [Kde a jak smím létat](https://openskylab.space/edu_viz_eu_rules.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/eu_rules_pro_cs.ipynb) · verze 1.0 · asi 60 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku o zeměpisných zónách UAS. Na aktuálních datech ŘLP ověříš, zda geometrie zón odpovídá jejich popisu, sestavíš mapu povolené výšky letu kolem Brna z gridových sítí, spočítáš ze zpráv METAR, jak vysoko ve skutečnosti leží letové hladiny, zkontroluješ data platnosti zón proti cyklu AIRAC a nakreslíš svislý řez zónami z Bystrce na letiště Tuřany nad skutečným terénem. Je to výuková pomůcka, ne právní posouzení: před letem vždy ověř zóny v aplikaci DroneMap a podmínky v opatřeních obecné povahy ÚCL.

## Cíl

Změřit poloměry kruhových zón a porovnat je s popisem, spojit gridové sítě GRID_CTR a GRID_ATZ do mapy povolené výšky, převést letové hladiny na skutečnou nadmořskou výšku podle QNH a teploty, ověřit data platnosti proti cyklu AIRAC a sestavit svislý řez zónami nad terénem DMR 5G.

## Data

Zeměpisné zóny UAS ve formátu GeoJSON (referenční hranice) ze stránky ŘLP https://aim.rlp.cz/?lang=cz&p=uas-gz, stažené v okamžiku spuštění, kromě vrstev větších než zvolený limit; zprávy METAR letiště Brno-Tuřany (LKTB) za posledních 7 dní z Aviation Weather Center (NOAA); nadmořská výška terénu z Digitálního modelu reliéfu ČR 5. generace (DMR 5G, ČÚZK). Převod letové hladiny na skutečnou výšku používá standardní atmosféru ICAO s teplotou upravenou podle letiště, je to přiblížení.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a zóny

Načteme seznam aktuálních zón ze stránky ŘLP a stáhneme všechny vrstvy do zvoleného limitu velikosti a obě gridové sítě. Stahování trvá asi minutu.

Parametry, které student mění:

- `MAX_MB = 20`: největší stahovaný soubor (MB); obě gridové sítě se stáhnou vždy

### 2. Odpovídá geometrie zón popisu?

U zón, které popis definuje vzdáleností od bodu (vztažný bod letiště ARP, heliportu HRP), změříme poloměr v datech: poloměr kruhu se stejnou plochou jako vnější hranice prvku. Výpočet běží v metrech v souřadnicích UTM 33N.

Parametry, které student mění:

- `CHECK = {"LKR315A": [5500], "LKR315B": [1550], "LKR314D": [5500], "LKR315C": [3000, 1000, 200], "LKR315D": [3000, 1000, 200]}`: vrstva → poloměry podle popisu na stránce ŘLP (m)

**Úkol 1.** Které vrstvy odpovídají popisu a které ne? U LKR315A najdi prvky výrazně menší a větší než 5500 m a vysvětli, čím to může být (podívej se, kde leží). U LKR315B, LKR315C a LKR315D spočítej, o kolik procent se poloměr v datech liší od popisu na stránce ŘLP. Najdi v opatření obecné povahy ÚCL k zónám LKR315, jaké vzdálenosti platí, a rozhodni, čím se má pilot řídit: popisem, nebo hranicí zóny v DroneMap.

### 3. Mapa povolené výšky kolem Brna

Gridové sítě GRID_CTR (kolem řízených letišť, buňky 30″) a GRID_ATZ (prostory neřízeného letového provozu, buňky 15″) udávají v každé buňce, do jaké výšky nad terénem je let povolen bez dalšího souhlasu. Území vzorkujeme po 7,5″, takže každý bod leží uvnitř jedné buňky. Vedle toho spočítáme, kolik zón od země (GND) se v bodě překrývá.

Parametry, které student mění:

- `BBOX = (16.45, 49.10, 16.80, 49.30)`: území (zem. délka a šířka: západ, jih, východ, sever)

**Úkol 2.** Jaký podíl území smíš podle sítí přeletět ve 120 m, jaký jen do 30 m a kde nesmíš vůbec? Kde je povolená výška 0 m a proč právě tam (porovnej s polohou letiště Tuřany, letiště Medlánky a heliportů v pravé mapě)? Znamená šedé území mimo síť, že tam smíš letět bez omezení? Vzpomeň na velké vrstvy, které jsme nestáhli.

### 4. Jak vysoko je letová hladina?

Letová hladina FL je tlaková výška ve stovkách stop při standardním tlaku 1013,25 hPa. Skutečná nadmořská výška hladiny závisí na tlaku u země (QNH) a na teplotě vzduchu: v teplém vzduchu leží výš, ve studeném níž. Vezmeme QNH a teplotu ze zpráv METAR za posledních 7 dní a spočítáme skutečnou výšku hladin, které jsou dolní hranicí prostorů LKR320A.

Parametry, které student mění:

- `STATION = "LKTB"`: letiště, ze kterého vezmeme QNH a teplotu (zprávy METAR)
- `FLS = [65, 95]`: letové hladiny (např. dolní hranice prostorů LKR320A)

**Úkol 3.** O kolik metrů se během týdne měnila skutečná výška FL65 a FL95? Co ji ovlivňuje víc, QNH, nebo teplota? Spočítej, kolik metrů výšky odpovídá změně QNH o 1 hPa. Jak vysoko nad Děvínem (asi 550 m n. m.) začíná prostor LKTB4 (FL65) v nejnižším a nejvyšším případě? Proč se v letectví vyšší hranice udávají letovými hladinami, i když jejich skutečná výška kolísá?

### 5. Kdy zóny platí: cyklus AIRAC

Změny leteckých informací se zveřejňují k pevným datům cyklu AIRAC, která jdou po 28 dnech, a ŘLP aktualizuje data zón v návaznosti na tento cyklus. Každý prvek zóny má datum platnosti (effective_date). Zjistíme, která data platnosti jsou data AIRAC.

**Úkol 4.** Která data platnosti odpovídají cyklu AIRAC a která ne? Které vrstvy se měnily nejčastěji a proč právě ty? Zóna OOPUAS-0055 má datum mimo cyklus: najdi na stránce ŘLP nebo v DroneMap, o jakou zónu jde, a vysvětli, proč může vzniknout mimo cyklus. Kdy je příští datum AIRAC a co uděláš před letem po tomto datu?

### 6. Svislý řez zónami

Na přímce z Bystrce na letiště Brno-Tuřany navzorkujeme terén z DMR 5G po 25 m a pro každou zónu, kterou přímka protíná, převedeme dolní a horní hranici na nadmořskou výšku (AGL nad terénem, FL jako ve standardní atmosféře). Černá čára je terén plus povolená výška z gridových sítí.

Parametry, které student mění:

- `A = (49.2467, 16.4798)`: začátek profilu (Bystrc, Kozí horka)
- `B = (49.1510, 16.6940)`: konec profilu (letiště Brno-Tuřany)
- `FLIGHT_AGL = 120`: plánovaná výška letu nad terénem (m)

**Úkol 5.** Na kolika procentech délky profilu smíš podle sítí letět ve 120 m nad terénem a kde povolená výška klesá k nule? Které zóny profil protíná od země a které začínají vysoko nad dronem? Nastav FLIGHT_AGL na 50 m: jak se výsledek změní? Proč pro let dronu nestačí znát jen zóny, do kterých padá místo startu?

**Rozšíření (nepovinné).** Nastav BBOX, A, B a STATION na okolí letiště Václava Havla (STATION = "LKPR", konec profilu 50,10° s. š., 14,26° v. d.) a porovnej mapu povolené výšky a svislý řez s Brnem.

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Zeměpisné zóny UAS: Řízení letového provozu České republiky, s. p., AIM, https://aim.rlp.cz/?lang=cz&p=uas-gz; mapa zón: https://dronemap.gov.cz
- Prováděcí nařízení Komise (EU) 2019/947 o pravidlech a postupech pro provoz bezpilotních letadel, čl. 15 (zeměpisné zóny UAS).
- Úřad pro civilní letectví: opatření obecné povahy k zeměpisným zónám UAS (LKR311 až LKR320), https://www.caa.gov.cz
- Zprávy METAR: NOAA Aviation Weather Center, Data API, https://aviationweather.gov/data/api/
- Výška terénu: Digitální model reliéfu ČR 5. generace (DMR 5G), © ČÚZK, licence CC BY 4.0, služba https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer
- ICAO (1993). *Manual of the ICAO Standard Atmosphere*, Doc 7488, 3. vyd. (tlaková výška).
- ICAO, Annex 15 k Úmluvě o mezinárodním civilním letectví, *Aeronautical Information Services* (systém AIRAC, 28denní cyklus).

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
