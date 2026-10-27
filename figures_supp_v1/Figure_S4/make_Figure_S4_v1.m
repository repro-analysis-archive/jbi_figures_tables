% make_Figure_S4_v1.m — Supplementary Figure S4 (supplement v6): mask check (protocol §3.1, step 3), per-centre radial
% profiles m_c(rho) of the grayscale mean standardized frame (180 points per centre), the visible radius rho_c per centre
% and the mask radius r = 0.45. Rendering source of truth; reads only hash-guarded canonical JSON
% (canonical_supplement/s4_mask_profiles.json, from the step-4 record's mask_check.json); computes nothing.
% Layout as the package figS4 (one panel per centre, free vertical scales); house palette instead of orange: profile navy
% line, rho_c solid #4D4D4D, r = 0.45 dashed #4D4D4D; the key copies the drawn objects. Template sizes 14 / 15 / 16 pt.
% Frame counts are in Table S1. TIF = the vector PDF rasterised by poppler (jbi_export_v4).
% Run:  matlab -batch "close all force; clear; run('<repo>/figures_supp_v1/Figure_S4/make_Figure_S4_v1.m')"

here = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(here));
addpath(fullfile(root, 'figures', 'common'));
S = jbi_style_v3();
D = jbi_read_supp(root, 's4_mask_profiles');
rows = D.rows;
assert(numel(rows) == 4 * 180, 'Figure S4 expects 4 centres x 180 points');
assert(D.r == 0.45);

W = S.width_cm; H = 16.0;
[fig, cv] = jbi_canvas(W, H);
centres = [2 3 4 5];
axX = [2.5, 11.1]; axW = 7.4; axH = 5.0; axY = [H - 6.3, H - 12.4];
H1 = struct(); n = 0;
for q = 1:4
    i = ceil(q / 2); j = 2 - mod(q, 2);
    r = rows([rows.centre] == centres(q));
    [~, o] = sort([r.point]); r = r(o);
    rc = D.visible_radius.(sprintf('x%d', centres(q)));
    assert(all([r.visible_radius] == rc));
    ax = jbi_axes(fig, S, [axX(j) axY(i) axW axH]);
    m = [r.m]; pad = 0.06 * (max(m) - min(m));
    yl = [min(m) - pad, max(m) + pad];
    set(ax, 'XLim', [0 0.72], 'XTick', 0:0.1:0.7, 'YLim', yl, 'XTickLabelRotation', 0);
    hR = plot(ax, [rc rc], yl, '-', 'Color', S.g4D, 'LineWidth', 1.0, 'Tag', sprintf('S4:rhoc:%d', centres(q)), ...
        'UserData', rc);
    hM = plot(ax, [D.r D.r], yl, '--', 'Color', S.g4D, 'LineWidth', 1.0, 'Tag', sprintf('S4:mask:%d', centres(q)));
    hP = plot(ax, [r.rho], m, '-', 'Color', S.navy, 'LineWidth', 1.1, 'Tag', sprintf('S4:profile:%d', centres(q)));
    n = n + numel(r);
    if q == 1
        H1.profile = hP; H1.rhoc = hR; H1.mask = hM;
    end
    if j == 1
        ylabel(ax, 'Mean gray level', 'FontName', S.font, 'FontSize', S.axis, 'Color', S.k);
    end
    if i == 1
        set(ax, 'XTickLabel', []);
    end
    text(cv, axX(j), axY(i) + axH + 0.62, sprintf('Centre %d', centres(q)), 'FontName', S.font, 'FontSize', S.axis, ...
        'Color', S.k, 'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle');
    jbi_panel_label(fig, S, sprintf('(%s)', char('A' + q - 1)), axX(j) - 2.35 * (j == 1) - 1.25 * (j == 2), ...
        axY(i) + axH + 0.92);                          % above the top y tick label
end
assert(n == 720);
text(cv, (axX(1) + axX(2) + axW) / 2, axY(2) - 1.05, 'Radius ρ (fraction of the square side)', 'FontName', S.font, ...
    'FontSize', S.axis, 'Color', S.k, 'HorizontalAlignment', 'center', 'VerticalAlignment', 'middle', 'Interpreter', 'none');

% ------------------------------------------------------------------ key: glyphs copied from the drawn objects
key = axes(fig, 'Units', 'normalized', 'Position', [0 0 W 1.7] ./ [W H W H], 'XLim', [0 W], 'YLim', [0 1.7], ...
    'Visible', 'off', 'Tag', 'key');
hold(key, 'on');
src = {H1.profile, H1.rhoc, H1.mask}; tg = {'key:profile', 'key:rhoc', 'key:mask'};
lab = {'Radial profile m_c(ρ)', 'Visible radius ρ_c', 'Mask radius r = 0.45'};
kx = [0.6, 9.6, 0.6]; ky = [1.15, 1.15, 0.5]; gw = 1.4;   % two rows (the three labels do not fit one row at 14 pt)
for q = 1:3
    l = src{q};
    plot(key, kx(q) + [0 gw], [ky(q) ky(q)], l.LineStyle, 'Color', l.Color, 'LineWidth', l.LineWidth, 'Tag', tg{q});
    text(key, kx(q) + gw + 0.25, ky(q), lab{q}, 'FontName', S.font, 'FontSize', S.legend, 'Color', S.k, ...
        'HorizontalAlignment', 'left', 'VerticalAlignment', 'middle', 'Interpreter', 'tex');
end

jbi_export_v4(fig, fullfile(here, 'Figure_S4_v1'), S);   % TIF from the vector PDF (poppler)
close(fig);
fprintf('Figure_S4_v1 written: %s\n', here);
