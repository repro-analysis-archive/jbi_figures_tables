#!/bin/zsh
# Clean rebuild test of the v3-revision outputs: move the v2 outputs and the canonical data aside, rebuild from the
# package + scripts (each MATLAB figure in a fresh session), compare (compare_builds.py --v2), re-run the v3 QA.
# Old (v1) outputs are not touched. Usage: scripts/rebuild_check_v3.sh <scratch_dir>
set -e
ROOT="/Volumes/ADDATA/医療動画/JBI_figures_tables"
MATLAB=/Applications/MATLAB_R2025b.app/bin/matlab
B="$1/before_rebuild_v3"
cd "$ROOT"
/bin/rm -rf "$B"
mkdir -p "$B/canonical" "$B/graphical_abstract" "$B/tables"
for n in 1 2 3 4 5; do mkdir -p "$B/figures_v2/Figure_$n"; done
mv canonical/*.json canonical/*.csv canonical/SHA256SUMS.txt "$B/canonical/"
for n in 2 3 4 5; do mv figures_v2/Figure_$n/Figure_${n}_v2.{fig,pdf,tif} "$B/figures_v2/Figure_$n/"; done
mv figures_v2/Figure_1/Figure_1_v2.{pptx,pdf,tif} "$B/figures_v2/Figure_1/"
mv graphical_abstract/Graphical_abstract_v2.{pptx,pdf,tif} "$B/graphical_abstract/"
mv tables/Table_1_v2.{docx,pdf,csv} tables/Table_2_v2.{docx,pdf,csv} tables/Table_S5_v2.{docx,pdf,csv} "$B/tables/"
find canonical figures_v2 graphical_abstract tables -name '._*' -type f -delete   # exFAT AppleDouble files (gitignored)
.venv/bin/python -I scripts/freeze.py
for n in 2 3 4 5; do
  $MATLAB -batch "close all force; clear; run('$ROOT/figures_v2/Figure_$n/make_Figure_${n}_v2.m')" 2>&1 | grep -v "sun.awt" | tail -1
done
node figures_v2/Figure_1/make_Figure_1_v2.js
(cd figures_v2/Figure_1 && soffice --headless --convert-to pdf Figure_1_v2.pptx >/dev/null 2>&1 && \
  pdftoppm -r 1200 -tiff -tiffcompression lzw -singlefile Figure_1_v2.pdf Figure_1_v2)
node graphical_abstract/make_Graphical_abstract_v2.js
(cd graphical_abstract && soffice --headless --convert-to pdf Graphical_abstract_v2.pptx >/dev/null 2>&1 && \
  pdftoppm -r 1200 -tiff -tiffcompression lzw -singlefile Graphical_abstract_v2.pdf Graphical_abstract_v2)
.venv/bin/python -I scripts/build_tables_v2.py
(cd tables && for n in 1_v2 2_v2 S5_v2; do soffice --headless --convert-to pdf Table_$n.docx >/dev/null 2>&1; done)
.venv/bin/python -I scripts/compare_builds.py "$B" --v2
$MATLAB -batch "addpath('$ROOT/figures/common'); verify_plotted_v2('$ROOT')" 2>&1 | grep -v "sun.awt" | tail -1
for f in figures_v2/Figure_1/Figure_1_v2 figures_v2/Figure_2/Figure_2_v2 figures_v2/Figure_3/Figure_3_v2 \
         figures_v2/Figure_4/Figure_4_v2 figures_v2/Figure_5/Figure_5_v2 graphical_abstract/Graphical_abstract_v2; do
  .venv/bin/python -I scripts/qa_measure.py $f.pdf --tif $f.tif | head -1
done
.venv/bin/python -I scripts/qa_tables_v2.py | grep -E "^Table|PASS|FAIL"
.venv/bin/python -I scripts/qa_schematic_numbers.py --v2
.venv/bin/python -I scripts/qa_blind.py --v2 | tail -1
