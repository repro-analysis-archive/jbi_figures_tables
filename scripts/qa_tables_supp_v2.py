#!/usr/bin/env python3
"""QA of Table_S3_v2 and Table_S4_v2 (task v7 §2): the table-template checks of qa_tables.py; only the five recorded
cells differ from v1 in the displayed cells (CSV and docx tables), each equal to its recorded sign-visible display with
the marker; no "−0.000" left in a table cell; the footnotes differ from v1 only by the added sentence (S3) or by the
replaced sentence (S4); page counts unchanged. Writes qa/tables_qa_supp_v2.json.

    .venv/bin/python -I scripts/qa_tables_supp_v2.py
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
T = ROOT / "tables"


def cells(path):
    return [[c.text for c in r.cells] for t in Document(path).tables for r in t.rows]


def notes(path):
    d = Document(path)
    return [p.text for p in d.paragraphs if p.text and not p.text.startswith(("Table S", "(A)", "(B)", "(C)"))]


def main():
    nz = json.loads((ROOT / "canonical_supplement" / "validation.json").read_text())["v7_negative_zero_S3_S4"]
    out, ok = {}, True
    for n, ntab in ((3, 1), (4, 3)):
        v1, v2 = T / f"Table_S{n}_v1", T / f"Table_S{n}_v2"
        d = qt.docx_checks(Path(f"{v2}.docx"))
        p = qt.pdf_checks(Path(f"{v2}.pdf"), ntab)
        p1 = qt.pdf_checks(Path(f"{v1}.pdf"), ntab)
        a = list(csv.reader(open(f"{v1}.csv", newline=""))); b = list(csv.reader(open(f"{v2}.csv", newline="")))
        diff_csv = [(i, j, x, y) for i, (ra, rb) in enumerate(zip(a, b)) for j, (x, y) in enumerate(zip(ra, rb)) if x != y]
        ca, cb = cells(f"{v1}.docx"), cells(f"{v2}.docx")
        diff_doc = [(i, j, x, y) for i, (ra, rb) in enumerate(zip(ca, cb)) for j, (x, y) in enumerate(zip(ra, rb)) if x != y]
        mine = [r for r in nz if r["table"] == f"S{n}"]
        want = sorted(r["display"] for r in mine)
        got = sorted(re.search(r"(−0\.000\d+)a", y).group(1) for _, _, _, y in diff_doc)
        na, nb = notes(f"{v1}.docx"), notes(f"{v2}.docx")
        added = [x for x in nb if x not in na]
        removed = [x for x in na if x not in nb]
        checks = {
            "Normal style only": set(d["paragraph_styles"]) == {"Normal"},
            "no shading": d["shading_elements"] == 0 and p["filled_rects"] == 0,
            "cell borders top/bottom only": set(d["cell_borders"]) <= {"top", "bottom"},
            "bold only caption + header": not d["stray_bold"],
            "Arial 11 pt": set(d["run_fonts"]) <= {"Arial"} and set(d["run_sizes_pt"]) == {11.0},
            "PDF fonts Arial embedded": all(("Arial" in f and f.endswith("emb=yes")) for f in p["pdffonts"]),
            "no vertical rules": p["vertical_rules"] == 0,
            "pages unchanged": p["pages"] == p1["pages"],
            "CSV: only the recorded cells differ": len(diff_csv) == len(mine) and len(a) == len(b),
            "docx tables: only the recorded cells differ": len(diff_doc) == len(mine) and len(ca) == len(cb),
            "displays equal validation.json": got == want,
            "no −0.000 left in a table cell": not any(re.search(r"−0\.000(?!\d)", x) for r in cb for x in r),
            "footnotes: one added, S4 one sentence replaced": (len(added) == 1 and not removed) if n == 3 else
                (len(added) == 2 and len(removed) == 1 and "−0.000 is negative" in removed[0] and
                 removed[0].replace(" A value shown as −0.000 is negative and rounds to zero at 3 decimals (committed "
                                    "rounding).", "") in added),
        }
        out[f"Table_S{n}_v2"] = dict(pages=p["pages"], rules_per_page=p["rules_per_page"], csv_changes=diff_csv,
                                     docx_changes=diff_doc, footnotes_added=added, footnotes_removed=removed,
                                     checks=checks)
        ok &= all(checks.values())
        print(f"Table_S{n}_v2: pages {p['pages']} (v1 {p1['pages']}); changes {[(y) for _, _, _, y in diff_doc]}; "
              f"{'PASS' if all(checks.values()) else 'FAIL ' + str([k for k, v in checks.items() if not v])}")
    (ROOT / "qa" / "tables_qa_supp_v2.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("TABLES-SUPP-V2", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
