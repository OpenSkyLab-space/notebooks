"""Write README.md with a table of all notebooks built from src/.

Usage:
    python tools/readme.py
"""
import pathlib

from build import AI_NOTE, REPO, ROOT, SITE, load

COLAB = "https://colab.research.google.com/assets/colab-badge.svg"


def main():
    rows = []
    for path in sorted((ROOT / "src").glob("*.py")):
        if path.stem.startswith("_"):
            continue
        meta = load(path.stem).META
        links = " ".join(
            f"[![{lang.upper()}]({COLAB})](https://colab.research.google.com/github/{REPO}/blob/main/{path.stem}_{lang}.ipynb) "
            f"[{lang.upper()}]({path.stem}_{lang}.ipynb)"
            for lang in ("cs", "en"))
        docs = f"[CS](docs/cs/{path.stem}.md) [EN](docs/en/{path.stem}.md)"
        rows.append(f"| [{meta['visual']['cs']}]({SITE}/edu_viz_{path.stem}.html) | {meta['title']['cs']} | {meta['minutes']} | {links} | {docs} |")
    text = f"""# OpenSkyLab · notebooky k vizuálům / notebooks for the visuals

Notebooky pro Google Colab k interaktivním výukovým vizuálům [OpenSkyLab]({SITE}) o dálkovém průzkumu a dronech.
Každý notebook pracuje se skutečnými otevřenými daty, má 4 až 6 úkolů a parametry, které student mění.
Každý existuje česky (`_cs`) a anglicky (`_en`). Ke každému je popis toho, co se v něm dělá, ve složce `docs/`.

Google Colab notebooks for the [OpenSkyLab]({SITE}) interactive teaching visuals on remote sensing and drones.
Every notebook works with real open data, has 4 to 6 tasks and parameters for the student to change.
Each one exists in Czech (`_cs`) and English (`_en`). A description of what each one does is in the `docs/` folder.

| Vizuál / visual | Notebook | min | Colab | Popis / description |
|---|---|---|---|---|
{chr(10).join(rows)}

## Jak vznikají / How they are made

Obě jazykové verze i jejich popisy se generují z jednoho zdroje v `src/<kmen>.py` (`python tools/build.py`, `python tools/docs.py`) a před zveřejněním se celé spustí
na skutečných datech (`python tools/run.py`), takže uložené výstupy jsou z opravdového běhu.

Both language versions and their descriptions are generated from one source in `src/<stem>.py` (`python tools/build.py`, `python tools/docs.py`) and, before publishing,
run in full on real data (`python tools/run.py`), so the stored outputs come from a real run.

## Licence

Text a kód: OpenSkyLab, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Data mají licence svých poskytovatelů,
uvedené v každém notebooku. / Text and code: OpenSkyLab, CC BY 4.0. Data are under the licences of their providers,
listed in each notebook.

{AI_NOTE['cs']}

{AI_NOTE['en']}
"""
    (ROOT / "README.md").write_text(text, encoding="utf-8")
    print(f"README.md: {len(rows)} notebooks")


if __name__ == "__main__":
    main()
