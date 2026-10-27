% make_Figure_S5_v1.m — Supplementary Figure S5 (supplement v6): exploratory X1/X2 per-cell Δ not shown in main
% Figure 6. Rendering source of truth; reads only hash-guarded canonical JSON (canonical_supplement/s5_x_cells.json,
% 756 rows of x_comparisons_cells.csv); computes nothing. Four pages (multi-page vector PDF):
%   page 1 (A)–(C): the main-figure slice group (12 cells) for the three comparisons whose other groups are in main
%          Figure 6 — X1 k−C vs step-6 k−C, X1 k−C vs step-6 k (site retained), X2 k−C vs step-6 k−C; columns k.
%   pages 2–4 (D)–(F): every group (P1b-FM 48, P2-FM 12, slice 12 cells) for X1 vs step-6 NV, X2 vs step-6 NV and
%          X2 vs step-6 k (site retained); one full-width panel per k so that 72 cells stay legible.
% Encoding and cell order of main Figure 6 (make_Figure_5_v2.m): navy filled circles with edges, gray 95% intervals,
% dotted zero line; P1b-FM by (P, K, alpha, gamma) with P blocks and light K separators, P2-FM by cell index (W blocks),
% slice by (P, K) with light P separators; cell 15 belongs to both P2-FM and the slice and is shown in both. y shared
% within a row (page 1) or a page (pages 2–4). Template sizes 14/15/16 pt. Per-page .fig and 1,200-dpi TIF (poppler).
% Run:  matlab -batch "close all force; clear; run('<repo>/figures_supp_v1/Figure_S5/make_Figure_S5_v1.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style_v3();
X = jbi_read_supp(root, 's5_x_cells');
rows = X.rows;
assert(numel(rows) == 756);
arms = {'FM-P−C', 'FM-S−C', 'REF−C'}; colTitle = {'k = FM-P', 'k = FM-S', 'k = REF'};
ttl = containers.Map({'X1|minusC', 'X1|FM', 'X2|minusC', 'X1|NV', 'X2|NV', 'X2|FM'}, ...
    {'Exploratory X1: k−C vs step-6 k−C (slice)', 'Exploratory X1: k−C vs step-6 k (site retained; slice)', ...
     'Exploratory X2: k−C vs step-6 k−C (slice)', 'Exploratory X1: k−C vs step-6 NV', ...
     'Exploratory X2: k−C vs step-6 NV', 'Exploratory X2: k−C vs step-6 k (site retained)'});
pages = fullfile(here, 'pages'); if ~isfolder(pages), mkdir(pages); end
pdf = fullfile(here, 'Figure_S5_v1.pdf'); if isfile(pdf), delete(pdf); end
W = S.width_cm; n = 0; np = 0;

