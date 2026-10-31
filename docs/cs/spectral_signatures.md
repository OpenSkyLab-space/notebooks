# Spektrální signatury ze Sentinelu-2: les, pole, voda a sníh (Roztoky a Krkonoše)

Popis notebooku k vizuálu [Spektrální signatury](https://openskylab.space/edu_viz_spectral_signatures.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/spectral_signatures_cs.ipynb) · verze 1.0 · asi 45 min · šest úkolů

## O čem notebook je

Vizuál ukazuje, jak chlorofyl, voda v listech, sušina a LAI mění spektrální křivku vegetace a proč NDVI v hustém porostu přestává růst. Tady to ověříš na skutečných pixelech Sentinelu-2 u Roztok a na časové řadě jednoho pole během sezóny 2024.

## Cíl

Porovnat skutečné spektrální křivky povrchů, najít polohu červené hrany, ukázat nasycení NDVI na časové řadě pole a vysvětlit, proč stejný index z jiných pásem dává jiné číslo.

## Data

Sentinel-2 L2A z katalogu Earth Search na AWS: scéna `S2B_33UVR_20240721_0_L2A` (21. 7. 2024, okolí Roztok), bezoblačné scény dlaždice 33UVR z března až října 2024 pro časovou řadu a `S2A_33UWS_20240308_0_L2A` (Krkonoše se sněhem); třídy ESA WorldCover 2021. Stahuje se asi 30 MB, časová řada trvá 1 až 3 minuty.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

### 2. Spektrální křivky skutečných povrchů

Načte knihovny a stáhne data.

**Úkol 1.** Popiš křivku lesa: proč je v modré a červené nízko, v zelené malé maximum a mezi 0,70 a 0,78 µm prudký nárůst? Proč má pole (koncem července často zralé obilí nebo strniště) v červené víc a v NIR méně než les? Který povrch má v kterých pásmech největší rozptyl (šíři pásu kolem křivky) a proč?

### 3. Poloha červené hrany

Červená hrana je strmý nárůst odrazivosti mezi červenou a NIR. Její polohu (REP) odhadneme lineární interpolací z pásem B4, B5, B6 a B7 (Guyot a Baret 1988). Víc chlorofylu posouvá hranu k delším vlnovým délkám.

**Úkol 2.** Který vegetační povrch má červenou hranu nejdál a proč? Má smysl počítat REP u vody nebo zástavby? Podívej se, jaké hodnoty vyjdou, a vysvětli, proč index bez vegetace nedává fyzikální smysl, i když vrátí číslo.

### 4. Nasycení NDVI během sezóny

Vezmeme jeden pixel pole u Únětic a všechny bezoblačné snímky z roku 2024. Porovnáme NDVI = (NIR − R)/(NIR + R), NDRE = (NIR − RE1)/(NIR + RE1) a NDMI = (NIR − SWIR1)/(NIR + SWIR1).

Parametry, které student mění:

- `lon, lat = 14.3516, 50.1632`: bod (pole u Únětic); zkus i les, např. 14.366, 50.148

**Úkol 3.** Kdy pole dosáhlo maxima a kdy byla sklizeň? V jakém rozsahu NDVI se graf NDVI–NDRE ohýbá, tj. NDVI už skoro neroste, ale NDRE ano? Vysvětli nasycení: proč červená při vysokém LAI už nemůže klesnout níž, ale červená hrana se ještě posouvá?

**Úkol 4.** Jak se během sezóny chová NDMI a proč klesá dřív nebo rychleji než NDVI, když porost dozrává? Změň bod na les (`14.366, 50.148`) a porovnej: proč je u lesa řada mnohem plošší?

### 5. Voda a sníh

NDWI (zelená a NIR, McFeeters 1996) zvýrazní vodu, NDSI (zelená a SWIR 1,6 µm) sníh. Sníh je ve viditelném jasný, ale v SWIR pohlcuje; oblaka odrážejí v obou.

Parametry, které student mění:

- `thr = 0.4`: práh NDSI pro sníh (MODIS používá 0,4)

**Úkol 5.** Proč NDSI odliší sníh od oblaků, i když jsou ve viditelném oba bílé? Změň práh na 0,2 a 0,6: kde se maska mění nejvíc (zasněžený les, stíny, otevřené plochy)? Proč je voda (Vltava) v NDWI kladná a vegetace záporná?

### 6. Stejný index, jiné číslo

NDVI lze ze Sentinelu-2 spočítat s širokým pásmem B8 (střed kolem 833 nm, šířka přes 100 nm, pixel 10 m) nebo s úzkým B8A (865 nm, šířka asi 21 nm, pixel 20 m). Dron s multispektrální kamerou nebo Landsat mají zase jiná pásma. Porovnáme obě varianty na stejných pixelech.

**Úkol 6.** O kolik se obě NDVI liší a kterým směrem? Navrhni dvě příčiny (poloha a šířka pásma, rozlišení 10 vs. 20 m). Co z toho plyne, když chceš porovnat NDVI z dronu s NDVI ze Sentinelu-2 nebo staré a nové mapy NDVI?

**Rozšíření (nepovinné).** Porovnej výsledky se spolužákem, který spustil notebook pro jiné místo: liší se červená hrana lesa, nasycení NDVI na poli nebo rozdíl NDVI(B8A) − NDVI(B8)? Čím to může být (plodina, druh lesa, datum snímku)?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); COG kopie v registru AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje podle [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).
- Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Poloha červené hrany lineární interpolací: Guyot, G., Baret, F. (1988). Utilisation de la haute résolution spectrale pour suivre l'état des couverts végétaux. *Proc. 4th Int. Colloquium on Spectral Signatures of Objects in Remote Sensing*, ESA SP-287, 279–286.
- Nasycení NDVI a indexy s červenou hranou: Gitelson, A. A., Merzlyak, M. N. (1994). Spectral reflectance changes associated with autumn senescence of *Aesculus hippocastanum* L. and *Acer platanoides* L. leaves. *Journal of Plant Physiology* 143, 286–292. https://doi.org/10.1016/S0176-1617(11)81633-0
- NDWI: McFeeters, S. K. (1996). The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features. *International Journal of Remote Sensing* 17, 1425–1432. https://doi.org/10.1080/01431169608948714
- NDSI pro sníh: Hall, D. K., Riggs, G. A., Salomonson, V. V. (1995). Development of methods for mapping global snow cover using MODIS. *Remote Sensing of Environment* 54, 127–140. https://doi.org/10.1016/0034-4257(95)00137-P

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
