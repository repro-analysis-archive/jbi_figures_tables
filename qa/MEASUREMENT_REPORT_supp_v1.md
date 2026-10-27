# Measurement report — supplement v6 (template §7; measured from the exported files)

| figure | pages | page size (mm) | text sizes (pt) | min (pt) | fonts | raster objects | overlaps / near | edge < 0.3 mm | TIF dpi | TIF = PDF page |
|---|---|---|---|---|---|---|---|---|---|---|
| Figure_S1 | 10 | 209.9 × 297.04 | [11.0, 12.0, 13.0, 14.0] | 11.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | [600.0] | 10/10 |
| Figure_S2 | 24 | 209.9 × 297.04 | [11.0, 12.0, 13.0, 14.0] | 11.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | [600.0] | 24/24 |
| Figure_S3 | 24 | 209.9 × 297.04 | [11.0, 12.0, 13.0, 14.0] | 11.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | [600.0] | 24/24 |
| Figure_S4 | 1 | 189.79 × 160.16 | [11.0, 14.0, 15.0, 16.0] | 11.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | [1200.0] | 1/1 |
| Figure_S5 | 4 | 189.79 × 184.15, 189.79 × 194.03 | [14.0, 15.0, 16.0] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | [1200.0] | 4/4 |
| Figure_S6 | 1 | 189.79 × 206.02 | [14.0, 15.0, 16.0] | 14.0 | Arial-BoldMT, ArialMT (emb=yes) | 0 | 0 | 0 | [1200.0] | 1/1 |

Heatmap pages (S1–S3): cell values 11 pt, ticks 12, labels 13, titles 14 pt bold (template conflict recorded; the accepted 9-pt floor was not needed). S5, S6: 14 / 15 / 16 pt. The subscript A of φ_A touches its base glyph by design and is excluded from the overlap count.

## Plotted vs canonical (`qa/plotted_vs_canonical_supp_v6.json`)

* Figure_S1: PASS — pages 10, values 1200, mismatches 0, key_classes 11, key_complete True
* Figure_S2: PASS — pages 24, values 2880, mismatches 0, key_classes 7, key_complete True
* Figure_S3: PASS — pages 24, values 2880, mismatches 0, key_classes 5, key_complete True
* Figure_S4: PASS — points 720, mismatches 0, key_glyphs 3, key_ok True
* Figure_S5: PASS — pages 4, values 756, mismatches 0
* Figure_S6: PASS — points 36, mismatches 0, key_glyphs 8, key_ok True

## Cross-checks against the main-figure values (`canonical_supplement/validation.json`)

* anchors: SITE vs NV, W = 0, K = 1, P = 30 (alpha 0.5, gamma 1), D = 8.73427182094206; NV, W = 30, K = 1, P = 0 (alpha 0.5, gamma 1), coverage = 0.85
* main Figure 4 (`w_history_D`) rows equal: 72; slice (`fig2B_slice_D`): 24; main Figure 5 (`fig5_bias_coverage`): 144; main Figure 2 (B, C) rows equal to S6: 36
* families reproduced from the S1 cells (mean = D̄ exactly): P1a 66 cells, mean 1.925 = D̄ 1.925 (max |cell diff| 0.0); P1b-SITE 48 cells, mean 2.198 = D̄ 2.198 (max |cell diff| 0.0); P1b-FM 48 cells, mean 0.594 = D̄ 0.594 (max |cell diff| 0.0); P2-SITE 18 cells, mean 0.052 = D̄ 0.052 (max |cell diff| 0.0); P2-FM 12 cells, mean 0.005 = D̄ 0.005 (max |cell diff| 0.0); P2-ORACLE 12 cells, mean 0.042 = D̄ 0.042 (max |cell diff| 0.0)
* report_cells.csv vs cell_metrics.csv: {'rows': 2880, 'max_rel_diff_rel_bias': 8.249572409854163e-13, 'coverage': 'identical', 'display_strings': 'identical'}
* cells rounding to ±0: D 12, relative bias 4
* Figure S4: 720 points; inputs/mask_check.json (provided by the investigator; SHA-256 equals the blob hash in SUPPLEMENT_20261020/SOURCES.md); 4 x 180 points; consistent with tableS4_mask_check.csv; n_frames, rho_c (4 centres), min rho_c, r equal to the package table

## Tables (`qa/tables_qa_supp_v1.json`)

| table | pages | rules per page | vertical rules | run sizes (pt) | paragraph styles | cells compared with the package CSV | checks |
|---|---|---|---|---|---|---|---|
| Table_S1_v1 | 1 | [3] | 0 | {'11.0': 19} | {'Normal': 18} | 12 | PASS (14) |
| Table_S2_v1 | 3 | [3, 2, 3] | 0 | {'11.0': 371} | {'Normal': 231} | XML/CSV = Table_S5_v2 | PASS (14) |
| Table_S3_v1 | 2 | [3, 3] | 0 | {'11.0': 339} | {'Normal': 336} | 324 | PASS (13) |
| Table_S4_v1 | 2 | [9, 0] | 0 | {'11.0': 105} | {'Normal': 100} | 81 | PASS (13) |
| Table_S5_v1 | 4 | [3, 2, 3, 0] | 0 | {'11.0': 319} | {'Normal': 306} | 288 | PASS (13) |
| Table_S6_v1 | 2 | [3, 3] | 0 | {'11.0': 232} | {'Normal': 231} | 216 | PASS (13) |

## Captions (`qa/captions_supp_v1.json`): PASS — headings ['Figure S1', 'Figure S2', 'Figure S3', 'Figure S4', 'Figure S5', 'Figure S6', 'Table S1', 'Table S2', 'Table S3', 'Table S4', 'Table S5', 'Table S6']

## Supplementary Material document (`qa/supplementary_docx_v1.json`)

* result PASS; LibreOffice PDF 98 pages, fonts ['Arial-BoldMT', 'Arial-ItalicMT', 'ArialMT'], images 64; paragraph styles ['Normal']; automatic numbering 0; sections 13
* order: Supplementary Material → Supplementary Methods (SM 1–7) → SM 1 → Provenance → SM 2 → SM 3 → SM 4 → SM 5 → SM 6 → X1 / X2 → B → SM 7 → Table S1 → Table S2 → Table S3 → Table S4 → Table S5 → Table S6 → Figure S1 → Figure S2 → Figure S3 → Figure S4 → Figure S5 → Figure S6; every caption once: True
* images per figure {'Figure S1': 10, 'Figure S2': 24, 'Figure S3': 24, 'Figure S4': 1, 'Figure S5': 4, 'Figure S6': 1}; widths (mm) {'Figure S1': [190.0], 'Figure S2': [190.0], 'Figure S3': [190.0], 'Figure S4': [189.82], 'Figure S5': [189.82], 'Figure S6': [189.82]}
* methods text equal to the converted draft: True (31875 characters); placeholders kept {'[REF:': [15, 15], '[TO FILL': [1, 1]}; characters missing in Arial left: []

## Blind scan (`qa/blind_scan_supp_v6.json`): 84 files, hits 0

## Clean rebuild (`qa/REBUILD_TEST_supp_v6.md`)

Result: PASS

