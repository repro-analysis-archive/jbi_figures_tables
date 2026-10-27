function xc = jbi_x2cm(ax, x)
%JBI_X2CM Horizontal data coordinate of axes ax -> figure centimetres (linear x axes only).
wh = ax.Parent.UserData.canvasCm;
p = ax.Position .* [wh wh];
xl = ax.XLim;
xc = p(1) + (x - xl(1)) ./ (xl(2) - xl(1)) .* p(3);
end
