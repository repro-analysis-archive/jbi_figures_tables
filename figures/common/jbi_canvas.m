function [fig, cv] = jbi_canvas(wcm, hcm)
%JBI_CANVAS White figure of wcm x hcm cm plus an invisible full-size axes whose data units are centimetres
%   (origin bottom-left), used to place text and guides at exact physical positions.

fig = figure('Visible', 'off', 'Color', 'w', 'Units', 'centimeters', 'Position', [1 1 wcm hcm], ...
    'Renderer', 'painters');
fig.UserData.canvasCm = [wcm hcm];
cv = axes(fig, 'Units', 'normalized', 'Position', [0 0 1 1], 'XLim', [0 wcm], 'YLim', [0 hcm], ...
    'Visible', 'off', 'HitTest', 'off', 'Tag', 'canvas');
hold(cv, 'on');
end
