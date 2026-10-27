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

## 6. v3 revision (2026-10-27; task `CC_TASK_JBI_figures_tables_v3.md`, base commit `ee3b19f`)

Made after all results were known, by the same rules (no number changed, nothing selected, exploratory never in a
confirmatory panel, interval definitions of §3, claim ceilings of §5). Old files are kept unchanged; revised files carry
the suffix `_v2` (figures in `figures_v2/`). `SS_DS203_JBI_manuscript_plan_v3.md` is still absent from the work folder
and from the Mac (searched again); the task text was followed.

| # | Change | Reason / rule | What is shown (nothing hidden) |
|---|---|---|---|
| 1 | **New Figure 3: per-cell D against K by W (0, 5, 30), SITE vs NV and ORACLE vs ORACLE−C, α = 0.5, γ = 1, φ_A = 0, primary set (72 values; replaces v2 Figure 2B)** | At the pre-result slice (W = 30) the per-cell D is near zero, whereas at W = 0 it is large and positive; protocol §12.1 anticipated that pre-window history can break the direction, which is why P1b is defined on W = 0 cells (§12.2). The figure shows the W dimension only | Row (C) W = 30 is the unchanged pre-result slice; rows (A) and (B) add W only (α, γ fixed at the slice values); every K × P cell of each row is drawn; all other α and γ values remain in Supplementary Figure S1. Canonical `w_history_D.json` with the four task anchors (8.734, −0.044, 10.512, 0.071; exact values in `validation.json`); 14 of the 72 cells belong to a family and reproduce `families.json` D_j exactly. No interval (none exists for single cells) |
| 2 | Template §2-1 sizes in every figure: tick 14, axis label 15, panel label 16 pt (schematic: body 14, headings 15, panel labels 16; graphical abstract ≥ 10 pt at 130 mm) | task v3 §3 priority 2 | All figures reached the sizes; content was reduced instead of the font (Figure 1) and layouts were re-stacked: Figure 2 facets stacked vertically; Figure 3 x tick labels only on the bottom row (same K axis); Figure 4 (A) with the key on the first row, (B) (C) on the second; Figure 5 row titles above the rows. Heights 148–232 mm at 190 mm width |
| 3 | Figure 1: panel (D) removed (estimand, estimator, representations: Methods); (B) cut to the time structure and the causal diagram (the lines with the grid values, cell counts, replicate count and site-loading permutation were removed; they are in Methods); per-centre counts kept for the 278- and 158-case sets only (the others are in Table 1); workflow boxes shortened to three lines (dates and OSF identifiers kept; "73,200 units" and the step-6 start date dropped, the latter equals the step-5 record date) | reduce content rather than font size | Removed items are in Methods / Table 1 |
| 4 | Figure 4 key built from the drawn objects: marker, vertical bar (two-sided 95% interval, own entry), short horizontal tick (one-sided upper bound), dashed and dotted lines; checked object by object (`verify_plotted_v2.m`) | legend ↔ plot (task v3 §3) | — |
| 5 | Figure 5: P1b-FM cells re-ordered by (P, K, α, γ) so that the P = 5 and P = 30 blocks are contiguous and labelled; light separators between the K sub-blocks (K labels at 14 pt are wider than a 6-cell block, so the K order is stated in the caption); P2-FM in cell order with separators between W sub-blocks | readable cell order (task v3 §3); the order uses design factors only, not values | All 60 cells per panel, as before; canonical `x_cells_order_v3.json` |
| 6 | Graphical abstract: two-row layout (confirmatory row; erasure and X1 row) plus one descriptive line; wording per task (evaluation; "no prior action history (W = 0)"; "slightly higher"; the W = 30 line verbatim) | ≥ 10 pt at 130 mm | Numbers: 2.198 and 0.052 (Table 2) only; "278-case" removed (not a Table 2 number) |
| 7 | Table 1: arms block removed (Figure 1C); "Selection" column moved into a footnote; Table 2 compacted (column widths, shorter footnotes); both on one A4 landscape page at 11 pt with 15 mm top / bottom margins (left / right 25 mm) | one page at 11 pt (task v3 §3) | All rows and all footnote content kept; the margin is a typesetting choice of the table file only |
| 8 | Table S5 = old Table 3 renamed (document XML identical apart from "Table S5."; CSV identical) | task v3 §1 | — |

Conflicts (v3) and resolution:

