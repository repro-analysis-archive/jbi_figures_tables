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

## v3 revision (2026-10-27)

Revised outputs carry the suffix `_v2` (figures in `figures_v2/`; `Graphical_abstract_v2.*`; `Table_1_v2`, `Table_2_v2`, `Table_S5_v2`; `CAPTIONS_v2.md`); the earlier outputs are unchanged. New numbering: Figure 1 design, Figure 2 families, Figure 3 prior action history (new), Figure 4 erasure, Figure 5 X1/X2, Table 1, Table 2, Supplementary Table S5. Rebuild and checks: `scripts/rebuild_check_v3.sh <scratch_dir>`; report `qa/MEASUREMENT_REPORT_v2.md`; decisions `POST_RESULT_PRESENTATION_JBI.md` §6.

## v4 revision (2026-10-27)

Task `CC_TASK_JBI_figures_tables_v4.md`. Revised outputs carry the suffix `_v3`: `figures_v3/Figure_1..4/` (markers 1.5 mm filled in Figures 2–4; Figures 1 and 3 at most 220 mm high, font sizes unchanged) and `tables/Table_2_v3.*` ("Locked rule outcome"; the one bound shown as −0.0003). Current set: Figures 1–4 `_v3`, Figure 5 `_v2`, Table 1 `_v2`, Table 2 `_v3`, Table S5 `_v2`, graphical abstract `_v2`, captions `CAPTIONS_v2.md`. The data-figure TIFs of v4 are the MATLAB vector PDFs rasterised by poppler (`figures/common/jbi_export_v4.m`; MATLAB's raster export clips markers at its 4,000-px render tiles). Rebuild and checks: `scripts/rebuild_check_v4.sh <scratch_dir>`; report `qa/MEASUREMENT_REPORT_v3.md`; decisions `POST_RESULT_PRESENTATION_JBI.md` §7.

## v5 revision (2026-10-27) — current set

Task `CC_TASK_JBI_figures_tables_v5.md`. Complete figure set with the suffix `_v4` in `figures_v4/Figure_1..6/`, numbered in the order of first citation in Results: 1 design (= `Figure_1_v3`), 2 erasure (= `Figure_4_v3`), 3 families (= `Figure_2_v3`), 4 prior action history (= `Figure_3_v3`), 5 relative bias and coverage at the slice (new; `make_Figure_5_v4.m`, canonical `fig5_bias_coverage.json`), 6 exploratory X1/X2 (= `Figure_5_v2`; TIF from its PDF). Renumbered files are byte copies made by `scripts/renumber_v5.py`. Captions `CAPTIONS_v4.md`; tables `Table_1_v2`, `Table_2_v3`, `Table_S5_v2`; graphical abstract `Graphical_abstract_v2`. Rebuild and checks: `scripts/rebuild_check_v5.sh <scratch_dir>`; report `qa/MEASUREMENT_REPORT_v4.md`; decisions `POST_RESULT_PRESENTATION_JBI.md` §8.

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
| `figures_v2/Figure_1/Figure_1_v2.pdf` | 83893 | `1e88e7ba947b5f088e77000a920dea257ab59634946e9a7d3d489513e5b8a045` |
| `figures_v2/Figure_1/Figure_1_v2.pptx` | 128077 | `c506da8186a96f1419c1071d8cf5473b96260df90c0e67fc5f2b54232402f996` |
| `figures_v2/Figure_1/Figure_1_v2.tif` | 5639674 | `5e7c9c526ab3d98d770a04751ca689d7ebadfb1466e3c22d7ef3a19a72c438ab` |
| `figures_v2/Figure_2/Figure_2_v2.fig` | 25303 | `6dcb7f75c8fe7641132a1027161fc8c4d9cd6c7c4e3c23a80c82077c62c5e27c` |
| `figures_v2/Figure_2/Figure_2_v2.pdf` | 15606 | `a208030971b23e87ed2b7c66ba995d3a80f93f8ec9b062bc3cdb816577a51905` |
| `figures_v2/Figure_2/Figure_2_v2.tif` | 3414489 | `aee38406820fe8b398d7ff74ec6f8bbdcaf36e9e19dccc1e98e6e5ac6215ceef` |
| `figures_v2/Figure_3/Figure_3_v2.fig` | 36691 | `75baed1e0505d15bb7a3f3dbfd6f0c302240b7ca0c1e9bfe019bea6ee7da257f` |
| `figures_v2/Figure_3/Figure_3_v2.pdf` | 21087 | `991fcd9f8b8d13c8c7b1974fd44d4e75caa46226b0a2b67f8cb48a432d833461` |
| `figures_v2/Figure_3/Figure_3_v2.tif` | 6824359 | `76ed0a50b007d39d8a3c4c27598718e88c92a12cdd24ccaea58362b71dc65360` |
| `figures_v2/Figure_4/Figure_4_v2.fig` | 65547 | `3c08905da523bcf607fa63544a8e72d7177d60b68fe0c2778ed2acc2d62716df` |
| `figures_v2/Figure_4/Figure_4_v2.pdf` | 22578 | `fb214c6d3d7b5ef600821b501ca34620e1f71649e30ea0fb773b9aff433320ca` |
| `figures_v2/Figure_4/Figure_4_v2.tif` | 4030223 | `7b01dd9336d3518aca6e17a175d9f118761e874a271e18cd6a2e7e5fd73a1bc4` |
| `figures_v2/Figure_5/Figure_5_v2.fig` | 178010 | `d5d033b33bd7660a05e977bfc629ae5c631adc356846f35f5c97c19cd885919f` |
| `figures_v2/Figure_5/Figure_5_v2.pdf` | 117420 | `5dcfdb99d10bed55ce97bffc8fa2977b2b269d144e70402e1e362315c1eecc1d` |
| `figures_v2/Figure_5/Figure_5_v2.tif` | 7410183 | `ce7397df5f369419b3c3853a69a909117bcc32402a19f0f1f8dbe54328ce8502` |
| `figures_v3/Figure_1/Figure_1_v3.pdf` | 83898 | `7377206b9fa252f3e9a8e2f3741427bbce81c0c9608b08bb28ea6ae90f98c4d5` |
| `figures_v3/Figure_1/Figure_1_v3.pptx` | 128076 | `3701733f0531d637b30a3693049b1ea3e70ec007f323fe3defca8467dcc41870` |
| `figures_v3/Figure_1/Figure_1_v3.tif` | 5478962 | `1fb71a9efd950db437d6cdaae4fe78d852ef5a2e4ee42703bd7d87669843c2fd` |
| `figures_v3/Figure_2/Figure_2_v3.fig` | 25296 | `5f071c3281fc789478beb15639e8257bba2aabd5ca3e9733eef905a86ad12311` |
| `figures_v3/Figure_2/Figure_2_v3.pdf` | 15639 | `09d1b39b625f80e19c27d30fc8fc3f974c4033333a4831608d7c1bb7485f5060` |
| `figures_v3/Figure_2/Figure_2_v3.tif` | 2628078 | `1b836db4b9b042ac695c3b9dfec435a78d92ee1c6d3c5ad3c86252cc57d0a2be` |
| `figures_v3/Figure_3/Figure_3_v3.fig` | 36796 | `d8b6816afbb049e917cfe647627774a7fb0e78179042684a87773584610e208c` |
| `figures_v3/Figure_3/Figure_3_v3.pdf` | 21165 | `fc1047de6ad2bc142589f91787cc2a86f7e0e4c2b7b5c01dd3bb31f9df3881d6` |
| `figures_v3/Figure_3/Figure_3_v3.tif` | 3911596 | `f9a9ab8c084eccb1eead48b642635fbf4d994ee16165599a99ca905c4915d382` |
| `figures_v3/Figure_4/Figure_4_v3.fig` | 65450 | `1494000406aab9bb8a91dfd260c8218499410d9c26c28c38e3df5b8afc8ca3fe` |
| `figures_v3/Figure_4/Figure_4_v3.pdf` | 22658 | `23ff5d65bf6e2e7740a69267af32305ade10c6a3eeb9e181416351d5785d8229` |
| `figures_v3/Figure_4/Figure_4_v3.tif` | 3023524 | `4b117272047c30103d37ee66b18e3848d9315b7f196cd0d94ec5fd823931eb7b` |
| `figures_v4/Figure_1/Figure_1_v4.pdf` | 83898 | `7377206b9fa252f3e9a8e2f3741427bbce81c0c9608b08bb28ea6ae90f98c4d5` |
| `figures_v4/Figure_1/Figure_1_v4.pptx` | 128076 | `3701733f0531d637b30a3693049b1ea3e70ec007f323fe3defca8467dcc41870` |
| `figures_v4/Figure_1/Figure_1_v4.tif` | 5478962 | `1fb71a9efd950db437d6cdaae4fe78d852ef5a2e4ee42703bd7d87669843c2fd` |
| `figures_v4/Figure_2/Figure_2_v4.fig` | 65450 | `1494000406aab9bb8a91dfd260c8218499410d9c26c28c38e3df5b8afc8ca3fe` |
| `figures_v4/Figure_2/Figure_2_v4.pdf` | 22658 | `23ff5d65bf6e2e7740a69267af32305ade10c6a3eeb9e181416351d5785d8229` |
| `figures_v4/Figure_2/Figure_2_v4.tif` | 3023524 | `4b117272047c30103d37ee66b18e3848d9315b7f196cd0d94ec5fd823931eb7b` |
| `figures_v4/Figure_3/Figure_3_v4.fig` | 25296 | `5f071c3281fc789478beb15639e8257bba2aabd5ca3e9733eef905a86ad12311` |
| `figures_v4/Figure_3/Figure_3_v4.pdf` | 15639 | `09d1b39b625f80e19c27d30fc8fc3f974c4033333a4831608d7c1bb7485f5060` |
| `figures_v4/Figure_3/Figure_3_v4.tif` | 2628078 | `1b836db4b9b042ac695c3b9dfec435a78d92ee1c6d3c5ad3c86252cc57d0a2be` |
| `figures_v4/Figure_4/Figure_4_v4.fig` | 36796 | `d8b6816afbb049e917cfe647627774a7fb0e78179042684a87773584610e208c` |
| `figures_v4/Figure_4/Figure_4_v4.pdf` | 21165 | `fc1047de6ad2bc142589f91787cc2a86f7e0e4c2b7b5c01dd3bb31f9df3881d6` |
| `figures_v4/Figure_4/Figure_4_v4.tif` | 3911596 | `f9a9ab8c084eccb1eead48b642635fbf4d994ee16165599a99ca905c4915d382` |
| `figures_v4/Figure_5/Figure_5_v4.fig` | 77701 | `a0a77ba4af3701f2110150e49b7871a91808413ef69a368a36f92f8d8180b157` |
| `figures_v4/Figure_5/Figure_5_v4.pdf` | 44490 | `566544e695f9ff4cec027fe4c94d5d71466e09c44c606defeec321ed2425e22f` |
| `figures_v4/Figure_5/Figure_5_v4.tif` | 4073764 | `e528c21b556af43b36a477631e3973fc0e1ef90c0c45aeb03b1b853d767e1ec5` |
| `figures_v4/Figure_6/Figure_6_v4.fig` | 178010 | `d5d033b33bd7660a05e977bfc629ae5c631adc356846f35f5c97c19cd885919f` |
| `figures_v4/Figure_6/Figure_6_v4.pdf` | 117420 | `5dcfdb99d10bed55ce97bffc8fa2977b2b269d144e70402e1e362315c1eecc1d` |
| `figures_v4/Figure_6/Figure_6_v4.tif` | 4776666 | `66b9ac3950723bfe2d10a7b91bf32a37709122ab90e82b2f51a555aafeec6f34` |
| `graphical_abstract/Graphical_abstract.pdf` | 54044 | `375f3cfda8c39d1d1e8006600e53a29b91abe87a5237862d46d7900f20375373` |
| `graphical_abstract/Graphical_abstract.pptx` | 67080 | `9227afe3ed00773121f4890d832826be321fc4ff7647510cdee0f621c670bacf` |
| `graphical_abstract/Graphical_abstract.tif` | 1239924 | `d526822eb4b5c6e0fb23786897e06ab3abe30ebfe4a09eed31fd9c2ee952346e` |
| `graphical_abstract/Graphical_abstract_v2.pdf` | 51644 | `c66757aa12aa9fbfdb5f0ebaa7a7ddbbef01763d4b2f94fb6c40e00eb0b78f24` |
| `graphical_abstract/Graphical_abstract_v2.pptx` | 58232 | `ed10a56107a66802adb75baa7b7faf9814261a0c65a112e2fc7dc204dacbb610` |
| `graphical_abstract/Graphical_abstract_v2.tif` | 1316470 | `e12dfc88c3f664562b410f8ae83ca33659c5878507bdaf712da897399775ecd1` |
| `tables/Table_1.csv` | 2548 | `d3490c6f596bdec19e0dd70b2ce43b3f01bf7515db0e6e4f581f6a908333de45` |
| `tables/Table_1.docx` | 39771 | `e59907539bd4d7ed3254d1bc509bfc6f75554ce0211a015a8d9ffeadca290989` |
| `tables/Table_1.pdf` | 101851 | `c008f4cc918511cfb34afd15799e59154c1257666452d3091a39982d77dd1ec9` |
| `tables/Table_1_v2.csv` | 1867 | `76d36a97c9ab1128b5880365cd7da49bcb95334ea5604e9e4cf0de06c3b54fc2` |
| `tables/Table_1_v2.docx` | 39077 | `77499b322dac8d55b331d1fae896791043761c2169e2bf7930cf20d2bdb5e6c4` |
| `tables/Table_1_v2.pdf` | 83747 | `6dc82786f914fb0517eead9dae1ae0929a49f22138b1b6fee5a455f44e205163` |
| `tables/Table_2.csv` | 2038 | `506d9006e955a1940028c20b447bb375c5278922dac911bc9e6a5c154b3db908` |
| `tables/Table_2.docx` | 39471 | `f8444d6da14ef9921fdda57a5cfef294ae919fa844fbc8395904a5f3a0884c06` |
| `tables/Table_2.pdf` | 113168 | `10e2d923d69861a797cf7a4aecf3d613ac13c3e3a9b9afd7f78a569be8bd9ee2` |
| `tables/Table_2_v2.csv` | 2006 | `9d8bb7ce8dbcdfa218202f0bb24487de47978fbc6393ba1be796379dc537557d` |
| `tables/Table_2_v2.docx` | 39080 | `5b1a4b314be31dbc3c30e2d0b1c8c70d77184353444ea7225af8fcb7c78a9c3b` |
| `tables/Table_2_v2.pdf` | 109292 | `329e49991e961d06c5770999a383f3256afea02de9615d36e126b3e9857299bb` |
| `tables/Table_2_v3.csv` | 2026 | `9bcfaa5241cc573a96e15e613f241d9923c28c81bb1ecdc4633976afe8730919` |
| `tables/Table_2_v3.docx` | 39246 | `eba09df3e51334b54f15a4bcc21867362b57284857fb7f8d6881887977a8b4cc` |
| `tables/Table_2_v3.pdf` | 111018 | `f8d819a67a8181dbc800830a5b91d104df05c0b2475c30ac0372ae555b52f2dd` |
| `tables/Table_3.csv` | 5468 | `2feca4d14f57cec04006f95b1d5faa0fb1588592d0989cbcaa242ed5a712d1f2` |
| `tables/Table_3.docx` | 40345 | `1b2fed3b123cb0416e4969ed0f0aee794324d3a7cd58032c8c4717a6d6aae5d3` |
| `tables/Table_3.pdf` | 145339 | `351ff12aa150a36bfd825b9b973de27683e933cfa9f82221dfad7d5404f13101` |
| `tables/Table_S5_v2.csv` | 5468 | `2feca4d14f57cec04006f95b1d5faa0fb1588592d0989cbcaa242ed5a712d1f2` |
| `tables/Table_S5_v2.docx` | 40346 | `6ae658ca5fef32401c84ec89b87937530ebc94c98bfa1ef2bdae27d61bf1a9a1` |
| `tables/Table_S5_v2.pdf` | 145365 | `7289939ac49f48fa113012e16b0e1cafdc35b3687576fa1b6a0e99ae389f1223` |
