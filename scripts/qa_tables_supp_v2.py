#!/usr/bin/env python3
"""QA of Table_S2_v2 (task v8 §1), Table_S3_v2 and Table_S4_v2 (task v7 §2): the table-template checks of qa_tables.py; only the five recorded
cells differ from v1 in the displayed cells (CSV and docx tables), each equal to its recorded sign-visible display with
the marker; no "−0.000" left in a table cell; the footnotes differ from v1 only by the added sentence (S3) or by the
replaced sentence (S4); page counts unchanged. v8: Table S2 v2 (footnote letter j; a–i are in use), the displays of
the three shared quantities identical in S2 v2 and S4 v2, no "−0.000" in any current Table S1–S6, and build_tables.table3
with its default arguments still reproducing Table_S2_v1 (rebuilt in a temporary folder). Writes qa/tables_qa_supp_v2.json.

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
    val = json.loads((ROOT / "canonical_supplement" / "validation.json").read_text())
    nz = val["v7_negative_zero_S3_S4"] + val["v8_negative_zero_S2"]
    out, ok = {}, True
    for n, ntab in ((2, 1), (3, 1), (4, 3)):
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
        got = sorted(re.search(r"(−0\.000\d+)[aj]", y).group(1) for _, _, _, y in diff_doc)
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
            "footnotes: one added, S4 one sentence replaced": (len(added) == 1 and not removed) if n in (2, 3) else
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
    # ---- v8 cross-checks
    s4 = {r["row"]: r["display"] for r in val["v7_negative_zero_S3_S4"] if r["table"] == "S4"}
    cross = {r["row"]: (r["display"], s4[r["same_as_table_S4_v2"].split(" [")[0]]) for r in val["v8_negative_zero_S2"]}
    out["S2_v2_vs_S4_v2"] = {k: dict(S2=a, S4=b, identical=a == b) for k, (a, b) in cross.items()}
    ok &= all(a == b for a, b in cross.values())
    current = ["Table_S1_v1", "Table_S2_v2", "Table_S3_v2", "Table_S4_v2", "Table_S5_v1", "Table_S6_v1"]
    left = {s: [x for r in cells(T / f"{s}.docx") for x in r if re.search(r"−0\.000(?!\d)", x)] for s in current}
    out["negative_zero_left_in_current_S1_S6"] = left
    ok &= not any(left.values())
    import tempfile, zipfile
    spec2 = importlib.util.spec_from_file_location("build_tables", HERE / "build_tables.py")
    bt = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(bt)
    with tempfile.TemporaryDirectory() as d:
        bt.OUT = Path(d)
        bt.table3(num="S2", stem="Table_S2_v1")
        same = zipfile.ZipFile(Path(d) / "Table_S2_v1.docx").read("word/document.xml") == \
            zipfile.ZipFile(T / "Table_S2_v1.docx").read("word/document.xml") and \
            (Path(d) / "Table_S2_v1.csv").read_bytes() == (T / "Table_S2_v1.csv").read_bytes()
    out["table3_default_reproduces_Table_S2_v1"] = same
    ok &= same
    print("S2 v2 vs S4 v2:", out["S2_v2_vs_S4_v2"])
    print("−0.000 left in current Tables S1–S6:", {k: len(v) for k, v in left.items()})
    print("table3 defaults reproduce Table_S2_v1:", same)
    (ROOT / "qa" / "tables_qa_supp_v2.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("TABLES-SUPP-V2", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