| Conflict | Resolution |
|---|---|
| Template §2-1 sizes (14 / 15 / 16 pt) vs a 190 mm width with many panels | Reduce content and re-stack layouts; no figure needed a smaller size; heights up to 232 mm (Figure 1) |
| Marker targets (template §5-C, absolute mm) vs larger fonts | Markers kept at the template targets (filled 0.97–1.14 mm, open 1.18–1.32 mm); not enlarged to match the fonts |
| Table template margins (≈ 2.5 cm, manuscript body) vs one page at 11 pt | 15 mm top / bottom margins in the two table files |
| Figure 3 y label once per row at 15 pt (51.6 mm) | Panels 52.5 mm high so that the label fits each row |

## 7. v4 revision (2026-10-27; task `CC_TASK_JBI_figures_tables_v4.md`, base commit `480312d`)

Made after all results were known, by the same rules (v2 §0–§2, v3 §0: canonical provenance, no new number, no
selection, exploratory separation, the interval definitions of §3, the claim ceilings of §5, templates). Three items
only: markers, heights, Table 2. Revised files carry the suffix `_v3` (figures in `figures_v3/`); every earlier file is
unchanged. Not revised (no `_v3` file): Figure 5, Tables 1 and S5, the graphical abstract, `CAPTIONS_v2.md`. Measured
values: `qa/MEASUREMENT_REPORT_v3.md`.

| # | Change | Rule / reason | What is shown (nothing hidden) |
|---|---|---|---|
| 1 | Markers of Figures 2, 3 and 4 enlarged: every MarkerSize of v2 multiplied by one factor per figure (Figures 2 and 4: 3.65 / 2.6 = 1.404; Figure 3: 3.35 / 2.2 = 1.523) so that the filled circle is 1.50 mm outside; edge widths, colours, offsets and every other setting as v2 | task v4 §1.1; template §5-C allows hollow / angular markers a different nominal size, so their v2 nominal ratios to the circle are kept (visual equivalence as accepted in v3) | Outer sizes before → after (PDF paths; `qa/markers_v4.json`): Figure 2 navy circle 1.129 → 1.499, open square 1.283 → 1.695, open triangle 1.321 × 1.180 → 1.748 × 1.549, open diamond 1.182 × 1.484 → 1.552 × 1.977 mm; Figure 3 (all filled) circle 1.094 → 1.499, square 1.143 → 1.575, triangle 1.293 × 1.162 → 1.805 × 1.605 mm; Figure 4 navy circle 1.129 → 1.499, open square 1.283 → 1.695 mm. Same number of markers at the same x centres (y within 0.07 mm: a triangle grows about its anchor); in Figures 2 and 4 every text span (text, font, size, position to 0.01 mm) and every non-marker path are identical to v2, in Figure 3 every text, font and size and the number of each kind of path (`qa/v4_unchanged.json`) |
| 2 | Figure 5 not changed | Task v4 §1.1 "5 if the same applies": it does not — 60 cells share a 52-mm panel (pitch 0.765 mm); a 1.5-mm marker would overlap its neighbour by 0.735 mm (reaching almost to the neighbour's centre) and would hide 180 of the 540 intervals completely (122 at the current 0.97 mm), against template §5-C ("individual outlines remain distinguishable") | `Figure_5_v2` stays the current Figure 5 (filled circle 0.97 mm, within the template's filled target 0.95–1.15 mm) |
| 3 | Figure 1 height 232 → 219 mm, every font size unchanged (14 / 15 / 16 pt) | task v4 §1.2: spacing between the panels ((A)–(B) 3 → 2.5 mm, (B)–(C) 4.5 → 2.5 mm, (C)–(D) 3.5 → 2.5 mm), inside (A) (heading to the first box 2 mm less; gaps between the set boxes 2.5–2.75 → 1.5 mm, the representation box re-centred on the stack) and inside (D) (heading to the steps 1 mm less; steps to the exploratory boxes 4 → 3.5 mm), bottom margin 4 → 1.5 mm | Same 112 shapes, texts, sizes, colours, x positions, widths and heights; only y positions changed, and the four vertical connectors that join boxes whose spacing changed are shorter (35 → 31.5, 6.75 → 5.5, 4 → 3.5, 4 → 3.5 mm); no text overlap or near pair (< 0.5 mm) |
| 4 | Figure 3 height 228.25 → 219.07 mm (PDF page; canvas 21.9 cm) | task v4 §1.2: row height reduced moderately — axes 52.5 → 49.5 mm, all gaps, margins, ticks and the free y scales (three labelled ticks per row) unchanged | The y label (51.6 mm at 15 pt) now runs 1.0 mm past each end of its 49.5-mm axis; it stays inside its row band (0.9 mm from the row title's glyph box, 9.4 mm from the next row's label). This supersedes the v3 resolution "panels 52.5 mm high so that the label fits each row" (§6), because the label cannot fit at ≤ 220 mm without a smaller font or tighter row gaps, and tighter gaps would make the row titles ambiguous (template §5-B) |
| 5 | Table 2: column "Direction rule" → "Locked rule outcome" with footnote a ("Mechanical outcome of the §12.3 aggregation in every row, qualified by the Status column (not tested; reported separately)"), followed by the unchanged direction-rule text | task v4 §1.3 (a) | Column values unchanged |
| 6 | Table 2: the primary-set P2-FM lower bound, exactly −0.00028834867676637266 (`families.json['primary:P2-FM']['ci_lo']`; 3 decimals would show −0.000), displayed as −0.0003 with footnote b ("Lower bound shown with 4 decimals so that its sign is visible …; all other values have 3 decimals") | task v4 §1.3 (b); the number of decimals is the smallest at which the rounded value is non-zero, chosen by rule in `freeze.py` (`sign_decimals`) and frozen in `canonical/validation.json` → `v4_table2_sign_decimals` with the exact value and its check against `families.json` | No other value of Table 2 rounds to −0.000; CSV: only the heading and this cell differ from `Table_2_v2.csv`; still one A4 landscape page at 11 pt |
| 7 | **Finding and fix: TIF of the data figures.** MATLAB's raster export at 1,200 dpi renders in 4,000-px tiles and clips a marker that straddles a tile boundary: the TIF loses part of the marker while the vector PDF is correct. Affected earlier TIFs (one marker each; files left unchanged): `Figure_3` (v1), `Figure_2_v2` (the W = 0 square of P2-SITE lost its left side), `Figure_4_v2`. `print -dtiff`, `print -image`, `-opengl` and `exportgraphics` all showed it. The v3 TIFs of Figures 2–4 are MATLAB's own vector PDF rasterised by poppler at 1,200 dpi (`figures/common/jbi_export_v4.m`) | template §7-3 (marker outlines must survive in the submitted raster) | TIF ↔ PDF: every marker complete and the whole image identical in ink (`qa/tif_markers_*.json`, `qa/tif_vs_pdf_*.json`); TIF size = PDF page (189.80 mm wide) |

