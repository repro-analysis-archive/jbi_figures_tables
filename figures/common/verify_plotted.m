function verify_plotted(root)
%VERIFY_PLOTTED Plotted-vs-canonical check (template §7-5) and legend<->plot invariant (§5-C) for Figures 2-4.
%   Opens each saved .fig, reads every tagged marker series and the interval / bound lines, and compares them with
%   the hash-guarded canonical JSON with zero tolerance. Writes qa/plotted_vs_canonical.json.

addpath(fullfile(root, 'figures', 'common'));
out = struct();

% ------------------------------------------------------------------ Figure 2
F = jbi_read(root, 'fam_dbar'); fam = F.rows; fam = fam([fam.in_fig2A]);
B = jbi_read(root, 'fig2B_slice_D'); sl = B.rows;
h = openfig(fullfile(root, 'figures', 'Figure_2', 'Figure_2.fig'), 'invisible');
L = findall(h, 'Type', 'line');
nA = 0; nB = 0; bad = {};
for r = fam'
    m = findobj(L, 'Tag', sprintf('A:%s:%s', r.family, r.set));
    if numel(m) ~= 1 || m.XData ~= r.D_bar
        bad{end + 1} = sprintf('A marker %s %s', r.family, r.set); %#ok<AGROW>
        continue
    end
    LA = findobj(ancestor(m, 'axes'), 'Type', 'line');          % search only the marker's own axes
    ci = findobj(LA, '-function', @(o) numel(o.XData) == 2 && isequal(o.XData, [r.ci_lo r.ci_hi]) && ...
        all(o.YData == m.YData));
    if numel(ci) ~= 1, bad{end + 1} = sprintf('A interval %s %s', r.family, r.set); end %#ok<AGROW>
    nA = nA + 1;
end
pairs = {'SITE vs NV', 'ORACLE vs ORACLE−C'};
for k = 1:2
    for P = [0 5 30]
        m = findobj(L, 'Tag', sprintf('B:%s:P%d', pairs{k}, P));
        r = sl(strcmp({sl.pair}, pairs{k}) & [sl.P] == P);
        [~, o] = sort([r.K]); r = r(o);
        if numel(m) ~= 1 || ~isequal(m.XData, [r.K]) || ~isequal(m.YData, [r.D_without_minus_with])
            bad{end + 1} = sprintf('B %s P%d', pairs{k}, P); %#ok<AGROW>
        end
        nB = nB + numel(r);
    end
end
lg = findall(h, 'Type', 'legend');
legOK = all(arrayfun(@(g) all(arrayfun(@(p) ~isempty(p.XData), g.PlotChildren)), lg));
out.Figure_2 = struct('panelA_points', nA, 'panelB_points', nB, 'mismatches', {bad}, ...
    'legend_entries', {cellfun(@(c) strjoin(c, ' | '), {lg.String}, 'UniformOutput', false)}, ...
    'legend_handles_plotted', legOK, 'result', ternary(isempty(bad) && nA == 11 && nB == 24 && legOK));
close(h);

% ------------------------------------------------------------------ Figure 3
D = jbi_read(root, 'fig3_ba'); rows = D.rows;
h = openfig(fullfile(root, 'figures', 'Figure_3', 'Figure_3.fig'), 'invisible');
L = findall(h, 'Type', 'line');
n = 0; bad = {};
for r = rows'
    m = findobj(L, 'Tag', sprintf('%s:%s:%s:%s', r.block, r.key, r.set, r.probe));
    if numel(m) ~= 1 || m.YData ~= r.ba
        bad{end + 1} = sprintf('%s %s %s %s marker', r.block, r.key, r.set, r.probe); %#ok<AGROW>
        continue
    end
    x = m.XData;
    LA = findobj(ancestor(m, 'axes'), 'Type', 'line');          % search only the marker's own axes
    ci = findobj(LA, '-function', @(o) numel(o.XData) == 2 && all(o.XData == x) && isequal(o.YData, [r.lo_2p5 r.hi_97p5]));
    ub = findobj(LA, 'Tag', 'upper', '-function', @(o) abs(mean(o.XData) - x) < 1e-12 && all(o.YData == r.upper_one_sided_95));
    if numel(ci) ~= 1 || numel(ub) ~= 1
        bad{end + 1} = sprintf('%s %s %s %s interval/bound', r.block, r.key, r.set, r.probe); %#ok<AGROW>
    end
    n = n + 1;
