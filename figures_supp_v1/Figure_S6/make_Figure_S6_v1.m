% make_Figure_S6_v1.m — Supplementary Figure S6 (supplement v6): exploratory analysis B, case-level site balanced
% accuracy by evaluation set. Rendering source of truth; reads only hash-guarded canonical JSON
% (canonical_supplement/s6_b.json, the 36 rows of b_main.csv; equal to main Figure 2 (B), (C)); computes nothing.
% Layout as the package figB (rows: representation FM-P, FM-S, REF; columns: (A) transport, (B) within-set refit,
% never pooled; x = evaluation set S1, S2, S3). Encoding of main Figure 2 (make_Figure_4_v3.m): linear probe navy
% filled circle, MLP probe open square, vertical bar = two-sided 95% interval, short horizontal tick = one-sided 95%
% upper bound, dashed 0.35 boundary, dotted 0.25 chance; the key copies the plotted objects. Template sizes 14/15/16 pt.
% TIF = the vector PDF rasterised by poppler (jbi_export_v4).
% Run:  matlab -batch "close all force; clear; run('<repo>/figures_supp_v1/Figure_S6/make_Figure_S6_v1.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style_v3();
D = jbi_read_supp(root, 's6_b');
rows = D.rows;
assert(numel(rows) == 36, 'Figure S6 expects 3 keys x 2 analyses x 2 probes x 3 sets');

