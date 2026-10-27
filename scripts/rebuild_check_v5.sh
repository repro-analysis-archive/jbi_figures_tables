#!/bin/zsh
# Clean rebuild test of the v5-revision outputs (suffix _v4): move them, CAPTIONS_v4.md and the canonical data aside,
# re-freeze from the package, rebuild the new Figure 5 in a fresh MATLAB session (no existing .fig opened), redo the
# renumbering byte copies (renumber_v5.py) and CAPTIONS_v4.md, compare with the moved build (compare_builds.py --v4),
# then re-run the v5 QA on the rebuilt files. Earlier outputs are not touched. Usage: scripts/rebuild_check_v5.sh <scratch>
set -e
ROOT="/Volumes/ADDATA/医療動画/JBI_figures_tables"
MATLAB=/Applications/MATLAB_R2025b.app/bin/matlab
B="$1/before_rebuild_v5"
cd "$ROOT"
/bin/rm -rf "$B"
mkdir -p "$B/canonical"
for n in 1 2 3 4 5 6; do mkdir -p "$B/figures_v4/Figure_$n"; done
mv canonical/*.json canonical/*.csv canonical/SHA256SUMS.txt "$B/canonical/"
for n in 1 2 3 4 5 6; do
  find figures_v4/Figure_$n -maxdepth 1 -type f -name "Figure_${n}_v4.*" -exec mv {} "$B/figures_v4/Figure_$n/" \;
  [[ $n == 5 ]] || find figures_v4/Figure_$n -maxdepth 1 -type f -name "make_Figure_${n}_v4.*" -exec mv {} "$B/figures_v4/Figure_$n/" \;
done
mv CAPTIONS_v4.md "$B/"
find canonical figures_v4 -name '._*' -type f -delete   # exFAT AppleDouble files (gitignored)
.venv/bin/python -I scripts/freeze.py
$MATLAB -batch "close all force; clear; run('$ROOT/figures_v4/Figure_5/make_Figure_5_v4.m')" 2>&1 | grep -v "sun.awt" | tail -1
.venv/bin/python -I scripts/renumber_v5.py | tail -1
.venv/bin/python -I scripts/make_captions_v4.py
find canonical figures_v4 -name '._*' -type f -delete
for n in 1 2 3 4 6; do
  for f in "$B"/figures_v4/Figure_$n/make_Figure_${n}_v4.*; do cmp "$f" figures_v4/Figure_$n/$(basename "$f") && echo "identical  $(basename "$f")"; done
done
cmp "$B/CAPTIONS_v4.md" CAPTIONS_v4.md && echo "identical  CAPTIONS_v4.md"
.venv/bin/python -I scripts/compare_builds.py "$B" --v4
$MATLAB -batch "addpath('$ROOT/figures/common'); verify_plotted_v4('$ROOT')" 2>&1 | grep -v "sun.awt" | tail -1
for n in 1 2 3 4 5 6; do
  .venv/bin/python -I scripts/qa_measure.py figures_v4/Figure_$n/Figure_${n}_v4.pdf --tif figures_v4/Figure_$n/Figure_${n}_v4.tif 2>/dev/null | head -1
done
.venv/bin/python -I scripts/qa_markers_v5.py
.venv/bin/python -I scripts/qa_tif_markers.py figures_v4/Figure_5/Figure_5_v4 figures_v4/Figure_6/Figure_6_v4 | tail -1
.venv/bin/python -I scripts/qa_tif_vs_pdf.py figures_v4/Figure_1/Figure_1_v4 figures_v4/Figure_2/Figure_2_v4 \
  figures_v4/Figure_3/Figure_3_v4 figures_v4/Figure_4/Figure_4_v4 figures_v4/Figure_5/Figure_5_v4 \
  figures_v4/Figure_6/Figure_6_v4 2>/dev/null | tail -1
.venv/bin/python -I scripts/qa_captions_v4.py | tail -1
.venv/bin/python -I scripts/qa_blind.py --v4 2>/dev/null | tail -1
