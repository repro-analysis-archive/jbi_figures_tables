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
| `canonical/fig5_bias_coverage.csv` | `6ba3b9f3175ff7efc86b0566de9c3bfd71d8329529960d0a4868734fed66ec8f` |
| `canonical/fig5_bias_coverage.json` | `3bd234204f0fabbfb97586ed58ff23bf4239802ef1f5789f2f0ba94b9164666f` |
| `canonical/ga_values.json` | `a1189d04b2f689c63197a0a08a91c5bdfea93669ec553f412d8aba63ba3d4734` |
| `canonical/gsite.json` | `f53932cfbd7f096c21047153aad24e10ffb7e9b3980502ef8d34e39278c92c5c` |
| `canonical/inputs_sha256.json` | `51149613f5711412407423d39e7da512ba038ca824afb9dca2db956bd43bd8f8` |
| `canonical/schematic_values.json` | `f78b6f65669603a33e8cbba2d1f5b6741c09a63bd32247cc1cbeb08c3ea65049` |
| `canonical/table1.json` | `639eebe004e56d28c9a6cf9fe1d990e55d2d0259c048c70a63dcf79576ac8421` |
| `canonical/table3.json` | `ac5c372d7acb54441055fbcf0d46ebfeeefa6691cb5a2c79fc72f8f03c7d2399` |
| `canonical/validation.json` | `21bc0bca8ca81645d36056595ff3e0ce0df8ab16378b8da551fb455bdd5d06ba` |
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

## v5 revision (2026-10-27): current files in the order of first citation

| element | current file | canonical file → field | package source → field |
|---|---|---|---|
| Figure 1 | `figures_v4/Figure_1/Figure_1_v4.*` (byte copy of `Figure_1_v3`) | `schematic_values.json`, `table1.json` | as v3 Figure 1 |
| Figure 2 | `figures_v4/Figure_2/Figure_2_v4.*` (byte copy of `Figure_4_v3`) | `fig3_ba.json` → ba, lo_2p5, hi_97p5, upper_one_sided_95 | `checks.json`, `b_main.csv` |
| Figure 3 | `figures_v4/Figure_3/Figure_3_v4.*` (byte copy of `Figure_2_v3`) | `fam_dbar.json` rows with in_fig2A → D_bar, ci_lo, ci_hi | `families.json` |
| Figure 4 | `figures_v4/Figure_4/Figure_4_v4.*` (byte copy of `Figure_3_v3`) | `w_history_D.json` → D_without_minus_with | `cell_metrics.csv`, `contrast` formula |
| Figure 5 (new) | `figures_v4/Figure_5/Figure_5_v4.*` | `fig5_bias_coverage.json` → rel_bias_pct (= 100 × rel_bias), coverage (arm, K, P); anchors in `validation.json` → v5_bias_coverage_anchors_exact (NV, K = 1, P = 0, rel_bias = 0.10283144587487024; NV, K = 1, P = 0, coverage = 0.85; FULL, K = 1, P = 30, rel_bias = 0.33023840439297236; ORACLE−C, K = 2, P = 0, coverage = 0.97) | `cell_metrics.csv` (set primary, W 30, alpha 0.5, gamma 1, phi 0; 12 arms) → rel_bias, coverage |
| Figure 6 | `figures_v4/Figure_6/Figure_6_v4.*` (byte copy of `Figure_5_v2`; TIF from its PDF) | `fig4_x_cells.json`, `x_cells_order_v3.json` | `x_comparisons_cells.csv` |
| Tables 1, 2, S5; graphical abstract | `tables/Table_1_v2.*`, `tables/Table_2_v3.*`, `tables/Table_S5_v2.*`, `graphical_abstract/Graphical_abstract_v2.*` (unchanged) | as v4 revision | as v4 revision |

Byte identity of the renumbered files with their sources: `qa/renumber_v5.json`.

## v6 supplement (2026-10-27): sources of the supplementary figures and tables

Written by `scripts/freeze_supplement.py` into `canonical_supplement/` (the main `canonical/` is read with its hash guard for the cross-checks and not written).

