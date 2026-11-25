# Teplota Brna z Landsatu 8: Planckův zákon v praxi

Popis notebooku k laboratoři [Záření černého tělesa](https://openskylab.space/edu_viz_blackbody_radiation.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/blackbody_radiation_brno_cs.ipynb) · verze 1.0 · asi 45 min · pět úkolů

## O čem notebook je

Laboratoř ukazuje Planckův zákon, Wienův posun, čtvrtou mocninu Stefanova–Boltzmannova zákona a vliv emisivity. Tady stejné vzorce použiješ na skutečný termální snímek Landsatu 8 ze slunečného 8. srpna 2020 a z digitálních čísel spočítáš teplotu povrchu Brna.

## Cíl

Převést termální pásmo Landsatu 8 z DN na zář a jasovou teplotu, opravit ji o emisivitu, odhadnout chybu ze špatné emisivity a odrazu oblohy a ukázat, proč družice hledají malé požáry ve 3,9 µm.

## Data

Landsat 8 OLI/TIRS, Collection 1 Level-1, scéna `LC08_L1TP_190026_20200808_20200821_01_T1` (8. 8. 2020, 9:45 UTC, oblačnost 2,5 %), pásma B4, B5 a B10 a soubor MTL s kalibračními konstantami z veřejného archivu Google Cloud. Čte se jen výřez 16 × 16 km kolem centra Brna (asi 3 MB).

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Notebook je uložený bez výstupů; čísla a grafy vzniknou až při spuštění a u průběžně aktualizovaných dat se mohou mezi běhy lišit.

## Postup krok za krokem

### 1. Příprava

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

### 2. Planckův zákon, Wien a čtvrtá mocnina

### Z teploty na spektrální zář: Planckův zákon

Planckův zákon popisuje, jak záření černého tělesa závisí na vlnové délce a teplotě:

$$
L_\lambda(\lambda, T) =
\frac{2 h c^2}{\lambda^5}
\frac{1}{\exp\!\left(\frac{h c}{\lambda k T}\right)-1}.
$$

| Symbol | Význam | Jednotka ve vzorci |
| --- | --- | --- |
| $\lambda$ | vlnová délka | $\mathrm{m}$ |
| $T$ | teplota černého tělesa | $\mathrm{K}$ |
| $h$ | Planckova konstanta | $\mathrm{J\,s}$ |
| $c$ | rychlost světla ve vakuu | $\mathrm{m\,s^{-1}}$ |
| $k$ | Boltzmannova konstanta | $\mathrm{J\,K^{-1}}$ |

Spektrální zář $L_\lambda$ v tomto vzorci má jednotku
$\mathrm{W\,m^{-2}\,sr^{-1}\,m^{-1}}$: je vyjádřena na metr vlnové délky.

**Jak vzorec souvisí s kódem:** `planck(lam_um, T)` přijímá vlnovou délku v µm
a teplotu v K. První `1e-6` převádí vlnovou délku z µm na m. Poslední `1e-6`
převádí vypočtenou zář na $\mathrm{W\,m^{-2}\,sr^{-1}\,\mu m^{-1}}$, tedy na µm
vlnové délky, které používáme v notebooku.

`np.expm1(x)` počítá $e^x-1$; pro malé hodnoty $x$ je numericky přesnější
než přímý zápis `np.exp(x) - 1`.

### Ze spektrální záře na jasovou teplotu

**Jasová teplota** $T_b$ je teplota černého tělesa, které by na dané vlnové délce
mělo naměřenou spektrální zář. Vyjádřením teploty z Planckova zákona dostaneme:

$$
T_b(\lambda, L_\lambda) =
\frac{h c}{\lambda k}
\frac{1}{\ln\!\left(1+\frac{2 h c^2}{\lambda^5 L_\lambda}\right)}.
$$

Symboly a jednotky jsou stejné jako výše: $\lambda$ je v metrech a $L_\lambda$
je zář na metr vlnové délky. Výsledná teplota $T_b$ je v kelvinech.
U skutečného povrchu se jasová teplota může lišit od jeho teploty; vliv
emisivity prozkoumáme v dalších částech notebooku.

**Jak vzorec souvisí s kódem:** `planck_inv(lam_um, L)` přijímá vlnovou délku
v µm a zář v $\mathrm{W\,m^{-2}\,sr^{-1}\,\mu m^{-1}}$. Vlnovou délku proto
násobí `1e-6` a zář násobí `1e6`, aby ve vzorci byly jednotky na metr.
Funkce vrací jasovou teplotu v K.

`np.log1p(x)` počítá přirozený logaritmus $\ln(1+x)$; pro malé hodnoty $x$
je numericky přesnější než přímý zápis `np.log(1 + x)`.

Parametry, které student mění:

- `T_list = [300, 600, 900, 5772]`: teploty v K (krajina, kamna, požár, povrch Slunce)

**Úkol 1.** Kolikrát vzroste celkový tok a kolikrát zář v 10,9 µm, když teplotu zdvojnásobíš z 300 na 600 K? Proč se obě čísla liší? Spočítej také, o kolik procent víc vyzáří asfalt o 45 °C než tráva o 25 °C.

### 3. Skutečná scéna: z DN na jasovou teplotu

Pásmo B10 (10,6–11,2 µm) ukládá digitální čísla (DN). Soubor MTL obsahuje koeficienty lineárního převodu na spektrální zář a konstanty $K_1$, $K_2$ pro převod záře na jasovou teplotu:

$$
L_\lambda = M_L \cdot DN + A_L, \qquad T_b = \frac{K_2}{\ln\!\left(\frac{K_1}{L_\lambda} + 1\right)}.
$$

$M_L$ a $A_L$ jsou `RADIANCE_MULT_BAND_10` a `RADIANCE_ADD_BAND_10`, $L_\lambda$ vychází ve W·m⁻²·sr⁻¹·µm⁻¹ a $T_b$ v kelvinech. Druhý vzorec je Planckův zákon zjednodušený na jedno pásmo: $K_1$ a $K_2$ v sobě mají konstanty $h$, $c$, $k$ a efektivní vlnovou délku pásma.

Parametry, které student mění:

- `lon, lat, half = 16.61, 49.195, 8000`: střed výřezu (°) a poloviční šířka (m)

**Úkol 2.** Najdi na mapě Svratku a Brněnskou přehradu, lesy (třeba kolem Kohoutovic) a zastavěné plochy s velkými halami (letiště Tuřany, průmyslové areály). Jaké jasové teploty mají? Proč je rozdíl mezi vodou a střechami hal kolem poledne tak velký? Proč není jasová teplota totéž co teplota povrchu?

### 4. Emisivita

Reálné povrchy vyzařují méně než černé těleso: $L_\lambda = \varepsilon \, B_\lambda(T)$, kde $B_\lambda$ je Planckova funkce a $\varepsilon$ emisivita (0 až 1). Emisivitu odhadneme z NDVI zjednodušenou metodou prahů podle Sobrina a kol. (2004): holý povrch 0,97, plná vegetace 0,99, mezi tím podle podílu vegetace s opravou na vícenásobné odrazy mezi rostlinami a půdou. Vodě (NDVI < 0) dáme typickou hodnotu 0,991. Odraz oblohy a atmosféru zatím zanedbáme.

Parametry, které student mění:

- `eps_soil, eps_veg, eps_water = 0.97, 0.99, 0.991`: emisivity
- `T_true = 273.15 + 40`: skutečná teplota povrchu v K

**Úkol 3.** Kde je oprava o emisivitu největší a proč? Zhruba o kolik kelvinů se senzor splete na každou setinu emisivity? Změň `eps_soil` na 0,95 (beton, asfalt) a sleduj, jak se změní oprava v zastavěných plochách.

### 5. Odraz oblohy

Povrch s emisivitou ε odráží 1 − ε dlouhovlnného záření, které na něj svítí z oblohy. Jasná obloha je v 10 µm velmi studená, zatažená má zhruba teplotu základny oblačnosti. Senzor dostane

$$
L_\lambda = \varepsilon \, B_\lambda(T) + (1 - \varepsilon) \, B_\lambda(T_\mathrm{obloha}).
$$

Parametry, které student mění:

- `T_surf = z_viz("T_surf", 273.15 + 27)`: teplota povrchu

**Úkol 4.** Proč lesklý plech pod jasnou oblohou vypadá v termokameře mrazivě studený, i když má 27 °C? Proč při obloze stejně teplé jako povrch nehraje emisivita žádnou roli? Za jakého počasí bys proto plánoval termální snímkování střech?

### 6. Požár menší než pixel

Pixel je směs: podíl $p$ hoří při teplotě požáru, zbytek má teplotu pozadí, takže $L_\lambda = p \, B_\lambda(T_\mathrm{požár}) + (1 - p) \, B_\lambda(T_\mathrm{pozadí})$. Jako pozadí vezmeme medián skutečné jasové teploty z výřezu (Brno) a porovnáme pásmo 3,9 µm (požárová pásma MODIS a VIIRS leží mezi 3,7 a 4,1 µm) s pásmem 10,9 µm.

Parametry, které student mění:

- `T_fire = z_viz("T_fire", 900)`: teplota požáru v K

**Úkol 5.** Při jakém podílu požáru se pixel ohřeje o 10 K ve 3,9 µm a při jakém v 10,9 µm? Jakou plochu to je v pixelu MODIS 1 × 1 km? Vysvětli rozdíl Wienovým zákonem. Proč algoritmy ve dne hlídají i odražené Slunce ve 3,9 µm?

**Rozšíření (nepovinné).** Porovnej se spolužákem, který spustil notebook pro jiné místo a den: jaký rozsah jasových teplot vyšel jemu? Kolik z rozdílu může jít na vrub jiného dne a hodiny, jiné výšky Slunce a jiného složení krajiny?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Landsat 8 OLI/TIRS Collection 1 Level-1, U.S. Geological Survey; veřejný archiv Google Cloud (`gcp-public-data-landsat`). Data USGS jsou volná bez omezení užití (public domain), s uvedením zdroje.
- Převod DN na zář a jasovou teplotu: USGS (2019). *Landsat 8 (L8) Data Users Handbook*, verze 5.0, kap. 5.
- Emisivita z NDVI: Sobrino, J. A., Jiménez-Muñoz, J. C., Paolini, L. (2004). Land surface temperature retrieval from LANDSAT TM 5. *Remote Sensing of Environment* 90, 434–440. https://doi.org/10.1016/j.rse.2004.02.003
- Detekce požárů ve 3,9 a 11 µm: Giglio, L., Schroeder, W., Justice, C. O. (2016). The collection 6 MODIS active fire detection algorithm and fire products. *Remote Sensing of Environment* 178, 31–41. https://doi.org/10.1016/j.rse.2016.02.054

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
