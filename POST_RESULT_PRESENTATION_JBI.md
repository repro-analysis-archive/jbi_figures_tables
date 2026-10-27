# Post-result presentation choices for the JBI figures and tables (2026-10-27)

* **Task:** `CC_TASK_JBI_figures_tables_v2.md` (supersedes v1).
* **Made after all results were known:** the step-5, step-6 and step-7 records, X1/X2 (`1c8e628`), B (`458341f`), the
  readout, the fact base v5 and the package `POST_RESULT_PRESENTATION.md` were all available. Nothing here changes a
  number, a verdict, the pre-result slice or any committed record; nothing was re-estimated.
* **Package:** `/Volumes/ADDATA/医療動画/SS_DS203_manuscript_20261020/`, read only, `shasum -a 256 -c MANIFEST_SHA256.txt`
  248 / 248 OK before starting (`qa/PREFLIGHT.md`).

## 1. Inputs that were not provided

| Item | Status | What was done |
|---|---|---|
| `templates/` in the work folder | the work folder did not exist; no templates had been placed | the three templates were copied from `~/Desktop/` (SHA-256 in `templates/SHA256SUMS.txt`) |
| `SS_DS203_JBI_manuscript_plan_v3.md` | not found (Spotlight, ~/Downloads, ~/Desktop, ADDATA/医療動画) | the element definitions of task §5 (which cite plan v3 §4) were used verbatim; anything in plan v3 not restated in task §5 could not be applied |

No SOURCE MISSING occurred: every plotted or tabulated value is in the package.

## 2. Conflicts between rules and their resolution (precedence: task §2 > JBI > templates > task rest)

| # | Conflict | Resolution |
|---|---|---|
| 1 | Template §2-1 house sizes (tick 14 / axis 15 / panel 16 pt, from a 180 mm Med Phys figure) vs JBI full width 190 mm with 3–9 panels | Relative rule kept (tick → axis → panel = 9 / 10 / 11 pt; legends 9; secondary labels 8); measured minimum 8 pt (Figures 1–4), 7 pt (graphical abstract at 130 mm) |
| 2 | Template TIF 600 dpi vs JBI pure line art ≥ 1,000 dpi | All data figures and schematics are pure line art (no photographs or gradients): TIF at 1,200 dpi, LZW / PackBits |
| 3 | JBI full width 190 mm vs MATLAB rounding the PDF page up to whole points | Data-figure canvas 18.97 cm → PDF 538 pt = 189.79 mm, TIF 189.72 mm; schematics exactly 190.0 mm |
| 4 | Panel-label case: JBI not specified | Template default (A), (B), … |
| 5 | Template §2-8 (heading-like text belongs in the caption) vs hard limit 2.3 (exploratory clearly labelled) | Short in-figure category labels kept where they prevent misreading an exploratory result as confirmatory: Figure 3 panel titles "Exploratory analysis B: …", Figure 1 dashed boxes, graphical abstract "EXPLORATORY"; definitions and ceilings are in the captions |
| 6 | Hard limit 2.2 (show all families of the records) vs 2.3 (exploratory never in a confirmatory panel) | The W = 0 set's P1a (16 cells; outside the §10.3 scope, labelled exploratory in the results report §1) is not drawn in Figure 2A and not listed in Table 2; both refer to it (caption, Table 2 footnote); it remains in the results report (Supplement) |
| 7 | Template §3 (`fig_data.mat` via `savemat`) vs the venv (no SciPy needed) | MATLAB reads the canonical JSON directly with `jsondecode`, after its own SHA-256 check (template: "CSV でも可") |
| 8 | Template §15 PowerPoint export vs headless reproducibility | Schematics exported to PDF with LibreOffice 26.2 (native vector shapes, ArialMT / Arial-BoldMT embedded, no raster objects); the editable `.pptx` is kept |
| 9 | Notation with sub/superscripts in schematics vs 7 pt floor | LibreOffice renders `pptxgenjs` sub/superscript runs at 58 % (measured: 9 pt → 5.2 pt); schematics use plain forms registered in `NOTATION_REGISTRY.md` |
| 10 | Protocol text uses ∈ and ⌊ ⌋, which Arial lacks | Rewritten mechanically ("P = 5 or 30", "floor(…)", "K: 1, 2, 5, 15"); no value changed |
| 11 | Table template 11 pt vs the width of Tables 1–3 | 11 pt kept; all three tables on A4 landscape pages (text width 247 mm); Table 3 spans three pages with a repeated header row |
| 12 | Data-handling rule (no case identifiers in outputs) vs the package Table 1 text naming the one protocol-excluded case | Table 1 says "one case (timestamp beyond video end)"; the identifier is not reproduced |

## 3. Interval definitions (confirmed in the generating code, not assumed)

