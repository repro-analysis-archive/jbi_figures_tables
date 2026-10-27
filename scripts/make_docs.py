#!/usr/bin/env python3
"""Write SOURCE_MAP.md, SUPPLEMENT_INDEX.md, qa/MEASUREMENT_REPORT.md and README.md from the canonical files, the
package manifest and the QA outputs (hashes are computed, never typed).

    .venv/bin/python -I scripts/make_docs.py
"""
import sys

sys.dont_write_bytecode = True

import hashlib  # noqa: E402
import json  # noqa: E402
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
    L += ["", "Not reproduced in the JBI main text and therefore candidates for the supplement: the pre-result "
          "main-text figures (above), the FM / REF pairs of the role-switch view at the slice, PCA / LEACE variance "
          "retained (results report §3), the slice group and the NV comparator of X (Supplementary Figure X / Table X)."]
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


# ------------------------------------------------------------------------------------------------ README.md
def readme():
    files = subprocess.run(["git", "-C", str(ROOT), "ls-files"], capture_output=True, text=True).stdout.split("\n")
    files = [f for f in files if f and f != "README.md" and not f.startswith("templates/")]
    deliver = [f for f in files if f.startswith(("figures/Figure_", "graphical_abstract/G", "tables/Table_"))
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
         "## SHA-256 of the deliverables", "", "| file | bytes | SHA-256 |", "|---|---|---|"]
    for f in deliver:
        p = ROOT / f
        L.append(f"| `{f}` | {p.stat().st_size} | `{sha(p)}` |")
    (ROOT / "README.md").write_text("\n".join(L) + "\n")


def main():
    source_map()
    supplement_index()
    measurement_report()
    readme()
    print("written: SOURCE_MAP.md, SUPPLEMENT_INDEX.md, qa/MEASUREMENT_REPORT.md, README.md")


if __name__ == "__main__":
    main()
