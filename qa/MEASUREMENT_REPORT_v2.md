# Measurement report — v3 revision outputs (template §7; measured from the exported files)

| figure | PDF page (mm) | TIF (px @ dpi = mm) | regular text (pt) | bold text (pt) | panel labels (pt) | min (pt) | fonts | raster objects | overlaps / near | edge < 0.3 mm |
|---|---|---|---|---|---|---|---|---|---|---|
| Figure_1_v2 | 190.0 × 232.0 | [8977, 10961] @ 1200.0 = [190.01, 232.01] | [14] | [14, 15, 16] | [16] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |
| Figure_2_v2 | 189.79 × 148.17 | [8963, 6993] @ 1200.0 = [189.72, 148.02] | [14, 15] | [16] | [16] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |
| Figure_3_v2 | 189.79 × 228.25 | [8963, 10772] @ 1200.0 = [189.72, 228.01] | [14, 15] | [16] | [16] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |
| Figure_4_v2 | 189.79 × 157.34 | [8963, 7418] @ 1200.0 = [189.72, 157.01] | [14, 15] | [16] | [16] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |
| Figure_5_v2 | 189.79 × 206.02 | [8963, 9733] @ 1200.0 = [189.72, 206.02] | [14, 15] | [16] | [16] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |
| Graphical_abstract_v2 | 130.0 × 52.0 | [6142, 2457] @ 1200.0 = [130.01, 52.01] | [10] | [10, 11] | — | 10.01 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 |

Data figures: tick labels and category labels 14 pt, axis labels 15 pt, panel labels 16 pt bold. Figure 1: body 14 pt, headings 15 pt bold, panel labels 16 pt bold. Graphical abstract: body 10 pt, title 11 pt bold. No figure needed a size below the template values.

## Marker sizes (outer, including the edge line; from PDF paths)

| figure | shape | colour | edge (pt) | n | outer w × h (mm) |
|---|---|---|---|---|---|
| Figure_2_v2 | circle | #1A1A1A | 0.6 | 5 | 1.129 × 1.129 |
| Figure_2_v2 | other | #4D4D4D | 0.75 | 7 | 1.283 × 1.283 |
| Figure_2_v2 | triangle | #4D4D4D | 0.75 | 3 | 1.321 × 1.18 |
| Figure_3_v2 | circle | #1A1A1A | 0.9 | 25 | 1.094 × 1.094 |
| Figure_3_v2 | other | #1A1A1A | 0.9 | 25 | 1.143 × 1.143 |
| Figure_3_v2 | triangle | #1A1A1A | 0.9 | 25 | 1.293 × 1.162 |
| Figure_4_v2 | circle | #1A1A1A | 0.6 | 25 | 1.129 × 1.129 |
| Figure_4_v2 | other | #4D4D4D | 0.75 | 25 | 1.283 × 1.283 |
| Figure_5_v2 | circle | #1A1A1A | 0.45 | 540 | 0.97 × 0.97 |

## Plotted vs canonical and legend / key ↔ plot (`qa/plotted_vs_canonical_v2.json`)

* Figure_2: PASS — 11 points with their intervals / bounds; mismatches 0; Primary set (n = 158) | W = 0 set (n = 204) | W = 5 set (n = 201) | Single-file set (n = 123)
* Figure_3: PASS — 72 points with their intervals / bounds; mismatches 0; P = 0 | P = 5 | P = 30
* Figure_4: PASS — 48 points with their intervals / bounds; mismatches 0; key: key:chance (dotted line): PASS; key:boundary (dashed line): PASS; key:upper (horizontal tick): PASS; key:upper (horizontal tick): PASS; key:interval (vertical bar): PASS; key:interval (vertical bar): PASS; key:marker (marker): PASS; key:marker (marker): PASS
* Figure_5: PASS — 540 points with their intervals / bounds; mismatches 0; none (single series type; defined in caption)

## Schematic numbers (`qa/schematic_numbers_v2.json`)

* Figure_1_v2: 31 distinct numeric tokens; canonical 31, structural 0, unmatched 0
* Graphical_abstract_v2: 5 distinct numeric tokens; canonical 5, structural 0, unmatched 0

## Tables (`qa/tables_qa_v2.json`)

| table | pages | rules per page | vertical rules | shading | run sizes (pt) | paragraph styles | checks |
|---|---|---|---|---|---|---|---|
| Table_1_v2 | 1 | [6] | 0 | 0 + 0 | {'11.0': 91} | {'Normal': 77} | PASS (13) |
| Table_2_v2 | 1 | [3] | 0 | 0 + 0 | {'11.0': 172} | {'Normal': 161} | PASS (13) |
| Table_S5_v2 | 3 | [3, 2, 3] | 0 | 0 + 0 | {'11.0': 371} | {'Normal': 231} | PASS (12) |

## Clean rebuild (`qa/REBUILD_TEST_v3.md`)

Result: PASS

## Template §12-3 return block (v3)

```
[STYLE]        Arial; tick/axis/panel = 14/15/16 pt (Figure 1 body/heading/panel 14/15/16; GA 10–11); grayscale+navy #2B3D6B; label-case=(A)
[METHOD]       Fig2–5: B (make_Figure_N_v2.m from canonical JSON); Fig1, GA: §15 pptxgenjs
[FILES]        Fig2–5: .fig + .m + .pdf + .tif(1200); Fig1, GA: .js + .pptx + .pdf + .tif(1200)
[DATA_CHECK]   Figure_2:PASS  Figure_3:PASS  Figure_4:PASS  Figure_5:PASS   (hash guard y)
[★ PROVENANCE] manifest 248/248; recorded hashes 10/10; anchors 3/3 (v2) + 4/4 (v3 history) = PASS
[★ CI]          unchanged definitions (POST_RESULT_PRESENTATION_JBI.md §3); Figure 3 has no interval (none exists) = PASS
[★ LEGEND]      Fig2, Fig3 legends from plotted handles; Fig4 key glyphs = drawn objects (8/8) = PASS
[★ N/A]         absent set × family omitted with reason; W0:P1a not drawn = PASS
[CLASS]        Fig1–5: V; GA: V
[VECTOR]       pdffonts Arial only, emb=yes y ; pdfimages empty y ; unexpected rasterization n
[★ SCIENCE]    n / CI / reference / scale / unit / direction / categories = PASS (captions v2)
[★ REBUILD]    clean session + canonical data + scripts = PASS
[★ SIZE]       Figure_1_v2: 190.0 × 232.0 mm   Figure_2_v2: 189.79 × 148.17 mm   Figure_3_v2: 189.79 × 228.25 mm   Figure_4_v2: 189.79 × 157.34 mm   Figure_5_v2: 189.79 × 206.02 mm   Graphical_abstract_v2: 130.0 × 52.0 mm
[★ MARKER]     filled 0.97–1.14 mm; open / angular 1.16–1.32 mm (min 0.8)
[★ TEXT]       definitions in captions; in-figure category labels only
[★ BOX]        Fig2:off  Fig3:off  Fig4:off  Fig5:off
[★ MULTIPANEL] Fig3 y label once per row, shared within row, equal widths y; Fig5 equal widths y
[★ UNCHANGED]  all v2 (old) outputs; v2-suffixed outputs identical after the clean rebuild
[★ SCHEMATIC]  numbers vs canonical y ; notation registry y ; palette / font y
[BLIND]        metadata clean y ; AI traces 0 y ; email 0 y
[MAP]          v2 → v3 numbering in NOTATION_REGISTRY.md and SOURCE_MAP.md y
```

