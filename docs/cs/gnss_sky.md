# GNSS pod oblohou: skutečné družice, DOP, terén a výška v Bpv

Popis notebooku k vizuálu [GNSS pod oblohou](https://openskylab.space/edu_viz_gnss_sky.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/gnss_sky_cs.ipynb) · verze 1.0 · asi 50 min · pět úkolů

## O čem notebook je

Vizuál ukazuje, jak počet a rozložení družic určují DOP, co udělají překážky a elevační maska a proč je výška z GNSS méně přesná než poloha. Tady spočítáš polohy skutečných družic GPS, Galileo, GLONASS a BeiDou z vysílaných efemerid, skutečný horizont v údolí Vltavy z modelu terénu ČÚZK a převod elipsoidické výšky na výšku v Bpv z bodů bodového pole.

## Cíl

Nakreslit skutečnou oblohu GNSS nad Suchdolem, spočítat HDOP, VDOP a PDOP během dne, posoudit vliv lesa a hlubokého údolí, najít nejbližší referenční stanici CZEPOS a převést výšku z RTK do Bpv.

## Data

Vysílané efemeridy družic GPS, Galileo, GLONASS a BeiDou za jeden den (soubor RINEX navigačních zpráv sloučený IGS, archiv BKG, asi 1,3 MB); DMR 5G (ČÚZK) pro horizont v údolí; stanice sítě CZEPOS a zhušťovací body bodového pole s výškou v Bpv i elipsoidickou výškou ETRS89 ze služby ČÚZK BodovaPole.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a dráhy družic

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

Parametry, které student mění:

- `DAY = (datetime.now(timezone.utc) - timedelta(days=1)).date()`: den (UTC), výchozí je včerejšek; zkus třeba date(2026, 9, 1)

### 2. Z efemeridy poloha družice

Každá družice vysílá svou efemeridu: GPS, Galileo a BeiDou keplerovské prvky dráhy s opravami (velká poloosa, výstřednost, sklon, délka uzlu, argument šířky a jejich změny), GLONASS polohu, rychlost a zrychlení v jednom okamžiku, ze kterých se dráha dopočítá numerickou integrací. Přijímač z nich počítá polohu družice a z ní svou polohu. Efemerida platí jen několik hodin kolem svého referenčního času, proto se vysílají nové: GPS zhruba každé 2 h, BeiDou každou hodinu, GLONASS každých 30 min, Galileo i častěji. Výpočet podle rozhraní GPS (IS-GPS-200) a GLONASS (ICD GLONASS) dává polohu v souřadnicích pevně spojených se Zemí (ECEF).

Parametry, které student mění:

- `HOUR = 12`: hodina kontroly (UTC)
- `RANK = 1`: se kterou další efemeridou porovnat (1 = sousední, 3 = o tři dál)
- `LAT, LON = 50.130, 14.373`: místo (kampus v Suchdole)
- `T_SKY = T0 + timedelta(hours=12)`: čas obrázku oblohy (UTC)
- `mask = 10`: elevační maska (°)

**Úkol 1.** Jak daleko od středu Země obíhají družice jednotlivých systémů? Proč má BeiDou v tabulce i družice daleko výš (geostacionární a na šikmých geosynchronních drahách)? O kolik metrů se liší poloha téže družice ze dvou sousedních efemerid? Nastav `RANK = 3` a pak 6 a sleduj stáří porovnávané efemeridy i rozdíl polohy. Proč je u GPS při stejném `RANK` porovnávaná efemerida mnohem starší než u Galilea? Jak roste rozdíl se stářím a proč roste u GLONASS rychleji než u GPS (vysílaný stav a integrace, nebo dráhové prvky s opravami)? Proč se efemeridy musí vysílat stále znovu?

### 3. DOP během dne

DOP spočítáme z geometrie: každá družice dá řádek matice G s jednotkovým vektorem směru (východ, sever, nahoru) a jedničkou pro hodiny přijímače (každý systém má vlastní posun hodin). Q = (GᵀG)⁻¹, HDOP = √(Q_EE + Q_NN), VDOP = √Q_UU, PDOP = √(Q_EE + Q_NN + Q_UU).

**Úkol 2.** Proč je VDOP po celý den větší než HDOP? Vysvětli to tím, kde družice na obloze jsou a kde být nemohou. Kolik družic vidí přijímač se čtyřmi systémy a kolik jen s GPS, a jak se to projeví na PDOP? Nastav masku 20° a pak 5°.

### 4. Les na jihu, nebo na severu?

Okraj lesa zakryje oblohu do výšky asi 35° na jedné straně. Dráhy GPS (sklon 55°) a Galilea (56°) nevystoupí nad 55–56° zeměpisné šířky, a proto ve střední Evropě zůstává na severní obloze ve středních výškách místo bez družic. Nízko nad severním obzorem ale vidíme družice, které letí „za pólem“. Která strana lesa vadí víc, proto není samozřejmé a záleží na výšce lesa.

Parametry, které student mění:

- `forest_el = 35`: výška okraje lesa nad obzorem (°)

**Úkol 3.** Kde je na obloze z kroku 2 „díra“ bez družic a proč? Vyzkoušej forest_el 20°, 35° a 60°: vadí víc les na severu, nebo na jihu? Platí tedy častá rada „na severu je díra, takže les na severu nevadí“? Vysvětli výsledek podle toho, ve kterých výškách nad obzorem je na severu díra a ve kterých družice „za pólem“ (pomůže obrázek z kroku 2 v jiných hodinách, změň `T_SKY`). Kde bys postavil základnovou stanici nebo měřil vlícovací bod?

### 5. Hluboké údolí: skutečný horizont z DMR 5G

Pro bod u Vltavy v Roztokách spočítáme z modelu terénu výšku horizontu v každém azimutu a podle ní vybereme viditelné družice.

Parametry, které student mění:

- `VLAT, VLON = 50.1588, 14.3985`: bod v údolí (u Vltavy v Roztokách)

**Úkol 4.** Které směry údolí zakrývá nejvíc a proč? Jak vysoko horizont sahá a je údolí z pohledu GNSS se čtyřmi systémy opravdu „hluboké“? Zkus `mask = 20` nebo bod pod skalní stěnou. Ve kterých hodinách vybraného dne (UTC) bys v údolí měřil vlícovací body? Proč model terénu nezachytí všechno, co signál ve skutečnosti blokuje nebo odráží (stromy, budovy, skalní stěny)?

### 6. Referenční stanice CZEPOS

Přesnost RTK klesá se vzdáleností od referenční stanice, protože se rozcházejí vlivy ionosféry, troposféry a drah. Výrobci obvykle udávají přesnost ve tvaru 1 cm + 1 ppm (1 mm na každý km).

### 7. Elipsoidická výška, nebo Bpv?

RTK dává výšku nad elipsoidem GRS80 (ETRS89). Mapy a projekty v Česku používají normální výšku v Bpv. Rozdíl je výšková anomálie ζ = h − H. Vezmeme zhušťovací body bodového pole v okolí, které mají obě výšky.

Parametry, které student mění:

- `half = 15000`: poloviční šířka okolí (m)

**Úkol 5.** Jaká je výšková anomálie v okolí Suchdola a o kolik se mění na 30 km? Co se stane s modelem terénu nebo s vlícovacími body, když výšky z RTK zapíšeš jako Bpv bez převodu? Proč nestačí odečíst jednu konstantu pro celou republiku a co k převodu použít (model kvazigeoidu, transformační služba ČÚZK)? Jak daleko je nejbližší stanice CZEPOS a jak velkou chybu RTK z toho čekáš?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Vysílané efemeridy: International GNSS Service (IGS), denní sloučený soubor navigačních zpráv BRDC00IGS_R, archiv BKG https://igs.bkg.bund.de/root_ftp/IGS/BRDC/ (data IGS jsou volně dostupná, s uvedením zdroje). Johnston, G., Riddell, A., Hausler, G. (2017). The International GNSS Service. In *Springer Handbook of Global Navigation Satellite Systems*, 967–982.
- Výpočet polohy družic: IS-GPS-200 (rozhraní GPS, kap. 20.3.3.4.3), Galileo OS SIS ICD, BeiDou ICD B1I (geostacionární družice), GLONASS ICD (integrace pohybu, příloha J); formát RINEX 3.05 (IGS/RTCM).
- Bodová pole a stanice CZEPOS: © ČÚZK, služba https://ags.cuzk.cz/arcgis/rest/services/BodovaPole/MapServer (CC BY 4.0).
- DMR 5G: © ČÚZK, CC BY 4.0, https://ags.cuzk.cz/arcgis2/rest/services/dmr5g/ImageServer
- Hofmann-Wellenhof, B., Lichtenegger, H., Wasle, E. (2008). *GNSS – Global Navigation Satellite Systems*. Springer (DOP, víc systémů, RTK).

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
