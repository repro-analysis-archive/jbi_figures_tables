#!/usr/bin/env python3
"""Supplementary Tables S1–S6 (task CC_TASK_JBI_supplement_v6.md §4): Word .docx + CSV of the displayed cells; table
template rules as the main tables (Arial 11 pt; top, header-bottom and bottom rules only; bold header; "Table Sn." bold
only; footnotes; Normal style) via build_tables.py helpers. Values from hash-guarded canonical_supplement/ (the package
CSVs as text), formatted with the committed rounding (3 decimals, true minus sign); Table S1 keeps the recorded values
(exact grid values, as the committed table); Table S2 is Table_S5_v2 rebuilt with the caption number S2.

    .venv/bin/python -I scripts/build_tables_supp_v1.py
"""
import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build_tables", HERE / "build_tables.py")
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
ROOT, OUT = bt.ROOT, bt.OUT
MINUS = "−"
KEY = {"P": "FM-P", "S": "FM-S", "REF": "REF"}
ARM = {"FM-P-C": "FM-P−C", "FM-S-C": "FM-S−C", "REF-C": "REF−C"}
AN = {"a": "transport", "b": "within-set refit"}
PROBE = {"linear": "linear", "mlp": "MLP"}


def supp(name):
    p = ROOT / "canonical_supplement" / f"{name}.json"
    sums = dict(reversed(l.split()) for l in (ROOT / "canonical_supplement" / "SHA256SUMS.txt").read_text().splitlines())
    assert hashlib.sha256(p.read_bytes()).hexdigest() == sums[f"{name}.json"], f"hash guard failed: {name}"
    return json.loads(p.read_text())["rows"]


def f3(s):
    return f"{float(s):.3f}".replace("-", MINUS)


def iv(lo, hi):
    return f"({f3(lo)} to {f3(hi)})"


def comparator(s):
    return s.replace("step6 ", "step-6 ").replace("-C", MINUS + "C")


def save(doc, stem, hdr, rows, spans=()):
    doc.save(OUT / f"{stem}.docx")
    bt.write_csv(OUT / f"{stem}.csv", hdr, rows, spans)
    return len(rows) - len(spans)


# ------------------------------------------------------------------------------------------------ S1
def table_s1():
    T = supp("t_tableS4_mask_check")
    by = {(r["scope"], r["item"]): r["value"] for r in T}
    doc = bt.new_document(landscape=False)
    bt.caption(doc, "S1", "Mask check (protocol §3.1, step 3): visible radius of the grayscale mean standardized frame per "
                          "centre and the resulting mask radius.")
    hdr = ["Centre", "Frames in the mean frame", "Visible radius ρ_c (× side)"]
    rows = [[c, by[(f"centre {c}", "n_frames")], by[(f"centre {c}", "rho_c (visible_radius)")]] for c in ("2", "3", "4", "5")]
    bt.add_table(doc, hdr, rows, [30, 55, 60], align=["l", "r", "r"])
    bt.notes(doc, [
        f"min_c ρ_c = {by[('all centres', 'min_c rho_c (min_visible_radius)')]}; final mask radius r = "
        f"{by[('all centres', 'r (final mask radius, x side)')]} (× side). Rule (§3.1): r = 0.45 if min_c ρ_c ≥ 0.45, "
        f"otherwise r = 0.98 × min_c ρ_c; fallback: {by[('all centres', 'fallback r = 0.98 x min_c rho_c')]}. "
        f"Validity (run_meta.json mask_check_valid): {by[('all centres', 'mask_check_valid (run_meta.json)')]}.",
        "Values as recorded in the step-4 record (8d4c61a; package tableS4_mask_check.csv), not rounded; for centres 3–5, "
        "ρ_c equals the last point of the radial profile. Frames: every 60th grid frame of every case (256 × 256).",
    ])
    return save(doc, "Table_S1_v1", hdr, rows)


