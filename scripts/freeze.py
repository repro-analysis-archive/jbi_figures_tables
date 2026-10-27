#!/usr/bin/env python3
"""Freeze every plotted or tabulated value of the JBI figures and tables from the read-only SS-DS203 package.

Numerical computation / data freezing only (figure template §3). Nothing here re-estimates anything:
  * values are copied from committed records (families.json, cell_metrics.csv, checks.json, x1_e3.json,
    x_comparisons_cells.csv, b_main.csv, the package tables and the protocol);
  * the only derived quantity is the per-cell oriented difference D_j at the main-text slice (Figure 2B), computed with
    the committed plotting formula `contrast` of step7_prep make_figures.py (c938a56) from cell_metrics.csv and
    asserted equal to every D_j stored in families.json (all sets, all families).
Every input is SHA-256-guarded against the package manifest and, where one exists, against the hash recorded by the
generating step. Anchors of the task (§2.1) are asserted. Output: canonical/*.json (+ .csv mirrors), SHA256SUMS.txt.

    .venv/bin/python -I scripts/freeze.py
"""
import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

PKG = Path("/Volumes/ADDATA/医療動画/SS_DS203_manuscript_20261020")
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "canonical"

# name: (path in the package, SHA-256 recorded by the generating step or None)
INPUTS = {
    "families": ("02_records/step7_record_2880d73/results/step7/families.json",
                 "06ab647e679df65f5b617bceae7e42fff92ef8236fe29d5420f4ffa5ac8f71d5"),   # step7_manifest.json
    "cell_metrics": ("02_records/step7_record_2880d73/results/step7/cell_metrics.csv",
                     "588f991bd81a4f71a0b49e12d98521a4df11a286f49722757ba65b254efca0e8"),  # step7_manifest.json
    "step6_run_record": ("02_records/step7_record_2880d73/results/step6/run_record.json", None),
    "checks5": ("02_records/step5_record_0ebf2cf/checks.json",
                "ea4cfebf673cd94ef2904a0a5b5fe99b44619985ce5f022af38eac010a26b6e4"),    # SOURCES.md, REPORT.md
    "section13": ("02_records/section13_record_0667430/section13.json",
                  "36836684363ea0a51507405ad3a6692086288c44ce35ff3024951163baae1a35"),  # REPORT.md
    "grid_conditions": ("02_records/section13_record_0667430/grid_conditions.json", None),
    "gsite": ("08_additional/codelock/results_codelock_gate/gsite_record.json",
              "e09d78700455805bef3d37ada89d0d8a9160455fa02df56c6f094d212daad8f5"),      # REPORT.md
    "x1_e3": ("04_exploratory/X1_X2/results_X/x1_e3.json",
              "d95fe9752eb43ec0ef808d5e4c8d0ea48ab6f3e17a986575b817bfcdb92287bb"),      # SOURCES.md
    "x_cells": ("04_exploratory/X1_X2/results_X/x_comparisons_cells.csv",
                "3e6adde59f73aa00fc1fae57aa0851a365479293c203987b24e2fc5361c54637"),    # SOURCES.md
    "x_groups": ("04_exploratory/X1_X2/results_X/x_comparisons_groups.csv",
                 "98da2fc2b19176aa0c49c39f5260ef120511748c496fa7a968a3609e38d21fa6"),   # SOURCES.md
    "b_main": ("04_exploratory/B/results_B/b_main.csv",
               "0087268599b408e1f8988b52b4890c81c724815e9af27211949bdbe9dfa5ad81"),     # SOURCES.md
    "table1_sets": ("03_results/RESULTS_20261019/figures/table1_data_sets.csv", None),
    "table2_models": ("03_results/RESULTS_20261019/figures/table2_models.csv", None),
    "protocol": ("01_protocol/SS_PROTOCOL_DS203.md", None),
    "fact_base": ("02_records/SS_DS203_PROJECT_RECORD_for_evaluator_20261020_v5.md",
                  "c1d8d651535136907b461e2666b4671d4fc58c736a78e6bb61fbcac54dc27684"),  # POST_RESULT_PRESENTATION.md
    "presentation_decisions": ("03_results/PRESENTATION_DECISIONS.md", None),
    "key_commits": ("07_provenance/main_repository_key_commits.md", None),
}

