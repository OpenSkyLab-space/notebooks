# Lidar a fotogrammetrie v lese: mračna bodů a modely ČÚZK

Popis notebooku k vizuálu [LiDAR a fotogrammetrie v porostu](https://openskylab.space/edu_viz_lidar_canopy.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/lidar_canopy_cs.ipynb) · verze 1.0 · asi 50 min · šest úkolů

## O čem notebook je

Vizuál ukazuje, proč laserový pulz najde terén i pod korunami, zatímco fotogrammetrie vidí jen povrch. Tady to ověříš na skutečných datech ČÚZK z Roztockého háje u Suchdola: body terénu a povrchu z leteckého laserového skenování a povrch z obrazové korelace leteckých snímků.

## Cíl

Načíst a prohlédnout mračna bodů LAZ, zjistit, z kolikátého odrazu pocházejí body terénu v lese a na volné ploše, spočítat model výšky porostu CHM = DSM − DTM z lidaru i z fotogrammetrie, porovnat je v profilu, najít vrcholy stromů a vysvětlit rozdíly.

## Data

ČÚZK: DMR 5G (body terénu z leteckého laserového skenování, LAZ) a DMP 1G (body povrchu, LAZ) pro mapový list Kralupy nad Vltavou 7-7, rastry DMR 5G, DMP 1G a DMP OK (obrazová korelace) z obrazové služby ČÚZK; vše v S-JTSK (EPSG:5514), výšky Bpv. Data ČÚZK jsou otevřená (CC BY 4.0).

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a mračna bodů

Nainstaluje knihovny, které Colab nemá předem (`laspy`, `rasterio`), a stáhne data.

Parametry, které student mění:

- `SHEET = "KRAV77"`: mapový list SM5 (názvy listů jsou v atomové službě ČÚZK)
- `X0, Y0, X1, Y1 = -744800, -1036000, -743800, -1035300`: výřez v S-JTSK (m), Roztocký háj a Tiché údolí

**Úkol 1.** Kolik bodů na m² mají DMR 5G a DMP 1G? Skener jich na zem poslal mnohem víc: proč ČÚZK zveřejňuje jen vybrané (klíčové) body a podle čeho je asi vybíral? Ve kterém měsíci se skenovalo? Jak ovlivní listí, kolik pulzů projde až na zem, a proč se lidar pro model terénu ideálně létá mimo vegetační sezónu?

### 2. Z kolikátého odrazu je terén?

Každý bod nese číslo odrazu (return number) a počet odrazů pulzu (number of returns). Bod terénu s číslem odrazu 2 a víc znamená, že část pulzu se předtím odrazila od koruny a zbytek prošel mezerou až na zem. Les od volné plochy rozlišíme podle výšky povrchu nad terénem z rastrů DMP 1G a DMR 5G.

Parametry, které student mění:

- `RES = 2.0`: velikost pixelu rastrů (m)
- `FOREST_H = 5`: od jaké výšky povrchu nad terénem je to „les“ (m)

**Úkol 2.** Jaký podíl bodů terénu v lese pochází z 2. a dalšího odrazu a jaký na volné ploše? Proč není na volné ploše nula? Co by se stalo s modelem terénu pod lesem, kdyby skener zaznamenával jen první odraz? A proč fotogrammetrie (SfM) terén pod zapojeným porostem nenajde vůbec?

### 3. CHM z lidaru a z fotogrammetrie

CHM = DSM − DTM. DTM bereme vždy z lidaru (DMR 5G). DSM jednou z lidaru (DMP 1G), jednou z obrazové korelace leteckých měřických snímků (DMP OK), které ČÚZK pořídil později (letecké měřické snímkování probíhá obvykle od jara do léta). Obrazová korelace je stejný princip jako fotogrammetrie z dronu.

**Úkol 3.** Který CHM ukazuje v lese vyšší porost a o kolik (medián, 95. percentil)? Najdi aspoň tři důvody: roky mezi snímkováním, listí v létě a v době skenování, jak obrazová korelace „vyhlazuje“ mezery mezi korunami. Kde v mapě jsou rozdíly největší?

### 4. Profil porostem

Body obou mračen v pásu podél zvolené čáry a profily tří povrchů.

Parametry, které student mění:

- `A_XY = (-744300, -1035950)`: začátek profilu (S-JTSK, m)
- `B_XY = (-744300, -1035350)`: konec profilu
- `HALF_W = 5`: poloviční šířka pásu (m)

**Úkol 4.** Kde v profilu je les a kde volná plocha? Jak se liší DSM z lidaru a z fotogrammetrie na okraji lesa a v mezerách mezi korunami? Které body terénu jsou v lese z 2. a dalšího odrazu? Přesuň profil jinam (třeba přes údolí nebo budovy) a popiš, co vidíš.

### 5. Vrcholy stromů

Vrchol stromu hledáme jako lokální maximum CHM v okně dané velikosti, které je vyšší než zvolená mez. Použijeme fotogrammetrický DSM v plném rozlišení 0,5 m.

Parametry, které student mění:

- `WIN = 5`: velikost okna pro lokální maximum (m)
- `MIN_H = 10`: minimální výška stromu (m)
- `SUB = (-744600, -1035900, -744300, -1035600)`: menší výřez v lese (S-JTSK, m)

**Úkol 5.** Kolik stromů na hektar najdeš s oknem 3 m, 5 m a 9 m? Které číslo je nejblíž skutečnosti, pokud mají koruny průměr kolem 8–12 m, a proč malé okno počet přeceňuje? Co by se stalo s počtem, kdybys použil CHM z lidaru s pixelem 2 m?

### 6. Co se mezi snímkováními změnilo

Rozdíl CHM z fotogrammetrie a z lidaru ukazuje růst porostu, těžbu i chyby obou metod. Přesnost udává ČÚZK jako úplnou střední chybu výšky: DMR 5G 0,18 m v odkrytém a 0,3 m v zalesněném terénu, DMP 1G 0,4 m u budov a 0,7 m u vegetace.

Parametry, které student mění:

- `CHANGE = 5`: od jakého rozdílu výšky (m) to považujeme za změnu

**Úkol 6.** Je medián rozdílu v lese větší, než vysvětlí udávaná přesnost obou modelů? Kolik by musel les za ta léta vyrůst a je to realistické (dohledej, jaký je typický roční výškový přírůst dospělého listnatého lesa)? Najdi v mapě místa, kde porost zmizel (těžba, polom) nebo přibyl. Proč nejde z jednoho fotogrammetrického DSM bez lidarového DTM výšku porostu vůbec spočítat?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- ČÚZK: Digitální model reliéfu České republiky 5. generace (DMR 5G), úplná střední chyba výšky 0,18 m v odkrytém a 0,3 m v zalesněném terénu; Digitální model povrchu České republiky 1. generace (DMP 1G), úplná střední chyba výšky 0,4 m u budov a 0,7 m u vegetace; Digitální model povrchu z obrazové korelace (DMP OK). https://geoportal.cuzk.gov.cz
- Stahování LAZ: atomová služba ČÚZK, https://atom.cuzk.cz/DMR5G-SJTSK/DMR5G-SJTSK.xml a https://atom.cuzk.cz/DMP1G-SJTSK/DMP1G-SJTSK.xml; rastry: https://ags.cuzk.cz/arcgis2/rest/services
- ASPRS (2019). *LAS Specification 1.4 – R15* (třídy bodů, čísla odrazů, čas GPS).
- White, J. C., Wulder, M. A., Vastaranta, M. a kol. (2013). The utility of image-based point clouds for forest inventory: A comparison with airborne laser scanning. *Forests* 4(3), 518–536.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