# ------------------------------------------------------------------------------------------------ S3
def table_s3(stem="Table_S3_v1", extra_notes=()):
    """stem / extra_notes: for the v7 rebuild (build_tables_supp_v2.py); the defaults give the v1 table."""
    T = supp("t_tableX_group_summaries")
    doc = bt.new_document(landscape=True)
    bt.caption(doc, "S3", "Exploratory X1/X2: group summaries of the per-cell Δ for every analysis, arm, comparator and "
                          "group.")
    hdr = ["Arm", "Comparator", "Group", "Cells", "Mean Δ (95% interval)", "Cells with Δ < 0"]
    rows, spans = [], []
    for an in ("X1", "X2"):
        spans.append(len(rows))
        rows.append([{"X1": "X1: eraser (LEACE) refitted on the 158-case analysis region",
                      "X2": "X2: linear-only nuisance learners"}[an]] + [""] * 5)
        for r in (x for x in T if x["analysis"] == an):
            rows.append([ARM[r["arm"]], comparator(r["comparator"]), r["group"], r["n_cells"],
                         f"{f3(r['mean_delta'])} {iv(r['mean_delta_lo'], r['mean_delta_hi'])}",
                         r["n_cells_delta_negative"]])
    bt.add_table(doc, hdr, rows, [30, 45, 30, 20, 70, 40], align=["l", "l", "l", "r", "l", "r"], spans=spans,
                 span_space_pt=2)
    bt.notes(doc, [
        "Exploratory (outside the frozen protocol; plan registered on OSF, osf.io/5c627); no verdict. Δ = (|bias| X arm − "
        "|bias| step-6 arm) / mean truth per cell, always X arm − step-6 arm (negative: the X arm has the smaller "
        "|bias|); mean Δ = unweighted mean over the group's cells; 95% interval: paired bootstrap percentile interval "
        "(2,000 resamples of the 200 synthetic replicates within each cell; cells fixed); simulation uncertainty, not "
        "real-data sampling uncertainty.",
        "Groups: P1b-FM, the 48 W = 0 cells with P = 5 or 30; P2-FM, the 12 cells with K = 1, P = 0, α > 0; slice, the 12 "
        "main-text slice cells (W = 30, α = 0.5, γ = 1, φ_A = 0); cell 15 belongs to P2-FM and the slice. −C, linearly "
        "site-removed; NV, no video.",
        "Ceiling (fact base §8): exploratory; no verdict; cannot restore P1b-FM/P2-FM; nonlinear site information remains "
        "after X1; X2 changes do not show that erasure caused a difference.",
    ] + list(extra_notes))
    return save(doc, stem, hdr, rows, spans)


# ------------------------------------------------------------------------------------------------ S4
S4_NEGZERO = (" A value shown as −0.000 is negative and rounds to zero at 3 decimals (committed rounding).")


