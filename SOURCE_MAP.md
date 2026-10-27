# Source map — JBI figures and tables

Every plotted or tabulated value comes from a canonical file in `canonical/`, written by `scripts/freeze.py` from the read-only package `/Volumes/ADDATA/医療動画/SS_DS203_manuscript_20261020`. Each input is checked against the package manifest and, where the generating step recorded one, against that recorded hash; the MATLAB, Node and table builders re-check the canonical SHA-256 before reading.

## Package inputs

| name | package path | SHA-256 | recorded by the generating step |
|---|---|---|---|
| families | `02_records/step7_record_2880d73/results/step7/families.json` | `06ab647e679df65f5b617bceae7e42fff92ef8236fe29d5420f4ffa5ac8f71d5` | match |
| cell_metrics | `02_records/step7_record_2880d73/results/step7/cell_metrics.csv` | `588f991bd81a4f71a0b49e12d98521a4df11a286f49722757ba65b254efca0e8` | match |
| step6_run_record | `02_records/step7_record_2880d73/results/step6/run_record.json` | `f6e8b2d73aabd19c2f93faafe985e95b301e80a78557f1b39691f9c147e47e3e` | none recorded |
| checks5 | `02_records/step5_record_0ebf2cf/checks.json` | `ea4cfebf673cd94ef2904a0a5b5fe99b44619985ce5f022af38eac010a26b6e4` | match |
| section13 | `02_records/section13_record_0667430/section13.json` | `36836684363ea0a51507405ad3a6692086288c44ce35ff3024951163baae1a35` | match |
| grid_conditions | `02_records/section13_record_0667430/grid_conditions.json` | `ef6f33ae54582c5b4f2031cd986e801c262c5bd2f5f852a863a9bfcafba67744` | none recorded |
| gsite | `08_additional/codelock/results_codelock_gate/gsite_record.json` | `e09d78700455805bef3d37ada89d0d8a9160455fa02df56c6f094d212daad8f5` | match |
| x1_e3 | `04_exploratory/X1_X2/results_X/x1_e3.json` | `d95fe9752eb43ec0ef808d5e4c8d0ea48ab6f3e17a986575b817bfcdb92287bb` | match |
| x_cells | `04_exploratory/X1_X2/results_X/x_comparisons_cells.csv` | `3e6adde59f73aa00fc1fae57aa0851a365479293c203987b24e2fc5361c54637` | match |
| x_groups | `04_exploratory/X1_X2/results_X/x_comparisons_groups.csv` | `98da2fc2b19176aa0c49c39f5260ef120511748c496fa7a968a3609e38d21fa6` | match |
| b_main | `04_exploratory/B/results_B/b_main.csv` | `0087268599b408e1f8988b52b4890c81c724815e9af27211949bdbe9dfa5ad81` | match |
| table1_sets | `03_results/RESULTS_20261019/figures/table1_data_sets.csv` | `f4d82598d15b3fcac77aef9ec7e851cae2a437df66a4c70ea6d8a9bf4863fbe9` | none recorded |
| table2_models | `03_results/RESULTS_20261019/figures/table2_models.csv` | `438ada7d3aec652a693bf63ac26cf72601c0b994cef89f297e7d54bac4583a99` | none recorded |
| protocol | `01_protocol/SS_PROTOCOL_DS203.md` | `cd7e14026c6ace5b2e2e6987c9e73421401cc6b168b3d25830d116b12d748926` | none recorded |
| fact_base | `02_records/SS_DS203_PROJECT_RECORD_for_evaluator_20261020_v5.md` | `c1d8d651535136907b461e2666b4671d4fc58c736a78e6bb61fbcac54dc27684` | match |
| presentation_decisions | `03_results/PRESENTATION_DECISIONS.md` | `6b02e8b480a90f923ac4a60feae1e101fc12af281289867995e4bb2d3f2b6637` | none recorded |
| key_commits | `07_provenance/main_repository_key_commits.md` | `89340aa24f04cf3ea00ba0e6a7ffb3816fe61f5088a60098fbb6d765a7a3af63` | none recorded |

