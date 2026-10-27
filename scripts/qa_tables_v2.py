#!/usr/bin/env python3
"""QA of the v3-revision tables (Table_1_v2, Table_2_v2, Table_S5_v2) with the checks of qa_tables.py, plus the page
count target of task v3 §3 (Tables 1 and 2 on one page). Writes qa/tables_qa_v2.json.

    .venv/bin/python -I scripts/qa_tables_v2.py
"""
import sys

sys.dont_write_bytecode = True

import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("qa_tables", HERE / "qa_tables.py")
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)
ROOT = HERE.parent


def main():
    out, ok = {}, True
    for stem, n_tables, max_pages in (("Table_1_v2", 2, 1), ("Table_2_v2", 1, 1), ("Table_S5_v2", 1, None)):
        d = qt.docx_checks(ROOT / "tables" / f"{stem}.docx")
        p = qt.pdf_checks(ROOT / "tables" / f"{stem}.pdf", n_tables)
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
            "rules: 2 per header + 1 per table": p["horizontal_rules"] >= 3 * n_tables,
        }
        if max_pages:
            checks[f"pages <= {max_pages}"] = p["pages"] <= max_pages
        out[stem] = dict(docx=d, pdf=p, checks=checks)
        ok &= all(checks.values())
        print(f"{stem}: pages {p['pages']} ({p['page_mm'][0]} x {p['page_mm'][1]} mm); rules per page "
              f"{p['rules_per_page']}; vertical {p['vertical_rules']}; fills {p['filled_rects']}; fonts "
              f"{p['pdffonts']}; run sizes {d['run_sizes_pt']}; styles {d['paragraph_styles']}")
        for k, v in checks.items():
            if not v:
                print("   FAIL", k)
        print("   all checks PASS" if all(checks.values()) else "   checks FAILED")
    (ROOT / "qa" / "tables_qa_v2.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
