from _common import S2_HELPERS

META = {
    "version": "1.0",
    "minutes": 50,
    "title": {"cs": "Od pixelu ke třídě: klasifikace Sentinelu-2 u Roztok", "en": "From pixel to class: classifying Sentinel-2 near Roztoky"},
    "visual": {"cs": "Od pixelu ke třídě", "en": "From pixel to class"},
    "lead": {
        "cs": "Ve vizuálu jsi dělil pixely prahem indexu, porovnával klasické klasifikátory a sledoval, jak se neuronová síť přeučí. Tady totéž uděláš na skutečném snímku Sentinel-2 od Roztok s referencí ESA WorldCover a přesnost vyhodnotíš chybovou maticí.",
        "en": "In the visual you split pixels with an index threshold, compared classic classifiers and watched a neural network overfit. Here you do the same on a real Sentinel-2 image near Roztoky with ESA WorldCover as reference and assess accuracy with a confusion matrix.",
    },
    "goal": {
        "cs": "najít práh NDVI a SAVI pro vegetaci, porovnat minimální vzdálenost, maximální věrohodnost, k-NN, náhodný les a neuronovou síť na trénovacích a testovacích pixelech a spočítat přesnost zpracovatele, uživatele a kappa.",
        "en": "find an NDVI and SAVI threshold for vegetation, compare minimum distance, maximum likelihood, k-NN, random forest and a neural network on training and test pixels, and compute producer's and user's accuracy and kappa.",
    },
    "data": {
        "cs": "Sentinel-2 L2A `S2B_33UVR_20240721_0_L2A` (21. 7. 2024) z katalogu Earth Search na AWS, výřez 4 × 4 km kolem Roztok a Suchdola; reference ESA WorldCover 10 m 2021 v200. Stahuje se asi 20 MB.",
        "en": "Sentinel-2 L2A `S2B_33UVR_20240721_0_L2A` (21 July 2024) from the Earth Search catalogue on AWS, a 4 × 4 km window around Roztoky and Suchdol; reference ESA WorldCover 10 m 2021 v200. About 20 MB is downloaded.",
    },
    "sources": {
        "cs": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); registr AWS Open Data (`sentinel-cogs`), katalog Earth Search (Element 84). Volné užití s uvedením zdroje.",
            "Zanaga, D. a kol. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Huete, A. R. (1988). A soil-adjusted vegetation index (SAVI). *Remote Sensing of Environment* 25, 295–309. https://doi.org/10.1016/0034-4257(88)90106-X",
            "Congalton, R. G., Green, K. (2019). *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices*, 3. vyd. CRC Press.",
            "Pedregosa, F. a kol. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.",
        ],
        "en": [
            "Copernicus Sentinel-2 data 2024, ESA (L2A, Sen2Cor); AWS Open Data registry (`sentinel-cogs`), Earth Search catalogue (Element 84). Free use with attribution.",
            "Zanaga, D. et al. (2022). *ESA WorldCover 10 m 2021 v200*. https://doi.org/10.5281/zenodo.7254221 (CC BY 4.0).",
            "Huete, A. R. (1988). A soil-adjusted vegetation index (SAVI). *Remote Sensing of Environment* 25, 295–309. https://doi.org/10.1016/0034-4257(88)90106-X",
            "Congalton, R. G., Green, K. (2019). *Assessing the Accuracy of Remotely Sensed Data: Principles and Practices*, 3rd ed. CRC Press.",
            "Pedregosa, F. et al. (2011). Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 12, 2825–2830.",
        ],
    },
}


