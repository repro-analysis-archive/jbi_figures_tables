# Clean rebuild test (template §4-0)

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
| `canonical/ga_values.json` | bytes | identical |
| `canonical/gsite.json` | bytes | identical |
| `canonical/inputs_sha256.json` | bytes | identical |
| `canonical/schematic_values.json` | bytes | identical |
| `canonical/table1.json` | bytes | identical |
| `canonical/table3.json` | bytes | identical |
| `canonical/validation.json` | bytes | identical |
| `figures/Figure_1/Figure_1.pdf` | text + vector paths (172 items) | identical |
| `figures/Figure_1/Figure_1.tif` | pixels 8977 x 7654 | identical |
| `figures/Figure_1/Figure_1.pptx` | slide XML | identical |
| `figures/Figure_2/Figure_2.pdf` | text + vector paths (188 items) | identical |
| `figures/Figure_2/Figure_2.tif` | pixels 8963 x 5292 | identical |
| `figures/Figure_3/Figure_3.pdf` | text + vector paths (306 items) | identical |
| `figures/Figure_3/Figure_3.tif` | pixels 8963 x 4134 | identical |
| `figures/Figure_4/Figure_4.pdf` | text + vector paths (1753 items) | identical |
| `figures/Figure_4/Figure_4.tif` | pixels 8963 x 6567 | identical |
| `graphical_abstract/Graphical_abstract.pdf` | text + vector paths (42 items) | identical |
| `graphical_abstract/Graphical_abstract.tif` | pixels 6142 x 2457 | identical |
| `graphical_abstract/Graphical_abstract.pptx` | slide XML | identical |
| `tables/Table_1.pdf` | text + vector paths (230 items) | identical |
| `tables/Table_1.docx` | document XML | identical |
| `tables/Table_2.pdf` | text + vector paths (207 items) | identical |
| `tables/Table_2.docx` | document XML | identical |
| `tables/Table_3.pdf` | text + vector paths (438 items) | identical |
| `tables/Table_3.docx` | document XML | identical |

**Result: PASS** (34 / 34 identical). The `.fig` files are checked by `verify_plotted.m` on the rebuilt figures (qa/plotted_vs_canonical.json); PDF creation dates differ by construction and are not part of the comparison.