# Task §2.1 anchors (exact values)
ANCHORS = {
    "primary:P1b-SITE D_bar": 2.197616863578595,
    "primary:P2-SITE D_bar": 0.052105083645894015,
    "X1 FM-P-C vs step6 FM-P, P1b-FM, mean delta": 0.5609627059097283,
}

SLICE = dict(W=30, alpha=0.5, gamma=1.0, phi=0.0)          # PRESENTATION_DECISIONS.md decision 1
ARM_LABEL = {"FM-P-C": "FM-P−C", "FM-S-C": "FM-S−C", "REF-C": "REF−C", "ORACLE-C": "ORACLE−C"}
KEY_LABEL = {"P": "FM-P", "S": "FM-S", "REF": "REF", "P-nat": "FM-P-nat"}
SET_LABEL = {"primary": "Primary (n = 158)", "W0": "W = 0 set (n = 204)", "W5": "W = 5 set (n = 201)",
             "single_file": "Single-file set (n = 123)"}


def f3(x):
    """Display string with 3 decimals and a true minus sign (U+2212); the single formatting rule for Table 2,
    Table 3 and the graphical abstract (3 decimals = the rounding of the committed reports)."""
    t = f"{x:.3f}"
    return t.replace("-", "−")


def lab(arm):
    return ARM_LABEL.get(arm, arm)


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_manifest():
    out = {}
    for line in (PKG / "MANIFEST_SHA256.txt").read_text().splitlines():
        h, p = line.split(None, 1)
        out[p[2:] if p.startswith("./") else p] = h
    return out


def guard_inputs():
    man = load_manifest()
    rec = {}
    for name, (rel, recorded) in INPUTS.items():
        actual = sha256(PKG / rel)
        assert man[rel] == actual, f"manifest mismatch: {rel}"
        if recorded is not None:
            assert recorded == actual, f"recorded-hash mismatch: {rel}"
        rec[name] = dict(path=rel, sha256=actual, manifest="match",
                         recorded_by_generating_step="match" if recorded else "none recorded")
    return rec


