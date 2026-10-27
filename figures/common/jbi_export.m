function jbi_export(fig, stem, S)
%JBI_EXPORT Save <stem>.fig, then the vector PDF and the line-art TIF from the same figure (template §6).
%   The canvas size is taken from UserData.canvasCm (the figure Position is pixel-snapped). PDF: print -vector
%   (page rounded up to whole points by MATLAB). TIF: print -dtiff at S.dpi with the exact PaperPosition.

set(findall(fig, '-property', 'FontName'), 'FontName', 'Arial');
wh = fig.UserData.canvasCm;
set(fig, 'PaperUnits', 'centimeters', 'PaperSize', wh, 'PaperPosition', [0 0 wh], ...
    'PaperPositionMode', 'manual', 'InvertHardcopy', 'off', 'Color', 'w');
savefig(fig, [stem '.fig']);
print(fig, [stem '.pdf'], '-dpdf', '-vector');
print(fig, [stem '.tif'], '-dtiff', sprintf('-r%d', S.dpi));
end
