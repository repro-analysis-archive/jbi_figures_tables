function verify_plotted_supp_v6(root)
%VERIFY_PLOTTED_SUPP_V6 Plotted-vs-canonical (zero tolerance) and key checks of the supplementary figures (v6):
%   S1 (5 pairs x 240 cells), S2 and S3 (12 arms x 240 cells): every cell rectangle and text on every page .fig — value
%   (UserData) equal to the canonical value, text equal to the canonical display string, face colour equal to the class
%   colour of the value (jbi_ramp_v6), no extra or missing cell; the key shows every class colour in order.
%   S5 (756 values): markers (value, cell order, x position) and their interval lines. S6 (36 points): marker, interval,
%   upper-bound tick; key glyphs copy the plotted objects (as verify_plotted_v2 for main Figure 2).
%   Writes qa/plotted_vs_canonical_supp_v6.json.

addpath(fullfile(root, 'figures', 'common'));
S = jbi_style_v3();
out = struct();
spec = {'S1', 's1_contrast_D', 'pair', 'D', 'D_disp', 'D'; ...
        'S2', 's23_bias_coverage', 'arm', 'rel_bias_pct', 'rel_bias_disp', 'rb'; ...
        'S3', 's23_bias_coverage', 'arm', 'coverage', 'coverage_disp', 'cov'};
