function n = jbi_heatmap_figure_v6(root, which, outdir)
%JBI_HEATMAP_FIGURE_V6 Build one all-cell heatmap figure of the supplement v6 (Figures S1–S3) from hash-guarded
%   canonical JSON: one A4 page per pair (S1) or arm (S2, S3) for the 216 phi_A = 0 cells, followed by its phi_A = 0.5
%   page (24 cells). Writes <outdir>/Figure_<which>_v1.pdf (all pages, vector), and per page
%   <outdir>/pages/Figure_<which>_v1_pNN.fig and .tif (600 dpi, the PDF page rasterised by poppler).
%   which: 'S1' (D per pair), 'S2' (relative bias per arm), 'S3' (coverage per arm). Returns the number of pages.

S = jbi_style_v3();
switch which
    case 'S1'
        D = jbi_read_supp(root, 's1_contrast_D'); rows = D.rows;
        groups = unique({rows.pair}, 'stable'); gfield = 'pair'; vfield = 'D'; dfield = 'D_disp'; R = jbi_ramp_v6('D', S);
        assert(numel(rows) == 5 * 240 && numel(groups) == 5);
    case {'S2', 'S3'}
        D = jbi_read_supp(root, 's23_bias_coverage'); rows = D.rows;
        groups = D.arms(:)'; gfield = 'arm';
        assert(numel(rows) == 12 * 240 && numel(groups) == 12);
        if strcmp(which, 'S2')
            vfield = 'rel_bias_pct'; dfield = 'rel_bias_disp'; R = jbi_ramp_v6('rb', S);
        else
            vfield = 'coverage'; dfield = 'coverage_disp'; R = jbi_ramp_v6('cov', S);
        end
end
pages = fullfile(outdir, 'pages');
if ~isfolder(pages), mkdir(pages); end
pdf = fullfile(outdir, sprintf('Figure_%s_v1.pdf', which));
if isfile(pdf), delete(pdf); end
n = 0;
for g = 1:numel(groups)
    for phi = [0 0.5]
        r = rows(strcmp({rows.(gfield)}, groups{g}) & [rows.phi] == phi);
        assert(numel(r) == 216 * (phi == 0) + 24 * (phi == 0.5));
        n = n + 1;
        ttl = sprintf('%s — φ_A = %g (%d cells)', groups{g}, phi, numel(r));
        fig = jbi_heatmap_page_v6(S, R, r, vfield, dfield, ttl, phi, sprintf('%s:p%02d', which, n));
        set(findall(fig, '-property', 'FontName'), 'FontName', 'Arial');
        wh = fig.UserData.canvasCm;
        set(fig, 'PaperUnits', 'centimeters', 'PaperSize', wh, 'PaperPosition', [0 0 wh], ...
            'PaperPositionMode', 'manual', 'InvertHardcopy', 'off', 'Color', 'w');
        fig.UserData.page = struct('figure', which, 'page', n, 'group', groups{g}, 'phi', phi, 'cells', numel(r));
        savefig(fig, fullfile(pages, sprintf('Figure_%s_v1_p%02d.fig', which, n)));
        exportgraphics(fig, pdf, 'ContentType', 'vector', 'Append', true, 'Padding', 'figure');
        close(fig);
    end
end
% per-page TIF at 600 dpi from the vector PDF (poppler; one source; see jbi_export_v4)
poppler = '/opt/homebrew/bin/pdftoppm';
assert(isfile(poppler), 'pdftoppm (poppler) not found');
for p = 1:n
    stem = fullfile(pages, sprintf('Figure_%s_v1_p%02d', which, p));
    [st, msg] = system(sprintf('"%s" -r 600 -f %d -l %d -tiff -tiffcompression lzw -singlefile "%s" "%s"', ...
        poppler, p, p, pdf, stem));
    assert(st == 0 && isfile([stem '.tif']), 'pdftoppm failed: %s', msg);
end
end
