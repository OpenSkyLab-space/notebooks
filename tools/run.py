"""Execute notebooks top to bottom and store the outputs in place.

Usage: python tools/run.py <stem>_cs.ipynb [...]   (default: all *_cs.ipynb and *_en.ipynb)
Each notebook runs in its own temporary working directory, so downloaded data never land in the repository.
"""
import pathlib
import sys
import tempfile
import time

import nbformat as nbf
from nbclient import NotebookClient

ROOT = pathlib.Path(__file__).resolve().parent.parent
files = [ROOT / f for f in sys.argv[1:]] or sorted(ROOT.glob("*_c[s].ipynb")) + sorted(ROOT.glob("*_en.ipynb"))
bad = []
for f in files:
    nb = nbf.read(f, as_version=4)
    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        try:
            NotebookClient(nb, timeout=900, kernel_name="python3", resources={"metadata": {"path": tmp}}).execute()
            status = "ok"
        except Exception as e:  # keep partial outputs for inspection
            status = "FAILED: " + str(e).splitlines()[-1][:300] if str(e) else "FAILED"
            bad.append(f.name)
    nbf.write(nb, f)
    print(f"{f.name}: {status} ({time.time() - t0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)