Conflicts (v4) and resolution:

| Conflict | Resolution |
|---|---|
| Template §0-3 / §6 (data-figure TIF straight from MATLAB) vs the tile clipping of every MATLAB raster export path | TIF = the MATLAB vector PDF rasterised by poppler (`pdftoppm -r 1200 -tiff -tiffcompression lzw`), inside the `.m` (one source: `.fig` → PDF → TIF; no manual tool; Figure 1 already used this route). Recorded as a deviation from the template's wording; the template's intent (no PowerPoint / Photoshop, same source for PDF and TIF) is kept |
| v3 decision "Figure 3 panels 52.5 mm so that the y label fits" vs v4 "≤ 220 mm without reducing a font size" | Row height reduced as the task says; the 1.0-mm label overhang is measured and recorded (row 4 above) |
| Blinding scan (byte regex) vs LZW pixel data | The regex matched two random byte strings inside the compressed pixel strips of `Figure_3_v3.tif` ("a@l.EP", "a@l.Aqjb"); for the v3 outputs the scan reads every byte of a TIF except its pixel strips (header, IFDs, tag values) |
| CAPTIONS update only if a caption must mention the extra decimals | No caption needs it (footnote b carries it), so no `CAPTIONS_v3.md`; the caption texts of `CAPTIONS_v2.md` apply to the `_v3` files unchanged; its Table 2 entry points to the footnotes, which are now in `tables/Table_2_v3.docx` (footnotes a and b added) |
| v3 measurement report grouped the Figure 2 diamond with the squares ("other", median 1.283 mm) | Per-shape sizes measured again for the before values (`qa_markers_v4.py`: diamond 1.182 × 1.484 mm); the v3 report is left as recorded |

## 8. v5 revision (2026-10-27; task `CC_TASK_JBI_figures_tables_v5.md`, base commit `355334e`)

Made after all results were known, by the same rules (v2 §0–§2, v3 §0) and with the poppler TIF of §7 for every TIF.
Two changes: (1) the bias / coverage figure is reinstated in the main text; (2) the figures are renumbered to the order
of first citation in Results (the Results text cites the erasure figure first, step-5 E3 in Section 4.1). A complete
set with the suffix `_v4` is in `figures_v4/Figure_1..6/`; every earlier file is unchanged. Tables 1 (v2), 2 (v3), S5
(v2) and the graphical abstract (v2) are unchanged and not renamed. Captions: `CAPTIONS_v4.md`.

