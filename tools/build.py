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
import re
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

# The "Settings from the lab" cell: False builds every notebook with plain parameter values instead
# (z_viz("NAME", default) becomes default) and without the cell.
LAB_SETTINGS = True

Z_VIZ = re.compile(r'z_viz\(\s*"[^"]+"\s*,\s*')


LINE_LENGTH = 88
PARAM_TAG = re.compile(r"^#\s*◀\s*(?P<kw>parametr|parameter)(?::\s*(?P<text>.*))?$")


def _sentence(text):
    text = text.strip()
    return text[:1].upper() + text[1:] + ("" if text.endswith((".", "!", "?", ":")) else ".")


def lift_comments(code):
    """Move an inline comment onto its own line above when the line would exceed LINE_LENGTH.

    A parameter tag stays inline: "# ◀ parametr: label (detail)" keeps the label inline and lifts the
    detail; if even that is too long, the whole description is lifted and only "# ◀ parametr" stays.
    """
    import io
    import tokenize
    lines = code.split("\n")
    masked = "\n".join("#" * len(line) if line.lstrip().startswith(("%", "!")) else line for line in lines)
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(masked + "\n").readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return code
    for tok in reversed(toks):
        if tok.type != tokenize.COMMENT:
            continue
        row, col = tok.start[0] - 1, tok.start[1]
        line = lines[row]
        head = line[:col].rstrip()
        if not head.strip() or len(f"{head}  {tok.string}") <= LINE_LENGTH:
            continue
        indent = line[: len(line) - len(line.lstrip())]
        m = PARAM_TAG.match(tok.string)
        if m and m["text"]:
            text, tag = m["text"], f"# ◀ {m['kw']}"
            pm = re.match(r"^(?P<main>[^()]+) \((?P<detail>[^()]+)\)$", text)
            if pm and len(f"{head}  {tag}: {pm['main']}") <= LINE_LENGTH:
                above, inline = pm["detail"], f"{head}  {tag}: {pm['main']}"
            else:
                above, inline = text, f"{head}  {tag}"
        elif m:
            continue
        else:
            above, inline = tok.string.lstrip("# "), head
        import textwrap
        wrapped = textwrap.wrap(_sentence(above), LINE_LENGTH - len(indent) - 2, break_long_words=False)
        lines[row:row + 1] = [f"{indent}# {w}" for w in wrapped] + [inline]
    return "\n".join(lines)


def strip_z_viz(text):
    """Replace z_viz("NAME", default[, mapping]) by default."""
    out, pos = [], 0
    for m in Z_VIZ.finditer(text):
        out.append(text[pos:m.start()])
        i, depth, start = m.end(), 0, m.end()
        while True:  # the default ends at the first comma or closing parenthesis at depth 0
            ch = text[i]
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                if depth == 0:
                    break
                depth -= 1
            elif ch == "," and depth == 0:
                break
            i += 1
        out.append(text[start:i].strip())
        depth = 0
        while not (text[i] == ")" and depth == 0):  # skip an optional mapping argument
            if text[i] in "([{":
                depth += 1
            elif text[i] in ")]}":
                depth -= 1
            i += 1
        pos = i + 1
    out.append(text[pos:])
    return "".join(out)


