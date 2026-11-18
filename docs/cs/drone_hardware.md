# Dron jako měřicí přístroj: časování, poloha a úhly na skutečném letu

Popis notebooku k laboratoři [Dron jako měřicí přístroj](https://openskylab.space/edu_viz_drone_hardware.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/drone_hardware_cs.ipynb) · verze 1.0 · asi 45 min · pět úkolů

## O čem notebook je

Laboratoř ukazuje, že dron je soustava přístrojů: přijímač GNSS, barometr, inerciální jednotka, gimbal a kamera, které měří každý trochu jinde a v trochu jiném okamžiku. Tady to ověříš na skutečném mapovacím letu nad Bahnami (DJI Mavic 2 Pro, bez RTK). Ke každému snímku máš polohu a výšky zapsané dronem, natočení těla a kamery a střed kamery spočtený z fotogrammetrie (SfM). Z jejich rozdílů zjistíš, jak rychle dron letěl, jak se naklání, o kolik se zpožďuje zápis polohy a jak moc se obraz rozmaže.

## Cíl

Z poloh a časů snímků určit řady, rychlost a rozestup snímků a najít chybějící snímky, porovnat náklon těla a kamery v řadách tam a zpět, oddělit zpoždění zápisu polohy od ramene páky antény, spočítat rozmazání pohybem a porovnat výšku z GNSS a z barometru.

## Data

Tabulka metadat 253 snímků letu nad Bahnami 31. 10. 2025 (EXIF a XMP od DJI) se středy kamer ze SfM, v místních souřadnicích (OpenSkyLab, CC BY 4.0).

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Data a trasa letu

Tabulka má jeden řádek na snímek. Polohy jsou v místní rovině v metrech (východ, sever), výšky nad místem vzletu. Mapovací let (`grid`) rozdělíme na řady podle skoků v poloze na sever a každé řadě určíme směr.

### 2. Rychlost, rozestup a chybějící snímky

Dron snímá v pravidelném intervalu. Rychlost v každé řadě je sklon přímky proložené polohou na východ v závislosti na čase. Čas je v EXIF jen na celé sekundy, proto přímka a ne rozdíly sousedních snímků.

**Úkol 1.** Jaká je rychlost, interval a rozestup snímků? Liší se řady na východ a na západ? Které snímky chybějí a dá se z rozestupů poznat, kde v řadě je díra?

### 3. Náklon těla a kamery

Multikoptéra letí dopředu tak, že se nakloní: tah rotorů pak má vodorovnou složku. Gimbal má náklon těla vyrovnat, aby kamera mířila kolmo dolů.

**Úkol 2.** Kam míří nos dronu v řadách na východ a na západ? Jaký je náklon těla v obou směrech a proč má opačné znaménko? Udržel gimbal kameru kolmo dolů? Proč náklon na východ a na západ není stejně velký?

### 4. Zpoždění zápisu polohy a rameno páky

Střed kamery ze SfM je určený ze snímků, poloha v EXIF z GNSS. Když se poloha zapíše o dt později než expozice, je posunutá o v · dt ve směru letu, takže v řadách tam a zpět má opačné znaménko. Anténa posunutá vůči kameře (rameno páky) dá posun, který se se směrem letu nemění, protože nos dronu míří stále stejně. Pozor: SfM bylo na polohy GNSS přiloženo podobnostní transformací, takže stálý posun celého bloku tím zmizel a z dat ho určit nejde.

Parametry, které student mění:

- `SPEED = z_viz("speed", 8.0)`: rychlost letu v laboratoři (m/s)
- `DT = z_viz("dt", 0.24)`: zpoždění zápisu polohy v laboratoři (s)
- `LEVER_X = z_viz("lever_x", 0.0)`: anténa před kamerou v laboratoři (m)
- `LEVER_Z = z_viz("lever_z", 0.2)`: anténa nad kamerou v laboratoři (m)

**Úkol 3.** Jaké zpoždění dt vychází z dat a jak se shoduje s laboratoří? Proč stálý posun vychází skoro nulový, i kdyby anténa byla před kamerou? Jak velký posun způsobí náklon těla s anténou 0,2 m nad kamerou a dá se odlišit od zpoždění?

### 5. Rozmazání pohybem a závěrka

Během expozice se dron posune o v · t_exp. Když je to víc než asi polovina pixelu na zemi (GSD), snímek se viditelně rozmaže. Kamera L1D-20c nemá mechanickou závěrku: čip se vyčítá po řádcích (rolling shutter) a během vyčtení se dron posune o v · t_read.

Parametry, které student mění:

- `T_EXP = z_viz("t_exp", 0.002)`: expoziční čas v laboratoři (s)
- `T_READ = z_viz("t_read", 0.03)`: doba vyčtení čipu v laboratoři (s), 0 = mechanická závěrka

**Úkol 4.** Jaké expoziční časy kamera použila a jak velké je rozmazání v pixelech? Jaký nejdelší čas by při této rychlosti a výšce dal rozmazání pod 0,5 px? Co bys změnil v plánu letu, kdyby bylo pod mrakem tmavěji?

### 6. Výška z GNSS a z barometru

Dron měří výšku barometrem (rozdíl tlaku proti místu vzletu) a přijímačem GNSS. `h_gnss` je absolutní výška z XMP posunutá tak, aby šla porovnat s `h_baro`.

**Úkol 5.** Který senzor drží výšku stabilněji a proč? Má rozdíl h_gnss − h_baro trend v čase? Čím se může barometr během letu posunout?

**Rozšíření (nepovinné).** Doplňkové snímky (`set == 'extra'`) mají jiný náklon kamery a výšku. Které z nich se v SfM neregistrovaly a proč?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Data letu: OpenSkyLab (2026), metadata letu Bahna 31. 10. 2025 odvozená ze snímků a z rekonstrukce SfM, licence CC BY 4.0, https://github.com/OpenSkyLab-space/notebooks/tree/main/data
- Pix4D: *How to correct for the rolling shutter effect* a *Time offset between GNSS and camera* (dokumentace Pix4Dmapper).
- Vautherin, J., Rutishauser, S., Schneider-Zapp, K., Choi, H. F., Chovancova, V., Glass, A., Strecha, C. (2016). Photogrammetric accuracy and modeling of rolling shutter cameras. *ISPRS Annals* III-3, 139–146.
- Groves, P. D. (2013). *Principles of GNSS, Inertial, and Multisensor Integrated Navigation Systems*, 2. vyd. Artech House (rameno páky, synchronizace senzorů).

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
