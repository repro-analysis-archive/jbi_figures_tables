#!/usr/bin/env python3
"""QA of Supplementary Tables S1–S6 (supplement v6 §4, §6): the table-template checks of qa_tables.py (Normal style,
no numbering, no shading, top / header-bottom / bottom rules only, bold only caption + header, Arial 11 pt, PDF fonts
embedded, no vertical rules), page count, the caption "Table Sn." once, and the value match to the package CSVs: every
data cell of every docx table is compared with the value re-formatted here from the package CSV row it belongs to
(3 decimals, true minus sign; Table S1 verbatim). Table S2 is compared with Table_S5_v2 (document XML identical apart
from the caption number; CSV identical). Writes qa/tables_qa_supp_v1.json.

    .venv/bin/python -I scripts/qa_tables_supp_v1.py
"""
import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

from docx import Document  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("qa_tables", HERE / "qa_tables.py")
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)
ROOT = HERE.parent
PKG = Path("/Volumes/ADDATA/医療動画/SS_DS203_manuscript_20261020/03_results/SUPPLEMENT_20261020")
M = "−"


def fm(s):
    return format(float(s), ".3f").replace("-", M)


def pkg(name):
    with open(PKG / name, newline="") as f:
        return list(csv.DictReader(f))


def body(path, k=0):
    """Data rows of docx table k as lists of cell texts (merged span rows kept as one string)."""
    t = Document(path).tables[k]
    out = []
    for row in t.rows[1:]:
        cells = [c.text for c in row.cells]
        out.append([cells[0]] if len(set(cells)) == 1 and len(cells) > 1 else cells)
    return out


def expected():
    ex = {}
    key = {"P": "FM-P", "S": "FM-S", "REF": "REF"}
    an = {"a": "transport", "b": "within-set refit"}
    pr = {"linear": "linear", "mlp": "MLP"}
    arm = {"FM-P-C": "FM-P−C", "FM-S-C": "FM-S−C", "REF-C": "REF−C"}
    t = {(r["scope"], r["item"]): r["value"] for r in pkg("tableS4_mask_check.csv")}
    ex["Table_S1_v1"] = [[[c, t[(f"centre {c}", "n_frames")], t[(f"centre {c}", "rho_c (visible_radius)")]]
                          for c in "2345"]]
    rows = []
    for a in ("X1", "X2"):
        rows.append(None)
        for r in (x for x in pkg("tableX_group_summaries.csv") if x["analysis"] == a):
            rows.append([arm[r["arm"]], r["comparator"].replace("step6 ", "step-6 ").replace("-C", M + "C"), r["group"],
                         r["n_cells"], f"{fm(r['mean_delta'])} ({fm(r['mean_delta_lo'])} to {fm(r['mean_delta_hi'])})",
                         r["n_cells_delta_negative"]])
    ex["Table_S3_v1"] = [rows]
    e3 = {(r["block"].split(" ")[0], r["key"], r["probe"], r["condition"], r["field"]): r["value"]
          for r in pkg("tableX_E3.csv")}
    A, B, C = [], [], []
    s5c, x1c = "step 5 (protocol LEACE)", "X1 (LEACE refitted on the analysis region)"
    for k in ("P", "S", "REF"):
        for p in ("linear", "mlp"):
            g = lambda c, f: e3[("E3-site", k, p, c, f)]  # noqa: E731
            A.append([key[k], pr[p], f"{fm(g(s5c, 'ba'))} ({fm(g(s5c, 'lo_2p5'))} to {fm(g(s5c, 'hi_97p5'))})",
                      fm(g(s5c, "upper_one_sided_95")),
                      f"{fm(g(x1c, 'ba'))} ({fm(g(x1c, 'lo_2p5'))} to {fm(g(x1c, 'hi_97p5'))})",
                      fm(g(x1c, "upper_one_sided_95"))])
        for c in ("step 5, before removal", "step 5, after protocol removal", "X1, after X1 removal"):
            g = lambda f: e3[("E2", k, "", c, f)]  # noqa: E731
            B.append([key[k], c, f"{fm(g('delta_auc'))} ({fm(g('ci_lo'))} to {fm(g('ci_hi'))})",
                      "met" if g("pass") == "true" else "not met"])
        C.append([key[k]] + [f"retained fraction {fm(e3[('E3-state', k, '', c, 'retained_fraction')])}"
                             if e3[("E3-state", k, "", c, "applicable")] == "true" else "not applicable (E2 primary failed)"
                             for c in ("step 5", "X1")])
    ex["Table_S4_v1"] = [A, B, C]
    jd = {}
    for r in pkg("tableB_judgements.csv"):
        jd.setdefault((r["key"], r["analysis"], r["probe"], r["pair"].split("->")[1]), []).append(r["statement"])
    rows = []
    for k in ("P", "S", "REF"):
        for a in ("a", "b"):
            rows.append(None)
            for r in (x for x in pkg("tableB_ba.csv") if x["key"] == k and x["analysis"] == a):
                rows.append([pr[r["probe"]], r["set"], r["cases"], r["rows"],
                             f"{fm(r['ba'])} ({fm(r['lo_2p5'])} to {fm(r['hi_97p5'])})", fm(r["upper_one_sided_95"]),
                             "yes" if r["exceeds_boundary_0.35"] == "True" else "no",
                             "\n".join(jd.get((k, a, r["probe"], r["set"]), [])) or "—"])
    ex["Table_S5_v1"] = [rows]
    rows = []
    for k in ("P", "S", "REF"):
        for a in ("a", "b"):
            rows.append(None)
            for r in (x for x in pkg("tableB_sens.csv") if x["key"] == k and x["analysis"] == a):
                rows.append([pr[r["probe"]], r["set"], r["draws"], fm(r["median"]), f"{fm(r['p2_5'])} to {fm(r['p97_5'])}",
                             f"{fm(r['min'])} to {fm(r['max'])}"])
    ex["Table_S6_v1"] = [rows]
    return ex


