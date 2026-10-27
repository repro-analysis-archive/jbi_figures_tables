#!/usr/bin/env python3
"""Write SOURCE_MAP.md, SUPPLEMENT_INDEX.md, qa/MEASUREMENT_REPORT.md and README.md from the canonical files, the
package manifest and the QA outputs (hashes are computed, never typed).

    .venv/bin/python -I scripts/make_docs.py
"""
import sys

sys.dont_write_bytecode = True

import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PKG = Path("/Volumes/ADDATA/医療動画/SS_DS203_manuscript_20261020")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def manifest():
    out = {}
    for line in (PKG / "MANIFEST_SHA256.txt").read_text().splitlines():
        h, p = line.split(None, 1)
        out[p[2:]] = h
    return out


def j(p):
    return json.loads((ROOT / p).read_text())


# ------------------------------------------------------------------------------------------------ SOURCE_MAP.md
def source_map():
    inp = j("canonical/inputs_sha256.json")
    sums = dict(reversed(line.split()) for line in (ROOT / "canonical/SHA256SUMS.txt").read_text().splitlines())
    val = j("canonical/validation.json")
    L = ["# Source map — JBI figures and tables", "",
         "Every plotted or tabulated value comes from a canonical file in `canonical/`, written by `scripts/freeze.py` "
         "from the read-only package `" + str(PKG) + "`. Each input is checked against the package manifest and, where "
         "the generating step recorded one, against that recorded hash; the MATLAB, Node and table builders re-check "
         "the canonical SHA-256 before reading.", "",
         "## Package inputs", "", "| name | package path | SHA-256 | recorded by the generating step |",
         "|---|---|---|---|"]
    for k, v in inp.items():
        L.append(f"| {k} | `{v['path']}` | `{v['sha256']}` | {v['recorded_by_generating_step']} |")
    L += ["", "## Canonical files", "", "| file | SHA-256 |", "|---|---|"]
    L += [f"| `canonical/{k}` | `{v}` |" for k, v in sorted(sums.items())]
    L += ["", "## Anchors and validations (`canonical/validation.json`)", ""]
    for k, v in val["anchors"].items():
        L.append(f"* {k} = {v['value']!r}: {v['status']}")
    L += [f"* families.json D_j reproduced from cell_metrics.csv with the committed `contrast` formula: "
          f"{val['families_D_cells_reproduced']} values, max |difference| {val['families_D_cells_max_abs_diff']}",
          f"* X group means reproduced from the per-cell Δ: {val['x_group_means_reproduced']} groups",
          f"* {val['c_b0_identity']}", f"* {val['x1_step5_reference']}", ""]
    L += ["## Map per element", "",
          "| element | cell group | canonical file → field | package source → field |", "|---|---|---|---|",
          "| Figure 1 (A) | cases, centre counts | `schematic_values.json` → n_*, centres_* | `03_results/RESULTS_20261019/figures/table1_data_sets.csv` → cases, centres_2_3_4_5; centres of the 278-case set from the fact base §2 |",
          "| Figure 1 (B) | δ, step length, grid, offsets, cells, M | `schematic_values.json` → delta, step_seconds, K, P, W, alpha, gamma, n_cells_main, phi_cells, M, offsets | protocol §2, §7.1, §7.2, §10.1, §10.2 (regex extraction, asserted) |",
          "| Figure 1 (C) | arms and covariates | `table1.json` → arms (names asserted against protocol §8) | protocol §8 |",
          "| Figure 1 (D) | folds, PCs, model names | `schematic_values.json` → folds, n_pcs; `table1.json` → models | protocol §2, §4.2; `table2_models.csv` |",
          "| Figure 1 (E) | dates, units, OSF | `schematic_values.json` → protocol_frozen, code_lock_date, step5_record_date, step6_units, step6_completed, step7_record_date, x_plan_date, x_osf, b_plan_date, b_osf | fact base §3, §7–9; `07_provenance/main_repository_key_commits.md`; `results/step6/run_record.json` → run_plan.n_units |",
          "| Figure 2 (A) | 11 family × set points | `fam_dbar.json` rows with in_fig2A → D_bar, ci_lo, ci_hi | `families.json` → `<set>:<family>`.D_bar, ci_lo, ci_hi (anchors P1b-SITE, P2-SITE) |",
          "| Figure 2 (B) | 24 per-cell D | `fig2B_slice_D.json` → D_without_minus_with (K, P) | `cell_metrics.csv` (set primary, W 30, alpha 0.5, gamma 1, phi 0; arms SITE/NV, ORACLE/ORACLE-C) → abs_bias, mean_truth; formula `make_figures.py` `contrast` (step7_prep c938a56) |",
          "| Figure 3 (A) | 12 BA points | `fig3_ba.json` block E3-site (step 5) → ba, lo_2p5, hi_97p5, upper_one_sided_95 | `checks.json` → `<key>`.E3_site_278 / E3_site_primary.`<probe>` |",
          "| Figure 3 (B, C) | 36 BA points | `fig3_ba.json` blocks B transport / B within-set refit | `b_main.csv` → ba, lo_2p5, hi_97p5, upper_one_sided_95 (key, analysis, probe, set) |",
          "| Figure 4 | 540 per-cell Δ | `fig4_x_cells.json` → delta, delta_lo, delta_hi | `x_comparisons_cells.csv` (analysis X1/X2; comparison minusC/FM; arm; groups) → delta, delta_lo, delta_hi; anchor X1 FM-P−C vs FM-P P1b-FM mean 0.5609627059097283 (`x_comparisons_groups.csv`) |",
          "| Table 1 (A) | sets | `table1.json` → sets (cases, centres, definition, design_cells, arms_run) | `table1_data_sets.csv`; design cells / arms counted from `cell_metrics.csv` |",
          "| Table 1 (B) | models | `table1.json` → models | `table2_models.csv` |",
          "| Table 1 (C) | arms | `table1.json` → arms | protocol §8 table |",
          "| Table 2 | 18 family × set rows | `fam_dbar.json` (role ≠ exploratory) → D_bar_3dp, ci_3dp, share_2dp, rule_verdict, conditions_failed, locked_verdict, tested | `families.json`; footnotes: protocol §12.2 (cells_definition, prediction), `gsite.json` ← `gsite_record.json` |",
          "| Table 3 | step-5 checks | `table3.json` → E1_*, E2_*, E3site_*, E3state_* per key | `checks.json` → `<key>`.<check> (ba / delta_auc, lo_2p5 / ci_lo, hi_97p5 / ci_hi, upper_one_sided_95, pass, retained_fraction) |",
          "| Table 3 | exploratory X1 | `table3.json` → X1_* | `x1_e3.json` → `<key>`.E3_site_primary_X1, E2_primary_after_removal_X1, E3_state_primary_X1 |",
          "| Graphical abstract | 2 numbers + counts | `ga_values.json` → P1b-SITE / P2-SITE D_bar_3dp; `schematic_values.json` → n_representation, n_primary | as Table 2 |",
          ""]
    L += ["## v3 revision (2026-10-27): map per element of the new numbering", "",
          "| element (v3) | file | canonical file → field | package source → field |", "|---|---|---|---|",
          "| Figure 1 | `figures_v2/Figure_1/Figure_1_v2.*` | `schematic_values.json` (n_*, centres_representation, centres_primary, delta, step_seconds, offsets, dates, OSF) and `table1.json` → arms | as v2 Figure 1 (A), (B), (C), (E) |",
          "| Figure 2 | `figures_v2/Figure_2/Figure_2_v2.*` | `fam_dbar.json` rows with in_fig2A → D_bar, ci_lo, ci_hi | `families.json` (as v2 Figure 2A) |",
          "| Figure 3 (new) | `figures_v2/Figure_3/Figure_3_v2.*` | `w_history_D.json` → D_without_minus_with (pair, W, K, P); anchors in `validation.json` → v3_history_anchors_exact | `cell_metrics.csv` (set primary, alpha 0.5, gamma 1, phi 0, W 0 / 5 / 30; arms SITE/NV, ORACLE/ORACLE-C) → abs_bias, mean_truth; formula `make_figures.py` `contrast`; 14 family cells checked against `families.json` |",
          "| Figure 4 | `figures_v2/Figure_4/Figure_4_v2.*` | `fig3_ba.json` (unchanged) | `checks.json`, `b_main.csv` (as v2 Figure 3) |",
          "| Figure 5 | `figures_v2/Figure_5/Figure_5_v2.*` | `fig4_x_cells.json` → delta, delta_lo, delta_hi (unchanged); display order `x_cells_order_v3.json` → order_v3 | `x_comparisons_cells.csv` (as v2 Figure 4) |",
          "| Table 1 | `tables/Table_1_v2.*` | `table1.json` → sets, models | `table1_data_sets.csv`, `table2_models.csv`, `cell_metrics.csv` |",
          "| Table 2 | `tables/Table_2_v2.*` | `fam_dbar.json` (18 rows), `gsite.json` | `families.json`, protocol §12.2, `gsite_record.json` |",
          "| Supplementary Table S5 | `tables/Table_S5_v2.*` | `table3.json` | `checks.json`, `x1_e3.json` (as v2 Table 3) |",
          "| Graphical abstract | `graphical_abstract/Graphical_abstract_v2.*` | `ga_values.json` → P1b-SITE / P2-SITE D_bar_3dp | as Table 2 |", ""]
    sd = val.get("v4_table2_sign_decimals", [])
    L += ["## v4 revision (2026-10-27): files of the current version", "",
          "Same canonical sources as the v3 revision; the only canonical change is the record "
          "`validation.json` → `v4_table2_sign_decimals` (no plotted or tabulated value changed).", "",
          "| element | current file | canonical file → field | note |", "|---|---|---|---|",
          "| Figure 1 | `figures_v3/Figure_1/Figure_1_v3.*` | as v3 (`schematic_values.json`, `table1.json`) | vertical spacing only |",
          "| Figure 2 | `figures_v3/Figure_2/Figure_2_v3.*` | as v3 (`fam_dbar.json` rows with in_fig2A) | markers only |",
          "| Figure 3 | `figures_v3/Figure_3/Figure_3_v3.*` | as v3 (`w_history_D.json`) | markers and row height only |",
          "| Figure 4 | `figures_v3/Figure_4/Figure_4_v3.*` | as v3 (`fig3_ba.json`) | markers only |",
          "| Figure 5 | `figures_v2/Figure_5/Figure_5_v2.*` (unchanged) | as v3 | not revised |",
          "| Table 1 | `tables/Table_1_v2.*` (unchanged) | as v3 | not revised |",
          "| Table 2 | `tables/Table_2_v3.*` | `fam_dbar.json` (18 rows), `gsite.json`; displayed bound "
          + "; ".join(f"{x['row']} {x['field']} = {x['value_repr']} → {x['display']} (`validation.json` → "
                      f"v4_table2_sign_decimals; `{x['source']}`)" for x in sd) + " | heading, footnotes a and b, one bound |",
          "| Supplementary Table S5 | `tables/Table_S5_v2.*` (unchanged) | as v3 | not revised |",
          "| Graphical abstract | `graphical_abstract/Graphical_abstract_v2.*` (unchanged) | as v3 | not revised |", ""]
    if "v5_bias_coverage_anchors_exact" in val:
        an = "; ".join(f"{k} = {v!r}" for k, v in val["v5_bias_coverage_anchors_exact"].items())
        L += ["## v5 revision (2026-10-27): current files in the order of first citation", "",
              "| element | current file | canonical file → field | package source → field |", "|---|---|---|---|",
              "| Figure 1 | `figures_v4/Figure_1/Figure_1_v4.*` (byte copy of `Figure_1_v3`) | `schematic_values.json`, `table1.json` | as v3 Figure 1 |",
              "| Figure 2 | `figures_v4/Figure_2/Figure_2_v4.*` (byte copy of `Figure_4_v3`) | `fig3_ba.json` → ba, lo_2p5, hi_97p5, upper_one_sided_95 | `checks.json`, `b_main.csv` |",
              "| Figure 3 | `figures_v4/Figure_3/Figure_3_v4.*` (byte copy of `Figure_2_v3`) | `fam_dbar.json` rows with in_fig2A → D_bar, ci_lo, ci_hi | `families.json` |",
              "| Figure 4 | `figures_v4/Figure_4/Figure_4_v4.*` (byte copy of `Figure_3_v3`) | `w_history_D.json` → D_without_minus_with | `cell_metrics.csv`, `contrast` formula |",
              "| Figure 5 (new) | `figures_v4/Figure_5/Figure_5_v4.*` | `fig5_bias_coverage.json` → rel_bias_pct (= 100 × rel_bias), coverage (arm, K, P); anchors in `validation.json` → v5_bias_coverage_anchors_exact (" + an + ") | `cell_metrics.csv` (set primary, W 30, alpha 0.5, gamma 1, phi 0; 12 arms) → rel_bias, coverage |",
              "| Figure 6 | `figures_v4/Figure_6/Figure_6_v4.*` (byte copy of `Figure_5_v2`; TIF from its PDF) | `fig4_x_cells.json`, `x_cells_order_v3.json` | `x_comparisons_cells.csv` |",
              "| Tables 1, 2, S5; graphical abstract | `tables/Table_1_v2.*`, `tables/Table_2_v3.*`, `tables/Table_S5_v2.*`, `graphical_abstract/Graphical_abstract_v2.*` (unchanged) | as v4 revision | as v4 revision |",
              "", "Byte identity of the renumbered files with their sources: `qa/renumber_v5.json`.", ""]
    if (ROOT / "canonical_supplement" / "SHA256SUMS.txt").exists():
        ss = dict(reversed(x.split()) for x in (ROOT / "canonical_supplement/SHA256SUMS.txt").read_text().splitlines())
        si = j("canonical_supplement/inputs_sha256.json")
        L += ["## v6 supplement (2026-10-27): sources of the supplementary figures and tables", "",
              "Written by `scripts/freeze_supplement.py` into `canonical_supplement/` (the main `canonical/` is read with "
              "its hash guard for the cross-checks and not written).", "",
              "| element | files | canonical file → field | package source → field |", "|---|---|---|---|",
              "| Figure S1 | `figures_supp_v1/Figure_S1/Figure_S1_v1.pdf`, `pages/` | `s1_contrast_D.json` → D, D_disp (pair, cell) | `cell_metrics.csv` (set primary) → abs_bias, mean_truth; formula `contrast`; all D_j of `families.json` reproduced |",
              "| Figures S2, S3 | `figures_supp_v1/Figure_S2/…`, `Figure_S3/…` | `s23_bias_coverage.json` → rel_bias_pct, rel_bias_disp; coverage, coverage_disp (arm, cell) | `cell_metrics.csv` (set primary) → rel_bias, coverage (= `report_cells.csv` within 1e-12) |",
              "| Figure S4 | `figures_supp_v1/Figure_S4/Figure_S4_v1.*` | `s4_mask_profiles.json` → rho, m (centre, point); visible_radius; r | `inputs/mask_check.json` (provided by the investigator; SHA-256 = SOURCES.md record of 8d4c61a) → profiles.<c>.rho, m; visible_radius; r; cross-checked with `tableS4_mask_check.csv` |",
              "| Supplementary Material | `supplementary/Supplementary_Material_v1.docx` | Tables S1–S6 docx, Figures S1–S6 images, `CAPTIONS_supplement_v1.md` | Methods: `inputs/JBI_Supplementary_Methods_draft_v2.md` (provided by the investigator) |",
              "| Figure S5 | `figures_supp_v1/Figure_S5/…` | `s5_x_cells.json` → delta, delta_lo, delta_hi, order (page, analysis, comparison, arm, group) | `x_comparisons_cells.csv` |",
              "| Figure S6 | `figures_supp_v1/Figure_S6/Figure_S6_v1.*` | `s6_b.json` → ba, lo_2p5, hi_97p5, upper_one_sided_95 | `b_main.csv` (= main `fig3_ba.json` B rows) |",
              "| Table S1 | `tables/Table_S1_v1.*` | `t_tableS4_mask_check.json` | `tableS4_mask_check.csv` |",
              "| Table S2 | `tables/Table_S2_v1.*` | main `table3.json` (as Table_S5_v2) | `checks.json`, `x1_e3.json` |",
              "| Table S3 | `tables/Table_S3_v1.*` | `t_tableX_group_summaries.json` | `tableX_group_summaries.csv` (= `x_comparisons_groups.csv`) |",
              "| Table S4 | `tables/Table_S4_v1.*` | `t_tableX_E3.json` | `tableX_E3.csv` |",
              "| Table S5 | `tables/Table_S5_v1.*` | `t_tableB_ba.json`, `t_tableB_judgements.json` | `tableB_ba.csv`, `tableB_judgements.csv` (= `b_judgements.csv`) |",
              "| Table S6 | `tables/Table_S6_v1.*` | `t_tableB_sens.json` | `tableB_sens.csv` (= `b_sensitivity_summary.csv`) |", "",
              "| canonical_supplement file | SHA-256 |", "|---|---|"] + \
             [f"| `canonical_supplement/{k}` | `{v}` |" for k, v in sorted(ss.items())] + \
             ["", "| package input | path | SHA-256 | recorded by the generating step |", "|---|---|---|---|"] + \
             [f"| {k} | `{v['path']}` | `{v['sha256']}` | {v['recorded_by_generating_step']} |" for k, v in si.items()] + [""]
    (ROOT / "SOURCE_MAP.md").write_text("\n".join(L) + "\n")


