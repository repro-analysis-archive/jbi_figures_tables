# Supplement index

Existing supplementary items in the read-only package (`/Volumes/ADDATA/医療動画/SS_DS203_manuscript_20261020`), with the SHA-256 from its manifest. Final supplementary numbering is left to the manuscript (the package keeps the labels S1–S4, X, X-E3, B and B-sens). X and B items are exploratory.

| label | content | package path | SHA-256 | source |
|---|---|---|---|---|
| S1 | Contrast Δ|bias| / mean truth, all 240 primary cells, one page pair per with/without-C pair | `03_results/RESULTS_20261019/figures/figS1_contrast_all_cells.pdf` | `772946915af50306fec0eb7d8b563d00d9db466e2460181d2cabdf69878e42ee` | step7_prep c938a56 make_figures.py (pre-result decision 2) |
| S2 | Relative bias, all cells, one page pair per arm | `03_results/RESULTS_20261019/figures/figS2_rel_bias_all_cells.pdf` | `cbf99b8299fffdb2e4bbc3c534cc4940f05e32066d178d6c42770dc0d43ad600` | as S1 |
| S3 | 95% interval coverage, all cells, one page pair per arm | `03_results/RESULTS_20261019/figures/figS3_coverage_all_cells.pdf` | `fbb970869a0b7ebeccd5e71dc1c17ebbd97706d7f2ee6bfe9411f481343c6a00` | as S1 |
| S4 (figure) | Mask check: per-centre radial profiles | `03_results/SUPPLEMENT_20261020/figS4_mask_profiles.pdf` | `8be01edc05fe570753a42f8cc93464195b978584406955878912bb910be9c89e` | step7_prep make_supplement.py; source mask_check.json (8d4c61a) |
| S4 (table) | Mask check values | `03_results/SUPPLEMENT_20261020/tableS4_mask_check.csv` | `8d6498c970c13f8f29e3f88cb44bd7674814213d139875996710236102056605` | as S4 figure; .md alongside |
| X (table) | Exploratory X1/X2 group summaries (54 rows) | `03_results/SUPPLEMENT_20261020/tableX_group_summaries.csv` | `98da2fc2b19176aa0c49c39f5260ef120511748c496fa7a968a3609e38d21fa6` | byte copy of x_comparisons_groups.csv (1c8e628) |
| X-E3 (table) | Exploratory X1 E3-site, E2, E3-state next to step 5 | `03_results/SUPPLEMENT_20261020/tableX_E3.csv` | `5b58e7c1f30d7f911d7a63e4d741c5c4cfd9d74a488d0d223eebd8ce186f6746` | x1_e3.json (1c8e628), checks.json (0ebf2cf) |
| X (figure) | Exploratory X1/X2 per-cell Δ, all 71 cells, all comparators | `03_results/SUPPLEMENT_20261020/figX_cell_delta.pdf` | `ed935465341713bbaff7a7b461f586cc550a4706ac7b0b77432977b1c7d5a4c9` | x_comparisons_cells.csv (1c8e628) |
| B (table) | Exploratory B balanced accuracy (36 rows) | `03_results/SUPPLEMENT_20261020/tableB_ba.csv` | `0087268599b408e1f8988b52b4890c81c724815e9af27211949bdbe9dfa5ad81` | byte copy of b_main.csv (458341f) |
| B (judgements) | Exploratory B judgement statements (36) | `03_results/SUPPLEMENT_20261020/tableB_judgements.csv` | `09f1c088df6e4eacb324916b1e08a9a8ac4a23303d4d668d35337781e0f8a5ad` | byte copy of b_judgements.csv |
| B-sens (table) | Exploratory B equal-size subsampling (36 rows) | `03_results/SUPPLEMENT_20261020/tableB_sens.csv` | `84b4cf4952669ff52981d4e99d94c7fbe67f9139d4d7e36e784298befbdb0148` | byte copy of b_sensitivity_summary.csv |
| B (figure) | Exploratory B BA by set | `03_results/SUPPLEMENT_20261020/figB_ba_by_set.pdf` | `254395e6eef9192bec45fd8e117eed72b9d1cb4ccf41f7815e94fa20b090666e` | b_main.csv (458341f) |
| Captions | Captions of S4, X, X-E3, B, B-sens | `03_results/SUPPLEMENT_20261020/CAPTIONS.md` | `953920d38d902509630adfba1e31789f1c9df79c3b47e444e1a0425c68b57b51` | fact base v5 §5, §8, §9 |
| Sources | Commit, path and blob SHA-256 of every supplementary source | `03_results/SUPPLEMENT_20261020/SOURCES.md` | `834823569d6bfc7a178a21bb5e2c1481d2a810cd4db441449de0835be774aab5` | — |
| Results report | Family verdicts, §13 ceilings, pre-causal checks, PCA / LEACE, all per-cell relative bias and coverage | `03_results/RESULTS_20261019/REPORT.md` | `f6935783e0299d80fa0124ca3e03d21b462fb64f1545e48df75043ed963436e4` | step7_prep make_report.py; inputs hashed in its header |
| Per-cell metrics | All metrics per set, cell and arm (3,504 rows) | `03_results/RESULTS_20261019/report_cells.csv` | `1fcdd42b57783424c28a986611b2f2df5abfb9a73a7f32a627a3d9b230a06f9c` | cell_metrics.csv (2880d73) + family labels |
| Pre-result main figures | Results-report Figures 1–4 drawn under the pre-result presentation decisions (bias / coverage vs K; role switch, five pairs; K × P heatmaps; checks) | `03_results/RESULTS_20261019/figures/fig1_bias_coverage_vs_K.pdf` | `bba0dc6fb897c79dba8ab91abad7b253dd451ca2dad97664f20a7bc8e3555ece` | fig2_role_switch.pdf, fig3_contrast_KP.pdf, fig4_checks.pdf alongside |
| X heatmaps | Exploratory X heatmaps | `04_exploratory/X1_X2/results_X/X_heatmaps.pdf` | `0dab320eda3407998481598be4036e460187d3bf9da8bd635faffada5b080faf` | 1c8e628 |
| S5 (table) | Representation diagnostics (former main Table 3; v3 revision) | work folder `tables/Table_S5_v2.docx` (+ .csv, .pdf) | `6ae658ca5fef32401c84ec89b87937530ebc94c98bfa1ef2bdae27d61bf1a9a1` | `build_tables.py` table3 via `build_tables_v2.py` (canonical `table3.json` ← checks.json, x1_e3.json) |

v3 revision: the slice-only role-switch view of v2 Figure 2B is superseded by main Figure 3 (its W = 30 row; main Figure 4 after the v5 renumbering); Supplementary Figure S1 holds every other α, γ (and W, φ_A) cell of the contrast.

v5 revision: the pre-result main-text Figure 1 (relative bias and coverage against K at the slice, `fig1_bias_coverage_vs_K.pdf`) is reinstated as main Figure 5 (house style, same content); Supplementary Figures S2 and S3 hold relative bias and coverage for every other cell. Main figures in the current numbering: 1 design, 2 erasure, 3 families, 4 prior action history, 5 bias / coverage, 6 exploratory X1/X2.

Not reproduced in the JBI main text and therefore candidates for the supplement: the pre-result main-text Figures 2–4 of the results report (role switch, K × P heatmaps, checks), the FM / REF pairs of the role-switch view at the slice, PCA / LEACE variance retained (results report §3), the slice group and the NV comparator of X (Supplementary Figure X / Table X).
