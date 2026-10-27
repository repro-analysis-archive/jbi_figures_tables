#!/usr/bin/env python3
"""QA of Tables 1–3 (table template §11; Word rules template v4 §2 / §18-G): Word XML and the rendered PDF.

Word: every paragraph in Normal style; no list numbering; no shading; table borders only top / header-bottom / bottom
(no left/right/insideV/insideH); bold only in "Table X." and the header rows; font Arial, 11 pt; header row repeated.
PDF (LibreOffice rendering): fonts embedded and Arial only; every drawn rule horizontal; rule count = 2 per header
occurrence (top and header-bottom, header repeated on each page) + 1 bottom rule per table; no filled rectangles.

    .venv/bin/python -I scripts/qa_tables.py
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import subprocess  # noqa: E402
import zipfile  # noqa: E402
from collections import Counter  # noqa: E402
from pathlib import Path  # noqa: E402

import pymupdf  # noqa: E402
from lxml import etree  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
MM = 25.4 / 72


def docx_checks(path):
    x = etree.fromstring(zipfile.ZipFile(path).read("word/document.xml"))
    paras = x.iter(f"{W}p")
    styles = Counter()
    numbered = 0
    for p in paras:
        ps = p.find(f"{W}pPr/{W}pStyle")
        styles[ps.get(f"{W}val") if ps is not None else "Normal"] += 1
        if p.find(f"{W}pPr/{W}numPr") is not None:
            numbered += 1
    shd = len(list(x.iter(f"{W}shd")))
    borders = Counter()
    for tcb in x.iter(f"{W}tcBorders"):
        for e in tcb:
            if e.get(f"{W}val") not in (None, "nil", "none"):
                borders[e.tag.replace(W, "")] += 1
    tbl_borders = Counter()
    for tb in x.iter(f"{W}tblBorders"):
        for e in tb:
            tbl_borders[(e.tag.replace(W, ""), e.get(f"{W}val"))] += 1
    tables = list(x.iter(f"{W}tbl"))
    header_repeat = sum(1 for t in tables if t.find(f"{W}tr/{W}trPr/{W}tblHeader") is not None)
    bold_texts = []
    fonts, sizes = Counter(), Counter()
    for r in x.iter(f"{W}r"):
        rpr = r.find(f"{W}rPr")
        t = "".join(tt.text or "" for tt in r.iter(f"{W}t"))
        if rpr is None or not t:
            continue
        rf = rpr.find(f"{W}rFonts")
        if rf is not None:
            fonts[rf.get(f"{W}ascii")] += 1
        sz = rpr.find(f"{W}sz")
        if sz is not None:
            sizes[int(sz.get(f"{W}val")) / 2] += 1
        bel = rpr.find(f"{W}b")
        if bel is not None and bel.get(f"{W}val") not in ("0", "false"):
            bold_texts.append(t)
    # bold runs must be "Table N." or lie in a header row (first row of a table)
    header_texts = set()
    for t in tables:
        tr = t.find(f"{W}tr")
        header_texts |= {"".join(tt.text or "" for tt in r.iter(f"{W}t")) for r in tr.iter(f"{W}r")}
    stray_bold = [b for b in bold_texts if not (b.startswith("Table ") or b in header_texts)]
    return dict(paragraph_styles=dict(styles), numbered_paragraphs=numbered, shading_elements=shd,
                cell_borders=dict(borders), table_level_borders={f"{k[0]}={k[1]}": v for k, v in tbl_borders.items()},
                tables=len(tables), header_row_repeat=header_repeat, run_fonts=dict(fonts), run_sizes_pt=dict(sizes),
                stray_bold=stray_bold)


def pdf_checks(path, n_tables):
    doc = pymupdf.open(path)
    fonts = subprocess.run(["pdffonts", str(path)], capture_output=True, text=True).stdout.strip().splitlines()[2:]
    horiz, vert, fills, sizes = 0, 0, 0, Counter()
    pages = []
    for page in doc:
        h_page = 0
        for d in page.get_drawings():
            r = d["rect"]
            if d.get("fill") is not None and r.width * MM > 1 and r.height * MM > 1:
                fills += 1
            for it in d["items"]:
                if it[0] == "l":
                    p, q = it[1], it[2]
                    if abs(p.y - q.y) < 0.2 and abs(p.x - q.x) * MM > 1:
                        horiz += 1; h_page += 1
                    elif abs(p.x - q.x) < 0.2 and abs(p.y - q.y) * MM > 1:
                        vert += 1
                elif it[0] == "re":
                    rr = it[1]
                    if rr.height * MM < 0.6 and rr.width * MM > 1:
                        horiz += 1; h_page += 1
                    elif rr.width * MM < 0.6 and rr.height * MM > 1:
                        vert += 1
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for s in ln["spans"]:
                    if s["text"].strip():
                        sizes[round(s["size"], 1)] += 1
        pages.append(h_page)
    return dict(pages=len(doc), page_mm=[round(doc[0].rect.width * MM, 1), round(doc[0].rect.height * MM, 1)],
                pdffonts=[" ".join(f.split()[:2]) + " emb=" + f.split()[-5] for f in fonts],
                horizontal_rules=horiz, rules_per_page=pages, vertical_rules=vert, filled_rects=fills,
                text_sizes_pt=dict(sorted(sizes.items())))


def main():
    out = {}
    ok = True
    for n, n_tables in ((1, 3), (2, 1), (3, 1)):
        d = docx_checks(ROOT / "tables" / f"Table_{n}.docx")
        p = pdf_checks(ROOT / "tables" / f"Table_{n}.pdf", n_tables)
        # expected rules: per page, 2 per header occurrence on that page; plus one bottom rule per table
        exp = 2 * sum(1 for _ in range(n_tables))  # first page headers
        checks = {
            "Normal style only": set(d["paragraph_styles"]) == {"Normal"},
            "no numbering": d["numbered_paragraphs"] == 0,
            "no shading": d["shading_elements"] == 0 and p["filled_rects"] == 0,
            "cell borders top/bottom only": set(d["cell_borders"]) <= {"top", "bottom"},
            "table-level borders nil": all(k.endswith("=nil") for k in d["table_level_borders"]),
            "header repeat": d["header_row_repeat"] == d["tables"],
            "bold only caption + header": not d["stray_bold"],
            "Arial runs": set(d["run_fonts"]) <= {"Arial"},
            "11 pt runs": set(d["run_sizes_pt"]) == {11.0},
            "PDF fonts Arial embedded": all(("Arial" in f and f.endswith("emb=yes")) for f in p["pdffonts"]),
            "no vertical rules": p["vertical_rules"] == 0,
            "rules: 2 per header + 1 per table": p["horizontal_rules"] >= exp + n_tables,
        }
        out[f"Table_{n}"] = dict(docx=d, pdf=p, checks=checks)
        ok &= all(checks.values())
        print(f"Table_{n}: pages {p['pages']} ({p['page_mm'][0]} x {p['page_mm'][1]} mm); rules per page "
              f"{p['rules_per_page']}; vertical {p['vertical_rules']}; fills {p['filled_rects']}; fonts "
              f"{p['pdffonts']}; text sizes {p['text_sizes_pt']}")
        for k, v in checks.items():
            if not v:
                print("   FAIL", k)
        print("   all checks PASS" if all(checks.values()) else "   checks FAILED")
    (ROOT / "qa" / "tables_qa.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