# ------------------------------------------------------------------------------------------------ SUPPLEMENT_INDEX
def supplement_index():
    man = manifest()
    items = [
        ("S1", "Contrast Δ|bias| / mean truth, all 240 primary cells, one page pair per with/without-C pair",
         "03_results/RESULTS_20261019/figures/figS1_contrast_all_cells.pdf", "step7_prep c938a56 make_figures.py (pre-result decision 2)"),
        ("S2", "Relative bias, all cells, one page pair per arm", "03_results/RESULTS_20261019/figures/figS2_rel_bias_all_cells.pdf", "as S1"),
        ("S3", "95% interval coverage, all cells, one page pair per arm", "03_results/RESULTS_20261019/figures/figS3_coverage_all_cells.pdf", "as S1"),
        ("S4 (figure)", "Mask check: per-centre radial profiles", "03_results/SUPPLEMENT_20261020/figS4_mask_profiles.pdf", "step7_prep make_supplement.py; source mask_check.json (8d4c61a)"),
        ("S4 (table)", "Mask check values", "03_results/SUPPLEMENT_20261020/tableS4_mask_check.csv", "as S4 figure; .md alongside"),
        ("X (table)", "Exploratory X1/X2 group summaries (54 rows)", "03_results/SUPPLEMENT_20261020/tableX_group_summaries.csv", "byte copy of x_comparisons_groups.csv (1c8e628)"),
        ("X-E3 (table)", "Exploratory X1 E3-site, E2, E3-state next to step 5", "03_results/SUPPLEMENT_20261020/tableX_E3.csv", "x1_e3.json (1c8e628), checks.json (0ebf2cf)"),
        ("X (figure)", "Exploratory X1/X2 per-cell Δ, all 71 cells, all comparators", "03_results/SUPPLEMENT_20261020/figX_cell_delta.pdf", "x_comparisons_cells.csv (1c8e628)"),
        ("B (table)", "Exploratory B balanced accuracy (36 rows)", "03_results/SUPPLEMENT_20261020/tableB_ba.csv", "byte copy of b_main.csv (458341f)"),
        ("B (judgements)", "Exploratory B judgement statements (36)", "03_results/SUPPLEMENT_20261020/tableB_judgements.csv", "byte copy of b_judgements.csv"),
        ("B-sens (table)", "Exploratory B equal-size subsampling (36 rows)", "03_results/SUPPLEMENT_20261020/tableB_sens.csv", "byte copy of b_sensitivity_summary.csv"),
        ("B (figure)", "Exploratory B BA by set", "03_results/SUPPLEMENT_20261020/figB_ba_by_set.pdf", "b_main.csv (458341f)"),
        ("Captions", "Captions of S4, X, X-E3, B, B-sens", "03_results/SUPPLEMENT_20261020/CAPTIONS.md", "fact base v5 §5, §8, §9"),
        ("Sources", "Commit, path and blob SHA-256 of every supplementary source", "03_results/SUPPLEMENT_20261020/SOURCES.md", "—"),
        ("Results report", "Family verdicts, §13 ceilings, pre-causal checks, PCA / LEACE, all per-cell relative bias and coverage", "03_results/RESULTS_20261019/REPORT.md", "step7_prep make_report.py; inputs hashed in its header"),
        ("Per-cell metrics", "All metrics per set, cell and arm (3,504 rows)", "03_results/RESULTS_20261019/report_cells.csv", "cell_metrics.csv (2880d73) + family labels"),
        ("Pre-result main figures", "Results-report Figures 1–4 drawn under the pre-result presentation decisions (bias / coverage vs K; role switch, five pairs; K × P heatmaps; checks)", "03_results/RESULTS_20261019/figures/fig1_bias_coverage_vs_K.pdf", "fig2_role_switch.pdf, fig3_contrast_KP.pdf, fig4_checks.pdf alongside"),
        ("X heatmaps", "Exploratory X heatmaps", "04_exploratory/X1_X2/results_X/X_heatmaps.pdf", "1c8e628"),
    ]
    L = ["# Supplement index", "",
         "Existing supplementary items in the read-only package (`" + str(PKG) + "`), with the SHA-256 from its "
         "manifest. Final supplementary numbering is left to the manuscript (the package keeps the labels S1–S4, X, "
         "X-E3, B and B-sens). X and B items are exploratory.", "",
         "| label | content | package path | SHA-256 | source |", "|---|---|---|---|---|"]
    for lab, what, path, src in items:
        L.append(f"| {lab} | {what} | `{path}` | `{man[path]}` | {src} |")
    s5 = ROOT / "tables" / "Table_S5_v2.docx"
    L.append(f"| S5 (table) | Representation diagnostics (former main Table 3; v3 revision) | work folder "
             f"`tables/Table_S5_v2.docx` (+ .csv, .pdf) | `{sha(s5)}` | `build_tables.py` table3 via `build_tables_v2.py` "
             "(canonical `table3.json` ← checks.json, x1_e3.json) |")
    L += ["", "v3 revision: the slice-only role-switch view of v2 Figure 2B is superseded by main Figure 3 (its W = 30 row; "
          "main Figure 4 after the v5 renumbering); Supplementary Figure S1 holds every other α, γ (and W, φ_A) cell of "
          "the contrast."]
    L += ["", "v5 revision: the pre-result main-text Figure 1 (relative bias and coverage against K at the slice, "
          "`fig1_bias_coverage_vs_K.pdf`) is reinstated as main Figure 5 (house style, same content); Supplementary "
          "Figures S2 and S3 hold relative bias and coverage for every other cell. Main figures in the current numbering: "
          "1 design, 2 erasure, 3 families, 4 prior action history, 5 bias / coverage, 6 exploratory X1/X2."]
    L += ["", "Not reproduced in the JBI main text and therefore candidates for the supplement: the pre-result "
          "main-text Figures 2–4 of the results report (role switch, K × P heatmaps, checks), the FM / REF pairs of the "
          "role-switch view at the slice, PCA / LEACE variance retained (results report §3), the slice group and the NV "
          "comparator of X (Supplementary Figure X / Table X)."]
    if (ROOT / "figures_supp_v1").exists():
        L += ["", "## v6: final supplementary numbering (house style; `CAPTIONS_supplement_v1.md`)", "",
              "| item | content | file(s) | former name | SHA-256 (PDF / docx) |", "|---|---|---|---|---|"]
        items = [("Figure S1", "All-cell heatmaps of D, one pair of pages per with/without-C pair (10 pages)", "figures_supp_v1/Figure_S1/Figure_S1_v1.pdf", "figS1"),
                 ("Figure S2", "All-cell heatmaps of relative bias, one pair of pages per arm (24 pages)", "figures_supp_v1/Figure_S2/Figure_S2_v1.pdf", "figS2"),
                 ("Figure S3", "All-cell heatmaps of 95% interval coverage, one pair of pages per arm (24 pages)", "figures_supp_v1/Figure_S3/Figure_S3_v1.pdf", "figS3"),
                 ("Figure S4", "Mask check: per-centre radial profiles", "figures_supp_v1/Figure_S4/Figure_S4_v1.pdf", "figS4"),
                 ("Figure S5", "Exploratory X1/X2 per-cell Δ not in main Figure 6 (4 pages)", "figures_supp_v1/Figure_S5/Figure_S5_v1.pdf", "figX"),
                 ("Figure S6", "Exploratory B balanced accuracy by evaluation set", "figures_supp_v1/Figure_S6/Figure_S6_v1.pdf", "figB"),
                 ("Table S1", "Mask check values", "tables/Table_S1_v1.docx", "tableS4"),
                 ("Table S2", "Representation diagnostics", "tables/Table_S2_v1.docx", "Table_S5_v2"),
                 ("Table S3", "Exploratory X1/X2 group summaries", "tables/Table_S3_v1.docx", "tableX_group_summaries"),
                 ("Table S4", "Exploratory X1 E3/E2 next to step 5", "tables/Table_S4_v1.docx", "tableX_E3"),
                 ("Table S5", "Exploratory B balanced accuracy and judgements", "tables/Table_S5_v1.docx", "tableB_ba + tableB_judgements"),
                 ("Table S6", "Exploratory B equal-size subsampling", "tables/Table_S6_v1.docx", "tableB_sens"),
                 ("Document", "Supplementary Material (Methods SM 1–7, Tables S1–S6, Figures S1–S6)",
                  "supplementary/Supplementary_Material_v1.docx", "—")]
        for lab, what, f, old_ in items:
            L.append(f"| {lab} | {what} | " + (f"`{f}`" if f else "—") + f" | {old_} | " + (f"`{sha(ROOT / f)}`" if f else "—") + " |")
        L += ["", "The package items above keep their package labels; the main text refers to the v6 numbers "
              "(\"Supplementary Table S5\" in the v3–v5 main records = Table S2)."]
    (ROOT / "SUPPLEMENT_INDEX.md").write_text("\n".join(L) + "\n")


