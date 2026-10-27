function verify_plotted_v4(root)
%VERIFY_PLOTTED_V4 Plotted-vs-canonical (zero tolerance) and key <-> plot checks for the new Figure 5 of the v5
%   revision (figures_v4/Figure_5/Figure_5_v4.fig): all 288 values (12 arms x 12 cells x 2 metrics) as line and marker
%   objects, 12 line series and 12 marker series per panel, one reference line per panel (0 / 0.95), and a key of 12
%   entries whose line, marker and text copy the plotted objects of that arm. The renumbered figures are byte copies
%   and are checked by hash (scripts/renumber_v5.py). Writes qa/plotted_vs_canonical_v4.json.

addpath(fullfile(root, 'figures', 'common'));
D = jbi_read(root, 'fig5_bias_coverage'); rows = D.rows; arms = D.arms(:)';
h = openfig(fullfile(root, 'figures_v4', 'Figure_5', 'Figure_5_v4.fig'), 'invisible');
L = findall(h, 'Type', 'line');
metric = {'rel_bias_pct', 'coverage'}; refY = [0 0.95]; Ps = [0 5 30];
bad = {}; n = 0; panels = {};
for i = 1:2
    for j = 1:3
        nl = 0; nm = 0; axs = [];
        for a = 1:numel(arms)
            r = rows(strcmp({rows.arm}, arms{a}) & [rows.P] == Ps(j));
            [~, o] = sort([r.K]); r = r(o); y = [r.(metric{i})];
            ln = findobj(L, 'Tag', sprintf('BC:%s:%s:P%d', arms{a}, metric{i}, Ps(j)));
            mk = findobj(L, 'Tag', sprintf('BCm:%s:%s:P%d', arms{a}, metric{i}, Ps(j)));
            if numel(ln) ~= 1 || numel(mk) ~= 1 || ~isequal(ln.XData, [r.K]) || ~isequal(ln.YData, y) || ...
                    ~isequal(mk.XData, [r.K]) || ~isequal(mk.YData, y) || ~strcmp(mk.LineStyle, 'none') || ...
                    strcmp(ln.Marker, 'none') == false
                bad{end + 1} = sprintf('%s %s P%d', arms{a}, metric{i}, Ps(j)); %#ok<AGROW>
                continue
            end
            nl = nl + 1; nm = nm + 1; n = n + numel(y);
            axs = [axs ancestor(ln, 'axes')]; %#ok<AGROW>
        end
        ax = unique(axs);
        ok1 = numel(ax) == 1;
        if ok1
            LA = findobj(ax, 'Type', 'line');
            series = findobj(LA, '-regexp', 'Tag', '^BC:'); markers = findobj(LA, '-regexp', 'Tag', '^BCm:');
            ref = findobj(LA, 'Tag', 'reference');
            ok1 = numel(series) == 12 && numel(markers) == 12 && numel(ref) == 1 && all(ref.YData == refY(i)) && ...
                numel(LA) == 25;
        end
        panels{end + 1} = sprintf('%s P = %d: %d lines, %d marker series, reference %s', metric{i}, Ps(j), nl, nm, ...
            tern(ok1)); %#ok<AGROW>
        if ~ok1, bad{end + 1} = sprintf('panel %s P%d', metric{i}, Ps(j)); end %#ok<AGROW>
    end
end
% key <-> plot
K = findall(h, 'Type', 'line', '-regexp', 'Tag', '^key:'); KM = findall(h, 'Type', 'line', '-regexp', 'Tag', '^keymarker:');
KT = findall(h, 'Type', 'text', '-regexp', 'Tag', '^keytext:');
same = @(a, b, props) all(cellfun(@(q) isequal(a.(q), b.(q)), props));
kmsg = {}; kOK = numel(K) == 12 && numel(KM) == 12 && numel(KT) == 12;
for a = 1:numel(arms)
    k = findobj(K, 'Tag', ['key:' arms{a}]); km = findobj(KM, 'Tag', ['keymarker:' arms{a}]);
    kt = findobj(KT, 'Tag', ['keytext:' arms{a}]);
    ln = findobj(L, 'Tag', sprintf('BC:%s:rel_bias_pct:P0', arms{a}));
    mk = findobj(L, 'Tag', sprintf('BCm:%s:rel_bias_pct:P0', arms{a}));
    ok = numel(k) == 1 && numel(km) == 1 && numel(kt) == 1 && strcmp(kt.String, arms{a}) && ...
        same(k, ln, {'LineStyle', 'Color', 'LineWidth'}) && ...
        same(km, mk, {'Marker', 'MarkerSize', 'MarkerFaceColor', 'MarkerEdgeColor', 'LineWidth'});
    % every panel draws the arm with the same style as the key
    for i = 1:2
        for j = 1:3
            l2 = findobj(L, 'Tag', sprintf('BC:%s:%s:P%d', arms{a}, metric{i}, Ps(j)));
            m2 = findobj(L, 'Tag', sprintf('BCm:%s:%s:P%d', arms{a}, metric{i}, Ps(j)));
            ok = ok && same(l2, ln, {'LineStyle', 'Color', 'LineWidth'}) && ...
                same(m2, mk, {'Marker', 'MarkerSize', 'MarkerFaceColor', 'MarkerEdgeColor', 'LineWidth'});
        end
    end
    kOK = kOK && ok; kmsg{end + 1} = sprintf('%s: %s', arms{a}, tern(ok)); %#ok<AGROW>
end
% the 12 (line style, colour, marker, face) combinations are distinct
sig = cellfun(@(a) sprintf('%s|%s|%s|%s', findobj(K, 'Tag', ['key:' a]).LineStyle, ...
    mat2str(findobj(K, 'Tag', ['key:' a]).Color), findobj(KM, 'Tag', ['keymarker:' a]).Marker, ...
    mat2str(double(findobj(KM, 'Tag', ['keymarker:' a]).MarkerFaceColor))), arms, 'UniformOutput', false);
distinct = numel(unique(sig)) == 12;
out.Figure_5 = struct('points', n, 'mismatches', {bad}, 'panels', {panels}, 'key_entries', {kmsg}, ...
    'key_entries_n', numel(K), 'key_glyphs_distinct', distinct, ...
    'result', tern(isempty(bad) && n == 288 && kOK && distinct));
close(h);
fid = fopen(fullfile(root, 'qa', 'plotted_vs_canonical_v4.json'), 'w');
fwrite(fid, jsonencode(out, 'PrettyPrint', true), 'char'); fclose(fid);
fprintf('Figure_5_v4 %s (%d values; key %d entries %s; distinct %s)\n', out.Figure_5.result, n, numel(K), tern(kOK), ...
    tern(distinct));
end


function s = tern(c)
if c, s = 'PASS'; else, s = 'FAIL'; end
end
