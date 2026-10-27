#!/bin/zsh
# Clean rebuild test: move every generated output aside, rebuild from the package + scripts, compare with the
# previous build (scripts/compare_builds.py), then re-run the QA. Usage: scripts/rebuild_check.sh <scratch_dir>
set -e
ROOT="/Volumes/ADDATA/医療動画/JBI_figures_tables"
MATLAB=/Applications/MATLAB_R2025b.app/bin/matlab
B="$1/before_rebuild"
cd "$ROOT"
/bin/rm -rf "$B"
mkdir -p "$B/canonical" "$B/figures/Figure_1" "$B/figures/Figure_2" "$B/figures/Figure_3" "$B/figures/Figure_4" \
         "$B/graphical_abstract" "$B/tables"
# 1. move generated outputs out of the repository (scripts stay)
mv canonical/*.json canonical/*.csv canonical/SHA256SUMS.txt "$B/canonical/"
for n in 2 3 4; do mv figures/Figure_$n/Figure_$n.{fig,pdf,tif} "$B/figures/Figure_$n/"; done
mv figures/Figure_1/Figure_1.{pptx,pdf,tif} "$B/figures/Figure_1/"
mv graphical_abstract/Graphical_abstract.{pptx,pdf,tif} "$B/graphical_abstract/"
mv tables/Table_*.{docx,pdf,csv} "$B/tables/"
find canonical figures graphical_abstract tables -name '._*' -type f -delete   # exFAT AppleDouble files (gitignored)
# 2. rebuild
.venv/bin/python -I scripts/freeze.py
for n in 2 3 4; do
  $MATLAB -batch "close all force; clear; run('$ROOT/figures/Figure_$n/make_Figure_$n.m')" 2>&1 | grep -v "sun.awt" | tail -1
done
node figures/Figure_1/make_Figure_1.js
(cd figures/Figure_1 && soffice --headless --convert-to pdf Figure_1.pptx >/dev/null 2>&1 && \
  pdftoppm -r 1200 -tiff -tiffcompression lzw -singlefile Figure_1.pdf Figure_1)
node graphical_abstract/make_Graphical_abstract.js
(cd graphical_abstract && soffice --headless --convert-to pdf Graphical_abstract.pptx >/dev/null 2>&1 && \
  pdftoppm -r 1200 -tiff -tiffcompression lzw -singlefile Graphical_abstract.pdf Graphical_abstract)
.venv/bin/python -I scripts/build_tables.py
(cd tables && for n in 1 2 3; do soffice --headless --convert-to pdf Table_$n.docx >/dev/null 2>&1; done)
# 3. compare and re-run QA on the rebuilt outputs
.venv/bin/python -I scripts/compare_builds.py "$B"
$MATLAB -batch "addpath('$ROOT/figures/common'); verify_plotted('$ROOT')" 2>&1 | grep -v "sun.awt" | tail -1
for f in figures/Figure_1/Figure_1 figures/Figure_2/Figure_2 figures/Figure_3/Figure_3 figures/Figure_4/Figure_4 \
         graphical_abstract/Graphical_abstract; do
  .venv/bin/python -I scripts/qa_measure.py $f.pdf --tif $f.tif | head -1
done
.venv/bin/python -I scripts/qa_tables.py | grep -E "^Table|PASS|FAIL"
.venv/bin/python -I scripts/qa_schematic_numbers.py