# ------------------------------------------------------------------------------------------------ MEASUREMENT_REPORT
def measurement_report():
    figs = [("Figure_1", "figures/Figure_1"), ("Figure_2", "figures/Figure_2"), ("Figure_3", "figures/Figure_3"),
            ("Figure_4", "figures/Figure_4"), ("Graphical_abstract", "graphical_abstract")]
    pvc = j("qa/plotted_vs_canonical.json")
    tq = j("qa/tables_qa.json")
    sn = j("qa/schematic_numbers.json")
    L = ["# Measurement report (template §7; measured from the exported files)", "",
         "| figure | PDF page (mm) | TIF (px @ dpi = mm) | text sizes (pt) | min (pt) | fonts embedded | raster objects | text overlaps / near (< 0.5 mm) | edge clearance < 0.3 mm |",
         "|---|---|---|---|---|---|---|---|---|"]
    for name, d in figs:
        m = j(f"qa/measure_{name}.json")
        t = m.get("tif", {})
        fonts = "; ".join(" ".join(x.split()[:1]) + (" yes" if x.split()[-5] == "yes" else " NO") for x in m["pdffonts"][2:])
        L.append(f"| {name} | {m['page_mm'][0]} × {m['page_mm'][1]} | {t.get('px')} @ {t.get('dpi', [None])[0]} = "
                 f"{t.get('mm')} | {m['text_sizes_pt']} | {m['min_text_pt']} | {fonts} | "
                 f"{max(0, len(m['pdfimages']) - 2)} | {len(m['text_overlaps'])} | {len(m['edge_clearance_below_0p3mm'])} |")
    L += ["", "## Marker sizes (outer size including the edge line; from PDF paths)", "",
          "| figure | part | shape | colour | edge (pt) | n | outer w × h (mm, median) |", "|---|---|---|---|---|---|---|"]
    for name, _ in figs[1:4]:
        for mk in j(f"qa/measure_{name}.json")["markers"]:
            if mk["part"] == "edge":
                L.append(f"| {name} | {mk['part']} | {mk['shape']} | {mk['colour']} | {mk['edge_pt']} | {mk['n']} | "
                         f"{mk['outer_w_mm_median']} × {mk['outer_h_mm_median']} |")
    L += ["", "Filled markers (navy face, near-black edge): template target 0.95–1.15 mm; open / angular markers: "
          "1.10–1.30 mm; hard minimum 0.8 mm. 'other' groups MATLAB's square and diamond edge paths.", "",
          "## Plotted vs canonical (MATLAB, zero tolerance; `qa/plotted_vs_canonical.json`)", ""]
    for k, v in pvc.items():
        pts = v.get("points", (v.get("panelA_points", 0) + v.get("panelB_points", 0)))
        L.append(f"* {k}: {v['result']} — {pts} points with their intervals / bounds; mismatches {len(v['mismatches'])}; "
                 f"legend: {v.get('legend_entries', v.get('legend'))}")
    L += ["", "## Schematic numbers (`qa/schematic_numbers.json`)", ""]
    for k, v in sn.items():
        L.append(f"* {k}: {len(v)} distinct numeric tokens; canonical {sum(r['source'] == 'canonical' for r in v)}, "
                 f"structural {sum(r['source'].startswith('structural') for r in v)}, unmatched "
                 f"{sum(r['source'] == 'UNMATCHED' for r in v)}")
    L += ["", "## Tables (Word XML and LibreOffice PDF; `qa/tables_qa.json`)", "",
          "| table | pages (A4 landscape) | horizontal rules per page | vertical rules | shading | fonts | run sizes (pt) | checks |",
          "|---|---|---|---|---|---|---|---|"]
    for k, v in tq.items():
        p, d = v["pdf"], v["docx"]
        L.append(f"| {k} | {p['pages']} | {p['rules_per_page']} | {p['vertical_rules']} | {d['shading_elements']} + "
                 f"{p['filled_rects']} | {', '.join(x.split()[0] for x in p['pdffonts'])} | {d['run_sizes_pt']} | "
                 f"{'PASS' if all(v['checks'].values()) else 'FAIL'} ({len(v['checks'])}) |")
    L += ["", "PDF text at 6.4 pt in the tables = Word superscript / subscript runs (footnote markers, D_j, S_t) as "
          "rendered by LibreOffice (58 % of 11 pt); the runs themselves are 11 pt.", ""]
    L += ["## Scientific / semantic QA (template §7-4)", "",
          "| figure | n / denominator | interval (confirmed in code) | reference | scale | unit / direction | categories / N/A |",
          "|---|---|---|---|---|---|---|",
          "| Figure 1 | 278 / 158 / 204 / 201 / 123 cases and centre counts = Table 1 (A) | — | — | — | — | populations drawn as parallel branches (per-W eligibility), single-file nested in the primary set; arms = protocol §8 |",
          "| Figure 2 (A) | cells per family 66 / 48 / 18 / 12 (sets 16–48 / 4–6) = Table 2; lower ≤ estimate ≤ upper asserted | paired replicate bootstrap of the family mean, cells fixed (grid.py) | 0 (difference) | linear; facets free, equal width (caption) | dimensionless; P1 without − with, P2 with − without (axis labels, caption) | set order primary, W = 0, W = 5, single-file; absent combinations omitted with reason; W0:P1a (exploratory) not drawn |",
          "| Figure 2 (B) | 12 cells per pair = the pre-result slice | none exists (point values; caption) | 0 | log K axis (1, 2, 5, 15), linear D | dimensionless; without − with for all cells; P2 cell sign note | P = 0 / 5 / 30 by marker and line style |",
          "| Figure 3 | 278 / 158 cases (S1 278; S2, S3 158) = checks.json, b_main.csv | site-stratified case bootstrap percentile; upper = 95th percentile (checks.py) | 0.35 boundary (dashed), 0.25 chance (dotted) | linear 0.1–1.02, shared | BA; higher = more site-decodable | FM-P / FM-S / REF; linear navy (criterion), MLP gray; (A) protocol vs (B, C) exploratory in separate axes |",
          "| Figure 4 | 48 + 12 cells per panel, 540 in total | paired replicate bootstrap percentile per cell (x_compare.py) | 0 | linear; shared within a row, free between rows (caption) | dimensionless; negative = X arm smaller |bias| | groups P1b-FM, P2-FM in record cell order; all panels exploratory |",
          ""]
    L += return_block()
    (ROOT / "qa" / "MEASUREMENT_REPORT.md").write_text("\n".join(L) + "\n")


