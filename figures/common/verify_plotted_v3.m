function verify_plotted_v3(root)
%VERIFY_PLOTTED_V3 Plotted-vs-canonical (zero tolerance) and legend/key <-> plot checks for the v4-revision data
%   figures (figures_v3/Figure_2..4; same checks as verify_plotted_v2; Figure 5 is unchanged in v4).
%   Writes qa/plotted_vs_canonical_v3.json.

addpath(fullfile(root, 'figures', 'common'));
out = struct();
fv = @(n) fullfile(root, 'figures_v3', sprintf('Figure_%d', n), sprintf('Figure_%d_v3.fig', n));

% ------------------------------------------------------------------ Figure 2 v3 (forest)
F = jbi_read(root, 'fam_dbar'); fam = F.rows; fam = fam([fam.in_fig2A]);
h = openfig(fv(2), 'invisible'); L = findall(h, 'Type', 'line'); bad = {}; n = 0;
for r = fam'
    m = findobj(L, 'Tag', sprintf('A:%s:%s', r.family, r.set));
    if numel(m) ~= 1 || m.XData ~= r.D_bar, bad{end + 1} = sprintf('%s %s marker', r.family, r.set); continue; end %#ok<AGROW>
    LA = findobj(ancestor(m, 'axes'), 'Type', 'line');
    ci = findobj(LA, '-function', @(o) numel(o.XData) == 2 && isequal(o.XData, [r.ci_lo r.ci_hi]) && all(o.YData == m.YData));
    if numel(ci) ~= 1, bad{end + 1} = sprintf('%s %s interval', r.family, r.set); end %#ok<AGROW>
    n = n + 1;
end
lg = findall(h, 'Type', 'legend');
legOK = numel(lg) == 1 && all(arrayfun(@(p) ~isempty(p.XData), lg.PlotChildren)) && numel(lg.String) == 4;
out.Figure_2 = struct('points', n, 'mismatches', {bad}, 'legend_entries', strjoin(lg.String, ' | '), ...
    'legend_handles_plotted', legOK, 'result', tern(isempty(bad) && n == 11 && legOK));
close(h);

% ------------------------------------------------------------------ Figure 3 v3 (prior action history)
D = jbi_read(root, 'w_history_D'); hr = D.rows;
h = openfig(fv(3), 'invisible'); L = findall(h, 'Type', 'line'); bad = {}; n = 0;
pairs = {'SITE vs NV', 'ORACLE vs ORACLE−C'};
for k = 1:2
    for Wv = [0 5 30]
        for P = [0 5 30]
            m = findobj(L, 'Tag', sprintf('H:%s:W%d:P%d', pairs{k}, Wv, P));
            r = hr(strcmp({hr.pair}, pairs{k}) & [hr.W] == Wv & [hr.P] == P);
            [~, o] = sort([r.K]); r = r(o);
            if numel(m) ~= 1 || ~isequal(m.XData, [r.K]) || ~isequal(m.YData, [r.D_without_minus_with])
                bad{end + 1} = sprintf('%s W%d P%d', pairs{k}, Wv, P); %#ok<AGROW>
            end
            n = n + numel(r);
        end
    end
end
zl = findobj(L, 'LineStyle', ':', '-function', @(o) all(o.YData == 0));
lg = findall(h, 'Type', 'legend');
legOK = numel(lg) == 1 && all(arrayfun(@(p) ~isempty(p.XData), lg.PlotChildren)) && isequal(lg.String, {'P = 0', 'P = 5', 'P = 30'});
out.Figure_3 = struct('points', n, 'mismatches', {bad}, 'zero_lines', numel(zl), 'legend_entries', ...
    strjoin(lg.String, ' | '), 'legend_handles_plotted', legOK, 'result', tern(isempty(bad) && n == 72 && numel(zl) == 6 && legOK));
close(h);