| element | files | canonical file → field | package source → field |
|---|---|---|---|
| Figure S1 | `figures_supp_v1/Figure_S1/Figure_S1_v1.pdf`, `pages/` | `s1_contrast_D.json` → D, D_disp (pair, cell) | `cell_metrics.csv` (set primary) → abs_bias, mean_truth; formula `contrast`; all D_j of `families.json` reproduced |
| Figures S2, S3 | `figures_supp_v1/Figure_S2/…`, `Figure_S3/…` | `s23_bias_coverage.json` → rel_bias_pct, rel_bias_disp; coverage, coverage_disp (arm, cell) | `cell_metrics.csv` (set primary) → rel_bias, coverage (= `report_cells.csv` within 1e-12) |
| Figure S4 | `figures_supp_v1/Figure_S4/Figure_S4_v1.*` | `s4_mask_profiles.json` → rho, m (centre, point); visible_radius; r | `inputs/mask_check.json` (provided by the investigator; SHA-256 = SOURCES.md record of 8d4c61a) → profiles.<c>.rho, m; visible_radius; r; cross-checked with `tableS4_mask_check.csv` |
| Supplementary Material | `supplementary/Supplementary_Material_v1.docx` | Tables S1–S6 docx, Figures S1–S6 images, `CAPTIONS_supplement_v1.md` | Methods: `inputs/JBI_Supplementary_Methods_draft_v2.md` (provided by the investigator) |
| Figure S5 | `figures_supp_v1/Figure_S5/…` | `s5_x_cells.json` → delta, delta_lo, delta_hi, order (page, analysis, comparison, arm, group) | `x_comparisons_cells.csv` |
| Figure S6 | `figures_supp_v1/Figure_S6/Figure_S6_v1.*` | `s6_b.json` → ba, lo_2p5, hi_97p5, upper_one_sided_95 | `b_main.csv` (= main `fig3_ba.json` B rows) |
| Table S1 | `tables/Table_S1_v1.*` | `t_tableS4_mask_check.json` | `tableS4_mask_check.csv` |
| Table S2 | `tables/Table_S2_v1.*` | main `table3.json` (as Table_S5_v2) | `checks.json`, `x1_e3.json` |
| Table S3 | `tables/Table_S3_v1.*` | `t_tableX_group_summaries.json` | `tableX_group_summaries.csv` (= `x_comparisons_groups.csv`) |
| Table S4 | `tables/Table_S4_v1.*` | `t_tableX_E3.json` | `tableX_E3.csv` |
| Table S5 | `tables/Table_S5_v1.*` | `t_tableB_ba.json`, `t_tableB_judgements.json` | `tableB_ba.csv`, `tableB_judgements.csv` (= `b_judgements.csv`) |
| Table S6 | `tables/Table_S6_v1.*` | `t_tableB_sens.json` | `tableB_sens.csv` (= `b_sensitivity_summary.csv`) |

| canonical_supplement file | SHA-256 |
|---|---|
| `canonical_supplement/inputs_sha256.json` | `92a88e6b3f0a41631758f4e95f4678677c0ae766b7be19cad220bd3af1850c91` |
| `canonical_supplement/s1_contrast_D.csv` | `2577d696f661a5b3f4914cbff54a9eca78c7eac4c432b657a477bd3aa3726e92` |
| `canonical_supplement/s1_contrast_D.json` | `7d7aeca078be39247ec63e272a88a9b95e19f2cacb0ccaf46ae031b13363f3b1` |
| `canonical_supplement/s23_bias_coverage.csv` | `84a0c69601f381c7e544062a46ddf291f3a84f6931a568dc38d89fae1b2fb816` |
| `canonical_supplement/s23_bias_coverage.json` | `b12ac28c3a8084b687f8626172892572f5cc652a7eb9ff8ea80971a4b513929c` |
| `canonical_supplement/s4_mask_profiles.csv` | `323122a9f7e18629224fb86760e4c571c7ee8df2981c219cf7de0f4783ec8508` |
| `canonical_supplement/s4_mask_profiles.json` | `be9aac230d730535a350250f6d585e76f73572c3c60c545554742d9a31baa1bc` |
| `canonical_supplement/s5_x_cells.csv` | `a3fe1a26f6f147719fcdf64e901b2782e62a7b2794b97e05830c46be6503e60a` |
| `canonical_supplement/s5_x_cells.json` | `bb1ff05dde98c37ab09e878d74e0c007ac025303074cd6da7bd12920aaf272b1` |
| `canonical_supplement/s6_b.csv` | `d89ccf6c7ecf1c415987cf14c0a80f24d5c76686d28e8c7fb91387de2e2566e2` |
| `canonical_supplement/s6_b.json` | `922daefff84d1a4fa170ced0eb2f68a43c98d5566657fe996c5ba034e3823c05` |
| `canonical_supplement/t_tableB_ba.csv` | `256297f0391c091e72b08dbccad98adb8e65c7b97a1edb3633ac356b893992bb` |
| `canonical_supplement/t_tableB_ba.json` | `9e086051c2256b49177046ee507ea9c4d072aab864542660238c7701029442f3` |
| `canonical_supplement/t_tableB_judgements.csv` | `8e4f9cbc1b333f3ab91c598b1f2dd0a42cc39cd5c3d5928790a187aeb0714f7c` |
| `canonical_supplement/t_tableB_judgements.json` | `a37229b9038fe6cc8e61e97f8d4c6598dd874fa88a4f8ea0983028f2180238d3` |
| `canonical_supplement/t_tableB_sens.csv` | `bf75f04a3dccec644e7170c7d5f273d72f7113cb309a65e0b55612797cd29301` |
| `canonical_supplement/t_tableB_sens.json` | `0da11606aafe96ea9b47f42419fcf704a9947ff958e84a07ec8e2ef1b84d1acf` |
| `canonical_supplement/t_tableS4_mask_check.csv` | `6912df3831bbf2c5033952040c76c0e23eafd085bcc9aafe80d510db4f957f14` |
| `canonical_supplement/t_tableS4_mask_check.json` | `ebdae71dadb9cbcb9e2fd033d952f3d42b278a09b16137ce285073a2938dffef` |
| `canonical_supplement/t_tableX_E3.csv` | `8c73f70ac232cb4cdb2b454b3f340b5557fc27ef4b3e6f523167e76f68c9f75b` |
| `canonical_supplement/t_tableX_E3.json` | `374bf6c9c5bb24535c0251735b827f2482ee3e2c06a95c9fc1cb7ef87f1bac4f` |
| `canonical_supplement/t_tableX_group_summaries.csv` | `1f388f66f5111d5d5478d767e77ad225df74b9aea88c21fc9c444079870b52dd` |
| `canonical_supplement/t_tableX_group_summaries.json` | `b928f43d02aa4c70ee5d7d47703e4f2944749eb08e682dc0a253a5972c6e3fde` |
| `canonical_supplement/validation.json` | `9cda9567fdecfd0475b5e267afee4d3d17120e456e7876b74bb082ef9134e3e6` |

