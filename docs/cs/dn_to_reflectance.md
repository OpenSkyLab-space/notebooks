# Od DN k odrazivosti: Landsat 8 nad Prahou

Popis notebooku k laboratoři [Od DN k odrazivosti](https://openskylab.space/edu_viz_dn_to_reflectance.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/dn_to_reflectance_cs.ipynb) · verze 1.0 · asi 45 min · pět úkolů

## O čem notebook je

Laboratoř prochází řetězec od digitálního čísla přes zář k odrazivosti nad atmosférou (TOA) a na povrchu (BOA) a ukazuje, co opraví metoda tmavého objektu (DOS) a empirická přímka. Tady celý řetězec spočítáš na dvou skutečných snímcích Landsatu 8 nad Prahou a výsledek porovnáš s odrazivostí Sentinelu-2 L2A z téhož týdne.

## Cíl

Převést DN na zář a odrazivost TOA, ukázat, proč DN ze dvou dnů nejsou srovnatelná, změřit vliv atmosféry na vodě a porovnat korekci DOS a empirickou přímku s odrazivostí na povrchu.

## Data

Landsat 8 OLI Collection 1 Level-1 z veřejného archivu Google Cloud: `LC08_L1TP_191025_20190626_20190705_01_T1` (26. 6. 2019, výška Slunce 60°) a `LC08_L1TP_191025_20190218_20190222_01_T1` (18. 2. 2019, výška Slunce 26°), pásma B1–B7, BQA a MTL. Pro srovnání Sentinel-2 L2A `S2B_33UVR_20190625_0_L2A` (25. 6. 2019) z Earth Search. Výřez 12 × 12 km kolem centra Prahy, asi 25 MB.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Notebook je uložený bez výstupů; čísla a grafy vzniknou až při spuštění a u průběžně aktualizovaných dat se mohou mezi běhy lišit.

## Postup krok za krokem

### 1. Příprava a data

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

### 2. Z DN na zář a odrazivost TOA

Zář: L = M_L · DN + A_L. Odrazivost TOA: ρ = (M_ρ · DN + A_ρ) / sin(výška Slunce). Koeficienty jsou v souboru MTL; v M_ρ je už započtena vzdálenost Země–Slunce i sluneční ozáření pásma.

**Úkol 1.** O kolik se mediány DN mezi létem a zimou liší a o kolik mediány odrazivosti TOA? Kolik z rozdílu DN vysvětlí jen výška Slunce (porovnej poměr sinů výšek)? Proč se ani odrazivost TOA mezi daty úplně neshoduje (stav porostu, případný sníh, atmosféra)?

### 3. Odrazivost na povrchu ze Sentinelu-2 jako reference

Sentinel-2 L2A z 25. 6. 2019 (o den dřív) má odrazivost BOA z modelu Sen2Cor. Převzorkujeme ho na mřížku Landsatu (průměr do pixelu 30 m) a přiřadíme si pásma s podobnou vlnovou délkou. Dokonalou shodu nečekej: jde o jiný senzor s trochu jinými pásmy, snímek o den dřív a z jiného úhlu pohledu.

**Úkol 2.** Porovnej oba obrázky se stejným roztažením barev. Proč působí snímek s odrazivostí TOA světleji, modřeji a méně kontrastně? Které povrchy se mezi TOA a BOA mění nejvíc, tmavé, nebo světlé? Vysvětli to aditivním příspěvkem atmosféry.

### 4. Modrá voda nad atmosférou

Vltava a nádrže jsou v NIR skoro černé. Porovnáme jejich odrazivost TOA a BOA ve všech pásmech: rozdíl je hlavně světlo rozptýlené atmosférou (zář dráhy).

**Úkol 3.** Jak se rozdíl TOA − BOA nad vodou mění s vlnovou délkou? Porovnej poměr mezi pásmy B1 a B4 s Rayleighovým zákonem (rozptyl ∝ λ⁻⁴). Proč je voda nad atmosférou modrá, i když je na povrchu tmavá ve všech pásmech?

### 5. Metoda tmavého objektu (DOS)

Předpokládáme, že nejtmavší pixely ve scéně mají na povrchu odrazivost skoro nulovou (běžně se bere 1 %, Chavez 1996). Co mají navíc, je zář dráhy, a tu odečteme od celé scény. DOS opraví jen aditivní část atmosféry.

Parametry, které student mění:

- `pct = 0.1`: percentil, který považujeme za tmavý objekt (%)
- `rho_dark = 0.01`: předpokládaná skutečná odrazivost tmavého objektu

**Úkol 4.** Ve kterých pásmech DOS chybu proti BOA zmenší a ve kterých ji naopak zvětší? Proč je bias DOS ve všech pásmech záporný (co DOS dělá s násobnou složkou, propustností atmosféry)? Nastav `pct = 2` a pak `rho_dark = 0`: co se stane? Kdy DOS selže úplně (zimní scéna se sněhem bez tmavých objektů, opar jen nad částí scény)?

### 6. Empirická přímka

Empirická přímka opravuje odrazivost pomocí sklonu a posunu. V terénu mohou
jako reference sloužit fyzické kalibrační panely se známou odrazivostí.
V tomto cvičení použijeme **referenční pixely**: jejich referenční odrazivost
převezmeme ze snímku Sentinel-2 L2A.

Pro každé pásmo hledáme přímku mezi odrazivostí TOA Landsatu a referenční
odrazivostí BOA. Touto přímkou potom opravíme celé pásmo:

$$
\widehat{\rho}_{\mathrm{BOA}} = a\,\rho_{\mathrm{TOA}} + b.
$$

- $\rho_{\mathrm{TOA}}$ je vstupní odrazivost na horní hranici atmosféry.
- $\widehat{\rho}_{\mathrm{BOA}}$ je náš odhad odrazivosti na povrchu.
- $a$ je **sklon** (`slope`): mění měřítko hodnot.
- $b$ je **posun** (`offset`): ke každé hodnotě přičítá stejnou opravu.

Odrazivost, sklon i posun jsou bezrozměrné. Pro zjednodušený model atmosféry

$$
\rho_{\mathrm{TOA}} \approx \rho_{\mathrm{dráhy}} + T\,\rho_{\mathrm{BOA}}
\quad\Rightarrow\quad
a \approx \frac{1}{T},\qquad b \approx -\frac{\rho_{\mathrm{dráhy}}}{T},
$$

kde $T$ je propustnost atmosféry a $\rho_{\mathrm{dráhy}}$ příspěvek rozptylu
v atmosféře vyjádřený jako odrazivost. Tento fyzikální výklad je přibližný:
zde srovnáváme dva různé senzory a referenční BOA je sama výsledkem zpracování.

### 6.1 Vyber referenční pixely a oprav snímek

V každém pásmu vybereme podle Sentinelu-2 `n_reference` nejtmavších a stejný
počet nejsvětlejších platných pixelů. Při `n_reference = 300` tedy přímku
prokládáme **600 dvojicemi hodnot**, ne dvěma průměry skupin. Různá pásma
mohou vybrat různé pixely.

Zápis `[valid]` vybere hodnoty na společných platných místech obou snímků
ve stejném pořadí. `np.argsort` vrátí jejich indexy od nejtmavších po
nejsvětlejší. `np.polyfit(..., deg=1)` z vybraných dvojic vypočítá sklon
a posun přímky. Tu pak použijeme na celé pásmo Landsatu.

**Po změně `n_reference` spusť znovu všechny tři buňky této části (6.1–6.3).**

### 6.2 Porovnej chyby všech tří postupů

Tabulka ukáže sklon a posun v každém pásmu a RMSE původní odrazivosti TOA,
korekce DOS a empirické přímky proti referenci Sentinel-2 BOA:

$$
\mathrm{RMSE} = \sqrt{\frac{1}{N}\sum_{i=1}^{N}
\left(\rho_i^{\mathrm{odhad}}-\rho_i^{\mathrm{reference}}\right)^2}.
$$

$N$ je počet všech platných pixelů a $i$ označuje jeden z nich. Menší RMSE
znamená lepší shodu s referencí. Všechny metody hodnotíme na stejných pixelech,
včetně těch použitých k proložení přímky; nejde tedy o nezávislé ověření přesnosti.

### 6.3 Zobraz shodu se Sentinelem-2

Na vodorovné ose je referenční BOA, na svislé ose odrazivost daného postupu.
Černá přímka 1 : 1 označuje úplnou shodu. Barvy rozlišují modré pásmo B2,
červené B4 a blízké infračervené B5.

Pro přehlednost vykreslíme jen **4 000 náhodně vybraných platných pixelů**,
stejných pro všechny grafy i pásma. Pevné semínko `0` zajistí opakovatelný
výběr. Tento vzorek slouží pouze ke kreslení; kalibraci ani RMSE nemění.

Parametry, které student mění:

- `n_reference = 300`: pixelů v každé skupině

**Úkol 5.** Proč má empirická přímka v modrých pásmech záporný posun a sklon jiný než 1? Co fyzikálně vyjadřují? Která metoda má nejmenší RMSE v jednotlivých pásmech a proč DOS nemůže opravit sklon? Nastav `n_reference = 20` a znovu spusť buňky 6.1–6.3: jak se změní sklon, posun a RMSE? Proč v terénu stačí k určení přímky dva kalibrační panely s různou známou odrazivostí, ale musí ležet ve stejném snímku a za stejného osvětlení?

**Rozšíření (nepovinné).** Porovnej výsledky se spolužákem, který spustil notebook pro jiné místo: vyšel podobný rozdíl TOA − BOA nad vodou a podobný sklon empirické přímky? Čím se mohou lišit (jiný den, jiný opar, jiná výška Slunce)?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Landsat 8 OLI Collection 1 Level-1, U.S. Geological Survey; veřejný archiv Google Cloud (`gcp-public-data-landsat`). Data USGS jsou bez omezení užití, s uvedením zdroje.
- USGS (2019). *Landsat 8 (L8) Data Users Handbook*, verze 5.0, kap. 5 (převod DN na zář a odrazivost TOA).
- Copernicus Sentinel-2 data 2019, ESA (L2A, Sen2Cor), registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.
- Chavez, P. S. (1988). An improved dark-object subtraction technique for atmospheric scattering correction of multispectral data. *Remote Sensing of Environment* 24, 459–479. https://doi.org/10.1016/0034-4257(88)90019-3
- Chavez, P. S. (1996). Image-based atmospheric corrections – revisited and improved. *Photogrammetric Engineering and Remote Sensing* 62(9), 1025–1036.
- Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20, 2653–2662. https://doi.org/10.1080/014311699211994

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
