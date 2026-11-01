from _common import S2_HELPERS

META = {
    "version": "1.0",
    "minutes": 75,
    "visual_stem": "image_classification",
    "title": {"cs": "Od pixelu ke třídě, pokročilá verze: časová řada, prostorová validace a odhad ploch",
              "en": "From pixel to class, advanced: time series, spatial validation and area estimates"},
    "visual": {"cs": "Od pixelu ke třídě", "en": "From pixel to class"},
    "lead": {
        "cs": "Pokročilá verze notebooku ke klasifikaci. Místo jednoho snímku pracuješ se třemi snímky Sentinel-2 z jara, léta a podzimu 2024 u Roztok, klasifikátor minimální vzdálenosti si napíšeš sám, přesnost ověříš prostorovou validací a plochy tříd odhadneš i s nejistotou, jak se to dělá v praxi. Část kódu doplňuješ sám.",
        "en": "The advanced version of the classification notebook. Instead of one image you work with three Sentinel-2 images from spring, summer and autumn 2024 near Roztoky, write the minimum distance classifier yourself, check accuracy with spatial validation and estimate class areas with their uncertainty, as is done in practice. Part of the code you write yourself.",
    },
    "goal": {
        "cs": "sestavit příznaky z časové řady, napsat a ověřit vlastní klasifikátor, porovnat náhodnou a prostorovou validaci, změřit přínos jednotlivých snímků a odhadnout plochy tříd s intervalem spolehlivosti podle dobré praxe (Olofsson a kol. 2014).",
        "en": "build features from a time series, write and check your own classifier, compare random and spatial validation, measure what each image adds, and estimate class areas with a confidence interval following good practice (Olofsson et al. 2014).",
    },
    "data": {
        "cs": "tři snímky Sentinel-2 L2A dlaždice 33UVR (27. 4., 21. 7. a 21. 9. 2024) z katalogu Earth Search na AWS, výřez 4 × 4 km kolem Roztok a Suchdola; reference ESA WorldCover 10 m 2021 v200. Stahuje se asi 60 MB.",
        "en": "three Sentinel-2 L2A images of tile 33UVR (27 April, 21 July and 21 September 2024) from the Earth Search catalogue on AWS, a 4 × 4 km window around Roztoky and Suchdol; reference ESA WorldCover 10 m 2021 v200. About 60 MB is downloaded.",
    },
    "sources": {
        "cs": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.",
            "Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015",
            "Roberts, D. R. a kol. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40, 913–929. https://doi.org/10.1111/ecog.02881",
            "Congalton, R. G., Green, K. (2019). *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices*, 3. vyd. CRC Press.",
            "Pedregosa, F. a kol. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.",
        ],
        "en": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.",
            "Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E., Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148, 42–57. https://doi.org/10.1016/j.rse.2014.02.015",
            "Roberts, D. R. et al. (2017). Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40, 913–929. https://doi.org/10.1111/ecog.02881",
            "Congalton, R. G., Green, K. (2019). *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices*, 3rd ed. CRC Press.",
            "Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a tři snímky", "## 1. Setup and three images")),
        ("code", "%pip install -q rasterio"),
        ("code", t('''
import requests, warnings
from itertools import combinations
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
from sklearn.neighbors import NearestCentroid
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, GroupKFold, cross_val_score, cross_val_predict
from sklearn.metrics import f1_score
warnings.filterwarnings("ignore")
''', '''
import requests, warnings
from itertools import combinations
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
from sklearn.neighbors import NearestCentroid
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, GroupKFold, cross_val_score, cross_val_predict
from sklearn.metrics import f1_score
warnings.filterwarnings("ignore")
''') + t(S2_HELPERS["cs"], S2_HELPERS["en"])),
        ("code", t('''
DATES = ["S2A_33UVR_20240427_0_L2A", "S2B_33UVR_20240721_0_L2A", "S2A_33UVR_20240921_0_L2A"]   # ◀ parametr: snímky jednoho roku (jaro, léto, podzim)
LON, LAT, HALF = 14.37, 50.14, 2000                                                          # ◀ parametr: střed výřezu a jeho poloviční šířka (m)
stack, clear = {}, None
for item_id in DATES:
    refl, scl, wl, grid, item = s2_window(item_id, LON, LAT, HALF)
    day = item["properties"]["datetime"][:10]
    stack[day] = refl
    m = np.isin(scl, [4, 5, 6])
    clear = m if clear is None else clear & m
    print(f"{item_id}: {day}, bez mraků {m.mean():.1%} výřezu")
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
CLASSES = {10: "les", 30: "louka", 40: "pole", 50: "zástavba", 80: "voda"}
COLORS = ["#2e7d32", "#9ccc65", "#f2c14e", "#c62828", "#1e88e5"]
names = list(CLASSES.values())
y_img = np.full(wc.shape, -1)
for i, k in enumerate(CLASSES):
    y_img[wc == k] = i
ok = clear & (y_img >= 0)
print(f"pixelů bez mraků ve všech snímcích a v pěti třídách: {ok.sum()} ({ok.mean():.1%})")
fig, ax = plt.subplots(1, len(stack) + 1, figsize=(4 * (len(stack) + 1), 4))
for a, (day, r) in zip(ax, stack.items()):
    a.imshow(np.clip(np.dstack([r["nir"], r["red"], r["green"]]) / np.array([0.45, 0.15, 0.15]), 0, 1)); a.set_title(f"{day} (NIR, R, G)")
ax[-1].imshow(np.ma.masked_less(y_img, 0), cmap=ListedColormap(COLORS), vmin=0, vmax=4, interpolation="nearest"); ax[-1].set_title("WorldCover 2021")
for a in ax: a.axis("off")
plt.show()
''', '''
DATES = ["S2A_33UVR_20240427_0_L2A", "S2B_33UVR_20240721_0_L2A", "S2A_33UVR_20240921_0_L2A"]   # ◀ parameter: images of one year (spring, summer, autumn)
LON, LAT, HALF = 14.37, 50.14, 2000                                                          # ◀ parameter: window centre and half width (m)
stack, clear = {}, None
for item_id in DATES:
    refl, scl, wl, grid, item = s2_window(item_id, LON, LAT, HALF)
    day = item["properties"]["datetime"][:10]
    stack[day] = refl
    m = np.isin(scl, [4, 5, 6])
    clear = m if clear is None else clear & m
    print(f"{item_id}: {day}, cloud-free {m.mean():.1%} of the window")
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
CLASSES = {10: "forest", 30: "grassland", 40: "cropland", 50: "built-up", 80: "water"}
COLORS = ["#2e7d32", "#9ccc65", "#f2c14e", "#c62828", "#1e88e5"]
names = list(CLASSES.values())
y_img = np.full(wc.shape, -1)
for i, k in enumerate(CLASSES):
    y_img[wc == k] = i
ok = clear & (y_img >= 0)
print(f"pixels cloud-free in all images and in the five classes: {ok.sum()} ({ok.mean():.1%})")
fig, ax = plt.subplots(1, len(stack) + 1, figsize=(4 * (len(stack) + 1), 4))
for a, (day, r) in zip(ax, stack.items()):
    a.imshow(np.clip(np.dstack([r["nir"], r["red"], r["green"]]) / np.array([0.45, 0.15, 0.15]), 0, 1)); a.set_title(f"{day} (NIR, R, G)")
ax[-1].imshow(np.ma.masked_less(y_img, 0), cmap=ListedColormap(COLORS), vmin=0, vmax=4, interpolation="nearest"); ax[-1].set_title("WorldCover 2021")
for a in ax: a.axis("off")
plt.show()
''')),
        ("md", t(
            "## 2. Příznaky z časové řady\n\nZ každého snímku vezmeme odrazivost deseti pásem a tři indexy: NDVI (zeleň), NDWI (voda, McFeeters 1996) a NDMI (vlhkost listů). Se třemi snímky má každý pixel 39 příznaků. Indexy jsou ve slovníku `INDICES` jako funkce a můžeš přidat vlastní.",
            "## 2. Features from a time series\n\nFrom every image we take the reflectance of ten bands and three indices: NDVI (greenness), NDWI (water, McFeeters 1996) and NDMI (leaf moisture). With three images every pixel has 39 features. The indices are functions in the `INDICES` dictionary, and you can add your own.")),
        ("code", t('''
INDICES = {                                                  # ◀ parametr: indexy počítané z každého snímku; přidej vlastní
    "NDVI": lambda r: (r["nir"] - r["red"]) / (r["nir"] + r["red"]),
    "NDWI": lambda r: (r["green"] - r["nir"]) / (r["green"] + r["nir"]),
    "NDMI": lambda r: (r["nir08"] - r["swir16"]) / (r["nir08"] + r["swir16"]),
}
FEAT_BANDS = ["blue", "green", "red", "rededge1", "rededge2", "rededge3", "nir", "nir08", "swir16", "swir22"]

def features(days):
    """Příznaky pro zvolené dny: odrazivost pásem a indexy. Vrací pole (řádky, sloupce, příznaky) a jejich názvy."""
    F, N = [], []
    for day in days:
        r = stack[day]
        for b in FEAT_BANDS:
            F.append(r[b]); N.append(f"{b} {day[5:]}")
        for name, f in INDICES.items():
            F.append(f(r)); N.append(f"{name} {day[5:]}")
    return np.dstack(F).astype(np.float32), N

DAYS = list(stack)
X_img, feat_names = features(DAYS)
print(f"{len(feat_names)} příznaků:", ", ".join(feat_names[:8]), "…")
prof = pd.DataFrame({day: [np.median(INDICES["NDVI"](stack[day])[ok & (y_img == i)]) for i in range(5)] for day in DAYS}, index=names)
ax = prof.T.plot(marker="o", color=COLORS, figsize=(7, 3.5)); ax.set(ylabel="medián NDVI", title="časový průběh NDVI podle třídy WorldCover"); plt.show()
prof.round(2)
''', '''
INDICES = {                                                  # ◀ parameter: indices computed from every image; add your own
    "NDVI": lambda r: (r["nir"] - r["red"]) / (r["nir"] + r["red"]),
    "NDWI": lambda r: (r["green"] - r["nir"]) / (r["green"] + r["nir"]),
    "NDMI": lambda r: (r["nir08"] - r["swir16"]) / (r["nir08"] + r["swir16"]),
}
FEAT_BANDS = ["blue", "green", "red", "rededge1", "rededge2", "rededge3", "nir", "nir08", "swir16", "swir22"]

def features(days):
    """Features for the chosen days: band reflectance and indices. Returns an array (rows, columns, features) and their names."""
    F, N = [], []
    for day in days:
        r = stack[day]
        for b in FEAT_BANDS:
            F.append(r[b]); N.append(f"{b} {day[5:]}")
        for name, f in INDICES.items():
            F.append(f(r)); N.append(f"{name} {day[5:]}")
    return np.dstack(F).astype(np.float32), N

DAYS = list(stack)
X_img, feat_names = features(DAYS)
print(f"{len(feat_names)} features:", ", ".join(feat_names[:8]), "…")
prof = pd.DataFrame({day: [np.median(INDICES["NDVI"](stack[day])[ok & (y_img == i)]) for i in range(5)] for day in DAYS}, index=names)
ax = prof.T.plot(marker="o", color=COLORS, figsize=(7, 3.5)); ax.set(ylabel="median NDVI", title="NDVI over time by WorldCover class"); plt.show()
prof.round(2)
''')),
        ("task", t(
            "Jak se mění medián NDVI louky a pole mezi dubnem, červencem a zářím a proč (osev, sklizeň, seč)? Proč je pro rozlišení pole a louky víc snímků lepší než jeden? Přidej do `INDICES` vlastní index, třeba NDRE = (nir − rededge1) / (nir + rededge1), spusť buňky znovu a v kroku 5 sleduj, jestli pomohl.",
            "How does the median NDVI of grassland and cropland change between April, July and September, and why (sowing, harvest, mowing)? Why are several images better than one for telling cropland from grassland? Add your own index to `INDICES`, for example NDRE = (nir − rededge1) / (nir + rededge1), run the cells again and watch in step 5 whether it helped.")),
        ("md", t(
            "## 3. Vlastní klasifikátor minimální vzdálenosti\n\nKlasifikátor minimální vzdálenosti přiřadí pixel třídě, jejíž střed (průměrný vektor příznaků) je nejblíž. Napíšeme ho v numpy na pár řádků a ověříme, že dává totéž co `NearestCentroid` ze scikit-learn. Trénujeme na severní polovině výřezu, testujeme na jižní. Větev pro Mahalanobisovu vzdálenost, která bere v úvahu rozptyl a korelace příznaků uvnitř třídy, doplníš sám.",
            "## 3. Your own minimum distance classifier\n\nThe minimum distance classifier assigns a pixel to the class whose centre (mean feature vector) is nearest. We write it in a few lines of numpy and check that it gives the same as `NearestCentroid` from scikit-learn. We train on the northern half of the window and test on the southern half. You write the branch for the Mahalanobis distance, which takes the spread and correlation of features within a class into account, yourself.")),
        ("code", t('''
rng = np.random.default_rng(0)
n_class = 600                     # ◀ parametr: vzorek pixelů na třídu
idx = np.flatnonzero(ok.ravel())
samp = np.concatenate([rng.choice(idx[y_img.ravel()[idx] == k], n_class, replace=False) for k in range(5)])
X_all = X_img.reshape(-1, X_img.shape[2])
X, y = X_all[samp], y_img.ravel()[samp]
rows_, cols_ = np.unravel_index(samp, y_img.shape)
train = rows_ < y_img.shape[0] // 2                       # sever trénuje, jih testuje
mu_, sd_ = X[train].mean(0), X[train].std(0)
Xs = (X - mu_) / sd_                                      # standardizace: každý příznak má průměr 0 a rozptyl 1

def min_distance(X_train, y_train, X_test, metric="euclid"):
    """Klasifikace minimální vzdáleností od středu třídy."""
    centres = np.array([X_train[y_train == k].mean(0) for k in range(5)])
    if metric == "euclid":
        d = ((X_test[:, None, :] - centres[None, :, :]) ** 2).sum(2)
    elif metric == "mahalanobis":
        raise NotImplementedError("doplň: kovarianční matice každé třídy, její inverze a vzdálenost (x − μ)ᵀ Σ⁻¹ (x − μ)")
    return d.argmin(1)

metric = "euclid"                 # ◀ parametr: "euclid", nebo po doplnění "mahalanobis"
pred = min_distance(Xs[train], y[train], Xs[~train], metric)
sk = NearestCentroid().fit(Xs[train], y[train]).predict(Xs[~train])
print(f"vlastní klasifikátor ({metric}): přesnost na jihu {np.mean(pred == y[~train]):.1%}; shoda se scikit-learn NearestCentroid {np.mean(pred == sk):.1%}")
qda = QuadraticDiscriminantAnalysis(reg_param=1e-3).fit(Xs[train], y[train])
print(f"maximální věrohodnost (QDA) pro srovnání: {qda.score(Xs[~train], y[~train]):.1%}")
''', '''
rng = np.random.default_rng(0)
n_class = 600                     # ◀ parameter: sample of pixels per class
idx = np.flatnonzero(ok.ravel())
samp = np.concatenate([rng.choice(idx[y_img.ravel()[idx] == k], n_class, replace=False) for k in range(5)])
X_all = X_img.reshape(-1, X_img.shape[2])
X, y = X_all[samp], y_img.ravel()[samp]
rows_, cols_ = np.unravel_index(samp, y_img.shape)
train = rows_ < y_img.shape[0] // 2                       # the north trains, the south tests
mu_, sd_ = X[train].mean(0), X[train].std(0)
Xs = (X - mu_) / sd_                                      # standardisation: every feature has mean 0 and variance 1

def min_distance(X_train, y_train, X_test, metric="euclid"):
    """Minimum distance to class centre classification."""
    centres = np.array([X_train[y_train == k].mean(0) for k in range(5)])
    if metric == "euclid":
        d = ((X_test[:, None, :] - centres[None, :, :]) ** 2).sum(2)
    elif metric == "mahalanobis":
        raise NotImplementedError("to do: covariance matrix of each class, its inverse and the distance (x − μ)ᵀ Σ⁻¹ (x − μ)")
    return d.argmin(1)

metric = "euclid"                 # ◀ parameter: "euclid", or "mahalanobis" once you have written it
pred = min_distance(Xs[train], y[train], Xs[~train], metric)
sk = NearestCentroid().fit(Xs[train], y[train]).predict(Xs[~train])
print(f"own classifier ({metric}): accuracy in the south {np.mean(pred == y[~train]):.1%}; agreement with scikit-learn NearestCentroid {np.mean(pred == sk):.1%}")
qda = QuadraticDiscriminantAnalysis(reg_param=1e-3).fit(Xs[train], y[train])
print(f"maximum likelihood (QDA) for comparison: {qda.score(Xs[~train], y[~train]):.1%}")
''')),
        ("task", t(
            "Doplň ve funkci `min_distance` větev `mahalanobis` (kovarianční matice každé třídy z trénovacích pixelů, `np.linalg.inv`, vzdálenost (x − μ)ᵀ Σ⁻¹ (x − μ)) a nastav `metric = \"mahalanobis\"`. Jak se výsledek srovná s eukleidovskou vzdáleností a s QDA? QDA je maximální věrohodnost: proč se od tvé Mahalanobisovy vzdálenosti přesto liší (člen s ln |Σ| a apriorní pravděpodobnosti)? Proč je u eukleidovské vzdálenosti nutná standardizace? Zkus ji vypnout (`Xs = X`).",
            "Write the `mahalanobis` branch in `min_distance` (covariance matrix of each class from the training pixels, `np.linalg.inv`, distance (x − μ)ᵀ Σ⁻¹ (x − μ)) and set `metric = \"mahalanobis\"`. How does the result compare with the Euclidean distance and with QDA? QDA is maximum likelihood: why does it still differ from your Mahalanobis distance (the ln |Σ| term and the prior probabilities)? Why is standardisation needed for the Euclidean distance? Try switching it off (`Xs = X`).")),
        ("md", t(
            "## 4. Náhodná, nebo prostorová validace?\n\nSousední pixely si jsou podobné. Když vzorek rozdělíme na trénovací a testovací náhodně, testovací pixel má často souseda v tréninku a přesnost vyjde příliš dobře. Prostorová validace dělí vzorek po čtvercích: celý čtverec je buď v tréninku, nebo v testu (Roberts a kol. 2017). Porovnáme náhodné rozdělení, čtverce a rozdělení na sever a jih.",
            "## 4. Random or spatial validation?\n\nNeighbouring pixels are similar. If we split the sample into training and test pixels at random, a test pixel often has a neighbour in training and the accuracy comes out too good. Spatial validation splits the sample by squares: a whole square is either in training or in testing (Roberts et al. 2017). We compare a random split, squares, and a north–south split.")),
        ("code", t('''
BLOCK_M = 500                     # ◀ parametr: velikost čtverců pro prostorovou validaci (m)
rf = RandomForestClassifier(200, max_depth=12, random_state=0, n_jobs=-1)
blocks = (rows_ * 10 // BLOCK_M) * 10000 + cols_ * 10 // BLOCK_M
cv = {
    "náhodné rozdělení (KFold)": cross_val_score(rf, X, y, cv=KFold(5, shuffle=True, random_state=0)),
    f"čtverce {BLOCK_M} m (GroupKFold)": cross_val_score(rf, X, y, cv=GroupKFold(5), groups=blocks),
    "sever × jih": np.array([rf.fit(X[train], y[train]).score(X[~train], y[~train]), rf.fit(X[~train], y[~train]).score(X[train], y[train])]),
}
print(f"čtverců s aspoň jedním pixelem vzorku: {len(np.unique(blocks))}")
pd.DataFrame({k: {"průměr": v.mean(), "min": v.min(), "max": v.max()} for k, v in cv.items()}).T.round(3)
''', '''
BLOCK_M = 500                     # ◀ parameter: size of the squares for spatial validation (m)
rf = RandomForestClassifier(200, max_depth=12, random_state=0, n_jobs=-1)
blocks = (rows_ * 10 // BLOCK_M) * 10000 + cols_ * 10 // BLOCK_M
cv = {
    "random split (KFold)": cross_val_score(rf, X, y, cv=KFold(5, shuffle=True, random_state=0)),
    f"squares {BLOCK_M} m (GroupKFold)": cross_val_score(rf, X, y, cv=GroupKFold(5), groups=blocks),
    "north × south": np.array([rf.fit(X[train], y[train]).score(X[~train], y[~train]), rf.fit(X[~train], y[~train]).score(X[train], y[train])]),
}
print(f"squares with at least one sample pixel: {len(np.unique(blocks))}")
pd.DataFrame({k: {"mean": v.mean(), "min": v.min(), "max": v.max()} for k, v in cv.items()}).T.round(3)
''')),
        ("task", t(
            "Proč vychází náhodné rozdělení nejlépe a rozdělení sever × jih nejhůř? Nastav `BLOCK_M` na 200 a 1000 m: jak se mění průměr a rozptyl přesnosti a proč? Kterému číslu bys věřil, kdyby se mapa měla použít na sousedním území, a které bys uvedl ve zprávě?",
            "Why does the random split come out best and the north × south split worst? Set `BLOCK_M` to 200 and 1000 m: how do the mean and spread of accuracy change and why? Which number would you trust if the map were to be used in a neighbouring area, and which would you report?")),
        ("md", t(
            "## 5. Co přinese který snímek\n\nPrůběh v čase odliší třídy, které jsou v jednom okamžiku podobné. Spočítáme přesnost náhodného lesa (prostorová validace po čtvercích) pro každý snímek zvlášť, pro dvojice i pro všechny tři, a míru F1 každé třídy pro letní snímek a pro všechny tři.",
            "## 5. What each image adds\n\nThe course over time separates classes that look alike at one moment. We compute the accuracy of a random forest (spatial validation by squares) for each image alone, for pairs and for all three, and the F1 score of each class for the summer image and for all three.")),
        ("code", t('''
day_of = np.array([n.split()[-1] for n in feat_names])
rows = {}
for r_ in range(1, len(DAYS) + 1):
    for combo in combinations(DAYS, r_):
        cols = np.isin(day_of, [d[5:] for d in combo])
        acc = cross_val_score(rf, X[:, cols], y, cv=GroupKFold(5), groups=blocks)
        rows[" + ".join(d[5:] for d in combo)] = {"příznaků": int(cols.sum()), "přesnost (čtverce)": acc.mean()}
res = pd.DataFrame(rows).T
print(res.round(3).to_string())
one, allc = np.isin(day_of, DAYS[1][5:]), np.ones(len(day_of), bool)
f1 = {}
for label, cols in [(f"jen {DAYS[1][5:]}", one), ("všechny snímky", allc)]:
    pr = cross_val_predict(rf, X[:, cols], y, cv=GroupKFold(5), groups=blocks)
    f1[label] = f1_score(y, pr, average=None)
pd.DataFrame(f1, index=names).round(2)
''', '''
day_of = np.array([n.split()[-1] for n in feat_names])
rows = {}
for r_ in range(1, len(DAYS) + 1):
    for combo in combinations(DAYS, r_):
        cols = np.isin(day_of, [d[5:] for d in combo])
        acc = cross_val_score(rf, X[:, cols], y, cv=GroupKFold(5), groups=blocks)
        rows[" + ".join(d[5:] for d in combo)] = {"features": int(cols.sum()), "accuracy (squares)": acc.mean()}
res = pd.DataFrame(rows).T
print(res.round(3).to_string())
one, allc = np.isin(day_of, DAYS[1][5:]), np.ones(len(day_of), bool)
f1 = {}
for label, cols in [(f"only {DAYS[1][5:]}", one), ("all images", allc)]:
    pr = cross_val_predict(rf, X[:, cols], y, cv=GroupKFold(5), groups=blocks)
    f1[label] = f1_score(y, pr, average=None)
pd.DataFrame(f1, index=names).round(2)
''')),
        ("task", t(
            "Který samotný snímek je nejlepší a která dvojice? O kolik pomohly všechny tři snímky a u které třídy nejvíc? Vysvětli to grafem NDVI z kroku 2. Kdy by další snímek už nepomohl a co by pak pomohlo víc (jiné příznaky, lepší reference, víc trénovacích pixelů)?",
            "Which single image is best, and which pair? How much did all three images help, and for which class most? Explain it with the NDVI plot from step 2. When would another image no longer help, and what would help more then (other features, a better reference, more training pixels)?")),
        ("md", t(
            "## 6. Mapa a odhad ploch s nejistotou\n\nPlocha třídy spočítaná z mapy (počet pixelů krát plocha pixelu) je zatížená chybami klasifikace. Dobrá praxe (Olofsson a kol. 2014) je odhadnout plochu z náhodného vzorku kontrolních pixelů vybraného zvlášť v každé třídě mapy (stratifikovaný výběr) a uvést interval spolehlivosti. Mapu vytvoříme z poloviny čtverců a plochy odhadneme na zbytku území. Referencí je tu WorldCover, který máme pro všechny pixely, takže můžeme odhad porovnat se skutečným součtem.",
            "## 6. A map and area estimates with uncertainty\n\nA class area counted from the map (number of pixels times pixel area) carries the classification errors. Good practice (Olofsson et al. 2014) is to estimate the area from a random sample of check pixels drawn separately in each map class (stratified sampling) and to report a confidence interval. We make the map from half of the squares and estimate areas on the rest of the area. The reference here is WorldCover, which we have for every pixel, so we can compare the estimate with the true total.")),
        ("code", t('''
n_h = 100                         # ◀ parametr: vzorek kontrolních pixelů v každé třídě mapy
blk = (np.indices(y_img.shape)[0] * 10 // BLOCK_M) * 10000 + np.indices(y_img.shape)[1] * 10 // BLOCK_M
ub = np.unique(blk)
train_blocks = rng.choice(ub, len(ub) // 2, replace=False)
in_train = np.isin(blk, train_blocks).ravel() & ok.ravel()
pool = np.flatnonzero(in_train)
tr = np.concatenate([rng.choice(pool[y_img.ravel()[pool] == k], min(400, int((y_img.ravel()[pool] == k).sum())), replace=False) for k in range(5)])
rf.fit(X_all[tr], y_img.ravel()[tr])
mapped = np.full(y_img.size, -1)
mapped[ok.ravel()] = rf.predict(X_all[ok.ravel()])
area = ok.ravel() & ~in_train                              # území mimo trénovací čtverce
W = np.array([np.mean(mapped[area] == h) for h in range(5)])
cm = np.zeros((5, 5))
for h in range(5):
    s = rng.choice(np.flatnonzero(area & (mapped == h)), n_h, replace=False)
    cm[h] = np.bincount(y_img.ravel()[s], minlength=5)
n_i = cm.sum(1, keepdims=True)
p = W[:, None] * cm / n_i                                  # odhad podílů plochy (řádek = mapa, sloupec = reference)
se = np.sqrt((W[:, None] ** 2 * (cm / n_i) * (1 - cm / n_i) / (n_i - 1)).sum(0))
A = area.sum() * 100 / 1e4                                 # ha
out = pd.DataFrame({"z mapy (ha)": W * A, "odhad ze vzorku (ha)": p.sum(0) * A, "± 95 % (ha)": 1.96 * se * A,
                    "WorldCover všech pixelů (ha)": [np.mean(y_img.ravel()[area] == k) * A for k in range(5)],
                    "přesnost uživatele": np.diag(cm) / n_i[:, 0], "přesnost zpracovatele": np.diag(p) / p.sum(0)}, index=names)
print(f"území {A:.0f} ha, celková přesnost {np.trace(p):.1%}, kontrolních pixelů {int(cm.sum())}")
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].imshow(np.ma.masked_less(mapped.reshape(y_img.shape), 0), cmap=ListedColormap(COLORS), vmin=0, vmax=4, interpolation="nearest"); ax[0].set_title("mapa: náhodný les, tři snímky")
ax[1].imshow(np.where(area.reshape(y_img.shape), 1.0, np.nan), cmap="Greys", vmin=0, vmax=2); ax[1].set_title("území pro odhad ploch (mimo trénink)")
for a in ax: a.axis("off")
plt.show()
out.round(2)
''', '''
n_h = 100                         # ◀ parameter: sample of check pixels in each map class
blk = (np.indices(y_img.shape)[0] * 10 // BLOCK_M) * 10000 + np.indices(y_img.shape)[1] * 10 // BLOCK_M
ub = np.unique(blk)
train_blocks = rng.choice(ub, len(ub) // 2, replace=False)
in_train = np.isin(blk, train_blocks).ravel() & ok.ravel()
pool = np.flatnonzero(in_train)
tr = np.concatenate([rng.choice(pool[y_img.ravel()[pool] == k], min(400, int((y_img.ravel()[pool] == k).sum())), replace=False) for k in range(5)])
rf.fit(X_all[tr], y_img.ravel()[tr])
mapped = np.full(y_img.size, -1)
mapped[ok.ravel()] = rf.predict(X_all[ok.ravel()])
area = ok.ravel() & ~in_train                              # area outside the training squares
W = np.array([np.mean(mapped[area] == h) for h in range(5)])
cm = np.zeros((5, 5))
for h in range(5):
    s = rng.choice(np.flatnonzero(area & (mapped == h)), n_h, replace=False)
    cm[h] = np.bincount(y_img.ravel()[s], minlength=5)
n_i = cm.sum(1, keepdims=True)
p = W[:, None] * cm / n_i                                  # estimated area proportions (row = map, column = reference)
se = np.sqrt((W[:, None] ** 2 * (cm / n_i) * (1 - cm / n_i) / (n_i - 1)).sum(0))
A = area.sum() * 100 / 1e4                                 # ha
out = pd.DataFrame({"from the map (ha)": W * A, "estimate from the sample (ha)": p.sum(0) * A, "± 95 % (ha)": 1.96 * se * A,
                    "WorldCover, all pixels (ha)": [np.mean(y_img.ravel()[area] == k) * A for k in range(5)],
                    "user's accuracy": np.diag(cm) / n_i[:, 0], "producer's accuracy": np.diag(p) / p.sum(0)}, index=names)
print(f"area {A:.0f} ha, overall accuracy {np.trace(p):.1%}, check pixels {int(cm.sum())}")
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].imshow(np.ma.masked_less(mapped.reshape(y_img.shape), 0), cmap=ListedColormap(COLORS), vmin=0, vmax=4, interpolation="nearest"); ax[0].set_title("map: random forest, three images")
ax[1].imshow(np.where(area.reshape(y_img.shape), 1.0, np.nan), cmap="Greys", vmin=0, vmax=2); ax[1].set_title("area for the area estimate (outside training)")
for a in ax: a.axis("off")
plt.show()
out.round(2)
''')),
        ("task", t(
            "Které třídy mapa nadhodnocuje a které podhodnocuje? Je blíž součtu WorldCoveru plocha z mapy, nebo odhad ze vzorku, a leží součet v intervalu ±95 %? Nastav `n_h` na 30 a 300: jak se mění interval a proč? V praxi referenci pro všechny pixely nemáš: proč pak plocha z mapy nestačí? A proč ani WorldCover není „pravda“ (jeho celková přesnost je kolem 77 %, Zanaga a kol. 2022)?",
            "Which classes does the map overestimate and which does it underestimate? Is the WorldCover total closer to the map area or to the sample estimate, and does it fall inside the ±95 % interval? Set `n_h` to 30 and 300: how does the interval change and why? In practice you do not have a reference for every pixel: why is the map area not enough then? And why is not even WorldCover the “truth” (its overall accuracy is about 77 %, Zanaga et al. 2022)?")),
        ("task", t(
            "+Vyzkoušej jiné místo: najdi v katalogu Earth Search tři bezoblačné snímky jednoho roku (jaro, léto, podzim), změň `DATES`, `LON` a `LAT` a podle zeměpisné polohy i dlaždici WorldCover v proměnné `WORLDCOVER` (dlaždice 3 × 3°, např. N48E015 pro Moravu). Vyjdou závěry kroků 4 až 6 stejně?",
            "+Try another place: find three cloud-free images of one year (spring, summer, autumn) in the Earth Search catalogue, change `DATES`, `LON` and `LAT`, and the WorldCover tile in the `WORLDCOVER` variable according to the location (3 × 3° tiles, e.g. N48E015 for Moravia). Do the conclusions of steps 4 to 6 hold?")),
    ]