def return_block():
    """Template §12-3 paste-safe return block, filled from the measurement files."""
    m = {n: j(f"qa/measure_{n}.json") for n in ("Figure_1", "Figure_2", "Figure_3", "Figure_4", "Graphical_abstract")}
    pvc = j("qa/plotted_vs_canonical.json")
    blind = j("qa/blind_scan.json")
    reb = (ROOT / "qa" / "REBUILD_TEST.md").read_text()

    def mk(n):
        e = [x for x in m[n]["markers"] if x["part"] == "edge"]
        return ", ".join(f"{x['shape']} {x['outer_w_mm_median']}" for x in e)
    size = "   ".join(f"{n}: {m[n]['page_mm'][0]} × {m[n]['page_mm'][1]} mm" for n in m)
    blind_ok = all(not any(v["hits"].values()) for v in blind.values())
    return ["", "## Template §12-3 return block", "", "```",
            "[STYLE]        Arial; tick/axis/panel = 9/10/11 pt (schematics 8/9/11; GA 7–9); grayscale+navy #2B3D6B; label-case=(A)",
            "[METHOD]       Fig2:B Fig3:B Fig4:B (no reference .fig exists; make_FigN.m from canonical JSON)  Fig1, GA: §15 pptxgenjs",
            "[FILES]        Fig2–4: .fig + .m + .pdf + .tif(1200); Fig1, GA: .js + .pptx + .pdf + .tif(1200)",
            "[DATA_CHECK]   " + "  ".join(f"{k}:{v['result']}" for k, v in pvc.items()) + "   (hash guard y)",
            "[★ PROVENANCE] manifest 248/248, recorded hashes 10/10 match, anchors 3/3 = PASS",
            "[★ CI]          D̄: paired replicate bootstrap (grid.py); Δ: paired replicate bootstrap (x_compare.py); BA: site-stratified case bootstrap (checks.py) = PASS",
            "[★ LEGEND]      legend↔plot bidirectional invariant = PASS (legends built from plotted handles; asserted)",
            "[★ N/A]         missing set × family combinations omitted, caption states why; W0:P1a (exploratory) not drawn = PASS",
            "[CLASS]        Fig1:V Fig2:V Fig3:V Fig4:V GA:V",
            "[VECTOR]       pdffonts non-empty & Arial emb=yes y ; pdfimages empty (class V) y ; unexpected rasterization n",
            "[★ SCIENCE]    n/CI/reference/scale/unit/direction/category mapping = PASS (qa/MEASUREMENT_REPORT.md; captions)",
            "[★ REBUILD]    clean MATLAB session + canonical data + `.m` = " + ("PASS" if "Result: PASS" in reb else "FAIL"),
            "[★ SIZE]       " + size + "  (JBI full width 190 mm; GA 13 cm: y)",
            "[★ MARKER]     Fig2: " + mk("Figure_2") + " | Fig3: " + mk("Figure_3") + " | Fig4: " + mk("Figure_4") + " (mm; min 0.8)",
            "[★ TEXT]       figure-internal text moved to caption y (category labels and 'Exploratory' titles kept; see POST_RESULT_PRESENTATION_JBI.md §2)",
            "[★ BOX]        Fig2:off  Fig3:off  Fig4:off   (forest / dot plots; y)",
            "[★ MULTIPANEL] shared-axis attribution ok y ; facet physical width equal y (Fig2A facets 58.5 mm; Fig4 panels 54.5 mm)",
            "[★ UNCHANGED]  none after the final round; clean rebuild identical",
            "[★ SCHEMATIC]  numbers vs canonical y (qa/schematic_numbers.json) ; notation registry y ; palette/font y",
            f"[BLIND]        metadata clean y ; AI traces 0 hits {'y' if blind_ok else 'n'} ; email 0 hits {'y' if blind_ok else 'n'}",
            "[MAP]          reference→target confirmed y (no earlier JBI figures; numbering = task §5)", "```", ""]


