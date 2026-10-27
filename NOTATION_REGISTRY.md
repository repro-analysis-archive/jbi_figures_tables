# Notation registry — JBI manuscript (figures, tables, captions, code)

Source of truth for symbols (figure template §15-4). Definitions follow the frozen protocol
(`01_protocol/SS_PROTOCOL_DS203.md`, commit 4c86dc5) and the fact base v5. "Figure form" is how the symbol is printed in
the schematics (Figure 1, graphical abstract), where sub- and superscripts are avoided because LibreOffice renders
`pptxgenjs` sub/superscript runs at 58% of the run size (9 pt → 5.2 pt, below the 7 pt floor; measured 2026-10-27).
In MATLAB figures and Word tables, subscripts are real subscripts where used.

## Design and data

| Symbol | Meaning | Values / definition | Source | Figure form |
|---|---|---|---|---|
| C | site (centre), 4 levels | centres 2–5 | protocol §2 | C |
| c(C) | site loading | (−3, −1, 1, 3)/√5, assigned to centres by a permutation drawn per replicate | §6 | c(C) |
| S_t | content state at step t | 1 if the appendix is visible by the end of step t (switch step s) | §2 | S |
| A_t | synthetic action at step t | A_t = μ + γ·c(C) + κ·S_t + α·U + φ_A·A_{t−1} + ε | §6 | A |
| Y | synthetic outcome | after the last post-window step | §6 | Y |
| U | synthetic unmeasured confounder | U ~ N(0, 1), unseen in the video | §6 | U |
| H_t | history | past synthetic actions (pre-window and earlier window steps) | §8 | H |
| R_t | video-derived representation | 64 principal components per 5-s step | §4.2 | R |
| R_t^(−C) | representation after linear site removal | LEACE fitted on the 278-case training folds | §4.3 | "R, site removed" |
| K | intervention duration (window steps) | 1, 2, 5, 15 | §10.1 | K |
| P | post-window steps | 0, 5, 30 | §10.1 | P |
| W | pre-window steps | 0, 5, 30 | §10.1 | W |
| α | unmeasured confounding strength (β = α) | 0, 0.5, 1 | §6, §10.1 | α |
| γ | site loading scale | 0.5, 1 | §6, §10.1 | γ |
| φ_A | action autoregression | 0 (primary), 0.5 (24 sensitivity cells) | §6, §10.1 | "autoregressive actions" |
| δ, d(a) | policy multiplier; policy | δ = 1.05; d(a) = δ·a at every window step | §7.1 | δ, d(a) |
| Ψ(δ) | mean outcome under the policy | estimand Ψ(δ) − Ψ(1) | §7.1 | Ψ(δ) |
| M | replicates per cell | 200 | §10.2 | "200 replicates" |
| s, O, w | switch step; window offset; window start | w = s + O, O = −15, …, 15 (site-stratified) | §7.2 | s, O, w |
| slice | main-text slice | W = 30, α = 0.5, γ = 1, φ_A = 0, primary set | PRESENTATION_DECISIONS.md | — |

## Results

| Symbol | Meaning | Definition | Source | Printed as |
|---|---|---|---|---|
| D_j | per-cell oriented difference | P1: (\|b without C\| − \|b with C\|)/Ψ̄_j; P2: (\|b with C\| − \|b without C\|)/Ψ̄_j | §12.3 | D_j (tables), D (figures) |
| D̄_F | family mean | unweighted mean of D_j over the family's cells | §12.3 | "Mean D" (no combining macron; Word rule template §12) |
| Δ | exploratory per-cell difference | (\|bias\| X arm − \|bias\| step-6 arm)/mean truth; not oriented by family | fact base §8 | Δ, "Δ (X − step 6)" |
| BA | balanced accuracy of the case-level site probe | chance 0.25 | §5 | BA |
| ΔAUC | E2 statistic | held-out AUC(base + R_t) − AUC(base) | §5.2 | ΔAUC |
| E1, E2, E3-site, E3-state | pre-causal checks | site encoding; state recovery; removal success (site, state retention) | §5 | as is |
| G-SITE | design check | η² of S at the window start on C, ≤ 0.01 | §5.4 | as is |
| P1a, P1b-SITE, P1b-FM, P2-SITE, P2-FM, P2-ORACLE, P3 | prediction families | §12.2 | §12.2 | as is |