W = S.width_cm; H = 20.6;
[fig, cv] = jbi_canvas(W, H);
keys = {'P', 'S', 'REF'}; keyLab = {'FM-P', 'FM-S', 'REF'};
an = {'a', 'b'}; colTitle = {'Exploratory B: transport', 'Exploratory B: within-set refit'};
probes = {'linear', 'mlp'}; sets = {'S1', 'S2', 'S3'};
pMk = {'o', 's'}; pMs = [3.65, 5.2];                     % as main Figure 2 (v4 marker sizes)
pFace = {S.navy, 'w'}; pEdge = {S.k, S.g4D}; pLw = [0.6, 0.75]; pCol = {S.navy, S.g6B};
dx = [-0.17, 0.17]; ciLw = 1.0; ubLw = 1.4; ubHalf = 0.13;
axX = [3.1, 11.2]; axW = 7.5; axH = 4.3;
axY = [H - 6.2, H - 11.5, H - 16.8];          % x tick labels on the bottom row only (same sets)
yl = [0.1 1.02];
H1 = struct(); plotted = zeros(1, 2); n = 0;
for i = 1:3
    for j = 1:2
        ax = jbi_axes(fig, S, [axX(j) axY(i) axW axH]);
        set(ax, 'XLim', [0.5 3.5], 'YLim', yl, 'YTick', 0.2:0.2:1.0, 'XTick', 1:3, 'XTickLabel', sets);
        if i < 3
            set(ax, 'XTickLabel', []);
        end
        hB = plot(ax, [0.5 3.5], [0.35 0.35], '--', 'Color', S.g4D, 'LineWidth', 1.0, 'Tag', 'boundary');
        hC = plot(ax, [0.5 3.5], [0.25 0.25], ':', 'Color', S.g8A, 'LineWidth', 1.1, 'Tag', 'chance');
        for s = 1:3
            for p = 1:2
                r = rows(strcmp({rows.key}, keys{i}) & strcmp({rows.analysis}, an{j}) & ...
                    strcmp({rows.probe}, probes{p}) & strcmp({rows.set}, sets{s}));
                assert(numel(r) == 1, 'missing canonical row');
                x = s + dx(p);
                hi = plot(ax, [x x], [r.lo_2p5 r.hi_97p5], '-', 'Color', pCol{p}, 'LineWidth', ciLw, 'Tag', 'interval');
                ht = plot(ax, x + [-ubHalf ubHalf], [1 1] * r.upper_one_sided_95, '-', 'Color', pCol{p}, ...
                    'LineWidth', ubLw, 'Tag', 'upper');
                hm = plot(ax, x, r.ba, pMk{p}, 'MarkerSize', pMs(p), 'MarkerFaceColor', pFace{p}, ...
                    'MarkerEdgeColor', pEdge{p}, 'LineWidth', pLw(p), 'LineStyle', 'none', ...
                    'Tag', sprintf('B:%s:%s:%s:%s', keys{i}, an{j}, probes{p}, sets{s}), ...
                    'UserData', [r.ba r.lo_2p5 r.hi_97p5 r.upper_one_sided_95]);
                plotted(p) = plotted(p) + 1; n = n + 1;
                if i == 1 && j == 1 && s == 1
                    H1.marker(p) = hm; H1.interval(p) = hi; H1.upper(p) = ht;
                end
            end
        end
        if j == 1
            ylabel(ax, 'Balanced accuracy', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k);
            text(cv, axX(1), axY(i) + axH + 0.45, keyLab{i}, 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, ...
                'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
        else
            set(ax, 'YTickLabel', []);
        end
        if i == 1
            H1.boundary = hB; H1.chance = hC;
        end
    end
end
assert(n == 36 && all(plotted > 0));
labX = [0.12, 10.35];
for j = 1:2
    jbi_panel_label(fig, S, sprintf('(%s)', char('A' + j - 1)), labX(j), H - 0.08);
    text(cv, labX(j) + 1.05, H - 0.36, colTitle{j}, 'FontName', S.font, 'FontSize', S.tick, 'Color', S.k, ...
        'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
end
text(cv, (axX(1) + axX(2) + axW) / 2, axY(3) - 1.05, 'Evaluation set', 'FontName', S.font, 'FontSize', S.axis, ...
    'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');

% ------------------------------------------------------------------ key: glyphs copied from the plotted objects
labels = {'Linear probe', 'MLP probe', 'Two-sided 95% interval', 'One-sided 95% upper bound', 'Boundary 0.35', ...
          'Chance 0.25'};
kx = [0.6, 9.6]; ky = [1.85, 1.2, 0.55]; gw = 1.7;   % two columns x three rows (markers + boundary | interval, bound, chance)
key = axes(fig, 'Units', 'normalized', 'Position', [0 0 W 2.2] ./ [W H W H], 'XLim', [0 W], 'YLim', [0 2.2], ...
    'Visible', 'off', 'Tag', 'key');
hold(key, 'on');
pos = [1 1; 1 2; 2 1; 2 2; 1 3; 2 3];             % (column, row) of key entries 1..6
slot = @(q) deal(kx(pos(q, 1)), ky(pos(q, 2)));
for q = 1:6
    [x0, y0] = slot(q);
    xm = x0 + gw / 2;
    switch q
        case {1, 2}
            m = H1.marker(q);
            plot(key, xm, y0, m.Marker, 'MarkerSize', m.MarkerSize, 'MarkerFaceColor', m.MarkerFaceColor, ...
                'MarkerEdgeColor', m.MarkerEdgeColor, 'LineWidth', m.LineWidth, 'LineStyle', 'none', 'Tag', 'key:marker');
        case 3
            for p = 1:2
                l = H1.interval(p);
                plot(key, xm + (p - 1.5) * 0.44 * [1 1], y0 + [-0.26 0.26], '-', 'Color', l.Color, ...
                    'LineWidth', l.LineWidth, 'Tag', 'key:interval');
            end
        case 4
            for p = 1:2
                l = H1.upper(p);
                halfcm = ubHalf / 3 * axW;
                plot(key, xm + (p - 1.5) * 0.8 + [-halfcm halfcm], [y0 y0], '-', 'Color', l.Color, ...
                    'LineWidth', l.LineWidth, 'Tag', 'key:upper');
            end
        case 5
            l = H1.boundary;
            plot(key, x0 + [0.1 gw - 0.1], [y0 y0], l.LineStyle, 'Color', l.Color, 'LineWidth', l.LineWidth, 'Tag', 'key:boundary');
        case 6
            l = H1.chance;
            plot(key, x0 + [0.1 gw - 0.1], [y0 y0], l.LineStyle, 'Color', l.Color, 'LineWidth', l.LineWidth, 'Tag', 'key:chance');
    end
    text(key, x0 + gw + 0.25, y0, labels{q}, 'FontName', S.font, 'FontSize', S.legend, 'Color', S.k, ...
        'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
end

jbi_export_v4(fig, fullfile(here, 'Figure_S6_v1'), S);   % TIF from the vector PDF (poppler)
close(fig);
fprintf('Figure_S6_v1 written: %s\n', here);
