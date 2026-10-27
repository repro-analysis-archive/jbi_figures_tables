% make_Figure_2.m — Figure 2 (confirmatory families) for the JBI manuscript.
% Rendering source of truth (template §4-0). Reads only hash-guarded canonical JSON; computes nothing.
%   (A) family mean D with 95 % percentile bootstrap intervals, P1a / P1b-SITE (left facet) and P2-SITE /
%       P2-ORACLE (right facet), primary set and the §10.3 sensitivity sets (grouped forest, template §5-C).
%   (B) per-cell D (|bias| without C − with C, / mean truth) against K, one line per P, at the main-text slice
%       W = 30, alpha = 0.5, gamma = 1, phi_A = 0 (primary set): SITE vs NV and ORACLE vs ORACLE−C.
% Run:  matlab -batch "close all force; clear; run('<repo>/figures/Figure_2/make_Figure_2.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style();
F = jbi_read(root, 'fam_dbar');
B = jbi_read(root, 'fig2B_slice_D');
fam = F.rows;
fam = fam([fam.in_fig2A]);
assert(numel(fam) == 11, 'Figure 2A expects 11 family x set points');

W = S.width_cm; H = 11.2;
[fig, cv] = jbi_canvas(W, H);

% ------------------------------------------------------------------------------------------------- (A)
sets = {'primary', 'W0', 'W5', 'single_file'};
setName = {'Primary set (n = 158)', 'W = 0 set (n = 204)', 'W = 5 set (n = 201)', 'Single-file set (n = 123)'};
mk = {'o', 's', '^', 'd'};
msz = [2.6, 3.7, 2.6, 2.6];                         % pt; measured from the PDF in qa/
face = {S.navy, 'w', 'w', 'w'};
edge = {S.k, S.g4D, S.g4D, S.g4D};
ciCol = {S.navy, S.g6B, S.g6B, S.g6B};
mlw = [0.6, 0.75, 0.75, 0.75];
off = [0.27, 0.09, -0.09, -0.27];                   % row-internal offsets (template §5-C)
facets = {{'P1a', 'P1b-SITE'}, {'P2-SITE', 'P2-ORACLE'}};
xl = {[-0.1 2.4], [-0.005 0.1]};
xt = {0:0.5:2, 0:0.02:0.1};
xlab = {'Mean D (without C − with C)', 'Mean D (with C − without C)'};
axA = gobjects(1, 2);
legH = gobjects(1, 4);
nPlotted = zeros(1, 4);
axX = [3.35, 12.85]; axW = 5.85; axY = 6.95; axH = 3.05;
for k = 1:2
    ax = jbi_axes(fig, S, [axX(k) axY axW axH]);
    axA(k) = ax;
    fams = facets{k};
    set(ax, 'XLim', xl{k}, 'XTick', xt{k}, 'YLim', [0.45 2.55], 'YTick', []);
    ax.YAxis.Visible = 'on';
    plot(ax, [0 0], [0.45 2.55], ':', 'Color', S.g8A, 'LineWidth', 0.9);          % zero reference
    for f = 1:2
        yf = 3 - f;                                                                % first family on top
        for s = 1:4
            r = fam(strcmp({fam.family}, fams{f}) & strcmp({fam.set}, sets{s}));
            if isempty(r)
                continue                                                            % not defined in that set
            end
            assert(numel(r) == 1);
            y = yf + off(s);
            plot(ax, [r.ci_lo r.ci_hi], [y y], '-', 'Color', ciCol{s}, 'LineWidth', 1.0);
            h = plot(ax, r.D_bar, y, mk{s}, 'MarkerSize', msz(s), 'MarkerFaceColor', face{s}, ...
                'MarkerEdgeColor', edge{s}, 'LineWidth', mlw(s), 'LineStyle', 'none', ...
                'DisplayName', setName{s}, 'Tag', sprintf('A:%s:%s', r.family, r.set), ...
                'UserData', [r.D_bar r.ci_lo r.ci_hi]);
            nPlotted(s) = nPlotted(s) + 1;
            if ~isgraphics(legH(s))
                legH(s) = h;
            end
        end
        % category label: family name, then the comparison (separate text objects; template note on PDF/TIF)
        yn = (yf - 0.45) / 2.1;
        cmp = fam(strcmp({fam.family}, fams{f}));
        text(ax, -0.025, yn + 0.055, fams{f}, 'Units', 'normalized', 'HorizontalAlignment', 'right', ...
            'VerticalAlignment', 'middle', 'FontName', S.font, 'FontSize', S.tick, 'Color', S.k);
        text(ax, -0.025, yn - 0.075, cmp(1).comparison, 'Units', 'normalized', 'HorizontalAlignment', 'right', ...
            'VerticalAlignment', 'middle', 'FontName', S.font, 'FontSize', S.small, 'Color', S.g4D);
    end
    xlabel(ax, xlab{k}, 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, 'Interpreter', 'none');
