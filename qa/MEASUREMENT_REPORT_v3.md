# Measurement report — v4 revision outputs (suffix `_v3`; template §7; measured from the exported files)

| figure | PDF page (mm) | TIF (px @ dpi = mm) | regular text (pt) | bold text (pt) | panel labels (pt) | min (pt) | fonts | raster objects | overlaps / near | edge < 0.3 mm |
|---|---|---|---|---|---|---|---|---|---|---|
| Figure_1_v3 | 190.0 × 219.0 | [8977, 10347] @ 1200.0 = [190.01, 219.01] | [14] | [14, 15, 16] | [16] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |
| Figure_2_v3 | 189.79 × 148.17 | [8967, 7000] @ 1200.0 = [189.8, 148.17] | [14, 15] | [16] | [16] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |
| Figure_3_v3 | 189.79 × 219.07 | [8967, 10350] @ 1200.0 = [189.8, 219.07] | [14, 15] | [16] | [16] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |
| Figure_4_v3 | 189.79 × 157.34 | [8967, 7434] @ 1200.0 = [189.8, 157.35] | [14, 15] | [16] | [16] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |

Font sizes unchanged from v3: data figures tick / category 14, axis 15, panel 16 pt bold; Figure 1 body 14, headings 15, panel labels 16 pt bold. Widths unchanged (data figures 189.79 mm PDF; Figure 1 190.0 mm). Heights: Figure 1 232.0 → 219.0 mm; Figure 3 228.25 → 219.07 mm (both ≤ 220 mm); Figures 2 and 4 unchanged. Not revised and not re-measured: Figure 5 (`Figure_5_v2`), graphical abstract (`Graphical_abstract_v2`).

## Marker sizes before (v2) → after (v3), outer incl. edge, from PDF paths (`qa/markers_v4.json`)

| figure | shape | face | edge (pt) | n | before w × h (mm) | after w × h (mm) |
|---|---|---|---|---|---|---|
| Figure_2 | circle | navy filled | 0.6 | 5 | 1.129 × 1.129 | 1.499 × 1.499 |
| Figure_2 | diamond | white (hollow) | 0.75 | 3 | 1.182 × 1.484 | 1.552 × 1.977 |
| Figure_2 | square | white (hollow) | 0.75 | 4 | 1.283 × 1.283 | 1.695 × 1.695 |
| Figure_2 | triangle | white (hollow) | 0.75 | 3 | 1.321 × 1.18 | 1.748 × 1.549 |
| Figure_3 | circle | navy filled | 0.9 | 25 | 1.094 × 1.094 | 1.499 × 1.499 |
| Figure_3 | square | navy filled | 0.9 | 25 | 1.143 × 1.143 | 1.575 × 1.575 |
| Figure_3 | triangle | navy filled | 0.9 | 25 | 1.293 × 1.162 | 1.805 × 1.605 |
| Figure_4 | circle | navy filled | 0.6 | 25 | 1.129 × 1.129 | 1.499 × 1.499 |
| Figure_4 | square | white (hollow) | 0.75 | 25 | 1.283 × 1.283 | 1.695 × 1.695 |
| Figure_5 | circle | navy filled | 0.45 | 540 | 0.97 × 0.97 | unchanged (not revised) |

Ticks, axes and panels: unchanged (`qa/v4_unchanged.json`: Figures 2 and 4 — every text span and every non-marker path identical to v2; Figure 3 — texts, fonts, sizes and path kinds identical, axes 52.5 → 49.5 mm high; Figure 1 — shapes, texts, sizes, colours, x positions, widths and heights identical, y positions and four vertical connector lengths changed).

| check | Figure_1 | Figure_2 | Figure_3 | Figure_4 |
|---|---|---|---|---|
| v4 unchanged-check | PASS | PASS | PASS | PASS |
| TIF ↔ PDF whole image (`qa/tif_vs_pdf_*`) | PASS | PASS | PASS | PASS |
| TIF markers complete (`qa/tif_markers_*`) | — | PASS | PASS | PASS |

## Finding: MATLAB raster export clips markers at its 4,000-px render tiles

| earlier TIF (unchanged) | markers | flagged (PDF ink not covered by the TIF > 10 %) and visual verdict |
|---|---|---|
| Figure_2 | 42 | none |
| Figure_3 | 50 | (84.86, 21.64) mm, 31 % uncovered: **clipped** (one side missing) |
| Figure_4 | 540 | none |
| Figure_2_v2 | 15 | (64.56, 14.19) mm, 11 % uncovered: intact (thinner MATLAB stroke); (169.63, 98.04) mm, 13 % uncovered: **clipped** (one side missing) |
| Figure_3_v2 | 75 | none |
| Figure_4_v2 | 50 | (84.45, 26.01) mm, 30 % uncovered: **clipped** (one side missing) |
| Figure_5_v2 | 540 | none |

