# Fotony v pásmech Sentinelu-2C

Popis notebooku k laboratoři [Švihadlo a fotony](https://openskylab.space/edu_viz_rope_and_photons.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/rope_and_photons_brno_cs.ipynb) · verze 1.0 · asi 40 min · šest úkolů

## O čem notebook je

V laboratoři jsi sledoval vlnu na laně. Její rychlost $v$, vlnovou délku
$\lambda$ (vzdálenost mezi sousedními vrcholy) a frekvenci $f$ (počet kmitů
za sekundu) spojuje vztah

$$
v = \lambda f.
$$

**Pro světlo ve vakuu platí stejný vztah**, s rychlostí světla $c$. Světlo
přenáší energii ve fotonech. Z vlnové délky určíme frekvenci a energii
jednoho fotonu:

$$
f = \frac{c}{\lambda}, \qquad E = hf.
$$

$h$ je Planckova konstanta; energii budeme vyjadřovat v elektronvoltech (eV),
jednotce energie. **Kratší vlnová délka znamená vyšší frekvenci a větší energii
fotonu.** Při stejné frekvenci znamená více fotonů dopadajících na stejnou
plochu za sekundu více přenesené energie; energie jednotlivého fotonu se nemění.
Tady to spočítáš pro skutečná pásma družice Sentinel-2C.

## Cíl

Z metadat skutečné scény Sentinel-2 spočítat frekvenci, energii fotonu a tok fotonů v každém pásmu a odvodit z nich, jaký detektor které pásmo potřebuje.

## Data

Metadata produktu Sentinel-2C L1C, dlaždice 33UXQ (okolí Brna), 5. 2. 2025 (`MTD_MSIL1C.xml` z veřejného archivu Google Cloud): střední vlnové délky, spektrální citlivost pásem a spektrální sluneční ozářenost nad atmosférou. Stahuje se asi 50 kB.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Notebook je uložený bez výstupů; čísla a grafy vzniknou až při spuštění a u průběžně aktualizovaných dat se mohou mezi běhy lišit.

## Postup krok za krokem

### 1. Příprava a data

Načte knihovny a stáhne data.

### 2. Vlnová délka a frekvence

Načte knihovny a stáhne data.

**Úkol 1.** Sloupec `lambda_x_f` je u všech pásem stejný. Co vyjadřuje a čemu odpovídá na laně v laboratoři? Kolikrát vyšší frekvenci má pásmo B2 (modrá) než B12 (SWIR 2)?

### 3. Energie jednoho fotonu

Energii jednoho fotonu určuje Planckův–Einsteinův vztah:

$$
E = hf = \frac{hc}{\lambda}.
$$

Používáme $h \approx 6{,}626\times10^{-34}\ \mathrm{J\,s}$,
$c \approx 3{,}00\times10^8\ \mathrm{m\,s^{-1}}$ a vlnovou délku
$\lambda$ v metrech, takže výsledek vyjde v joulech.
Protože $1\ \mathrm{eV} = 1{,}602\,176\,634\times10^{-19}\ \mathrm{J}$,
převedeme energii na eV vydělením touto hodnotou. V kódu ji poskytuje
číselná hodnota `e`, elementárního náboje v coulombech, ze `scipy.constants`.

**Úkol 2.** Ověř poměr energií modrého a červeného fotonu jen z vlnových délek, bez konstant. Proč stačí poměr λ? Jak se změní energie jednoho fotonu, když je modré světlo dvakrát jasnější?

### 4. Od energie záření k toku fotonů

Metadata uvádějí spektrální sluneční ozářenost $E_0$ nad atmosférou
v $\mathrm{W\,m^{-2}\,\mu m^{-1}}$. Vydělením energií jednoho fotonu
v joulech získáme počet fotonů dopadajících za sekundu na metr čtvereční
na jednotku vlnové délky, zde na mikrometr:

$$
\Phi_\lambda = \frac{E_0}{E}.
$$

$\Phi_\lambda$ má jednotku $\mathrm{s^{-1}\,m^{-2}\,\mu m^{-1}}$.
Jde o spektrální hustotu toku fotonů, nikoli o celkový počet fotonů v pásmu.

**Úkol 3.** Spektrální ozářenost E0 klesá od modré (B2) k SWIR 2 (B12) více než dvacetkrát. Klesá stejně i spektrální hustota toku fotonů? Vysvětli rozdíl. V kterém pásmu dopadá na metr čtvereční nejvíc fotonů na mikrometr spektra a proč to není pásmo s nejvyšším E0?

### 5. Které pásmo uvidí křemíkový čip

Foton detektor uvolní elektron jen tehdy, když má aspoň energii zakázaného pásu materiálu. U křemíku je to asi 1,12 eV. Spočítáme mezní vlnovou délku a podíváme se, jak velká část citlivosti každého pásma leží pod ní.

Parametry, které student mění:

- `Eg = 1.12`: šířka zakázaného pásu v eV (křemík 1,12; InGaAs asi 0,75; HgCdTe podle složení 0,1–0,5)

**Úkol 4.** Která pásma Sentinelu-2 by křemíkový detektor zachytil celá, která jen zčásti a která vůbec? Nastav `Eg = 0.75` (InGaAs) a spusť buňku znovu. Co se změnilo? Sentinel-2 má pro pásma B10 až B12 detektory z HgCdTe: proč?

### 6. Termální záření a radar

Porovnáme fotony z termálního pásma (10,9 µm, jako Landsat 8 TIRS) a z radaru Sentinel-1 (5,405 GHz) s typickou tepelnou energií kmitů v detektoru při pokojové teplotě, k · T.

Parametry, které student mění:

- `T = 300`: teplota detektoru v kelvinech

**Úkol 5.** Termální foton má energii jen asi čtyřikrát větší než k · T, radarový foton je víc než tisíckrát slabší než k · T. Proč proto termální kamery s fotonovými detektory chladí a proč mikrobolometr a radarová anténa neměří jednotlivé fotony, ale ohřev, resp. elektrické pole vlny? Nastav `T = 77` (kapalný dusík) a porovnej.

**Úkol 6.** Na jaké vlnové délce má foton energii 10 eV (přibližná hranice ionizace)? Do které oblasti spektra patří? Chemické vazby v molekulách mají energii v řádu několika eV. Vysvětli, proč jediný foton UV záření může poškodit DNA, zatímco silný radarový signál nese celkem víc energie, a přesto žádnou vazbu nerozbije ani nic neionizuje.

**Rozšíření (nepovinné).** Spolužáci mohou mít notebook pro jinou družici řady Sentinel-2 (2A, 2B nebo 2C). Porovnejte střední vlnové délky pásem a hodnoty E0: o kolik nanometrů se pásma stejného jména liší a proč s tím musí počítat, kdo skládá časovou řadu ze snímků více družic?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Copernicus Sentinel-2 data 2025, ESA; metadata L1C z veřejného archivu Google Cloud (`gcp-public-data-sentinel-2`). Licence: [Legal notice on the use of Copernicus Sentinel Data](https://sentinels.copernicus.eu/documents/247904/690755/Sentinel_Data_Legal_Notice), volné užití s uvedením zdroje.
- Konstanty h, c, e, k: v SI od roku 2019 přesně definované hodnoty, převzaté z `scipy.constants`; přehled CODATA 2022: [NIST](https://physics.nist.gov/cuu/pdf/wall_2022.pdf).
- Šířka zakázaného pásu křemíku 1,12 eV při 300 K: Sze, S. M., Ng, K. K. (2007). *Physics of Semiconductor Devices*, 3. vyd. Wiley.
- Frekvence radaru Sentinel-1 (pásmo C) 5,405 GHz: ESA, Sentinel-1 User Handbook.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