% ------------------------------------------------------------------ Figure 4 v3 (erasure) + key
B = jbi_read(root, 'fig3_ba'); rows = B.rows;
h = openfig(fv(4), 'invisible'); L = findall(h, 'Type', 'line'); bad = {}; n = 0;
for r = rows'
    m = findobj(L, 'Tag', sprintf('%s:%s:%s:%s', r.block, r.key, r.set, r.probe));
    if numel(m) ~= 1 || m.YData ~= r.ba, bad{end + 1} = sprintf('%s %s %s %s marker', r.block, r.key, r.set, r.probe); continue; end %#ok<AGROW>
    x = m.XData; LA = findobj(ancestor(m, 'axes'), 'Type', 'line');
    ci = findobj(LA, 'Tag', 'interval', '-function', @(o) all(o.XData == x) && isequal(o.YData, [r.lo_2p5 r.hi_97p5]));
    ub = findobj(LA, 'Tag', 'upper', '-function', @(o) abs(mean(o.XData) - x) < 1e-12 && all(o.YData == r.upper_one_sided_95));
    if numel(ci) ~= 1 || numel(ub) ~= 1, bad{end + 1} = sprintf('%s %s %s %s interval/bound', r.block, r.key, r.set, r.probe); end %#ok<AGROW>
    n = n + 1;
end
% key <-> plot: every key glyph copies the properties of a plotted object, and every plotted object class has a glyph
K = findall(h, 'Type', 'line', '-regexp', 'Tag', '^key:');
P = setdiff(L, K);
same = @(a, b, props) all(cellfun(@(q) isequal(a.(q), b.(q)), props));
kOK = true; kmsg = {};
for k = K'
    switch k.Tag
        case 'key:marker'
            c = findobj(P, '-regexp', 'Tag', ':(linear|mlp)$', 'Marker', k.Marker);
            ok = ~isempty(c) && same(k, c(1), {'Marker', 'MarkerSize', 'MarkerFaceColor', 'MarkerEdgeColor', 'LineWidth'});
            glyph = 'marker';
        case 'key:interval'
            c = findobj(P, 'Tag', 'interval', 'Color', k.Color);
            ok = ~isempty(c) && same(k, c(1), {'Color', 'LineWidth', 'LineStyle'}) && diff(k.XData) == 0 && diff(k.YData) > 0;
            glyph = 'vertical bar';
        case 'key:upper'
            c = findobj(P, 'Tag', 'upper', 'Color', k.Color);
            ok = ~isempty(c) && same(k, c(1), {'Color', 'LineWidth', 'LineStyle'}) && diff(k.YData) == 0;
            glyph = 'horizontal tick';
        case 'key:boundary'
            c = findobj(P, 'Tag', 'boundary'); ok = ~isempty(c) && same(k, c(1), {'Color', 'LineWidth', 'LineStyle'}); glyph = 'dashed line';
        case 'key:chance'
            c = findobj(P, 'Tag', 'chance'); ok = ~isempty(c) && same(k, c(1), {'Color', 'LineWidth', 'LineStyle'}); glyph = 'dotted line';
        otherwise
            ok = false; glyph = '?';
    end
    kOK = kOK && ok; kmsg{end + 1} = sprintf('%s (%s): %s', k.Tag, glyph, tern(ok)); %#ok<AGROW>
end
classes = {'interval', 'upper', 'boundary', 'chance'};
plottedClasses = all(cellfun(@(t) ~isempty(findobj(P, 'Tag', t)), classes));
keyClasses = all(cellfun(@(t) ~isempty(findobj(K, 'Tag', ['key:' t])), [classes {'marker'}]));
nKeyMarker = numel(findobj(K, 'Tag', 'key:marker'));
out.Figure_4 = struct('points', n, 'mismatches', {bad}, 'key_glyphs', {kmsg}, ...
    'key_covers_every_plotted_class', plottedClasses && keyClasses && nKeyMarker == 2, ...
    'result', tern(isempty(bad) && n == 48 && kOK && plottedClasses && keyClasses && nKeyMarker == 2));
close(h);

fid = fopen(fullfile(root, 'qa', 'plotted_vs_canonical_v3.json'), 'w');
fwrite(fid, jsonencode(out, 'PrettyPrint', true), 'char'); fclose(fid);
fprintf('Figure_2_v3 %s (%d); Figure_3_v3 %s (%d); Figure_4_v3 %s (%d; key %s)\n', ...
    out.Figure_2.result, out.Figure_2.points, out.Figure_3.result, out.Figure_3.points, out.Figure_4.result, ...
    out.Figure_4.points, tern(out.Figure_4.key_covers_every_plotted_class));
end


function s = tern(c)
if c, s = 'PASS'; else, s = 'FAIL'; end
end
