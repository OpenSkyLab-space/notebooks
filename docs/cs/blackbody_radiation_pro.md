# Záření černého tělesa, pokročilá verze: teplota povrchu, tepelný ostrov a sucho z Landsatu 8

Popis notebooku k vizuálu [Záření černého tělesa](https://openskylab.space/edu_viz_blackbody_radiation.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/blackbody_radiation_pro_cs.ipynb) · verze 1.0 · asi 65 min · čtyři úkolů

## O čem notebook je

Pokročilá verze notebooku k Planckovu zákonu. Teplotu povrchu tu z termálního pásma Landsatu 8 počítáš rovnicí přenosu záření, tedy s emisivitou i atmosférou, a zjistíš, která z oprav je důležitější. Výsledek použiješ na tepelný ostrov Prahy ve dvou dnech a na index sucha TVDI z prostoru teplota–NDVI.

## Cíl

Spočítat teplotu povrchu z rovnice přenosu záření a odhadnout vliv emisivity a atmosféry, změřit povrchový tepelný ostrov podle třídy pokryvu a sestavit z prostoru teplota–NDVI suchou a mokrou hranu a index TVDI.

## Data

Landsat 8 OLI/TIRS Collection 1 Level-1 z veřejného archivu Google Cloud: `LC08_L1TP_191025_20190626_20190705_01_T1` (26. 6. 2019, vlna veder) a `LC08_L1TP_191025_20170519_20170525_01_T1` (19. 5. 2017), pásma B4, B5, B10, BQA a MTL; třídy ESA WorldCover 2021 v200. Výřez 30 × 30 km kolem Prahy, asi 25 MB. Parametry atmosféry (propustnost, zář nahoru a dolů) se nestahují: jsou zadané jako orientační hodnoty a dají se změnit, skutečné hodnoty pro konkrétní den a místo dává například kalkulačka NASA (Barsi a kol. 2005).

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a dvě scény

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

Parametry, které student mění:

- `SCENES = {"2019-06-26": "LC08_L1TP_191025_20190626_20190705_01_T1", "2017-05-19": "LC08_L1TP_191025_20170519_20170525_01_T1"}`: dvě scény (vlna veder, jaro)
- `LON, LAT, HALF = 14.45, 50.08, 15000`: střed výřezu a jeho poloviční šířka (m)

### 2. Teplota povrchu z rovnice přenosu záření

Senzor nad atmosférou měří L = τ · [ε · B(Ts) + (1 − ε) · L↓] + L↑: záření povrchu zeslabené atmosférou, k tomu odraz záření oblohy a záření samotné atmosféry. Rovnici vyřešíme pro Ts. Emisivitu odhadneme z NDVI jako v základní verzi, parametry atmosféry τ, L↑ a L↓ jsou orientační hodnoty pro vlhké letní ovzduší.

Parametry, které student mění:

- `TAU, L_UP, L_DOWN = 0.80, 1.6, 2.7`: propustnost a zář atmosféry nahoru a dolů (W·m⁻²·sr⁻¹·µm⁻¹), orientační léto

**Úkol 1.** O kolik stupňů posune teplotu oprava o emisivitu a o kolik oprava o atmosféru? Jak moc se medián teploty změní, když τ změníš o 0,05? Co z toho plyne pro přesnost teploty povrchu, když parametry atmosféry pro daný den neznáš?

### 3. Povrchový tepelný ostrov

Porovnáme teplotu povrchu zástavby s okolní zemědělskou krajinou a lesem ve dvou dnech. Pro oba dny tu používáme stejné parametry atmosféry, což je zjednodušení: v květnu 2017 bylo ovzduší jiné než ve vlně veder 2019.

**Úkol 2.** Ve kterém dni je rozdíl mezi zástavbou a poli větší a proč, když vlna veder byla v červnu 2019? Proč se rozdíl zástavby a lesa mezi dny mění méně? Jak by se tepelný ostrov změnil v noci (vzpomeň na tepelnou setrvačnost)?

### 4. Prostor teplota–NDVI a index sucha TVDI

V grafu teploty povrchu proti NDVI tvoří pixely trojúhelník nebo lichoběžník. Horní, suchá hrana spojuje nejteplejší pixely pro každé NDVI (povrchy bez vody k výparu), dolní, mokrá hrana nejchladnější. TVDI = (Ts − Ts_mokrá) / (Ts_suchá(NDVI) − Ts_mokrá) leží mezi 0 (vlhko) a 1 (sucho) (Sandholt a kol. 2002). Počítáme ho pro louky a pole.

Parametry, které student mění:

- `NBINS = 20`: počet tříd NDVI pro hledání suché hrany

**Úkol 3.** Proč má suchá hrana záporný sklon, tj. proč jsou suché pixely s vyšším NDVI chladnější? Ve kterém dni vychází pole sušší a odpovídá to tomu, co víš o jaru 2017 a vlně veder 2019? Proč nelze TVDI dvou dnů srovnávat přímo, když se hrany počítají pro každý snímek zvlášť?

**Úkol 4.** Louky vycházejí v TVDI sušší než pole. Podívej se v mapě, kde louky podle WorldCoveru leží (městské trávníky, suché svahy, okraje zástavby). Které předpoklady metody (stejné počasí v celém výřezu, jen rozdíly ve vlhkosti, ne v drsnosti a nadmořské výšce) tu mohou neplatit? Změň `NBINS` a sleduj, jak citlivá je suchá hrana.

**Rozšíření (nepovinné).** Najdi v kalkulačce NASA (atmcorr.gsfc.nasa.gov) parametry atmosféry pro Prahu a oba dny, vlož je místo orientačních hodnot (pro každý den zvlášť) a porovnej teploty a tepelný ostrov.

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Landsat 8 OLI/TIRS Collection 1 Level-1, U.S. Geological Survey; veřejný archiv Google Cloud (`gcp-public-data-landsat`). Data USGS jsou bez omezení užití, s uvedením zdroje.
- Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- USGS (2019). *Landsat 8 (L8) Data Users Handbook*, verze 5.0, kap. 5.
- Sobrino, J. A., Jiménez-Muñoz, J. C., Paolini, L. (2004). Land surface temperature retrieval from LANDSAT TM 5. *Remote Sensing of Environment* 90, 434–440. https://doi.org/10.1016/j.rse.2004.02.003
- Barsi, J. A., Schott, J. R., Palluconi, F. D., Hook, S. J. (2005). Validation of a web-based atmospheric correction tool for single thermal band instruments. *Proc. SPIE* 5882, 58820E. https://doi.org/10.1117/12.619990
- Sandholt, I., Rasmussen, K., Andersen, J. (2002). A simple interpretation of the surface temperature/vegetation index space for assessment of surface moisture status. *Remote Sensing of Environment* 79, 213–224. https://doi.org/10.1016/S0034-4257(01)00274-7

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
