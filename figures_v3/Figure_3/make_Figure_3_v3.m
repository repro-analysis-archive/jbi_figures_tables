% make_Figure_3_v3.m — Figure 3 (v4 revision): dependence of the per-cell D on prior action history.
% v4 (task v4 §1.1–1.2): markers enlarged — MarkerSize of v2 multiplied by one factor (3.35 / 2.2) so that the circle
% is 1.5 mm outside (MarkerSize + edge 0.9 pt = 4.25 pt), square and triangle keep their v2 nominal ratios; row height
% reduced (axes 52.5 -> 49.5 mm, every gap and margin as v2) so that the figure is <= 220 mm high; all else as v2.
% TIF = the vector PDF rasterised by poppler at 1,200 dpi (jbi_export_v4): MATLAB's own raster export clips
% markers that straddle its 4,000-px render tiles (qa/tif_markers_*.json).
% Rendering source of truth. Reads only hash-guarded canonical JSON (canonical/w_history_D.json); computes nothing.
% Columns: SITE vs NV, ORACLE vs ORACLE−C; rows: W = 0, 5, 30 (alpha = 0.5, gamma = 1, phi_A = 0, primary set; the
% W = 30 row is the pre-result main-text slice). Per panel: x = K (log axis), one line per P with the marker and
% line-style coding of v2 Figure 2B. y shared within a row, free between rows; zero line in every panel; y label once
% per row; x tick labels and x label on the bottom row only (same K axis). Template §2-1 sizes 14 / 15 / 16 pt.
% Run:  matlab -batch "close all force; clear; run('<repo>/figures_v3/Figure_3/make_Figure_3_v3.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style_v3();
D = jbi_read(root, 'w_history_D');
rows = D.rows;
assert(numel(rows) == 72, 'Figure 3 expects 2 pairs x 3 W x 4 K x 3 P = 72 points');

W = S.width_cm; H = 21.9;                % v2: 22.8
[fig, cv] = jbi_canvas(W, H);

pairs = {'SITE vs NV', 'ORACLE vs ORACLE−C'};
Ws = [0 5 30];
rowTitle = {'W = 0', 'W = 5', 'W = 30'};
ylims = {[-0.6 11.2], [-0.2 1.9], [-0.06 0.08]};
yticks = {0:5:10, 0:0.5:1.5, -0.05:0.05:0.05};
Ps = [0 5 30];
pMk = {'o', 's', '^'};
pMs = [3.35, 4.57, 3.66];                % v2: [2.2, 3.0, 2.4]
pLs = {'-', '--', ':'};
pName = {'P = 0', 'P = 5', 'P = 30'};
axX = [2.55, 10.95]; axW = 7.75; axH = 4.95;   % v2: axH 5.25
axY = [H - 8.15, H - 14.25, H - 20.35];  % v2: [H - 8.45, H - 14.85, H - 21.25]; gaps unchanged
legB = gobjects(1, 3);
n = 0;
for i = 1:3
    for k = 1:2
        ax = jbi_axes(fig, S, [axX(k) axY(i) axW axH]);
        set(ax, 'XScale', 'log', 'XLim', [0.8 19], 'XTick', [1 2 5 15], 'XTickLabel', {'1', '2', '5', '15'}, ...
            'YLim', ylims{i}, 'YTick', yticks{i}, 'XMinorTick', 'off');
        plot(ax, [0.8 19], [0 0], ':', 'Color', S.g8A, 'LineWidth', 1.0);
        pr = rows(strcmp({rows.pair}, pairs{k}) & [rows.W] == Ws(i));
        assert(numel(pr) == 12);
        for j = 1:3
            r = pr([pr.P] == Ps(j));
            [~, o] = sort([r.K]);
            r = r(o);
            assert(isequal([r.K], [1 2 5 15]));
            assert(all([r.D_without_minus_with] > ylims{i}(1) & [r.D_without_minus_with] < ylims{i}(2)));
            h = plot(ax, [r.K], [r.D_without_minus_with], pLs{j}, 'Color', S.navy, 'LineWidth', 0.9, ...
                'Marker', pMk{j}, 'MarkerSize', pMs(j), 'MarkerFaceColor', S.navy, 'MarkerEdgeColor', S.k, ...
                'DisplayName', pName{j}, 'Tag', sprintf('H:%s:W%d:P%d', pairs{k}, Ws(i), Ps(j)), ...
                'UserData', [[r.K]' [r.D_without_minus_with]']);
            n = n + numel(r);
            if i == 1 && k == 1
                legB(j) = h;
                ax1 = ax;
            end
        end
        if k == 2
            set(ax, 'YTickLabel', []);
        else
            ylabel(ax, 'D (without C − with C)', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, ...
                'Interpreter', 'none');
        end
        if i < 3
            set(ax, 'XTickLabel', []);
        end
        if i == 1
            text(cv, axX(k), H - 1.85, pairs{k}, 'FontName', S.font, 'FontSize', S.tick, 'Color', S.k, ...
                'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
        end
    end
    jbi_panel_label(fig, S, sprintf('(%s)', char('A' + i - 1)), 0.12, axY(i) + axH + 0.82);
    text(cv, 1.3, axY(i) + axH + 0.5, rowTitle{i}, 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, ...
        'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
end
assert(n == 72);
text(cv, (axX(1) + axX(2) + axW) / 2, 0.38, 'Intervention duration K (window steps)', 'FontName', S.font, ...
    'FontSize', S.axis, 'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
lg = legend(ax1, legB, pName, 'Orientation', 'horizontal', 'Box', 'off', 'FontName', S.font, ...
    'FontSize', S.legend, 'TextColor', S.k, 'AutoUpdate', 'off');
lg.ItemTokenSize = [24 10];
lg.Units = 'centimeters';
lg.Position(1:2) = [axX(1) - 0.1, H - 0.95];

jbi_export_v4(fig, fullfile(here, 'Figure_3_v3'), S);   % TIF from the vector PDF (poppler); see jbi_export_v4
close(fig);
fprintf('Figure_3_v3 written: %s\n', here);

