% make_Figure_S1_v1.m — Supplementary Figure S1 (supplement v6): all-cell heatmaps of D = (|bias| without C − |bias| with C) / mean truth, one page per with/without-C pair,
% primary set, all 240 cells (PRESENTATION_DECISIONS.md item 2: rows alpha x gamma, columns W, each panel K x P; the
% phi_A = 0.5 cells on their own page; no averaging). Rendering source of truth; reads only hash-guarded canonical JSON
% (canonical_supplement/s1_contrast_D.json); computes nothing. Page layout, shading classes and type
% scale: jbi_heatmap_page_v6.m, jbi_ramp_v6.m. Outputs: Figure_S1_v1.pdf (all pages, vector) and pages/ (.fig per page,
% 600-dpi TIF per page rasterised from the PDF by poppler).
% Run:  matlab -batch "close all force; clear; run('<repo>/figures_supp_v1/Figure_S1/make_Figure_S1_v1.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
n = jbi_heatmap_figure_v6(root, 'S1', here);
fprintf('Figure_S1_v1 written: %d pages (%s)\n', n, here);
