function S = jbi_style()
%JBI_STYLE House style for the JBI data figures (figure template v11 §2; JBI values of task §3).
%   Arial; tick 9 / axis label 10 / panel label 11 pt bold at the final 190 mm width (relative rule of §2-1;
%   no text below 8 pt). Grayscale + one navy accent (#2B3D6B). Canvas width 18.97 cm so that the vector PDF page,
%   which MATLAB rounds up to whole points, stays at or below the JBI full width of 190 mm (538 pt = 189.8 mm).

assert(any(strcmpi(listfonts, 'Arial')), 'Arial is not available; stop before rendering.');

S.font = 'Arial';
S.tick = 9;
S.axis = 10;
S.legend = 9;
S.panel = 11;
S.small = 8;                         % smallest text used anywhere (secondary labels)

hex = @(h) sscanf(h(2:end), '%2x')' / 255;
S.navy = hex('#2B3D6B');
S.g4D = hex('#4D4D4D');              % readable secondary text / strong secondary marks
S.g6B = hex('#6B6B6B');              % graphical secondary
S.g8A = hex('#8A8A8A');              % residual / zero reference
S.gB3 = hex('#B3B3B3');              % guide / separator
S.gD0 = hex('#D0D0D0');
S.k = hex('#1A1A1A');                % text, axes, marker edge

S.width_cm = 18.97;                  % JBI full width (190 mm) after whole-point rounding of the PDF page
S.dpi = 1200;                        % pure line art (JBI >= 1,000 dpi; template: 1,200)
S.axlw = 0.6;                        % axes line width (pt)
S.mm = 72 / 25.4;                    % points per mm
end