def table_s4(stem="Table_S4_v1", negzero_sentence=S4_NEGZERO, extra_notes=()):
    """stem / negzero_sentence / extra_notes: for the v7 rebuild; the defaults give the v1 table."""
    T = supp("t_tableX_E3")
    v = {}
    for r in T:
        v[(r["block"].split(" ")[0], r["key"], r["probe"], r["condition"], r["field"])] = r["value"]
    doc = bt.new_document(landscape=True)
    bt.caption(doc, "S4", "Exploratory X1: E3-site, E2 and E3-state retention on the 158-case analysis region, next to "
                          "step 5.")
    p = doc.add_paragraph(); bt.rich(p, "(A) E3-site: case-level site balanced accuracy after removal"); p.paragraph_format.space_after = bt.Pt(3)
    hdrA = ["Representation", "Probe", "Step 5: BA (95% interval)", "Step 5: one-sided 95% upper bound",
            "X1: BA (95% interval)", "X1: one-sided 95% upper bound"]
    rowsA = []
    s5c, x1c = "step 5 (protocol LEACE)", "X1 (LEACE refitted on the analysis region)"
    for k in ("P", "S", "REF"):
        for pr in ("linear", "mlp"):
            g = lambda c, f: v[("E3-site", k, pr, c, f)]  # noqa: E731
            rowsA.append([KEY[k], PROBE[pr], f"{f3(g(s5c, 'ba'))} {iv(g(s5c, 'lo_2p5'), g(s5c, 'hi_97p5'))}",
                          f3(g(s5c, "upper_one_sided_95")), f"{f3(g(x1c, 'ba'))} {iv(g(x1c, 'lo_2p5'), g(x1c, 'hi_97p5'))}",
                          f3(g(x1c, "upper_one_sided_95"))])
    bt.add_table(doc, hdrA, rowsA, [34, 18, 52, 45, 52, 45], align=["l", "l", "l", "r", "l", "r"])
    p = doc.add_paragraph(); bt.rich(p, "(B) E2 primary: ΔAUC for S_t of base + R_t over base")
    p.paragraph_format.space_before = bt.Pt(5); p.paragraph_format.space_after = bt.Pt(3)
    hdrB = ["Representation", "Condition", "ΔAUC (95% CI)", "E2 criterion"]
    rowsB = []
    for k in ("P", "S", "REF"):
        for c in ("step 5, before removal", "step 5, after protocol removal", "X1, after X1 removal"):
            g = lambda f: v[("E2", k, "", c, f)]  # noqa: E731
            rowsB.append([KEY[k], c, f"{f3(g('delta_auc'))} {iv(g('ci_lo'), g('ci_hi'))}",
                          "met" if g("pass") == "true" else "not met"])
    bt.add_table(doc, hdrB, rowsB, [34, 70, 60, 40], align=["l", "l", "l", "l"])
    p = doc.add_paragraph(); bt.rich(p, "(C) E3-state retention (post / pre ΔAUC ≥ 0.50)")
    p.paragraph_format.space_before = bt.Pt(5); p.paragraph_format.space_after = bt.Pt(3)
    hdrC = ["Representation", "Step 5", "X1"]
    rowsC = []
    for k in ("P", "S", "REF"):
        cellv = []
        for c in ("step 5", "X1"):
            if v[("E3-state", k, "", c, "applicable")] == "true":
                cellv.append(f"retained fraction {f3(v[('E3-state', k, '', c, 'retained_fraction')])}")
            else:
                cellv.append("not applicable (E2 primary failed)")
        rowsC.append([KEY[k]] + cellv)
    bt.add_table(doc, hdrC, rowsC, [34, 80, 80], align=["l", "l", "l"])
    bt.notes(doc, [
        "Exploratory (X1; plan registered on OSF, osf.io/5c627); no verdict. X1 refits the LEACE eraser on the 158-case "
        "analysis region (training folds) and evaluates on held-out folds of the same population; step-5 values are the "
        "protocol LEACE fitted on the 278-case set. The linear E3-site value of X1 is a check of the procedure and does "
        "not gate X1. E3-site boundary 0.35 (one-sided upper bound); E2 criterion ΔAUC ≥ 0.05 and CI excluding 0. "
        "Intervals: case-level (cluster) bootstrap stratified by site (2,000 resamples)." + negzero_sentence,
        "Ceiling (fact base §8): exploratory; no verdict; cannot restore P1b-FM/P2-FM; nonlinear site information remains "
        "after X1; X2 changes do not show that erasure caused a difference. BA, balanced accuracy; MLP, two-layer "
        "multilayer perceptron probe.",
    ] + list(extra_notes))
    doc.save(OUT / f"{stem}.docx")
    with open(OUT / f"{stem}.csv", "w", newline="") as f:
        w = csv.writer(f)
        for title, h, rs in (("(A)", hdrA, rowsA), ("(B)", hdrB, rowsB), ("(C)", hdrC, rowsC)):
            w.writerow([title]); w.writerow(h)
            for r in rs:
                w.writerow(r)
    return len(rowsA) + len(rowsB) + len(rowsC)


