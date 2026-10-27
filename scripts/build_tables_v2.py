#!/usr/bin/env python3
"""v3 revision tables (task v3 §1, §3): Table_1_v2 (data and analysis sets and representations; arms block removed),
Table_2_v2 (all 18 non-exploratory family x set rows, compact, one page) and Table_S5_v2 (old Table 3, content
unchanged, renamed for the supplement). Same rules as build_tables.py (Arial 11 pt, top / header-bottom / bottom rules
only, Normal style, "Table X." bold) and the same canonical sources; helpers are reused from build_tables.py.

    .venv/bin/python -I scripts/build_tables_v2.py
"""
import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import importlib.util  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

from docx.shared import Mm, Pt  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build_tables", HERE / "build_tables.py")
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
OUT = bt.OUT


def page(doc):
    """A4 landscape; top / bottom margins 15 mm (left / right 25 mm) so that each v2 table fits one page."""
    sec = doc.sections[0]
    sec.top_margin = Mm(15)
    sec.bottom_margin = Mm(15)
    return doc


def table1_v2():
    T = bt.canonical("table1")
    sv = bt.canonical("schematic_values")
    doc = page(bt.new_document(landscape=True))
    bt.caption(doc, 1, "Data and analysis sets and video-derived representations.")
    p = doc.add_paragraph(); bt.rich(p, "(A) Data and analysis sets"); p.paragraph_format.space_after = Pt(3)
    hdrA = ["Set", "Cases", "Cases per centre\n(2 / 3 / 4 / 5)", "Definition", "Design cells", "Arms run{sup:a}"]
    rowsA = []
    for r in T["sets"]:
        name = r["set"].replace("representation set (E1, E3-site, PCA / LEACE)", "Representation set{sup:b}")
        name = name[0].upper() + name[1:]
        cpc = r["centres_2_3_4_5"].replace("all 278 full-length cases of centres 2–5", sv["centres_representation"])
        rowsA.append([name, str(r["cases"]), cpc, bt.typo(r["definition"]),
                      str(r["design_cells"]) if r["design_cells"] != "" else "—",
                      str(r["arms_run"]) if r["arms_run"] != "" else "—"])
    bt.add_table(doc, hdrA, rowsA, [46, 16, 36, 117, 18, 14], align=["l", "r", "l", "l", "r", "r"])
    p = doc.add_paragraph(); bt.rich(p, "(B) Representations (models and checkpoints)")
    p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(3)
    hdrB = ["Arm{sup:c}", "Model and checkpoint", "Kind", "Input", "Representation", "Reduction"]
    rowsB = [[r["arm"], re.sub(r"([/_])", "\\1\u200b", r["model"]).replace(", ", "\n"), r["kind"], r["input"],
              r["representation"], r["reduction"]] for r in T["models"]]
    sel = "; ".join(f"{r['arm'].split(' ')[0]}, {r['selection']}" for r in T["models"])
    bt.add_table(doc, hdrB, rowsB, [28, 70, 30, 38, 45, 36])
    # sets with identical arm lists are merged ("W = 0 and W = 5 sets"); the primary set runs all arms of Figure 1C
    runs = {}
    for r in T["sets"]:
        if r["arms"]:
            v = f"all {r['arms_run']} arms" if r["set"] == "primary causal set" else r["arms"].replace(" ", ", ")
            runs.setdefault(v, []).append(r["set"])
    runs = {" and ".join(k).replace("per-W set W = 0 and per-W set W = 5", "per-W sets W = 0 and W = 5"): v
            for v, k in runs.items()}
    bt.notes(doc, [
        "Cases: full-length DS203 videos of centres 2–5. Design cells: grid cells run in the set, each with 200 "
        "synthetic replicates. {sup:a}Arms run (Figure 1C): " + "; ".join(f"{k}, {v}" for k, v in runs.items()) + ".",
        "{sup:b}E1, E3-site, principal component analysis (PCA) and LEACE fitting; no causal grid. {sup:c}Selection "
        "(protocol §4.1 ranking and tie-breaks; Decision 005 for the reference): " + sel + ". s, switch step of the "
        "content state; n, number of 5-s steps; O, window offset; −C, linearly site-removed; nat, native frames.",
    ])
    doc.save(OUT / "Table_1_v2.docx")
    with open(OUT / "Table_1_v2.csv", "w", newline="") as f:
        w = csv.writer(f)
        for title, h, rows in (("(A)", hdrA, rowsA), ("(B)", hdrB, rowsB)):
            w.writerow([title]); w.writerow([x.replace("\n", " ") for x in h])
            for r in rows:
                w.writerow([str(x).replace("\n", " ") for x in r])
    return len(rowsA), len(rowsB)


