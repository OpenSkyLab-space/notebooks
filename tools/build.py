"""Build the Czech and English notebooks from one source file per lab.

Usage:
    python tools/build.py              # all sources in src/
    python tools/build.py gnss_sky ... # only these stems

Each src/<stem>.py defines META (dict) and cells(t), where t(cs, en) returns the text in the
language being built. cells() returns a list of (kind, text) with kind in md, code, task, answer.
The notebooks are written without outputs; tools/run.py executes them.
"""
import importlib.util
import pathlib
import sys

import nbformat as nbf

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "OpenSkyLab-space/notebooks"
SITE = "https://openskylab.space"

AI_NOTE = {
    "cs": "Materiál připravil tým OpenSkyLab s pomocí generativní AI Claude (Anthropic), která pomáhala s návrhem kódu a textu. Za obsah odpovídají autoři.",
    "en": "This resource was developed by the OpenSkyLab team with the assistance of the generative AI Claude (Anthropic), used for drafting code and text. The authors are responsible for the content.",
}


def load(stem):
    sys.path.insert(0, str(ROOT / "src"))
    spec = importlib.util.spec_from_file_location(stem, ROOT / "src" / f"{stem}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def units(stem):
    """(notebook stem, META, cells) for every notebook built from src/<stem>.py.

    A source with VARIANTS = {suffix: place} defines meta(place) and cells(t, place) and gives one notebook
    per place, <stem>_<suffix> (the empty suffix keeps <stem>). META["visual_stem"] names the visual
    when it differs from the stem (e.g. the advanced version of a notebook)."""
    mod = load(stem)
    if hasattr(mod, "VARIANTS"):
        return [(f"{stem}_{k}" if k else stem, dict(mod.meta(v), visual_stem=mod.meta(v).get("visual_stem", stem)),
                 lambda t, _v=v: mod.cells(t, _v)) for k, v in mod.VARIANTS.items()]
    return [(stem, dict(mod.META, visual_stem=mod.META.get("visual_stem", stem)), mod.cells)]

# notebooks that take settings from their lab (the cell "Settings from the lab"); advanced versions only where listed
VIZ_STEMS = {"flight_planner", "thermal_timing", "blackbody_radiation", "why_drones_fly", "drone_weather", "eu_rules", "gnss_sky",
             "multispectral_calibration"}
VIZ_PRO = {"eu_rules_pro"}


def viz_cell(stem, lang):
    t = (lambda cs, en: cs if lang == "cs" else en)
    return "\n".join([
        t("#@title Nastavení z laboratoře (nepovinné)", "#@title Settings from the lab (optional)"),
        t("#@markdown V laboratoři klikni na odkaz Notebook. Nastavení se zkopíruje; vlož ho sem místo `{}` (Ctrl+V) a buňku spusť.",
          "#@markdown In the lab, click the Notebook link. The settings are copied; paste them here in place of `{}` (Ctrl+V) and run the cell."),
        'Z_VIZUALU = {}  #@param {type:"raw"}',
        f'STEM = "{stem}"',
        "",
        "def z_viz(name, default, mapping=None):",
        t('    """Hodnota parametru z laboratoře, pokud ji vložený kód obsahuje; jinak výchozí hodnota."""',
          '    """Value of a parameter from the lab if the pasted code contains it; otherwise the default value."""'),
        '    z = Z_VIZUALU if isinstance(Z_VIZUALU, dict) and Z_VIZUALU.get("osl") == STEM else {}',
        "    if name not in z:",
        "        return default",
        "    v = z[name]",
        "    if mapping is not None:",
        "        if v not in mapping:",
        t('            print(f"{name}: hodnota {v!r} z laboratoře v tomto notebooku není, ponechávám {default!r}")',
          '            print(f"{name}: value {v!r} from the lab is not in this notebook, keeping {default!r}")'),
        "            return default",
        "        v = mapping[v]",
        "    elif isinstance(default, bool):",
        "        v = bool(v)",
        "    elif isinstance(default, int):",
        "        v = int(round(v))",
        "    elif isinstance(default, float):",
        "        v = float(v)",
        t('    print(f"{name} = {v!r}  (z laboratoře)")', '    print(f"{name} = {v!r}  (from the lab)")'),
        "    return v",
        "",
        'if isinstance(Z_VIZUALU, dict) and Z_VIZUALU and Z_VIZUALU.get("osl") != STEM:',
        t('''    print(f"Vložený kód je z jiné laboratoře ({Z_VIZUALU.get('osl')}), notebook ho nepoužije.")''',
          '''    print(f"The pasted code is from another lab ({Z_VIZUALU.get('osl')}), the notebook does not use it.")'''),
    ])

def header(meta, lang):
    t = (lambda cs, en: cs if lang == "cs" else en)
    stem = meta["stem"]
    colab = f"https://colab.research.google.com/github/{REPO}/blob/main/{stem}_{lang}.ipynb"
    other = "en" if lang == "cs" else "cs"
    viz = f"{SITE}/edu_viz_{meta['visual_stem']}.html"
    title = meta["title"][lang]
    lines = [
        f"# {title}",
        "",
        f"[![{t('Otevřít v Google Colab', 'Open in Google Colab')}](https://colab.research.google.com/assets/colab-badge.svg)]({colab})",
        "",
        t(f"**OpenSkyLab · notebook k laboratoři** [{meta['visual']['cs']}]({viz}) · [English version]({stem}_{other}.ipynb)",
          f"**OpenSkyLab · notebook for the lab** [{meta['visual']['en']}]({viz}) · [česká verze]({stem}_{other}.ipynb)"),
        "",
        meta["lead"][lang],
        "",
        t("**Cíl:** ", "**Goal:** ") + meta["goal"][lang],
        "",
        t("**Data:** ", "**Data:** ") + meta["data"][lang],
        "",
        t(f"**Úkoly:** {meta['tasks']['cs']}. Odpovědi piš do buněk *Tvoje odpověď* pod úkoly. "
          f"Řádky označené `# ◀ parametr` můžeš měnit a buňku spustit znovu (Shift + Enter).",
          f"**Tasks:** {meta['tasks']['en']}. Write your answers in the *Your answer* cells below the tasks. "
          f"Lines marked `# ◀ parameter` are meant to be changed; run the cell again with Shift + Enter."),
        "",
        t(f"**Čas:** asi {meta['minutes']} min. Potřebuješ Google účet (Colab); nic se neinstaluje do počítače. "
          "Buňky spouštěj popořadě shora dolů.",
          f"**Time:** about {meta['minutes']} min. You need a Google account (Colab); nothing is installed on your computer. "
          "Run the cells in order from top to bottom."),
    ]
    return "\n".join(lines)


def footer(meta, lang):
    t = (lambda cs, en: cs if lang == "cs" else en)
    stem = meta["stem"]
    url = f"https://github.com/{REPO}/blob/main/{stem}_{lang}.ipynb"
    cite = t(f"OpenSkyLab (2026). {meta['title']['cs']} [notebook, výukový materiál], verze {meta['version']}. {url}. Licence CC BY 4.0.",
             f"OpenSkyLab (2026). {meta['title']['en']} [notebook, teaching resource], version {meta['version']}. {url}. Licence CC BY 4.0.")
    src = "\n".join(f"- {s}" for s in meta["sources"][lang])
    return "\n".join([
        "---",
        t("### Zdroje dat a literatura", "### Data sources and references"),
        "",
        src,
        "",
        t("### Jak citovat", "### How to cite"),
        "",
        cite,
        "",
        t("Text a kód notebooku: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
          "Data mají licence svých poskytovatelů (viz výše).",
          "Notebook text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). "
          "Data are under their providers' licences (see above)."),
        "",
        f"*{AI_NOTE[lang]}*",
    ])


def build(stem):
    for out, meta, cells in units(stem):
        build_one(out, dict(meta, stem=out), cells)


def build_one(stem, meta, cells_fn):
    for lang in ("cs", "en"):
        t = (lambda cs, en, _l=lang: cs if _l == "cs" else en)
        nb = nbf.v4.new_notebook()
        nb.metadata = {
            "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
            "language_info": {"name": "python"},
            "colab": {"provenance": [], "toc_visible": True},
        }
        n_all = sum(1 for kind, text in cells_fn(t) if kind == "task" and not text.startswith("+"))
        meta["tasks"] = {"cs": ["", "", "", "", "čtyři", "pět", "šest"][n_all], "en": ["", "", "", "", "four", "five", "six"][n_all]}
        cells = [nbf.v4.new_markdown_cell(header(meta, lang))]
        if meta["visual_stem"] in VIZ_STEMS and (not stem.endswith("_pro") or stem in VIZ_PRO):
            cells.append(nbf.v4.new_code_cell(viz_cell(meta["visual_stem"], lang)))
        n_task = 0
        for kind, text in cells_fn(t):
            text = text.strip("\n")
            if kind == "md":
                cells.append(nbf.v4.new_markdown_cell(text))
            elif kind == "code":
                cells.append(nbf.v4.new_code_cell(text))
            elif kind == "task":
                n_task += not text.startswith("+")
                label = t("Úkol", "Task") + f" {n_task}" if not text.startswith("+") else t("Rozšíření (nepovinné)", "Extension (optional)")
                cells.append(nbf.v4.new_markdown_cell(f"> **✏️ {label}.** " + text.lstrip("+ ").replace("\n", "\n> ")))
                cells.append(nbf.v4.new_markdown_cell(t("*Tvoje odpověď:* ", "*Your answer:* ")))
            else:
                raise ValueError(kind)
        cells.append(nbf.v4.new_markdown_cell(footer(meta, lang)))
        assert 4 <= n_task <= 6, (stem, n_task)
        nb.cells = cells
        for i, c in enumerate(nb.cells):
            c["id"] = f"{stem[:20]}-{i:02d}"
        nbf.write(nb, ROOT / f"{stem}_{lang}.ipynb")
    print("built", stem)


if __name__ == "__main__":
    stems = sys.argv[1:] or sorted(p.stem for p in (ROOT / "src").glob("*.py") if not p.stem.startswith("_"))
    for s in stems:
        build(s)