| New number (files `Figure_N_v4.*`) | Content | Source file | How |
|---|---|---|---|
| Figure 1 | Study design | `figures_v3/Figure_1/Figure_1_v3.*` | byte copy (.pdf, .pptx, .tif, .js) |
| Figure 2 | Erasure evaluation (A step-5 E3; B, C exploratory B) | `figures_v3/Figure_4/Figure_4_v3.*` | byte copy (.fig, .pdf, .tif, .m) |
| Figure 3 | Confirmatory families (forest) | `figures_v3/Figure_2/Figure_2_v3.*` | byte copy |
| Figure 4 | Dependence on prior action history | `figures_v3/Figure_3/Figure_3_v3.*` | byte copy |
| Figure 5 | NEW: relative bias and coverage at the slice | `figures_v4/Figure_5/make_Figure_5_v4.m` | built from `canonical/fig5_bias_coverage.json` |
| Figure 6 | Exploratory X1/X2 | `figures_v2/Figure_5/Figure_5_v2.*` | byte copy (.fig, .pdf, .m); TIF from its PDF by poppler |

Figure 5 (task v5 §1). Reason: it is the pre-result main-text Figure 1 of `PRESENTATION_DECISIONS.md` (2026-10-09,
decision 1: relative bias and 95% interval coverage against K, by arm, one column per P, at the slice), which the JBI
main text had not shown since v2 (§4); reinstating it restores a decision fixed before any result existed. Content =
the package rendering `fig1_bias_coverage_vs_K.pdf` (definition unchanged: all 12 arms, the 12 K × P cells of the slice,
`rel_bias` and `coverage` of `cell_metrics.csv`; 288 values; anchors NV K = 1, P = 0 rel_bias 0.10283144587487024 and
coverage 0.85, FULL K = 1, P = 30 rel_bias 0.33023840439297236, ORACLE−C K = 2, P = 0 coverage 0.97, in
`validation.json`). Definitions confirmed in the code: rel_bias = mean(estimate − truth) / mean truth and coverage =
share of replicates with ci_lo ≤ truth ≤ ci_hi (`grid.py` `cell_metrics`); ci = estimate ± z_0.975 · SE with SE =
sd(IF)/√n of the contrast influence function (`sdr.py`). No interval is drawn for these metrics (none exists). Choices
made after the results:

| Choice | Reason |
|---|---|
| Rows (A) relative bias in %, (B) coverage; columns P = 0, 5, 30; x = K on a log axis (0.8–19); y shared within a row (bias −30 to 205 %, coverage −0.03 to 1.03); reference lines 0 and 0.95 (`#8A8A8A` dotted) | task v5 §1; template §5-B (equal widths) |
| Four groups by line style and shade — NV / SITE dashed `#6B6B6B`; the seven representation arms solid `#8A8A8A`; ORACLE−C / ORACLE dash-dot navy; FULL dotted `#4D4D4D` — and arms within a group by marker (NV / SITE ▽; FM-P ○, FM-S □, REF △, FM-P-nat pentagram; ORACLE pair ◇; FULL hexagram); filled marker = the arm has site information (C or a site-retaining representation), open = it has none (NV, the −C arms, ORACLE−C) | task v5 §1; the fill rule makes every with/without-C pair of the protocol (SITE/NV, FM-P/FM-P−C, FM-S/FM-S−C, REF/REF−C, ORACLE/ORACLE−C) a filled/open pair of one shape |
| Navy for ORACLE−C / ORACLE | template §2-3 (prominence = inferential role): the exact-state arms are the comparison that isolates the role of C when the state is known (P1a, P2-ORACLE); not chosen for their values. The representation arms get the lightest data shade because seven near-identical lines in a darker shade would hide the other groups; their markers keep dark edges so that each stays visible |
| Markers small with edges, no jitter: filled circle 1.31 mm outside (edge 0.5 pt `#1A1A1A`), open circle 1.41 mm (edge 0.8 pt in the group colour); other shapes 1.30–1.79 mm (`qa/markers_v5.json`); line and marker drawn as separate objects so that the marker edge (0.5 pt) can be thinner than the line | task v5 §1 ("the near-overlap of arms within a group is itself information"); with a 0.8-pt black edge the 1.2-mm markers looked black and hid the group shade (first render) |
| Draw order: representation arms, NV / SITE, FULL, ORACLE pair (navy on top) | the smallest groups stay visible where groups cross |
| Key of 12 entries in five columns under the panels (one column per group; the seven representation arms in two), built from the plotted line and marker objects | legend ↔ plot (template §5-C); MATLAB's legend cannot fill uneven columns without dummy entries |
| 189.79 × 184.15 mm | ≤ 220 mm at 14 / 15 / 16 pt (task v5 §1) |

