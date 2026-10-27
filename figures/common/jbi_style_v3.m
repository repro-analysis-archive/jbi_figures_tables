function S = jbi_style_v3()
%JBI_STYLE_V3 House style for the v3 revision (task v3 §3): figure template §2-1 sizes at the final 190 mm width —
%   tick 14 pt, axis label 15 pt, panel label 16 pt bold (relative rule tick -> axis -> panel kept); legends and
%   category labels 14 pt; no text below 14 pt. Palette, canvas width and dpi as jbi_style (v2).

S = jbi_style();
S.tick = 14;
S.axis = 15;
S.legend = 14;
S.panel = 16;
S.small = 14;
S.axlw = 0.8;
end