## Canonical files

| file | SHA-256 |
|---|---|
| `canonical/fam_dbar.csv` | `a6ab420c5e8f3d95f501fe73302058ab512d5355648c4a0139b3e556e2a2f67c` |
| `canonical/fam_dbar.json` | `d634d0e84b5b5dbfb4daf03db36bb3b01cb28c8a58d5370a9ff6bf75717c1bfd` |
| `canonical/fig2B_slice_D.csv` | `546f402b25bd687cf77ae1b810fd873ea54f549c7d055620297145cedaf91a6d` |
| `canonical/fig2B_slice_D.json` | `ac478d25d69b836f492aa6321b057ae4e4d484e9bf1198373cac3eb57b964bb9` |
| `canonical/fig3_ba.csv` | `9bb9e92f2c757903bf68eaed4a7c788e7a9745c30752a1d52f6eac9e19bd1241` |
| `canonical/fig3_ba.json` | `c38d780a8e7183c4a6db0a5ec50f534c9c22e0f5cee3407fa90518f3434d1469` |
| `canonical/fig4_x_cells.csv` | `af4a5eac2ff91f06b9200b37d2cc7b1953a465606556bebd7c47ffdddb969b4c` |
| `canonical/fig4_x_cells.json` | `0d4ad711caf5cf11e2e94213bcacea52013ae00208f2e5f24bf8e0595f23296b` |
| `canonical/ga_values.json` | `a1189d04b2f689c63197a0a08a91c5bdfea93669ec553f412d8aba63ba3d4734` |
| `canonical/gsite.json` | `f53932cfbd7f096c21047153aad24e10ffb7e9b3980502ef8d34e39278c92c5c` |
| `canonical/inputs_sha256.json` | `51149613f5711412407423d39e7da512ba038ca824afb9dca2db956bd43bd8f8` |
| `canonical/schematic_values.json` | `f78b6f65669603a33e8cbba2d1f5b6741c09a63bd32247cc1cbeb08c3ea65049` |
| `canonical/table1.json` | `639eebe004e56d28c9a6cf9fe1d990e55d2d0259c048c70a63dcf79576ac8421` |
| `canonical/table3.json` | `ac5c372d7acb54441055fbcf0d46ebfeeefa6691cb5a2c79fc72f8f03c7d2399` |
| `canonical/validation.json` | `30af8eb9d5fbb601c4dcc808a85d9fc2e357f332dade3a8c7db82411d258c075` |
| `canonical/w_history_D.csv` | `3e1ff505fdddd66ae1b000d0c607ca2fdd1a71a97a7efb213bf4897961c887b5` |
| `canonical/w_history_D.json` | `9e2c53ae1d6b486befd390ccffc31fd3ef7434a116d4203f63eb35d15ad8bec2` |
| `canonical/x_cells_order_v3.csv` | `d2db88517cc09e3eb57d32368bd9d36b885ed9ad0ffb19b11adb233849208c16` |
| `canonical/x_cells_order_v3.json` | `80d5fdb3d5e075b98dc23e8ba64a83d0275e79dfe69cd11b82a0ef4d2b2579ab` |

## Anchors and validations (`canonical/validation.json`)

* primary:P1b-SITE D_bar = 2.197616863578595: PASS
* primary:P2-SITE D_bar = 0.052105083645894015: PASS
* X1 FM-P-C vs step6 FM-P, P1b-FM, mean delta = 0.5609627059097283: PASS
* families.json D_j reproduced from cell_metrics.csv with the committed `contrast` formula: 470 values, max |difference| 0.0
* X group means reproduced from the per-cell Δ: 18 groups
* PASS (B S1 (a)(b) and S3 (b) equal step-5 E3_site_278 / E3_site_primary)
* PASS (x1_e3.json step5_reference equals checks.json E3_site_primary)

## Map per element

