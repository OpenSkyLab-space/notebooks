# Kdy letět s termokamerou: teplota povrchů ze skutečného počasí

Popis notebooku k vizuálu [Kdy letět s termokamerou](https://openskylab.space/edu_viz_thermal_timing.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/thermal_timing_cs.ipynb) · verze 1.0 · asi 45 min · šest úkolů

## O čem notebook je

Vizuál ukazuje, jak se voda, louka, asfalt, les a fotovoltaika během dne ohřívají a chladnou a kdy se dva povrchy v termosnímku slijí. Tady stejný typ modelu (energetická bilance povrchu s vedením tepla do hloubky) poženeš skutečným hodinovým počasím za poslední měsíce v Suchdole a hledáš nejlepší čas letu podle úlohy.

## Cíl

Spočítat denní chod teploty povrchů ze skutečného záření, teploty, vlhkosti, oblačnosti a větru, najít časy, kdy se dva povrchy teplotně překříží, porovnat jasný a zatažený den, ukázat vliv větru a emisivity nastavené v kameře a najít hodiny vhodné pro kontrolu fotovoltaiky.

## Data

hodinová teplota a vlhkost vzduchu, globální záření na vodorovnou i skloněnou plochu, oblačnost, vítr v 10 m a teplota povrchu půdy z Open-Meteo pro kampus v Suchdole, co služba vrátí za posledních 92 dní, obvykle dva až tři měsíce (model počasí, ne měření na místě); tepelné vlastnosti materiálů z literatury.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a skutečné počasí

Načte knihovny a stáhne data.

Parametry, které student mění:

- `LAT, LON = 50.130, 14.373`: místo (kampus v Suchdole)
- `TILT, AZ = 35, 0`: sklon a azimut fotovoltaiky (°; azimut 0 = jih, −90 = východ, 90 = západ)

### 2. Model povrchu a jeden jasný den

Pro každý povrch se každou minutu řeší energetická bilance **Rn = H + LE + G**:

- Rn: pohlcené sluneční záření (1 − albedo) · S plus dlouhovlnná bilance ε (L↓ − σ T⁴). L↓ z oblohy je z teploty a vlhkosti vzduchu (Brutsaert 1975) a z oblačnosti (Crawford a Duchon 1999).
- H: citelné teplo do vzduchu h · (T − Tₐ), h = 5,7 + 3,8 U, kde U je vítr ve 2 m (z větru v 10 m logaritmickým profilem, ×0,75).
- LE: výpar ρ L (q*(T) − qₐ) / (rₐ + r_s); odpor průduchů r_s je u louky 70 s/m, u lesa 100 s/m, voda se vypařuje volně, asfalt a panel vůbec.
- G: teplo do hloubky. Asfalt a půda mají 12 vrstev do 1 m, rybník je promíchaná vrstva vody 1 m, koruny lesa a FV panel jsou tenká vrstva bez vedení do země.

Sluneční záření, teplota, vlhkost, oblačnost a vítr jsou skutečné hodinové hodnoty z Open-Meteo. Model běží od začátku období, prvních 14 dní slouží k rozběhu.

Parametry, které student mění:

- `DAY = SUNNY`: den, např. "2026-09-10"; výchozí je nejslunečnější den
- `A, B = "voda", "louka"`: dvojice povrchů

**Úkol 1.** Odečti časy obou překřížení vody a louky. Proč je voda v noci teplejší než louka a v poledne chladnější? Porovnej modelovanou louku s teplotou povrchu půdy z Open-Meteo (tečkovaně): kde se liší nejvíc a čím to může být (je to taky model, ne měření)? Zkus dvojici asfalt × les.

### 3. Jasno, nebo zataženo?

Porovnáme nejslunečnější a nejzataženější den ze stažených dat. Amplituda je rozdíl mezi denním maximem a minimem teploty povrchu.

Parametry, které student mění:

- `DAYS = [SUNNY, CLOUDY]`: dny k porovnání (můžeš přidat třetí, např. "2026-09-20")

**Úkol 2.** O kolik se v zatažený den zmenšila amplituda asfaltu a vody? Co se stalo s rozdílem voda − louka v noci? Vysvětli roli slunečního záření ve dne a dlouhovlnného záření oblačnosti v noci.

### 4. Kalendář kontrastu: kdy letět

Pro každý den a hodinu spočítáme rozdíl teplot dvojice povrchů. Bílá místa jsou překřížení, kdy se povrchy v termosnímku slijí.

Parametry, které student mění:

- `A, B = "voda", "louka"`: dvojice povrchů
- `MIN_DT = 3`: kontrast, který ještě v termosnímku spolehlivě rozlišíš (K)

**Úkol 3.** Ve kterých hodinách je kontrast vody a louky spolehlivě velký a ve kterých se povrchy slévají? Jak se překřížení posouvají od léta k podzimu a proč? Hledáš vlhká místa v louce (dvojice louka × voda): kdy bys letěl a proč spíš ráno než v poledne?

### 5. Vítr

Stejné počasí spočítáme ještě jednou se slabším a silnějším větrem (vítr vynásobíme). Ostatní veličiny zůstanou skutečné.

Parametry, které student mění:

- `FACTORS = [0.5, 1, 2, 4]`: násobky skutečného větru
- `DAY_W = SUNNY`: den

**Úkol 4.** Jak se se silnějším větrem změní polední maximum asfaltu, ranní minimum louky a kontrast asfalt − louka? Proč vítr kontrasty v termosnímku zmenšuje? Jaký limit větru bys pro termální let doporučil?

### 6. Emisivita v kameře a fotovoltaika

Kamera měří vyzařování W = ε σ T⁴ + (1 − ε) σ T_odr⁴, kde druhý člen je odražené okolí. Teplotu z něj počítá s emisivitou ε_k a odraženou teplotou T_odr, které nastavíš v kameře. Zjednodušení: počítáme v celém spektru, ne jen v pásmu 8–14 µm, a odražené okolí bereme jako oblohu.

Pro kontrolu FV elektráren se doporučuje ozáření panelu aspoň 600 W/m² (IEA PVPS). Ozáření skloněné plochy máme z Open-Meteo.

Parametry, které student mění:

- `EPS_CAM = 1.00`: emisivita nastavená v kameře (zkus 0,95 a 0,85)
- `T_REFL = 20.0`: odražená teplota nastavená v kameře (°C)
- `HOURS = ["05:00", "13:00"]`: časy snímků
- `DAY_E = SUNNY`: den
- `THRESH = 600`: minimální ozáření panelu pro kontrolu FV (W/m²)

**Úkol 5.** S emisivitou 1,00 v kameře: který povrch se od své skutečné teploty liší nejvíc a proč FV panel vypadá chladnější, než je? Nastav 0,95 a pak 0,85: který povrch je teď správně a které ne? Proč je chyba v noci jiná než v poledne (uvaž odraženou oblohu)?

**Úkol 6.** Ve kterých měsících a hodinách bylo ozáření panelů aspoň 600 W/m²? Změň v kroku 1 sklon na 60° a azimut na −90° (východ) a buňky spusť znovu: jak se okno pro kontrolu posune? Proč je kontrast vadného nebo odpojeného modulu při slabém slunci malý?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744 (dlouhovlnné záření jasné oblohy).
- Crawford, T. M., Duchon, C. E. (1999). An improved parameterization for estimating effective atmospheric emissivity. *Journal of Applied Meteorology* 38, 474–480 (vliv oblačnosti).
- Oke, T. R. (1987). *Boundary Layer Climates*, 2. vyd. Routledge (tepelná vodivost a kapacita asfaltu a půdy, albeda).
- Maes, W. H. (2025). Practical guidelines for performing UAV mapping flights with snapshot sensors. *Remote Sensing* 17(4), 606. https://doi.org/10.3390/rs17040606 (plánování mapovacích letů včetně termálních).
- IEA PVPS Task 13 (2018). *Review on Infrared and Electroluminescence Imaging for PV Field Applications*, Report IEA-PVPS T13-10:2018 (emisivita skla 0,85, ozáření ≥ 600 W/m²).
- Přestup tepla prouděním h = 5,7 + 3,8 U (McAdams), tlak nasycených par Magnusovým vzorcem (WMO-No. 8, 2018).

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
