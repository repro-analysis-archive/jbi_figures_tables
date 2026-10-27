#!/usr/bin/env python3
"""Freeze every value of the supplementary figures and tables (task CC_TASK_JBI_supplement_v6.md) from the read-only
package into canonical_supplement/ (JSON + CSV mirrors, SHA256SUMS.txt, inputs_sha256.json, validation.json).

Numerical computation / data freezing only (figure template §3). Values are copied from the committed records; the
only derived quantity is D for Figure S1, computed with the committed `contrast` formula of freeze.py
(D = (|bias| without C − |bias| with C) / mean truth) and checked against every D_j of families.json. Every package
input is guarded by the package manifest (and by the hash recorded by its generating step where one exists); the main
canonical files used for cross-checks are guarded by canonical/SHA256SUMS.txt. The main canonical/ is not written.
Display strings follow the committed rounding (3 decimals; true minus sign) and the task: D 3 decimals with sign,
relative bias in % with one decimal and sign, coverage 2 decimals.

    .venv/bin/python -I scripts/freeze_supplement.py
"""
import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("freeze", HERE / "freeze.py")
fz = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fz)
PKG, ROOT = fz.PKG, fz.ROOT
OUT = ROOT / "canonical_supplement"
SUP = "03_results/SUPPLEMENT_20261020/"
INPUTS = {   # name: (package path, SHA-256 recorded by the generating step or None)
    "cell_metrics": fz.INPUTS["cell_metrics"],
    "families": fz.INPUTS["families"],
    "report_cells": ("03_results/RESULTS_20261019/report_cells.csv", None),
    "x_cells": fz.INPUTS["x_cells"],
    "x_groups": fz.INPUTS["x_groups"],
    "b_main": fz.INPUTS["b_main"],
    "b_judgements": ("04_exploratory/B/results_B/b_judgements.csv",
                     "09f1c088df6e4eacb324916b1e08a9a8ac4a23303d4d668d35337781e0f8a5ad"),     # SUPPLEMENT SOURCES.md
    "b_sens": ("04_exploratory/B/results_B/b_sensitivity_summary.csv",
               "84b4cf4952669ff52981d4e99d94c7fbe67f9139d4d7e36e784298befbdb0148"),           # SUPPLEMENT SOURCES.md
    "tableS4_mask_check": (SUP + "tableS4_mask_check.csv", None),
    "tableX_group_summaries": (SUP + "tableX_group_summaries.csv", None),
    "tableX_E3": (SUP + "tableX_E3.csv", None),
    "tableB_ba": (SUP + "tableB_ba.csv", None),
    "tableB_judgements": (SUP + "tableB_judgements.csv", None),
    "tableB_sens": (SUP + "tableB_sens.csv", None),
    "supplement_captions": (SUP + "CAPTIONS.md", None),
    "supplement_sources": (SUP + "SOURCES.md", None),
    "presentation_decisions": fz.INPUTS["presentation_decisions"],
}
# provided by the investigator (not in the package): the step-4 record's mask_check.json, placed in inputs/; guarded by
# the blob SHA-256 recorded in the package SUPPLEMENT_20261020/SOURCES.md (repository medical_video_causal_gate, 8d4c61a)
MASK = ("inputs/mask_check.json", "81c8eb46fa7abba4cb5024e073e30cc838c011d2d62488abbde72d73434d58d5")
PAIRS = [("SITE", "NV"), ("FM-P", "FM-P-C"), ("FM-S", "FM-S-C"), ("REF", "REF-C"), ("ORACLE", "ORACLE-C")]
ARMS = fz.BC_ARMS                    # NV, SITE, FM-P, FM-P-C, FM-S, FM-S-C, REF, REF-C, FM-P-nat, ORACLE-C, ORACLE, FULL
KEYS = ["K", "P", "W", "alpha", "gamma", "phi"]
MINUS = "−"


def sgn(x, d):
    return f"{x:+.{d}f}".replace("-", MINUS)


def f3(x):
    return f"{x:.3f}".replace("-", MINUS)


def guard():
    man = fz.load_manifest()
    rec = {}
    for name, (rel, recorded) in INPUTS.items():
        actual = fz.sha256(PKG / rel)
        assert man[rel] == actual, f"manifest mismatch: {rel}"
        if recorded is not None:
            assert recorded == actual, f"recorded-hash mismatch: {rel}"
        rec[name] = dict(path=rel, sha256=actual, manifest="match",
                         recorded_by_generating_step="match" if recorded else "none recorded")
    return rec


