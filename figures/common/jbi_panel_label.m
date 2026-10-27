function jbi_panel_label(fig, S, txt, x_cm, ytop_cm)
%JBI_PANEL_LABEL Panel label with MATLAB annotation (template §5-0): Arial bold, top edge at ytop_cm.

wh = fig.UserData.canvasCm;
h_cm = 0.55;
annotation(fig, 'textbox', [x_cm / wh(1), (ytop_cm - h_cm) / wh(2), 1.0 / wh(1), h_cm / wh(2)], ...
    'String', txt, 'FontName', S.font, 'FontWeight', 'bold', 'FontSize', S.panel, 'Color', S.k, ...
    'EdgeColor', 'none', 'Margin', 0, 'VerticalAlignment', 'top', 'HorizontalAlignment', 'left', ...
    'Interpreter', 'none', 'FitBoxToText', 'off', 'Tag', 'panel_label');
end
