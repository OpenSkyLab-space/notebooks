# Od pixelu ke třídě, pokročilá verze: časová řada, prostorová validace a odhad ploch

Popis notebooku k vizuálu [Od pixelu ke třídě](https://openskylab.space/edu_viz_image_classification.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/image_classification_pro_cs.ipynb) · verze 1.0 · asi 75 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku ke klasifikaci. Místo jednoho snímku pracuješ se třemi snímky Sentinel-2 z jara, léta a podzimu 2024 u Roztok, klasifikátor minimální vzdálenosti si napíšeš sám, přesnost ověříš prostorovou validací a plochy tříd odhadneš i s nejistotou, jak se to dělá v praxi. Část kódu doplňuješ sám.

## Cíl

Sestavit příznaky z časové řady, napsat a ověřit vlastní klasifikátor, porovnat náhodnou a prostorovou validaci, změřit přínos jednotlivých snímků a odhadnout plochy tříd s intervalem spolehlivosti podle dobré praxe (Olofsson a kol. 2014).

## Data

tři snímky Sentinel-2 L2A dlaždice 33UVR (27. 4., 21. 7. a 21. 9. 2024) z katalogu Earth Search na AWS, výřez 4 × 4 km kolem Roztok a Suchdola; reference ESA WorldCover 10 m 2021 v200. Stahuje se asi 60 MB.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a tři snímky

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

Parametry, které student mění:

- `DATES = ["S2A_33UVR_20240427_0_L2A", "S2B_33UVR_20240721_0_L2A", "S2A_33UVR_20240921_0_L2A"]`: snímky jednoho roku (jaro, léto, podzim)
- `LON, LAT, HALF = 14.37, 50.14, 2000`: střed výřezu a jeho poloviční šířka (m)

### 2. Příznaky z časové řady

Z každého snímku vezmeme odrazivost deseti pásem a tři indexy: NDVI (zeleň), NDWI (voda, McFeeters 1996) a NDMI (vlhkost listů). Se třemi snímky má každý pixel 39 příznaků. Indexy jsou ve slovníku `INDICES` jako funkce a můžeš přidat vlastní.

Parametry, které student mění:

- `INDICES = {`: indexy počítané z každého snímku; přidej vlastní

**Úkol 1.** Jak se mění medián NDVI louky a pole mezi dubnem, červencem a zářím a proč (osev, sklizeň, seč)? Proč je pro rozlišení pole a louky víc snímků lepší než jeden? Přidej do `INDICES` vlastní index, třeba NDRE = (nir − rededge1) / (nir + rededge1), spusť buňky znovu a v kroku 5 sleduj, jestli pomohl.

### 3. Vlastní klasifikátor minimální vzdálenosti

Klasifikátor minimální vzdálenosti přiřadí pixel třídě, jejíž střed (průměrný vektor příznaků) je nejblíž. Napíšeme ho v numpy na pár řádků a ověříme, že dává totéž co `NearestCentroid` ze scikit-learn. Trénujeme na severní polovině výřezu, testujeme na jižní. Větev pro Mahalanobisovu vzdálenost, která bere v úvahu rozptyl a korelace příznaků uvnitř třídy, doplníš sám.

Parametry, které student mění:

- `n_class = 600`: vzorek pixelů na třídu
- `metric = "euclid"`: "euclid", nebo po doplnění "mahalanobis"

**Úkol 2.** Doplň ve funkci `min_distance` větev `mahalanobis` (kovarianční matice každé třídy z trénovacích pixelů, `np.linalg.inv`, vzdálenost (x − μ)ᵀ Σ⁻¹ (x − μ)) a nastav `metric = "mahalanobis"`. Jak se výsledek srovná s eukleidovskou vzdáleností a s QDA? QDA je maximální věrohodnost: proč se od tvé Mahalanobisovy vzdálenosti přesto liší (člen s ln |Σ| a apriorní pravděpodobnosti)? Proč je u eukleidovské vzdálenosti nutná standardizace? Zkus ji vypnout (`Xs = X`).

### 4. Náhodná, nebo prostorová validace?

Sousední pixely si jsou podobné. Když vzorek rozdělíme na trénovací a testovací náhodně, testovací pixel má často souseda v tréninku a přesnost vyjde příliš dobře. Prostorová validace dělí vzorek po čtvercích: celý čtverec je buď v tréninku, nebo v testu (Roberts a kol. 2017). Porovnáme náhodné rozdělení, čtverce a rozdělení na sever a jih.

Parametry, které student mění:

- `BLOCK_M = 500`: velikost čtverců pro prostorovou validaci (m)

**Úkol 3.** Proč vychází náhodné rozdělení nejlépe a rozdělení sever × jih nejhůř? Nastav `BLOCK_M` na 200 a 1000 m: jak se mění průměr a rozptyl přesnosti a proč? Kterému číslu bys věřil, kdyby se mapa měla použít na sousedním území, a které bys uvedl ve zprávě?

### 5. Co přinese který snímek

Průběh v čase odliší třídy, které jsou v jednom okamžiku podobné. Spočítáme přesnost náhodného lesa (prostorová validace po čtvercích) pro každý snímek zvlášť, pro dvojice i pro všechny tři, a míru F1 každé třídy pro letní snímek a pro všechny tři.

**Úkol 4.** Který samotný snímek je nejlepší a která dvojice? O kolik pomohly všechny tři snímky a u které třídy nejvíc? Vysvětli to grafem NDVI z kroku 2. Kdy by další snímek už nepomohl a co by pak pomohlo víc (jiné příznaky, lepší reference, víc trénovacích pixelů)?

### 6. Mapa a odhad ploch s nejistotou

Plocha třídy spočítaná z mapy (počet pixelů krát plocha pixelu) je zatížená chybami klasifikace. Dobrá praxe (Olofsson a kol. 2014) je odhadnout plochu z náhodného vzorku kontrolních pixelů vybraného zvlášť v každé třídě mapy (stratifikovaný výběr) a uvést interval spolehlivosti. Mapu vytvoříme z poloviny čtverců a plochy odhadneme na zbytku území. Referencí je tu WorldCover, který máme pro všechny pixely, takže můžeme odhad porovnat se skutečným součtem.

Parametry, které student mění:

- `n_h = 100`: vzorek kontrolních pixelů v každé třídě mapy

**Úkol 5.** Které třídy mapa nadhodnocuje a které podhodnocuje? Je blíž součtu WorldCoveru plocha z mapy, nebo odhad ze vzorku, a leží součet v intervalu ±95 %? Nastav `n_h` na 30 a 300: jak se mění interval a proč? V praxi referenci pro všechny pixely nemáš: proč pak plocha z mapy nestačí? A proč ani WorldCover není „pravda“ (jeho celková přesnost je kolem 77 %, Zanaga a kol. 2022)?

**Rozšíření (nepovinné).** Vyzkoušej jiné místo: najdi v katalogu Earth Search tři bezoblačné snímky jednoho roku (jaro, léto, podzim), změň `DATES`, `LON` a `LAT` a podle zeměpisné polohy i dlaždici WorldCover v proměnné `WORLDCOVER` (dlaždice 3 × 3°, např. N48E015 pro Moravu). Vyjdou závěry kroků 4 až 6 stejně?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.
- Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015
- Roberts, D. R. a kol. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40, 913–929. https://doi.org/10.1111/ecog.02881
- Congalton, R. G., Green, K. (2019). *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices*, 3. vyd. CRC Press.
- Pedregosa, F. a kol. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