# notebooks that take settings from their lab (the cell "Settings from the lab"); advanced versions only where listed
VIZ_STEMS = {"flight_planner", "drone_hardware", "thermal_timing", "blackbody_radiation", "why_drones_fly", "drone_weather", "eu_rules", "gnss_sky",
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


VIZ_NOTE = ("> **💻 Co dělá kód:** Nepovinná buňka. Když do ní vložíš nastavení zkopírované z laboratoře a spustíš ji, převezmou buňky níže stejné hodnoty parametrů a u každé to vypíšou. Když ji necháš prázdnou, použijí se výchozí hodnoty. Nic nestahuje.",
            "> **💻 What the code does:** Optional cell. If you paste the settings copied from the lab and run it, the cells below take the same parameter values and say so for each one. If you leave it empty, the default values are used. It downloads nothing.")


def code_notes(stem, meta):
    """Popisy buněk kódu pro notebook: podle zdroje src/<stem>.py (verze míst a variant sdílejí popisy svého zdroje)."""
    sys.path.insert(0, str(ROOT / "src"))
    from _code_notes import NOTES
    src = meta["src"]
    return NOTES[src]


def build(stem):
    for out, meta, cells in units(stem):
        build_one(out, dict(meta, stem=out, src=stem), cells)


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
        if LAB_SETTINGS and meta["visual_stem"] in VIZ_STEMS and (not stem.endswith("_pro") or stem in VIZ_PRO):
            cells.append(nbf.v4.new_markdown_cell(t(*VIZ_NOTE)))
            cell = nbf.v4.new_code_cell(viz_cell(meta["visual_stem"], lang))
            cell.metadata["cellView"] = "form"
            cells.append(cell)
        n_task = 0
        notes = code_notes(stem, meta)
        n_code = 0
        for kind, text in cells_fn(t):
            text = text.strip("\n")
            if not LAB_SETTINGS:
                text = strip_z_viz(text)
            if kind in ("code", "setup"):
                text = lift_comments(text)
            if kind == "md":
                cells.append(nbf.v4.new_markdown_cell(text))
            elif kind == "setup":
                # required setup code (libraries, data access): collapsed in Colab, explained above
                cells.append(nbf.v4.new_markdown_cell(
                    t("**Povinná buňka, spusť ji jako první.** ", "**Required cell, run it first.** ") + t(*notes[n_code])
                    + t(" Kód je sbalený; zobrazíš ho pomocí **Show code**.", " The code is collapsed; reveal it with **Show code**.")))
                title = t("Příprava (spusť jako první)", "Setup (run first)")
                if text.startswith("# @title "):
                    title, _, text = text.partition("\n")
                    title = title[len("# @title "):]
                cell = nbf.v4.new_code_cell(f'# @title {title} {{display-mode: "form"}}\n' + text)
                cell.metadata["cellView"] = "form"
                cells.append(cell)
                n_code += 1
            elif kind == "code":
                if notes[n_code] is not None:  # None: the markdown cell above already explains the code
                    cells.append(nbf.v4.new_markdown_cell(t("> **💻 Co dělá kód:** ", "> **💻 What the code does:** ") + t(*notes[n_code])))
                cells.append(nbf.v4.new_code_cell(text))
                n_code += 1
            elif kind == "task":
                n_task += not text.startswith("+")
                label = t("Úkol", "Task") + f" {n_task}" if not text.startswith("+") else t("Rozšíření (nepovinné)", "Extension (optional)")
                cells.append(nbf.v4.new_markdown_cell(f"> **✏️ {label}.** " + text.lstrip("+ ").replace("\n", "\n> ")))
                cells.append(nbf.v4.new_markdown_cell(t("*Tvoje odpověď:* ", "*Your answer:* ")))
            else:
                raise ValueError(kind)
        cells.append(nbf.v4.new_markdown_cell(footer(meta, lang)))
        assert 4 <= n_task <= 6, (stem, n_task)
        assert n_code == len(notes), (stem, n_code, len(notes))
        nb.cells = cells
        for i, c in enumerate(nb.cells):
            c["id"] = f"{stem[:20]}-{i:02d}"
        nbf.write(nb, ROOT / f"{stem}_{lang}.ipynb")
        ruff(ROOT / f"{stem}_{lang}.ipynb")
    print("built", stem)


RUFF_VERSION = "0.16.2"
# Agreed style (notebook-authoring guide): 4 spaces, 88 characters, double quotes; lint rules E4, E7, E9, F, I.
RUFF_ARGS = ["--line-length", "88", "--config", "indent-width = 4", "--config", 'format.quote-style = "double"',
             "--config", 'format.indent-style = "space"']


def ruff(path):
    """Format the code cells of a built notebook and apply the safe lint fixes; fail on any remaining finding."""
    import subprocess
    run = lambda *a: subprocess.run([sys.executable, "-m", "ruff", *a], capture_output=True, text=True)
    v = run("--version").stdout.split()[-1]
    assert v == RUFF_VERSION, f"ruff {RUFF_VERSION} required, found {v} (pip install ruff=={RUFF_VERSION})"
    r = run("format", "--isolated", *RUFF_ARGS, str(path))
    assert r.returncode == 0, r.stderr
    r = run("check", "--isolated", "--fix", "--select", "E4,E7,E9,F,I", *RUFF_ARGS[:2], str(path))
    if r.returncode != 0:
        RUFF_FINDINGS.append(f"{path.name}:\n{r.stdout}")
    r = run("format", "--isolated", *RUFF_ARGS, str(path))
    assert r.returncode == 0, r.stderr


RUFF_FINDINGS = []


if __name__ == "__main__":
    stems = sys.argv[1:] or sorted(p.stem for p in (ROOT / "src").glob("*.py") if not p.stem.startswith("_"))
    for s in stems:
        build(s)
    if RUFF_FINDINGS:
        print("\n".join(RUFF_FINDINGS))
        sys.exit("ruff: findings above need a fix in src/")