Conflicts (v5) and resolution:

| Conflict | Resolution |
|---|---|
| Byte identity of the renumbered `.m` / `.js` with their sources vs template §4-0 (the `.m` regenerates the figure) | The copied scripts are byte-identical, so each re-creates its source-named outputs (e.g. `make_Figure_2_v4.m` writes `Figure_4_v3.*`); the renumbered files are produced by `scripts/renumber_v5.py` from the sources, whose scripts remain the rendering source of truth. Recorded in the script header and here |
| Byte identity of the Figure 6 TIF with `Figure_5_v2.tif` vs "the poppler TIF is used for every TIF" | The poppler rule wins: `Figure_6_v4.tif` is rasterised from the byte-copied `Figure_6_v4.pdf` (ink identical to the PDF, `qa/tif_vs_pdf_Figure_6_v4.json`); its `.fig`, `.pdf` and `.m` are byte copies. `Figure_5_v2.tif` had no clipped marker (§7), so the change is the export route only |
| Pre-result decision 1 names the figure "Figure 1"; it is now Figure 5 | Numbering follows citation order (task v5 §2); the content and slice are those of the decision |

## 9. v6: supplementary figures and tables (2026-10-27; task `CC_TASK_JBI_supplement_v6.md`, base commit `ef32e5c`)

