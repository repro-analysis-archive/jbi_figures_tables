% make_Figure_2_v2.m — Figure 2 (v3 revision): confirmatory families, grouped forest only (old Figure 2A).
% Rendering source of truth. Reads only hash-guarded canonical JSON; computes nothing. Template §2-1 sizes:
% tick 14 / axis 15 / panel 16 pt at 190 mm. Facets stacked: (A) P1 families, (B) P2 families, each full width with
% its own horizontal scale (equal physical width). Same shapes and inferential-role coding as v2.
% Run:  matlab -batch "close all force; clear; run('<repo>/figures_v2/Figure_2/make_Figure_2_v2.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style_v3();
F = jbi_read(root, 'fam_dbar');
fam = F.rows;
fam = fam([fam.in_fig2A]);
assert(numel(fam) == 11, 'Figure 2 expects 11 family x set points');

W = S.width_cm; H = 14.8;
[fig, cv] = jbi_canvas(W, H);

sets = {'primary', 'W0', 'W5', 'single_file'};
setName = {'Primary set (n = 158)', 'W = 0 set (n = 204)', 'W = 5 set (n = 201)', 'Single-file set (n = 123)'};
mk = {'o', 's', '^', 'd'};
msz = [2.6, 3.7, 2.6, 2.6];
face = {S.navy, 'w', 'w', 'w'};
edge = {S.k, S.g4D, S.g4D, S.g4D};
ciCol = {S.navy, S.g6B, S.g6B, S.g6B};
mlw = [0.6, 0.75, 0.75, 0.75];
off = [0.27, 0.09, -0.09, -0.27];
facets = {{'P1a', 'P1b-SITE'}, {'P2-SITE', 'P2-ORACLE'}};
xl = {[-0.1 2.4], [-0.005 0.1]};
xt = {0:0.5:2, 0:0.02:0.1};
xlab = {'Mean D (without C − with C)', 'Mean D (with C − without C)'};
axX = 6.35; axW = 12.2; axH = 4.1;
axY = [H - 6.25, H - 13.0];
labTop = [H - 0.08, H - 8.25];
legH = gobjects(1, 4);
nPlotted = zeros(1, 4);
axs = gobjects(1, 2);
for k = 1:2
    ax = jbi_axes(fig, S, [axX axY(k) axW axH]);
    axs(k) = ax;
    fams = facets{k};
    set(ax, 'XLim', xl{k}, 'XTick', xt{k}, 'YLim', [0.45 2.55], 'YTick', []);
    plot(ax, [0 0], [0.45 2.55], ':', 'Color', S.g8A, 'LineWidth', 1.0);
    for f = 1:2
        yf = 3 - f;
        for s = 1:4
            r = fam(strcmp({fam.family}, fams{f}) & strcmp({fam.set}, sets{s}));
            if isempty(r)
                continue
            end
            assert(numel(r) == 1);
            y = yf + off(s);
            plot(ax, [r.ci_lo r.ci_hi], [y y], '-', 'Color', ciCol{s}, 'LineWidth', 1.1);
            h = plot(ax, r.D_bar, y, mk{s}, 'MarkerSize', msz(s), 'MarkerFaceColor', face{s}, ...
                'MarkerEdgeColor', edge{s}, 'LineWidth', mlw(s), 'LineStyle', 'none', ...
                'DisplayName', setName{s}, 'Tag', sprintf('A:%s:%s', r.family, r.set), ...
                'UserData', [r.D_bar r.ci_lo r.ci_hi]);
            nPlotted(s) = nPlotted(s) + 1;
            if ~isgraphics(legH(s))
                legH(s) = h;
            end
        end
        yn = (yf - 0.45) / 2.1;
        cmp = fam(strcmp({fam.family}, fams{f}));
        text(ax, -0.02, yn + 0.075, fams{f}, 'Units', 'normalized', 'HorizontalAlignment', 'right', ...
            'VerticalAlignment', 'middle', 'FontName', S.font, 'FontSize', S.tick, 'Color', S.k);
        text(ax, -0.02, yn - 0.085, cmp(1).comparison, 'Units', 'normalized', 'HorizontalAlignment', 'right', ...
            'VerticalAlignment', 'middle', 'FontName', S.font, 'FontSize', S.tick, 'Color', S.g4D);
    end
    xlabel(ax, xlab{k}, 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k, 'Interpreter', 'none');
    jbi_panel_label(fig, S, sprintf('(%s)', char('A' + k - 1)), 0.12, labTop(k));
end
assert(all(nPlotted > 0), 'orphan legend entry: a set has no plotted point');
lg = legend(axs(1), legH, setName, 'NumColumns', 2, 'Box', 'off', 'FontName', S.font, ...
    'FontSize', S.legend, 'TextColor', S.k, 'AutoUpdate', 'off');
lg.ItemTokenSize = [12 10];
lg.Units = 'centimeters';
lg.Position(1:2) = [axX - 0.2, H - 1.75];

jbi_export(fig, fullfile(here, 'Figure_2_v2'), S);
close(fig);
fprintf('Figure_2_v2 written: %s\n', here);
