# Od pixelu ke třídě: klasifikace Sentinelu-2 u Brněnské přehrady

Popis notebooku k vizuálu [Od pixelu ke třídě](https://openskylab.space/edu_viz_image_classification.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/image_classification_brno_cs.ipynb) · verze 1.0 · asi 50 min · šest úkolů

## O čem notebook je

Ve vizuálu jsi dělil pixely prahem indexu, porovnával klasické klasifikátory a sledoval, jak se neuronová síť přeučí. Tady totéž uděláš na skutečném snímku Sentinel-2 u Brněnské přehrady s referencí ESA WorldCover a přesnost vyhodnotíš chybovou maticí.

## Cíl

Najít práh NDVI a SAVI pro vegetaci, porovnat minimální vzdálenost, maximální věrohodnost, k-NN, náhodný les a neuronovou síť na trénovacích a testovacích pixelech a spočítat přesnost zpracovatele, uživatele a kappa.

## Data

Sentinel-2 L2A `S2B_33UXQ_20240814_0_L2A` (14. 8. 2024) z katalogu Earth Search na AWS, výřez 4 × 4 km kolem Brněnské přehrady a Bystrce; reference ESA WorldCover 10 m 2021 v200. Stahuje se asi 20 MB.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a data

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

### 2. Práh NDVI: dvě chyby proti sobě

Vegetace = les, louka a pole podle WorldCover, ostatní = zástavba a voda. Pro každý práh spočítáme, kolik vegetace přehlédneme a kolik ne-vegetace označíme jako vegetaci.

Parametry, které student mění:

- `L = 0.5`: korekční faktor půdy pro SAVI (0 = NDVI, 0,5 obvykle, 1 řídký porost)

**Úkol 1.** Jaký práh NDVI je nejlepší a jaké chyby při něm zůstávají? Proč se nedá zbavit obou chyb současně? Které pixely „vegetace“ mají NDVI nízké (podívej se na pole: po žních je strniště, na jaře může být půda ještě holá) a proč je podle WorldCover počítáme jako vegetaci?

**Úkol 2.** Porovnej NDVI a SAVI. Nastav `L = 0`, `0.25` a `1`. Jak se mění rozsah hodnot a nejlepší práh? Proč SAVI méně závisí na jasu půdy a proč v hustém porostu na tom skoro nezáleží?

### 3. Trénovací a testovací pixely

Sousední pixely jsou si podobné, takže náhodné rozdělení by přesnost nadsadilo. Trénujeme proto na severní polovině výřezu a testujeme na jižní.

Parametry, které student mění:

- `n_train = 300`: počet trénovacích pixelů na třídu

### 4. Minimální vzdálenost a maximální věrohodnost

Načte knihovny a stáhne data.

**Úkol 3.** Čti chybovou matici maximální věrohodnosti: řádky jsou reference, sloupce výsledek. Která třída má nízkou přesnost zpracovatele (PA, je přehlížená) a která nízkou přesnost uživatele (UA, jiné třídy se do ní propadají)? Které dvojice tříd se nejvíc pletou a proč? Která z obou metod vyšla lépe? Maximální věrohodnost počítá s rozptylem a korelací pásem v každé třídě; proč přesto nemusí vyhrát (třídy nejsou normálně rozdělené, louka a les mají podobné spektrum, reference má chyby)?

### 5. Jak složitý model? k-NN a náhodný les

Načte knihovny a stáhne data.

**Úkol 4.** Při k = 1 je přesnost na trénovacích pixelech 100 % nebo skoro 100 %. Proč to nic neznamená? Které k a jaká hloubka stromů dávají nejlepší testovací přesnost? Popiš, jak vypadá přeučení a nedoučení v obou grafech.

### 6. Neuronová síť a přeučení

Malá síť s jednou skrytou vrstvou. Učíme ji na málo pixelech a sledujeme přesnost na tréninku a testu po epochách.

Parametry, které student mění:

- `hidden = 64`: počet skrytých neuronů
- `n_small = 30`: trénovacích pixelů na třídu (malý vzorek se snáz přeučí)

**Úkol 5.** Vyzkoušej `hidden` 4, 64 a 256 a `n_small` 30 a 300. Kdy se síť přeučí (trénink roste, test klesá nebo stagnuje)? Co by pomohlo: víc dat, menší síť, nebo zastavit učení dřív? Proč je rozdíl trénink–test u sítě větší než u maximální věrohodnosti?

### 7. Mapa výsledku

Načte knihovny a stáhne data.

**Úkol 6.** Najdi místa, kde se mapa liší od WorldCover. Je chyba vždy v klasifikaci? Uvažuj o tom, že WorldCover je z roku 2021 a sám má chyby, že jeden snímek z jednoho dne nerozliší louku od pole s pícninou ani zelené obilí na jaře od trávy a že pixel 10 m na okraji lesa je směs. Jak bys přesnost hodnotil poctivě?

**Rozšíření (nepovinné).** Porovnej své výsledky se spolužákem, který má notebook pro jiné místo (Roztoky, Brno, Hluboká nad Vltavou). Které třídy se jinde pletou víc a proč (roční doba snímku, druh krajiny, velikost polí)?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.
- Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Huete, A. R. (1988). A soil-adjusted vegetation index (SAVI). *Remote Sensing of Environment* 25, 295–309. https://doi.org/10.1016/0034-4257(88)90106-X
- Congalton, R. G., Green, K. (2019). *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices*, 3. vyd. CRC Press.
- Pedregosa, F. a kol. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
