# Spektrální signatury, pokročilá verze: model PROSAIL, nasycení indexů a odhad LAI

Popis notebooku k vizuálu [Spektrální signatury](https://openskylab.space/edu_viz_spectral_signatures.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/spectral_signatures_pro_cs.ipynb) · verze 1.0 · asi 75 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku ke spektrálním signaturám. Křivky z vizuálu tu počítá skutečný model přenosu záření PROSAIL, který spojuje optiku listu (PROSPECT) s porostem (SAIL). Ukážeš v něm, proč se NDVI nasycuje, sestavíš tabulku simulací a z ní odhadneš LAI pro každý pixel dvou snímků Sentinel-2 u Roztok, včetně nejistoty a míst, kde model selhává.

## Cíl

Zjistit, která pásma nesou informaci o chlorofylu, vodě, sušině a LAI, porovnat nasycení NDVI, NDRE a CIre v modelu, pochopit, proč je inverze modelu nejednoznačná, a odhadnout LAI z inverze tabulkou simulací se znalostí jejích mezí.

## Data

Dva snímky Sentinel-2 L2A dlaždice 33UVR (14. 5. a 21. 7. 2024) z katalogu Earth Search na AWS, výřez 4 × 4 km kolem Roztok a Únětic; třídy ESA WorldCover 2021 v200. Simulace počítá balíček `prosail` (PROSPECT-5 a 4SAIL) přímo v notebooku. Stahuje se asi 40 MB, tabulka simulací trvá 1 až 3 minuty. Pozemní měření LAI k výřezu nejsou k dispozici, takže výsledky inverze jsou odhady modelu, ne ověřené hodnoty.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava, dva snímky a model

Nainstaluje knihovny, které Colab nemá předem (`prosail`, `rasterio`), a stáhne data.

Parametry, které student mění:

- `DATES = ["S2A_33UVR_20240514_0_L2A", "S2B_33UVR_20240721_0_L2A"]`: dva snímky jedné sezóny (jaro, léto)
- `LON, LAT, HALF = 14.375, 50.155, 2000`: střed výřezu a jeho poloviční šířka (m)

### 2. Co model umí

PROSAIL počítá odrazivost porostu z vlastností listů (chlorofyl `cab`, voda `cw`, sušina `cm`, struktura `n`) a porostu (index listové plochy `lai`, průměrný úhel listů `ala`, půda pod porostem). Spektrum v krocích 1 nm převedeme na pásma Sentinelu-2. Spektrální citlivost pásem tu nahrazujeme Gaussovou křivkou, což je přiblížení; přesné křivky zveřejňuje ESA.

Parametry, které student mění:

- `VAR, VALUES = "cab", [10, 30, 50, 70]`: proměnná (cab, cw, cm, lai, ala) a její hodnoty

**Úkol 1.** Spusť buňku pro `cab`, `cw`, `cm`, `lai` a `ala`. Podle grafů a tabulky citlivosti řekni, která pásma Sentinelu-2 nesou informaci o chlorofylu, o vodě v listech a o LAI. Které dvě proměnné mění red edge a NIR skoro stejně, jen s opačným znaménkem, a co to znamená pro odhad LAI z jednoho snímku?

### 3. Nasycení indexů v modelu

Necháme LAI růst od 0 do 7 pro tři obsahy chlorofylu a sledujeme NDVI, NDRE a CIre = NIR/RE1 − 1 (Gitelson a kol. 2005). Tabulka ukazuje, při jakém LAI index dosáhne 90 % rozdílu mezi holou půdou a LAI 7, a jak moc index posune změna chlorofylu, vztaženo k tomuto rozdílu.

Parametry, které student mění:

- `INDICES = {`: indexy; přidej vlastní, např. MTCI

**Úkol 2.** Při jakém LAI se nasytí NDVI a při jakém NDRE a CIre? Proč se indexy s červenou hranou nasycují později? Jakou cenu za to platí (poslední sloupec)? Přidej do `INDICES` vlastní index, např. MTCI = (B6 − B5)/(B5 − B4), tj. `(b["rededge2"] - b["rededge1"]) / (b["rededge1"] - b["red"])`, a zařaď ho mezi ostatní.

### 4. Tabulka simulací a jeden pixel

Model neumí počítat pozpátku. Proto spustíme tisíce simulací s náhodnými hodnotami proměnných v zadaných rozsazích a pro pixel hledáme ty, jejichž pásma se nejvíc podobají naměřeným (nejmenší RMSE). Rozsahy jsou apriorní znalost: co o porostu víme předem. Pro každý snímek se tabulka počítá s jeho výškou Slunce.

Parametry, které student mění:

- `N_LUT = 20000`: počet simulací v tabulce
- `"lai": (0, 7), "ala": (30, 80), "psoil": (0, 1), "rsoil": (0.5, 1.5)}`: rozsahy proměnných (apriorní znalost)
- `K = 50`: kolik nejlepších řešení z tabulky vzít
- `PLON, PLAT = 14.3516, 50.1632`: bod (pole u Únětic); zkus les 14.366, 50.148

**Úkol 3.** Jak široké je rozpětí LAI mezi nejlepšími řešeními a jak souvisí s úhlem listů a chlorofylem (grafy vpravo)? Porovnej variační koeficient `lai`, `cab` a jejich součinu `ccc` (chlorofyl v porostu, µg na cm² půdy). Proč je součin určen lépe než každá složka zvlášť? Zkus `K = 10` a `K = 200` a bod v lese.

### 5. Mapa LAI a kde model nesedí

Stejný postup pro všechny pixely výřezu. Pro každý pixel dostaneme medián LAI z nejlepších řešení, jejich směrodatnou odchylku jako míru nejistoty a RMSE nejlepší simulace jako míru, jak dobře model pixel vůbec vysvětlí.

**Úkol 4.** Kde je RMSE největší a proč? Proč u vody vyjde nějaké LAI, i když tam žádné listy nejsou, a proč zástavba sedí skoro stejně dobře jako louka? Les tu vychází s LAI kolem 2, zatímco souhrn pozemních měření (Asner a kol. 2003) uvádí pro stálezelené lesy mírného pásu průměr 5,1 až 6,7. Které předpoklady PROSAILu (jedna souvislá vrstva listů, žádné kmeny, mezery ani stíny korun) k rozdílu přispívají?

### 6. LAI, NDVI a nejistota na skutečných datech

Načte knihovny a stáhne data.

**Úkol 5.** Od jakého NDVI roste nejistota LAI nejrychleji a jak to souvisí s nasycením z kroku 3? Jak se mezi květnem a červencem změnilo NDVI a LAI na polích, loukách a v lese? Proč by samotné NDVI podcenilo rozdíl mezi dvěma hustými porosty?

**Rozšíření (nepovinné).** Zužte rozsahy v `RANGES` podle toho, co o porostu víš (např. `ala` 50–65, `cab` 30–60), a spusť kroky 4 až 6 znovu. Jak se změní nejistota LAI? Co se stane, když apriorní znalost neplatí, třeba pro les s jiným úhlem listů?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.
- Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Jacquemoud, S. a kol. (2009). PROSPECT + SAIL models: A review of use for vegetation characterization. *Remote Sensing of Environment* 113, S56–S66. https://doi.org/10.1016/j.rse.2008.01.026
- Feret, J.-B. a kol. (2008). PROSPECT-4 and 5: Advances in the leaf optical properties model separating photosynthetic pigments. *Remote Sensing of Environment* 112, 3030–3043. https://doi.org/10.1016/j.rse.2008.02.012
- Verhoef, W., Jia, L., Xiao, Q., Su, Z. (2007). Unified optical-thermal four-stream radiative transfer theory for homogeneous vegetation canopies. *IEEE Transactions on Geoscience and Remote Sensing* 45, 1808–1822. https://doi.org/10.1109/TGRS.2007.895844
- Gómez-Dans, J. *prosail*: Python bindings for PROSPECT and SAIL. https://github.com/jgomezdans/prosail
- Combal, B. a kol. (2002). Retrieval of canopy biophysical variables from bidirectional reflectance using prior information to solve the ill-posed inverse problem. *Remote Sensing of Environment* 84, 1–15.
- Gitelson, A. A. a kol. (2005). Remote estimation of canopy chlorophyll content in crops. *Geophysical Research Letters* 32, L08403. https://doi.org/10.1029/2005GL022688
- Asner, G. P., Scurlock, J. M. O., Hicke, J. A. (2003). Global synthesis of leaf area index observations: implications for ecological and remote sensing studies. *Global Ecology and Biogeography* 12, 191–205. https://doi.org/10.1046/j.1466-822X.2003.00026.x
- Pedregosa, F. a kol. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