end
lg = findall(h, 'Type', 'legend');
legOK = all(arrayfun(@(p) ~isempty(p.XData), lg.PlotChildren));
ref = [unique([findobj(L, 'LineStyle', '--').YData]) unique([findobj(L, 'LineStyle', ':').YData])];
out.Figure_3 = struct('points', n, 'mismatches', {bad}, 'legend_entries', strjoin(lg.String, ' | '), ...
    'legend_handles_plotted', legOK, 'reference_lines', ref, ...
    'result', ternary(isempty(bad) && n == 48 && legOK && isequal(ref, [0.35 0.25])));
close(h);

% ------------------------------------------------------------------ Figure 4
X = jbi_read(root, 'fig4_x_cells'); xr = X.rows;
h = openfig(fullfile(root, 'figures', 'Figure_4', 'Figure_4.fig'), 'invisible');
L = findall(h, 'Type', 'line');
cmp = {'X1', 'minusC'; 'X1', 'FM'; 'X2', 'minusC'};
arms = {'FM-P−C', 'FM-S−C', 'REF−C'};
groups = {'P1b-FM', 'P2-FM'}; x0 = [0 51];
n = 0; bad = {};
for i = 1:3
    for j = 1:3
        for g = 1:2
            m = findobj(L, 'Tag', sprintf('%s:%s:%s:%s', cmp{i, 1}, cmp{i, 2}, arms{j}, groups{g}));
            r = xr(strcmp({xr.analysis}, cmp{i, 1}) & strcmp({xr.comparison}, cmp{i, 2}) & ...
                strcmp({xr.arm}, arms{j}) & strcmp({xr.group}, groups{g}));
            [~, o] = sort([r.order_in_group]); r = r(o);
            if numel(m) ~= 1 || ~isequal(m.YData, [r.delta]) || ~isequal(m.XData, x0(g) + [r.order_in_group])
                bad{end + 1} = sprintf('%s %s %s %s markers', cmp{i, 1}, cmp{i, 2}, arms{j}, groups{g}); %#ok<AGROW>
                continue
            end
            ax = ancestor(m, 'axes');
            LI = findobj(ax, 'Type', 'line', 'Tag', '');
            for q = 1:numel(r)
                xx = x0(g) + r(q).order_in_group;
                ok = any(arrayfun(@(o) numel(o.XData) == 2 && all(o.XData == xx) && ...
                    isequal(o.YData, [r(q).delta_lo r(q).delta_hi]), LI));
                if ~ok, bad{end + 1} = sprintf('%s %s %s cell %d interval', cmp{i, 1}, cmp{i, 2}, arms{j}, r(q).cell); end %#ok<AGROW>
            end
            n = n + numel(r);
        end
    end
end
out.Figure_4 = struct('points', n, 'mismatches', {bad}, 'legend', 'none (single series type; defined in caption)', ...
    'result', ternary(isempty(bad) && n == 540));
close(h);

fid = fopen(fullfile(root, 'qa', 'plotted_vs_canonical.json'), 'w');
fwrite(fid, jsonencode(out, 'PrettyPrint', true), 'char');
fclose(fid);
fprintf('Figure_2 %s (A %d, B %d); Figure_3 %s (%d); Figure_4 %s (%d)\n', out.Figure_2.result, ...
    out.Figure_2.panelA_points, out.Figure_2.panelB_points, out.Figure_3.result, out.Figure_3.points, ...
    out.Figure_4.result, out.Figure_4.points);
end


function s = ternary(c)
if c, s = 'PASS'; else, s = 'FAIL'; end
end
