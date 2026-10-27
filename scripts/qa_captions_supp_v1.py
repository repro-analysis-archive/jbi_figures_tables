#!/usr/bin/env python3
"""Cross-check of CAPTIONS_supplement_v1.md (supplement v6 §5, §6): every caption number Figure S1–S6 and Table S1–S6
present exactly once and in order; "Exploratory" is the first word for Figures S5, S6 and Tables S3–S6; the panel letters
a figure caption uses exist as panel labels in that figure's PDF (all pages); references to main figures ("main Figure
N (X)") point to existing main figures (figures_v4) and panels; the caption titles of Tables S1–S6 equal the captions in
the table .docx files. Writes qa/captions_supp_v1.json.

    .venv/bin/python -I scripts/qa_captions_supp_v1.py
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

import pymupdf  # noqa: E402
from docx import Document  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def labels(pdf):
    out = set()
    for page in pymupdf.open(pdf):
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for s in ln["spans"]:
                    if "Bold" in s["font"] and re.fullmatch(r"\([A-F]\)", s["text"].strip()):
                        out.add(s["text"].strip()[1])
    return sorted(out)


def main():
    text = (ROOT / "CAPTIONS_supplement_v1.md").read_text()
    body = text.split("\n---\n", 1)[1]
    caps = {m.group(1): m.group(2) for m in re.finditer(r"^\*\*((?:Figure|Table) S\d)\.\*\* (.*?)(?=\n\n|\Z)", body, re.S | re.M)}
    heads = re.findall(r"^\*\*((?:Figure|Table) S\d)\.\*\*", body, re.M)
    want = [f"Figure S{n}" for n in range(1, 7)] + [f"Table S{n}" for n in range(1, 7)]
    rep, ok = dict(headings=heads), heads == want
    rep["exploratory_first_word"] = {}
    for k in ("Figure S5", "Figure S6", "Table S3", "Table S4", "Table S5", "Table S6"):
        good = caps[k].startswith("Exploratory")
        rep["exploratory_first_word"][k] = good
        ok &= good
    rep["panels"] = {}
    for n in (1, 2, 3, 5, 6):
        k = f"Figure S{n}"
        cap = re.sub(r"main Figure \d \([A-F]\)(?: and \([A-F]\))?", "", caps[k])
        used = set()
        for m in re.finditer(r"\(([A-F])\)(?:–\(([A-F])\))?", cap):
            a, b = m.group(1), m.group(2) or m.group(1)
            used |= {chr(c) for c in range(ord(a), ord(b) + 1)}
        have = labels(ROOT / "figures_supp_v1" / f"Figure_S{n}" / f"Figure_S{n}_v1.pdf")
        miss = sorted(used - set(have))
        rep["panels"][k] = dict(used=sorted(used), labels_in_pdf=have, missing=miss)
        ok &= not miss
    refs = []
    for m in re.finditer(r"main Figure (\d)(?: \(([A-F])\)(?: and \(([A-F])\))?)?", text):
        n = int(m.group(1))
        have = labels(ROOT / "figures_v4" / f"Figure_{n}" / f"Figure_{n}_v4.pdf") if 1 <= n <= 6 else []
        good = 1 <= n <= 6 and all(x in have for x in (m.group(2), m.group(3)) if x)
        refs.append(dict(ref=m.group(0), ok=good))
        ok &= good
    rep["main_figure_refs"] = refs
    rep["table_titles"] = {}
    for n in range(1, 7):
        doc = Document(ROOT / "tables" / f"Table_S{n}_v1.docx")
        title = next(p.text for p in doc.paragraphs if p.text.startswith(f"Table S{n}."))
        good = caps[f"Table S{n}"].replace("\n", " ").startswith(title[len(f"Table S{n}. "):].rstrip("."))
        rep["table_titles"][f"Table S{n}"] = good
        ok &= good
    rep["result"] = "PASS" if ok else "FAIL"
    (ROOT / "qa" / "captions_supp_v1.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in rep.items() if k != "main_figure_refs"}, ensure_ascii=False))
    print("main refs:", sorted({(r["ref"], r["ok"]) for r in refs}))
    print("CAPTIONS-SUPP", rep["result"])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
