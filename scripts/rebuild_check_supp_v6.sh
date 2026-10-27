#!/bin/zsh
# Clean rebuild test of the supplement v6 outputs: move them and canonical_supplement/ aside, re-freeze from the package,
# rebuild every supplementary figure in a fresh MATLAB session and the tables, compare with the moved build
# (compare_supp.py), then re-run the supplement QA. The main set is not touched. Usage: scripts/rebuild_check_supp_v6.sh <scratch>
set -e
ROOT="/Volumes/ADDATA/医療動画/JBI_figures_tables"
MATLAB=/Applications/MATLAB_R2025b.app/bin/matlab
B="$1/before_rebuild_supp_v6"
cd "$ROOT"
/bin/rm -rf "$B"
mkdir -p "$B/canonical_supplement" "$B/tables"
mv canonical_supplement/*.json canonical_supplement/*.csv canonical_supplement/SHA256SUMS.txt "$B/canonical_supplement/"
mkdir -p "$B/supplementary"
for n in 1 2 3 4 5 6; do
  mkdir -p "$B/figures_supp_v1/Figure_S$n/pages"
  find figures_supp_v1/Figure_S$n -maxdepth 1 -type f -name "Figure_S${n}_v1.*" -exec mv {} "$B/figures_supp_v1/Figure_S$n/" \;
  [[ -d figures_supp_v1/Figure_S$n/pages ]] && find figures_supp_v1/Figure_S$n/pages -type f -name "Figure_S${n}_v1_p*" -exec mv {} "$B/figures_supp_v1/Figure_S$n/pages/" \;
done
for n in 1 2 3 4 5 6; do mv tables/Table_S${n}_v1.{docx,pdf,csv} "$B/tables/"; done
mv supplementary/Supplementary_Material_v1.{docx,pdf} "$B/supplementary/"
find canonical_supplement figures_supp_v1 tables -name '._*' -type f -delete   # exFAT AppleDouble files (gitignored)
.venv/bin/python -I scripts/freeze_supplement.py
for n in 1 2 3 4 5 6; do
  $MATLAB -batch "close all force; clear; run('$ROOT/figures_supp_v1/Figure_S$n/make_Figure_S${n}_v1.m')" 2>&1 | grep -v "sun.awt" | tail -1
done
.venv/bin/python -I scripts/build_tables_supp_v1.py
(cd tables && for n in 1 2 3 4 5 6; do soffice --headless --convert-to pdf Table_S${n}_v1.docx >/dev/null 2>&1; done)
find tables -name '._*' -type f -delete
.venv/bin/python -I scripts/build_supplementary_material_v1.py | head -1
.venv/bin/python -I scripts/qa_supplementary_docx_v1.py | tail -1      # also writes the LibreOffice PDF
find canonical_supplement figures_supp_v1 tables -name '._*' -type f -delete
.venv/bin/python -I scripts/compare_supp.py "$B"
$MATLAB -batch "addpath('$ROOT/figures/common'); verify_plotted_supp_v6('$ROOT')" 2>&1 | grep -v "sun.awt" | tail -1
.venv/bin/python -I scripts/qa_measure_supp.py 2>/dev/null | tail -6
.venv/bin/python -I scripts/qa_tables_supp_v1.py | tail -1
.venv/bin/python -I scripts/qa_captions_supp_v1.py | tail -1
.venv/bin/python -I scripts/qa_blind.py --supp 2>/dev/null | tail -1