def main_canonical(name):
    p = ROOT / "canonical" / f"{name}.json"
    sums = dict(reversed(line.split()) for line in (ROOT / "canonical" / "SHA256SUMS.txt").read_text().splitlines())
    assert hashlib.sha256(p.read_bytes()).hexdigest() == sums[f"{name}.json"], f"hash guard failed: canonical/{name}"
    return json.loads(p.read_text())


def write(name, obj, rows=None):
    (OUT / f"{name}.json").write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")
    if rows is not None:
        with open(OUT / f"{name}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow(r)


def cell_key(r):
    return dict(cell=int(r.cell), K=int(r.K), P=int(r.P), W=int(r.W), alpha=float(r.alpha), gamma=float(r.gamma),
                phi=float(r.phi))


# ---------------------------------------------------------------------------------------------- Figures S1–S3
def s1_rows(prim):
    rows = []
    for w, wo in PAIRS:
        d = fz.contrast(prim, w, wo).reset_index().sort_values(["phi", "W", "alpha", "gamma", "K", "P"])
        assert len(d) == 240
        for r in d.itertuples(index=False):
            rows.append(dict(pair=f"{fz.lab(w)} vs {fz.lab(wo)}", with_arm=fz.lab(w), without_arm=fz.lab(wo),
                             **cell_key(r), abs_bias_with=float(r.abs_bias_with),
                             abs_bias_without=float(r.abs_bias_without), mean_truth=float(r.mean_truth),
                             D=float(r.D), D_disp=sgn(float(r.D), 3),
                             source="cell_metrics.csv (set primary) -> abs_bias, mean_truth; formula contrast"))
    return rows


def s23_rows(prim, rc):
    """report_cells.csv is a re-serialisation of cell_metrics.csv (last-digit float differences, <= 1e-12 relative):
    values come from cell_metrics.csv (hash recorded by step 7); report_cells.csv must agree within 1e-12 relative and
    give the same display strings."""
    rows, worst = [], 0.0
    rcp = rc[rc.set == "primary"].set_index(["cell", "arm"])
    for a in ARMS:
        for r in prim[prim.arm == a].sort_values(["phi", "W", "alpha", "gamma", "K", "P"]).itertuples(index=False):
            q = rcp.loc[(int(r.cell), a)]
            rb = float(r.rel_bias)
            assert abs(q.rel_bias - rb) <= 1e-12 * abs(rb) and q.coverage == r.coverage, (a, r.cell)
            assert sgn(100.0 * q.rel_bias, 1) == sgn(100.0 * rb, 1), (a, r.cell)
            worst = max(worst, abs(q.rel_bias - rb) / abs(rb))
            rows.append(dict(arm=fz.lab(a), arm_record=a, **cell_key(r), M=int(r.M), M_finite=int(r.M_finite),
                             rel_bias=rb, rel_bias_pct=100.0 * rb, rel_bias_disp=sgn(100.0 * rb, 1),
                             coverage=float(r.coverage), coverage_disp=f"{float(r.coverage):.2f}",
                             source="cell_metrics.csv (set primary) -> rel_bias, coverage (= report_cells.csv)"))
    return rows, worst


# ---------------------------------------------------------------------------------------------- Figure S5
S5_SLICE = [("X1", "minusC"), ("X1", "FM"), ("X2", "minusC")]     # their P1b-FM / P2-FM cells are in main Figure 6
S5_ALL = [("X1", "NV"), ("X2", "NV"), ("X2", "FM")]               # not in main Figure 6 at all
S5_ARMS = ["FM-P-C", "FM-S-C", "REF-C"]


def s5_rows(xc):
    """Per-cell Δ of every (analysis, comparison, arm, group) not in main Figure 6, in main-Figure-6 cell order:
    P1b-FM by (P, K, alpha, gamma); P2-FM by cell index (W, alpha, gamma); slice by (P, K). Cell 15 belongs to both
    P2-FM and the slice and is shown in both groups (as in the package figX)."""
    rows = []
    groups = {g: xc[xc.groups.str.split(",").apply(lambda s: g in s)] for g in ("P1b-FM", "P2-FM", "slice")}
    keyf = {"P1b-FM": lambda d: d.sort_values(["P", "K", "alpha", "gamma"]),
            "P2-FM": lambda d: d.sort_values(["cell"]), "slice": lambda d: d.sort_values(["P", "K"])}
    for page, combos, gl in (("slice", S5_SLICE, ["slice"]), ("all", S5_ALL, ["P1b-FM", "P2-FM", "slice"])):
        for an, cmpn in combos:
            for arm in S5_ARMS:
                for g in gl:
                    d = groups[g]
                    d = keyf[g](d[(d.analysis == an) & (d.comparison == cmpn) & (d.arm == arm)])
                    assert len(d) == {"P1b-FM": 48, "P2-FM": 12, "slice": 12}[g], (an, cmpn, arm, g, len(d))
                    for i, r in enumerate(d.itertuples(index=False)):
                        rows.append(dict(page=page, analysis=an, comparison=cmpn, arm=fz.lab(arm),
                                         comparator=r.comparator.replace("step6 ", "step-6 ").replace("-C", MINUS + "C"),
                                         group=g, order=i + 1, cell=int(r.cell), K=int(r.K), P=int(r.P), W=int(r.W),
                                         alpha=float(r.alpha), gamma=float(r.gamma), M=int(r.M),
                                         delta=float(r.delta), delta_lo=float(r.delta_lo), delta_hi=float(r.delta_hi),
                                         source=f"x_comparisons_cells.csv[{r.seed_name}]"))
    return rows


# ---------------------------------------------------------------------------------------------- tables
def table_rows(csvpath):
    return pd.read_csv(PKG / csvpath, dtype=str, keep_default_na=False).to_dict("records")


def main():
    OUT.mkdir(exist_ok=True)
    rec = guard()
    mask_raw = (ROOT / MASK[0]).read_bytes()
    assert hashlib.sha256(mask_raw).hexdigest() == MASK[1], "mask_check.json hash differs from SOURCES.md"
    assert MASK[1] in (PKG / INPUTS["supplement_sources"][0]).read_text(), "hash not listed in SOURCES.md"
    rec["mask_check"] = dict(path=MASK[0], sha256=MASK[1], manifest="not in the package (provided by the investigator)",
                             recorded_by_generating_step="match (SUPPLEMENT_20261020/SOURCES.md, 8d4c61a)")
    cm = pd.read_csv(PKG / INPUTS["cell_metrics"][0])
    prim = cm[cm.set == "primary"]
    assert len(prim) == 2880 and prim.cell.nunique() == 240 and (prim.M_finite == 200).all()
    rc = pd.read_csv(PKG / INPUTS["report_cells"][0])
    fams = json.loads((PKG / INPUTS["families"][0]).read_text())
    xc = pd.read_csv(PKG / INPUTS["x_cells"][0])
    bm = pd.read_csv(PKG / INPUTS["b_main"][0])
    val = {}

    s1 = s1_rows(prim)
    s23, rc_worst = s23_rows(prim, rc)
    s5 = s5_rows(xc)

    # ---- cross-checks against the main-figure canonical values and the family records (exact equality)
    by1 = {(r["pair"], r["cell"]): r for r in s1}
    by23 = {(r["arm"], r["cell"]): r for r in s23}
    wh = main_canonical("w_history_D")["rows"]
    assert all(by1[(r["pair"], r["cell"])]["D"] == r["D_without_minus_with"] for r in wh)
    sl = main_canonical("fig2B_slice_D")["rows"]
    assert all(by1[(r["pair"], r["cell"])]["D"] == r["D_without_minus_with"] for r in sl)
    bc = main_canonical("fig5_bias_coverage")["rows"]
    assert all(by23[(r["arm"], r["cell"])]["rel_bias"] == r["rel_bias"] and
               by23[(r["arm"], r["cell"])]["coverage"] == r["coverage"] for r in bc)
    fam_pair = {"P1a": "ORACLE vs ORACLE−C", "P1b-SITE": "SITE vs NV", "P1b-FM": "FM-P vs FM-P−C",
                "P2-SITE": "SITE vs NV", "P2-FM": "FM-P vs FM-P−C", "P2-ORACLE": "ORACLE vs ORACLE−C"}
    fam_check = {}
    for f, pair in fam_pair.items():
        v = fams[f"primary:{f}"]
        sign = 1.0 if v["kind"] == "P1" else -1.0
        cells = sorted(int(c) for c in v["D_cells"])
        vals = np.array([sign * by1[(pair, c)]["D"] for c in cells])
        assert np.allclose(vals, [v["D_cells"][str(c)] for c in cells], rtol=1e-9, atol=0), f
        fam_check[f] = dict(pair=pair, cells=len(cells), mean_from_S1=float(vals.mean()), D_bar=v["D_bar"],
                            mean_3dp=f3(float(vals.mean())), D_bar_3dp=f3(v["D_bar"]),
                            max_abs_diff_cells=float(np.max(np.abs(vals - np.array([v["D_cells"][str(c)] for c in cells])))))
        assert fam_check[f]["mean_3dp"] == fam_check[f]["D_bar_3dp"]
    a1 = by1[("SITE vs NV", next(r["cell"] for r in s1 if r["pair"] == "SITE vs NV" and r["W"] == 0 and r["K"] == 1 and
                                   r["P"] == 30 and r["alpha"] == 0.5 and r["gamma"] == 1.0 and r["phi"] == 0.0))]
    assert a1["D_disp"] == "+8.734"
    a2 = by23[("NV", next(r["cell"] for r in s23 if r["arm"] == "NV" and r["W"] == 30 and r["K"] == 1 and r["P"] == 0 and
                            r["alpha"] == 0.5 and r["gamma"] == 1.0 and r["phi"] == 0.0))]
    assert a2["coverage_disp"] == "0.85"
    val["anchors"] = {"SITE vs NV, W = 0, K = 1, P = 30 (alpha 0.5, gamma 1), D": a1["D"],
                      "NV, W = 30, K = 1, P = 0 (alpha 0.5, gamma 1), coverage": a2["coverage"]}
    val["cross_checks"] = dict(
        w_history_D_rows_equal=len(wh), fig2B_slice_rows_equal=len(sl), fig5_bias_coverage_rows_equal=len(bc),
        report_cells_agree_with_cell_metrics=dict(rows=len(s23), max_rel_diff_rel_bias=rc_worst, coverage="identical",
                                                  display_strings="identical"),
        families_reproduced=fam_check)

    # ---- S5 vs main Figure 6: no overlap, and the shared rows of the x canonical are equal
    main_x = main_canonical("fig4_x_cells")["rows"]
    in_main = {(r["analysis"], r["comparison"], r["arm"], r["group"], r["cell"]) for r in main_x}
    assert not any((r["analysis"], r["comparison"], r["arm"], r["group"], r["cell"]) in in_main for r in s5)
    assert len(s5) == 3 * 3 * 12 + 3 * 3 * 72, len(s5)

    # ---- S6: the 36 B rows; equal to the main canonical fig3_ba B blocks (main Figure 2 (B), (C))
    s6 = []
    for r in bm.sort_values(["key", "analysis", "probe", "set"]).itertuples(index=False):
        s6.append(dict(key=r.key, key_label=fz.KEY_LABEL[r.key], analysis=r.analysis,
                       analysis_label="transport" if r.analysis == "a" else "within-set refit", probe=r.probe,
                       set=r.set, cases=int(r.cases), ba=float(r.ba), lo_2p5=float(r.lo_2p5), hi_97p5=float(r.hi_97p5),
                       upper_one_sided_95=float(r.upper_one_sided_95), source=f"b_main.csv[{r.boot_name}]"))
    assert len(s6) == 36
    fb = {(r["key"], r["block"], r["probe"], r["set"]): r for r in main_canonical("fig3_ba")["rows"]}
    for r in s6:
        m = fb[(r["key"], "B transport" if r["analysis"] == "a" else "B within-set refit", r["probe"], r["set"])]
        assert (m["ba"], m["lo_2p5"], m["hi_97p5"], m["upper_one_sided_95"]) == \
               (r["ba"], r["lo_2p5"], r["hi_97p5"], r["upper_one_sided_95"]), r
    val["cross_checks"]["S6_equals_main_figure_2_BC_rows"] = 36

    # ---- tables: package CSVs as text (values unchanged); table builders format them
    tabs = {name: table_rows(INPUTS[name][0]) for name in ("tableS4_mask_check", "tableX_group_summaries", "tableX_E3",
                                                           "tableB_ba", "tableB_judgements", "tableB_sens")}
    assert [len(tabs[k]) for k in tabs] == [12, 54, 132, 36, 36, 36], [len(tabs[k]) for k in tabs]
    xg = pd.read_csv(PKG / INPUTS["x_groups"][0], dtype=str, keep_default_na=False).to_dict("records")
    assert xg == tabs["tableX_group_summaries"]                          # byte-level copy in the package
    bj = pd.read_csv(PKG / INPUTS["b_judgements"][0], dtype=str, keep_default_na=False).to_dict("records")
    assert bj == tabs["tableB_judgements"]
    bs = pd.read_csv(PKG / INPUTS["b_sens"][0], dtype=str, keep_default_na=False).to_dict("records")
    assert bs == tabs["tableB_sens"]

    write("s1_contrast_D", dict(description="Figure S1: per-cell D = (|bias| without C − |bias| with C) / mean truth, "
                                            "primary set, all 240 cells, 5 with/without-C pairs", rows=s1), s1)
    write("s23_bias_coverage", dict(description="Figures S2, S3: relative bias and coverage of the Wald 95% interval, "
                                                "primary set, all 240 cells, 12 arms", arms=[fz.lab(a) for a in ARMS],
                                    rows=s23), s23)
    # ---- S4: per-centre radial profiles; cross-checked with the package table (n_frames, rho_c, min, r)
    mk = json.loads(mask_raw)
    t4 = {(r["scope"], r["item"]): r["value"] for r in tabs["tableS4_mask_check"]}
    s4 = []
    for c in ("2", "3", "4", "5"):
        pr = mk["profiles"][c]
        assert len(pr["rho"]) == len(pr["m"]) == 180
        assert str(pr["n_frames"]) == t4[(f"centre {c}", "n_frames")]
        assert float(t4[(f"centre {c}", "rho_c (visible_radius)")]) == mk["visible_radius"][c]
        for i, (rho, m) in enumerate(zip(pr["rho"], pr["m"])):
            s4.append(dict(centre=int(c), point=i + 1, rho=float(rho), m=float(m), n_frames=int(pr["n_frames"]),
                           visible_radius=float(mk["visible_radius"][c]), source=f"mask_check.json profiles.{c}"))
    for c in ("3", "4", "5"):
        assert mk["profiles"][c]["rho"][-1] == mk["visible_radius"][c]          # rho_c = last profile point (table note)
    assert float(t4[("all centres", "min_c rho_c (min_visible_radius)")]) == mk["min_visible_radius"] == \
        min(mk["visible_radius"].values())
    assert float(t4[("all centres", "r (final mask radius, x side)")]) == mk["r"] == 0.45
    write("s4_mask_profiles", dict(description="Figure S4: per-centre radial profiles m_c(rho) of the grayscale mean "
                                               "standardized frame (180 points per centre), visible radius rho_c per "
                                               "centre, minimum and mask radius r (step-4 record 8d4c61a)",
                                   r=mk["r"], min_visible_radius=mk["min_visible_radius"],
                                   visible_radius={c: mk["visible_radius"][c] for c in ("2", "3", "4", "5")}, rows=s4), s4)
    val["cross_checks"]["S4_equals_tableS4_mask_check"] = "n_frames, rho_c (4 centres), min rho_c, r"
    write("s5_x_cells", dict(description="Figure S5: exploratory X1/X2 per-cell Δ not shown in main Figure 6 (slice "
                                         "group of X1 k−C vs step-6 k−C, X1 k−C vs step-6 k, X2 k−C vs step-6 k−C; all "
                                         "groups of X1 vs step-6 NV, X2 vs step-6 NV, X2 vs step-6 k)", rows=s5), s5)
    write("s6_b", dict(description="Figure S6: exploratory B balanced accuracy (36 rows of b_main.csv)", rows=s6), s6)
    for name, rows in tabs.items():
        write("t_" + name, dict(source=INPUTS[name][0], rows=rows), rows)
    write("inputs_sha256", rec)
    val.update(s4_values=len(s4), s1_values=len(s1), s2_values=len(s23), s3_values=len(s23), s5_values=len(s5), s6_values=len(s6),
               s1_round_to_zero_3dp=sum(r["D_disp"] in ("+0.000", MINUS + "0.000") for r in s1),
               s2_round_to_zero_1dp=sum(r["rel_bias_disp"] in ("+0.0", MINUS + "0.0") for r in s23),
               figure_S4="inputs/mask_check.json (provided by the investigator; SHA-256 equals the blob hash in "
                         "SUPPLEMENT_20261020/SOURCES.md); 4 x 180 points; consistent with tableS4_mask_check.csv")
    write("validation", val)
    files = sorted(p for p in OUT.iterdir() if p.suffix in (".json", ".csv"))
    (OUT / "SHA256SUMS.txt").write_text("".join(f"{fz.sha256(p)}  {p.name}\n" for p in files))
    print(f"inputs guarded {len(rec)}; S1 {len(s1)}, S2/S3 {len(s23)}, S5 {len(s5)}, S6 {len(s6)} values; families "
          f"reproduced {', '.join(f'{k} {v['mean_3dp']}' for k, v in fam_check.items())}; files {len(files)}")


if __name__ == "__main__":
    main()
