# Švihadlo a fotony, pokročilá verze: kolik fotonů zachytí pixel Sentinelu-2 a dronu

Popis notebooku k vizuálu [Švihadlo a fotony](https://openskylab.space/edu_viz_rope_and_photons.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/rope_and_photons_pro_cs.ipynb) · verze 1.0 · asi 60 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku o fotonech. Ze skutečné scény Sentinel-2 nad Roztoky spočítáš, kolik fotonů dopadne za dobu přeletu jednoho pixelu na detektor v pásmech B02, B04, B08 a B11, jaký z toho plyne odstup signálu od šumu a jak ho mění velikost dalekohledu. Pak stejný výpočet uděláš pro kameru na dronu a zjistíš, proč malý objektiv nízko nad zemí sbírá podobně mnoho fotonů jako dalekohled na dráze.

## Cíl

Z odrazivosti L1C spočítat zář a počet fotoelektronů v pixelu, odvodit odstup signálu od šumu √N, nasimulovat fotonový šum pro různé pupily, porovnat družici s dronem přes součin A·Ω a ověřit, jak SNR roste se slučováním pixelů a jak se má ke kvantování.

## Data

Copernicus Sentinel-2B L1C `S2B_MSIL1C_20240721T100559_N0510_R022_T33UVR_20240721T121133` (21. 7. 2024) z veřejného archivu Google Cloud: metadata MTD_MSIL1C a MTD_TL a výřezy 4 × 4 km pásem B02, B04, B08 a B11 kolem Roztok, asi 2 MB. Parametry přístroje (pupila 150 mm, výška dráhy 786 km) jsou převzaté z popisu MSI. Účinnost ETA a parametry dronu jsou orientační odhady: skutečný přístroj má složitější konstrukci (typy detektorů, u některých pásem sčítání více řádků), takže čísla ukazují řád, ne přesné SNR Sentinelu-2.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a scéna Sentinel-2

Z odrazivosti nad atmosférou ρ (TOA) dostaneme zář L = ρ · E0 · U · cos(θs) / π, kde E0 je sluneční ozáření v pásmu, U oprava na vzdálenost Země–Slunce a θs zenitový úhel Slunce. Všechny tři hodnoty jsou v metadatech scény.

Parametry, které student mění:

- `LON, LAT, HALF = 14.375, 50.145, 2000`: střed výřezu (okolí Roztok) a poloviční šířka (m)

### 2. Fotonový rozpočet pixelu

Dalekohled s plochou pupily A vidí jeden pixel pod prostorovým úhlem Ω = (pixel / výška)². Energie, která za dobu t přijde z pixelu, je L · A · Ω · Δλ · t; vydělená energií fotonu h·c/λ a vynásobená účinností ETA dává počet fotoelektronů N. Za t bereme dobu, za kterou stopa družice přejede jeden pixel. Příchod fotonů je náhodný (Poissonův), proto je šum √N a odstup signálu od šumu SNR = √N. Šum detektoru a elektroniky tu zanedbáváme.

Parametry, které student mění:

- `D_PUPIL = 0.150`: průměr vstupní pupily dalekohledu (m); MSI má ekvivalent 150 mm
- `H_ORBIT = 786e3`: výška dráhy (m)
- `ETA = 0.3`: podíl fotonů, které se změní v elektron (propustnost optiky × kvantová účinnost), odhad

**Úkol 1.** Proč má B11 nejvíc fotoelektronů, i když je zář v krátkovlnném infračerveném pásmu nižší než v blízkém infračerveném? Rozlož rozdíl mezi B04 a B11 na příspěvky šířky pásma, vlnové délky (energie fotonu), velikosti pixelu a doby přeletu.

**Úkol 2.** Porovnej SNR tmavých (2 %) a světlých (98 %) pixelů v B04. Které povrchy ve výřezu to jsou? Změň `ETA` na 0,6 a pak na 0,15: jak se změní SNR a proč jen s odmocninou?

### 3. Jak vypadá fotonový šum

Nasimulujeme snímek B04 tak, jak by ho zachytily pupily různé velikosti: místo očekávaného počtu N vylosujeme pro každý pixel náhodné číslo z Poissonova rozdělení. Obraz terénu je ve všech třech stejný, mění se jen šum.

Parametry, které student mění:

- `DIAMETERS = [0.150, 0.050, 0.015]`: průměry pupily k porovnání (m)

**Úkol 3.** Pupila se zmenší třikrát (150 → 50 mm). Kolikrát klesne N a kolikrát SNR? Při jakém průměru pupily by SNR mediánu v B04 kleslo pod 10? Ověř změnou `DIAMETERS`.

### 4. Dron proti družici

Pro dron počítáme se stejným pásmem B04 a stejnou září, protože scéna je stejná. Doba expozice je tu nejdelší možná, aby se obraz za letu nerozmazal o víc než jeden pixel (pixel / rychlost). Parametry dronu jsou orientační, odpovídají malé multispektrální kameře.

Parametry, které student mění:

- `DRONE = dict(D=0.003, H=100.0, gsd=0.05, speed=8.0)`: dron: pupila (m), výška letu (m), pixel na zemi (m), rychlost (m/s), orientačně

**Úkol 4.** Pupila dronu má asi 2500krát menší plochu než pupila MSI, a přesto je počet fotoelektronů srovnatelný, dokonce vyšší. Vysvětli to pomocí součinu A·Ω a doby expozice. Co se stane s N, když dron poletí dvakrát výš se stejnou kamerou (pixel se zvětší dvakrát)?

### 5. Slučování pixelů a kvantování

Sloučením n × n pixelů se sečtou fotoelektrony, signál roste s n², šum s n, SNR tedy s n. Na konci porovnáme fotonový šum s krokem kvantování: hodnota v L1C je celé číslo (DN) a jeden krok DN odpovídá určitému počtu elektronů.

**Úkol 5.** Kolikrát vzroste SNR, když 10m pixely sloučíš do 60 m? Co tím ztratíš? Je kvantování L1C pro přesnost hodnot důležité, nebo převládá fotonový šum? Co by se stalo, kdyby se odrazivost ukládala jen s 8 bity (krok 1/255)?

**Rozšíření (nepovinné).** Změň `H_ORBIT` na 500 km a `D_PUPIL` tak, aby SNR zůstalo stejné. Porovnej výsledek s menšími družicemi pro pozorování Země, o kterých něco víš.

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Copernicus Sentinel-2 data 2024, ESA; L1C z veřejného archivu Google Cloud (`gcp-public-data-sentinel-2`). Licence: [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice), volné užití s uvedením zdroje.
- ESA: *Sentinel-2 MSI Instrument*, technický průvodce (https://sentinel.esa.int/web/sentinel/technical-guides/sentinel-2-msi/msi-instrument).
- The multispectral instrument of the Sentinel2 program. *Proc. SPIE* 10566, 105660H (ICSO 2008). https://doi.org/10.1117/12.2308278
- Konstanty h a c: v SI od roku 2019 přesně definované hodnoty, převzaté z `scipy.constants`.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
