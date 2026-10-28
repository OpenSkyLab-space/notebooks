"""Build the Czech and English notebooks from one source file per visual.

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


def header(meta, lang):
    t = (lambda cs, en: cs if lang == "cs" else en)
    stem = meta["stem"]
    colab = f"https://colab.research.google.com/github/{REPO}/blob/main/{stem}_{lang}.ipynb"
    other = "en" if lang == "cs" else "cs"
    viz = f"{SITE}/edu_viz_{stem}.html"
    title = meta["title"][lang]
    lines = [
        f"# {title}",
        "",
        f"[![{t('Otevřít v Google Colab', 'Open in Google Colab')}](https://colab.research.google.com/assets/colab-badge.svg)]({colab})",
        "",
        t(f"**OpenSkyLab · notebook k vizuálu** [{meta['visual']['cs']}]({viz}) · [English version]({stem}_{other}.ipynb)",
          f"**OpenSkyLab · notebook for the visual** [{meta['visual']['en']}]({viz}) · [česká verze]({stem}_{other}.ipynb)"),
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
    mod = load(stem)
    meta = dict(mod.META, stem=stem)
    for lang in ("cs", "en"):
        t = (lambda cs, en, _l=lang: cs if _l == "cs" else en)
        nb = nbf.v4.new_notebook()
        nb.metadata = {
            "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
            "language_info": {"name": "python"},
            "colab": {"provenance": [], "toc_visible": True},
        }
        n_all = sum(1 for kind, text in mod.cells(t) if kind == "task" and not text.startswith("+"))
        meta["tasks"] = {"cs": ["", "", "", "", "čtyři", "pět", "šest"][n_all], "en": ["", "", "", "", "four", "five", "six"][n_all]}
        cells = [nbf.v4.new_markdown_cell(header(meta, lang))]
        n_task = 0
        for kind, text in mod.cells(t):
            text = text.strip("\n")
            if kind == "md":
                cells.append(nbf.v4.new_markdown_cell(text))
            elif kind == "code":
                cells.append(nbf.v4.new_code_cell(text))
            elif kind == "task":
                n_task += 1
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
