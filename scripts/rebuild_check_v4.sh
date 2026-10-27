#!/bin/zsh
# Clean rebuild test of the v4-revision outputs (suffix _v3): move them and the canonical data aside, re-freeze from the
# package, rebuild every v3 output from its script (each MATLAB figure in a fresh session; no existing .fig opened),
# compare with the moved build (compare_builds.py --v3), then re-run the v4 QA on the rebuilt files.
# Earlier outputs (no suffix, _v2) are not touched. Usage: scripts/rebuild_check_v4.sh <scratch_dir>
set -e
ROOT="/Volumes/ADDATA/医療動画/JBI_figures_tables"
MATLAB=/Applications/MATLAB_R2025b.app/bin/matlab
B="$1/before_rebuild_v4"
cd "$ROOT"
/bin/rm -rf "$B"
mkdir -p "$B/canonical" "$B/tables"
for n in 1 2 3 4; do mkdir -p "$B/figures_v3/Figure_$n"; done
mv canonical/*.json canonical/*.csv canonical/SHA256SUMS.txt "$B/canonical/"
for n in 2 3 4; do mv figures_v3/Figure_$n/Figure_${n}_v3.{fig,pdf,tif} "$B/figures_v3/Figure_$n/"; done
mv figures_v3/Figure_1/Figure_1_v3.{pptx,pdf,tif} "$B/figures_v3/Figure_1/"
mv tables/Table_2_v3.{docx,pdf,csv} "$B/tables/"
find canonical figures_v3 tables -name '._*' -type f -delete   # exFAT AppleDouble files (gitignored)
.venv/bin/python -I scripts/freeze.py
for n in 2 3 4; do
  $MATLAB -batch "close all force; clear; run('$ROOT/figures_v3/Figure_$n/make_Figure_${n}_v3.m')" 2>&1 | grep -v "sun.awt" | tail -1
done
node figures_v3/Figure_1/make_Figure_1_v3.js
(cd figures_v3/Figure_1 && soffice --headless --convert-to pdf Figure_1_v3.pptx >/dev/null 2>&1 && \
  pdftoppm -r 1200 -tiff -tiffcompression lzw -singlefile Figure_1_v3.pdf Figure_1_v3)
.venv/bin/python -I scripts/build_tables_v3.py
(cd tables && soffice --headless --convert-to pdf Table_2_v3.docx >/dev/null 2>&1)
find canonical figures_v3 tables -name '._*' -type f -delete
.venv/bin/python -I scripts/compare_builds.py "$B" --v3
$MATLAB -batch "addpath('$ROOT/figures/common'); verify_plotted_v3('$ROOT')" 2>&1 | grep -v "sun.awt" | tail -1
for n in 1 2 3 4; do
  .venv/bin/python -I scripts/qa_measure.py figures_v3/Figure_$n/Figure_${n}_v3.pdf --tif figures_v3/Figure_$n/Figure_${n}_v3.tif | head -1
done
.venv/bin/python -I scripts/qa_markers_v4.py | tail -12
.venv/bin/python -I scripts/qa_tif_markers.py figures_v3/Figure_2/Figure_2_v3 figures_v3/Figure_3/Figure_3_v3 figures_v3/Figure_4/Figure_4_v3 | tail -1
.venv/bin/python -I scripts/qa_tif_vs_pdf.py figures_v3/Figure_1/Figure_1_v3 figures_v3/Figure_2/Figure_2_v3 \
  figures_v3/Figure_3/Figure_3_v3 figures_v3/Figure_4/Figure_4_v3 2>/dev/null | tail -1
.venv/bin/python -I scripts/qa_v4_unchanged.py | tail -1
.venv/bin/python -I scripts/qa_tables_v3.py | grep -E "^Table|bound|PASS|FAIL"
.venv/bin/python -I scripts/qa_schematic_numbers.py --v3
.venv/bin/python -I scripts/qa_blind.py --v3 2>/dev/null | tail -1
