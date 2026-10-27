% make_Figure_5_v2.m — Figure 5 (v3 revision; old Figure 4): exploratory X1 / X2 per-cell Delta.
% Rendering source of truth. Reads only hash-guarded canonical JSON (fig4_x_cells.json for the values,
% x_cells_order_v3.json for the display order); computes nothing. Content as v2 Figure 4 (3 comparisons x 3 arms,
% all 60 cells of P1b-FM and P2-FM per panel). Changes (task v3 §3): template §2-1 sizes 14 / 15 / 16 pt; readable cell
% order — P1b-FM in two contiguous blocks P = 5 and P = 30 (within each: K = 1, 2, 5, 15, then alpha, gamma), with light
% separators between the K sub-blocks; P2-FM in cell order (W = 0, 5, 30, then alpha, gamma) with separators between
% the W sub-blocks; block and group labels under the axis.
% Run:  matlab -batch "close all force; clear; run('<repo>/figures_v2/Figure_5/make_Figure_5_v2.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style_v3();
X = jbi_read(root, 'fig4_x_cells');
O = jbi_read(root, 'x_cells_order_v3');
rows = X.rows; ord = O.rows;
assert(numel(rows) == 540 && numel(ord) == 60);

W = S.width_cm; H = 20.6;
[fig, cv] = jbi_canvas(W, H);

cmp = {'X1', 'minusC'; 'X1', 'FM'; 'X2', 'minusC'};
rowTitle = {'X1: k−C vs step-6 k−C', 'X1: k−C vs step-6 k (site retained)', 'X2: k−C vs step-6 k−C'};
arms = {'FM-P−C', 'FM-S−C', 'REF−C'};
colTitle = {'k = FM-P', 'k = FM-S', 'k = REF'};
% x positions: P1b-FM P = 5 at 1..24, P = 30 at 27..50; P2-FM at 55..66
xOf = @(g, o) (g == 1) .* (o + 2 * (o > 24)) + (g == 2) .* (54 + o);
groups = {'P1b-FM', 'P2-FM'};
ylims = {[-0.45 0.45], [-0.3 2.5], [-0.35 0.3]};
yticks = {-0.4:0.2:0.4, 0:0.5:2.5, -0.2:0.2:0.2};
axX = [2.2, 7.75, 13.3]; axW = 5.2; axH = 4.0;
axY = [H - 5.8, H - 12.35, H - 18.9];
n = 0;
for i = 1:3
    for j = 1:3
        ax = jbi_axes(fig, S, [axX(j) axY(i) axW axH]);
        set(ax, 'XLim', [-1 67], 'YLim', ylims{i}, 'YTick', yticks{i}, 'XTick', []);
        yl = ylims{i};
        % separators: P blocks / groups (guide gray), K and W sub-blocks (very light)
        for xs = [25.5 52.5]
            plot(ax, [xs xs], yl, '-', 'Color', S.gB3, 'LineWidth', 0.6, 'Tag', 'separator');
        end
        for xs = [6.5 12.5 18.5 32.5 38.5 44.5 58.5 62.5]
            plot(ax, [xs xs], yl, '-', 'Color', S.gD0, 'LineWidth', 0.5, 'Tag', 'subseparator');
        end
        plot(ax, [-1 67], [0 0], ':', 'Color', S.g8A, 'LineWidth', 1.0);
        for g = 1:2
            r = rows(strcmp({rows.analysis}, cmp{i, 1}) & strcmp({rows.comparison}, cmp{i, 2}) & ...
                strcmp({rows.arm}, arms{j}) & strcmp({rows.group}, groups{g}));
            og = ord(strcmp({ord.group}, groups{g}));
            [tf, loc] = ismember([r.cell], [og.cell]);
            assert(all(tf) && numel(r) == numel(og));
            o = [og(loc).order_v3];
            [o, s] = sort(o);
            r = r(s);
            assert(all([r.delta_lo] >= yl(1) & [r.delta_hi] <= yl(2)), 'interval outside y-limits');
            x = xOf(g, o);
            plot(ax, [x; x], [[r.delta_lo]; [r.delta_hi]], '-', 'Color', S.g6B, 'LineWidth', 0.5);
            plot(ax, x, [r.delta], 'o', 'MarkerSize', 2.3, 'MarkerFaceColor', S.navy, 'MarkerEdgeColor', S.k, ...
                'LineWidth', 0.45, 'LineStyle', 'none', 'Tag', sprintf('%s:%s:%s:%s', cmp{i, 1}, cmp{i, 2}, ...
                arms{j}, groups{g}), 'UserData', [[r.cell]' [r.delta]' [r.delta_lo]' [r.delta_hi]' x(:)]);
            n = n + numel(r);
        end
        % block labels (row 1) and group labels (row 2) under the axis, in cm below the axis
        lab = {12.5, 'P = 5'; 38.5, 'P = 30'};
        for q = 1:2
            text(cv, jbi_x2cm(ax, lab{q, 1}), axY(i) - 0.38, lab{q, 2}, 'FontName', S.font, 'FontSize', S.tick, ...
                'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
        end
        grp = {25.5, 'P1b-FM'; 60.5, 'P2-FM'};
        for q = 1:2
            text(cv, jbi_x2cm(ax, grp{q, 1}), axY(i) - 0.98, grp{q, 2}, 'FontName', S.font, 'FontSize', S.tick, ...
                'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
        end
        if j == 1
            ylabel(ax, 'Δ (X − step 6)', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k);
        else
            set(ax, 'YTickLabel', []);
        end
        if i == 1
            text(cv, axX(j) + axW / 2, H - 0.42, colTitle{j}, 'FontName', S.font, 'FontSize', S.axis, ...
                'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
        end
    end
    text(cv, 1.15, axY(i) + axH + 0.66, rowTitle{i}, 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, ...
        'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
    jbi_panel_label(fig, S, sprintf('(%s)', char('A' + i - 1)), 0.12, axY(i) + axH + 0.98);
end
assert(n == 540);

jbi_export(fig, fullfile(here, 'Figure_5_v2'), S);
close(fig);
fprintf('Figure_5_v2 written: %s\n', here);