def measurement_report_v2():
    figs = [("Figure_1_v2", "schematic"), ("Figure_2_v2", "data"), ("Figure_3_v2", "data"), ("Figure_4_v2", "data"),
            ("Figure_5_v2", "data"), ("Graphical_abstract_v2", "GA")]
    pvc = j("qa/plotted_vs_canonical_v2.json")
    tq = j("qa/tables_qa_v2.json")
    sn = j("qa/schematic_numbers_v2.json")
    blind = j("qa/blind_scan_v2.json")
    reb = (ROOT / "qa" / "REBUILD_TEST_v3.md").read_text()
    L = ["# Measurement report — v3 revision outputs (template §7; measured from the exported files)", "",
         "| figure | PDF page (mm) | TIF (px @ dpi = mm) | regular text (pt) | bold text (pt) | panel labels (pt) | min (pt) | fonts | raster objects | overlaps / near | edge < 0.3 mm |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    rows = {}
    for name, kind in figs:
        m = j(f"qa/measure_{name}.json")
        t = m.get("tif", {})
        reg = sorted({round(x["size"]) for x in m["spans"] if "Bold" not in x["font"]})
        bold = sorted({round(x["size"]) for x in m["spans"] if "Bold" in x["font"]})
        pan = sorted({round(x["size"]) for x in m["spans"] if "Bold" in x["font"] and re.fullmatch(r"\([A-F]\)", x["text"].strip())})
        fonts = ", ".join(sorted({x.split()[0].split("+")[-1] for x in m["pdffonts"][2:]}))
        rows[name] = dict(reg=reg, bold=bold, pan=pan, mm=m["page_mm"])
        L.append(f"| {name} | {m['page_mm'][0]} × {m['page_mm'][1]} | {t.get('px')} @ {t.get('dpi', [None])[0]} = {t.get('mm')} | "
                 f"{reg} | {bold} | {pan or '—'} | {m['min_text_pt']} | {fonts} (emb=yes) | {max(0, len(m['pdfimages']) - 2)} | "
                 f"{len(m['text_overlaps'])} | {len(m['edge_clearance_below_0p3mm'])} |")
    L += ["", "Data figures: tick labels and category labels 14 pt, axis labels 15 pt, panel labels 16 pt bold. Figure 1: body "
          "14 pt, headings 15 pt bold, panel labels 16 pt bold. Graphical abstract: body 10 pt, title 11 pt bold. No figure "
          "needed a size below the template values.", "",
          "## Marker sizes (outer, including the edge line; from PDF paths)", "",
          "| figure | shape | colour | edge (pt) | n | outer w × h (mm) |", "|---|---|---|---|---|---|"]
    for name, kind in figs:
        if kind != "data":
            continue
        for mk in j(f"qa/measure_{name}.json")["markers"]:
            if mk["part"] == "edge":
                L.append(f"| {name} | {mk['shape']} | {mk['colour']} | {mk['edge_pt']} | {mk['n']} | {mk['outer_w_mm_median']} × {mk['outer_h_mm_median']} |")
    L += ["", "## Plotted vs canonical and legend / key ↔ plot (`qa/plotted_vs_canonical_v2.json`)", ""]
    for k, v in pvc.items():
        extra = v.get("legend_entries", v.get("legend", ""))
        if "key_glyphs" in v:
            extra = "key: " + "; ".join(v["key_glyphs"])
        L.append(f"* {k}: {v['result']} — {v['points']} points with their intervals / bounds; mismatches {len(v['mismatches'])}; {extra}")
    L += ["", "## Schematic numbers (`qa/schematic_numbers_v2.json`)", ""]
    for k, v in sn.items():
        L.append(f"* {k}: {len(v)} distinct numeric tokens; canonical {sum(r['source'] == 'canonical' for r in v)}, "
                 f"structural {sum(r['source'].startswith('structural') for r in v)}, unmatched {sum(r['source'] == 'UNMATCHED' for r in v)}")
    L += ["", "## Tables (`qa/tables_qa_v2.json`)", "",
          "| table | pages | rules per page | vertical rules | shading | run sizes (pt) | paragraph styles | checks |", "|---|---|---|---|---|---|---|---|"]
    for k, v in tq.items():
        p, d = v["pdf"], v["docx"]
        L.append(f"| {k} | {p['pages']} | {p['rules_per_page']} | {p['vertical_rules']} | {d['shading_elements']} + {p['filled_rects']} | "
                 f"{d['run_sizes_pt']} | {d['paragraph_styles']} | {'PASS' if all(v['checks'].values()) else 'FAIL'} ({len(v['checks'])}) |")
    L += ["", "## Clean rebuild (`qa/REBUILD_TEST_v3.md`)", "", "Result: " + ("PASS" if "Result: PASS" in reb else "FAIL"),
          "", "## Template §12-3 return block (v3)", "", "```",
          "[STYLE]        Arial; tick/axis/panel = 14/15/16 pt (Figure 1 body/heading/panel 14/15/16; GA 10–11); grayscale+navy #2B3D6B; label-case=(A)",
          "[METHOD]       Fig2–5: B (make_Figure_N_v2.m from canonical JSON); Fig1, GA: §15 pptxgenjs",
          "[FILES]        Fig2–5: .fig + .m + .pdf + .tif(1200); Fig1, GA: .js + .pptx + .pdf + .tif(1200)",
          "[DATA_CHECK]   " + "  ".join(f"{k}:{v['result']}" for k, v in pvc.items()) + "   (hash guard y)",
          "[★ PROVENANCE] manifest 248/248; recorded hashes 10/10; anchors 3/3 (v2) + 4/4 (v3 history) = PASS",
          "[★ CI]          unchanged definitions (POST_RESULT_PRESENTATION_JBI.md §3); Figure 3 has no interval (none exists) = PASS",
          "[★ LEGEND]      Fig2, Fig3 legends from plotted handles; Fig4 key glyphs = drawn objects (8/8) = PASS",
          "[★ N/A]         absent set × family omitted with reason; W0:P1a not drawn = PASS",
          "[CLASS]        Fig1–5: V; GA: V",
          "[VECTOR]       pdffonts Arial only, emb=yes y ; pdfimages empty y ; unexpected rasterization n",
          "[★ SCIENCE]    n / CI / reference / scale / unit / direction / categories = PASS (captions v2)",
          "[★ REBUILD]    clean session + canonical data + scripts = " + ("PASS" if "Result: PASS" in reb else "FAIL"),
          "[★ SIZE]       " + "   ".join(f"{k}: {v['mm'][0]} × {v['mm'][1]} mm" for k, v in rows.items()),
          "[★ MARKER]     filled 0.97–1.14 mm; open / angular 1.16–1.32 mm (min 0.8)",
          "[★ TEXT]       definitions in captions; in-figure category labels only",
          "[★ BOX]        Fig2:off  Fig3:off  Fig4:off  Fig5:off",
          "[★ MULTIPANEL] Fig3 y label once per row, shared within row, equal widths y; Fig5 equal widths y",
          "[★ UNCHANGED]  all v2 (old) outputs; v2-suffixed outputs identical after the clean rebuild",
          "[★ SCHEMATIC]  numbers vs canonical y ; notation registry y ; palette / font y",
          f"[BLIND]        metadata clean y ; AI traces 0 {'y' if all(not any(v['hits'].values()) for v in blind.values()) else 'n'} ; email 0 y",
          "[MAP]          v2 → v3 numbering in NOTATION_REGISTRY.md and SOURCE_MAP.md y", "```", ""]
    (ROOT / "qa" / "MEASUREMENT_REPORT_v2.md").write_text("\n".join(L) + "\n")


def measurement_report_v3():
    figs = ["Figure_1_v3", "Figure_2_v3", "Figure_3_v3", "Figure_4_v3"]
    pvc = j("qa/plotted_vs_canonical_v3.json")
    tq = j("qa/tables_qa_v3.json")["Table_2_v3"]
    sn = j("qa/schematic_numbers_v3.json")
    blind = j("qa/blind_scan_v3.json")
    mk = j("qa/markers_v4.json")
    un = j("qa/v4_unchanged.json")
    reb = (ROOT / "qa" / "REBUILD_TEST_v4.md").read_text()
    L = ["# Measurement report — v4 revision outputs (suffix `_v3`; template §7; measured from the exported files)", "",
         "| figure | PDF page (mm) | TIF (px @ dpi = mm) | regular text (pt) | bold text (pt) | panel labels (pt) | min (pt) | fonts | raster objects | overlaps / near | edge < 0.3 mm |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    rows = {}
    for name in figs:
        m = j(f"qa/measure_{name}.json")
        t = m.get("tif", {})
        reg = sorted({round(x["size"]) for x in m["spans"] if "Bold" not in x["font"]})
        bold = sorted({round(x["size"]) for x in m["spans"] if "Bold" in x["font"]})
        pan = sorted({round(x["size"]) for x in m["spans"] if "Bold" in x["font"] and re.fullmatch(r"\([A-F]\)", x["text"].strip())})
        fonts = ", ".join(sorted({x.split()[0].split("+")[-1] for x in m["pdffonts"][2:]}))
        rows[name] = dict(mm=m["page_mm"], tif=t.get("mm"))
        L.append(f"| {name} | {m['page_mm'][0]} × {m['page_mm'][1]} | {t.get('px')} @ {t.get('dpi', [None])[0]} = {t.get('mm')} | "
                 f"{reg} | {bold} | {pan or '—'} | {m['min_text_pt']} | {fonts} (emb=yes) | {max(0, len(m['pdfimages']) - 2)} | "
                 f"{len(m['text_overlaps'])} | {len(m['edge_clearance_below_0p3mm'])} |")
    L += ["", "Font sizes unchanged from v3: data figures tick / category 14, axis 15, panel 16 pt bold; Figure 1 body 14, "
          "headings 15, panel labels 16 pt bold. Widths unchanged (data figures 189.79 mm PDF; Figure 1 190.0 mm). "
          "Heights: Figure 1 232.0 → 219.0 mm; Figure 3 228.25 → 219.07 mm (both ≤ 220 mm); Figures 2 and 4 unchanged. "
          "Not revised and not re-measured: Figure 5 (`Figure_5_v2`), graphical abstract (`Graphical_abstract_v2`).", "",
          "## Marker sizes before (v2) → after (v3), outer incl. edge, from PDF paths (`qa/markers_v4.json`)", "",
          "| figure | shape | face | edge (pt) | n | before w × h (mm) | after w × h (mm) |", "|---|---|---|---|---|---|---|"]
    for f, v in mk.items():
        for i, b in enumerate(v["markers_before"]):
            a = v["markers_after"][i] if v["markers_after"] else None
            L.append(f"| {f} | {b['shape']} | {b['face']} | {b['edge_pt']} | {b['n']} | {b['outer_w_mm']} × {b['outer_h_mm']} | "
                     + (f"{a['outer_w_mm']} × {a['outer_h_mm']} |" if a else "unchanged (not revised) |"))
    L += ["", "Ticks, axes and panels: unchanged (`qa/v4_unchanged.json`: Figures 2 and 4 — every text span and every "
          "non-marker path identical to v2; Figure 3 — texts, fonts, sizes and path kinds identical, axes 52.5 → 49.5 mm high; "
          "Figure 1 — shapes, texts, sizes, colours, x positions, widths and heights identical, y positions and four vertical "
          "connector lengths changed).", "",
          "| check | Figure_1 | Figure_2 | Figure_3 | Figure_4 |", "|---|---|---|---|---|",
          "| v4 unchanged-check | " + " | ".join(un[k]["result"] for k in ("Figure_1", "Figure_2", "Figure_3", "Figure_4")) + " |",
          "| TIF ↔ PDF whole image (`qa/tif_vs_pdf_*`) | " + " | ".join(j(f"qa/tif_vs_pdf_Figure_{n}_v3.json")["result"] for n in (1, 2, 3, 4)) + " |",
          "| TIF markers complete (`qa/tif_markers_*`) | — | " + " | ".join(
              "PASS" if not j(f"qa/tif_markers_Figure_{n}_v3.json")["flagged"] else "FAIL" for n in (2, 3, 4)) + " |", "",
          "## Finding: MATLAB raster export clips markers at its 4,000-px render tiles", "",
          "| earlier TIF (unchanged) | markers | flagged (PDF ink not covered by the TIF > 10 %) and visual verdict |",
          "|---|---|---|"]
    clipped = {("Figure_3", (84.86, 21.64)), ("Figure_2_v2", (169.63, 98.04)), ("Figure_4_v2", (84.45, 26.01))}
    for stem in ("Figure_2", "Figure_3", "Figure_4", "Figure_2_v2", "Figure_3_v2", "Figure_4_v2", "Figure_5_v2"):
        r = j(f"qa/tif_markers_{stem}.json")
        fl = "; ".join(f"({x['centre_mm'][0]}, {x['centre_mm'][1]}) mm, {round(100 * x['uncovered_frac'])} % uncovered: "
                       + ("**clipped** (one side missing)" if (stem, tuple(x["centre_mm"])) in clipped else
                          "intact (thinner MATLAB stroke)") for x in r["flagged"]) or "none"
        L.append(f"| {stem} | {r['markers']} | {fl} |")
    L += ["", "Visual verdicts from PDF | TIF crops at 1,200 dpi: `qa/tif_tile_clipping_evidence.png`. Each clipped marker "
          "straddles a 4,000-px tile boundary of MATLAB's raster export (x = 4,000 or 8,000 px, or 4,000 px from the "
          "bottom). The v3 TIFs are the MATLAB vector PDFs rasterised by poppler (`jbi_export_v4.m`): no flagged marker.", "",
          "## Plotted vs canonical and legend / key ↔ plot (`qa/plotted_vs_canonical_v3.json`)", ""]
    for k, v in pvc.items():
        extra = v.get("legend_entries", "")
        if "key_glyphs" in v:
            extra = "key: " + "; ".join(v["key_glyphs"])
        L.append(f"* {k}_v3: {v['result']} — {v['points']} points with their intervals / bounds; mismatches {len(v['mismatches'])}; {extra}")
    L += ["", "## Schematic numbers (`qa/schematic_numbers_v3.json`)", ""]
    for k, v in sn.items():
        L.append(f"* {k}: {len(v)} distinct numeric tokens; canonical {sum(r['source'] == 'canonical' for r in v)}, "
                 f"unmatched {sum(r['source'] == 'UNMATCHED' for r in v)}")
    p, d, b = tq["pdf"], tq["docx"], tq["bound"]
    L += ["", "## Table 2 v3 (`qa/tables_qa_v3.json`)", "",
          f"* pages {p['pages']} (A4 landscape {p['page_mm'][0]} × {p['page_mm'][1]} mm); rules per page {p['rules_per_page']}; "
          f"vertical rules {p['vertical_rules']}; shading {d['shading_elements']} + {p['filled_rects']}; run sizes {d['run_sizes_pt']}; "
          f"paragraph styles {d['paragraph_styles']}; fonts {', '.join(p['pdffonts'])}",
          f"* bound {b['row']} {b['field']}: exact {b['exact']} (families.json) → displayed {b['display']} "
          f"({b['decimals']} decimals; 3 decimals would give {b['display_3dp']})",
          "* CSV cells changed vs Table_2_v2: " + "; ".join(f"row {i} col {c}: '{x}' → '{y}'" for i, c, x, y in tq["csv_changes_vs_v2"]),
          f"* checks: {'PASS' if all(tq['checks'].values()) else 'FAIL'} ({len(tq['checks'])})", "",
          "## Clean rebuild (`qa/REBUILD_TEST_v4.md`)", "", "Result: " + ("PASS" if "Result: PASS" in reb else "FAIL"), "",
          "## Template §12-3 return block (v4)", "", "```",
          "[STYLE]        Arial; tick/axis/panel = 14/15/16 pt (Figure 1 body/heading/panel 14/15/16); grayscale+navy #2B3D6B; label-case=(A)",
          "[METHOD]       Fig2–4: B (make_Figure_N_v3.m from canonical JSON); Fig1: §15 pptxgenjs",
          "[FILES]        Fig2–4: .fig + .m + .pdf + .tif(1200; from the vector PDF); Fig1: .js + .pptx + .pdf + .tif(1200)",
          "[DATA_CHECK]   " + "  ".join(f"{k}_v3:{v['result']}" for k, v in pvc.items()) + "   (hash guard y)",
          "[★ PROVENANCE] manifest + recorded hashes + anchors as v3 = PASS; validation.json + v4_table2_sign_decimals (bound equals families.json)",
          "[★ CI]          unchanged definitions (§3); Figure 3 has no interval (none exists) = PASS",
          "[★ LEGEND]      Fig2, Fig3 legends from plotted handles; Fig4 key glyphs = drawn objects (8/8) = PASS",
          "[★ N/A]         absent set × family omitted with reason; W0:P1a not drawn = PASS",
          "[CLASS]        Fig1–4: V",
          "[VECTOR]       pdffonts Arial only, emb=yes y ; pdfimages empty y ; unexpected rasterization n",
          "[★ SCIENCE]    n / CI / reference / scale / unit / direction / categories = PASS (values, captions unchanged)",
          "[★ REBUILD]    clean session + canonical data + scripts = " + ("PASS" if "Result: PASS" in reb else "FAIL"),
          "[★ SIZE]       " + "   ".join(f"{k}: {v['mm'][0]} × {v['mm'][1]} mm" for k, v in rows.items()),
          "[★ MARKER]     filled circle 1.499 mm (Fig2–4); hollow / angular 1.55–1.98 mm (v2 nominal ratios kept); Fig5 unchanged 0.97 mm",
          "[★ TEXT]       definitions in captions; in-figure category labels only (unchanged)",
          "[★ BOX]        Fig2:off  Fig3:off  Fig4:off",
          "[★ MULTIPANEL] Fig3 y label once per row (1.0 mm past each axis end, inside its row band), equal widths y",
          "[★ UNCHANGED]  Figure 5, Tables 1 / S5, graphical abstract, captions; all earlier files byte-identical",
          "[★ SCHEMATIC]  numbers vs canonical y ; notation registry y ; palette / font y",
          f"[BLIND]        metadata clean y ; AI traces 0 {'y' if all(not any(v['hits'].values()) for v in blind.values()) else 'n'} ; email 0 y (TIF pixel strips excluded)",
          "[MAP]          v4 current-file map in SOURCE_MAP.md y", "```", ""]
    (ROOT / "qa" / "MEASUREMENT_REPORT_v3.md").write_text("\n".join(L) + "\n")


def measurement_report_v4():
    figs = [f"Figure_{n}_v4" for n in range(1, 7)]
    pvc = j("qa/plotted_vs_canonical_v4.json")["Figure_5"]
    mk = j("qa/markers_v5.json")["markers"]
    rn = j("qa/renumber_v5.json")
    cap = j("qa/captions_v4.json")
    blind = j("qa/blind_scan_v4.json")
    reb = (ROOT / "qa" / "REBUILD_TEST_v5.md").read_text()
    L = ["# Measurement report — v5 revision (suffix `_v4`; template §7; measured from the exported files)", "",
         "| figure | source | PDF page (mm) | TIF (px @ dpi = mm) | regular text (pt) | bold text (pt) | panel labels | min (pt) | fonts | raster objects | overlaps / near | edge < 0.3 mm | TIF ↔ PDF |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for name in figs:
        m = j(f"qa/measure_{name}.json")
        t = m.get("tif", {})
        reg = sorted({round(x["size"]) for x in m["spans"] if "Bold" not in x["font"]})
        bold = sorted({round(x["size"]) for x in m["spans"] if "Bold" in x["font"]})
        pan = sorted({x["text"].strip() for x in m["spans"] if "Bold" in x["font"] and re.fullmatch(r"\([A-F]\)", x["text"].strip())})
        fonts = ", ".join(sorted({x.split()[0].split("+")[-1] for x in m["pdffonts"][2:]}))
        src = rn[name[:-3]]["source"]
        tvp = j(f"qa/tif_vs_pdf_{name}.json")["result"]
        L.append(f"| {name} | `{src}` | {m['page_mm'][0]} × {m['page_mm'][1]} | {t.get('px')} @ {t.get('dpi', [None])[0]} = {t.get('mm')} | "
                 f"{reg} | {bold} | {' '.join(pan)} | {m['min_text_pt']} | {fonts} (emb=yes) | {max(0, len(m['pdfimages']) - 2)} | "
                 f"{len(m['text_overlaps'])} | {len(m['edge_clearance_below_0p3mm'])} | {tvp} |")
    L += ["", "All heights ≤ 220 mm; widths as before (data figures 189.79 mm PDF, Figure 1 190.0 mm). Tick / category 14, "
          "axis 15, panel labels 16 pt bold in every data figure; Figure 1 body 14, headings 15, panel labels 16 pt.", "",
          "## New Figure 5: markers (outer incl. edge, from PDF paths; `qa/markers_v5.json`)", "",
          "| shape | kind | edge colour | n (incl. key) | outer w × h (mm) |", "|---|---|---|---|---|"]
    for m in mk:
        L.append(f"| {m['shape']} | {m['kind']} | {m['edge_colour']} | {m['n']} | {m['outer_w_mm']} × {m['outer_h_mm']} |")
    L += ["", "## New Figure 5: plotted vs canonical and key ↔ plot (`qa/plotted_vs_canonical_v4.json`)", "",
          f"* {pvc['result']} — {pvc['points']} values (12 arms × 12 cells × 2 metrics) as line and marker objects; "
          f"mismatches {len(pvc['mismatches'])}",
          "* panels: " + "; ".join(pvc["panels"]),
          f"* key: {pvc['key_entries_n']} entries, each copying the plotted line and marker of its arm in all six panels: "
          + ", ".join(pvc["key_entries"]) + f"; 12 glyphs distinct: {pvc['key_glyphs_distinct']}", "",
          "## Renumbered figures: byte identity with their sources (`qa/renumber_v5.json`)", "",
          "| file | source | identical |", "|---|---|---|"]
    for k, v in rn.items():
        for r in v["files"]:
            L.append(f"| `{r['file']}` | `{r['source']}` | {'yes' if r['byte_identical'] else ('poppler TIF of the PDF' if r['byte_identical'] is None else 'NO')} |")
    L += ["", "## Captions cross-check (`qa/captions_v4.json`)", "",
          f"* headings {cap['headings']}; result {cap['result']}"]
    for k, v in cap["figures"].items():
        L.append(f"* {k}: source {v['source']}; body identical to source: {v['body_identical_to_source']}; panel letters used "
                 f"{v['panel_letters_used']} ⊆ labels in the PDF {v['panel_labels_in_pdf']}")
    L.append("* references: " + ", ".join(sorted({r["ref"] for r in cap["references"]})) + " — all resolve")
    L += ["", "## Clean rebuild (`qa/REBUILD_TEST_v5.md`)", "", "Result: " + ("PASS" if "Result: PASS" in reb else "FAIL"), "",
          "## Template §12-3 return block (v5)", "", "```",
          "[STYLE]        Arial; tick/axis/panel = 14/15/16 pt (Figure 1 body/heading/panel 14/15/16); grayscale+navy #2B3D6B; label-case=(A)",
          "[METHOD]       Fig5: B (make_Figure_5_v4.m from canonical JSON); Fig1–4, 6: byte copies of their sources (renumber_v5.py)",
          "[FILES]        per data figure .fig + .m + .pdf + .tif(1200, poppler from the PDF); Fig1 .js + .pptx + .pdf + .tif(1200)",
          f"[DATA_CHECK]   Figure_5_v4:{pvc['result']} (288 values; hash guard y); renumbered: byte identity y",
          "[★ PROVENANCE] manifest + recorded hashes + anchors (v2 3/3, v3 4/4, v5 4/4) = PASS",
          "[★ CI]          Figure 5: Wald 95% interval from the influence function (sdr.py), coverage share (grid.py) confirmed in code; no interval drawn",
          f"[★ LEGEND]      Figure 5 key 12 / 12 from plotted objects, 12 series per panel = {pvc['result']}",
          "[★ N/A]         none (all 12 arms × 12 cells exist; M_finite 200 everywhere)",
          "[CLASS]        Fig1–6: V",
          "[VECTOR]       pdffonts Arial only, emb=yes y ; pdfimages empty y ; unexpected rasterization n",
          "[★ SCIENCE]    n / reference (0, 0.95) / log K / unit (%) / direction / categories = PASS",
          "[★ REBUILD]    clean session + canonical data + scripts = " + ("PASS" if "Result: PASS" in reb else "FAIL"),
          "[★ SIZE]       " + "   ".join(f"{n}: {j(f'qa/measure_{n}.json')['page_mm'][0]} × {j(f'qa/measure_{n}.json')['page_mm'][1]} mm" for n in figs),
          "[★ MARKER]     Fig5 filled circle 1.31 mm, open circle 1.41 mm, other shapes 1.30–1.79 mm (small, with edges); Fig1–4, 6 unchanged",
          "[★ TEXT]       definitions in captions; in-figure category labels only",
          "[★ BOX]        Fig2:off  Fig3:off  Fig4:off  Fig5:off  Fig6:off",
          "[★ MULTIPANEL] Fig5 y shared within a row, y label once per row, x label once, equal widths y",
          "[★ UNCHANGED]  content of Figures 1–4, 6 (byte copies), Tables 1, 2, S5, graphical abstract; all earlier files",
          "[★ SCHEMATIC]  Figure 1 = Figure_1_v3 (numbers vs canonical y)",
          f"[BLIND]        metadata clean y ; AI traces 0 {'y' if all(not any(v['hits'].values()) for v in blind.values()) else 'n'} ; email 0 y (TIF pixel strips excluded)",
          "[MAP]          v3/v4 → v5 numbering in POST_RESULT §8, NOTATION_REGISTRY.md, SOURCE_MAP.md y", "```", ""]
    (ROOT / "qa" / "MEASUREMENT_REPORT_v4.md").write_text("\n".join(L) + "\n")


def measurement_report_supp():
    m = j("qa/measure_supp_v6.json")
    pv = j("qa/plotted_vs_canonical_supp_v6.json")
    tq = j("qa/tables_qa_supp_v1.json")
    cap = j("qa/captions_supp_v1.json")
    sd = j("qa/supplementary_docx_v1.json")
    blind = j("qa/blind_scan_supp_v6.json")
    val = j("canonical_supplement/validation.json")
    reb = (ROOT / "qa" / "REBUILD_TEST_supp_v6.md").read_text()
    L = ["# Measurement report — supplement v6 (template §7; measured from the exported files)", "",
         "| figure | pages | page size (mm) | text sizes (pt) | min (pt) | fonts | raster objects | overlaps / near | edge < 0.3 mm | TIF dpi | TIF = PDF page |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in m.items():
        fonts = ", ".join(sorted({x.split()[0].split("+")[-1] for x in v["pdffonts"]}))
        L.append(f"| {k} | {v['pages']} | {', '.join(f'{a} × {b}' for a, b in v['page_sizes_mm'])} | {v['text_sizes_pt']} | "
                 f"{v['min_text_pt']} | {fonts} (emb=yes) | {v['raster_objects']} | {v['overlaps']} | {v['edge_issues']} | "
                 f"{v['tif_dpi']} | {v['tif_identical_pages']}/{v['pages']} |")
    L += ["", "Heatmap pages (S1–S3): cell values 11 pt, ticks 12, "
          "labels 13, titles 14 pt bold (template conflict recorded; the accepted 9-pt floor was not needed). S5, S6: 14 / 15 / "
          "16 pt. The subscript A of φ_A touches its base glyph by design and is excluded from the overlap count.", "",
          "## Plotted vs canonical (`qa/plotted_vs_canonical_supp_v6.json`)", ""]
    for k, v in pv.items():
        L.append(f"* {k}: {v['result']} — " + ", ".join(f"{kk} {vv if not isinstance(vv, list) else len(vv)}"
                                                          for kk, vv in v.items() if kk != "result"))
    cc = val["cross_checks"]
    L += ["", "## Cross-checks against the main-figure values (`canonical_supplement/validation.json`)", "",
          f"* anchors: " + "; ".join(f"{k} = {v!r}" for k, v in val["anchors"].items()),
          f"* main Figure 4 (`w_history_D`) rows equal: {cc['w_history_D_rows_equal']}; slice (`fig2B_slice_D`): "
          f"{cc['fig2B_slice_rows_equal']}; main Figure 5 (`fig5_bias_coverage`): {cc['fig5_bias_coverage_rows_equal']}; "
          f"main Figure 2 (B, C) rows equal to S6: {cc['S6_equals_main_figure_2_BC_rows']}",
          "* families reproduced from the S1 cells (mean = D̄ exactly): " + "; ".join(
              f"{k} {v['cells']} cells, mean {v['mean_3dp']} = D̄ {v['D_bar_3dp']} (max |cell diff| {v['max_abs_diff_cells']})"
              for k, v in cc["families_reproduced"].items()),
          f"* report_cells.csv vs cell_metrics.csv: {cc['report_cells_agree_with_cell_metrics']}",
          f"* cells rounding to ±0: D {val['s1_round_to_zero_3dp']}, relative bias {val['s2_round_to_zero_1dp']}",
          f"* Figure S4: {val['s4_values']} points; {val['figure_S4']}; {cc['S4_equals_tableS4_mask_check']} equal to the package table", "",
          "## Tables (`qa/tables_qa_supp_v1.json`)", "",
          "| table | pages | rules per page | vertical rules | run sizes (pt) | paragraph styles | cells compared with the package CSV | checks |",
          "|---|---|---|---|---|---|---|---|"]
    for k, v in tq.items():
        p, d = v["pdf"], v["docx"]
        L.append(f"| {k} | {p['pages']} | {p['rules_per_page']} | {p['vertical_rules']} | {d['run_sizes_pt']} | "
                 f"{d['paragraph_styles']} | {v['cells_compared'] if v['cells_compared'] is not None else 'XML/CSV = Table_S5_v2'} | "
                 f"{'PASS' if all(v['checks'].values()) else 'FAIL'} ({len(v['checks'])}) |")
    L += ["", f"## Captions (`qa/captions_supp_v1.json`): {cap['result']} — headings {cap['headings']}", "",
          "## Supplementary Material document (`qa/supplementary_docx_v1.json`)", "",
          f"* result {sd['result']}; LibreOffice PDF {sd['pdf']['pages']} pages, fonts {sd['pdf']['fonts']}, images "
          f"{sd['pdf']['images']}; paragraph styles {sd['word']['paragraph_styles']}; automatic numbering "
          f"{sd['word']['numbered_paragraphs']}; sections {sd['word']['sections']}",
          f"* order: {' → '.join(sd['order'])}; every caption once: {sd['captions_once']}",
          f"* images per figure {sd['images_per_figure']}; widths (mm) {sd['image_widths_mm']}",
          f"* methods text equal to the converted draft: {sd['methods_text_equal']} ({sd['methods_chars']} characters); "
          f"placeholders kept {sd['placeholders']}; characters missing in Arial left: {sd['arial_missing_chars_in_docx']}", "",
          f"## Blind scan (`qa/blind_scan_supp_v6.json`): {len(blind)} files, hits "
          f"{sum(any(v['hits'].values()) for v in blind.values())}", "",
          "## Clean rebuild (`qa/REBUILD_TEST_supp_v6.md`)", "", "Result: " + ("PASS" if "Result: PASS" in reb else "FAIL"), ""]
    (ROOT / "qa" / "MEASUREMENT_REPORT_supp_v1.md").write_text("\n".join(L) + "\n")


# ------------------------------------------------------------------------------------------------ README.md
def readme():
    files = subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True).stdout.split("\n")
    files = [f for f in files if f and f != "README.md" and not f.startswith("templates/")]
    deliver = [f for f in files if f.startswith(("figures/Figure_", "figures_v2/Figure_", "figures_v3/Figure_",
                                                 "figures_v4/Figure_", "figures_supp_v1/Figure_", "graphical_abstract/G",
                                                 "tables/Table_"))
               and not f.endswith((".m", ".js"))]
    L = ["# JBI figures, tables and graphical abstract — SS-DS203 manuscript", "",
         "Built 2026-10-27 from the read-only package `" + str(PKG) + "` (manifest verified, 248 / 248). Task: "
         "`CC_TASK_JBI_figures_tables_v2.md`.", "",
         "## Contents", "",
         "* `figures/Figure_1/` — schematic (`make_Figure_1.js` → `.pptx` → LibreOffice `.pdf` → 1,200-dpi `.tif`)",
         "* `figures/Figure_2..4/` — data figures (`make_Figure_N.m` → `.fig` → vector `.pdf` + 1,200-dpi `.tif`); "
         "`figures/common/` shared MATLAB helpers and `verify_plotted.m`",
         "* `graphical_abstract/` — `make_Graphical_abstract.js` → `.pptx`, `.pdf`, `.tif`",
         "* `tables/` — `Table_1..3.docx` (editable), `.csv` (displayed cells), `.pdf` (LibreOffice rendering for QA)",
         "* `canonical/` — frozen values (`scripts/freeze.py`), `SHA256SUMS.txt`",
         "* `CAPTIONS.md`, `SOURCE_MAP.md`, `NOTATION_REGISTRY.md`, `POST_RESULT_PRESENTATION_JBI.md`, "
         "`SUPPLEMENT_INDEX.md`, `qa/MEASUREMENT_REPORT.md`, `qa/` measurement JSON, `templates/`", "",
         "## Rebuild (clean)", "", "```",
         ".venv/bin/python -I scripts/freeze.py",
         "for n in 2 3 4; do /Applications/MATLAB_R2025b.app/bin/matlab -batch \"close all force; clear; "
         "run('figures/Figure_$n/make_Figure_$n.m')\"; done",
         "node figures/Figure_1/make_Figure_1.js; (cd figures/Figure_1 && soffice --headless --convert-to pdf "
         "Figure_1.pptx && pdftoppm -r 1200 -tiff -tiffcompression lzw -singlefile Figure_1.pdf Figure_1)",
         "node graphical_abstract/make_Graphical_abstract.js; (cd graphical_abstract && soffice --headless "
         "--convert-to pdf Graphical_abstract.pptx && pdftoppm -r 1200 -tiff -tiffcompression lzw -singlefile "
         "Graphical_abstract.pdf Graphical_abstract)",
         ".venv/bin/python -I scripts/build_tables.py; (cd tables && for n in 1 2 3; do soffice --headless "
         "--convert-to pdf Table_$n.docx; done)",
         "scripts/rebuild_check.sh   # the clean-rebuild comparison used for qa/REBUILD_TEST.md", "```", "",
         "## v3 revision (2026-10-27)", "",
         "Revised outputs carry the suffix `_v2` (figures in `figures_v2/`; `Graphical_abstract_v2.*`; `Table_1_v2`, "
         "`Table_2_v2`, `Table_S5_v2`; `CAPTIONS_v2.md`); the earlier outputs are unchanged. New numbering: Figure 1 "
         "design, Figure 2 families, Figure 3 prior action history (new), Figure 4 erasure, Figure 5 X1/X2, Table 1, Table 2, "
         "Supplementary Table S5. Rebuild and checks: `scripts/rebuild_check_v3.sh <scratch_dir>`; report "
         "`qa/MEASUREMENT_REPORT_v2.md`; decisions `POST_RESULT_PRESENTATION_JBI.md` §6.", "",
         "## v4 revision (2026-10-27)", "",
         "Task `CC_TASK_JBI_figures_tables_v4.md`. Revised outputs carry the suffix `_v3`: `figures_v3/Figure_1..4/` "
         "(markers 1.5 mm filled in Figures 2–4; Figures 1 and 3 at most 220 mm high, font sizes unchanged) and "
         "`tables/Table_2_v3.*` (\"Locked rule outcome\"; the one bound shown as −0.0003). Current set: Figures 1–4 `_v3`, "
         "Figure 5 `_v2`, Table 1 `_v2`, Table 2 `_v3`, Table S5 `_v2`, graphical abstract `_v2`, captions "
         "`CAPTIONS_v2.md`. The data-figure TIFs of v4 are the MATLAB vector PDFs rasterised by poppler "
         "(`figures/common/jbi_export_v4.m`; MATLAB's raster export clips markers at its 4,000-px render tiles). "
         "Rebuild and checks: `scripts/rebuild_check_v4.sh <scratch_dir>`; report `qa/MEASUREMENT_REPORT_v3.md`; "
         "decisions `POST_RESULT_PRESENTATION_JBI.md` §7.", "",
         "## v5 revision (2026-10-27) — current set", "",
         "Task `CC_TASK_JBI_figures_tables_v5.md`. Complete figure set with the suffix `_v4` in `figures_v4/Figure_1..6/`, "
         "numbered in the order of first citation in Results: 1 design (= `Figure_1_v3`), 2 erasure (= `Figure_4_v3`), "
         "3 families (= `Figure_2_v3`), 4 prior action history (= `Figure_3_v3`), 5 relative bias and coverage at the "
         "slice (new; `make_Figure_5_v4.m`, canonical `fig5_bias_coverage.json`), 6 exploratory X1/X2 (= `Figure_5_v2`; "
         "TIF from its PDF). Renumbered files are byte copies made by `scripts/renumber_v5.py`. Captions `CAPTIONS_v4.md`; "
         "tables `Table_1_v2`, `Table_2_v3`, `Table_S5_v2`; graphical abstract `Graphical_abstract_v2`. Rebuild and checks: "
         "`scripts/rebuild_check_v5.sh <scratch_dir>`; report `qa/MEASUREMENT_REPORT_v4.md`; decisions "
         "`POST_RESULT_PRESENTATION_JBI.md` §8.", "",
         "## v6 supplement (2026-10-27)", "",
         "Task `CC_TASK_JBI_supplement_v6.md`. Supplementary Figures S1–S6 in `figures_supp_v1/` (multi-page "
         "vector PDF; per-page .fig and TIF in `pages/`), Tables S1–S6 in `tables/Table_S*_v1.*`, captions "
         "`CAPTIONS_supplement_v1.md`, the Word document `supplementary/Supplementary_Material_v1.docx`; values in "
         "`canonical_supplement/` (`scripts/freeze_supplement.py`); investigator-provided inputs in `inputs/` "
         "(`mask_check.json`, `JBI_Supplementary_Methods_draft_v2.md`). Rebuild and checks: "
         "`scripts/rebuild_check_supp_v6.sh <scratch_dir>`; report "
         "`qa/MEASUREMENT_REPORT_supp_v1.md`; decisions `POST_RESULT_PRESENTATION_JBI.md` §9.", "",
         "## SHA-256 of the deliverables", "", "| file | bytes | SHA-256 |", "|---|---|---|"]
    for f in deliver:
        p = ROOT / f
        L.append(f"| `{f}` | {p.stat().st_size} | `{sha(p)}` |")
    (ROOT / "README.md").write_text("\n".join(L) + "\n")


def main():
    source_map()
    supplement_index()
    if "--supp" in sys.argv[1:]:
        measurement_report_supp()   # main-set reports are left as recorded
    elif "--v4" in sys.argv[1:]:
        measurement_report_v4()     # earlier reports are left as recorded
    elif "--v3" in sys.argv[1:]:
        measurement_report_v3()     # the v1 and v2 reports are left as recorded
    elif "--v2" in sys.argv[1:]:
        measurement_report_v2()     # the v1 report (qa/MEASUREMENT_REPORT.md) is left as recorded
    else:
        measurement_report()
    readme()
    print("written: SOURCE_MAP.md, SUPPLEMENT_INDEX.md, qa/MEASUREMENT_REPORT.md, README.md")


if __name__ == "__main__":
    main()
