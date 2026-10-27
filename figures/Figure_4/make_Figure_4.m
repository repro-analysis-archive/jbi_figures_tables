% make_Figure_4.m — Figure 4 (Exploratory X1/X2) for the JBI manuscript.
% Rendering source of truth (template §4-0). Reads only hash-guarded canonical JSON; computes nothing.
% Per-cell Delta = (|bias| X arm − |bias| step-6 arm) / mean truth with its 95 % paired percentile bootstrap
% interval, all cells of the groups P1b-FM (48) and P2-FM (12), cells in increasing index within each group.
%   rows:    (A) X1 k−C vs step-6 k−C;  (B) X1 k−C vs step-6 k (site retained);  (C) X2 k−C vs step-6 k−C
%   columns: representation k = FM-P, FM-S, REF
% y-scales are shared within a row and differ between rows. Every panel is exploratory.
% Run:  matlab -batch "close all force; clear; run('<repo>/figures/Figure_4/make_Figure_4.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style();
D = jbi_read(root, 'fig4_x_cells');
rows = D.rows;
assert(numel(rows) == 540, 'Figure 4 expects 3 comparisons x 3 arms x 60 cells');

W = S.width_cm; H = 13.9;
[fig, cv] = jbi_canvas(W, H);

cmp = {'X1', 'minusC'; 'X1', 'FM'; 'X2', 'minusC'};
rowTitle = {'X1: k−C vs step-6 k−C', 'X1: k−C vs step-6 k (site retained)', 'X2: k−C vs step-6 k−C'};
arms = {'FM-P−C', 'FM-S−C', 'REF−C'};
colTitle = {'k = FM-P', 'k = FM-S', 'k = REF'};
groups = {'P1b-FM', 'P2-FM'};
x0 = [0, 51];                                   % P1b-FM at 1..48, P2-FM at 52..63
ylims = {[-0.45 0.45], [-0.3 2.5], [-0.35 0.3]};
yticks = {-0.4:0.2:0.4, 0:0.5:2.5, -0.2:0.2:0.2};

axX = [1.75, 7.55, 13.35]; axW = 5.45; axH = 3.05;
axY = [9.5, 5.2, 0.9];
for i = 1:3
    for j = 1:3
        ax = jbi_axes(fig, S, [axX(j) axY(i) axW axH]);
        set(ax, 'XLim', [-1 65], 'YLim', ylims{i}, 'YTick', yticks{i}, 'XTick', [24.5 57.5], ...
            'XTickLabel', groups, 'TickLength', [0.012 0.012], 'XTickLabelRotation', 0);
        ax.XAxis.TickLength = [0 0];
        plot(ax, [-1 65], [0 0], ':', 'Color', S.g8A, 'LineWidth', 0.9);
        n = 0;
        for g = 1:2
            r = rows(strcmp({rows.analysis}, cmp{i, 1}) & strcmp({rows.comparison}, cmp{i, 2}) & ...
                strcmp({rows.arm}, arms{j}) & strcmp({rows.group}, groups{g}));
            [~, o] = sort([r.order_in_group]);
            r = r(o);
            assert(numel(r) == 48 * (g == 1) + 12 * (g == 2));
            assert(all([r.delta_lo] >= ylims{i}(1) & [r.delta_hi] <= ylims{i}(2)), 'interval outside y-limits');
            x = x0(g) + [r.order_in_group];
            plot(ax, [x; x], [[r.delta_lo]; [r.delta_hi]], '-', 'Color', S.g6B, 'LineWidth', 0.5);
            plot(ax, x, [r.delta], 'o', 'MarkerSize', 2.3, 'MarkerFaceColor', S.navy, 'MarkerEdgeColor', ...
                S.k, 'LineWidth', 0.45, 'LineStyle', 'none', 'Tag', sprintf('%s:%s:%s:%s', cmp{i, 1}, ...
                cmp{i, 2}, arms{j}, groups{g}), 'UserData', [[r.cell]' [r.delta]' [r.delta_lo]' [r.delta_hi]']);
            n = n + numel(r);
        end
        assert(n == 60);
        if j == 1
            ylabel(ax, 'Δ (X − step 6)', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k);
        else
            set(ax, 'YTickLabel', []);
        end
        if i == 1
            text(cv, axX(j) + axW / 2, H - 0.32, colTitle{j}, 'FontName', S.font, 'FontSize', S.axis, ...
                'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
        end
    end
    % row title next to the panel label (category label of the comparison)
    text(cv, 0.95, axY(i) + axH + 0.36, rowTitle{i}, 'FontName', S.font, 'FontSize', S.tick, 'Color', S.k, ...
        'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
    jbi_panel_label(fig, S, sprintf('(%s)', char('A' + i - 1)), 0.12, axY(i) + axH + 0.64);
end

jbi_export(fig, fullfile(here, 'Figure_4'), S);
close(fig);
fprintf('Figure_4 written: %s\n', here);
