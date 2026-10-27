% make_Figure_5_v4.m — Figure 5 (v5 revision, new): relative bias and coverage of the 95% interval at the slice.
% The pre-result main-text Figure 1 of PRESENTATION_DECISIONS.md (2026-10-09, decision 1), reinstated in the house style
% (task v5 §1); same definition as the package rendering fig1_bias_coverage_vs_K.pdf. Rendering source of truth. Reads
% only hash-guarded canonical JSON (canonical/fig5_bias_coverage.json); computes nothing (rel_bias_pct is frozen).
% Rows: (A) relative bias (%), (B) coverage; columns: P = 0, 5, 30; x = K (log axis); y shared within a row; reference
% lines 0 (bias) and 0.95 (coverage). All 12 arms in every panel, all in the key (built from the plotted lines).
% Encoding (template §2-3: prominence = inferential role): four groups by line style and shade — NV / SITE dashed
% #6B6B6B; the seven representation arms solid #8A8A8A; ORACLE−C / ORACLE dash-dot navy (exact-state arms); FULL dotted
% #4D4D4D (exchangeability oracle) — arms within a group by marker; filled = the arm has site information (C or a
% site-retaining representation), open = it has none (NV, the −C arms, ORACLE−C). Small markers with edges, no jitter,
% so that the near-overlap within a group stays visible. Each arm is drawn as a line (Tag BC:...) and a marker-only
% object on the same points (Tag BCm:...), so that the marker edge can be thinner than the line: filled markers edge
% 0.5 pt #1A1A1A (a thicker black edge hides the group shade at this size), open markers edge 0.8 pt in the group
% colour (template §5-C 0.7–0.9 pt). Draw order: representation, NV / SITE, FULL, ORACLE pair.
% TIF = the vector PDF rasterised by poppler (jbi_export_v4). Template §2-1 sizes 14 / 15 / 16 pt.
% Run:  matlab -batch "close all force; clear; run('<repo>/figures_v4/Figure_5/make_Figure_5_v4.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style_v3();
D = jbi_read(root, 'fig5_bias_coverage');
rows = D.rows;
assert(numel(rows) == 144, 'Figure 5 expects 12 arms x 4 K x 3 P = 144 rows (288 values)');

