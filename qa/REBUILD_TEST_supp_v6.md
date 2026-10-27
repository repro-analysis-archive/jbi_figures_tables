# Clean rebuild test (template §4-0) — supplement v6

The supplement outputs and `canonical_supplement/` were moved out of the repository; the canonical data were re-frozen from the package (`freeze_supplement.py`) and every supplementary figure was rebuilt from its `.m` in its own `matlab -batch` session (no existing `.fig` opened), the tables from `build_tables_supp_v1.py`; the rebuilt files were compared with the previous build. The `.fig` files are checked by `verify_plotted_supp_v6.m` on the rebuilt figures; PDF creation dates differ by construction and are not compared.

| file | compared | result |
|---|---|---|
| `canonical_supplement/SHA256SUMS.txt` | bytes | identical |
| `canonical_supplement/inputs_sha256.json` | bytes | identical |
| `canonical_supplement/s1_contrast_D.csv` | bytes | identical |
| `canonical_supplement/s1_contrast_D.json` | bytes | identical |
| `canonical_supplement/s23_bias_coverage.csv` | bytes | identical |
| `canonical_supplement/s23_bias_coverage.json` | bytes | identical |
| `canonical_supplement/s5_x_cells.csv` | bytes | identical |
| `canonical_supplement/s5_x_cells.json` | bytes | identical |
| `canonical_supplement/s6_b.csv` | bytes | identical |
| `canonical_supplement/s6_b.json` | bytes | identical |
| `canonical_supplement/t_tableB_ba.csv` | bytes | identical |
| `canonical_supplement/t_tableB_ba.json` | bytes | identical |
| `canonical_supplement/t_tableB_judgements.csv` | bytes | identical |
| `canonical_supplement/t_tableB_judgements.json` | bytes | identical |
| `canonical_supplement/t_tableB_sens.csv` | bytes | identical |
| `canonical_supplement/t_tableB_sens.json` | bytes | identical |
| `canonical_supplement/t_tableS4_mask_check.csv` | bytes | identical |
| `canonical_supplement/t_tableS4_mask_check.json` | bytes | identical |
| `canonical_supplement/t_tableX_E3.csv` | bytes | identical |
| `canonical_supplement/t_tableX_E3.json` | bytes | identical |
| `canonical_supplement/t_tableX_group_summaries.csv` | bytes | identical |
| `canonical_supplement/t_tableX_group_summaries.json` | bytes | identical |
| `canonical_supplement/validation.json` | bytes | identical |
| `figures_supp_v1/Figure_S1/Figure_S1_v1.pdf` | text + vector paths (6365 items) | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p01.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p02.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p03.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p04.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p05.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p06.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p07.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p08.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p09.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p10.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/Figure_S2_v1.pdf` | text + vector paths (14964 items) | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p01.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p02.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p03.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p04.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p05.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p06.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p07.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p08.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p09.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p10.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p11.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p12.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p13.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p14.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p15.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p16.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p17.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p18.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p19.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p20.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p21.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p22.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p23.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p24.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/Figure_S3_v1.pdf` | text + vector paths (14820 items) | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p01.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p02.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p03.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p04.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p05.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p06.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p07.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p08.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p09.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p10.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p11.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p12.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p13.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p14.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p15.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p16.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p17.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p18.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p19.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p20.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p21.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p22.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p23.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p24.tif` | pixels 4959 x 7017 | identical |
| `figures_supp_v1/Figure_S5/Figure_S5_v1.pdf` | text + vector paths (2649 items) | identical |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p01.tif` | pixels 8967 x 9167 | identical |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p02.tif` | pixels 8967 x 8700 | identical |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p03.tif` | pixels 8967 x 8700 | identical |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p04.tif` | pixels 8967 x 8700 | identical |
| `figures_supp_v1/Figure_S6/Figure_S6_v1.pdf` | text + vector paths (254 items) | identical |
| `figures_supp_v1/Figure_S6/Figure_S6_v1.tif` | pixels 8967 x 9734 | identical |
| `tables/Table_S1_v1.docx` | document XML | identical |
| `tables/Table_S1_v1.csv` | bytes | identical |
| `tables/Table_S1_v1.pdf` | text + vector paths | identical |
| `tables/Table_S2_v1.docx` | document XML | identical |
| `tables/Table_S2_v1.csv` | bytes | identical |
| `tables/Table_S2_v1.pdf` | text + vector paths | identical |
| `tables/Table_S3_v1.docx` | document XML | identical |
| `tables/Table_S3_v1.csv` | bytes | identical |
| `tables/Table_S3_v1.pdf` | text + vector paths | identical |
| `tables/Table_S4_v1.docx` | document XML | identical |
| `tables/Table_S4_v1.csv` | bytes | identical |
| `tables/Table_S4_v1.pdf` | text + vector paths | identical |
| `tables/Table_S5_v1.docx` | document XML | identical |
| `tables/Table_S5_v1.csv` | bytes | identical |
| `tables/Table_S5_v1.pdf` | text + vector paths | identical |
| `tables/Table_S6_v1.docx` | document XML | identical |
| `tables/Table_S6_v1.csv` | bytes | identical |
| `tables/Table_S6_v1.pdf` | text + vector paths | identical |

**Result: PASS** (109 / 109 identical).