def write(name, obj, rows=None):
    """canonical/<name>.json (full precision; MATLAB reads only these) and, for row data, a CSV mirror (RFC 4180)."""
    (OUT / f"{name}.json").write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")
    if rows is not None:
        cols = list(rows[0].keys())
        with open(OUT / f"{name}.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for r in rows:
                w.writerow(r)


def close(a, b, tol=1e-12):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --------------------------------------------------------------------------------------------- families (Fig 2A, T2)
def contrast(cm, w, wo):
    """Committed step7_prep make_figures.py `contrast`: D = (|bias| without C − |bias| with C) / mean truth."""
    a = cm[cm.arm == w].set_index("cell")
    b = cm[cm.arm == wo].set_index("cell")
    j = a.index.intersection(b.index)
    out = a.loc[j, ["K", "P", "W", "alpha", "gamma", "phi"]].copy()
    assert np.allclose(a.loc[j, "mean_truth"], b.loc[j, "mean_truth"], rtol=0, atol=0), "truth differs between arms"
    out["abs_bias_with"] = a.loc[j, "abs_bias"]
    out["abs_bias_without"] = b.loc[j, "abs_bias"]
    out["mean_truth"] = a.loc[j, "mean_truth"]
    out["D"] = (b.loc[j, "abs_bias"] - a.loc[j, "abs_bias"]) / a.loc[j, "mean_truth"]
    return out


def validate_families(fams, cm_all):
    """Every stored D_j equals the contrast formula on cell_metrics (P2 sign reversed); D̄ = mean D_j; share."""
    n = 0
    worst = 0.0
    for key, v in fams.items():
        s = v["set"]
        cm = cm_all[cm_all.set == s]
        d = contrast(cm, v["with_arm"], v["without_arm"])
        sign = 1.0 if v["kind"] == "P1" else -1.0
        cells = sorted(int(c) for c in v["D_cells"])
        assert len(cells) == v["n_cells"], key
        for c in cells:
            mine = sign * float(d.loc[c, "D"])
            rec = float(v["D_cells"][str(c)])
            worst = max(worst, abs(mine - rec))
            assert close(mine, rec, 1e-9), (key, c, mine, rec)
            n += 1
        dc = np.array([float(v["D_cells"][str(c)]) for c in cells])
        assert close(float(dc.mean()), v["D_bar"], 1e-12), key
        assert close(float((dc > 0).mean()), v["share_positive"], 1e-12), key
        assert v["ci_lo"] <= v["D_bar"] <= v["ci_hi"], key
    return n, worst


def protocol_families(proto):
    """Protocol §12.2 family table: cells (definition) and prediction, markdown stripped."""
    sec = proto.split("### 12.2 Families", 1)[1].split("### 12.3", 1)[0]
    out = {}
    for line in sec.splitlines():
        c = [x.strip().replace("\x00", "|") for x in line.replace("\\|", "\x00").strip().strip("|").split("|")]
        if len(c) == 5 and c[0] not in ("family", "---") and not c[0].startswith("-"):
            clean = [re.sub(r"\*\*\[v0\.4-final2?\]\*\* ?|\*\*|\\", "", x).strip() for x in c]
            out[clean[0]] = dict(cells_definition=clean[2], prediction=clean[3], conditions_protocol=clean[4])
    return out


def family_rows(fams, gsite, sec13, pf):
    """All families of families.json with their role; W0:P1a (outside the §10.3 scope) is role 'exploratory'."""
    scope_103 = {"W0": {"P1b-SITE", "P1b-FM", "P2-SITE", "P2-FM", "P2-ORACLE"},
                 "W5": {"P1b-SITE", "P1b-FM", "P2-SITE", "P2-FM", "P2-ORACLE"},
                 "single_file": {"P1b-SITE", "P1b-FM", "P2-SITE", "P2-FM"}}   # protocol §10.3 (arms run per set)
    order_f = ["P1a", "P1b-SITE", "P1b-FM", "P2-SITE", "P2-FM", "P2-ORACLE"]
    order_s = ["primary", "W0", "W5", "single_file"]
    rows = []
    for key, v in fams.items():
        s, f = v["set"], v["family"]
        if s == "primary":
            role = "primary (enters verdicts)"
        elif f in scope_103[s]:
            role = "sensitivity (§10.3; reported separately)"
        else:
            role = "exploratory (outside the §10.3 scope)"
        tested = not v["conditions_failed"]
        if s == "primary":
            reported = (f"{v['verdict']}: consistent with the theory-motivated direction" if tested and
                        v["verdict"] == "SUPPORTED" else "Not tested (§13); descriptive")
        elif role.startswith("sensitivity"):
            reported = ("Same direction rule met; reported separately (not a verdict)" if tested and
                        v["rule_verdict"] == "SUPPORTED" else
                        ("Not tested (§13); descriptive" if not tested else
                         f"Direction rule {v['rule_verdict']}; reported separately (not a verdict)"))
        else:
            reported = "Exploratory; not a verdict"
        gs = None
        if v["kind"] == "P2":
            gs = gsite["sets"][s]["eta2_S_window_start"] if s in gsite["sets"] else None
        rows.append(dict(
            set=s, set_label=SET_LABEL[s], family=f, kind=v["kind"], with_arm=lab(v["with_arm"]),
            without_arm=lab(v["without_arm"]), comparison=f"{lab(v['with_arm'])} vs {lab(v['without_arm'])}",
            n_cells=v["n_cells"], D_bar=v["D_bar"], ci_lo=v["ci_lo"], ci_hi=v["ci_hi"],
            share_positive=v["share_positive"], rule_verdict=v["rule_verdict"], locked_verdict=v["verdict"],
            conditions_required=" + ".join(v["conditions_required"]) or "none",
            conditions_failed=" + ".join(v["conditions_failed"]) or "none", tested=tested,
            enters_verdicts=v["enters_verdicts"], role=role, reported=reported,
            gsite_eta2_set=gs if gs is not None else "",
            cells_definition=pf[f]["cells_definition"], prediction=pf[f]["prediction"],
            in_fig2A=bool(f in ("P1a", "P1b-SITE", "P2-SITE", "P2-ORACLE") and not role.startswith("exploratory")),
            D_bar_3dp=f3(v["D_bar"]), ci_3dp=f"{f3(v['ci_lo'])} to {f3(v['ci_hi'])}",
            share_2dp=f"{v['share_positive']:.2f}",
            source=f"families.json['{key}']"))
    rows.sort(key=lambda r: (order_s.index(r["set"]), order_f.index(r["family"])))
    assert set(sec13["families_tested"]) == set(order_f)
    return rows


# ------------------------------------------------------------------------------------------------ Figure 2B slice
def slice_rows(cm_all):
    cm = cm_all[(cm_all.set == "primary") & (cm_all.W == SLICE["W"]) & (cm_all.alpha == SLICE["alpha"]) &
                (cm_all.gamma == SLICE["gamma"]) & (cm_all.phi == SLICE["phi"])]
    rows = []
    for w, wo in (("SITE", "NV"), ("ORACLE", "ORACLE-C")):
        d = contrast(cm, w, wo).reset_index().sort_values(["P", "K"])
        assert len(d) == 12 and set(d.K) == {1, 2, 5, 15} and set(d.P) == {0, 5, 30}, (w, len(d))
        for r in d.itertuples(index=False):
            rows.append(dict(pair=f"{lab(w)} vs {lab(wo)}", with_arm=lab(w), without_arm=lab(wo), cell=int(r.cell),
                             K=int(r.K), P=int(r.P), W=int(r.W), alpha=float(r.alpha), gamma=float(r.gamma),
                             phi=float(r.phi), abs_bias_with=float(r.abs_bias_with),
                             abs_bias_without=float(r.abs_bias_without), mean_truth=float(r.mean_truth),
                             D_without_minus_with=float(r.D),
                             p2_family_cell=bool(int(r.K) == 1 and int(r.P) == 0),
                             source="cell_metrics.csv (set primary; arms with/without); formula make_figures.py "
                                    "contrast (step7_prep c938a56)"))
    return rows


# ------------------------------------------------------------------------------------------------------ Figure 3
def ba_rows(checks, bm):
    rows = []
    for key in ("P", "S", "REF"):
        for s_name, field in (("278", "E3_site_278"), ("158", "E3_site_primary")):
            e = checks[key][field]
            for probe in ("linear", "mlp"):
                q = e[probe]
                rows.append(dict(block="E3-site (step 5)", role="protocol check", key=key, rep=KEY_LABEL[key],
                                 set=s_name, probe=probe, ba=q["ba"], lo_2p5=q["lo_2p5"], hi_97p5=q["hi_97p5"],
                                 upper_one_sided_95=q["upper_one_sided_95"], n_cases=q["n_cases"],
                                 exceeds_0p35=bool(q["upper_one_sided_95"] > 0.35),
                                 source=f"checks.json[{key}][{field}][{probe}]"))
    names = {"a": "B transport", "b": "B within-set refit"}
    for r in (pd.Series(x) for x in bm.to_dict("records")):
        rows.append(dict(block=names[r.analysis], role="exploratory", key=r.key, rep=KEY_LABEL[r.key], set=r.set,
                         probe=r.probe, ba=float(r.ba), lo_2p5=float(r.lo_2p5), hi_97p5=float(r.hi_97p5),
                         upper_one_sided_95=float(r.upper_one_sided_95), n_cases=int(r.cases),
                         exceeds_0p35=bool(r["exceeds_boundary_0.35"]),
                         source=f"b_main.csv[key={r.key} analysis={r.analysis} probe={r.probe} set={r.set}]"))
    # C-B0: B (a)/(b) on S1 and (b) on S3 reproduce step 5 (B_REPORT.md control); asserted here as well
    for key in ("P", "S", "REF"):
        for probe in ("linear", "mlp"):
            e278 = checks[key]["E3_site_278"][probe]
            e158 = checks[key]["E3_site_primary"][probe]
            for an, st, ref in (("a", "S1", e278), ("b", "S1", e278), ("b", "S3", e158)):
                m = bm[(bm.key == key) & (bm.analysis == an) & (bm.probe == probe) & (bm.set == st)].iloc[0]
                for f in ("ba", "lo_2p5", "hi_97p5", "upper_one_sided_95"):
                    assert m[f] == ref[f], (key, probe, an, st, f)
    return rows


# ------------------------------------------------------------------------------------------------------ Figure 4
FIG4_COMPARISONS = (("X1", "minusC"), ("X1", "FM"), ("X2", "minusC"))   # task §5 Figure 4


def x_rows(xc, xg):
    rows = []
    for a, comp in FIG4_COMPARISONS:
        for arm in ("FM-P-C", "FM-S-C", "REF-C"):
            sub = xc[(xc.analysis == a) & (xc.comparison == comp) & (xc.arm == arm)]
            for g in ("P1b-FM", "P2-FM"):
                gs = sub[sub.groups.str.split(",").apply(lambda L: g in L)].sort_values("cell")
                grp = xg[(xg.analysis == a) & (xg.comparison == comp) & (xg.arm == arm) & (xg.group == g)].iloc[0]
                assert len(gs) == grp.n_cells, (a, comp, arm, g)
                assert close(float(gs.delta.mean()), float(grp.mean_delta), 1e-12), (a, comp, arm, g)
                assert int((gs.delta < 0).sum()) == int(grp.n_cells_delta_negative)
                for i, r in enumerate(gs.itertuples(index=False)):
                    assert r.delta_lo <= r.delta <= r.delta_hi, (a, comp, arm, r.cell)
                    rows.append(dict(analysis=a, comparison=comp, arm=lab(arm), comparator=r.comparator.replace(
                        "step6 ", "step-6 ").replace("-C", "−C"), group=g, order_in_group=i + 1, cell=int(r.cell),
                        K=int(r.K), P=int(r.P), W=int(r.W), alpha=float(r.alpha), gamma=float(r.gamma),
                        M=int(r.M), delta=float(r.delta), delta_lo=float(r.delta_lo), delta_hi=float(r.delta_hi),
                        group_mean_delta=float(grp.mean_delta), group_mean_lo=float(grp.mean_delta_lo),
                        group_mean_hi=float(grp.mean_delta_hi), source=f"x_comparisons_cells.csv[{r.seed_name}]"))
    return rows


# ------------------------------------------------------------------------------------------------ Tables 1 and 3
def protocol_arms(proto):
    sec = proto.split("## 8. Adjustment arms", 1)[1].split("## 9.", 1)[0]
    rows = []
    for line in sec.splitlines():
        m = re.match(r"^\| (.+?) \| (.+?) \|$", line)
        if m and m.group(1) not in ("arm", "---"):
            clean = [re.sub(r"\*\*|\[v0\.4\] ?", "", g).strip() for g in (m.group(1), m.group(2))]
            rows.append(tuple(clean))
    return rows


def table1(t1, t2, proto, cm_all):
    sets = []
    run = {s: (int(g.cell.nunique()), sorted(g.arm.unique())) for s, g in cm_all.groupby("set")}
    key = {"primary causal set": "primary", "per-W set W = 0": "W0", "per-W set W = 5": "W5",
           "single-file set": "single_file"}
    for r in t1.itertuples(index=False):
        s = key.get(r.set)
        sets.append(dict(set=r.set, cases=int(r.cases), centres_2_3_4_5=r.centres_2_3_4_5,
                         definition=r.definition.replace("Center3_020", "one case"),
                         source=r.source, design_cells=run[s][0] if s else "", arms_run=len(run[s][1]) if s else "",
                         arms=" ".join(lab(a) for a in run[s][1]) if s else ""))
    models = [{k: getattr(r, k) for k in t2.columns} for r in t2.itertuples(index=False)]
    arms = [dict(arm=a, adjustment_set=b) for a, b in protocol_arms(proto)]
    return dict(sets=sets, models=models, arms=arms)


def table3(checks, x1):
    def ci(e, lo="lo_2p5", hi="hi_97p5", est="ba"):
        return dict(est=e[est], lo=e[lo], hi=e[hi])
    out = []
    for key in ("P", "S", "REF", "P-nat"):
        c = checks[key]
        rec = dict(key=key, rep=KEY_LABEL[key])
        for s, f in (("278", "E1_278"), ("158", "E1_primary"), ("123", "E1_single_file")):
            rec[f"E1_linear_{s}"] = dict(**ci(c[f]), upper=c[f]["upper_one_sided_95"], passed=c[f]["pass"])
            rec[f"E1_mlp_{s}"] = dict(**ci(c[f.replace("E1_", "E1_MLP_")]), reporting_only=True)
        for s, f in (("158", "E2_primary"), ("123", "E2_single_file")):
            rec[f"E2_{s}"] = dict(**ci(c[f], "ci_lo", "ci_hi", "delta_auc"), met=c[f]["pass"])
            fa = f + "_after_removal"
            rec[f"E2_after_{s}"] = (dict(**ci(c[fa], "ci_lo", "ci_hi", "delta_auc"), met=c[fa]["pass"])
                                    if fa in c else None)
        for f in ("E2_278", "E2_278_normtime", "E2_primary_normtime", "E2_single_file_normtime",
                  "E2_primary_history"):
            rec[f] = dict(**ci(c[f], "ci_lo", "ci_hi", "delta_auc"), reporting_only=True)
        for s, f in (("278", "E3_site_278"), ("158", "E3_site_primary"), ("123", "E3_site_single_file")):
            if f in c:
                for probe in ("linear", "mlp"):
                    q = c[f][probe]
                    rec[f"E3site_{probe}_{s}"] = dict(**ci(q), upper=q["upper_one_sided_95"],
                                                       passed=(c[f]["pass"] if probe == "linear" else None),
                                                       exceeds_0p35=bool(q["upper_one_sided_95"] > 0.35))
            else:
                rec[f"E3site_linear_{s}"] = rec[f"E3site_mlp_{s}"] = None
        for s, f in (("158", "E3_state_primary"), ("123", "E3_state_single_file")):
            rec[f"E3state_{s}"] = c.get(f)
        if key in x1:
            x = x1[key]
            for probe in ("linear", "mlp"):
                q = x["E3_site_primary_X1"][probe]
                rec[f"X1_E3site_{probe}_158"] = dict(**ci(q), upper=q["upper_one_sided_95"],
                                                     exceeds_0p35=bool(q["upper_one_sided_95"] > 0.35))
            e = x["E2_primary_after_removal_X1"]
            rec["X1_E2_after_158"] = dict(**ci(e, "ci_lo", "ci_hi", "delta_auc"), met=e["pass"])
            rec["X1_E3state_158"] = x["E3_state_primary_X1"]
            # x1_e3.json carries its own copy of the step-5 E3 reference: must equal checks.json
            assert x["step5_reference"]["E3_site_primary"] == c["E3_site_primary"], key
            assert x["step5_reference"]["E2_primary_pass"] == c["E2_primary"]["pass"], key
        out.append(rec)
    return out


# ---------------------------------------------------------------------------------------- schematic numbers
def schematic_values(t1, proto, run6, fact, decisions, keyc):
    def find(pat, text, cast=str):
        m = re.search(pat, text)
        assert m, pat
        return cast(m.group(1))

    sets = {r.set: dict(cases=int(r.cases), centres=r.centres_2_3_4_5) for r in t1.itertuples(index=False)}
    centres_278 = find(r"278 full-length cases \(centres 2–5: ([0-9/]+)\)", fact)
    grid = find(r"\* K ∈ \{([^}]*)\}; P ∈", proto)
    v = dict(
        n_representation=sets["representation set (E1, E3-site, PCA / LEACE)"]["cases"],
        centres_representation=centres_278.replace("/", " / "),
        n_primary=sets["primary causal set"]["cases"], centres_primary=sets["primary causal set"]["centres"],
        n_W0=sets["per-W set W = 0"]["cases"], centres_W0=sets["per-W set W = 0"]["centres"],
        n_W5=sets["per-W set W = 5"]["cases"], centres_W5=sets["per-W set W = 5"]["centres"],
        n_single=sets["single-file set"]["cases"], centres_single=sets["single-file set"]["centres"],
        n_excluded=sets["excluded from the primary set"]["cases"],
        centres_excluded=sets["excluded from the primary set"]["centres"],
        delta=find(r"d\(a\) = δ·a, δ = ([0-9.]+)", proto),
        step_seconds=find(r"\*\*Step:\*\* ([0-9]+) s of physical time", proto),
        K=grid, P=find(r"P ∈ \{([^}]*)\}; W", proto), W=find(r"W ∈ \{([^}]*)\}; α", proto),
        alpha=find(r"α ∈ \{([^}]*)\}; γ", proto), gamma=find(r"γ ∈ \{([^}]*)\}\. That is", proto),
        n_cells_main=find(r"That is ([0-9]+) cells", proto),
        phi_cells=find(r"\(([0-9]+) cells\)\.\n", proto),
        M=find(r"M = ([0-9]+) synthetic replicates per cell", proto),
        offsets=find(r"O_i ∈ \{([^}]*)\}", proto),
        n_pcs=find(r"reduced to ([0-9]+) principal components", proto),
        folds=find(r"case-level ([0-9]+)-fold", proto),
        step6_units=f"{run6['run_plan']['n_units']:,}",
        protocol_frozen=find(r"Protocol frozen: [0-9a-f]+ \(([0-9-]+) ", fact),
        x_plan_date=find(r"Plan b6d1cf7 \(([0-9-]+) ", fact), x_osf=find(r"OSF (https://osf.io/5c627)", fact),
        b_plan_date=find(r"Plan e1c27b4 \(([0-9-]+) ", fact), b_osf=find(r"OSF (https://osf.io/g9ymw)", fact),
        step6_completed=find(r"Step 6 completed ([0-9-]+) ", fact),
        x_records_date=find(r"records 1c8e628 \(([0-9-]+) ", fact),
        b_records_date=find(r"records 458341f \(([0-9-]+) ", fact),
        slice=find(r"slice (W = 30, α = 0\.5, γ = 1, φ_A = 0), primary set", decisions),
        code_lock_date=find(r"\| final code lock \(§14 step 2\) \| `98cba1e[0-9a-f]*` \| ([0-9-]+) ", keyc),
        step4_record_date=find(r"\| step-4 record \| `8d4c61a[0-9a-f]*` \| ([0-9-]+) ", keyc),
        step5_record_date=find(r"\| step-5 record \(chain\) \| `0ebf2cf[0-9a-f]*` \| ([0-9-]+) ", keyc),
        step6_launch_date=find(r"\| step-6 runner \(chain; step-6 launch\) \| `7adaf13[0-9a-f]*` \| ([0-9-]+) ", keyc),
        step7_record_date=find(r"\| step-7 record \| `2880d73[0-9a-f]*` \| ([0-9-]+) ", keyc),
    )
    assert v["delta"] == "1.05" and v["step_seconds"] == "5" and v["M"] == "200" and v["n_cells_main"] == "216"
    assert v["n_representation"] == 278 and v["n_primary"] == 158
    return v


def main():
    OUT.mkdir(exist_ok=True)
    guard = guard_inputs()
    fams = json.loads((PKG / INPUTS["families"][0]).read_text())
    cm_all = pd.read_csv(PKG / INPUTS["cell_metrics"][0])
    checks = json.loads((PKG / INPUTS["checks5"][0]).read_text())
    sec13 = json.loads((PKG / INPUTS["section13"][0]).read_text())
    gsite = json.loads((PKG / INPUTS["gsite"][0]).read_text())
    x1 = json.loads((PKG / INPUTS["x1_e3"][0]).read_text())
    xc = pd.read_csv(PKG / INPUTS["x_cells"][0])
    xg = pd.read_csv(PKG / INPUTS["x_groups"][0])
    bm = pd.read_csv(PKG / INPUTS["b_main"][0])
    t1 = pd.read_csv(PKG / INPUTS["table1_sets"][0])
    t2 = pd.read_csv(PKG / INPUTS["table2_models"][0])
    proto = (PKG / INPUTS["protocol"][0]).read_text()
    fact = (PKG / INPUTS["fact_base"][0]).read_text()
    decisions = (PKG / INPUTS["presentation_decisions"][0]).read_text()
    run6 = json.loads((PKG / INPUTS["step6_run_record"][0]).read_text())
    keyc = (PKG / INPUTS["key_commits"][0]).read_text()
    pf = protocol_families(proto)
    assert set(pf) == {"P1a", "P1b-SITE", "P1b-FM", "P2-SITE", "P2-FM", "P2-ORACLE", "P3"}, sorted(pf)

    # anchors (task §2.1)
    assert fams["primary:P1b-SITE"]["D_bar"] == ANCHORS["primary:P1b-SITE D_bar"]
    assert fams["primary:P2-SITE"]["D_bar"] == ANCHORS["primary:P2-SITE D_bar"]
    g = xg[(xg.analysis == "X1") & (xg.arm == "FM-P-C") & (xg.comparator == "step6 FM-P") & (xg.group == "P1b-FM")]
    assert len(g) == 1 and float(g.mean_delta.iloc[0]) == ANCHORS["X1 FM-P-C vs step6 FM-P, P1b-FM, mean delta"]

    n_checked, worst = validate_families(fams, cm_all)

    fam = family_rows(fams, gsite, sec13, pf)
    write("fam_dbar", dict(description="Family D̄ with 95 % percentile bootstrap interval (2,000 resamples of the "
                                       "200 replicates within each cell, same indices for both arms and the truth; "
                                       "cells fixed; seed 20261008), all sets of families.json",
                           rows=fam), fam)

    sl = slice_rows(cm_all)
    # the P2 cell of the slice equals families.json D_j (P2 orientation = −D_without_minus_with)
    for r in sl:
        if r["p2_family_cell"]:
            fk = "primary:P2-SITE" if r["with_arm"] == "SITE" else "primary:P2-ORACLE"
            assert close(-r["D_without_minus_with"], fams[fk]["D_cells"][str(r["cell"])], 1e-9), r
    write("fig2B_slice_D", dict(description="Per-cell D = (|bias| without C − |bias| with C) / mean truth at the "
                                            "main-text slice (W = 30, α = 0.5, γ = 1, φ_A = 0, primary set); "
                                            "point values; no per-cell interval exists for step 6",
                                slice=SLICE, rows=sl), sl)

    ba = ba_rows(checks, bm)
    write("fig3_ba", dict(description="Case-level site balanced accuracy after linear site removal: estimate, 95 % "
                                      "percentile interval and one-sided 95 % upper bound (case bootstrap stratified "
                                      "by site, 2,000 resamples, seed 20261008)", rows=ba), ba)

    xr = x_rows(xc, xg)
    write("fig4_x_cells", dict(description="Exploratory X1/X2 per-cell Δ = (|bias| X arm − |bias| step-6 arm) / "
                                           "mean truth with 95 % paired percentile bootstrap interval (2,000 "
                                           "resamples of replicates within the cell; cells fixed)", rows=xr), xr)

    write("table1", table1(t1, t2, proto, cm_all))
    write("table3", dict(rows=table3(checks, x1)))
    sv = schematic_values(t1, proto, run6, fact, decisions, keyc)
    write("schematic_values", sv)

    ga = {f: next(r for r in fam if r["set"] == "primary" and r["family"] == f)
          for f in ("P1a", "P1b-SITE", "P2-SITE", "P2-ORACLE")}
    write("ga_values", {f: dict(D_bar=r["D_bar"], ci_lo=r["ci_lo"], ci_hi=r["ci_hi"], n_cells=r["n_cells"],
                                D_bar_3dp=r["D_bar_3dp"], ci_3dp=r["ci_3dp"], reported=r["reported"])
                        for f, r in ga.items()})
    write("gsite", dict(primary=gsite["sets"]["primary"]["eta2_S_window_start"],
                        W0=gsite["sets"]["W0"]["eta2_S_window_start"],
                        W5=gsite["sets"]["W5"]["eta2_S_window_start"], gate="≤ 0.01",
                        source="gsite_record.json sets.<set>.eta2_S_window_start"))

    write("inputs_sha256", guard)
    write("validation", dict(
        anchors={k: dict(value=v, status="PASS") for k, v in ANCHORS.items()},
        families_D_cells_reproduced=n_checked, families_D_cells_max_abs_diff=worst,
        family_rows=len(fam), fig2A_points=sum(r["in_fig2A"] for r in fam), fig2B_rows=len(sl),
        fig3_rows=len(ba), fig4_rows=len(xr), x_group_means_reproduced=len(FIG4_COMPARISONS) * 3 * 2,
        c_b0_identity="PASS (B S1 (a)(b) and S3 (b) equal step-5 E3_site_278 / E3_site_primary)",
        x1_step5_reference="PASS (x1_e3.json step5_reference equals checks.json E3_site_primary)"))

    files = sorted(p for p in OUT.iterdir() if p.suffix in (".json", ".csv"))
    (OUT / "SHA256SUMS.txt").write_text("".join(f"{sha256(p)}  {p.name}\n" for p in files))
    print(f"inputs guarded: {len(guard)}; anchors: 3/3 PASS; family D_j reproduced: {n_checked} (max |diff| "
          f"{worst:.2e}); rows: fam {len(fam)} (fig2A {sum(r['in_fig2A'] for r in fam)}), slice {len(sl)}, "
          f"ba {len(ba)}, x {len(xr)}; files: {len(files)}")


if __name__ == "__main__":
    main()