# ------------------------------------------------------------------------------------------------ S5
def table_s5():
    T = supp("t_tableB_ba")
    J = supp("t_tableB_judgements")
    jd = {}
    for r in J:
        a, b = r["pair"].split("->")
        jd.setdefault((r["key"], r["analysis"], r["probe"], b), []).append(r["statement"])
    doc = bt.new_document(landscape=True)
    bt.caption(doc, "S5", "Exploratory B: case-level site balanced accuracy per representation, analysis, probe and "
                          "evaluation set, with the generated judgement statements.")
    hdr = ["Probe", "Set", "Cases", "Steps", "BA (95% interval)", "One-sided 95% upper bound", "Exceeds 0.35",
           "Judgement statements (pairs ending at this set)"]
    rows, spans = [], []
    for k in ("P", "S", "REF"):
        for an in ("a", "b"):
            spans.append(len(rows))
            rows.append([f"{KEY[k]}, {AN[an]}"] + [""] * 7)
            for r in (x for x in T if x["key"] == k and x["analysis"] == an):
                st = jd.get((k, an, r["probe"], r["set"]), [])
                rows.append([PROBE[r["probe"]], r["set"], r["cases"], r["rows"],
                             f"{f3(r['ba'])} {iv(r['lo_2p5'], r['hi_97p5'])}", f3(r["upper_one_sided_95"]),
                             "yes" if r["exceeds_boundary_0.35"] == "True" else "no",
                             "\n".join(st) if st else "—"])
    assert sum(len(x[7].split("\n")) for x in rows if x[7] not in ("", "—")) == len(J) == 36
    bt.add_table(doc, hdr, rows, [17, 12, 18, 18, 50, 30, 22, 80], align=["l", "l", "r", "r", "l", "r", "l", "l"],
                 spans=spans, span_space_pt=2)
    bt.notes(doc, [
        "Exploratory (outside the frozen protocol; plan registered on OSF, osf.io/g9ymw, after the step-7 verdicts had "
        "been generated); no verdict. Transport: the probe fitted as in E3 on S1 and evaluated on the held-out cases of "
        "each set; within-set refit: the probe refitted within each set; the two are separate analyses and are never "
        "pooled or contrasted. Sets: S1, 278 cases, all steps; S2, 158 primary cases, all steps; S3, 158 primary cases, "
        "analysis region (75 steps per case). Steps: step rows evaluated.",
        "BA, case-level site balanced accuracy (four centres; chance 0.25) after linear site removal; 95% interval and "
        "one-sided 95% upper bound: case-level bootstrap stratified by site (2,000 resamples). The boundary 0.35 applies "
        "to the upper bound. Judgement statements as generated by the analysis (b_judgements.csv) for the pairs "
        "S1→S2, S2→S3 and S1→S3, listed at the later set.",
        "Ceiling (fact base §9): B locates where the judgement changes; it does not identify why. The subsampling "
        "changes centre balance, case set and steps per case at the same time. MLP, two-layer multilayer perceptron.",
    ])
    return save(doc, "Table_S5_v1", hdr, rows, spans)


# ------------------------------------------------------------------------------------------------ S6
def table_s6():
    T = supp("t_tableB_sens")
    doc = bt.new_document(landscape=True)
    bt.caption(doc, "S6", "Exploratory B: equal-size subsampling (28 cases per centre, 75 steps per case, 20 draws).")
    hdr = ["Probe", "Set", "Draws", "Median BA", "2.5–97.5% across draws", "Min–max"]
    rows, spans = [], []
    for k in ("P", "S", "REF"):
        for an in ("a", "b"):
            spans.append(len(rows))
            rows.append([f"{KEY[k]}, {AN[an]}"] + [""] * 5)
            for r in (x for x in T if x["key"] == k and x["analysis"] == an):
                rows.append([PROBE[r["probe"]], r["set"], r["draws"], f3(r["median"]),
                             f"{f3(r['p2_5'])} to {f3(r['p97_5'])}", f"{f3(r['min'])} to {f3(r['max'])}"])
    bt.add_table(doc, hdr, rows, [25, 18, 20, 30, 55, 50], align=["l", "l", "r", "r", "l", "l"], spans=spans,
                 span_space_pt=2)
    bt.notes(doc, [
        "Exploratory (analysis B; plan registered on OSF, osf.io/g9ymw); no verdict. In each of S1–S3, 28 cases per centre "
        "and 75 steps per case were drawn 20 times; for each draw the point BA was computed (transport: the S1-fitted "
        "probe; within-set refit: refitted within the subsample); the table gives the median, the 2.5–97.5% range across "
        "the 20 draws and the minimum–maximum; descriptive point estimates, no bootstrap, no judgement.",
        "Ceiling (fact base §9): B locates where the judgement changes; it does not identify why. BA, case-level site "
        "balanced accuracy (chance 0.25); MLP, two-layer multilayer perceptron.",
    ])
    return save(doc, "Table_S6_v1", hdr, rows, spans)


def main():
    n = dict(S1=table_s1(), S2=len(bt.table3(num="S2", stem="Table_S2_v1")), S3=table_s3(), S4=table_s4(),
             S5=table_s5(), S6=table_s6())
    print("rows:", n)


if __name__ == "__main__":
    main()
