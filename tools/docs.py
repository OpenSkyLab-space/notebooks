"""Write a description of every notebook (docs/<lang>/<stem>.md) from the same source as the notebook.

Usage:
    python tools/docs.py              # all sources in src/
    python tools/docs.py gnss_sky ... # only these stems

The description lists what the notebook does step by step, its parameters and tasks, the data and
the sources, so it can go on the web next to the visual without drifting from the notebook.
"""
import re
import sys

from build import AI_NOTE, REPO, ROOT, SITE, load

PARAM = re.compile(r"^\s*(?P<code>.+?)\s*#\s*◀\s*(?:parametr|parameter):\s*(?P<text>.+)$")
COUNT = {"cs": ["", "", "", "", "čtyři", "pět", "šest"], "en": ["", "", "", "", "four", "five", "six"]}


def steps(cells):
    """Group the cells into numbered sections: heading, explanation, parameters, tasks, packages."""
    out = []
    for kind, text in cells:
        text = text.strip("\n")
        if kind == "md" and text.startswith("## "):
            head, _, body = text.partition("\n")
            out.append({"title": head[3:].strip(), "body": [body.strip()] if body.strip() else [], "params": [], "tasks": [], "pip": []})
        elif kind == "md":
            out[-1]["body"].append(text)
        elif kind == "code":
            for line in text.splitlines():
                if line.startswith("%pip"):
                    out[-1]["pip"] += [p.strip('"') for p in line.split()[3:]]
                m = PARAM.match(line)
                if m:
                    out[-1]["params"].append((m["code"], m["text"]))
        elif kind == "task":
            out[-1]["tasks"].append(text.lstrip("+ "))
    return out


def page(stem, lang):
    mod = load(stem)
    meta = mod.META
    t = (lambda cs, en: cs if lang == "cs" else en)
    sec = steps(mod.cells(t))
    n_tasks = sum(len(s["tasks"]) for s in sec)
    pips = sorted({p.split("[")[0] for s in sec for p in s["pip"]})
    colab = f"https://colab.research.google.com/github/{REPO}/blob/main/{stem}_{lang}.ipynb"
    lines = [
        f"# {meta['title'][lang]}",
        "",
        t(f"Popis notebooku k vizuálu [{meta['visual']['cs']}]({SITE}/edu_viz_{stem}.html). "
          f"[Otevřít v Google Colab]({colab}) · verze {meta['version']} · asi {meta['minutes']} min · {COUNT['cs'][n_tasks]} úkolů",
          f"Description of the notebook for the visual [{meta['visual']['en']}]({SITE}/edu_viz_{stem}.html). "
          f"[Open in Google Colab]({colab}) · version {meta['version']} · about {meta['minutes']} min · {COUNT['en'][n_tasks]} tasks"),
        "",
        t("## O čem notebook je", "## What the notebook is about"),
        "",
        meta["lead"][lang],
        "",
        t("## Cíl", "## Goal"),
        "",
        meta["goal"][lang][0].upper() + meta["goal"][lang][1:],
        "",
        t("## Data", "## Data"),
        "",
        meta["data"][lang],
        "",
        t("Všechna data jsou otevřená a stahují se přímo v notebooku při spuštění, bez registrace a bez klíčů. "
          "Uložené výstupy v notebooku pocházejí ze skutečného běhu; při novém spuštění se čísla mohou lišit, pokud se data průběžně aktualizují.",
          "All data are open and are downloaded inside the notebook when it runs, with no registration and no keys. "
          "The stored outputs come from a real run; a new run may give different numbers where the data are updated continuously."),
        "",
        t("## Postup krok za krokem", "## Step by step"),
        "",
    ]
    n = 0
    for s in sec:
        lines += [f"### {s['title']}", ""]
        body = s["body"] or ([t("Nainstaluje knihovny, které Colab nemá předem (" + ", ".join(f"`{p}`" for p in pips) + "), a stáhne data.",
                                "Installs the libraries Colab lacks (" + ", ".join(f"`{p}`" for p in pips) + ") and downloads the data.")]
                             if s["pip"] else [t("Načte knihovny a stáhne data.", "Loads the libraries and downloads the data.")])
        lines += [b + "\n" for b in body]
        if s["params"]:
            lines += [t("Parametry, které student mění:", "Parameters the student changes:"), ""]
            lines += [f"- `{code}`: {text}" for code, text in s["params"]] + [""]
        for task in s["tasks"]:
            n += 1
            lines += [f"**{t('Úkol', 'Task')} {n}.** {task}", ""]
    lines += [
        t("## Co je potřeba", "## Requirements"),
        "",
        t("Google účet a prohlížeč; notebook běží v Google Colab a nic se neinstaluje do počítače. "
          "Buňky se spouštějí popořadě shora dolů, odpovědi se píšou do buněk *Tvoje odpověď* pod úkoly.",
          "A Google account and a browser; the notebook runs in Google Colab and nothing is installed on the computer. "
          "Cells are run in order from top to bottom, answers go into the *Your answer* cells below the tasks."),
        "",
        t("## Zdroje dat a literatura", "## Data sources and references"),
        "",
    ]
    lines += [f"- {s}" for s in meta["sources"][lang]]
    lines += [
        "",
        "---",
        "",
        t("Text a kód: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů (viz výše).",
          "Text and code: OpenSkyLab, licence [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data are under their providers' licences (see above)."),
        "",
        f"*{AI_NOTE[lang]}*",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    stems = sys.argv[1:] or sorted(p.stem for p in (ROOT / "src").glob("*.py") if not p.stem.startswith("_"))
    for stem in stems:
        for lang in ("cs", "en"):
            out = ROOT / "docs" / lang / f"{stem}.md"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(page(stem, lang), encoding="utf-8")
        print("docs", stem)
