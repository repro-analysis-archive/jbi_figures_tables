% make_Figure_3.m — Figure 3 (erasure evaluation) for the JBI manuscript.
% Rendering source of truth (template §4-0). Reads only hash-guarded canonical JSON; computes nothing.
%   (A) step-5 E3-site: site balanced accuracy after linear site removal, linear and MLP probes, 278-case set and
%       158-case analysis region, for FM-P, FM-S and REF.
%   (B) Exploratory analysis B, transport: the 278-case (S1) probe evaluated on S1, S2 and S3.
%   (C) Exploratory analysis B, within-set refit: the probe refitted within S1, S2 and S3.
% Points: BA; vertical bar: 95 % percentile interval; horizontal tick: one-sided 95 % upper bound.
% Reference lines: boundary 0.35 (dashed) and chance 0.25 (dotted). Exploratory panels never share an axes with (A).
% Run:  matlab -batch "close all force; clear; run('<repo>/figures/Figure_3/make_Figure_3.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style();
D = jbi_read(root, 'fig3_ba');
rows = D.rows;
assert(numel(rows) == 48, 'Figure 3 expects 12 E3 rows and 36 B rows');

W = S.width_cm; H = 8.75;
[fig, cv] = jbi_canvas(W, H);

blocks = {'E3-site (step 5)', 'B transport', 'B within-set refit'};
titles = {'E3-site (step 5)', 'Exploratory analysis B: transport', 'Exploratory analysis B: within-set refit'};
setsOf = {{'278', '158'}, {'S1', 'S2', 'S3'}, {'S1', 'S2', 'S3'}};
keys = {'P', 'S', 'REF'};
keyLab = {'FM-P', 'FM-S', 'REF'};
probes = {'linear', 'mlp'};
pName = {'Linear probe', 'MLP probe'};
pMk = {'o', 's'};
pMs = [2.6, 3.7];
pFace = {S.navy, 'w'};
pEdge = {S.k, S.g4D};
pLw = [0.6, 0.75];
pCol = {S.navy, S.g6B};
dx = [-0.17, 0.17];

axX = [1.75, 7.6, 13.25]; axW = [4.55, 5.3, 5.3]; axY = 1.25; axH = 5.65;
yl = [0.1 1.02];
axs = gobjects(1, 3);
hProbe = gobjects(1, 2);
hTick = gobjects(1, 1);
plotted = zeros(3, 2);
for b = 1:3
    ax = jbi_axes(fig, S, [axX(b) axY axW(b) axH]);
    axs(b) = ax;
    sts = setsOf{b};
    ns = numel(sts);
    gap = ns + 0.6;
    xpos = @(g, s) (g - 1) * gap + s;
    xlimv = [0.45, xpos(3, ns) + 0.55];
    set(ax, 'XLim', xlimv, 'YLim', yl, 'YTick', 0.2:0.2:1.0);
    hB = plot(ax, xlimv, [0.35 0.35], '--', 'Color', S.g4D, 'LineWidth', 0.8);
    hC = plot(ax, xlimv, [0.25 0.25], ':', 'Color', S.g8A, 'LineWidth', 0.9);
    ticks = []; tlabs = {};
    for g = 1:3
        for s = 1:ns
            x0 = xpos(g, s);
            ticks(end + 1) = x0; %#ok<SAGROW>
            tlabs{end + 1} = sts{s}; %#ok<SAGROW>
            for p = 1:2
                r = rows(strcmp({rows.block}, blocks{b}) & strcmp({rows.key}, keys{g}) & ...
                    strcmp({rows.set}, sts{s}) & strcmp({rows.probe}, probes{p}));
                assert(numel(r) == 1, 'missing canonical row');
                x = x0 + dx(p);
                plot(ax, [x x], [r.lo_2p5 r.hi_97p5], '-', 'Color', pCol{p}, 'LineWidth', 0.9);
                ht = plot(ax, x + [-0.13 0.13], [1 1] * r.upper_one_sided_95, '-', 'Color', pCol{p}, ...
                    'LineWidth', 1.3, 'Tag', 'upper');
                h = plot(ax, x, r.ba, pMk{p}, 'MarkerSize', pMs(p), 'MarkerFaceColor', pFace{p}, ...
                    'MarkerEdgeColor', pEdge{p}, 'LineWidth', pLw(p), 'LineStyle', 'none', ...
                    'Tag', sprintf('%s:%s:%s:%s', blocks{b}, keys{g}, sts{s}, probes{p}), ...
                    'UserData', [r.ba r.lo_2p5 r.hi_97p5 r.upper_one_sided_95]);
                plotted(b, p) = plotted(b, p) + 1;
                if ~isgraphics(hProbe(p))
                    hProbe(p) = h;
                end
                if ~isgraphics(hTick) && p == 1
                    hTick = ht;
                end
            end
        end
        % representation label under its group of set labels
        text(ax, mean([xpos(g, 1) xpos(g, ns)]), yl(1) - 0.088, keyLab{g}, 'Units', 'data', 'FontName', S.font, ...
            'FontSize', S.tick, 'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'top', ...
            'Clipping', 'off');
    end
    set(ax, 'XTick', ticks, 'XTickLabel', tlabs, 'XTickLabelRotation', 0);
    title(ax, titles{b}, 'FontName', S.font, 'FontSize', S.tick, 'FontWeight', 'normal', 'Color', S.k, ...
        'Interpreter', 'none');
    ax.TitleHorizontalAlignment = 'left';
    if b == 1
        hBound = hB; hChance = hC;
    end
end
assert(all(plotted(:) > 0), 'orphan legend entry');
ylabel(axs(1), 'Site balanced accuracy', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k);
set(hTick, 'DisplayName', 'One-sided 95% upper bound');
lg = legend(axs(1), [hProbe hTick hBound hChance], ...
    {'Linear probe', 'MLP probe', 'One-sided 95% upper bound', 'Boundary 0.35', 'Chance 0.25'}, ...
    'Orientation', 'horizontal', 'Box', 'off', 'FontName', S.font, 'FontSize', S.legend, 'TextColor', S.k, ...
    'AutoUpdate', 'off');
lg.ItemTokenSize = [14 8];
lg.Units = 'centimeters';
lg.Position(1:2) = [1.75, H - 0.62];
labX = [0.12, axX(2) - 0.95, axX(3) - 0.95];
for b = 1:3
    jbi_panel_label(fig, S, sprintf('(%s)', char('A' + b - 1)), labX(b), axY + axH + 0.72);
end

jbi_export(fig, fullfile(here, 'Figure_3'), S);
close(fig);
fprintf('Figure_3 written: %s\n', here);