for f = 1:3
    which = spec{f, 1}; C = jbi_read_supp(root, spec{f, 2}); rows = C.rows; R = jbi_ramp_v6(spec{f, 6}, S);
    if f == 1, groups = unique({rows.pair}, 'stable'); else, groups = C.arms(:)'; end
    bad = {}; n = 0; p = 0; keyok = true;
    for g = 1:numel(groups)
        for phi = [0 0.5]
            p = p + 1;
            exp = rows(strcmp({rows.(spec{f, 3})}, groups{g}) & [rows.phi] == phi);
            h = openfig(fullfile(root, 'figures_supp_v1', ['Figure_' which], 'pages', sprintf('Figure_%s_v1_p%02d.fig', which, p)), 'invisible');
            tp = sprintf('%s:p%02d', which, p);
            rects = findall(h, 'Type', 'rectangle', '-regexp', 'Tag', ['^rect:' tp ':']);
            texts = findall(h, 'Type', 'text', '-regexp', 'Tag', ['^text:' tp ':']);
            if numel(rects) ~= numel(exp) || numel(texts) ~= numel(exp)
                bad{end + 1} = sprintf('%s page %d: %d rects, %d texts for %d cells', which, p, numel(rects), numel(texts), numel(exp)); %#ok<AGROW>
            end
            for q = 1:numel(exp)
                e = exp(q); v = e.(spec{f, 4});
                rc = findobj(rects, 'Tag', sprintf('rect:%s:%d', tp, e.cell));
                tx = findobj(texts, 'Tag', sprintf('text:%s:%d', tp, e.cell));
                ok = numel(rc) == 1 && numel(tx) == 1 && rc.UserData == v && tx.UserData == v && ...
                    strcmp(tx.String, e.(spec{f, 5})) && isequal(rc.FaceColor, R.colours(R.cls(v), :));
                if ~ok, bad{end + 1} = sprintf('%s page %d cell %d', which, p, e.cell); end %#ok<AGROW>
                n = n + 1;
            end
            ks = findall(h, 'Type', 'rectangle', '-regexp', 'Tag', '^key:');
            kc = cell2mat(arrayfun(@(q) findobj(ks, 'Tag', sprintf('key:%d', q)).FaceColor, (1:numel(ks))', 'UniformOutput', false));
            keyok = keyok && numel(ks) == size(R.colours, 1) && isequal(kc, R.colours);
            close(h);
        end
    end
    out.(['Figure_' which]) = struct('pages', p, 'values', n, 'mismatches', {bad}, 'key_classes', size(R.colours, 1), ...
        'key_complete', keyok, 'result', tern(isempty(bad) && keyok && n == numel(rows)));
end

% ------------------------------------------------------------------ S5
X = jbi_read_supp(root, 's5_x_cells'); xr = X.rows; bad = {}; n = 0;
for p = 1:4
    h = openfig(fullfile(root, 'figures_supp_v1', 'Figure_S5', 'pages', sprintf('Figure_S5_v1_p%02d.fig', p)), 'invisible');
    L = findall(h, 'Type', 'line', '-regexp', 'Tag', '^S5:');
    for m = L'
        t = split(m.Tag, ':');                          % S5:analysis:comparison:arm:group
        e = xr(strcmp({xr.analysis}, t{2}) & strcmp({xr.comparison}, t{3}) & strcmp({xr.arm}, t{4}) & ...
            strcmp({xr.group}, t{5}) & strcmp({xr.page}, tern2(p == 1, 'slice', 'all')));
        [~, o] = sort([e.order]); e = e(o);
        u = m.UserData;
        if ~isequal(u(:, 1)', [e.cell]) || ~isequal(m.YData, [e.delta]) || ~isequal(m.XData, u(:, 5)')
            bad{end + 1} = sprintf('page %d %s markers', p, m.Tag); continue %#ok<AGROW>
        end
        I = findall(h, 'Type', 'line', 'Tag', ['i' m.Tag]);
        for q = 1:numel(e)
            okq = any(arrayfun(@(o) all(o.XData == m.XData(q)) && isequal(o.YData, [e(q).delta_lo e(q).delta_hi]), I));
            if ~okq, bad{end + 1} = sprintf('page %d %s cell %d interval', p, m.Tag, e(q).cell); end %#ok<AGROW>
        end
        n = n + numel(e);
    end
    close(h);
end
out.Figure_S5 = struct('pages', 4, 'values', n, 'mismatches', {bad}, 'result', tern(isempty(bad) && n == numel(xr)));

% ------------------------------------------------------------------ S6
B = jbi_read_supp(root, 's6_b'); br = B.rows; bad = {}; n = 0;
h = openfig(fullfile(root, 'figures_supp_v1', 'Figure_S6', 'Figure_S6_v1.fig'), 'invisible'); L = findall(h, 'Type', 'line');
for r = br'
    m = findobj(L, 'Tag', sprintf('B:%s:%s:%s:%s', r.key, r.analysis, r.probe, r.set));
    if numel(m) ~= 1 || m.YData ~= r.ba, bad{end + 1} = sprintf('%s %s %s %s marker', r.key, r.analysis, r.probe, r.set); continue; end %#ok<AGROW>
    x = m.XData; LA = findobj(ancestor(m, 'axes'), 'Type', 'line');
    ci = findobj(LA, 'Tag', 'interval', '-function', @(o) all(o.XData == x) && isequal(o.YData, [r.lo_2p5 r.hi_97p5]));
    ub = findobj(LA, 'Tag', 'upper', '-function', @(o) abs(mean(o.XData) - x) < 1e-12 && all(o.YData == r.upper_one_sided_95));
    if numel(ci) ~= 1 || numel(ub) ~= 1, bad{end + 1} = sprintf('%s %s %s %s interval/bound', r.key, r.analysis, r.probe, r.set); end %#ok<AGROW>
    n = n + 1;
end
K = findall(h, 'Type', 'line', '-regexp', 'Tag', '^key:'); P = setdiff(L, K);
same = @(a, b, props) all(cellfun(@(q) isequal(a.(q), b.(q)), props));
kOK = numel(K) == 8;
for k = K'
    switch k.Tag
        case 'key:marker'
            c = findobj(P, '-regexp', 'Tag', ':(linear|mlp):', 'Marker', k.Marker);
            ok = ~isempty(c) && same(k, c(1), {'Marker', 'MarkerSize', 'MarkerFaceColor', 'MarkerEdgeColor', 'LineWidth'});
        case 'key:interval'
            c = findobj(P, 'Tag', 'interval', 'Color', k.Color); ok = ~isempty(c) && same(k, c(1), {'Color', 'LineWidth', 'LineStyle'});
        case 'key:upper'
            c = findobj(P, 'Tag', 'upper', 'Color', k.Color); ok = ~isempty(c) && same(k, c(1), {'Color', 'LineWidth', 'LineStyle'});
        case {'key:boundary', 'key:chance'}
            c = findobj(P, 'Tag', k.Tag(5:end)); ok = ~isempty(c) && same(k, c(1), {'Color', 'LineWidth', 'LineStyle'});
        otherwise
            ok = false;
    end
    kOK = kOK && ok;
end
close(h);
out.Figure_S6 = struct('points', n, 'mismatches', {bad}, 'key_glyphs', numel(K), 'key_ok', kOK, ...
    'result', tern(isempty(bad) && n == 36 && kOK));

fid = fopen(fullfile(root, 'qa', 'plotted_vs_canonical_supp_v6.json'), 'w');
fwrite(fid, jsonencode(out, 'PrettyPrint', true), 'char'); fclose(fid);
fn = fieldnames(out);
for i = 1:numel(fn)
    fprintf('%s %s; ', fn{i}, out.(fn{i}).result);
end
fprintf('\n');
end


function s = tern(c)
if c, s = 'PASS'; else, s = 'FAIL'; end
end


function s = tern2(c, a, b)
if c, s = a; else, s = b; end
end
