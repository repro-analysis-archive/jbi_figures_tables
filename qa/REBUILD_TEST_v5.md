# Clean rebuild test (template §4-0) — v5 revision outputs

All generated outputs were moved out of the repository; canonical data were re-frozen from the package and every figure, the graphical abstract and the tables were rebuilt from their scripts (each MATLAB figure in its own `matlab -batch "close all force; clear; run(...)"` session; no existing `.fig` was opened). The rebuilt files were compared with the previous build.

| file | compared | result |
|---|---|---|
| `canonical/SHA256SUMS.txt` | bytes | identical |
| `canonical/fam_dbar.csv` | bytes | identical |
| `canonical/fam_dbar.json` | bytes | identical |
| `canonical/fig2B_slice_D.csv` | bytes | identical |
| `canonical/fig2B_slice_D.json` | bytes | identical |
| `canonical/fig3_ba.csv` | bytes | identical |
| `canonical/fig3_ba.json` | bytes | identical |
| `canonical/fig4_x_cells.csv` | bytes | identical |
| `canonical/fig4_x_cells.json` | bytes | identical |
| `canonical/fig5_bias_coverage.csv` | bytes | identical |
| `canonical/fig5_bias_coverage.json` | bytes | identical |
| `canonical/ga_values.json` | bytes | identical |
| `canonical/gsite.json` | bytes | identical |
| `canonical/inputs_sha256.json` | bytes | identical |
| `canonical/schematic_values.json` | bytes | identical |
| `canonical/table1.json` | bytes | identical |
| `canonical/table3.json` | bytes | identical |
| `canonical/validation.json` | bytes | identical |
| `canonical/w_history_D.csv` | bytes | identical |
| `canonical/w_history_D.json` | bytes | identical |
| `canonical/x_cells_order_v3.csv` | bytes | identical |
| `canonical/x_cells_order_v3.json` | bytes | identical |
| `figures_v4/Figure_1/Figure_1_v4.pdf` | text + vector paths (156 items) | identical |
| `figures_v4/Figure_1/Figure_1_v4.tif` | pixels 8977 x 10347 | identical |
| `figures_v4/Figure_1/Figure_1_v4.pptx` | slide XML | identical |
| `figures_v4/Figure_2/Figure_2_v4.pdf` | text + vector paths (288 items) | identical |
| `figures_v4/Figure_2/Figure_2_v4.tif` | pixels 8967 x 7434 | identical |
| `figures_v4/Figure_3/Figure_3_v4.pdf` | text + vector paths (87 items) | identical |
| `figures_v4/Figure_3/Figure_3_v4.tif` | pixels 8967 x 7000 | identical |
| `figures_v4/Figure_4/Figure_4_v4.pdf` | text + vector paths (268 items) | identical |
| `figures_v4/Figure_4/Figure_4_v4.tif` | pixels 8967 x 10350 | identical |
| `figures_v4/Figure_5/Figure_5_v4.pdf` | text + vector paths (804 items) | identical |
| `figures_v4/Figure_5/Figure_5_v4.tif` | pixels 8967 x 8700 | identical |
| `figures_v4/Figure_6/Figure_6_v4.pdf` | text + vector paths (1843 items) | identical |
| `figures_v4/Figure_6/Figure_6_v4.tif` | pixels 8967 x 9734 | identical |

**Result: PASS** (35 / 35 identical). The `.fig` files are checked by `verify_plotted.m` on the rebuilt figures (qa/plotted_vs_canonical.json); PDF creation dates differ by construction and are not part of the comparison.