| element | cell group | canonical file → field | package source → field |
|---|---|---|---|
| Figure 1 (A) | cases, centre counts | `schematic_values.json` → n_*, centres_* | `03_results/RESULTS_20261019/figures/table1_data_sets.csv` → cases, centres_2_3_4_5; centres of the 278-case set from the fact base §2 |
| Figure 1 (B) | δ, step length, grid, offsets, cells, M | `schematic_values.json` → delta, step_seconds, K, P, W, alpha, gamma, n_cells_main, phi_cells, M, offsets | protocol §2, §7.1, §7.2, §10.1, §10.2 (regex extraction, asserted) |
| Figure 1 (C) | arms and covariates | `table1.json` → arms (names asserted against protocol §8) | protocol §8 |
| Figure 1 (D) | folds, PCs, model names | `schematic_values.json` → folds, n_pcs; `table1.json` → models | protocol §2, §4.2; `table2_models.csv` |
| Figure 1 (E) | dates, units, OSF | `schematic_values.json` → protocol_frozen, code_lock_date, step5_record_date, step6_units, step6_completed, step7_record_date, x_plan_date, x_osf, b_plan_date, b_osf | fact base §3, §7–9; `07_provenance/main_repository_key_commits.md`; `results/step6/run_record.json` → run_plan.n_units |
| Figure 2 (A) | 11 family × set points | `fam_dbar.json` rows with in_fig2A → D_bar, ci_lo, ci_hi | `families.json` → `<set>:<family>`.D_bar, ci_lo, ci_hi (anchors P1b-SITE, P2-SITE) |
| Figure 2 (B) | 24 per-cell D | `fig2B_slice_D.json` → D_without_minus_with (K, P) | `cell_metrics.csv` (set primary, W 30, alpha 0.5, gamma 1, phi 0; arms SITE/NV, ORACLE/ORACLE-C) → abs_bias, mean_truth; formula `make_figures.py` `contrast` (step7_prep c938a56) |
| Figure 3 (A) | 12 BA points | `fig3_ba.json` block E3-site (step 5) → ba, lo_2p5, hi_97p5, upper_one_sided_95 | `checks.json` → `<key>`.E3_site_278 / E3_site_primary.`<probe>` |
| Figure 3 (B, C) | 36 BA points | `fig3_ba.json` blocks B transport / B within-set refit | `b_main.csv` → ba, lo_2p5, hi_97p5, upper_one_sided_95 (key, analysis, probe, set) |
| Figure 4 | 540 per-cell Δ | `fig4_x_cells.json` → delta, delta_lo, delta_hi | `x_comparisons_cells.csv` (analysis X1/X2; comparison minusC/FM; arm; groups) → delta, delta_lo, delta_hi; anchor X1 FM-P−C vs FM-P P1b-FM mean 0.5609627059097283 (`x_comparisons_groups.csv`) |
| Table 1 (A) | sets | `table1.json` → sets (cases, centres, definition, design_cells, arms_run) | `table1_data_sets.csv`; design cells / arms counted from `cell_metrics.csv` |
| Table 1 (B) | models | `table1.json` → models | `table2_models.csv` |
| Table 1 (C) | arms | `table1.json` → arms | protocol §8 table |
| Table 2 | 18 family × set rows | `fam_dbar.json` (role ≠ exploratory) → D_bar_3dp, ci_3dp, share_2dp, rule_verdict, conditions_failed, locked_verdict, tested | `families.json`; footnotes: protocol §12.2 (cells_definition, prediction), `gsite.json` ← `gsite_record.json` |
| Table 3 | step-5 checks | `table3.json` → E1_*, E2_*, E3site_*, E3state_* per key | `checks.json` → `<key>`.<check> (ba / delta_auc, lo_2p5 / ci_lo, hi_97p5 / ci_hi, upper_one_sided_95, pass, retained_fraction) |
| Table 3 | exploratory X1 | `table3.json` → X1_* | `x1_e3.json` → `<key>`.E3_site_primary_X1, E2_primary_after_removal_X1, E3_state_primary_X1 |
| Graphical abstract | 2 numbers + counts | `ga_values.json` → P1b-SITE / P2-SITE D_bar_3dp; `schematic_values.json` → n_representation, n_primary | as Table 2 |

