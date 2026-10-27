# Measurement report (template §7; measured from the exported files)

| figure | PDF page (mm) | TIF (px @ dpi = mm) | text sizes (pt) | min (pt) | fonts embedded | raster objects | text overlaps / near (< 0.5 mm) | edge clearance < 0.3 mm |
|---|---|---|---|---|---|---|---|---|
| Figure_1 | 190.0 × 162.0 | [8977, 7654] @ 1200.0 = [190.01, 162.01] | [7.99, 9.01, 11.0] | 7.99 | BAAAAA+Arial-BoldMT yes; CAAAAA+ArialMT yes | 0 | 0 | 0 |
| Figure_2 | 189.79 × 112.18 | [8963, 5292] @ 1200.0 = [189.72, 112.01] | [8.0, 9.0, 10.0, 11.0] | 8.0 | ArialMT yes; Arial-BoldMT yes | 0 | 0 | 0 |
| Figure_3 | 189.79 × 87.84 | [8963, 4134] @ 1200.0 = [189.72, 87.5] | [9.0, 10.0, 11.0] | 9.0 | ArialMT yes; Arial-BoldMT yes | 0 | 0 | 0 |
| Figure_4 | 189.79 × 139.35 | [8963, 6567] @ 1200.0 = [189.72, 139.0] | [9.0, 10.0, 11.0] | 9.0 | ArialMT yes; Arial-BoldMT yes | 0 | 0 | 0 |
| Graphical_abstract | 130.0 × 52.0 | [6142, 2457] @ 1200.0 = [130.01, 52.01] | [7.0, 7.99, 9.01] | 7.0 | BAAAAA+Arial-BoldMT yes; CAAAAA+ArialMT yes | 0 | 0 | 0 |

## Marker sizes (outer size including the edge line; from PDF paths)

| figure | part | shape | colour | edge (pt) | n | outer w × h (mm, median) |
|---|---|---|---|---|---|---|
| Figure_2 | edge | circle | #1A1A1A | 0.6 | 5 | 1.129 × 1.129 |
| Figure_2 | edge | circle | #1A1A1A | 0.9 | 9 | 1.094 × 1.094 |
| Figure_2 | edge | other | #1A1A1A | 0.9 | 9 | 1.143 × 1.143 |
| Figure_2 | edge | other | #4D4D4D | 0.75 | 7 | 1.283 × 1.283 |
| Figure_2 | edge | triangle | #1A1A1A | 0.9 | 9 | 1.293 × 1.162 |
| Figure_2 | edge | triangle | #4D4D4D | 0.75 | 3 | 1.321 × 1.18 |
| Figure_3 | edge | circle | #1A1A1A | 0.6 | 25 | 1.129 × 1.129 |
| Figure_3 | edge | other | #4D4D4D | 0.75 | 25 | 1.283 × 1.283 |
| Figure_4 | edge | circle | #1A1A1A | 0.45 | 540 | 0.97 × 0.97 |

Filled markers (navy face, near-black edge): template target 0.95–1.15 mm; open / angular markers: 1.10–1.30 mm; hard minimum 0.8 mm. 'other' groups MATLAB's square and diamond edge paths.

## Plotted vs canonical (MATLAB, zero tolerance; `qa/plotted_vs_canonical.json`)

* Figure_2: PASS — 35 points with their intervals / bounds; mismatches 0; legend: ['P = 0 | P = 5 | P = 30', 'Primary set (n = 158) | W = 0 set (n = 204) | W = 5 set (n = 201) | Single-file set (n = 123)']
* Figure_3: PASS — 48 points with their intervals / bounds; mismatches 0; legend: Linear probe | MLP probe | One-sided 95% upper bound | Boundary 0.35 | Chance 0.25
* Figure_4: PASS — 540 points with their intervals / bounds; mismatches 0; legend: none (single series type; defined in caption)

## Schematic numbers (`qa/schematic_numbers.json`)

* Figure_1: 52 distinct numeric tokens; canonical 51, structural 1, unmatched 0
* Graphical_abstract: 4 distinct numeric tokens; canonical 4, structural 0, unmatched 0

## Tables (Word XML and LibreOffice PDF; `qa/tables_qa.json`)

| table | pages (A4 landscape) | horizontal rules per page | vertical rules | shading | fonts | run sizes (pt) | checks |
|---|---|---|---|---|---|---|---|
| Table_1 | 2 | [6, 3] | 0 | 0 + 0 | BAAAAA+Arial-BoldMT, CAAAAA+ArialMT | {'11.0': 158} | PASS (12) |
| Table_2 | 2 | [3, 0] | 0 | 0 + 0 | BAAAAA+Arial-BoldMT, CAAAAA+ArialMT | {'11.0': 179} | PASS (12) |
| Table_3 | 3 | [3, 2, 3] | 0 | 0 + 0 | BAAAAA+Arial-BoldMT, CAAAAA+ArialMT | {'11.0': 371} | PASS (12) |

PDF text at 6.4 pt in the tables = Word superscript / subscript runs (footnote markers, D_j, S_t) as rendered by LibreOffice (58 % of 11 pt); the runs themselves are 11 pt.