| package input | path | SHA-256 | recorded by the generating step |
|---|---|---|---|
| cell_metrics | `02_records/step7_record_2880d73/results/step7/cell_metrics.csv` | `588f991bd81a4f71a0b49e12d98521a4df11a286f49722757ba65b254efca0e8` | match |
| families | `02_records/step7_record_2880d73/results/step7/families.json` | `06ab647e679df65f5b617bceae7e42fff92ef8236fe29d5420f4ffa5ac8f71d5` | match |
| report_cells | `03_results/RESULTS_20261019/report_cells.csv` | `1fcdd42b57783424c28a986611b2f2df5abfb9a73a7f32a627a3d9b230a06f9c` | none recorded |
| x_cells | `04_exploratory/X1_X2/results_X/x_comparisons_cells.csv` | `3e6adde59f73aa00fc1fae57aa0851a365479293c203987b24e2fc5361c54637` | match |
| x_groups | `04_exploratory/X1_X2/results_X/x_comparisons_groups.csv` | `98da2fc2b19176aa0c49c39f5260ef120511748c496fa7a968a3609e38d21fa6` | match |
| b_main | `04_exploratory/B/results_B/b_main.csv` | `0087268599b408e1f8988b52b4890c81c724815e9af27211949bdbe9dfa5ad81` | match |
| b_judgements | `04_exploratory/B/results_B/b_judgements.csv` | `09f1c088df6e4eacb324916b1e08a9a8ac4a23303d4d668d35337781e0f8a5ad` | match |
| b_sens | `04_exploratory/B/results_B/b_sensitivity_summary.csv` | `84b4cf4952669ff52981d4e99d94c7fbe67f9139d4d7e36e784298befbdb0148` | match |
| tableS4_mask_check | `03_results/SUPPLEMENT_20261020/tableS4_mask_check.csv` | `8d6498c970c13f8f29e3f88cb44bd7674814213d139875996710236102056605` | none recorded |
| tableX_group_summaries | `03_results/SUPPLEMENT_20261020/tableX_group_summaries.csv` | `98da2fc2b19176aa0c49c39f5260ef120511748c496fa7a968a3609e38d21fa6` | none recorded |
| tableX_E3 | `03_results/SUPPLEMENT_20261020/tableX_E3.csv` | `5b58e7c1f30d7f911d7a63e4d741c5c4cfd9d74a488d0d223eebd8ce186f6746` | none recorded |
| tableB_ba | `03_results/SUPPLEMENT_20261020/tableB_ba.csv` | `0087268599b408e1f8988b52b4890c81c724815e9af27211949bdbe9dfa5ad81` | none recorded |
| tableB_judgements | `03_results/SUPPLEMENT_20261020/tableB_judgements.csv` | `09f1c088df6e4eacb324916b1e08a9a8ac4a23303d4d668d35337781e0f8a5ad` | none recorded |
| tableB_sens | `03_results/SUPPLEMENT_20261020/tableB_sens.csv` | `84b4cf4952669ff52981d4e99d94c7fbe67f9139d4d7e36e784298befbdb0148` | none recorded |
| supplement_captions | `03_results/SUPPLEMENT_20261020/CAPTIONS.md` | `953920d38d902509630adfba1e31789f1c9df79c3b47e444e1a0425c68b57b51` | none recorded |
| supplement_sources | `03_results/SUPPLEMENT_20261020/SOURCES.md` | `834823569d6bfc7a178a21bb5e2c1481d2a810cd4db441449de0835be774aab5` | none recorded |
| presentation_decisions | `03_results/PRESENTATION_DECISIONS.md` | `6b02e8b480a90f923ac4a60feae1e101fc12af281289867995e4bb2d3f2b6637` | none recorded |
| mask_check | `inputs/mask_check.json` | `81c8eb46fa7abba4cb5024e073e30cc838c011d2d62488abbde72d73434d58d5` | match (SUPPLEMENT_20261020/SOURCES.md, 8d4c61a) |

