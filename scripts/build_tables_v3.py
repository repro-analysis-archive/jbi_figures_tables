#!/usr/bin/env python3
"""v4 revision table (task v4 §1.3): Table_2_v3 = Table_2_v2 with (a) the column "Direction rule" renamed "Locked rule
outcome" and a footnote that it is the mechanical outcome of the §12.3 aggregation, which the Status column qualifies,
and (b) the one bound whose 3-decimal string is "−0.000" shown with the decimals needed to display its sign (the
exact value and its display are frozen in canonical/validation.json → v4_table2_sign_decimals by freeze.py) and a
footnote saying so. Every other cell, rounding, rule, width and footnote as Table_2_v2 (build_tables_v2.py).

    .venv/bin/python -I scripts/build_tables_v3.py
"""
import sys

sys.dont_write_bytecode = True

import importlib.util  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build_tables_v2", HERE / "build_tables_v2.py")
b2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b2)
bt, OUT = b2.bt, b2.OUT


def table2_v3():
    F = bt.canonical("fam_dbar")["rows"]
    gs = bt.canonical("gsite")
    extra = bt.canonical("validation")["v4_table2_sign_decimals"]
    assert len(extra) == 1, "task v4 names one bound shown as −0.000"
    ex = extra[0]
    doc = b2.page(bt.new_document(landscape=True))
    bt.caption(doc, 2, "Family verdicts in the primary set (protocol §12.3) and the same families in the sensitivity "
                       "sets (§10.3).")
    hdr = ["Family", "Comparison (with vs without C)", "Cells", "Mean D (95% CI)", "Share D_j > 0",
           "Locked rule outcome{sup:a}", "Failed (§13)", "Status"]
    order = [("primary", "Primary set, 158 cases (enters family verdicts)"),
             ("W0", "W = 0 set, 204 cases (sensitivity; reported separately)"),
             ("W5", "W = 5 set, 201 cases (sensitivity; reported separately)"),
             ("single_file", "Single-file set, 123 cases (sensitivity; reported separately)")]
    rows, spans, shown = [], [], 0
    for s, label in order:
        sub = [r for r in F if r["set"] == s and not r["role"].startswith("exploratory")]
        spans.append(len(rows)); rows.append([label] + [""] * 7)
        for r in sub:
            ci = r["ci_3dp"]
            if r["source"] == f"families.json['{ex['row']}']":
                assert ex["field"] == "ci_lo" and r["ci_lo"] == ex["value"] and bt.f3(r["ci_lo"]) == ex["display_3dp"]
                assert ci.startswith(ex["display_3dp"] + " to ")
                ci = ex["display"] + "{sup:b}" + ci[len(ex["display_3dp"]):]
                shown += 1
            assert not re.search(r"−0\.000(?!\d)", ci + " " + r["D_bar_3dp"]), r["source"]   # no sign-hiding rounding left
            rows.append([r["family"], r["comparison"], str(r["n_cells"]), f"{r['D_bar_3dp']} ({ci})",
                         r["share_2dp"], r["rule_verdict"].capitalize(),
                         "None" if r["conditions_failed"] == "none" else r["conditions_failed"], bt.status(r)])
    assert len(rows) - len(spans) == 18 and shown == 1
    excluded = [r for r in F if r["role"].startswith("exploratory")]
    bt.add_table(doc, hdr, rows, [26, 47, 15, 48, 21, 26, 24, 40],
                 align=["l", "l", "r", "l", "r", "l", "l", "l"], spans=spans, span_space_pt=2)
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
        "{sup:a}Mechanical outcome of the §12.3 aggregation in every row, qualified by the Status column (not tested; "
        "reported separately). Direction rule (§12.3): supported if lower bound > 0 and D_j > 0 in ≥ 75% of cells; "
        "contradicted if upper bound < 0 or D_j > 0 in ≤ 25%; otherwise inconclusive. Only the primary set yields verdicts "
        "(consistent with the theory-motivated direction); families failing §13 (E3-site failed on the 158-case set; "
        "Supplementary Table S5) are not tested; sensitivity sets never enter verdicts.",
        f"{{sup:b}}Lower bound shown with {ex['decimals']} decimals so that its sign is visible (3 decimals would display "
        f"{ex['display_3dp']}); all other values have 3 decimals.",
        "Cells (§12.2): " + "; ".join(f"{' and '.join(v)}, {k}" for k, v in defs.items()) + f". G-SITE (≤ 0.01): "
        f"primary {gs['primary']:.4f}, W = 0 {gs['W0']:.4f}, W = 5 {gs['W5']:.4f}; none for the single-file set. The "
        "W = 0 set's P1a (" + ", ".join(f"{r['n_cells']} cells" for r in excluded) + "; outside §10.3; exploratory) "
        "is not shown.",
        "C, site; NV, no video; ORACLE, exact content state and C; ORACLE−C, state without C; FM-P, primary "
        "representation; FM-P−C, FM-P after linear site removal.",
    ])
    doc.save(OUT / "Table_2_v3.docx")
    bt.write_csv(OUT / "Table_2_v3.csv", hdr, rows, spans)
    return len(rows)


def main():
    n = table2_v3()
    print(f"Table_2_v3: {n} rows")


if __name__ == "__main__":
    main()