def cells(t):
    return [
        ("md", t("## 1. Příprava a data", "## 1. Setup and data")),
        ("code", "%pip install -q rasterio"),
        ("code", '''
import requests, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import rasterio
from rasterio.warp import reproject, Resampling
from pyproj import Transformer
from sklearn.neighbors import NearestCentroid, KNeighborsClassifier
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, cohen_kappa_score
warnings.filterwarnings("ignore")
''' + t(S2_HELPERS["cs"], S2_HELPERS["en"])),
        ("code", t('''
refl, scl, wl, grid, item = s2_window("S2B_33UVR_20240721_0_L2A", 14.37, 50.14, 2000)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
CLASSES = {10: "les", 30: "louka", 40: "pole", 50: "zástavba", 80: "voda"}
COLORS = ["#2e7d32", "#9ccc65", "#f2c14e", "#c62828", "#1e88e5"]
FEAT = ["blue", "green", "red", "nir", "swir16", "swir22"]
X_img = np.dstack([refl[b] for b in FEAT])
ok = np.isin(scl, [4, 5, 6]) & np.isin(wc, list(CLASSES))
print("pixely podle třídy WorldCover:", {CLASSES[k]: int(((wc == k) & ok).sum()) for k in CLASSES})
fig, ax = plt.subplots(1, 2, figsize=(11, 5))
ax[0].imshow(np.clip(np.dstack([refl["red"], refl["green"], refl["blue"]]) / 0.15, 0, 1)); ax[0].set_title("Sentinel-2, 21. 7. 2024")
lab = np.full(wc.shape, np.nan); [lab.__setitem__(wc == k, i) for i, k in enumerate(CLASSES)]
ax[1].imshow(lab, cmap=ListedColormap(COLORS), vmin=0, vmax=4, interpolation="nearest"); ax[1].set_title("ESA WorldCover 2021 (reference)")
for a in ax: a.axis("off")
plt.show()
''', '''
refl, scl, wl, grid, item = s2_window("S2B_33UVR_20240721_0_L2A", 14.37, 50.14, 2000)
wc = read_on_grid(WORLDCOVER, grid, Resampling.nearest, np.uint8)
CLASSES = {10: "forest", 30: "meadow", 40: "field", 50: "built-up", 80: "water"}
COLORS = ["#2e7d32", "#9ccc65", "#f2c14e", "#c62828", "#1e88e5"]
FEAT = ["blue", "green", "red", "nir", "swir16", "swir22"]
X_img = np.dstack([refl[b] for b in FEAT])
ok = np.isin(scl, [4, 5, 6]) & np.isin(wc, list(CLASSES))
print("pixels per WorldCover class:", {CLASSES[k]: int(((wc == k) & ok).sum()) for k in CLASSES})
fig, ax = plt.subplots(1, 2, figsize=(11, 5))
ax[0].imshow(np.clip(np.dstack([refl["red"], refl["green"], refl["blue"]]) / 0.15, 0, 1)); ax[0].set_title("Sentinel-2, 21 July 2024")
lab = np.full(wc.shape, np.nan); [lab.__setitem__(wc == k, i) for i, k in enumerate(CLASSES)]
ax[1].imshow(lab, cmap=ListedColormap(COLORS), vmin=0, vmax=4, interpolation="nearest"); ax[1].set_title("ESA WorldCover 2021 (reference)")
for a in ax: a.axis("off")
plt.show()
''')),
        ("md", t(
            "## 2. Práh NDVI: dvě chyby proti sobě\n\nVegetace = les, louka a pole podle WorldCover, ostatní = zástavba a voda. Pro každý práh spočítáme, kolik vegetace přehlédneme a kolik ne-vegetace označíme jako vegetaci.",
            "## 2. NDVI threshold: two errors against each other\n\nVegetation = forest, meadow and field according to WorldCover, the rest = built-up and water. For each threshold we count how much vegetation we miss and how much non-vegetation we label as vegetation.")),
        ("code", t('''
L = 0.5            # ◀ parametr: korekční faktor půdy pro SAVI (0 = NDVI, 0,5 obvykle, 1 řídký porost)
nir, red = refl["nir"], refl["red"]
ndvi = (nir - red) / (nir + red)
savi = (1 + L) * (nir - red) / (nir + red + L)
veg = np.isin(wc, [10, 30, 40])
fig, ax = plt.subplots(1, 2, figsize=(12, 3.8))
for a, (name, idx) in zip(ax, [("NDVI", ndvi), (f"SAVI (L = {L})", savi)]):
    thr = np.linspace(-0.2, 0.9, 111)
    miss = [np.mean(idx[ok & veg] < t_) for t_ in thr]          # vegetace přehlédnutá
    false = [np.mean(idx[ok & ~veg] >= t_) for t_ in thr]       # zástavba a voda jako vegetace
    total = [np.mean((idx[ok] >= t_) == veg[ok]) for t_ in thr]
    best = thr[int(np.argmax(total))]
    a.plot(thr, miss, label="vegetace přehlédnutá"); a.plot(thr, false, label="ostatní jako vegetace"); a.plot(thr, total, "k", label="celková přesnost")
    a.axvline(best, color="gray", ls=":"); a.set(xlabel=name, title=f"{name}: nejlepší práh {best:.2f}, přesnost {max(total):.1%}")
ax[0].legend(); plt.show()
''', '''
L = 0.5            # ◀ parameter: SAVI soil adjustment factor (0 = NDVI, 0.5 usual, 1 sparse vegetation)
nir, red = refl["nir"], refl["red"]
ndvi = (nir - red) / (nir + red)
savi = (1 + L) * (nir - red) / (nir + red + L)
veg = np.isin(wc, [10, 30, 40])
fig, ax = plt.subplots(1, 2, figsize=(12, 3.8))
for a, (name, idx) in zip(ax, [("NDVI", ndvi), (f"SAVI (L = {L})", savi)]):
    thr = np.linspace(-0.2, 0.9, 111)
    miss = [np.mean(idx[ok & veg] < t_) for t_ in thr]          # vegetation missed
    false = [np.mean(idx[ok & ~veg] >= t_) for t_ in thr]       # built-up and water as vegetation
    total = [np.mean((idx[ok] >= t_) == veg[ok]) for t_ in thr]
    best = thr[int(np.argmax(total))]
    a.plot(thr, miss, label="vegetation missed"); a.plot(thr, false, label="other as vegetation"); a.plot(thr, total, "k", label="overall accuracy")
    a.axvline(best, color="gray", ls=":"); a.set(xlabel=name, title=f"{name}: best threshold {best:.2f}, accuracy {max(total):.1%}")
ax[0].legend(); plt.show()
''')),
        ("task", t(
            "Jaký práh NDVI je nejlepší a jaké chyby při něm zůstávají? Proč se nedá zbavit obou chyb současně? Které pixely „vegetace“ mají NDVI nízké (podívej se na pole po žních) a proč je podle WorldCover počítáme jako vegetaci?",
            "Which NDVI threshold is best and which errors remain? Why can you not get rid of both errors at once? Which “vegetation” pixels have a low NDVI (look at harvested fields) and why are they counted as vegetation in WorldCover?")),
        ("task", t(
            "Porovnej NDVI a SAVI. Nastav `L = 0`, `0.25` a `1`. Jak se mění rozsah hodnot a nejlepší práh? Proč SAVI méně závisí na jasu půdy a proč v hustém porostu na tom skoro nezáleží?",
            "Compare NDVI and SAVI. Set `L = 0`, `0.25` and `1`. How do the range of values and the best threshold change? Why does SAVI depend less on soil brightness and why does it hardly matter in dense vegetation?")),
        ("md", t(
            "## 3. Trénovací a testovací pixely\n\nSousední pixely jsou si podobné, takže náhodné rozdělení by přesnost nadsadilo. Trénujeme proto na severní polovině výřezu a testujeme na jižní.",
            "## 3. Training and test pixels\n\nNeighbouring pixels are similar, so a random split would overstate accuracy. We therefore train on the northern half of the window and test on the southern half.")),
        ("code", t('''
n_train = 300      # ◀ parametr: počet trénovacích pixelů na třídu
rng = np.random.default_rng(1)
rows_ = np.arange(wc.shape[0])[:, None].repeat(wc.shape[1], 1)
def sample(mask, n):
    X, y = [], []
    for i, k in enumerate(CLASSES):
        idx = np.flatnonzero((mask & (wc == k)).ravel())
        idx = rng.choice(idx, min(n, len(idx)), replace=False)
        X.append(X_img.reshape(-1, len(FEAT))[idx]); y += [i] * len(idx)
    return np.vstack(X), np.array(y)
north, south = ok & (rows_ < wc.shape[0] // 2), ok & (rows_ >= wc.shape[0] // 2)
Xtr, ytr = sample(north, n_train)
Xte, yte = sample(south, 2000)
print("trénink:", np.bincount(ytr), "test:", np.bincount(yte))
names = list(CLASSES.values())

def report(model, title):
    pred = model.predict(Xte)
    cm = confusion_matrix(yte, pred, labels=range(5))
    pa, ua = np.diag(cm) / cm.sum(1), np.diag(cm) / np.maximum(cm.sum(0), 1)
    tab = pd.DataFrame(cm.astype(object), index=[f"ref {n}" for n in names], columns=names)
    tab["PA"] = pa.round(2); tab.loc["UA"] = list(ua.round(2)) + [""]
    print(f"{title}: celková přesnost test {np.mean(pred == yte):.1%}, trénink {model.score(Xtr, ytr):.1%}, kappa {cohen_kappa_score(yte, pred):.2f}")
    return tab
''', '''
n_train = 300      # ◀ parameter: number of training pixels per class
rng = np.random.default_rng(1)
rows_ = np.arange(wc.shape[0])[:, None].repeat(wc.shape[1], 1)
def sample(mask, n):
    X, y = [], []
    for i, k in enumerate(CLASSES):
        idx = np.flatnonzero((mask & (wc == k)).ravel())
        idx = rng.choice(idx, min(n, len(idx)), replace=False)
        X.append(X_img.reshape(-1, len(FEAT))[idx]); y += [i] * len(idx)
    return np.vstack(X), np.array(y)
north, south = ok & (rows_ < wc.shape[0] // 2), ok & (rows_ >= wc.shape[0] // 2)
Xtr, ytr = sample(north, n_train)
Xte, yte = sample(south, 2000)
print("training:", np.bincount(ytr), "test:", np.bincount(yte))
names = list(CLASSES.values())

def report(model, title):
    pred = model.predict(Xte)
    cm = confusion_matrix(yte, pred, labels=range(5))
    pa, ua = np.diag(cm) / cm.sum(1), np.diag(cm) / np.maximum(cm.sum(0), 1)
    tab = pd.DataFrame(cm.astype(object), index=[f"ref {n}" for n in names], columns=names)
    tab["PA"] = pa.round(2); tab.loc["UA"] = list(ua.round(2)) + [""]
    print(f"{title}: overall accuracy test {np.mean(pred == yte):.1%}, training {model.score(Xtr, ytr):.1%}, kappa {cohen_kappa_score(yte, pred):.2f}")
    return tab
''')),
        ("md", t(
            "## 4. Minimální vzdálenost a maximální věrohodnost",
            "## 4. Minimum distance and maximum likelihood")),
        ("code", t('''
mind = NearestCentroid().fit(Xtr, ytr)
display(report(mind, "Minimální vzdálenost"))
ml = QuadraticDiscriminantAnalysis(reg_param=1e-3).fit(Xtr, ytr)      # gaussovská maximální věrohodnost
display(report(ml, "Maximální věrohodnost"))
''', '''
mind = NearestCentroid().fit(Xtr, ytr)
display(report(mind, "Minimum distance"))
ml = QuadraticDiscriminantAnalysis(reg_param=1e-3).fit(Xtr, ytr)      # Gaussian maximum likelihood
display(report(ml, "Maximum likelihood"))
''')),
        ("task", t(
            "Čti chybovou matici maximální věrohodnosti: řádky jsou reference, sloupce výsledek. Která třída má nízkou přesnost zpracovatele (PA, je přehlížená) a která nízkou přesnost uživatele (UA, jiné třídy se do ní propadají)? Které dvojice tříd se nejvíc pletou a proč? Která z obou metod vyšla lépe? Maximální věrohodnost počítá s rozptylem a korelací pásem v každé třídě; proč přesto nemusí vyhrát (třídy nejsou normálně rozdělené, louka a les mají podobné spektrum, reference má chyby)?",
            "Read the maximum likelihood confusion matrix: rows are the reference, columns the result. Which class has a low producer's accuracy (PA, it is missed) and which a low user's accuracy (UA, other classes fall into it)? Which pairs of classes are confused most and why? Which of the two methods did better? Maximum likelihood accounts for the spread and correlation of bands within each class; why might it still not win (classes are not normally distributed, meadow and forest have similar spectra, the reference has errors)?")),
        ("md", t(
            "## 5. Jak složitý model? k-NN a náhodný les",
            "## 5. How complex a model? k-NN and random forest")),
        ("code", t('''
ks = [1, 3, 5, 10, 25, 50, 100]
depths = [1, 2, 3, 5, 8, 12, None]
acc = {"k-NN trénink": [], "k-NN test": [], "les trénink": [], "les test": []}
for k_ in ks:
    m = KNeighborsClassifier(k_).fit(Xtr, ytr); acc["k-NN trénink"].append(m.score(Xtr, ytr)); acc["k-NN test"].append(m.score(Xte, yte))
for d in depths:
    m = RandomForestClassifier(200, max_depth=d, random_state=0, n_jobs=-1).fit(Xtr, ytr)
    acc["les trénink"].append(m.score(Xtr, ytr)); acc["les test"].append(m.score(Xte, yte))
fig, ax = plt.subplots(1, 2, figsize=(12, 3.6))
ax[0].plot(ks, acc["k-NN trénink"], "o-", label="trénink"); ax[0].plot(ks, acc["k-NN test"], "s-", label="test")
ax[0].set(xscale="log", xlabel="k (počet sousedů)", ylabel="celková přesnost", title="k-NN"); ax[0].legend()
lbl = [str(d) for d in depths]
ax[1].plot(lbl, acc["les trénink"], "o-", label="trénink"); ax[1].plot(lbl, acc["les test"], "s-", label="test")
ax[1].set(xlabel="max. hloubka stromu", title="náhodný les (200 stromů)"); ax[1].legend(); plt.show()
''', '''
ks = [1, 3, 5, 10, 25, 50, 100]
depths = [1, 2, 3, 5, 8, 12, None]
acc = {"k-NN training": [], "k-NN test": [], "forest training": [], "forest test": []}
for k_ in ks:
    m = KNeighborsClassifier(k_).fit(Xtr, ytr); acc["k-NN training"].append(m.score(Xtr, ytr)); acc["k-NN test"].append(m.score(Xte, yte))
for d in depths:
    m = RandomForestClassifier(200, max_depth=d, random_state=0, n_jobs=-1).fit(Xtr, ytr)
    acc["forest training"].append(m.score(Xtr, ytr)); acc["forest test"].append(m.score(Xte, yte))
fig, ax = plt.subplots(1, 2, figsize=(12, 3.6))
ax[0].plot(ks, acc["k-NN training"], "o-", label="training"); ax[0].plot(ks, acc["k-NN test"], "s-", label="test")
ax[0].set(xscale="log", xlabel="k (number of neighbours)", ylabel="overall accuracy", title="k-NN"); ax[0].legend()
lbl = [str(d) for d in depths]
ax[1].plot(lbl, acc["forest training"], "o-", label="training"); ax[1].plot(lbl, acc["forest test"], "s-", label="test")
ax[1].set(xlabel="max. tree depth", title="random forest (200 trees)"); ax[1].legend(); plt.show()
''')),
        ("task", t(
            "Při k = 1 je přesnost na trénovacích pixelech 100 % nebo skoro 100 %. Proč to nic neznamená? Které k a jaká hloubka stromů dávají nejlepší testovací přesnost? Popiš, jak vypadá přeučení a nedoučení v obou grafech.",
            "With k = 1 the accuracy on training pixels is 100 % or nearly so. Why does that mean nothing? Which k and which tree depth give the best test accuracy? Describe what overfitting and underfitting look like in both plots.")),
        ("md", t(
            "## 6. Neuronová síť a přeučení\n\nMalá síť s jednou skrytou vrstvou. Učíme ji na málo pixelech a sledujeme přesnost na tréninku a testu po epochách.",
            "## 6. A neural network and overfitting\n\nA small network with one hidden layer. We train it on few pixels and watch training and test accuracy over the epochs.")),
        ("code", t('''
hidden = 64        # ◀ parametr: počet skrytých neuronů
n_small = 30       # ◀ parametr: trénovacích pixelů na třídu (malý vzorek se snáz přeučí)
Xs, ys = sample(north, n_small)
mu, sd = Xs.mean(0), Xs.std(0)
net = MLPClassifier((hidden,), learning_rate_init=0.01, alpha=0.0, random_state=0)
hist = []
for epoch in range(400):
    net.partial_fit((Xs - mu) / sd, ys, classes=range(5))
    hist.append((net.score((Xs - mu) / sd, ys), net.score((Xte - mu) / sd, yte)))
hist = np.array(hist)
plt.figure(figsize=(8, 3.5)); plt.plot(hist[:, 0], label="trénink"); plt.plot(hist[:, 1], label="test")
plt.xlabel("epocha"); plt.ylabel("celková přesnost"); plt.title(f"síť {hidden} neuronů, {n_small} pixelů na třídu"); plt.legend(); plt.show()
print(f"konec: trénink {hist[-1, 0]:.1%}, test {hist[-1, 1]:.1%}; nejlepší test {hist[:, 1].max():.1%} v epoše {hist[:, 1].argmax()}")
''', '''
hidden = 64        # ◀ parameter: number of hidden neurons
n_small = 30       # ◀ parameter: training pixels per class (a small sample overfits more easily)
Xs, ys = sample(north, n_small)
mu, sd = Xs.mean(0), Xs.std(0)
net = MLPClassifier((hidden,), learning_rate_init=0.01, alpha=0.0, random_state=0)
hist = []
for epoch in range(400):
    net.partial_fit((Xs - mu) / sd, ys, classes=range(5))
    hist.append((net.score((Xs - mu) / sd, ys), net.score((Xte - mu) / sd, yte)))
hist = np.array(hist)
plt.figure(figsize=(8, 3.5)); plt.plot(hist[:, 0], label="training"); plt.plot(hist[:, 1], label="test")
plt.xlabel("epoch"); plt.ylabel("overall accuracy"); plt.title(f"network with {hidden} neurons, {n_small} pixels per class"); plt.legend(); plt.show()
print(f"end: training {hist[-1, 0]:.1%}, test {hist[-1, 1]:.1%}; best test {hist[:, 1].max():.1%} at epoch {hist[:, 1].argmax()}")
''')),
        ("task", t(
            "Vyzkoušej `hidden` 4, 64 a 256 a `n_small` 30 a 300. Kdy se síť přeučí (trénink roste, test klesá nebo stagnuje)? Co by pomohlo: víc dat, menší síť, nebo zastavit učení dřív? Proč je rozdíl trénink–test u sítě větší než u maximální věrohodnosti?",
            "Try `hidden` 4, 64 and 256 and `n_small` 30 and 300. When does the network overfit (training rises, test falls or stalls)? What would help: more data, a smaller network or stopping earlier? Why is the training–test gap larger for the network than for maximum likelihood?")),
        ("md", t("## 7. Mapa výsledku", "## 7. Result map")),
        ("code", t('''
best = RandomForestClassifier(200, max_depth=12, random_state=0, n_jobs=-1).fit(Xtr, ytr)
display(report(best, "Náhodný les, hloubka 12"))
pred = best.predict(X_img.reshape(-1, len(FEAT))).reshape(wc.shape).astype(float)
pred[~np.isin(scl, [4, 5, 6])] = np.nan
fig, ax = plt.subplots(1, 2, figsize=(11, 5))
for a, (img, title) in zip(ax, [(lab, "WorldCover 2021"), (pred, "náhodný les, Sentinel-2 2024")]):
    a.imshow(img, cmap=ListedColormap(COLORS), vmin=0, vmax=4, interpolation="nearest"); a.set_title(title); a.axis("off")
a.axhline(wc.shape[0] / 2, color="w", lw=1); plt.show()
''', '''
best = RandomForestClassifier(200, max_depth=12, random_state=0, n_jobs=-1).fit(Xtr, ytr)
display(report(best, "Random forest, depth 12"))
pred = best.predict(X_img.reshape(-1, len(FEAT))).reshape(wc.shape).astype(float)
pred[~np.isin(scl, [4, 5, 6])] = np.nan
fig, ax = plt.subplots(1, 2, figsize=(11, 5))
for a, (img, title) in zip(ax, [(lab, "WorldCover 2021"), (pred, "random forest, Sentinel-2 2024")]):
    a.imshow(img, cmap=ListedColormap(COLORS), vmin=0, vmax=4, interpolation="nearest"); a.set_title(title); a.axis("off")
a.axhline(wc.shape[0] / 2, color="w", lw=1); plt.show()
''')),
        ("task", t(
            "Najdi místa, kde se mapa liší od WorldCover. Je chyba vždy v klasifikaci? Uvažuj o tom, že WorldCover je z roku 2021 a sám má chyby, že jeden snímek z léta nerozliší louku od pole s pícninou a že pixel 10 m na okraji lesa je směs. Jak bys přesnost hodnotil poctivě?",
            "Find places where the map differs from WorldCover. Is the error always in the classification? Consider that WorldCover is from 2021 and has errors of its own, that a single summer image cannot tell a meadow from a field of forage crops, and that a 10 m pixel at a forest edge is a mixture. How would you assess accuracy honestly?")),
    ]
