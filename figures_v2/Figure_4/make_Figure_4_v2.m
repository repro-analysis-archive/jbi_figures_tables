% make_Figure_4_v2.m — Figure 4 (v3 revision; old Figure 3): evaluation of linear site erasure.
% Rendering source of truth. Reads only hash-guarded canonical JSON; computes nothing. Content as v2 Figure 3:
%   (A) step-5 E3-site (278 / 158 cases); (B) exploratory analysis B, transport; (C) exploratory analysis B,
%   within-set refit; each in its own axes. Changes (task v3 §3): template §2-1 sizes 14 / 15 / 16 pt; (A) on the
%   first row with the key, (B) and (C) on the second row; the key shows the glyphs actually drawn — marker, vertical
%   bar (two-sided 95% interval, own entry), short horizontal tick (one-sided upper bound), dashed and dotted lines —
%   built from the properties of the plotted objects and asserted against them.
% Run:  matlab -batch "close all force; clear; run('<repo>/figures_v2/Figure_4/make_Figure_4_v2.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style_v3();
D = jbi_read(root, 'fig3_ba');
rows = D.rows;
assert(numel(rows) == 48, 'Figure 4 expects 12 E3 rows and 36 B rows');

W = S.width_cm; H = 15.7;
[fig, cv] = jbi_canvas(W, H);

blocks = {'E3-site (step 5)', 'B transport', 'B within-set refit'};
titles = {'E3-site (step 5)', 'Exploratory B: transport', 'Exploratory B: within-set refit'};
setsOf = {{'278', '158'}, {'S1', 'S2', 'S3'}, {'S1', 'S2', 'S3'}};
keys = {'P', 'S', 'REF'};
keyLab = {'FM-P', 'FM-S', 'REF'};
probes = {'linear', 'mlp'};
pMk = {'o', 's'};
pMs = [2.6, 3.7];
pFace = {S.navy, 'w'};
pEdge = {S.k, S.g4D};
pLw = [0.6, 0.75];
pCol = {S.navy, S.g6B};
dx = [-0.17, 0.17];
ciLw = 1.0; ubLw = 1.4; ubHalf = 0.13;

