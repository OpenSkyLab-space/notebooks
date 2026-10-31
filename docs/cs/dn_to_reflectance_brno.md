# Od DN k odrazivosti: Landsat 8 nad Brnem

Popis notebooku k vizuálu [Od DN k odrazivosti](https://openskylab.space/edu_viz_dn_to_reflectance.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/dn_to_reflectance_brno_cs.ipynb) · verze 1.0 · asi 45 min · pět úkolů

## O čem notebook je

Vizuál prochází řetězec od digitálního čísla přes zář k odrazivosti nad atmosférou (TOA) a na povrchu (BOA) a ukazuje, co opraví metoda tmavého objektu (DOS) a empirická přímka. Tady celý řetězec spočítáš na dvou skutečných snímcích Landsatu 8 nad Brnem a výsledek porovnáš s odrazivostí Sentinelu-2 L2A z téhož týdne.

## Cíl

Převést DN na zář a odrazivost TOA, ukázat, proč DN ze dvou dnů nejsou srovnatelná, změřit vliv atmosféry na vodě a porovnat korekci DOS a empirickou přímku s odrazivostí na povrchu.

## Data

Landsat 8 OLI Collection 1 Level-1 z veřejného archivu Google Cloud: `LC08_L1TP_190026_20200808_20200821_01_T1` (8. 8. 2020, výška Slunce 54°) a `LC08_L1TP_190026_20190227_20190309_01_T1` (27. 2. 2019, výška Slunce 30°), pásma B1–B7, BQA a MTL. Pro srovnání Sentinel-2 L2A `S2B_33UXQ_20200808_0_L2A` (8. 8. 2020) z Earth Search. Výřez 12 × 12 km od Brněnské přehrady k centru Brna, asi 25 MB.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a data

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

### 2. Z DN na zář a odrazivost TOA

Zář: L = M_L · DN + A_L. Odrazivost TOA: ρ = (M_ρ · DN + A_ρ) / sin(výška Slunce). Koeficienty jsou v souboru MTL; v M_ρ je už započtena vzdálenost Země–Slunce i sluneční ozáření pásma.

**Úkol 1.** O kolik se mediány DN mezi létem a zimou liší a o kolik mediány odrazivosti TOA? Kolik z rozdílu DN vysvětlí jen výška Slunce (porovnej poměr sinů výšek)? Proč se ani odrazivost TOA mezi daty úplně neshoduje (stav porostu, případný sníh, atmosféra)?

### 3. Odrazivost na povrchu ze Sentinelu-2 jako reference

Sentinel-2 L2A z 8. 8. 2020 (týž den) má odrazivost BOA z modelu Sen2Cor. Převzorkujeme ho na mřížku Landsatu (průměr do pixelu 30 m) a přiřadíme si pásma s podobnou vlnovou délkou. Dokonalou shodu nečekej: jde o jiný senzor s trochu jinými pásmy, snímek pořízený asi o 20 minut později a z jiného úhlu pohledu.

**Úkol 2.** Porovnej oba obrázky se stejným roztažením barev. Proč působí snímek s odrazivostí TOA světleji, modřeji a méně kontrastně? Které povrchy se mezi TOA a BOA mění nejvíc, tmavé, nebo světlé? Vysvětli to aditivním příspěvkem atmosféry.

### 4. Modrá voda nad atmosférou

Brněnská přehrada a Svratka jsou v NIR skoro černé. Porovnáme jejich odrazivost TOA a BOA ve všech pásmech: rozdíl je hlavně světlo rozptýlené atmosférou (zář dráhy).

**Úkol 3.** Jak se rozdíl TOA − BOA nad vodou mění s vlnovou délkou? Porovnej poměr mezi pásmy B1 a B4 s Rayleighovým zákonem (rozptyl ∝ λ⁻⁴). Proč je voda nad atmosférou modrá, i když je na povrchu tmavá ve všech pásmech?

### 5. Metoda tmavého objektu (DOS)

Předpokládáme, že nejtmavší pixely ve scéně mají na povrchu odrazivost skoro nulovou (běžně se bere 1 %, Chavez 1996). Co mají navíc, je zář dráhy, a tu odečteme od celé scény. DOS opraví jen aditivní část atmosféry.

Parametry, které student mění:

- `pct = 0.1`: percentil, který považujeme za tmavý objekt (%)
- `rho_dark = 0.01`: předpokládaná skutečná odrazivost tmavého objektu

**Úkol 4.** Ve kterých pásmech DOS chybu proti BOA zmenší a ve kterých ji naopak zvětší? Proč je bias DOS ve všech pásmech záporný (co DOS dělá s násobnou složkou, propustností atmosféry)? Nastav `pct = 2` a pak `rho_dark = 0`: co se stane? Kdy DOS selže úplně (zimní scéna se sněhem bez tmavých objektů, opar jen nad částí scény)?

### 6. Empirická přímka

V terénu se na snímek položí tmavý a světlý panel se změřenou odrazivostí. Tady jako panely poslouží tmavé a světlé pixely, jejichž odrazivost na povrchu známe ze Sentinelu-2. Pro každé pásmo proložíme přímku ρ_BOA = a · ρ_TOA + b: posun b souvisí se září dráhy a sklon s propustností atmosféry: pro ρ_TOA ≈ ρ_dráhy + T · ρ_BOA vychází a ≈ 1/T a b ≈ −ρ_dráhy/T.

Parametry, které student mění:

- `n_panel = 300`: kolik nejtmavších a nejsvětlejších pixelů použít jako panely

**Úkol 5.** Proč má empirická přímka v modrých pásmech záporný posun a sklon jiný než 1? Co fyzikálně vyjadřují? Která metoda dopadla nejlépe a proč DOS nemůže opravit sklon? Nastav `n_panel = 20`: co se stane se spolehlivostí přímky? Proč v terénu stačí dva panely, ale musí ležet ve stejném snímku a za stejného osvětlení?

**Rozšíření (nepovinné).** Porovnej výsledky se spolužákem, který spustil notebook pro jiné místo: vyšel podobný rozdíl TOA − BOA nad vodou a podobný sklon empirické přímky? Čím se mohou lišit (jiný den, jiný opar, jiná výška Slunce)?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; veřejný archiv Google Cloud (`gcp-public-data-landsat`). Data USGS jsou bez omezení užití, s uvedením zdroje.
- USGS (2019). *Landsat 8 (L8) Data Users Handbook*, verze 5.0, kap. 5 (převod DN na zář a odrazivost TOA).
- Copernicus Sentinel-2 data 2020, ESA (L2A, Sen2Cor), registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.
- Chavez, P. S. (1988). An improved dark-object subtraction technique for atmospheric scattering correction of multispectral data. *Remote Sensing of Environment* 24, 459–479. https://doi.org/10.1016/0034-4257(88)90019-3
- Chavez, P. S. (1996). Image-based atmospheric corrections – revisited and improved. *Photogrammetric Engineering and Remote Sensing* 62(9), 1025–1036.
- Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20, 2653–2662. https://doi.org/10.1080/014311699211994

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
