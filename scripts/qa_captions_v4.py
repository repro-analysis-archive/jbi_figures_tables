#!/usr/bin/env python3
"""Cross-check of CAPTIONS_v4.md (task v5 §4): headings Figure 1–6 once and in order; the caption bodies of Figures
1–4 and 6 identical to their CAPTIONS_v2.md sources (new <- old: 1 <- 1, 2 <- 4, 3 <- 2, 4 <- 3, 6 <- 5); every panel
letter a caption uses exists as a panel label in its figure (figures_v4/Figure_N/Figure_N_v4.pdf); every main-figure
reference (e.g. "Figure 1C") points to an existing figure and panel; every "Supplementary Figure/Table" reference is
an item of SUPPLEMENT_INDEX.md. Writes qa/captions_v4.json.

    .venv/bin/python -I scripts/qa_captions_v4.py
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

import pymupdf  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NEW_FROM_OLD = {1: 1, 2: 4, 3: 2, 4: 3, 6: 5}


def captions(text):
    return {int(m.group(1)): m.group(2) for m in
            re.finditer(r"^\*\*Figure (\d)\.\*\* (.*?)(?=\n\n)", text, re.S | re.M)}


def panel_labels(n):
    page = pymupdf.open(ROOT / "figures_v4" / f"Figure_{n}" / f"Figure_{n}_v4.pdf")[0]
    return sorted({s["text"].strip()[1] for b in page.get_text("dict")["blocks"] for ln in b.get("lines", [])
                   for s in ln["spans"] if "Bold" in s["font"] and re.fullmatch(r"\([A-F]\)", s["text"].strip())})


def letters_used(body):
    used = set()
    for m in re.finditer(r"\(([A-F](?:, [A-F])*)\)", body):
        used |= set(m.group(1).split(", "))
    for m in re.finditer(r"\b(?:panels?|rows?) ([A-F])(?: and ([A-F]))?\b", body):
        used |= {x for x in m.groups() if x}
    return sorted(used)


def main():
    text = (ROOT / "CAPTIONS_v4.md").read_text()
    v4, v2 = captions(text), captions((ROOT / "CAPTIONS_v2.md").read_text())
    heads = [int(x) for x in re.findall(r"^\*\*Figure (\d)\.\*\*", text, re.M)]
    supp = (ROOT / "SUPPLEMENT_INDEX.md").read_text()
    supp_labels = set(re.findall(r"^\| (S\d|X|B)(?: \((?:figure|table)\))? \|", supp, re.M)) | {"S5"}
    rep, ok = dict(headings=heads, figures={}), heads == [1, 2, 3, 4, 5, 6]
    labels = {n: panel_labels(n) for n in range(1, 7)}
    for n in range(1, 7):
        body = v4[n]
        same = None if n == 5 else body == v2[NEW_FROM_OLD[n]]
        used = letters_used(body)
        missing = [x for x in used if x not in labels[n]]
        rep["figures"][f"Figure_{n}"] = dict(source=("new" if n == 5 else f"CAPTIONS_v2 Figure {NEW_FROM_OLD[n]}"),
                                             body_identical_to_source=same, panel_labels_in_pdf=labels[n],
                                             panel_letters_used=used, missing=missing)
        ok &= (same is not False) and not missing
    refs = []
    for m in re.finditer(r"(?<!Supplementary )\bFigure (\d)([A-F])?\b", text.split("\n---\n", 1)[1]):
        n, p = int(m.group(1)), m.group(2)
        good = 1 <= n <= 6 and (p is None or p in labels[n])
        refs.append(dict(ref=m.group(0), ok=good))
        ok &= good
    for m in re.finditer(r"Supplementary (?:Figures?|Tables?) ((?:S\d|X)(?: and (?:S\d|X))?)", text):
        for lab in re.findall(r"S\d|X", m.group(1)):
            good = lab in supp_labels
            refs.append(dict(ref=f"Supplementary {lab}", ok=good))
            ok &= good
    rep["references"] = refs
    rep["result"] = "PASS" if ok else "FAIL"
    (ROOT / "qa" / "captions_v4.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    for k, v in rep["figures"].items():
        print(k, v)
    print("references:", sorted({(r["ref"], r["ok"]) for r in refs}))
    print("CAPTIONS", rep["result"])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
