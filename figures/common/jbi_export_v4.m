function jbi_export_v4(fig, stem, S)
%JBI_EXPORT_V4 Save <stem>.fig and the vector PDF as jbi_export; the TIF is the vector PDF rasterised by poppler at
%   S.dpi (task v4 finding). MATLAB print -dtiff, print -image, -opengl and exportgraphics at 1,200 dpi all render in
%   4,000-px tiles and clip markers that straddle a tile boundary (Figure 2 v3: the W = 0 square of P2-SITE lost its
%   left side; the vector PDF is correct). Rasterising MATLAB's own vector PDF keeps one source (.fig -> PDF -> TIF)
%   and makes the TIF show exactly what the PDF shows. The TIF size is the PDF page (whole points).

set(findall(fig, '-property', 'FontName'), 'FontName', 'Arial');
wh = fig.UserData.canvasCm;
set(fig, 'PaperUnits', 'centimeters', 'PaperSize', wh, 'PaperPosition', [0 0 wh], ...
    'PaperPositionMode', 'manual', 'InvertHardcopy', 'off', 'Color', 'w');
savefig(fig, [stem '.fig']);
print(fig, [stem '.pdf'], '-dpdf', '-vector');
poppler = '/opt/homebrew/bin/pdftoppm';
assert(isfile(poppler), 'pdftoppm (poppler) not found at %s', poppler);
cmd = sprintf('"%s" -r %d -tiff -tiffcompression lzw -singlefile "%s.pdf" "%s"', poppler, S.dpi, stem, stem);
[st, msg] = system(cmd);
assert(st == 0 && isfile([stem '.tif']), 'pdftoppm failed: %s', msg);
end