arms = {'NV', 'SITE', 'FM-P', 'FM-P−C', 'FM-S', 'FM-S−C', 'REF', 'REF−C', 'FM-P-nat', 'ORACLE−C', 'ORACLE', 'FULL'};
assert(isequal(D.arms(:)', arms), 'arm list differs from the canonical file');
grp = [1 1 2 2 2 2 2 2 2 3 3 4];
gLs = {'--', '-', '-.', ':'};
gCol = {S.g6B, S.g8A, S.navy, S.g4D};
gLw = [0.8, 0.8, 0.9, 1.1];
openEdge = {S.g6B, S.g6B, S.navy, S.g4D};       % open-marker edge: never lighter than #6B6B6B
mk = {'v', 'v', 'o', 'o', 's', 's', '^', '^', 'p', 'd', 'd', 'h'};
filled = logical([0 1 1 0 1 0 1 0 1 0 1 1]);
msz = containers.Map({'v', 'o', 's', '^', 'p', 'd', 'h'}, {3.2, 3.2, 4.55, 3.2, 4.8, 3.2, 4.4});
eFill = 0.5; eOpen = 0.8;                       % marker edge widths (pt)
order = [find(grp == 2), find(grp == 1), find(grp == 4), find(grp == 3)];

W = S.width_cm; H = 18.4;
[fig, cv] = jbi_canvas(W, H);
axX = [2.3, 7.95, 13.6]; axW = 5.25; axH = 6.0;
axY = [H - 7.0, H - 14.0];
Ps = [0 5 30];
metric = {'rel_bias_pct', 'coverage'};
ylab = {'Relative bias (%)', '95% interval coverage'};
ylims = {[-30 205], [-0.03 1.03]};
yticks = {0:50:200, 0:0.2:1};
refY = [0, 0.95];
first = gobjects(1, numel(arms)); firstM = gobjects(1, numel(arms));
n = 0;
for i = 1:2
    for j = 1:3
        ax = jbi_axes(fig, S, [axX(j) axY(i) axW axH]);
        set(ax, 'XScale', 'log', 'XLim', [0.8 19], 'XTick', [1 2 5 15], 'XTickLabel', {'1', '2', '5', '15'}, ...
            'YLim', ylims{i}, 'YTick', yticks{i}, 'XMinorTick', 'off');
        plot(ax, [0.8 19], [refY(i) refY(i)], ':', 'Color', S.g8A, 'LineWidth', 1.0, 'Tag', 'reference');
        for a = order
            r = rows(strcmp({rows.arm}, arms{a}) & [rows.P] == Ps(j));
            [~, o] = sort([r.K]);
            r = r(o);
            assert(isequal([r.K], [1 2 5 15]));
            y = [r.(metric{i})];
            assert(all(y > ylims{i}(1) & y < ylims{i}(2)), 'value outside the y-limits');
            g = grp(a);
            if filled(a)
                face = gCol{g}; edge = S.k; ew = eFill;
            else
                face = 'w'; edge = openEdge{g}; ew = eOpen;
            end
            h = plot(ax, [r.K], y, gLs{g}, 'Color', gCol{g}, 'LineWidth', gLw(g), ...
                'Tag', sprintf('BC:%s:%s:P%d', arms{a}, metric{i}, Ps(j)), 'UserData', [[r.K]' y']);
            hm = plot(ax, [r.K], y, 'LineStyle', 'none', 'Marker', mk{a}, 'MarkerSize', msz(mk{a}), ...
                'MarkerFaceColor', face, 'MarkerEdgeColor', edge, 'LineWidth', ew, ...
                'Tag', sprintf('BCm:%s:%s:P%d', arms{a}, metric{i}, Ps(j)));
            n = n + numel(y);
            if ~isgraphics(first(a))
                first(a) = h; firstM(a) = hm;
            end
        end
        if j == 1
            ylabel(ax, ylab{i}, 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, 'Interpreter', 'none');
        else
            set(ax, 'YTickLabel', []);
        end
        if i == 1
            set(ax, 'XTickLabel', []);
            text(cv, axX(j) + axW / 2, H - 0.42, sprintf('P = %d', Ps(j)), 'FontName', S.font, 'FontSize', S.tick, ...
                'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
        end
    end
end
assert(n == 288);
jbi_panel_label(fig, S, '(A)', 0.12, H - 0.08);
jbi_panel_label(fig, S, '(B)', 0.12, axY(1) - 0.25);
text(cv, (axX(1) + axX(3) + axW) / 2, axY(2) - 1.15, 'Intervention duration K (window steps)', 'FontName', S.font, ...
    'FontSize', S.axis, 'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');

% ------------------------------------------------------------------ key: one entry per arm, glyph copied from the plot
cols = {1:2, 3:6, 7:9, 10:11, 12};               % one column per group (the representation arms in two columns)
tok = 1.0; tgap = 0.22; cgap = 0.55; dy = 0.62;
ky0 = axY(2) - 2.05;
x = 0.35;                                        % key starts at the left margin (five columns at 14 pt)
for c = 1:numel(cols)
    wmax = 0;
    for q = 1:numel(cols{c})
        a = cols{c}(q);
        h = first(a); m = firstM(a); yk = ky0 - (q - 1) * dy;
        plot(cv, x + [0 tok], [yk yk], h.LineStyle, 'Color', h.Color, 'LineWidth', h.LineWidth, 'Tag', ['key:' arms{a}]);
        plot(cv, x + tok / 2, yk, 'LineStyle', 'none', 'Marker', m.Marker, 'MarkerSize', m.MarkerSize, ...
            'MarkerFaceColor', m.MarkerFaceColor, 'MarkerEdgeColor', m.MarkerEdgeColor, 'LineWidth', m.LineWidth, ...
            'Tag', ['keymarker:' arms{a}]);
        t = text(cv, x + tok + tgap, yk, arms{a}, 'FontName', S.font, 'FontSize', S.legend, 'Color', S.k, ...
            'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle', 'Interpreter', 'none', 'Tag', ['keytext:' arms{a}]);
        wmax = max(wmax, t.Extent(3));
    end
    x = x + tok + tgap + wmax + cgap;
end
assert(x - cgap <= W - 0.1, 'key wider than the canvas');

jbi_export_v4(fig, fullfile(here, 'Figure_5_v4'), S);   % TIF from the vector PDF (poppler); see jbi_export_v4
close(fig);
fprintf('Figure_5_v4 written: %s (key ends at %.2f cm of %.2f)\n', here, x - cgap, W);
