#!/usr/bin/env python3
"""QA of the v4-revision table (Table_2_v3): the checks of qa_tables.py / qa_tables_v2.py (one page, rules, 11 pt,
Normal style, Arial) plus the v4 items — the column heading "Locked rule outcome" with its footnote, the one bound
shown with extra decimals equal to canonical/validation.json, no other sign-hiding "−0.000" in a table cell, and every
other displayed cell identical to Table_2_v2. Writes qa/tables_qa_v3.json.

    .venv/bin/python -I scripts/qa_tables_v3.py
"""
import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

from docx import Document  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("qa_tables", HERE / "qa_tables.py")
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)
ROOT = HERE.parent


def main():
    stem = "Table_2_v3"
    d = qt.docx_checks(ROOT / "tables" / f"{stem}.docx")
    p = qt.pdf_checks(ROOT / "tables" / f"{stem}.pdf", 1)
    ex = json.loads((ROOT / "canonical" / "validation.json").read_text())["v4_table2_sign_decimals"][0]
    v2 = list(csv.reader(open(ROOT / "tables" / "Table_2_v2.csv", newline="")))
    v3 = list(csv.reader(open(ROOT / "tables" / f"{stem}.csv", newline="")))
    changed = [(i, j, a, b) for i, (r2, r3) in enumerate(zip(v2, v3)) for j, (a, b) in enumerate(zip(r2, r3)) if a != b]
    doc = Document(ROOT / "tables" / f"{stem}.docx")
    cells = [c.text for t in doc.tables for row in t.rows for c in row.cells]
    notes = [q.text for q in doc.paragraphs]
    shown = ex["display"]
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
        "rules: 2 per header + 1 per table": p["horizontal_rules"] >= 3,
        "pages <= 1": p["pages"] <= 1,
        "heading 'Locked rule outcome' (no 'Direction rule' heading)": "Locked rule outcomea" in cells and
            "Direction rule" not in cells,
        "footnote a: mechanical outcome of §12.3, qualified by Status": any(
            n.startswith("aMechanical outcome of the §12.3 aggregation") and "Status column" in n for n in notes),
        "footnote b: additional decimals": any(n.startswith(f"bLower bound shown with {ex['decimals']} decimals")
                                                 for n in notes),
        "bound displayed once, equal to validation.json": sum(c.count(shown + "b") for c in cells) == 1 and
            shown == f"{ex['value']:.{ex['decimals']}f}".replace("-", "−"),
        "no −0.000 left in a table cell": not any(re.search(r"−0\.000(?!\d)", c) for c in cells),
        "CSV: only the heading and the bound changed vs Table_2_v2": len(v2) == len(v3) and [(i, j) for i, j, _, _ in changed]
            == [(0, 5), (6, 3)],
    }
    out = {stem: dict(docx=d, pdf=p, checks=checks, csv_changes_vs_v2=changed,
                      bound=dict(row=ex["row"], field=ex["field"], exact=ex["value_repr"], display=shown,
                                 decimals=ex["decimals"], display_3dp=ex["display_3dp"]))}
    print(f"{stem}: pages {p['pages']} ({p['page_mm'][0]} x {p['page_mm'][1]} mm); rules per page "
          f"{p['rules_per_page']}; vertical {p['vertical_rules']}; fills {p['filled_rects']}; fonts {p['pdffonts']}; "
          f"run sizes {d['run_sizes_pt']}; styles {d['paragraph_styles']}")
    print(f"   bound {ex['row']} {ex['field']} = {ex['value_repr']} -> displayed {shown}; CSV changes {changed}")
    for k, v in checks.items():
        if not v:
            print("   FAIL", k)
    ok = all(checks.values())
    print("   all checks PASS" if ok else "   checks FAILED")
    (ROOT / "qa" / "tables_qa_v3.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
