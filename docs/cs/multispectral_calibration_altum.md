# Kalibrace multispektrální kamery: od DN k odrazivosti na skutečných snímcích

Popis notebooku k vizuálu [Kalibrace multispektrální kamery](https://openskylab.space/edu_viz_multispectral_calibration.html). [Otevřít v Google Colab](https://colab.research.google.com/github/OpenSkyLab-space/notebooks/blob/main/multispectral_calibration_altum_cs.ipynb) · verze 1.0 · asi 45 min · pět úkolů

## O čem notebook je

Vizuál ukazuje, co s odrazivostí udělá mrak, náklon dronu, vinětace a malý panel. Tady projdeš celý řetězec na skutečných snímcích kamery MicaSense Altum: snímek kalibračního panelu před letem a snímek z letu nad křižovatkou silnic, lesem, stromořadím a travnatým polem. Všechny potřebné údaje (černá úroveň, vinětace, kalibrační koeficienty, odrazivost panelu, údaje senzoru osvětlení DLS 2) jsou uložené přímo v souborech TIFF.

## Cíl

Převést DN na radianci krok za krokem, z panelu spočítat kalibrační koeficient, porovnat odrazivost jen z panelu, jen z DLS a z obou dohromady, ukázat vliv vinětace, saturace a náklonu senzoru DLS a spočítat NDVI ze sesazených pásem.

## Data

Dva snímky (5 multispektrálních pásem) kamery MicaSense Altum s DLS 2 z ukázkových dat MicaSense (repozitář micasense/imageprocessing, licence MIT): IMG_0000 (panel RP06, 6. 4. 2022 20:00 UTC) a IMG_0021 (let o 2 minuty později asi 100 m nad terénem), 47,70° s. š., 122,14° z. d. Altum má i termální pásmo 6, které tento notebook nepoužívá.

Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.

## Postup krok za krokem

### 1. Příprava a snímky

Načte knihovny a stáhne data.

### 2. Od DN k radianci

Model MicaSense (stejný jako v knihovně `micasense/image.py`):

L = V(r) · R(y) · (DN − černá úroveň) / (zisk · expozice) · a₁ / 2¹⁶

- černá úroveň: signál bez světla (tag BlackLevel),
- V(r) = 1 / (1 + k₀r + … + k₅r⁶): korekce vinětace podle vzdálenosti r od středu vinětace (novější kamery ukládají místo toho 2D polynom v souřadnicích x, y),
- R(y) = 1 / (1 + a₂ y / expozice − a₃ y): korekce podle řádku (snímač se čte po řádcích),
- a₁: radiometrický kalibrační koeficient z výroby. Výsledek je spektrální radiance ve W/m²/sr/nm.

Parametry, které student mění:

- `BAND = 4`: pásmo 1 modré, 2 zelené, 3 červené, 4 NIR, 5 red edge

**Úkol 1.** Projdi pásma 1 až 5. O kolik procent zesiluje korekce vinětace signál v rohu snímku a ve kterém pásmu nejvíc? Kolik procent pixelů je saturovaných a kde ve snímku jsou? Proč saturovaný pixel nejde opravit žádnou kalibrací a co s tím při letu uděláš?

### 3. Kalibrační panel

V metadatech snímku panelu je oblast uprostřed panelu, kterou na snímku našel software kamery (ReflectArea, čtyři rohy v pixelech), a jeho odrazivost v daném pásmu (Albedo) z kalibračního listu. Z průměrné radiance panelu L_p plyne koeficient k = ρ_panel / L_p a odrazivost každého pixelu ρ = k · L.

Parametry, které student mění:

- `SHRINK = 1.0`: zmenšení oblasti z metadat (1 = celá oblast, 0,3 = jen střed)
- `GROW_PX = 0`: oblast naopak zvětšit o tolik pixelů (napodobí nepřesné vyznačení panelu)

**Úkol 2.** Nastav GROW_PX na 30, 60 a 90 (podívej se na detail, kam oblast sahá): jak se změní průměrná radiance panelu a koeficient k? O kolik procent by se tím posunula odrazivost celé mapy? Pak nastav SHRINK = 0,2: co se stane s variabilitou a proč? Proč se do průměru berou jen pixely ze středu panelu a proč musí být panel na snímku dost velký (kolik pixelů tu má)?

### 4. Senzor osvětlení DLS a jeho náklon

DLS měří ozáření na svou horní plochu. Když se dron nakloní ke Slunci, dopadá na senzor víc přímého záření, než kolik dopadá na vodorovný terén. DLS 2 proto rozkládá ozáření na přímou a rozptýlenou složku a přepočítává ho na vodorovnou plochu: E_vod = E_přímé · sin(výška Slunce) + E_rozptýlené.

Parametry, které student mění:

- `TILT = 10`: náklon senzoru DLS (°)

**Úkol 3.** O kolik procent se mezi snímkem panelu a snímkem z letu změnilo vodorovné ozáření (časy snímků vypsala první buňka)? Jak velkou chybu odrazivosti způsobí náklon 10° a 20° ke Slunci a od Slunce? Proč je chyba při nízkém Slunci větší a proč pomáhá, když je rozptýlené složky hodně (zataženo)?

### 5. Tři způsoby kalibrace

- **jen panel:** ρ = k · L. Předpokládá, že se osvětlení od snímku panelu nezměnilo.
- **jen DLS:** ρ = π · L / E_vod. Spoléhá na tovární kalibraci kamery i DLS.
- **panel + DLS:** ρ = k · L · E_vod(panel) / E_vod(snímek). Panel určí absolutní úroveň, DLS sleduje změny osvětlení.

Kontrola: když metodu „jen DLS“ použijeme na samotný panel, měli bychom dostat jeho známou odrazivost.

Parametry, které student mění:

- `REGIONS = {"silnice": (slice(500, 840), slice(660, 750)), "travnaté pole": (slice(200, 800), slice(1550, 1950)), "les": (slice(100, 800), slice(40, 500))}`: oblasti (řádky, sloupce)

**Úkol 4.** Jakou odrazivost panelu dá metoda „jen DLS“ a o kolik procent se liší od kalibračního listu? Která metoda je tu nejspolehlivější a proč? O kolik se liší „jen panel“ a „panel + DLS“ a čím to je (vrať se ke kroku 4)? Odpovídají křivky silnice, travnatého pole a lesa tomu, co znáš ze spektrálních signatur?

### 6. NDVI a co s ním dělá kalibrace

NDVI = (ρ_NIR − ρ_R) / (ρ_NIR + ρ_R). Porovnáme NDVI z radiance (bez kalibrace), z kalibrace „panel + DLS“ a z kalibrace bez korekce vinětace.

Parametry, které student mění:

- `NDVI_MIN = 0.5`: práh NDVI pro „vegetaci“

**Úkol 5.** Proč se NDVI z radiance tolik liší od NDVI z odrazivosti, i když jde o stejný snímek? Proč vynechání korekce vinětace NDVI skoro nezmění, ale odrazivost v rozích ano (srovnej s krokem 2)? Jak by se změnil podíl vegetace, kdyby někdo prahoval NDVI z radiance?

**Rozšíření (nepovinné).** Spolužáci mohou mít notebook pro jinou kameru (RedEdge-MX, Altum, Altum-PT). Porovnejte koeficient k z panelu, změnu ozáření mezi panelem a letem a rozdíl metod „jen DLS“ a „panel + DLS“. Liší se víc kamery, nebo podmínky osvětlení při letu?

## Co je potřeba

Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.

## Zdroje dat a literatura

- Snímky a postup radiometrické kalibrace: MicaSense, Inc. (2017–2023). *imageprocessing* (licence MIT), https://github.com/micasense/imageprocessing, soubory data/ALTUM/IMG_0000_*.tif a IMG_0021_*.tif a micasense/image.py (vinětace, radiance, odrazivost).
- MicaSense: RedEdge Camera Radiometric Calibration Model; Use of Calibrated Reflectance Panels for MicaSense Data (podpora MicaSense).
- Smith, G. M., Milton, E. J. (1999). The use of the empirical line method to calibrate remotely sensed data to reflectance. *International Journal of Remote Sensing* 20(13), 2653–2662.
- Přehled kalibrace multispektrálních a hyperspektrálních kamer na UAV: Aasen, H., Honkavaara, E., Lucieer, A., Zarco-Tejada, P. J. (2018). Quantitative remote sensing at ultra-high resolution with UAV spectroscopy. *Remote Sensing* 10(7), 1091.

---

Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).

*Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.*