Made after all results were known, by the same rules (v2 §0–§2, v3 §0; poppler TIF). The main v5 set is not touched.
Outputs: `figures_supp_v1/Figure_S1..S6/` (S4 not produced), `tables/Table_S1_v1..S6_v1.*`, `CAPTIONS_supplement_v1.md`.
Values: `canonical_supplement/` written by `scripts/freeze_supplement.py` (package inputs guarded by the manifest and,
where recorded, by the generating step's hash; the main `canonical/` is read with its hash guard and not written).

| Item | Status |
|---|---|
| Figure S1 (D, 5 pairs × 240 cells, 10 pages) | built; 1,200 values; each family's cells reproduce `families.json` D_j exactly and its mean equals D̄ (P1a 1.925, P1b-SITE 2.198, P1b-FM 0.594, P2-SITE 0.052, P2-FM 0.005, P2-ORACLE 0.042); the 72 cells of main Figure 4 and the 24 slice cells of `fig2B_slice_D` are identical |
| Figures S2, S3 (12 arms × 240 cells, 24 pages each) | built; 2,880 values each; the 144 slice rows of main Figure 5 identical; `report_cells.csv` agrees with `cell_metrics.csv` within 8.2 × 10⁻¹³ relative (re-serialisation; display strings identical; coverage identical) — values from `cell_metrics.csv` |
| Figure S4 | built after the investigator provided `mask_check.json` (2026-10-27; copied to `inputs/`; SHA-256 81c8eb46…58d5 = the blob hash recorded in the package `SUPPLEMENT_20261020/SOURCES.md` for the step-4 record `8d4c61a`); 720 points (4 centres × 180); n_frames, ρ_c, min ρ_c and r equal `tableS4_mask_check.csv`; for centres 3–5 ρ_c is the last profile point (asserted). Before the file was provided the figure was SOURCE MISSING (not in the package; values were not read from the rendered `figS4_mask_profiles.pdf`) |
| Figure S5 (4 pages) | built; 756 values: the slice group of X1 k−C vs step-6 k−C, X1 k−C vs step-6 k and X2 k−C vs step-6 k−C (their other groups are in main Figure 6), and every group of X1 vs step-6 NV, X2 vs step-6 NV and X2 vs step-6 k; no cell of main Figure 6 repeated (asserted) |
| Figure S6 | built; the 36 rows of `b_main.csv`, identical to main Figure 2 (B), (C) (asserted), arranged by evaluation set as the package figure |
| Tables S1–S6 | built; S2 = Table_S5_v2 rebuilt with the number S2 (document XML identical apart from "Table S2."; CSV identical) |
| `Supplementary_Material_v1.docx` | built in `supplementary/` from the draft provided by the investigator (`inputs/JBI_Supplementary_Methods_draft_v2.md`, SHA-256 7d0e1f7b…1843), Tables S1–S6 and Figures S1–S6; 98 pages in the LibreOffice rendering; QA `qa/supplementary_docx_v1.json` |

Choices made after the results:

| Choice | Reason |
|---|---|
| Heatmap pages (S1–S3): A4 portrait (595 × 842 pt), layout of the package figures (rows α × γ, columns W, panel rows K, panel columns P); the 24 φ_A = 0.5 cells on their own page in the W = 5 column with the same cell size | pre-result decision 2; same reading on every page |
| Type scale on the heatmap pages: cell values 11 pt, tick labels 12, axis and row/column labels 13, page titles 14 pt bold (measured minimum 11 pt) | template §2-1 (14 / 15 / 16 pt) does not fit 216 values per A4 page; the task accepted a relative scale with a 9-pt floor, which was not needed. Recorded as a template conflict |
| Shading by discrete classes on round boundaries (`figures/common/jbi_ramp_v6.m`): D diverging — white for |D| < 0.01, navy tints (to 60% navy) for D > 0 and gray tints (to #8A8A8A) for D < 0 at 0.01, 0.05, 0.1, 0.5, 1; relative bias sequential gray on |relative bias| at 5, 10, 25, 50, 100, 200%; coverage sequential gray, darker for lower coverage, at 0.90, 0.75, 0.50, 0.25 | classes are readable without a colour scale (steps in lightness, colour-blind safe; the sign of D and of relative bias is also in the cell text); boundaries are round numbers, not fitted to the data; the darkest shades keep #1A1A1A text at contrast ≥ 4.5; one scale for all pages of a figure. Every class is shown in each page's key (a full scale, not series entries) |
| Cell text: D with 3 decimals and sign, relative bias in % with one decimal and sign, coverage with 2 decimals | task v6 §2; display strings frozen in `canonical_supplement` by Python. 12 D values and 4 relative-bias values round to ±0 (shown as +0.000 / −0.000 / ±0.0); coverage values are multiples of 0.005 and 2 decimals follow Python's formatting of the stored value (exact values in the CSV) |
| Tables: committed rounding (3 decimals, true minus sign), including −0.000 where a negative value rounds to zero (Table S4: S X1 ΔAUC, REF ΔAUC lower bounds; noted in its footnote); Table S1 values verbatim (exact grid values, as the committed table) | task v6 §4 ("rounding 3 d.p. as the committed reports"; Table S2 a byte copy). The v4 rule for Table 2 (decimals needed to show the sign) is therefore not applied in the supplement — open for the investigator |
| Table S5: the 36 judgement statements as a column, each statement verbatim at the later set of its pair (S2: S1→S2; S3: S2→S3 and S1→S3) | task v6 §4 ("as a column or footnote") |
| Figure S5: page 1 a 3 × 3 grid (12 slice cells per panel); pages 2–4 one full-width panel per k (72 cells at 1.8 mm pitch) | the 72-cell groups would be 0.64 mm apart in a 3 × 3 grid; encoding, separators and cell order as main Figure 6 |
| Figures S5, S6 at the template sizes (14 / 15 / 16 pt), 190 mm wide; S6 markers as main Figure 2 (v4 sizes) | task v6 §3 |
| TIF: S1–S3 one 600-dpi TIF per page; S5 one 1,200-dpi TIF per page; S6 1,200 dpi; all rasterised from the vector PDF by poppler and identical to a fresh rendering of the same page | multi-page figures; 58 A4 pages at 1,200 dpi would be several GB; 600 dpi is the Word-paste resolution of the template |
| The subscript A of φ_A in the heatmap page titles touches its base glyph; the text-overlap check excludes that pair only | TeX subscript by design |

Figure S4 (house style instead of the package's orange): one panel per centre (A)–(D) with free vertical scales; navy
profile line; ρ_c solid #4D4D4D; r = 0.45 dashed #4D4D4D; frame counts in Table S1, not in the figure; key from the drawn
lines in two rows (the three labels do not fit one row at 14 pt). 189.79 × 160.16 mm.

Supplementary Material document (`scripts/build_supplementary_material_v1.py`):

| Choice | Reason |
|---|---|
| Order: Supplementary Methods (SM 1–7), Tables S1–S6, Figures S1–S6 | task v6 §5 |
| Normal style only, bold headings of the same size, no Heading / list styles or automatic numbering; bullets as "•" (level 1), "–" (2), "·" (3) with hanging indents, numbered items as literal numbers; Arial 11 pt; prose line spacing 1.5; 2.5-cm margins; continuous page numbers | manuscript template Word rules (the draft's bullet lists may be kept, task v6 §5) |
| Tables: the body of each `Table_Sn_v1.docx` copied element by element into its own section (source orientation and margins; single spacing of the table template) | captions and footnotes exactly as the table files |
| Figure sections with 10-mm margins; Figures S4–S6 pasted at 100% (189.82 mm) as 600-dpi TIF rasterised from the vector PDF; each A4 page of Figures S1–S3 pasted at the page width (190 mm) from its 600-dpi page TIF, embedded as lossless PNG (pixels identical, asserted; 'L' for the gray S2/S3 pages); each figure's caption first | task v6 §5; PNG keeps the document at 22.8 MB instead of about 170 MB with TIF |
| Draft conversion: the HTML comment (editorial note for the auditor) not rendered; " — draft v2" dropped from the title; Markdown markup rendered; "∈" → "in", ⌈x⌉ → ceil(x), ⌊x⌋ → floor(x), Unicode super/subscripts → Word super/subscript runs, x_y identifiers → base + subscript (code spans verbatim); five references renumbered to the v6 items ("Table S4" (mask check) → Table S1; "Tables X, X-E3, B, B-sens" → Tables S3–S6; "Figures X, B" → Figures S5, S6). Every other character verbatim; the [REF: …] (15) and [TO FILL] (1) placeholders are kept for the investigator | Arial has no ∈, ⌈⌉⌊⌋ or superscript minus (as main conflict #10); final numbering (task v6 §1). Checked: the docx methods text equals the draft after these rules (`qa/supplementary_docx_v1.json`) |
| QA rendering: LibreOffice PDF export without image downsampling (`ReduceImageResolution` false) | the default export reduces images to 300 dpi |
| Blinding scan of the document: the AI-use declaration of SM 1 ("… independently evaluated with ChatGPT (OpenAI), as declared in the main text") is excluded from the AI-trace count (its two matches); no other match | the declaration is required content (manuscript template, AI-use disclosure), not a tool trace; it should be checked against the journal's double-blind rules by the investigator |

Cross-references in the main set that the new supplementary numbering changes (the main set is not edited in v6):
"Supplementary Table S5" (Table 2 v3 footnote; `CAPTIONS_v4.md`, Figure 6) → **Table S2**; "Supplementary Figure X and
Table X" (`CAPTIONS_v4.md`, Figure 6) → **Figure S5 and Table S3**; "Supplementary Figure S1" and "Supplementary Figures S2
and S3" are unchanged.

## 10. v7 revision (2026-10-27; task `CC_TASK_JBI_GA_and_tables_v7.md`, base commit `8e5e882`)

Mandatory revisions from the content audit; nothing else in the figure set is touched (the v6 supplement files, the
main v5 set and every earlier file are unchanged).

| # | Change | Rule / reason | What is shown |
|---|---|---|---|
| 1 | Graphical abstract v3 (`graphical_abstract/Graphical_abstract_v3.*`, from `make_Graphical_abstract_v3.js` = the v2 script with exactly two text changes): the erasure box now reads "Linear site erasure / (prespecified linear-probe criterion) / Fitting set (278): met / Analysis windows (158): not met / Representation families not tested"; the bottom line reads "At the prespecified α = 0.5, γ = 1 slice, 30 prior action steps largely attenuated the site difference (descriptive)" | content audit (task v7 §1) | Title, confirmatory boxes ("No prior action history (W = 0)", "slightly higher"), exploratory box and numbers unchanged; numbers in the GA all canonical (0, 1, 30, 0.5, 158, 278, 0.052, 2.198). Layout only as needed at the same sizes: the erasure box 1.5 mm wider (its line "(prespecified linear-probe criterion)" is 54.7 mm at 10 pt), the exploratory box 1.5 mm narrower (longest line 61.2 mm), the bottom line on two lines, canvas 130 × 56 mm (v2: 52 mm; limit 60) |
| 2 | Supplementary Tables S3 and S4 v2: the five cells shown as −0.000 now show the decimals needed for their sign (Table 2 rule of v4) with footnote a; S4's v1 sentence about −0.000 removed | task v7 §2 | Exact values read from the package CSVs (S4 also equal to `checks.json` / `x1_e3.json`), recorded in `canonical_supplement/validation.json` → `v7_negative_zero_S3_S4`: S3 X2 FM-S−C vs step-6 FM-S−C, P2-FM, mean Δ −0.0004556214274979232 → −0.0005; S3 X2 REF−C vs step-6 REF−C, P1b-FM, mean Δ −0.00026330432994649554 → −0.0003; S4 E2, S, X1 after X1 removal, ΔAUC −0.00046687915783594214 → −0.0005; S4 E2, REF, step 5 before removal, CI lower bound −0.0004872832492350014 → −0.0005; S4 E2, REF, step 5 after protocol removal, CI lower bound −0.0003989757726410605 → −0.0004. Only these cells and the footnotes differ from v1 (`qa/tables_qa_supp_v2.json`); page counts unchanged (2 / 2) |
| 3 | `CAPTIONS_supplement_v2.md` | the Table S3 / S4 entries point to the v2 files and name footnote a (the S4 entry listed "−0.000") | caption texts otherwise unchanged |

Other "−0.000" strings in Tables S1–S6 (listed, not changed in v7): Table S2 (= Table_S5_v2) shows the same three S4
quantities — S X1 E2 ΔAUC after X1 removal (−0.00046687915783594214), REF E2 lower bounds before and after protocol
removal (−0.0004872832492350014, −0.0003989757726410605); full-precision sources exist (`canonical/table3.json` ←
`checks.json`, `x1_e3.json`), recorded in `validation.json` → `v7_negative_zero_other_tables`. Table S2 is outside
task v7, so it still shows −0.000 for these three values (now displayed with 4 decimals in Table S4).

Not regenerated in v7: `supplementary/Supplementary_Material_v1.docx` and the auditor package still contain the v1
Tables S3 and S4.

## 11. v8 revision (2026-10-27; task `CC_TASK_JBI_tableS2_and_handoff_v8.md`, base commit `600988d`)

Nothing else in the figure set is touched; Table S2 v1 and every other file are unchanged.

| # | Change | Rule / reason | What is shown |
|---|---|---|---|
| 1 | Supplementary Table S2 v2 (`tables/Table_S2_v2.*`): the three cells shown as −0.000 (the same quantities as three cells of Table S4 v2) displayed as in Table S4 v2, with the Table S4 footnote wording | negative-zero consistency between S2 and S4 (task v8 §1); Table 2 rule of v4 | Exact values read from the package and checked equal to `canonical/table3.json` (Table S2's source) and to the Table S4 v2 records; recorded in `canonical_supplement/validation.json` → `v8_negative_zero_S2`: REF, E2 before removal, CI lower bound −0.0004872832492350014 (`checks.json` REF.E2_primary.ci_lo) → −0.0005; REF, E2 after protocol removal, CI lower bound −0.0003989757726410605 (`checks.json` REF.E2_primary_after_removal.ci_lo) → −0.0004; S, X1 E2 after X1 removal, ΔAUC −0.00046687915783594214 (`x1_e3.json` S.E2_primary_after_removal_X1.delta_auc) → −0.0005. Each display is identical in S2 v2 and S4 v2. Only these cells and one added footnote differ from Table S2 v1; page count unchanged (3) |
| 2 | Footnote letter j in Table S2 v2 (Table S4 v2 uses a) | Table S2 already uses the letters a–i (a = the single-file set); the same footnote text under the next free letter avoids a clash of meanings | footnote j: "Shown with 4 decimals so that its sign is visible (3 decimals would display −0.000); all other values have 3 decimals." |
| 3 | `CAPTIONS_supplement_v3.md` | the Table S2 entry points to `Table_S2_v2.docx` and names footnote j; the title and the version note name v3; nothing else changed | — |
| 4 | Handoff package for the auditor's Word update (`HANDOFF_JBI_word_update_v2_<date-time>.zip`) | task v8 §2 | the manuscript v6 texts provided by the investigator (with SHA-256), GA v3, Tables S2–S4 v2, `CAPTIONS_supplement_v3.md`, `validation.json` and sections 10–11 of this record |

After v8 no "−0.000" remains in the current Tables S1–S6 (`Table_S1_v1`, `Table_S2_v2`, `Table_S3_v2`, `Table_S4_v2`,
`Table_S5_v1`, `Table_S6_v1`; `qa/tables_qa_supp_v2.json`). `build_tables.table3` gained an `extra_notes` argument; with its
default it still reproduces Table_S2_v1 exactly (document XML and CSV, checked).

Observed in the investigator's `JBI_Supplementary_Methods_draft_v4.md` (copied unchanged into the handoff): compared with
draft v3 it changes the title (v3 → v4) and five lines with the label corrections (Table S4 → S1 twice; X / X-E3 / B /
B-sens / Figures X, B → S3–S6 / S5, S6 three times); in three of these lines it also adds or replaces a parenthesis
("; renumbered for submission"; "(and main Figure 6)" and "(and main Figure 2B, C)" in place of
"(`SUPPLEMENT_20261020/`)"). No other line differs.