Visual verdicts from PDF | TIF crops at 1,200 dpi: `qa/tif_tile_clipping_evidence.png`. Each clipped marker straddles a 4,000-px tile boundary of MATLAB's raster export (x = 4,000 or 8,000 px, or 4,000 px from the bottom). The v3 TIFs are the MATLAB vector PDFs rasterised by poppler (`jbi_export_v4.m`): no flagged marker.

## Plotted vs canonical and legend / key ↔ plot (`qa/plotted_vs_canonical_v3.json`)

* Figure_2_v3: PASS — 11 points with their intervals / bounds; mismatches 0; Primary set (n = 158) | W = 0 set (n = 204) | W = 5 set (n = 201) | Single-file set (n = 123)
* Figure_3_v3: PASS — 72 points with their intervals / bounds; mismatches 0; P = 0 | P = 5 | P = 30
* Figure_4_v3: PASS — 48 points with their intervals / bounds; mismatches 0; key: key:chance (dotted line): PASS; key:boundary (dashed line): PASS; key:upper (horizontal tick): PASS; key:upper (horizontal tick): PASS; key:interval (vertical bar): PASS; key:interval (vertical bar): PASS; key:marker (marker): PASS; key:marker (marker): PASS

## Schematic numbers (`qa/schematic_numbers_v3.json`)

* Figure_1_v3: 31 distinct numeric tokens; canonical 31, unmatched 0

## Table 2 v3 (`qa/tables_qa_v3.json`)

* pages 1 (A4 landscape 297.0 × 210.0 mm); rules per page [3]; vertical rules 0; shading 0 + 0; run sizes {'11.0': 178}; paragraph styles {'Normal': 162}; fonts BAAAAA+Arial-BoldMT TrueType emb=yes, CAAAAA+ArialMT TrueType emb=yes
* bound primary:P2-FM ci_lo: exact -0.00028834867676637266 (families.json) → displayed −0.0003 (4 decimals; 3 decimals would give −0.000)
* CSV cells changed vs Table_2_v2: row 0 col 5: 'Direction rule' → 'Locked rule outcome{sup:a}'; row 6 col 3: '0.005 (−0.000 to 0.012)' → '0.005 (−0.0003{sup:b} to 0.012)'
* checks: PASS (19)

## Clean rebuild (`qa/REBUILD_TEST_v4.md`)

Result: PASS

## Template §12-3 return block (v4)

```
[STYLE]        Arial; tick/axis/panel = 14/15/16 pt (Figure 1 body/heading/panel 14/15/16); grayscale+navy #2B3D6B; label-case=(A)
[METHOD]       Fig2–4: B (make_Figure_N_v3.m from canonical JSON); Fig1: §15 pptxgenjs
[FILES]        Fig2–4: .fig + .m + .pdf + .tif(1200; from the vector PDF); Fig1: .js + .pptx + .pdf + .tif(1200)
[DATA_CHECK]   Figure_2_v3:PASS  Figure_3_v3:PASS  Figure_4_v3:PASS   (hash guard y)
[★ PROVENANCE] manifest + recorded hashes + anchors as v3 = PASS; validation.json + v4_table2_sign_decimals (bound equals families.json)
[★ CI]          unchanged definitions (§3); Figure 3 has no interval (none exists) = PASS
[★ LEGEND]      Fig2, Fig3 legends from plotted handles; Fig4 key glyphs = drawn objects (8/8) = PASS
[★ N/A]         absent set × family omitted with reason; W0:P1a not drawn = PASS
[CLASS]        Fig1–4: V
[VECTOR]       pdffonts Arial only, emb=yes y ; pdfimages empty y ; unexpected rasterization n
[★ SCIENCE]    n / CI / reference / scale / unit / direction / categories = PASS (values, captions unchanged)
[★ REBUILD]    clean session + canonical data + scripts = PASS
[★ SIZE]       Figure_1_v3: 190.0 × 219.0 mm   Figure_2_v3: 189.79 × 148.17 mm   Figure_3_v3: 189.79 × 219.07 mm   Figure_4_v3: 189.79 × 157.34 mm
[★ MARKER]     filled circle 1.499 mm (Fig2–4); hollow / angular 1.55–1.98 mm (v2 nominal ratios kept); Fig5 unchanged 0.97 mm
[★ TEXT]       definitions in captions; in-figure category labels only (unchanged)
[★ BOX]        Fig2:off  Fig3:off  Fig4:off
[★ MULTIPANEL] Fig3 y label once per row (1.0 mm past each axis end, inside its row band), equal widths y
[★ UNCHANGED]  Figure 5, Tables 1 / S5, graphical abstract, captions; all earlier files byte-identical
[★ SCHEMATIC]  numbers vs canonical y ; notation registry y ; palette / font y
[BLIND]        metadata clean y ; AI traces 0 y ; email 0 y (TIF pixel strips excluded)
[MAP]          v4 current-file map in SOURCE_MAP.md y
```