## v3 revision (2026-10-27): map per element of the new numbering

| element (v3) | file | canonical file → field | package source → field |
|---|---|---|---|
| Figure 1 | `figures_v2/Figure_1/Figure_1_v2.*` | `schematic_values.json` (n_*, centres_representation, centres_primary, delta, step_seconds, offsets, dates, OSF) and `table1.json` → arms | as v2 Figure 1 (A), (B), (C), (E) |
| Figure 2 | `figures_v2/Figure_2/Figure_2_v2.*` | `fam_dbar.json` rows with in_fig2A → D_bar, ci_lo, ci_hi | `families.json` (as v2 Figure 2A) |
| Figure 3 (new) | `figures_v2/Figure_3/Figure_3_v2.*` | `w_history_D.json` → D_without_minus_with (pair, W, K, P); anchors in `validation.json` → v3_history_anchors_exact | `cell_metrics.csv` (set primary, alpha 0.5, gamma 1, phi 0, W 0 / 5 / 30; arms SITE/NV, ORACLE/ORACLE-C) → abs_bias, mean_truth; formula `make_figures.py` `contrast`; 14 family cells checked against `families.json` |
| Figure 4 | `figures_v2/Figure_4/Figure_4_v2.*` | `fig3_ba.json` (unchanged) | `checks.json`, `b_main.csv` (as v2 Figure 3) |
| Figure 5 | `figures_v2/Figure_5/Figure_5_v2.*` | `fig4_x_cells.json` → delta, delta_lo, delta_hi (unchanged); display order `x_cells_order_v3.json` → order_v3 | `x_comparisons_cells.csv` (as v2 Figure 4) |
| Table 1 | `tables/Table_1_v2.*` | `table1.json` → sets, models | `table1_data_sets.csv`, `table2_models.csv`, `cell_metrics.csv` |
| Table 2 | `tables/Table_2_v2.*` | `fam_dbar.json` (18 rows), `gsite.json` | `families.json`, protocol §12.2, `gsite_record.json` |
| Supplementary Table S5 | `tables/Table_S5_v2.*` | `table3.json` | `checks.json`, `x1_e3.json` (as v2 Table 3) |
| Graphical abstract | `graphical_abstract/Graphical_abstract_v2.*` | `ga_values.json` → P1b-SITE / P2-SITE D_bar_3dp | as Table 2 |

## v4 revision (2026-10-27): files of the current version

Same canonical sources as the v3 revision; the only canonical change is the record `validation.json` → `v4_table2_sign_decimals` (no plotted or tabulated value changed).

| element | current file | canonical file → field | note |
|---|---|---|---|
| Figure 1 | `figures_v3/Figure_1/Figure_1_v3.*` | as v3 (`schematic_values.json`, `table1.json`) | vertical spacing only |
| Figure 2 | `figures_v3/Figure_2/Figure_2_v3.*` | as v3 (`fam_dbar.json` rows with in_fig2A) | markers only |
| Figure 3 | `figures_v3/Figure_3/Figure_3_v3.*` | as v3 (`w_history_D.json`) | markers and row height only |
| Figure 4 | `figures_v3/Figure_4/Figure_4_v3.*` | as v3 (`fig3_ba.json`) | markers only |
| Figure 5 | `figures_v2/Figure_5/Figure_5_v2.*` (unchanged) | as v3 | not revised |
| Table 1 | `tables/Table_1_v2.*` (unchanged) | as v3 | not revised |
| Table 2 | `tables/Table_2_v3.*` | `fam_dbar.json` (18 rows), `gsite.json`; displayed bound primary:P2-FM ci_lo = -0.00028834867676637266 → −0.0003 (`validation.json` → v4_table2_sign_decimals; `families.json['primary:P2-FM']['ci_lo']`) | heading, footnotes a and b, one bound |
| Supplementary Table S5 | `tables/Table_S5_v2.*` (unchanged) | as v3 | not revised |
| Graphical abstract | `graphical_abstract/Graphical_abstract_v2.*` (unchanged) | as v3 | not revised |