## Arms and analyses

| Name | Meaning | Note |
|---|---|---|
| NV, SITE, ORACLE−C, ORACLE, FULL | reference arms (§8) | |
| FM-P, FM-S, REF | primary (SurgeNetCholec), secondary (LeanVAE-4ch), reference (Cosmos-1.0-Tokenizer-CV8x8x8) representation arms | records spell the site-removed arms with a hyphen (`FM-P-C`); the manuscript uses the minus sign U+2212 (`FM-P−C`) |
| FM-P−C, FM-S−C, REF−C | site-removed arms | |
| FM-P-nat | primary model, native frames (sensitivity) | no −C arm |
| k | representation index in Figure 4 | k = FM-P, FM-S, REF; "k−C" its site-removed arm |
| X1, X2 | exploratory analyses (OSF osf.io/5c627) | X1: LEACE refitted on the 158-case analysis region; X2: linear-only nuisance learners |
| analysis B | exploratory analysis (OSF osf.io/g9ymw) | "transport" and "within-set refit" (the records' (a) and (b)) |
| S1, S2, S3 | evaluation sets of analysis B | S1 278 cases all steps; S2 158 cases all steps; S3 158 cases analysis region |

## Collisions found and their resolution

| Collision | Resolution (applied in figures, tables, captions) |
|---|---|
| Records key the representations as P, S, REF, but P is also the number of post-window steps and S the content state | Representations are always written FM-P, FM-S, REF (Figure 3 group labels, Figure 4 columns, Table 3 columns) |
| S1–S3 (analysis-B sets) vs Supplementary Figures S1–S4 vs state S vs FM-S | Always "evaluation set S1" / "sets S1–S3"; supplementary items always "Supplementary Figure S1" etc. |
| "B" = exploratory analysis B vs "B = 2,000" bootstrap resamples (records) vs panel label (B) | Captions write "2,000 bootstrap resamples" and "analysis B"; Figure 3 panel (B) is titled "Exploratory analysis B: transport" |
| Analysis B's (a)/(b) vs lower-case panel labels | Named "transport" and "within-set refit" |
| Δ (exploratory difference) vs ΔAUC (E2) | ΔAUC is used only as the compound E2 term; Δ alone always means the X difference |
| D̄ with a combining macron (Word/PDF risk) | "Mean D" in figures, tables and the graphical abstract; D̄_F named once in the Table 2 footnote |
| ∈ is not in Arial | Figure 1 writes "K: 1, 2, 5, 15"; tables write "P = 5 or 30" (mechanical rewrite in `build_tables.py`) |
| Z (theory-map factor) appears in the protocol arm text (Table 1C) | Defined in the Table 1 footnote |

## v3 revision (2026-10-27): numbering and new labels

| Item | v2 | v3 | Note |
|---|---|---|---|
| Study design | Figure 1 (A)–(E) | Figure 1 (A)–(D) | old (D) estimand / estimator text removed (Methods); old (E) workflow is now (D) |
| Confirmatory families | Figure 2A | Figure 2 (A) P1, (B) P2 | facets now labelled as panels |
| Prior action history | — (slice only, Figure 2B) | Figure 3 (A) W = 0, (B) W = 5, (C) W = 30 | same D orientation as v2 Figure 2B: "D (without C − with C)" |
| Erasure evaluation | Figure 3 | Figure 4 | key: "Two-sided 95% interval" (vertical bar), "One-sided 95% upper bound" (short horizontal tick) |
| Exploratory X1/X2 | Figure 4 | Figure 5 | block labels "P = 5", "P = 30" (post-window steps) under P1b-FM |
| Representation diagnostics | Table 3 | Supplementary Table S5 | content unchanged |
| Graphical abstract | "benchmark" | "evaluation" | task v3 §3 |

No new symbol was introduced. "P = 5" / "P = 30" in Figure 5 are post-window steps P (registry above), not the
representation key P (always written FM-P). Supplementary Table S5 continues the package's S1–S4 numbering; the
analysis-B evaluation sets remain "sets S1–S3".

## v5 revision (2026-10-27): numbering in the order of first citation, and the bias / coverage figure

Figure numbers elsewhere in this registry are those of the revision in which the row was written; the current numbers
are below (files `figures_v4/Figure_N/Figure_N_v4.*`). Tables, Supplementary Table S5 and the graphical abstract keep
their numbers. Table 2 v3 heading "Locked rule outcome" (v4 revision) is a column name, not a symbol.

| Content | v3 / v4 number | v5 number | Labels in the figure |
|---|---|---|---|
| Study design | Figure 1 | Figure 1 | (A)–(D) unchanged |
| Erasure evaluation | Figure 4 | Figure 2 | (A) step-5 E3-site; (B), (C) exploratory analysis B |
| Confirmatory families | Figure 2 | Figure 3 | (A) P1, (B) P2 |
| Prior action history | Figure 3 | Figure 4 | (A) W = 0, (B) W = 5, (C) W = 30 |
| Relative bias and coverage at the slice | — (package results-report Figure 1, pre-result decision 1) | Figure 5 (new) | (A) relative bias, (B) coverage; columns "P = 0", "P = 5", "P = 30" |
| Exploratory X1/X2 | Figure 5 | Figure 6 | (A)–(C); "k" = representation index (k = FM-P, FM-S, REF), "k−C" its site-removed arm |

New result quantities (Figure 5; definitions from `ss_benchmark/grid.py` `cell_metrics` and `sdr.py`):

| Symbol | Meaning | Definition | Printed as |
|---|---|---|---|
| relative bias | per arm and cell | mean over the 200 replicates of (estimate − truth) / mean truth (`rel_bias`); shown × 100 | "Relative bias (%)" |
| coverage | per arm and cell | share of the 200 replicates whose Wald 95% interval (estimate ± z_0.975 · SE, SE from the influence function) contains the truth | "95% interval coverage" |

Arm names in the Figure 5 key are those of the arms table above (U+2212 in −C). "P = 0" … "P = 30" are post-window
steps P, not the representation key P (always written FM-P).

## v6 (2026-10-27): supplementary numbering (final) and labels

| Supplementary item | Former name | Labels in the figure / table |
|---|---|---|
| Figure S1 | figS1 | page titles "<pair> — φ_A = 0 (216 cells)" / "φ_A = 0.5 (24 cells)"; "W = 0/5/30"; "α = …", "γ = …"; "K (window steps)", "P (post-window steps)"; key "D (without C − with C)" |
| Figure S2 | figS2 | page titles "<arm> — φ_A = …"; key "\|relative bias\| (%)" |
| Figure S3 | figS3 | page titles "<arm> — φ_A = …"; key "coverage of the 95% interval" |
| Figure S4 | figS4 | (A)–(D) "Centre 2" … "Centre 5"; "Mean gray level"; "Radius ρ (fraction of the square side)"; key "Radial profile m_c(ρ)", "Visible radius ρ_c", "Mask radius r = 0.45" |
| Figure S5 | figX | (A)–(F); "k = FM-P/FM-S/REF"; "Δ (X − step 6)"; blocks "P = 0/5/30", groups "P1b-FM", "P2-FM", "slice" |
| Figure S6 | figB | (A) transport, (B) within-set refit; rows FM-P, FM-S, REF; sets S1–S3 |
| Table S1 | tableS4 | ρ_c, r (× side) |
| Table S2 | Table_S5_v2 (Supplementary Table S5 of v3–v5) | as before |
| Table S3 | tableX_group_summaries | — |
| Table S4 | tableX_E3 | — |
| Table S5 | tableB_ba + tableB_judgements | — |
| Table S6 | tableB_sens | — |

"Supplementary Table S5" in the main-set records of v3–v5 means the current **Table S2**. The analysis-B evaluation
sets keep the names "sets S1–S3"; the figure keys write "Evaluation set" and the captions "evaluation set S1" so that
they are not read as Figures/Tables S1–S3. "slice" = the 12 main-text slice cells (W = 30, α = 0.5, γ = 1, φ_A = 0).
φ_A is printed with a TeX subscript in the heatmap page titles (Arial).
