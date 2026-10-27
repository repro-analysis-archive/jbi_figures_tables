# Measurement report — v5 revision (suffix `_v4`; template §7; measured from the exported files)

| figure | source | PDF page (mm) | TIF (px @ dpi = mm) | regular text (pt) | bold text (pt) | panel labels | min (pt) | fonts | raster objects | overlaps / near | edge < 0.3 mm | TIF ↔ PDF |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Figure_1_v4 | `figures_v3/Figure_1/Figure_1_v3` | 190.0 × 219.0 | [8977, 10347] @ 1200.0 = [190.01, 219.01] | [14] | [14, 15, 16] | (A) (B) (C) (D) | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | PASS |
| Figure_2_v4 | `figures_v3/Figure_4/Figure_4_v3` | 189.79 × 157.34 | [8967, 7434] @ 1200.0 = [189.8, 157.35] | [14, 15] | [16] | (A) (B) (C) | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | PASS |
| Figure_3_v4 | `figures_v3/Figure_2/Figure_2_v3` | 189.79 × 148.17 | [8967, 7000] @ 1200.0 = [189.8, 148.17] | [14, 15] | [16] | (A) (B) | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | PASS |
| Figure_4_v4 | `figures_v3/Figure_3/Figure_3_v3` | 189.79 × 219.07 | [8967, 10350] @ 1200.0 = [189.8, 219.07] | [14, 15] | [16] | (A) (B) (C) | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | PASS |
| Figure_5_v4 | `new (figures_v4/Figure_5/make_Figure_5_v4.m)` | 189.79 × 184.15 | [8967, 8700] @ 1200.0 = [189.8, 184.15] | [14, 15] | [16] | (A) (B) | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | PASS |
| Figure_6_v4 | `figures_v2/Figure_5/Figure_5_v2` | 189.79 × 206.02 | [8967, 9734] @ 1200.0 = [189.8, 206.04] | [14, 15] | [16] | (A) (B) (C) | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | PASS |

All heights ≤ 220 mm; widths as before (data figures 189.79 mm PDF, Figure 1 190.0 mm). Tick / category 14, axis 15, panel labels 16 pt bold in every data figure; Figure 1 body 14, headings 15, panel labels 16 pt.

## New Figure 5: markers (outer incl. edge, from PDF paths; `qa/markers_v5.json`)