| Quantity | Construction | Code |
|---|---|---|
| D̄_F 95% interval (Figure 2A, Table 2) | percentile 2.5 / 97.5 of a bootstrap of the family mean: within each cell the 200 replicates are resampled with the same indices for both arms and the truth (mean truth recomputed per resample); cells fixed; 2,000 resamples; seed 20261008 | `ss_benchmark/grid.py` `_d_values`, `family_verdict` (package `08_additional/code/`) |
| Per-cell Δ 95% interval (Figure 4) | percentile 2.5 / 97.5 of a paired bootstrap of the replicates within the cell (same indices for both arms and the truth); 2,000 resamples (`n_boot` = null → `N_BOOTSTRAP` 2,000) | `xplore/x_compare.py` `compare` (`ss_exploratory.bundle`, `1c8e628`); `x_run_record.json` |
| BA 95% interval and one-sided upper bound (Figure 3, Table 3) | case bootstrap stratified by site (cases resampled with all their steps); percentiles 2.5 / 97.5 and the 95th percentile; 2,000 resamples; seed 20261008 | `ss_benchmark/checks.py` `bootstrap_case_weights`, `ba_with_ci` |
| E2 ΔAUC 95% interval (Table 3) | case-cluster bootstrap, percentiles 2.5 / 97.5 | `checks.py` `e2_auc` |
| Per-cell D at the slice (Figure 2B) | no interval exists in the records (the protocol defines intervals for family means only); none was computed | — |

## 4. Choices per output

| Output | Choice made after the results |
|---|---|
| Main-text set | Follows task §5 (plan v3 §4): Figure 1 schematic; Figure 2 confirmatory; Figure 3 erasure; Figure 4 exploratory X1/X2; Tables 1–3; graphical abstract. This reorganises the pre-result main-text list of `PRESENTATION_DECISIONS.md` (2026-10-09: bias / coverage vs K; role switch for five pairs; K × P heatmaps; E1–E3 and PCA / LEACE). The pre-result slice (W = 30, α = 0.5, γ = 1, φ_A = 0) is unchanged. The pre-result figures stay available as supplementary items (`SUPPLEMENT_INDEX.md`) |
| Figure 1 | Five panels (sets as parallel branches from the 278-case set, design and causal diagram, arm × covariate matrix, estimand / estimator, workflow with automatic commits and the OSF-registered exploratory analyses). Dates and OSF identifiers from the fact base and `main_repository_key_commits.md`; commit hashes left to the Methods. 190 × 162 mm |
| Figure 2A | Grouped forest; P1 and P2 families in two facets of equal physical width with free horizontal scales (P1 means ≈ 2, P2 means ≈ 0.05); within a family row the four sets are offset vertically (primary on top). Navy = primary set because only it enters verdicts (inferential role, template §2-3); sensitivity sets in gray with distinct open shapes. Missing set × family combinations are structural and omitted (caption) |
| Figure 2B | Exactly the task element: SITE vs NV and ORACLE vs ORACLE−C at the slice; K on a log axis; one line per P with marker + line-style coding. Orientation: without C − with C for every cell, as in the committed pre-result plotting code (`make_figures.py` `contrast`); the K = 1, P = 0 cell is the P2 cell (sign note in the caption). The FM, REF pairs at the slice remain in the results-report figures (Supplement) |
| Figure 3 | Three separate axes: (A) step-5 E3-site (278 / 158); (B) analysis-B transport; (C) analysis-B within-set refit. Linear probe navy (the prespecified criterion probe), MLP gray. Single-file E3-site is in Table 3 (the element names the 278- and 158-case sets) |
| Figure 4 | Exactly the task element: X1 vs step-6 k−C, X1 vs step-6 k, X2 vs step-6 k−C; groups P1b-FM and P2-FM; all 60 cells per panel in record cell order; y shared within a row. The slice group, the NV comparator and X2 vs step-6 k are in Supplementary Figure X / Table X (package). Group means are not drawn (they are in Supplementary Table X) |
| Table 1 | Three blocks under one caption: (A) sets (package `table1_data_sets.csv` + design cells and arms counted from `cell_metrics.csv`), (B) models (package `table2_models.csv`), (C) arms (protocol §8 text). The "source" column of the package table is left to `SOURCE_MAP.md` |
| Table 2 | One table with set sub-headers; all 18 non-exploratory family × set rows of `families.json`; status words derived mechanically ("Verdict: supported", "Not tested (§13)", "Reported separately"); family definitions in a footnote |
| Table 3 | All checks of `checks.json` for FM-P, FM-S, REF and FM-P-nat on the 278, 158 and single-file sets, reporting-only paths in their own block, and the X1 block last and separately labelled; PCA / LEACE variance retained is not in the element and stays in the results report §3 |
| Graphical abstract | 130 × 52 mm (5 × 13 cm aspect); numbers only from Table 2 (P1b-SITE 2.198, P2-SITE 0.052, same strings); the X1 block is dashed and labelled EXPLORATORY with no numbers |
| Rounding | 3 decimals (the committed reports' rounding), true minus sign; one formatting function (`f3`) for Tables 2–3 and the graphical abstract; shares 2 decimals |
| Fonts | Arial only (checked with `pdffonts`); gray text never lighter than #4D4D4D |

## 5. Claim ceilings applied (fact base §7–9)

No "harm", no "mechanism"; D and Δ described as dimensionless relative differences in absolute bias; Δ = X arm − step-6
arm (negative = smaller |bias|); verdicts as "consistent with the theory-motivated direction" within the constructed DGP;
E3-site wording "no longer exceeds the prespecified linear site-encoding boundary"; X: "exploratory; no verdict; cannot
restore P1b-FM/P2-FM; nonlinear site information remains after X1; X2 changes do not show that erasure caused a
difference"; B: "locates where the judgement changes; does not identify why".