% ------------------------------------------------------------------ page 1: slice group, 3 x 3
H = 19.4; [fig, cv] = jbi_canvas(W, H);
combos = {'X1', 'minusC'; 'X1', 'FM'; 'X2', 'minusC'};
axX = [2.2, 7.75, 13.3]; axW = 5.2; axH = 4.0; axY = [H - 5.6, H - 11.6, H - 17.6];
xs = @(o) o + (o > 4) + (o > 8);                   % slice: P = 0 at 1–4, P = 5 at 6–9, P = 30 at 11–14
for i = 1:3
    sub = rows(strcmp({rows.page}, 'slice') & strcmp({rows.analysis}, combos{i, 1}) & strcmp({rows.comparison}, combos{i, 2}));
    assert(numel(sub) == 36);
    yl = padlim([[sub.delta_lo] [sub.delta_hi]]);
    for j = 1:3
        ax = jbi_axes(fig, S, [axX(j) axY(i) axW axH]);
        set(ax, 'XLim', [0 15], 'YLim', yl, 'XTick', []);
        for xsep = [5 10]
            plot(ax, [xsep xsep], yl, '-', 'Color', S.gD0, 'LineWidth', 0.5, 'Tag', 'subseparator');
        end
        plot(ax, [0 15], [0 0], ':', 'Color', S.g8A, 'LineWidth', 1.0, 'Tag', 'zero');
        r = sub(strcmp({sub.arm}, arms{j}));
        [~, o] = sort([r.order]); r = r(o);
        x = xs([r.order]);
        n = n + drawcells(ax, S, r, x, sprintf('S5:%s:%s:%s:slice', combos{i, 1}, combos{i, 2}, arms{j}));
        lab = {2.5, 'P = 0'; 7.5, 'P = 5'; 12.5, 'P = 30'};
        for q = 1:3
            text(cv, jbi_x2cm(ax, lab{q, 1}), axY(i) - 0.38, lab{q, 2}, 'FontName', S.font, 'FontSize', S.tick, ...
                'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
        end
        if j == 1
            ylabel(ax, 'Δ (X − step 6)', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k);
        else
            set(ax, 'YTickLabel', []);
        end
        if i == 1
            text(cv, axX(j) + axW / 2, H - 0.42, colTitle{j}, 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, ...
                'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
        end
    end
    text(cv, 1.15, axY(i) + axH + 0.66, ttl([combos{i, 1} '|' combos{i, 2}]), 'FontName', S.font, 'FontSize', S.axis, ...
        'Color', S.k, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
    jbi_panel_label(fig, S, sprintf('(%s)', char('A' + i - 1)), 0.12, axY(i) + axH + 0.98);
end
np = np + 1; exportpage(fig, pages, pdf, np);

% ------------------------------------------------------------------ pages 2–4: all groups, one panel per k
combos = {'X1', 'NV'; 'X2', 'NV'; 'X2', 'FM'};
xo = containers.Map({'P1b-FM', 'P2-FM', 'slice'}, {@(o) o + 2 * (o > 24), @(o) 54 + o, @(o) 70 + o + (o > 4) + (o > 8)});
for i = 1:3
    H = 18.4; [fig, cv] = jbi_canvas(W, H);
    axX = 2.6; axW = 15.9; axH = 3.9; axY = [H - 6.0, H - 11.0, H - 16.0];
    sub = rows(strcmp({rows.page}, 'all') & strcmp({rows.analysis}, combos{i, 1}) & strcmp({rows.comparison}, combos{i, 2}));
    assert(numel(sub) == 216);
    yl = padlim([[sub.delta_lo] [sub.delta_hi]]);
    for j = 1:3
        ax = jbi_axes(fig, S, [axX axY(j) axW axH]);
        set(ax, 'XLim', [-1 86], 'YLim', yl, 'XTick', []);
        for xsep = [25.5 52.5 68.5]
            plot(ax, [xsep xsep], yl, '-', 'Color', S.gB3, 'LineWidth', 0.6, 'Tag', 'separator');
        end
        for xsep = [6.5 12.5 18.5 32.5 38.5 44.5 58.5 62.5 75.5 80.5]
            plot(ax, [xsep xsep], yl, '-', 'Color', S.gD0, 'LineWidth', 0.5, 'Tag', 'subseparator');
        end
        plot(ax, [-1 86], [0 0], ':', 'Color', S.g8A, 'LineWidth', 1.0, 'Tag', 'zero');
        for g = {'P1b-FM', 'P2-FM', 'slice'}
            r = sub(strcmp({sub.arm}, arms{j}) & strcmp({sub.group}, g{1}));
            [~, o] = sort([r.order]); r = r(o);
            f = xo(g{1});
            n = n + drawcells(ax, S, r, f([r.order]), sprintf('S5:%s:%s:%s:%s', combos{i, 1}, combos{i, 2}, arms{j}, g{1}));
        end
        ylabel(ax, 'Δ (X − step 6)', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k);
        text(cv, axX, axY(j) + axH + 0.42, colTitle{j}, 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, ...
            'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
    end
    lab = {12.5, 'P = 5'; 38.5, 'P = 30'};
    for q = 1:2
        text(cv, jbi_x2cm(ax, lab{q, 1}), axY(3) - 0.38, lab{q, 2}, 'FontName', S.font, 'FontSize', S.tick, ...
            'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
    end
    grp = {25.5, 'P1b-FM'; 60.5, 'P2-FM'; 77, 'slice'};
    for q = 1:3
        text(cv, jbi_x2cm(ax, grp{q, 1}), axY(3) - 0.98, grp{q, 2}, 'FontName', S.font, 'FontSize', S.tick, ...
            'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
    end
    text(cv, 1.15, H - 0.42, ttl([combos{i, 1} '|' combos{i, 2}]), 'FontName', S.font, 'FontSize', S.axis, ...
        'Color', S.k, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
    jbi_panel_label(fig, S, sprintf('(%s)', char('D' + i - 1)), 0.12, H - 0.08);
    np = np + 1; exportpage(fig, pages, pdf, np);
end
assert(n == 756, 'not every value was drawn');
poppler = '/opt/homebrew/bin/pdftoppm';
for p = 1:np
    stem = fullfile(pages, sprintf('Figure_S5_v1_p%02d', p));
    [st, msg] = system(sprintf('"%s" -r 1200 -f %d -l %d -tiff -tiffcompression lzw -singlefile "%s" "%s"', ...
        poppler, p, p, pdf, stem));
    assert(st == 0 && isfile([stem '.tif']), 'pdftoppm failed: %s', msg);
end
fprintf('Figure_S5_v1 written: %d pages, %d values (%s)\n', np, n, here);


function k = drawcells(ax, S, r, x, tag)
plot(ax, [x; x], [[r.delta_lo]; [r.delta_hi]], '-', 'Color', S.g6B, 'LineWidth', 0.5, 'Tag', ['i' tag]);
plot(ax, x, [r.delta], 'o', 'MarkerSize', 2.3, 'MarkerFaceColor', S.navy, 'MarkerEdgeColor', S.k, ...
    'LineWidth', 0.45, 'LineStyle', 'none', 'Tag', tag, ...
    'UserData', [[r.cell]' [r.delta]' [r.delta_lo]' [r.delta_hi]' x(:)]);
k = numel(r);
end


function yl = padlim(v)
% y-limits from the plotted interval ends with 6 % padding (rendering only; every interval inside the axes)
lo = min(v); hi = max(v); pad = 0.06 * (hi - lo);
yl = [min(lo - pad, -pad), max(hi + pad, pad)];
end


function exportpage(fig, pages, pdf, p)
set(findall(fig, '-property', 'FontName'), 'FontName', 'Arial');
wh = fig.UserData.canvasCm;
set(fig, 'PaperUnits', 'centimeters', 'PaperSize', wh, 'PaperPosition', [0 0 wh], 'PaperPositionMode', 'manual', ...
    'InvertHardcopy', 'off', 'Color', 'w');
savefig(fig, fullfile(pages, sprintf('Figure_S5_v1_p%02d.fig', p)));
exportgraphics(fig, pdf, 'ContentType', 'vector', 'Append', true, 'Padding', 'figure');
close(fig);
end
