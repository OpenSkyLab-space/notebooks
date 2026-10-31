# Proč dron letí, pokročilá verze: výkon v dopředném letu, vítr, hustota vzduchu a vliv země

Popis notebooku k vizuálu [Proč dron letí](https://openskylab.space/edu_viz_why_drones_fly.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/why_drones_fly_pro_cs.ipynb) · verze 1.0 · asi 55 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku o letu dronu. Mavic 3E podle výrobce visí 38 minut, ale stálou rychlostí 32,4 km/h letí 45 minut: v dopředném letu tedy potřebuje méně výkonu než na místě. Sestavíš model výkonu z teorie hybnosti, nakalibruješ ho na tyto dva údaje a použiješ ho na nejlepší rychlost pro výdrž a dolet, na skutečný vítr ve 120 m za poslední tři měsíce, na hustotu vzduchu a na let těsně nad zemí.

## Cíl

Rozložit výkon dronu na indukovaný, profilový a škodlivý, nakalibrovat model na údaje výrobce, najít rychlost nejdelší výdrže a největšího doletu i s protivětrem, vyhodnotit skutečný vítr a hustotu vzduchu za 92 dní a odhadnout vliv země při visení nízko.

## Data

Hodinový vítr v 10 a 120 m, teplota, vlhkost a tlak za posledních 92 dní z Open-Meteo pro Roztoky (modelová data, ne měření); hmotnost, vrtule, baterie a výdrž Mavicu 3E z technického listu DJI (45 min letu stálou rychlostí 32,4 km/h bez větru u hladiny moře do vybití, 38 min visení). Účinnost rotoru FM, indukční ztráty a obvodová rychlost listu jsou odhady; účinnost pohonu a plochu odporu notebook dopočítá kalibrací, takže v nich jsou schované i všechny ostatní ztráty (elektronika, kamera, baterie).

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava

Načte knihovny a stáhne data.

### 2. Model výkonu a jeho kalibrace

Výkon rozložíme na tři části. **Indukovaný** výkon jde na urychlení vzduchu dolů; v dopředném letu proudí diskem víc vzduchu, takže stačí menší indukovaná rychlost (Glauert). **Profilový** výkon spotřebuje odpor listů vrtule a s rychlostí mírně roste. **Škodlivý** výkon překonává odpor trupu a roste s třetí mocninou rychlosti. Dvě neznámé, účinnost pohonu η a ekvivalentní plochu odporu f, určíme z výdrže při visení a při letu 9 m/s.

Parametry, které student mění:

- `KAPPA = 1.15`: indukční ztráty proti ideálnímu disku (nerovnoměrný tok, konec listu)
- `FM = 0.60`: účinnost rotoru při visení (figure of merit)
- `V_TIP = 90.0`: obvodová rychlost konce listu (m/s), odhad

**Úkol 1.** Proč indukovaný výkon s rychlostí klesá a škodlivý roste? Při jaké rychlosti má dron nejdelší výdrž a při jaké největší dolet, a proč to nejsou stejné rychlosti? Je ekvivalentní plocha odporu f věrohodná pro dron velikosti Mavicu (odhadni čelní plochu trupu a součinitel odporu kolem 1)? Změň `FM` na 0,5 a 0,7: jak se změní kalibrace a výsledné rychlosti?

### 3. Let proti větru

Při protivětru se počítá energie na kilometr vůči zemi: výkon dělený rychlostí vůči zemi (V − vítr). Tabulka ukazuje nejlepší rychlost vůči vzduchu pro různý protivítr a srovnání se stálými 9 m/s.

**Úkol 2.** Proč má dron při protivětru letět rychleji vůči vzduchu, i když tím roste výkon? Kolikrát víc energie na kilometr spotřebuje návrat proti větru 6 m/s, když letí optimální rychlostí, a kolikrát, když drží 9 m/s? Při jakém větru přestane stačit normální režim s rychlostí 15 m/s?

### 4. Skutečný vítr za poslední tři měsíce

Z Open-Meteo stáhneme hodinový vítr v 10 a 120 m a počasí za 92 dní pro Roztoky a vybereme denní hodiny 8–18 h. Pro každou hodinu spočítáme energii na kilometr návratu, kdyby celý vítr ve 120 m foukal proti.

Parametry, které student mění:

- `LAT, LON = 50.152, 14.392`: místo (Roztoky)
- `WIND_LIMIT = 12.0`: odolnost vůči větru podle výrobce (m/s)

**Úkol 3.** Jak se liší vítr v 10 a ve 120 m a co to znamená, když vítr odhaduješ u země před vzletem? V kolika procentech denních hodin by vítr ve 120 m překročil odolnost dronu? O kolik procent víc energie na kilometr spotřebuje typický návrat proti větru proti bezvětří a co z toho plyne pro rezervu baterie?

### 5. Hustota vzduchu

Z tlaku, teploty a vlhkosti spočítáme hustotu vzduchu v Roztokách za stejných 92 dní a přidáme hustotu pro vysoké hory. Předpokládáme, že účinnost rotoru FM a pohonu η se s hustotou nemění.

Parametry, které student mění:

- `RHO_MOUNTAIN = 0.90`: hustota pro vysoké hory (kg/m³), zhruba 2600 m n. m.

**Úkol 4.** O kolik se v řidším vzduchu zkrátí doba visení a jak se posunou rychlosti nejdelší výdrže a největšího doletu? Proč se dolet v horách téměř nemění, i když výkon roste? (Porovnej, jak na hustotě závisí indukovaný a škodlivý výkon.) Co by se stalo, kdyby dron ve stejných horách nesl náklad, který zvýší hmotnost o 20 %? Zkus `m` v buňce modelu.

### 6. Visení těsně nad zemí

Blízko země se proud pod rotorem nemůže volně rozšířit, indukovaná rychlost klesne a stejný tah stojí méně výkonu. Cheeseman a Bennett (1955) to popsali vztahem v_IGE / v_OGE = 1 − (R / 4z)², kde z je výška rotoru nad zemí. Vztah platí pro jeden rotor; u kvadrokoptéry se proudy čtyř vrtulí navíc ovlivňují.

**Úkol 5.** Do jaké výšky nad zemí je vliv země u Mavicu znatelný (úspora výkonu nad 2 %)? Proč dron při přistání těsně nad zemí „plave“ a proč je to u velkých vrtulí výraznější v metrech? Proč ti vliv země nepomůže při letu nad vysokou vegetací nebo nad vodou se zvlněnou hladinou stejně jako nad betonem?

**Rozšíření (nepovinné).** Uprav model na Matrice 350 RTK (hmotnost 6,47 kg, vrtule 21″, baterie 2 × 263 Wh). Výrobce udává 55 min letu bez nákladu; doplň `T_FLIGHT`, odhadni `T_HOVER` a sleduj, jak výdrž klesá s nákladem až do maximální vzletové hmotnosti 9,2 kg.

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- DJI: *Mavic 3 Enterprise, specifikace* (https://enterprise.dji.com/mavic-3-enterprise/specs): vzletová hmotnost 915 g, baterie 77 Wh, max. doba letu 45 min a max. doba visení 38 min bez větru, odolnost vůči větru 12 m/s, max. rychlost 15 m/s v normálním a 21 m/s ve sportovním režimu. Podmínky měření 45 min (stálá rychlost 32,4 km/h u hladiny moře do vybití) uvádějí technické listy prodejců.
- Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*, 2. vyd. Cambridge University Press (teorie hybnosti v dopředném letu, rozklad výkonu, K ≈ 4,65).
- Glauert, H. (1926). A general theory of the autogyro. *ARC R&M* 1111 (indukovaná rychlost v dopředném letu).
- Cheeseman, I. C., Bennett, W. E. (1955). The effect of the ground on a helicopter rotor in forward flight. *ARC R&M* 3021.
- Hustota vlhkého vzduchu přes virtuální teplotu; tlak nasycených par Magnusovým vzorcem (WMO-No. 8, 2018).

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
