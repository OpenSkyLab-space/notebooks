"""Kód sdílený notebooky o dronech a jejich datech."""

import re as _re

def bi(code):
    """Z textu se značkami {{cs||en}} vrátí (cs, en)."""
    pat = _re.compile(r"\{\{(.*?)\|\|(.*?)\}\}", _re.S)
    return pat.sub(lambda m: m.group(1), code), pat.sub(lambda m: m.group(2), code)