## Scientific / semantic QA (template §7-4)

| figure | n / denominator | interval (confirmed in code) | reference | scale | unit / direction | categories / N/A |
|---|---|---|---|---|---|---|
| Figure 1 | 278 / 158 / 204 / 201 / 123 cases and centre counts = Table 1 (A) | — | — | — | — | populations drawn as parallel branches (per-W eligibility), single-file nested in the primary set; arms = protocol §8 |
| Figure 2 (A) | cells per family 66 / 48 / 18 / 12 (sets 16–48 / 4–6) = Table 2; lower ≤ estimate ≤ upper asserted | paired replicate bootstrap of the family mean, cells fixed (grid.py) | 0 (difference) | linear; facets free, equal width (caption) | dimensionless; P1 without − with, P2 with − without (axis labels, caption) | set order primary, W = 0, W = 5, single-file; absent combinations omitted with reason; W0:P1a (exploratory) not drawn |
| Figure 2 (B) | 12 cells per pair = the pre-result slice | none exists (point values; caption) | 0 | log K axis (1, 2, 5, 15), linear D | dimensionless; without − with for all cells; P2 cell sign note | P = 0 / 5 / 30 by marker and line style |
| Figure 3 | 278 / 158 cases (S1 278; S2, S3 158) = checks.json, b_main.csv | site-stratified case bootstrap percentile; upper = 95th percentile (checks.py) | 0.35 boundary (dashed), 0.25 chance (dotted) | linear 0.1–1.02, shared | BA; higher = more site-decodable | FM-P / FM-S / REF; linear navy (criterion), MLP gray; (A) protocol vs (B, C) exploratory in separate axes |
| Figure 4 | 48 + 12 cells per panel, 540 in total | paired replicate bootstrap percentile per cell (x_compare.py) | 0 | linear; shared within a row, free between rows (caption) | dimensionless; negative = X arm smaller |bias| | groups P1b-FM, P2-FM in record cell order; all panels exploratory |


## Template §12-3 return block

```
[STYLE]        Arial; tick/axis/panel = 9/10/11 pt (schematics 8/9/11; GA 7–9); grayscale+navy #2B3D6B; label-case=(A)
[METHOD]       Fig2:B Fig3:B Fig4:B (no reference .fig exists; make_FigN.m from canonical JSON)  Fig1, GA: §15 pptxgenjs
[FILES]        Fig2–4: .fig + .m + .pdf + .tif(1200); Fig1, GA: .js + .pptx + .pdf + .tif(1200)
[DATA_CHECK]   Figure_2:PASS  Figure_3:PASS  Figure_4:PASS   (hash guard y)
[★ PROVENANCE] manifest 248/248, recorded hashes 10/10 match, anchors 3/3 = PASS
[★ CI]          D̄: paired replicate bootstrap (grid.py); Δ: paired replicate bootstrap (x_compare.py); BA: site-stratified case bootstrap (checks.py) = PASS
[★ LEGEND]      legend↔plot bidirectional invariant = PASS (legends built from plotted handles; asserted)
[★ N/A]         missing set × family combinations omitted, caption states why; W0:P1a (exploratory) not drawn = PASS
[CLASS]        Fig1:V Fig2:V Fig3:V Fig4:V GA:V
[VECTOR]       pdffonts non-empty & Arial emb=yes y ; pdfimages empty (class V) y ; unexpected rasterization n
[★ SCIENCE]    n/CI/reference/scale/unit/direction/category mapping = PASS (qa/MEASUREMENT_REPORT.md; captions)
[★ REBUILD]    clean MATLAB session + canonical data + `.m` = PASS
[★ SIZE]       Figure_1: 190.0 × 162.0 mm   Figure_2: 189.79 × 112.18 mm   Figure_3: 189.79 × 87.84 mm   Figure_4: 189.79 × 139.35 mm   Graphical_abstract: 130.0 × 52.0 mm  (JBI full width 190 mm; GA 13 cm: y)
[★ MARKER]     Fig2: circle 1.129, circle 1.094, other 1.143, other 1.283, triangle 1.293, triangle 1.321 | Fig3: circle 1.129, other 1.283 | Fig4: circle 0.97 (mm; min 0.8)
[★ TEXT]       figure-internal text moved to caption y (category labels and 'Exploratory' titles kept; see POST_RESULT_PRESENTATION_JBI.md §2)
[★ BOX]        Fig2:off  Fig3:off  Fig4:off   (forest / dot plots; y)
[★ MULTIPANEL] shared-axis attribution ok y ; facet physical width equal y (Fig2A facets 58.5 mm; Fig4 panels 54.5 mm)
[★ UNCHANGED]  none after the final round; clean rebuild identical
[★ SCHEMATIC]  numbers vs canonical y (qa/schematic_numbers.json) ; notation registry y ; palette/font y
[BLIND]        metadata clean y ; AI traces 0 hits y ; email 0 hits y
[MAP]          reference→target confirmed y (no earlier JBI figures; numbering = task §5)
```

