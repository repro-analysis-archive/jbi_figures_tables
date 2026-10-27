function R = jbi_ramp_v6(kind, S)
%JBI_RAMP_V6 Shading classes of the all-cell heatmaps (Figures S1–S3, supplement v6). Discrete classes on round
%   boundaries (chosen for readability, not fitted to the data), house palette only, text #1A1A1A on every class
%   (darkest shade #8A8A8A or 60% navy: contrast with #1A1A1A >= 4.5). Fields: edges (class boundaries), colours
%   (one row per class, lowest class first), labels (boundary labels for the key), title, and cls = @(v) class index.
%     'D'   diverging on D: gray tints for D < 0, white for |D| < 0.01, navy tints for D > 0; boundaries at
%           ±0.01, ±0.05, ±0.1, ±0.5, ±1 (a class includes its lower boundary).
%     'rb'  sequential gray on |relative bias| in %: < 5 white; 5, 10, 25, 50, 100, 200 (>= 200 darkest).
%     'cov' sequential gray on coverage: >= 0.90 white; 0.75, 0.50, 0.25 (< 0.25 darkest).

white = [1 1 1];
gray = @(f) 1 - f * (1 - S.g8A);                  % f = 1 -> #8A8A8A
navy = @(f) 1 - 0.6 * f * (1 - S.navy);           % f = 1 -> 60 % navy tint
switch kind
    case 'D'
        b = [0.01 0.05 0.1 0.5 1];
        R.edges = [-fliplr(b) b];                 % 10 boundaries -> 11 classes
        R.colours = [cell2mat(arrayfun(@(f) gray(f), (5:-1:1)' / 5, 'UniformOutput', false)); white; ...
                     cell2mat(arrayfun(@(f) navy(f), (1:5)' / 5, 'UniformOutput', false))];
        R.labels = arrayfun(@(e) strrep(sprintf('%g', e), '-', char(8722)), R.edges, 'UniformOutput', false);
        R.title = 'D (without C − with C)';
        R.cls = @(v) 1 + sum(v >= R.edges);
    case 'rb'
        R.edges = [5 10 25 50 100 200];
        R.colours = [white; cell2mat(arrayfun(@(f) gray(f), (1:6)' / 6, 'UniformOutput', false))];
        R.labels = arrayfun(@(e) sprintf('%g', e), R.edges, 'UniformOutput', false);
        R.title = '|relative bias| (%)';
        R.cls = @(v) 1 + sum(abs(v) >= R.edges);
    case 'cov'
        R.edges = [0.25 0.5 0.75 0.9];
        R.colours = [cell2mat(arrayfun(@(f) gray(f), (4:-1:1)' / 4, 'UniformOutput', false)); white];
        R.labels = arrayfun(@(e) sprintf('%g', e), R.edges, 'UniformOutput', false);
        R.title = 'coverage of the 95% interval';
        R.cls = @(v) 1 + sum(v >= R.edges);
    otherwise
        error('unknown ramp %s', kind);
end
R.kind = kind;
end