axH = 5.0;
pos = [2.45, H - 6.75, 7.4, axH; 2.45, H - 13.95, 7.6, axH; 11.0, H - 13.95, 7.6, axH];
labTop = [H - 0.08, H - 8.1, H - 8.1];
labX = [0.12, 0.12, 10.25];
yl = [0.1 1.02];
plotted = zeros(3, 2);
H1 = struct();
for b = 1:3
    ax = jbi_axes(fig, S, pos(b, :));
    sts = setsOf{b};
    ns = numel(sts);
    gap = ns + 0.6;
    xpos = @(g, s) (g - 1) * gap + s;
    xlimv = [0.45, xpos(3, ns) + 0.55];
    set(ax, 'XLim', xlimv, 'YLim', yl, 'YTick', 0.2:0.2:1.0);
    hB = plot(ax, xlimv, [0.35 0.35], '--', 'Color', S.g4D, 'LineWidth', 1.0, 'Tag', 'boundary');
    hC = plot(ax, xlimv, [0.25 0.25], ':', 'Color', S.g8A, 'LineWidth', 1.1, 'Tag', 'chance');
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
                hi = plot(ax, [x x], [r.lo_2p5 r.hi_97p5], '-', 'Color', pCol{p}, 'LineWidth', ciLw, 'Tag', 'interval');
                ht = plot(ax, x + [-ubHalf ubHalf], [1 1] * r.upper_one_sided_95, '-', 'Color', pCol{p}, ...
                    'LineWidth', ubLw, 'Tag', 'upper');
                hm = plot(ax, x, r.ba, pMk{p}, 'MarkerSize', pMs(p), 'MarkerFaceColor', pFace{p}, ...
                    'MarkerEdgeColor', pEdge{p}, 'LineWidth', pLw(p), 'LineStyle', 'none', ...
                    'Tag', sprintf('%s:%s:%s:%s', blocks{b}, keys{g}, sts{s}, probes{p}), ...
                    'UserData', [r.ba r.lo_2p5 r.hi_97p5 r.upper_one_sided_95]);
                plotted(b, p) = plotted(b, p) + 1;
                if b == 1 && g == 1 && s == 1
                    H1.marker(p) = hm; H1.interval(p) = hi; H1.upper(p) = ht;
                end
            end
        end
        text(ax, mean([xpos(g, 1) xpos(g, ns)]), yl(1) - 0.125, keyLab{g}, 'Units', 'data', 'FontName', S.font, ...
            'FontSize', S.tick, 'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'top', ...
            'Clipping', 'off');
    end
    set(ax, 'XTick', ticks, 'XTickLabel', tlabs, 'XTickLabelRotation', 0);
    if b == 3
        set(ax, 'YTickLabel', []);
    else
        ylabel(ax, 'Balanced accuracy', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k);
    end
    text(cv, pos(b, 1) + 0.3 * (b == 3), pos(b, 2) + axH + 0.42, titles{b}, 'FontName', S.font, 'FontSize', S.tick, ...
        'Color', S.k, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
    jbi_panel_label(fig, S, sprintf('(%s)', char('A' + b - 1)), labX(b), labTop(b));
    if b == 1
        H1.boundary = hB; H1.chance = hC;
    end
end
assert(all(plotted(:) > 0), 'orphan key entry');

% ------------------------------------------------------------------ key: glyphs copied from the plotted objects
kx = 10.25; ky = H - 1.55; dy = 0.82; gw = 1.7;
key = axes(fig, 'Units', 'normalized', 'Position', [kx ky - 5.6 gw 5.6] ./ [W H W H], 'XLim', [0 gw], ...
    'YLim', [ky - 5.6 ky], 'Visible', 'off', 'Tag', 'key');
hold(key, 'on');
labels = {'Linear probe', 'MLP probe', 'Two-sided 95% interval', 'One-sided 95% upper bound', 'Boundary 0.35', ...
          'Chance 0.25'};
yk = ky - 0.35 - (0:5) * dy;
for p = 1:2       % markers
    m = H1.marker(p);
    plot(key, gw / 2, yk(p), m.Marker, 'MarkerSize', m.MarkerSize, 'MarkerFaceColor', m.MarkerFaceColor, ...
        'MarkerEdgeColor', m.MarkerEdgeColor, 'LineWidth', m.LineWidth, 'LineStyle', 'none', 'Tag', 'key:marker');
end
for p = 1:2       % vertical bars (two-sided interval), one per probe colour
    l = H1.interval(p); xk = gw / 2 + [-0.22 0.22];
    plot(key, [xk(p) xk(p)], yk(3) + [-0.26 0.26], '-', 'Color', l.Color, 'LineWidth', l.LineWidth, 'Tag', 'key:interval');
end
for p = 1:2       % short horizontal ticks (one-sided upper bound), same half-width in cm as in the panels
    l = H1.upper(p); xk = gw / 2 + [-0.4 0.4];
    halfcm = ubHalf / diff(get(ancestor(l, 'axes'), 'XLim')) * pos(1, 3);
    plot(key, xk(p) + [-halfcm halfcm], [yk(4) yk(4)], '-', 'Color', l.Color, 'LineWidth', l.LineWidth, 'Tag', 'key:upper');
end
plot(key, [0.1 gw - 0.1], [yk(5) yk(5)], H1.boundary.LineStyle, 'Color', H1.boundary.Color, ...
    'LineWidth', H1.boundary.LineWidth, 'Tag', 'key:boundary');
plot(key, [0.1 gw - 0.1], [yk(6) yk(6)], H1.chance.LineStyle, 'Color', H1.chance.Color, ...
    'LineWidth', H1.chance.LineWidth, 'Tag', 'key:chance');
for i = 1:6
    text(cv, kx + gw + 0.25, yk(i), labels{i}, 'FontName', S.font, 'FontSize', S.legend, 'Color', S.k, ...
        'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
end

jbi_export(fig, fullfile(here, 'Figure_4_v2'), S);
close(fig);
fprintf('Figure_4_v2 written: %s\n', here);
