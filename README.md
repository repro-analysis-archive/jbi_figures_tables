# JBI figures, tables and graphical abstract — SS-DS203 manuscript

Built 2026-10-27 from the read-only package `/Volumes/ADDATA/医療動画/SS_DS203_manuscript_20261020` (manifest verified, 248 / 248). Task: `CC_TASK_JBI_figures_tables_v2.md`.

## Contents

* `figures/Figure_1/` — schematic (`make_Figure_1.js` → `.pptx` → LibreOffice `.pdf` → 1,200-dpi `.tif`)
* `figures/Figure_2..4/` — data figures (`make_Figure_N.m` → `.fig` → vector `.pdf` + 1,200-dpi `.tif`); `figures/common/` shared MATLAB helpers and `verify_plotted.m`
* `graphical_abstract/` — `make_Graphical_abstract.js` → `.pptx`, `.pdf`, `.tif`
* `tables/` — `Table_1..3.docx` (editable), `.csv` (displayed cells), `.pdf` (LibreOffice rendering for QA)
* `canonical/` — frozen values (`scripts/freeze.py`), `SHA256SUMS.txt`
* `CAPTIONS.md`, `SOURCE_MAP.md`, `NOTATION_REGISTRY.md`, `POST_RESULT_PRESENTATION_JBI.md`, `SUPPLEMENT_INDEX.md`, `qa/MEASUREMENT_REPORT.md`, `qa/` measurement JSON, `templates/`

## Rebuild (clean)

```
.venv/bin/python -I scripts/freeze.py
for n in 2 3 4; do /Applications/MATLAB_R2025b.app/bin/matlab -batch "close all force; clear; run('figures/Figure_$n/make_Figure_$n.m')"; done
node figures/Figure_1/make_Figure_1.js; (cd figures/Figure_1 && soffice --headless --convert-to pdf Figure_1.pptx && pdftoppm -r 1200 -tiff -tiffcompression lzw -singlefile Figure_1.pdf Figure_1)
node graphical_abstract/make_Graphical_abstract.js; (cd graphical_abstract && soffice --headless --convert-to pdf Graphical_abstract.pptx && pdftoppm -r 1200 -tiff -tiffcompression lzw -singlefile Graphical_abstract.pdf Graphical_abstract)
.venv/bin/python -I scripts/build_tables.py; (cd tables && for n in 1 2 3; do soffice --headless --convert-to pdf Table_$n.docx; done)
scripts/rebuild_check.sh   # the clean-rebuild comparison used for qa/REBUILD_TEST.md
```

## SHA-256 of the deliverables

| file | bytes | SHA-256 |
|---|---|---|
| `figures/Figure_1/Figure_1.pdf` | 88831 | `359c62118b760590c9ecf9ac69b4e3013bb1913d958811013d17981ea7a514a9` |
| `figures/Figure_1/Figure_1.pptx` | 135265 | `63a2b3d66278c7f0d328b3a82338c2d3af64e1ea471fa54dda44726a82e9ba6c` |
| `figures/Figure_1/Figure_1.tif` | 4600844 | `e2bebf63645192bbfd94e07eaf7e37c5eb9188ee70cc0cd98128d7134b32c5f7` |
| `figures/Figure_2/Figure_2.fig` | 37578 | `ef801f9a497a04ba2722144911aef3a862fd63b07740f14dae31927baaf13825` |
| `figures/Figure_2/Figure_2.pdf` | 19710 | `395d862ee03f478101aab506cd5e39b3dee901c52c8c9c1fea34838b5c705b7d` |
| `figures/Figure_2/Figure_2.tif` | 3305237 | `15de3f4c7b3c758ac5ca4cc46d0d764f88251dd7291f260dc91bad5b041edf15` |
| `figures/Figure_3/Figure_3.fig` | 61726 | `97c6d31cb1cecd04de4a8cd67ced055d52bed3f93b708d5c7e6618fd0b1ba43e` |
| `figures/Figure_3/Figure_3.pdf` | 22034 | `86806ea70f13857acd319f92853ced8733a680a4f41fc405bdd0c247da0c238f` |
| `figures/Figure_3/Figure_3.tif` | 2393093 | `f6eaff3dcb038126318d2f546f4748c6cd66cab5505c10dc9b537db44536c995` |
| `figures/Figure_4/Figure_4.fig` | 154586 | `99d0c83d9d0363ec7f50705e30bda5022b36ab7959740a0122273e32bc1d0b9a` |
| `figures/Figure_4/Figure_4.pdf` | 114948 | `b7e534cadf9c5580862b23e9ea5f8d07316e3649ee0591715b9c5482e770114e` |
| `figures/Figure_4/Figure_4.tif` | 4783565 | `762dcace2ecca7839eeb1ac3e4276f0d5205cdbdec2e183d1cc296df65bc11c7` |
| `graphical_abstract/Graphical_abstract.pdf` | 54044 | `375f3cfda8c39d1d1e8006600e53a29b91abe87a5237862d46d7900f20375373` |
| `graphical_abstract/Graphical_abstract.pptx` | 67080 | `9227afe3ed00773121f4890d832826be321fc4ff7647510cdee0f621c670bacf` |
| `graphical_abstract/Graphical_abstract.tif` | 1239924 | `d526822eb4b5c6e0fb23786897e06ab3abe30ebfe4a09eed31fd9c2ee952346e` |
| `tables/Table_1.csv` | 2548 | `d3490c6f596bdec19e0dd70b2ce43b3f01bf7515db0e6e4f581f6a908333de45` |
| `tables/Table_1.docx` | 39771 | `e59907539bd4d7ed3254d1bc509bfc6f75554ce0211a015a8d9ffeadca290989` |
| `tables/Table_1.pdf` | 101851 | `c008f4cc918511cfb34afd15799e59154c1257666452d3091a39982d77dd1ec9` |
| `tables/Table_2.csv` | 2038 | `506d9006e955a1940028c20b447bb375c5278922dac911bc9e6a5c154b3db908` |
| `tables/Table_2.docx` | 39471 | `f8444d6da14ef9921fdda57a5cfef294ae919fa844fbc8395904a5f3a0884c06` |
| `tables/Table_2.pdf` | 113168 | `10e2d923d69861a797cf7a4aecf3d613ac13c3e3a9b9afd7f78a569be8bd9ee2` |
| `tables/Table_3.csv` | 5468 | `2feca4d14f57cec04006f95b1d5faa0fb1588592d0989cbcaa242ed5a712d1f2` |
| `tables/Table_3.docx` | 40345 | `1b2fed3b123cb0416e4969ed0f0aee794324d3a7cd58032c8c4717a6d6aae5d3` |
| `tables/Table_3.pdf` | 145339 | `351ff12aa150a36bfd825b9b973de27683e933cfa9f82221dfad7d5404f13101` |