| shape | kind | edge colour | n (incl. key) | outer w × h (mm) |
|---|---|---|---|---|
| circle | filled (edge 0.5 pt #1A1A1A) | #1A1A1A | 25 | 1.305 × 1.305 |
| diamond | filled (edge 0.5 pt #1A1A1A) | #1A1A1A | 25 | 1.305 × 1.678 |
| hexagram | filled (edge 0.5 pt #1A1A1A) | #1A1A1A | 25 | 1.521 × 1.729 |
| pentagram | filled (edge 0.5 pt #1A1A1A) | #1A1A1A | 25 | 1.787 × 1.708 |
| square | filled (edge 0.5 pt #1A1A1A) | #1A1A1A | 25 | 1.428 × 1.428 |
| triangle | filled (edge 0.5 pt #1A1A1A) | #1A1A1A | 50 | 1.477 × 1.302 |
| circle | open (edge 0.8 pt, group colour) | #6B6B6B | 25 | 1.411 × 1.411 |
| diamond | open (edge 0.8 pt, group colour) | #2B3D6B | 25 | 1.411 × 1.784 |
| square | open (edge 0.8 pt, group colour) | #6B6B6B | 25 | 1.534 × 1.534 |
| triangle | open (edge 0.8 pt, group colour) | #6B6B6B | 50 | 1.582 × 1.408 |

## New Figure 5: plotted vs canonical and key ↔ plot (`qa/plotted_vs_canonical_v4.json`)

* PASS — 288 values (12 arms × 12 cells × 2 metrics) as line and marker objects; mismatches 0
* panels: rel_bias_pct P = 0: 12 lines, 12 marker series, reference PASS; rel_bias_pct P = 5: 12 lines, 12 marker series, reference PASS; rel_bias_pct P = 30: 12 lines, 12 marker series, reference PASS; coverage P = 0: 12 lines, 12 marker series, reference PASS; coverage P = 5: 12 lines, 12 marker series, reference PASS; coverage P = 30: 12 lines, 12 marker series, reference PASS
* key: 12 entries, each copying the plotted line and marker of its arm in all six panels: NV: PASS, SITE: PASS, FM-P: PASS, FM-P−C: PASS, FM-S: PASS, FM-S−C: PASS, REF: PASS, REF−C: PASS, FM-P-nat: PASS, ORACLE−C: PASS, ORACLE: PASS, FULL: PASS; 12 glyphs distinct: True

## Renumbered figures: byte identity with their sources (`qa/renumber_v5.json`)

| file | source | identical |
|---|---|---|
| `figures_v4/Figure_1/Figure_1_v4.pdf` | `figures_v3/Figure_1/Figure_1_v3.pdf` | yes |
| `figures_v4/Figure_1/Figure_1_v4.pptx` | `figures_v3/Figure_1/Figure_1_v3.pptx` | yes |
| `figures_v4/Figure_1/Figure_1_v4.tif` | `figures_v3/Figure_1/Figure_1_v3.tif` | yes |
| `figures_v4/Figure_1/make_Figure_1_v4.js` | `figures_v3/Figure_1/make_Figure_1_v3.js` | yes |
| `figures_v4/Figure_2/Figure_2_v4.fig` | `figures_v3/Figure_4/Figure_4_v3.fig` | yes |
| `figures_v4/Figure_2/Figure_2_v4.pdf` | `figures_v3/Figure_4/Figure_4_v3.pdf` | yes |
| `figures_v4/Figure_2/Figure_2_v4.tif` | `figures_v3/Figure_4/Figure_4_v3.tif` | yes |
| `figures_v4/Figure_2/make_Figure_2_v4.m` | `figures_v3/Figure_4/make_Figure_4_v3.m` | yes |
| `figures_v4/Figure_3/Figure_3_v4.fig` | `figures_v3/Figure_2/Figure_2_v3.fig` | yes |
| `figures_v4/Figure_3/Figure_3_v4.pdf` | `figures_v3/Figure_2/Figure_2_v3.pdf` | yes |
| `figures_v4/Figure_3/Figure_3_v4.tif` | `figures_v3/Figure_2/Figure_2_v3.tif` | yes |
| `figures_v4/Figure_3/make_Figure_3_v4.m` | `figures_v3/Figure_2/make_Figure_2_v3.m` | yes |
| `figures_v4/Figure_4/Figure_4_v4.fig` | `figures_v3/Figure_3/Figure_3_v3.fig` | yes |
| `figures_v4/Figure_4/Figure_4_v4.pdf` | `figures_v3/Figure_3/Figure_3_v3.pdf` | yes |
| `figures_v4/Figure_4/Figure_4_v4.tif` | `figures_v3/Figure_3/Figure_3_v3.tif` | yes |
| `figures_v4/Figure_4/make_Figure_4_v4.m` | `figures_v3/Figure_3/make_Figure_3_v3.m` | yes |
| `figures_v4/Figure_6/Figure_6_v4.fig` | `figures_v2/Figure_5/Figure_5_v2.fig` | yes |
| `figures_v4/Figure_6/Figure_6_v4.pdf` | `figures_v2/Figure_5/Figure_5_v2.pdf` | yes |
| `figures_v4/Figure_6/make_Figure_6_v4.m` | `figures_v2/Figure_5/make_Figure_5_v2.m` | yes |
| `figures_v4/Figure_6/Figure_6_v4.tif` | `figures_v2/Figure_5/Figure_5_v2.pdf (rasterised by poppler, 1,200 dpi)` | poppler TIF of the PDF |

## Captions cross-check (`qa/captions_v4.json`)

* headings [1, 2, 3, 4, 5, 6]; result PASS
* Figure_1: source CAPTIONS_v2 Figure 1; body identical to source: True; panel letters used ['A', 'B', 'C', 'D'] ⊆ labels in the PDF ['A', 'B', 'C', 'D']
* Figure_2: source CAPTIONS_v2 Figure 4; body identical to source: True; panel letters used ['A', 'B', 'C'] ⊆ labels in the PDF ['A', 'B', 'C']
* Figure_3: source CAPTIONS_v2 Figure 2; body identical to source: True; panel letters used ['A', 'B'] ⊆ labels in the PDF ['A', 'B']
* Figure_4: source CAPTIONS_v2 Figure 3; body identical to source: True; panel letters used ['A', 'B', 'C'] ⊆ labels in the PDF ['A', 'B', 'C']
* Figure_5: source new; body identical to source: None; panel letters used ['A', 'B'] ⊆ labels in the PDF ['A', 'B']
* Figure_6: source CAPTIONS_v2 Figure 5; body identical to source: True; panel letters used ['A', 'B', 'C'] ⊆ labels in the PDF ['A', 'B', 'C']
* references: Figure 1, Figure 1C, Figure 2, Figure 3, Figure 4, Figure 5, Figure 6, Supplementary S1, Supplementary S2, Supplementary S3, Supplementary S5, Supplementary X — all resolve

## Clean rebuild (`qa/REBUILD_TEST_v5.md`)

Result: PASS

## Template §12-3 return block (v5)

```
[STYLE]        Arial; tick/axis/panel = 14/15/16 pt (Figure 1 body/heading/panel 14/15/16); grayscale+navy #2B3D6B; label-case=(A)
[METHOD]       Fig5: B (make_Figure_5_v4.m from canonical JSON); Fig1–4, 6: byte copies of their sources (renumber_v5.py)
[FILES]        per data figure .fig + .m + .pdf + .tif(1200, poppler from the PDF); Fig1 .js + .pptx + .pdf + .tif(1200)
[DATA_CHECK]   Figure_5_v4:PASS (288 values; hash guard y); renumbered: byte identity y
[★ PROVENANCE] manifest + recorded hashes + anchors (v2 3/3, v3 4/4, v5 4/4) = PASS
[★ CI]          Figure 5: Wald 95% interval from the influence function (sdr.py), coverage share (grid.py) confirmed in code; no interval drawn
[★ LEGEND]      Figure 5 key 12 / 12 from plotted objects, 12 series per panel = PASS
[★ N/A]         none (all 12 arms × 12 cells exist; M_finite 200 everywhere)
[CLASS]        Fig1–6: V
[VECTOR]       pdffonts Arial only, emb=yes y ; pdfimages empty y ; unexpected rasterization n
[★ SCIENCE]    n / reference (0, 0.95) / log K / unit (%) / direction / categories = PASS
[★ REBUILD]    clean session + canonical data + scripts = PASS
[★ SIZE]       Figure_1_v4: 190.0 × 219.0 mm   Figure_2_v4: 189.79 × 157.34 mm   Figure_3_v4: 189.79 × 148.17 mm   Figure_4_v4: 189.79 × 219.07 mm   Figure_5_v4: 189.79 × 184.15 mm   Figure_6_v4: 189.79 × 206.02 mm
[★ MARKER]     Fig5 filled circle 1.31 mm, open circle 1.41 mm, other shapes 1.30–1.79 mm (small, with edges); Fig1–4, 6 unchanged
[★ TEXT]       definitions in captions; in-figure category labels only
[★ BOX]        Fig2:off  Fig3:off  Fig4:off  Fig5:off  Fig6:off
[★ MULTIPANEL] Fig5 y shared within a row, y label once per row, x label once, equal widths y
[★ UNCHANGED]  content of Figures 1–4, 6 (byte copies), Tables 1, 2, S5, graphical abstract; all earlier files
[★ SCHEMATIC]  Figure 1 = Figure_1_v3 (numbers vs canonical y)
[BLIND]        metadata clean y ; AI traces 0 y ; email 0 y (TIF pixel strips excluded)
[MAP]          v3/v4 → v5 numbering in POST_RESULT §8, NOTATION_REGISTRY.md, SOURCE_MAP.md y
```

