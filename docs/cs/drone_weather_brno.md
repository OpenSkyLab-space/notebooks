# Můžu letět? Skutečné zprávy METAR a vítr ve výšce letu

Popis notebooku k vizuálu [Můžu letět? Počasí pro drony](https://openskylab.space/edu_viz_drone_weather.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/drone_weather_brno_cs.ipynb) · verze 1.0 · asi 45 min · pět úkolů

## O čem notebook je

Ve vizuálu jsi dekódoval ukázkové zprávy METAR, přepočítal vítr z letiště na místo a výšku letu a rozhodoval podle semaforu. Tady stáhneš skutečné zprávy METAR z českých letišť za posledních 24 hodin, sám je dekóduješ a výsledek porovnáš s modelovou předpovědí větru ve 80 a 120 m.

## Cíl

Dekódovat METAR, spočítat relativní vlhkost a odhad základny oblačnosti, přepočítat vítr v 10 m na výšku letu nad jiným terénem, odhadnout návrat proti větru a rozhodnout o letu na příštích 24 hodin.

## Data

Zprávy METAR a TAF z letišť Brno-Tuřany (LKTB), Náměšť nad Oslavou (LKNA), Kunovice (LKKU) a Ostrava (LKMT) ze služby NOAA Aviation Weather Center; hodinová předpověď z Open-Meteo pro Brno-Bystrc u Brněnské přehrady. Data se mění každou půlhodinu, tvoje čísla budou jiná než v uloženém notebooku.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a skutečné zprávy METAR

Načte knihovny a stáhne data.

Parametry, které student mění:

- `STATIONS = "LKTB,LKNA,LKKU,LKMT"`: kódy letišť ICAO

### 2. Vlastní dekodér

Zpráva má pevné pořadí skupin: letiště, čas, vítr (směr, rychlost, nárazy G), dohlednost v metrech nebo CAVOK, jevy (RA déšť, SN sníh, BR kouřmo, FG mlha, - slabý, + silný), oblačnost (FEW, SCT, BKN, OVC a výška ve stovkách stop), teplota/rosný bod (M = minus) a tlak QNH. Část za TEMPO, BECMG nebo NOSIG je krátká předpověď a dekodér ji vynechá.

**Úkol 1.** Vyber si jednu zprávu a dekóduj ji ručně skupinu po skupině; souhlasí s tabulkou? Které skupiny by samy o sobě vyloučily let VLOS (dohlednost, mlha, nízká oblačnost, srážky)? Proč je pro pilota důležitější rozdíl T − Td než samotná teplota?

**Úkol 2.** Jak dobře odhad 125 m · (T − Td) odpovídá skutečně nahlášené základně? Odhad platí pro kupovitou oblačnost v dobře promíchané vrstvě za dne. Najdi zprávy, kde selhává, a vysvětli proč (noc, vrstevnatá oblačnost, inverze, oblačnost z jiné vzduchové hmoty).

### 3. Vítr ve výšce letu nad jiným terénem

Letiště měří vítr v 10 m nad trávou (délka drsnosti z0 = 0,03 m). Ve výšce promíchání 60 m je vliv povrchu malý, tam vítr přeneseme na místo letu s jinou drsností z0 a posunutím nulové roviny d (Wieringa 1986). Platí pro neutrální zvrstvení (vítr, oblačno); za slunečného dne nebo v noci se profil liší.

Parametry, které student mění:

- `u10 = float(met[met["stanice"] == "LKTB"]["vítr m/s"].iloc[0])`: vítr v 10 m (výchozí je poslední METAR z Brna)

**Úkol 3.** Proč nad lesem vychází ve 30 m slabší průměrný vítr než nad vodou, ale ve 100 m skoro stejný? Kolega říká: „Letiště hlásí 6 m/s, dron snese 12 m/s, máme dvojnásobnou rezervu.“ Nastav `u10 = 6` a odpověz mu čísly pro výšku 100 m. Jak se poměr 80 m / 10 m z modelu Open-Meteo liší od našeho profilu a proč (zvrstvení během dne a noci)?

### 4. Cesta zpět proti větru

Dron letí vůči vzduchu rychlostí V, vítr ve výšce letu má rychlost U. Na trase D tam po větru a zpět proti větru trvá let t = D/(V + U) + D/(V − U).

Parametry, které student mění:

- `V, D = 12.0, 800`: rychlost vůči vzduchu (m/s) a vzdálenost od pilota (m)

**Úkol 4.** Odvoď ze vzorce, při jakém větru se čas tam a zpět zdvojnásobí (výsledek U = V/√2 vypisuje buňka). Proč nestačí, že průměrný vítr ve výšce letu je pod odolností dronu, když jsou nárazy (sloupec nárazy v METAR) o 30–50 % vyšší? Jak bys podle toho naplánoval trasu?

### 5. Semafor na příštích 48 hodin

Pro každou hodinu předpovědi z Open-Meteo pro místo letu rozhodneme: vítr ve 120 m a nárazy proti limitu dronu, srážky, dohlednost a riziko námrazy (teplota pod 1 °C a T − Td do 2 °C).

Parametry, které student mění:

- `limit = 12.0`: odolnost dronu vůči větru (m/s)

**Úkol 5.** Kdy bys v příštích 48 hodinách letěl a co v ostatních hodinách rozhoduje? Porovnej předpověď s posledním TAF pro Brno: shodují se? Nárazy ve 120 m jsme odhadli poměrem nárazů a větru v 10 m; proč je to hrubé a proč je výsledek spíš na straně bezpečnosti, nebo naopak? Nastav `limit = 10.7` (odolnost malého dronu do 250 g, např. DJI Mini 4 Pro). Co se změní?

**Rozšíření (nepovinné).** Spolužáci mohou mít notebook pro jiné místo a jiná letiště (Roztoky a Praha; Brno-Bystrc a Brno-Tuřany; Hluboká a Linec). Porovnejte ve stejnou hodinu vítr z METAR, poměr větru 80 m / 10 m z Open-Meteo a výsledek semaforu. Proč se poměr liší podle místa a terénu?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- METAR a TAF: NOAA/NWS Aviation Weather Center, https://aviationweather.gov/data/api/ (veřejná data vlády USA).
- Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- Relativní vlhkost a tlak nasycených par (Magnusův vzorec): WMO (2018). *Guide to Instruments and Methods of Observation* (WMO-No. 8), příloha 4.B.
- Přenos větru přes výšku promíchání 60 m: Wieringa, J. (1986). Roughness-dependent geographical interpolation of surface wind speed averages. *Quarterly Journal of the Royal Meteorological Society* 112, 867–889; Verkaik, J. W. (2000). Evaluation of two gustiness models for exposure correction calculations. *Journal of Applied Meteorology* 39, 1613–1626.
- Klíč ke zprávám METAR: ICAO Annex 3 / WMO-No. 306, kód FM 15.
- Odolnost DJI Mavic 3 Enterprise vůči větru 12 m/s, max. rychlost 15 m/s v normálním režimu, 21 m/s ve sportovním (technický list DJI); odolnost DJI Mini 4 Pro vůči větru 10,7 m/s.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
