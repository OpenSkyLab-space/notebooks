# Proč dron letí: vztlak, hybnost a skutečná hustota vzduchu

Popis notebooku k vizuálu [Proč dron letí](https://openskylab.space/edu_viz_why_drones_fly.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/why_drones_fly_cs.ipynb) · verze 1.0 · asi 45 min · pět úkolů

## O čem notebook je

Vizuál vysvětluje vztlak profilu, pádový úhel, teorii hybnosti rotoru a nebezpečné režimy klesání. Tady teorii hybnosti použiješ na skutečné drony (DJI Mavic 3 Enterprise a Matrice 350 RTK) a na skutečnou hustotu vzduchu, kterou spočítáš z měřeného a modelovaného počasí na horách i v nížině.

## Cíl

Spočítat vztlak tenkého profilu a jeho mez, indukovanou rychlost a výkon při visení, ukázat, jak hustota vzduchu mění výdrž, a odhadnout rychlost klesání, při které hrozí vírový prstenec.

## Data

Hodinová teplota, tlak a vlhkost za posledních 92 dní z Open-Meteo pro Prahu, Sněžku a Lomnický štít; hmotnost, průměr vrtulí, baterie a výdrž dronů z technických listů DJI.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava

Načte knihovny a stáhne data.

### 2. Vztlak profilu a pád

Podle teorie tenkého profilu roste součinitel vztlaku lineárně s úhlem náběhu: c_L = 2π (α − α₀), kde α₀ ≈ −2 · prohnutí / hloubka (záporné pro prohnutý profil). Skutečný profil se ale při úhlu kolem 12–16° odtrhne a vztlak spadne. Vztlak L = ½ ρ v² S c_L.

Parametry, které student mění:

- `camber = 0.04`: prohnutí profilu (podíl hloubky; 0 = souměrný, 0,04 = 4 %)
- `alpha_stall = 14`: pádový úhel (°), z měření skutečných profilů zhruba 12–16°

**Úkol 1.** Proč prohnutý profil nese i při úhlu náběhu 0° a souměrný ne? Nastav `camber = 0`. Při jakém úhlu by křídlo uneslo 2,5 kg? Proč teorie tenkého profilu nad pádovým úhlem neplatí a co se v tu chvíli děje s prouděním na horní straně? (Průběh za pádem je v grafu jen schematický.)

### 3. Dva pohledy na jednu sílu

Rotor při visení vrhá vzduch dolů. Teorie hybnosti: tah T = ṁ · w, kde w = 2 v_i je rychlost vzduchu daleko pod rotorem a ṁ = ρ A v_i hmotnostní tok diskem. Odtud v_i = √(T / (2 ρ A)). Tentýž tah je i rozdíl tlaků nad a pod diskem: Δp = T / A.

**Úkol 2.** Ověř, že sloupec ṁ · 2 v_i dává stejné číslo jako tah rotoru. Proč jsou rozdíl tlaků a hybnost vrženého vzduchu dva popisy téže síly, ne dvě síly, které se sčítají? Proč má Matrice 350 větší zatížení disku a vyšší indukovanou rychlost, i když má mnohem větší vrtule?

### 4. Skutečná hustota vzduchu: nížina, hory, teplo a chlad

Ideální výkon při visení je P = T^(3/2) / √(2 ρ A), tedy roste s 1/√ρ. Hustotu spočítáme z tlaku, teploty a vlhkosti za posledních 92 dní. Vypsaná nadmořská výška je výška bodu modelu Open-Meteo; u štítů je nižší než skutečný vrchol (Lomnický štít má 2634 m n. m.).

Parametry, které student mění:

- `FM, eta = 0.60, 0.80`: účinnost rotoru (figure of merit) a účinnost motoru s regulátorem

**Úkol 3.** O kolik procent je vzduch na Lomnickém štítu řidší než v Praze a o kolik procent víc výkonu potřebuje dron k visení? Ověř, že poměr výkonů je √(ρ_Praha / ρ_štít). Jaké FM a η by musely platit, aby odhad doby visení odpovídal údaji výrobce? Proč výrobce udává výdrž za ideálních podmínek?

**Úkol 4.** Proč velké pomalé vrtule potřebují k visení méně výkonu než malé rychlé? Vysvětli to z P = T · v_i: kterou ze dvou veličin větší disk mění? Proč přesto nemá malý dron obří vrtule?

### 5. Klesání a vírový prstenec

Když dron klesá svisle rychlostí srovnatelnou s indukovanou rychlostí při visení v_h, vzduch, který rotor tlačí dolů, se mu vrací shora skrz disk. Podle Leishmana (2006) je oblast vírového prstence zhruba mezi 0,5 v_h a 1,5 v_h (přesná mez závisí na měření).

Parametry, které student mění:

- `site = "Sněžka"`: místo (hustota = medián za 92 dní)

**Úkol 5.** Při jaké svislé rychlosti klesání hrozí vírový prstenec u Mavicu a u Matrice? Leží maximální rychlost klesání od výrobce v této oblasti? Proč je bezpečnější klesat šikmo nebo s dopřednou rychlostí a proč je nebezpečné rychlé svislé klesání těsně nad zemí, kdy už není prostor na vybrání?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Počasí: Open-Meteo.com (CC BY 4.0), https://open-meteo.com
- DJI Mavic 3 Enterprise (3E): vzletová hmotnost 915 g, vrtule 9453F (9,4″), baterie 77 Wh, max. doba visení 38 min, max. rychlost klesání 6 m/s; DJI Matrice 350 RTK: hmotnost s bateriemi TB65 6,47 kg, max. vzletová 9,2 kg, vrtule 21″, 2 × 263 Wh, max. rychlost klesání 7 m/s (technické listy DJI).
- Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*, 2. vyd. Cambridge University Press (teorie hybnosti, účinnost FM, vírový prstenec).
- Anderson, J. D. (2017). *Fundamentals of Aerodynamics*, 6. vyd. McGraw-Hill (teorie tenkého profilu).
- Hustota vlhkého vzduchu přes virtuální teplotu; tlak nasycených par Magnusovým vzorcem (WMO-No. 8, 2018).

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
