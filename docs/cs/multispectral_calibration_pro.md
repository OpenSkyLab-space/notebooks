# Kalibrace multispektrální kamery, pokročilá verze: geometrie pásem, chyby NDVI, termální a panchromatické pásmo

Popis notebooku k vizuálu [Kalibrace multispektrální kamery](https://openskylab.space/edu_viz_multispectral_calibration.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/multispectral_calibration_pro_cs.ipynb) · verze 1.0 · asi 60 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku o kalibraci multispektrální kamery. Kamera MicaSense Altum-PT má sedm samostatných objektivů: pět multispektrálních, jeden panchromatický a jeden termální. Na skutečném snímku z letu zjistíš, jak se pásma vůči sobě posouvají, otáčejí a liší měřítkem a co to dělá s NDVI, jak se chyba kalibrace jednoho pásma přenáší do indexů, jak souvisí teplota povrchu s vegetací a co umí a neumí zostření panchromatickým pásmem.

## Cíl

Změřit paralaxu mezi pásmy a z ní vzdálenost kamery od panelu, sesadit pásma afinní transformací a porovnat ji s metadaty soustavy kamer, odvodit citlivost NDVI na chybu kalibrace, přenést NDVI na mřížku termokamery a porovnat ho s teplotou povrchu a zostřit pásma panchromatickým snímkem.

## Data

Dva snímky (všech 7 pásem) kamery MicaSense Altum-PT s DLS 2 z ukázkových dat MicaSense (repozitář micasense/imageprocessing, licence MIT): IMG_0000 (panel RP06, 15. 8. 2022 19:16 UTC) a IMG_0010 (let o 3 minuty později, asi 97 m nad terénem), 48,51° s. š., 122,42° z. d. Pět multispektrálních pásem má 2064 × 1544 pixelů, panchromatické 4112 × 3008 a termální 320 × 256. Termální pásmo je v setinách kelvinu a kamera počítá s emisivitou 1,0 (přesnost podle výrobce ±5 K).

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a snímky

Načteme všech sedm pásem snímku z letu a pět pásem snímku panelu. Tabulka ukazuje, že každé pásmo má vlastní objektiv s trochu jinou ohniskovou vzdáleností a že objektivy jsou od sebe posunuté o centimetry (RigTranslations v metadatech, vůči zelenému pásmu).

### 2. Paralaxa mezi pásmy

Dva objektivy vzdálené o T vidí stejný bod ve vzdálenosti H posunutý o Δ = T · f / (H · p) pixelů, kde f je ohnisková vzdálenost a p velikost pixelu snímače. Ze 100 m je to kolem jednoho pixelu, z metru ze země přes sto. Část posunu nezávisí na vzdálenosti (objektivy nejsou přesně rovnoběžné), proto porovnáme posun na snímku panelu a na snímku z letu: rozdíl je téměř čistá paralaxa panelu.

**Úkol 1.** Proč se posun pásem na snímku panelu liší od posunu na snímku z letu o desítky pixelů, když jde o stejnou kameru? Z jaké vzdálenosti byl panel vyfocen a jak tomu odpovídá výška letu nad terénem? Spočítej paralaxu modrého pásma vůči zelenému při letu ve 30 m a při letu ve 40 m nad lesem s korunami vysokými 20 m (pro koruny i pro zem). Proč pak k sesazení pásem nestačí jeden posun pro celý snímek?

### 3. Měřítko a otočení pásem

Posun změříme zvlášť v každé dlaždici 256 × 256 pixelů a proložíme ho afinní transformací d = t + A · (x, y): t je posun ve středu, z matice A plyne rozdíl měřítka a otočení. Rozdíl měřítka by měl odpovídat poměru ohniskových vzdáleností, otočení třetímu úhlu RigRelatives (v metadatech ve stupních).

Parametry, které student mění:

- `TILE = 256`: velikost dlaždice (px)
- `BAND = 3`: pásmo pro mapu posunů (1 modré, 3 červené, 4 NIR, 5 red edge)

**Úkol 2.** Proč se posun pásem mění po snímku (podívej se na šipky pro červené pásmo a pak pro NIR)? Souhlasí měřítko s poměrem ohniskových vzdáleností a otočení s RigRelatives? O kolik pixelů se v rohu snímku liší skutečný posun od posunu ve středu? Kde ve snímku a na kterých objektech se NDVI z celopixelového posunu (jako v základní verzi) liší od afinního sesazení nejvíc a proč právě tam?

### 4. Jak se chyba kalibrace přenáší do NDVI

Když má NIR relativní chybu e_NIR a červené pásmo e_Red, změní se NDVI přibližně o ΔNDVI ≈ (1 − NDVI²) / 2 · (e_NIR − e_Red). Společná chyba obou pásem se vyruší. Porovnáme vzorec s výpočtem na snímku a podíváme se, co s indexy udělá kalibrace jen z DLS bez panelu.

Parametry, které student mění:

- `REGIONS = {"silnice": (slice(1140, 1260), slice(1570, 1650)), "suchá louka": (slice(100, 500), slice(1120, 1500)), "sad": (slice(20, 640), slice(20, 560))}`: oblasti (řádky, sloupce)
- `ERR_RED, ERR_NIR = 0.00, 0.05`: relativní chyba kalibrace červeného a NIR pásma (0,05 = +5 %)

**Úkol 3.** Nastav ERR_NIR = 0,05 a ERR_RED = 0: proč se NDVI silnice a louky posune víc než NDVI sadu? Ověř vzorec pro ERR_RED = 0,05 a pro ERR_RED = ERR_NIR. Kalibrace jen z DLS dává odrazivost v jednotlivých pásmech jinou o jednotky až desítky procent (poměr vypsal výpočet), přesto se NDVI změní jen o setiny. Proč? Pro které úlohy tedy stačí DLS bez panelu a pro které ne?

### 5. Termální pásmo a vegetace

Termální pásmo ukládá teplotu v setinách kelvinu, vypočtenou s emisivitou 1,0. Skutečný povrch má emisivitu nižší a část záření, které kamera vidí, je odražená obloha. V přiblížení šedého tělesa σT_b⁴ = ε σT⁴ + (1 − ε) σT_obl⁴. Termokamera má hrubší pixel i jinou ohniskovou vzdálenost, proto NDVI zprůměrujeme na velikost termálního pixelu, přepočteme přes hlavní body objektivů a zbývající posun najdeme tak, aby korelace NDVI a teploty byla co nejsilnější.

Parametry, které student mění:

- `EPS = 0.95`: emisivita povrchu pro opravu (kamera počítá s 1,0)
- `T_SKY = -30.0`: jasová teplota oblohy (°C), předpoklad pro jasnou oblohu

**Úkol 4.** Jak velký je termální pixel na zemi a kolik multispektrálních pixelů do něj padne? Jak teplé jsou silnice, suchá louka a sad a čím se dá vysvětlit, že je sad o tolik chladnější? Najdi v grafu a na mapách body s NDVI pod nulou a nízkou teplotou: co to je? Nastav EPS na 0,97 (vegetace) a 0,92 (suchá půda) a T_SKY na −10 °C (oblačno): o kolik se teplota změní a je to víc, nebo méně než přesnost kamery?

### 6. Zostření panchromatickým pásmem

Panchromatické pásmo zachycuje široký rozsah vlnových délek (střed a šířka jsou v tabulce v kroku 1) s dvakrát jemnějším pixelem. Metoda HPM (high-pass modulation) vynásobí každé převzorkované pásmo poměrem pan / pan rozmazané na rozlišení MS. Pan nejdřív sesadíme s průměrem pásem 1–4 stejně jako v kroku 3.

Parametry, které student mění:

- `CROP = (slice(1000, 1400), slice(1400, 1850))`: výřez v pixelech MS (řádky, sloupce)

**Úkol 5.** Kolikrát jemnější je panchromatický pixel a o kolik se zvýšil podíl jemných detailů v červeném pásmu? Proč je NDVI ze zostřených pásem stejné jako z nezostřených (rozdíl je na úrovni zaokrouhlení)? Proč zostření nemění průměrnou odrazivost? Pan zahrnuje i část NIR: je zostřené červené pásmo u vegetace stejně věrohodné jako zostřené zelené? Uvaž, jak vegetace vypadá v pan a jak v červeném pásmu.

**Rozšíření (nepovinné).** Z tabulky GSD spočítej, v jaké výšce by měl termální pixel 10 cm a jaký by pak měly pixel multispektrální pásma. Kolikrát víc letových linií by to při stejném bočním překryvu znamenalo proti letu v 97 m? Ověř to v notebooku Plánovač letu dronu.

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Snímky: MicaSense, Inc. (2017–2023). *imageprocessing* (licence MIT), https://github.com/micasense/imageprocessing, soubory data/ALTUM-PT/IMG_0000_*.tif a IMG_0010_*.tif a micasense/image.py (radiance, vinětace, termální pásmo).
- MicaSense: Altum and Altum-PT Thermal Band – FAQ, https://support.micasense.com/hc/en-us/articles/360036377834 (setiny kelvinu, emisivita 1,0, přesnost ±5 K).
- Zitová, B., Flusser, J. (2003). Image registration methods: a survey. *Image and Vision Computing* 21(11), 977–1000.
- Kuglin, C. D., Hines, D. C. (1975). The phase correlation image alignment method. *Proceedings of the IEEE International Conference on Cybernetics and Society*, 163–165.
- Vivone, G. a kol. (2015). A critical comparison among pansharpening algorithms. *IEEE Transactions on Geoscience and Remote Sensing* 53(5), 2565–2586.
- Norman, J. M., Becker, F. (1995). Terminology in thermal infrared remote sensing of natural surfaces. *Agricultural and Forest Meteorology* 77, 153–166.
- Carlson, T. N., Gillies, R. R., Perry, E. M. (1994). A method to make use of thermal infrared temperature and NDVI measurements to infer surface soil water content and fractional vegetation cover. *Remote Sensing Reviews* 9, 161–173.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