end
assert(all(nPlotted > 0), 'orphan legend entry: a set has no plotted point');
lgA = legend(axA(1), legH, setName, 'Orientation', 'horizontal', 'Box', 'off', 'FontName', S.font, ...
    'FontSize', S.legend, 'TextColor', S.k, 'AutoUpdate', 'off');
lgA.ItemTokenSize = [10 8];
lgA.Units = 'centimeters';
lgA.Position(1:2) = [3.35, 10.28];
jbi_panel_label(fig, S, '(A)', 0.12, H - 0.08);

% ------------------------------------------------------------------------------------------------- (B)
rows = B.rows;
pairs = {'SITE vs NV', 'ORACLE vs ORACLE−C'};
Ps = [0 5 30];
pMk = {'o', 's', '^'};
pMs = [2.2, 3.0, 2.4];
pLs = {'-', '--', ':'};
pName = {'P = 0', 'P = 5', 'P = 30'};
axB = gobjects(1, 2);
legB = gobjects(1, 3);
bX = [2.0, 10.75]; bW = 7.9; bY = 1.25; bH = 3.35;
for k = 1:2
    ax = jbi_axes(fig, S, [bX(k) bY bW bH]);
    axB(k) = ax;
    set(ax, 'XScale', 'log', 'XLim', [0.8 19], 'XTick', [1 2 5 15], 'XTickLabel', {'1', '2', '5', '15'}, ...
        'YLim', [-0.06 0.08], 'YTick', -0.05:0.05:0.05, 'XMinorTick', 'off');
    plot(ax, [0.8 19], [0 0], ':', 'Color', S.g8A, 'LineWidth', 0.9);
    pr = rows(strcmp({rows.pair}, pairs{k}));
    assert(numel(pr) == 12);
    for j = 1:3
        r = pr([pr.P] == Ps(j));
        [~, o] = sort([r.K]);
        r = r(o);
        assert(isequal([r.K], [1 2 5 15]));
        h = plot(ax, [r.K], [r.D_without_minus_with], pLs{j}, 'Color', S.navy, 'LineWidth', 0.9, ...
            'Marker', pMk{j}, 'MarkerSize', pMs(j), 'MarkerFaceColor', S.navy, 'MarkerEdgeColor', S.k, ...
            'DisplayName', pName{j}, 'Tag', sprintf('B:%s:P%d', pairs{k}, Ps(j)), ...
            'UserData', [[r.K]' [r.D_without_minus_with]']);
        if k == 1
            legB(j) = h;
        end
    end
    title(ax, pairs{k}, 'FontName', S.font, 'FontSize', S.tick, 'FontWeight', 'normal', 'Color', S.k, ...
        'Interpreter', 'none');
    ax.TitleHorizontalAlignment = 'left';
end
ylabel(axB(1), 'D (without C − with C)', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, ...
    'Interpreter', 'none');
set(axB(2), 'YTickLabel', []);
text(cv, (bX(1) + bX(2) + bW) / 2, 0.32, 'Intervention duration K (window steps)', 'FontName', S.font, ...
    'FontSize', S.axis, 'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle');
lgB = legend(axB(1), legB, pName, 'Orientation', 'horizontal', 'Box', 'off', 'FontName', S.font, ...
    'FontSize', S.legend, 'TextColor', S.k, 'AutoUpdate', 'off');
lgB.ItemTokenSize = [18 8];
lgB.Units = 'centimeters';
lgB.Position(1:2) = [2.0, 5.08];
jbi_panel_label(fig, S, '(B)', 0.12, 5.62);

% ------------------------------------------------------------------------------------------------- export
jbi_export(fig, fullfile(here, 'Figure_2'), S);
close(fig);
fprintf('Figure_2 written: %s\n', here);
