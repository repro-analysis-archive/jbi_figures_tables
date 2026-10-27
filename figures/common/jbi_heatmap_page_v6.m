function fig = jbi_heatmap_page_v6(S, R, rows, vfield, dfield, ttl, phi, tagp)
%JBI_HEATMAP_PAGE_V6 One A4-portrait page of an all-cell heatmap (Figures S1–S3, supplement v6; definition of
%   PRESENTATION_DECISIONS.md item 2): rows alpha x gamma (6), columns W (0, 5, 30), each panel K (rows 1, 2, 5, 15) x
%   P (columns 0, 5, 30), no averaging. The phi_A = 0.5 page has only W = 5, K in {1, 5}, P in {0, 5} (its 24 cells),
%   drawn with the same cell size in the W = 5 column. Each cell: a rectangle shaded by class (jbi_ramp_v6) and its
%   value as text (the canonical display string). Own key at the bottom. Relative type scale for this dense page (cell
%   11 / tick 12 / labels 13 / title 14 pt bold; template conflict recorded). Tags: rect:<tagp>:<cell>,
%   text:<tagp>:<cell> (UserData = value); every value and colour is checked by verify_plotted_supp_v6.m.

W = 20.99; H = 29.66;                                  % A4 portrait after whole-point rounding (595 x 841 pt)
[fig, cv] = jbi_canvas(W, H);
fs.cell = 11; fs.tick = 12; fs.lab = 13; fs.title = 14;
Ws = [0 5 30]; Ks = [1 2 5 15]; Ps = [0 5 30];
ag = [0 0.5; 0 1; 0.5 0.5; 0.5 1; 1 0.5; 1 1];
if phi == 0.5
    colW = 5; Ks = [1 5]; Ps = [0 5];
else
    colW = Ws;
end
axX0 = 4.1; gapX = 0.2; pw = (W - 0.8 - axX0 - 2 * gapX) / 3; cw = pw / 3;
top = H - 2.5; gapY = 0.35; ph = (top - 4.45 - 5 * gapY) / 6; ch = ph / 4;
text(cv, 0.8, H - 0.95, ttl, 'FontName', S.font, 'FontSize', fs.title, 'FontWeight', 'bold', 'Color', S.k, ...
    'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle', 'Interpreter', 'tex', 'Tag', 'title');
nc = 0;
for i = 1:6
    y0 = top - (i - 1) * (ph + gapY);
    yc = y0 - numel(Ks) * ch / 2;                      % centre of the panels of this row
    text(cv, 1.45, yc + 0.3, sprintf('α = %g', ag(i, 1)), 'FontName', S.font, 'FontSize', fs.lab, ...
        'Color', S.k, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle', 'Interpreter', 'none');
    text(cv, 1.45, yc - 0.3, sprintf('γ = %g', ag(i, 2)), 'FontName', S.font, 'FontSize', fs.lab, ...
        'Color', S.k, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle', 'Interpreter', 'none');
    for j = 1:3
        if ~ismember(Ws(j), colW)
            continue
        end
        x0 = axX0 + (j - 1) * (pw + gapX);
        nk = numel(Ks); np = numel(Ps);
        ax = axes(fig, 'Units', 'normalized', 'Position', [x0, y0 - nk * ch, np * cw, nk * ch] ./ [W H W H]);
        hold(ax, 'on');
        set(ax, 'XLim', [0.5 np + 0.5], 'YLim', [0.5 nk + 0.5], 'YDir', 'reverse', 'Box', 'on', 'Layer', 'top', ...
            'TickLength', [0 0], 'XTick', 1:np, 'YTick', 1:nk, 'XTickLabel', [], 'YTickLabel', [], ...
            'LineWidth', 0.6, 'XColor', S.k, 'YColor', S.k, 'FontName', S.font, 'FontSize', fs.tick, 'Color', 'none');
        if j == find(ismember(Ws, colW), 1)
            set(ax, 'YTickLabel', arrayfun(@num2str, Ks, 'UniformOutput', false));
        end
        if i == 6
            set(ax, 'XTickLabel', arrayfun(@num2str, Ps, 'UniformOutput', false));
        end
        ax.XAxis.FontSize = fs.tick; ax.YAxis.FontSize = fs.tick;
        for a = 1:nk
            for b = 1:np
                r = rows([rows.W] == Ws(j) & [rows.alpha] == ag(i, 1) & [rows.gamma] == ag(i, 2) & ...
                    [rows.K] == Ks(a) & [rows.P] == Ps(b));
                assert(numel(r) == 1, 'missing or duplicated cell');
                v = r.(vfield);
                c = R.colours(R.cls(v), :);
                rectangle(ax, 'Position', [b - 0.5, a - 0.5, 1, 1], 'FaceColor', c, 'EdgeColor', 'w', ...
                    'LineWidth', 0.5, 'Tag', sprintf('rect:%s:%d', tagp, r.cell), 'UserData', v);
                t = text(ax, b, a, r.(dfield), 'FontName', S.font, 'FontSize', fs.cell, 'Color', S.k, ...
                    'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'Interpreter', 'none', ...
                    'Tag', sprintf('text:%s:%d', tagp, r.cell), 'UserData', v);
                t.Units = 'centimeters';
                assert(t.Extent(3) < cw - 0.1, 'cell text wider than its cell: %s', r.(dfield));
                nc = nc + 1;
            end
        end
    end
end
assert(nc == numel(rows), 'not every cell of the page was drawn');
for j = 1:3
    if ismember(Ws(j), colW)
        x0 = axX0 + (j - 1) * (pw + gapX);
        text(cv, x0 + numel(Ps) * cw / 2, H - 2.05, sprintf('W = %d', Ws(j)), 'FontName', S.font, 'FontSize', fs.lab, ...
            'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'Interpreter', 'none');
    end
end
yb = top - 5 * (ph + gapY) - ph;                       % bottom edge of the last row of panels (phi = 0 geometry)
if phi == 0.5
    yb = top - 5 * (ph + gapY) - numel(Ks) * ch;
end
text(cv, 0.95, (top + yb) / 2, 'K (window steps)', 'FontName', S.font, 'FontSize', fs.lab, 'Color', S.k, ...
    'Rotation', 90, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'Interpreter', 'none');
xc = axX0 + 1.5 * pw + gapX;
if phi == 0.5
    xc = axX0 + pw + gapX + numel(Ps) * cw / 2;
end
text(cv, xc, yb - 1.05, 'P (post-window steps)', 'FontName', S.font, 'FontSize', fs.lab, 'Color', S.k, ...
    'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'Interpreter', 'none');
% ------------------------------------------------------------------ key: every class of the ramp, same on every page
nk = size(R.colours, 1); sw = min(1.35, (W - 1.6) / nk); kx0 = (W - nk * sw) / 2; ky = 1.55;
text(cv, kx0, ky + 0.8, R.title, 'FontName', S.font, 'FontSize', fs.lab, 'Color', S.k, ...
    'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle', 'Interpreter', 'none', 'Tag', 'keytitle');
for q = 1:nk
    rectangle(cv, 'Position', [kx0 + (q - 1) * sw, ky, sw, 0.45], 'FaceColor', R.colours(q, :), 'EdgeColor', S.g6B, ...
        'LineWidth', 0.5, 'Tag', sprintf('key:%d', q));
end
for q = 1:numel(R.edges)
    text(cv, kx0 + q * sw, ky - 0.3, R.labels{q}, 'FontName', S.font, 'FontSize', fs.tick, 'Color', S.k, ...
        'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'Interpreter', 'none', 'Tag', 'keylabel');
end
end
