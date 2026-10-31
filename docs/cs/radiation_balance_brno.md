# Kam zmizí sluneční záření: bilance povrchů ze Sentinelu-2 (Brno a Jeseníky)

Popis notebooku k vizuálu [Kam zmizí záření](https://openskylab.space/edu_viz_radiation_balance.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/radiation_balance_brno_cs.ipynb) · verze 1.0 · asi 40 min · šest úkolů

## O čem notebook je

Ve vizuálu se dopadající záření dělí na odražené, pohlcené a prošlé, ρ + α + τ = 1, a podle Kirchhoffova zákona platí ε = α. Tady odrazivost změříš na skutečných pixelech Sentinelu-2 (les, louka, pole, zástavba, voda a sníh), spočítáš, kolik záření povrchy pohltí za skutečného počasí, a odhadneš, jak se ohřejí.

## Cíl

Ze skutečné odrazivosti spočítat pohltivost a albedo povrchů, použít Kirchhoffův zákon na sníh a kovy a z energetické bilance s aktuálním počasím odhadnout rovnovážnou teplotu povrchu a navrhnout chladnou střechu.

## Data

Sentinel-2 L2A (odrazivost na povrchu) z katalogu Earth Search na AWS: scéna `S2B_33UXQ_20240814_0_L2A` (14. 8. 2024, okolí Brněnské přehrady) a `S2B_33UXR_20240130_0_L2A` (30. 1. 2024, Hrubý Jeseník kolem Pradědu se sněhem); třídy pokryvu ESA WorldCover 2021; hodinové počasí pro Brno z Open-Meteo (posledních 92 dní). Stahuje se asi 15 MB.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava

Nainstaluje knihovny, které Colab nemá předem (`rasterio`), a stáhne data.

### 2. Odrazivost skutečných povrchů

Načteme výřez 3 × 3 km kolem Brněnské přehrady a pro každou třídu ESA WorldCover vezmeme medián odrazivosti čistých pixelů (bez mraků a stínů podle masky SCL). Přidáme sníh z okolí Pradědu; aby šlo o otevřený sníh bez stromů, bereme jen sněhové pixely se zelenou odrazivostí nad 0,5.

### 3. Pohltivost: α = 1 − ρ − τ

Pixel je pro družici neprůhledný: co neodrazí zpět, pohltí porost, půda nebo voda pod ním. Pro celý pixel proto platí α = 1 − ρ. (U jednoho listu je τ v NIR asi stejně velké jako ρ; uvnitř porostu se ale prošlé záření dál odráží a pohlcuje.)

**Úkol 1.** Kde les a louka pohlcují nejvíc a kde nejmíň? Proč je pro rostlinu výhodné NIR skoro nepohlcovat? Proč voda v NIR pohltí téměř vše, co do ní pronikne?

**Úkol 2.** Sníh je ve viditelném světle bílý. Jakou má pohltivost v pásmu 1,6 µm (B11)? Podle Kirchhoffova zákona je při stejné vlnové délce ε = α. Termální pásmo (10 µm) Sentinel-2 nemá, ale trend od viditelného k SWIR naznačuje, jak se sníh chová dál. Proč je sníh v termální oblasti skoro černé těleso (ε ≈ 0,99) a co z toho plyne pro měření jeho teploty termokamerou?

### 4. Albedo: kolik slunečního záření povrch odrazí celkem

Albedo je odrazivost vážená spektrem Slunce. Liang (2001) ho pro pásma Landsatu odvodil jako lineární kombinaci; použijeme odpovídající pásma Sentinelu-2 (B2, B4, B8, B11, B12), takže výsledek je přibližný.

### 5. Skutečné počasí a energetická bilance

Z Open-Meteo vezmeme nejslunečnější hodinu posledních 92 dní v Brně: globální záření S, teplotu vzduchu, rosný bod a vítr. Povrch v rovnováze (bez vypařování a vedení do země) splní

(1 − albedo) · S + ε · L↓ = ε · σ · T⁴ + h · (T − T_vzduch),

kde L↓ je dlouhovlnné záření oblohy (Brutsaert 1975, jasná obloha) a h = 5,7 + 3,8 · u je přestup tepla prouděním.

Parametry, které student mění:

- `u = row.wind_speed_10m * 0.75`: vítr u povrchu (zhruba 3/4 větru v 10 m)

**Úkol 3.** Seřaď povrchy podle pohlceného záření a podle rovnovážné teploty. Skutečný osluněný les nebo louka bývají jen o pár stupňů teplejší než vzduch. Který člen bilance v modelu chybí? Jak se toho využívá při hledání vodního stresu porostu termokamerou z dronu? Proč model u vody selže úplně?

**Úkol 4.** Změň `u` na 0,5 a pak na 6 m/s. Jak se změní rovnovážná teplota zástavby? Proč vítr teplotní rozdíly mezi povrchy zmenšuje?

### 6. Navrhni chladnou střechu

Měníme albedo a emisivitu střechy při stejném skutečném počasí. Lesklý kov odráží hodně slunce, ale v termální oblasti skoro nevyzařuje (ε ≈ 0,1); bílý nátěr odráží slunce a zároveň vyzařuje (ε ≈ 0,9).

Parametry, které student mění:

- `for eps in (0.05, 0.3, 0.6, 0.9):`: emisivity střechy

**Úkol 5.** Jakou teplotu by měla střecha s albedem zástavby z tvého výřezu a jakou bílá střecha (albedo 0,8, ε 0,9)? Proč je lesklý plech s albedem 0,6 (ε 0,05) o tolik teplejší než nátěr se stejným albedem a emisivitou 0,9? Jaké vlastnosti má mít ideální nátěr v pásmu 0,3–2,5 µm a jaké v 8–13 µm?

**Úkol 6.** Vyber z tabulky `met` jinou hodinu, třeba nejteplejší, a vlož ji místo `row` (např. `row = met.loc[met.temperature_2m.idxmax()]` pro nejteplejší hodinu). Jak se změní pořadí a teploty povrchů? Model dává sněhu teplotu nad 0 °C: proč to ve skutečnosti nejde a na co se přebytek energie spotřebuje? Proč na jaře sníh na slunci přesto neroztaje hned, i když S je vysoké?

**Rozšíření (nepovinné).** Porovnej výsledky se spolužákem, který spustil notebook pro jiné místo: liší se albedo zástavby, pole a sněhu? Vyšla nejslunečnější hodina v jiný den a s jiným S?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Copernicus Sentinel-2 data 2024, ESA, zpracováno ESA (L2A, Sen2Cor); COG kopie v registru AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje podle [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice).
- Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. Zenodo. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Počasí: Open-Meteo.com, model ICON/ECMWF podle dostupnosti (CC BY 4.0). https://open-meteo.com
- Albedo z úzkých pásem: Liang, S. (2001). Narrowband to broadband conversions of land surface albedo I: Algorithms. *Remote Sensing of Environment* 76, 213–238. https://doi.org/10.1016/S0034-4257(00)00205-4
- Dlouhovlnné záření jasné oblohy: Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744. https://doi.org/10.1029/WR011i005p00742
- Součinitel přestupu tepla prouděním h = 5,7 + 3,8 · u: McAdams, W. H. (1954). *Heat Transmission*, 3. vyd. McGraw-Hill (převzato v Duffie, J. A., Beckman, W. A., *Solar Engineering of Thermal Processes*).

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