def main():
    ex = expected()
    out, ok = {}, True
    pages_max = {"Table_S1_v1": 1}
    for n in range(1, 7):
        stem = f"Table_S{n}_v1"
        ntab = 3 if n == 4 else 1
        d = qt.docx_checks(ROOT / "tables" / f"{stem}.docx")
        p = qt.pdf_checks(ROOT / "tables" / f"{stem}.pdf", ntab)
        doc = Document(ROOT / "tables" / f"{stem}.docx")
        texts = [q.text for q in doc.paragraphs] + [c.text for t in doc.tables for r in t.rows for c in r.cells]
        checks = {
            "Normal style only": set(d["paragraph_styles"]) == {"Normal"},
            "no numbering": d["numbered_paragraphs"] == 0,
            "no shading": d["shading_elements"] == 0 and p["filled_rects"] == 0,
            "cell borders top/bottom only": set(d["cell_borders"]) <= {"top", "bottom"},
            "table-level borders nil": all(k.endswith("=nil") for k in d["table_level_borders"]),
            "bold only caption + header": not d["stray_bold"],
            "Arial runs": set(d["run_fonts"]) <= {"Arial"},
            "11 pt runs": set(d["run_sizes_pt"]) == {11.0},
            "PDF fonts Arial embedded": all(("Arial" in f and f.endswith("emb=yes")) for f in p["pdffonts"]),
            "no vertical rules": p["vertical_rules"] == 0,
            "rules: 2 per header + 1 per table": p["horizontal_rules"] >= 3 * ntab,
            f"caption 'Table S{n}.' once": sum(t.count(f"Table S{n}.") for t in texts) == 1,
        }
        if stem in pages_max:
            checks["pages <= 1"] = p["pages"] <= 1
        if n == 2:
            a = zipfile.ZipFile(ROOT / "tables" / "Table_S5_v2.docx").read("word/document.xml").decode()
            b = zipfile.ZipFile(ROOT / "tables" / f"{stem}.docx").read("word/document.xml").decode()
            checks["document XML = Table_S5_v2 apart from the caption number"] = a.replace("Table S5.", "Table S2.") == b
            checks["CSV = Table_S5_v2.csv"] = (ROOT / "tables" / "Table_S5_v2.csv").read_bytes() == \
                (ROOT / "tables" / f"{stem}.csv").read_bytes()
            nvals = None
        else:
            mism, nvals = [], 0
            for k, rows in enumerate(ex[stem]):
                got = body(ROOT / "tables" / f"{stem}.docx", k)
                if len(got) != len(rows):
                    mism.append(f"table {k}: {len(got)} rows vs {len(rows)} expected")
                    continue
                for g, e in zip(got, rows):
                    if e is None:
                        continue                                  # span (section heading) row
                    nvals += len(e)
                    if g != e:
                        mism.append(f"table {k}: {g} != {e}")
            checks["values match the package CSV"] = not mism
        out[stem] = dict(docx=d, pdf=p, checks=checks, cells_compared=nvals)
        ok &= all(checks.values())
        print(f"{stem}: pages {p['pages']}; tables {d['tables']}; rules/page {p['rules_per_page']}; vertical "
              f"{p['vertical_rules']}; run sizes {d['run_sizes_pt']}; styles {d['paragraph_styles']}; cells compared "
              f"{nvals}; {'PASS' if all(checks.values()) else 'FAIL ' + str([k for k, v in checks.items() if not v])}")
    (ROOT / "qa" / "tables_qa_supp_v1.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("TABLES-SUPP", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