def table2_v2():
    F = bt.canonical("fam_dbar")["rows"]
    gs = bt.canonical("gsite")
    doc = page(bt.new_document(landscape=True))
    bt.caption(doc, 2, "Family verdicts in the primary set (protocol §12.3) and the same families in the sensitivity "
                       "sets (§10.3).")
    hdr = ["Family", "Comparison (with vs without C)", "Cells", "Mean D (95% CI)", "Share D_j > 0", "Direction rule",
           "Failed (§13)", "Status"]
    order = [("primary", "Primary set, 158 cases (enters family verdicts)"),
             ("W0", "W = 0 set, 204 cases (sensitivity; reported separately)"),
             ("W5", "W = 5 set, 201 cases (sensitivity; reported separately)"),
             ("single_file", "Single-file set, 123 cases (sensitivity; reported separately)")]
    rows, spans = [], []
    for s, label in order:
        sub = [r for r in F if r["set"] == s and not r["role"].startswith("exploratory")]
        spans.append(len(rows)); rows.append([label] + [""] * 7)
        for r in sub:
            rows.append([r["family"], r["comparison"], str(r["n_cells"]), f"{r['D_bar_3dp']} ({r['ci_3dp']})",
                         r["share_2dp"], r["rule_verdict"].capitalize(),
                         "None" if r["conditions_failed"] == "none" else r["conditions_failed"], bt.status(r)])
    assert len(rows) - len(spans) == 18
    excluded = [r for r in F if r["role"].startswith("exploratory")]
    bt.add_table(doc, hdr, rows, [26, 47, 15, 48, 21, 26, 24, 40],
                 align=["l", "l", "r", "l", "r", "l", "l", "l"], spans=spans, span_space_pt=2)
    # family cell definitions from protocol §12.2 (canonical), families with the same cells merged
    defs = {}
    for r in F:
        if r["set"] == "primary":
            d = r["cells_definition"]
            if d.startswith("the same"):
                d = next(x["cells_definition"] for x in F if x["set"] == "primary" and x["family"] == "P1b-SITE")
            defs.setdefault(bt.typo(d), []).append(r["family"])
    bt.notes(doc, [
        "D_j = (|bias| without C − |bias| with C)/mean truth (P1) or (|bias| with C − |bias| without C)/mean truth (P2); "
        "positive = as predicted; dimensionless. Mean D = unweighted mean over the family's cells (D̄_F). 95% CI: paired "
        "bootstrap percentile interval (2,000 resamples of the 200 synthetic replicates within each cell, same indices "
        "for both arms and the truth; cells fixed): simulation uncertainty, not real-data sampling uncertainty.",
        "Direction rule (§12.3): supported if lower bound > 0 and D_j > 0 in ≥ 75% of cells; contradicted if upper "
        "bound < 0 or D_j > 0 in ≤ 25%; otherwise inconclusive. Only the primary set yields verdicts (consistent with "
        "the theory-motivated direction); families failing §13 (E3-site failed on the 158-case set; Supplementary "
        "Table S5) are not tested; sensitivity sets never enter verdicts.",
        "Cells (§12.2): " + "; ".join(f"{' and '.join(v)}, {k}" for k, v in defs.items()) + f". G-SITE (≤ 0.01): "
        f"primary {gs['primary']:.4f}, W = 0 {gs['W0']:.4f}, W = 5 {gs['W5']:.4f}; none for the single-file set. The "
        "W = 0 set's P1a (" + ", ".join(f"{r['n_cells']} cells" for r in excluded) + "; outside §10.3; exploratory) "
        "is not shown.",
        "C, site; NV, no video; ORACLE, exact content state and C; ORACLE−C, state without C; FM-P, primary "
        "representation; FM-P−C, FM-P after linear site removal.",
    ])
    doc.save(OUT / "Table_2_v2.docx")
    bt.write_csv(OUT / "Table_2_v2.csv", hdr, rows, spans)
    return len(rows)


def main():
    a, b = table1_v2()
    n2 = table2_v2()
    n3 = len(bt.table3(num="S5", stem="Table_S5_v2"))
    print(f"Table_1_v2: {a}+{b} rows; Table_2_v2: {n2} rows; Table_S5_v2: {n3} rows")


if __name__ == "__main__":
    main()
