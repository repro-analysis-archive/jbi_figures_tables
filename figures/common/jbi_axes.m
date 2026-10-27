function ax = jbi_axes(fig, S, pos_cm)
%JBI_AXES Axes at [x y w h] in cm with the house style (Arial, tick size, outward ticks, box off).

wh = fig.UserData.canvasCm;
ax = axes(fig, 'Units', 'normalized', 'Position', pos_cm ./ [wh wh]);
hold(ax, 'on');
set(ax, 'FontName', S.font, 'FontSize', S.tick, 'TickDir', 'out', 'Box', 'off', 'LineWidth', S.axlw, ...
    'XColor', S.k, 'YColor', S.k, 'Layer', 'top', 'TickLength', [0.012 0.012], 'Color', 'none');
ax.XAxis.FontSize = S.tick;
ax.YAxis.FontSize = S.tick;
end
