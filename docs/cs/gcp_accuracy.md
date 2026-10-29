# Vlícovací a kontrolní body: přesnost transformace na skutečném bodovém poli

Popis notebooku k vizuálu [Vlícovací body a přesnost](https://openskylab.space/edu_viz_gcp_accuracy.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/gcp_accuracy_cs.ipynb) · verze 1.0 · asi 45 min · čtyři úkolů

## O čem notebook je

Vizuál simuluje, jak rozmístění vlícovacích bodů a způsob georeferencování ovlivní přesnost mapy z dronu. Tady stejné principy ověříš na skutečných bodech bodového pole ČÚZK: každý bod má souřadnice z GNSS v ETRS89 a zároveň souřadnice v S-JTSK a nadmořskou výšku v Bpv. Převod mezi systémy odhadneš z několika vlícovacích bodů a jeho přesnost změříš na ostatních, nezávislých kontrolních bodech. Je to stejná úloha jako georeferencování bloku snímků, jen na území desítek kilometrů.

## Cíl

Odhadnout podobnostní (Helmertovu) transformaci z vlícovacích bodů, porovnat odchylky na vlícovacích a kontrolních bodech pro různé rozmístění, převést elipsoidické výšky na Bpv, posoudit, kolik kontrolních bodů je potřeba, a ukázat, kdy složitější transformace škodí.

## Data

trigonometrické a zhušťovací body ČÚZK v okolí Prahy se souřadnicemi S-JTSK, výškou Bpv a souřadnicemi ETRS89 (B, L, elipsoidická výška) ze statického měření GNSS, služba BodovaPole (vrstva 2).

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a body bodového pole

Nainstaluje knihovny, které Colab nemá předem (`pyproj`), a stáhne data.

Parametry, které student mění:

- `CX, CY = -742000, -1045000`: střed území v S-JTSK (EPSG:5514, m), Praha
- `HALF = 30000`: polovina strany území (m)

### 2. Helmertova transformace z vlícovacích bodů

Podobnostní transformace má 4 parametry (posun x, y, otočení, měřítko): x' = a·x − b·y + tₓ, y' = b·x + a·y + t_y. Odhadneme ji metodou nejmenších čtverců z vlícovacích bodů a pak ji použijeme na všechny body. Odchylka na vlícovacím bodě říká jen, jak dobře se transformace k těmto bodům přizpůsobila. Přesnost ukážou až kontrolní body, které do výpočtu nevstoupily. RMSE_H = √(průměr(Δx² + Δy²)).

Pozor: S-JTSK má vlastní deformace a měřítko Křovákova zobrazení se mění se zeměpisnou šířkou, takže ani nejlepší podobnostní transformace na takovém území není dokonalá. ČÚZK proto pro převod používá transformaci s opravnou sítí. Pro nás je to výhoda: je tu skutečná, předem neznámá chyba, kterou musí odhalit kontrolní body.

Parametry, které student mění:

- `LAYOUT = "shluk v rohu"`: jedno z rozmístění výše

**Úkol 1.** Pro „shluk v rohu“ porovnej RMSE_H na vlícovacích a na kontrolních bodech. Proč jsou odchylky na vlícovacích bodech tak malé a proč z nich nelze vykázat přesnost? Kde na mapě rostou odchylky kontrolních bodů? Pak zvol „rohy + střed“: proč je teď odchylka na vlícovacích bodech větší než na kontrolních?

### 3. Porovnání rozmístění, polohy i výšky

GNSS dává elipsoidickou výšku h, mapy v ČR používají nadmořskou (normální) výšku v Bpv: H = h − ζ, kde ζ je výšková anomálie (v okolí Prahy kolem 44–46 m). Když z vlícovacích bodů odhadneme ζ jako konstantu, nebo jako rovinu, dostaneme výšky na kontrolních bodech. RMSE_V = √(průměr ΔH²).

Z jediného vlícovacího bodu lze polohově odhadnout jen posun. UTM a S-JTSK jsou ale vůči sobě pootočené a mají jiné měřítko, proto tu chyba vyjde v kilometrech. U bloku snímků z RTK nebo PPK je natočení i měřítko dané už polohami snímků.

**Úkol 2.** Které rozmístění je nejlepší polohově a které výškově? Proč body „jen podél linie“ polohu ještě drží, ale rovinu výšek (náklon) neurčí? Co dělá jediný bod ve středu a k čemu se přesto hodí, když máš RTK nebo PPK? Proč by záměna elipsoidické a nadmořské výšky byla v ČR chyba desítek metrů?

### 4. Kolik kontrolních bodů?

Přesnost odhadujeme z omezeného počtu kontrolních bodů, takže i samotné RMSE má nejistotu. Vybereme náhodně 12 nebo 30 kontrolních bodů mnohokrát po sobě a podíváme se, jak moc se odhad mění.

Parametry, které student mění:

- `LAYOUT_N = "10 rovnoměrně"`: rozmístění vlícovacích bodů
- `COUNTS = [5, 12, 30]`: počty kontrolních bodů
- `DRAWS = 2000`: počet náhodných výběrů

**Úkol 3.** Jak široké je rozmezí odhadu RMSE_H (5. až 95. percentil) s 5, 12 a 30 kontrolními body? Proč ASPRS požaduje aspoň 30 kontrolních bodů? Proč musí být kontrolní body rozmístěné po celém území a ne třeba jen u silnice?

### 5. Složitější transformace a málo bodů

Helmertova transformace má 4 parametry, afinní 6 (navíc dvě různá měřítka a zkosení) a polynom 2. stupně 12. Víc parametrů se k vlícovacím bodům přizpůsobí lépe. Jestli to pomůže i na kontrolních bodech, záleží na tom, jestli skutečný rozdíl mezi systémy takový tvar má, a na tom, kolik je vlícovacích bodů. Vlícovací body losujeme náhodně a díváme se na medián i na 90. percentil (nepříznivé losování).

Parametry, které student mění:

- `N_GCP = [3, 4, 6, 8, 12, 20, 40]`: počty vlícovacích bodů
- `REPEAT = 200`: počet losování pro každý počet

**Úkol 4.** Která transformace je nejlepší se 3–4 body a která se 40 body? Proč je afinní transformace při všech počtech o něco horší než Helmertova, kdežto polynom 2. stupně je od 8 bodů výrazně lepší? Co to říká o tvaru skutečného rozdílu mezi S-JTSK a UTM? Porovnej 90. percentil polynomu se 6 body s mediánem: jak riskantní je model, který má skoro tolik parametrů jako podmínek? Podle čeho bys v praxi volil model transformace nebo počet parametrů autokalibrace kamery?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Bodová pole: © ČÚZK, služba https://ags.cuzk.cz/arcgis/rest/services/BodovaPole/MapServer (CC BY 4.0); geodetické údaje bodů na https://geoportal.cuzk.gov.cz
- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 1.0 (RMSE_H, RMSE_V, nejméně 30 kontrolních bodů).
- Sanz-Ablanedo, E., Chandler, J. H., Rodríguez-Pérez, J. R., Ordóñez, C. (2018). Accuracy of Unmanned Aerial Vehicle (UAV) and SfM Photogrammetry Survey as a Function of the Number and Location of Ground Control Points Used. *Remote Sensing* 10(10), 1606.
- Hofmann-Wellenhof, B., Lichtenegger, H., Wasle, E. (2008). *GNSS – Global Navigation Satellite Systems*. Springer (elipsoidická a normální výška, výšková anomálie).

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
