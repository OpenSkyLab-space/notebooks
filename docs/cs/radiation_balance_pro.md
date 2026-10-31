# Kam zmizí sluneční záření, pokročilá verze: denní chod teploty povrchu

Popis notebooku k vizuálu [Kam zmizí záření](https://openskylab.space/edu_viz_radiation_balance.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/radiation_balance_pro_cs.ipynb) · verze 1.0 · asi 60 min · pět úkolů

## O čem notebook je

Pokročilá verze notebooku k radiační bilanci. Místo rovnováhy v jedné hodině tu povrch ohříváš a ochlazuješ hodinu po hodině při skutečném počasí několika dní. K pohlcenému záření a vyzařování přibude výpar a tok tepla do země, takže uvidíš, proč je les v poledne chladnější než pole a proč město v noci zůstává teplé.

## Cíl

Sestavit z reálného počasí sluneční a dlouhovlnné záření, spočítat denní chod teploty povrchu modelem force-restore, rozdělit čistou radiaci na citelné teplo, výpar a tok do země a vysvětlit vliv albeda, dostupnosti vody a tepelné setrvačnosti.

## Data

Albedo povrchů ze scény Sentinel-2 L2A `S2B_33UVR_20240721_0_L2A` (21. 7. 2024, okolí Roztok) a tříd ESA WorldCover 2021; hodinové počasí pro Prahu z Open-Meteo (posledních 92 dní, simulují se dny kolem nejslunečnějšího z nich). Stahuje se asi 5 MB. Vlastnosti povrchů (dostupnost vody, tepelná setrvačnost) jsou orientační a model je zjednodušený: výsledky ukazují souvislosti, nejsou předpovědí skutečné teploty.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a albedo povrchů

Albedo čtyř povrchů spočítáme stejně jako v základní verzi (Liang 2001, pásma Sentinelu-2). Vodu vynecháme: voda se promíchává a teplo ukládá do hloubky, což jednovrstvý model povrchu nepopíše.

### 2. Skutečné počasí jako vstup

Z Open-Meteo vezmeme hodinové globální záření, teplotu, rosný bod, vítr, oblačnost a tlak. Dlouhovlnné záření oblohy L↓ počítáme z emisivity jasné oblohy (Brutsaert 1975) a oblačnost c přičteme ve tvaru Crawforda a Duchona (1999): ε = ε_jasno · (1 − c) + c. Oblačnost tu bereme z modelu počasí, ne z měření.

Parametry, které student mění:

- `LAT, LON = 50.08, 14.42`: místo pro počasí (Praha)
- `N_DAYS = 4`: kolik dní simulovat (nejslunečnější den je uprostřed)

**Úkol 1.** Najdi v grafech noc s jasnou a noc se zataženou oblohou. O kolik se v nich liší L↓ a proč? Co to znamená pro ochlazování povrchu v noci?

### 3. Model povrchu

Čistá radiace Rn = (1 − albedo) · S + ε · L↓ − ε · σ · Ts⁴ se dělí na citelné teplo H = h · (Ts − T_vzduch), výpar LE = β · (L_v/c_p) · h · (q_sat(Ts) − q_vzduch) a tok do země G = Rn − H − LE. Teplotu povrchu Ts posouvá G podle modelu force-restore (Noilhan a Planton 1989): dTs/dt = C_T · G − (2π/τ) · (Ts − T2), kde C_T = 2√(π/τ)/P a P je tepelná setrvačnost. β říká, kolik vody má povrch k dispozici (0 suchý beton, 1 mokrý povrch).

Parametry, které student mění:

- `SURF = pd.DataFrame({`: vlastnosti povrchů (orientační)
- `WIND = 0.75`: vítr u povrchu jako podíl větru v 10 m

**Úkol 2.** Který povrch je nejteplejší v poledne a který v noci? Proč je zástavba v poledne chladnější než pole, i když skoro nic neodpařuje, a v noci naopak nejteplejší? V kolik hodin UTC má povrch maximum a proč až po slunečním poledni (v Praze kolem 11:00 UTC)?

### 4. Kam se energie během dne rozdělí

Načte knihovny a stáhne data.

**Úkol 3.** Kolik procent čisté radiace spotřebuje les na výpar a kolik zástavba? Co říká Bowenův poměr a proč u lesa vychází pod 1? Proč je denní součet G kladný, tj. co se během slunečných dní děje s teplem v zemi?

### 5. Setrvačnost a voda

Načte knihovny a stáhne data.

Parametry, které student mění:

- `TEST = "zástavba"`: povrch, na kterém zkoušíme vlastnosti

**Úkol 4.** Jak se s rostoucí tepelnou setrvačností P mění denní rozkmit teploty a čas maxima? A jak s dostupností vody β? Který z obou zásahů by víc pomohl proti přehřívání ulic ve dne a který v noci (zeleň a zalévání, nebo jiné materiály)?

### 6. Srovnání s rovnováhou ze základní verze

Načte knihovny a stáhne data.

**Úkol 5.** O kolik stupňů je rovnovážná teplota bez výparu a toku do země vyšší než teplota z modelu? Které dva členy bilance rozdíl vysvětlují a u kterého povrchu je který důležitější? Proč termokamera z dronu v poledne ukáže mezi lesem a polem rozdíl, ze kterého lze usuzovat na vodní stres?

**Rozšíření (nepovinné).** Změň `LAT, LON` na jiné místo (třeba horskou stanici) nebo `N_DAYS` na 10 a podívej se, jak se mění noční minima při jasné a zatažené obloze. Proč jsou mrazové kotliny nejchladnější za jasných a klidných nocí?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.
- Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).
- Počasí: Open-Meteo.com (CC BY 4.0). https://open-meteo.com
- Liang, S. (2001). Narrowband to broadband conversions of land surface albedo I: Algorithms. *Remote Sensing of Environment* 76, 213–238. https://doi.org/10.1016/S0034-4257(00)00205-4
- Brutsaert, W. (1975). On a derivable formula for long-wave radiation from clear skies. *Water Resources Research* 11, 742–744. https://doi.org/10.1029/WR011i005p00742
- Crawford, T. M., Duchon, C. E. (1999). An improved parameterization for estimating effective atmospheric emissivity for use in calculating daytime downwelling longwave radiation. *Journal of Applied Meteorology* 38, 474–480.
- Noilhan, J., Planton, S. (1989). A simple parameterization of land surface processes for meteorological models. *Monthly Weather Review* 117, 536–549. https://doi.org/10.1175/1520-0493(1989)117<0536:ASPOLS>2.0.CO;2
- Oke, T. R., Mills, G., Christen, A., Voogt, J. A. (2017). *Urban Climates*. Cambridge University Press.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
