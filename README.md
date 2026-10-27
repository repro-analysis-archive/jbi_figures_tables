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

## v6 supplement (2026-10-27)

Task `CC_TASK_JBI_supplement_v6.md`. Supplementary Figures S1–S6 in `figures_supp_v1/` (multi-page vector PDF; per-page .fig and TIF in `pages/`), Tables S1–S6 in `tables/Table_S*_v1.*`, captions `CAPTIONS_supplement_v1.md`, the Word document `supplementary/Supplementary_Material_v1.docx`; values in `canonical_supplement/` (`scripts/freeze_supplement.py`); investigator-provided inputs in `inputs/` (`mask_check.json`, `JBI_Supplementary_Methods_draft_v2.md`). Rebuild and checks: `scripts/rebuild_check_supp_v6.sh <scratch_dir>`; report `qa/MEASUREMENT_REPORT_supp_v1.md`; decisions `POST_RESULT_PRESENTATION_JBI.md` §9.

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
| `figures_supp_v1/Figure_S1/Figure_S1_v1.pdf` | 227827 | `1bb45fa24a2982deb6616a3b421956e557b1f7487a7eeab97ccdfb08d410a37b` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p01.fig` | 163447 | `4daab63994fdfd7156b8cfa4c276cf242ebf149c6d25307c4bc72ad5d848e5c1` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p01.tif` | 4771182 | `42f28804adad769909245fa07e44e1e28f55529c368c4c78d2bec4c60c31c0d5` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p02.fig` | 41965 | `fe9d85bb933fc695c38e1711570e494bcd288c7389f844141a95bebaf159d080` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p02.tif` | 2056860 | `c257e6a211255a57b660ff8172f8d087d73340fc5792810df561288ce0a7026c` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p03.fig` | 163311 | `14c5e65b16376438887bbedcb18ea54348508913395cf8ce3fe6e56a7019b59a` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p03.tif` | 4889560 | `1bca59449e3781a49d90fa0128c39b0601a7b58f264d38e3cced5e69180e9c5a` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p04.fig` | 41948 | `c6a1c3a42bce279350754dad93adcfc0a0712dc0a05e894300a0503b917b8cbf` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p04.tif` | 2017820 | `362cc4ba616c53c7e40e1e7e3d5081959c8d870064aa10311ced48f708bbfb9f` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p05.fig` | 163128 | `4ddd8f69fcf4d3a2e65331e617c11156e34acaff10dd4ed4959904a1f59b0b8d` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p05.tif` | 4591032 | `bcc9c7849e50573bedf53fbd4ffb8f9352b813953216ea4435987e35b2572fc1` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p06.fig` | 41830 | `bad22bcb4adcc73efd8f6091783b454bf336f5a6c97e160b3ec85107622aca02` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p06.tif` | 1924738 | `2071da7525bc8f2c1a874d47d417892b6a0ae3bc01bcfc1df80bb806e4344671` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p07.fig` | 163256 | `6f87f50829fa82e8456d5361bf48a3404e464927bbde4a7037eebf4fc6ecf95a` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p07.tif` | 4709304 | `8212a7816f4396b1cbf28bed9d94acc08d63f373cda6f29201e1e23ae5474bf0` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p08.fig` | 41838 | `29401f5213b79769fa79d001549456db7caa11508ea4520ecd587d84cbe93d44` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p08.tif` | 1948292 | `4581e42adfc7e98f5f4cf047c5a4410e1ae3e57dfe06011908da2d9368f81103` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p09.fig` | 163558 | `317415f8ae91d4f7ade4457fe5f364d57632d792159a68327aa7abdc974392e0` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p09.tif` | 5025078 | `ef5f8a890fc35cb5e7f802590f3bc0a90eb98993b65ce2510b3b204f79fe59b0` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p10.fig` | 41888 | `5ee5bfd8a907d4bcaa400f0e48895652229e5e2f4e41cb251f72ab46d5ebb406` |
| `figures_supp_v1/Figure_S1/pages/Figure_S1_v1_p10.tif` | 2131236 | `7aefc42dab1e40f7622f3a043de1ab19caff72685e3f2697a4e5843bbc15765d` |
| `figures_supp_v1/Figure_S2/Figure_S2_v1.pdf` | 544072 | `f9834b1241dce0be77ebedb91b5cbd00f638ade292ec2bf6b8cc30a9e7916cfd` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p01.fig` | 159144 | `73e115338ac934015eab7eeba49b66cb12abbf5ff68ffc1d29b4686b4dc7558c` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p01.tif` | 3601176 | `1a06e0a91503e02d7db34c34432e0da2a357d0fcf7c23f71b49ce0a178ffa6f1` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p02.fig` | 39952 | `c042bc1b3ae74e8820524ccec0b298e69741acb8598005fd9ae5684dbc7fba10` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p02.tif` | 1943698 | `5644e3942a22c37c0b10eeccb9f5697e2d0839d44b52995fdc069025a3905057` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p03.fig` | 159059 | `71972076c43a343c1b8a2d451009c5c2dc3976526bcb51874cdebb112b97dfdb` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p03.tif` | 3477604 | `3577e85f5c5f64ad5035eeeb09fc1b06de7a4c2ddbfe120ce37a045babc56c84` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p04.fig` | 39948 | `c7d5cfc22ce8bf0c85338aa7f5f4b9f24406f145b386dbad82e69ee902f38a27` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p04.tif` | 1956634 | `f380bea598638fa46a1e93a920a9f5a6ebb5fdf3eff02db48559af2bd3f5982e` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p05.fig` | 159246 | `35d0593b30be6d049df327f6d5451b7a9f6fb6cdc58f43af57aa1f64f7bcbcd3` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p05.tif` | 3702874 | `9615773dcbb8b74525735cafe3b0e20cc87e9638dfb422fd7896586ba7943ae2` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p06.fig` | 39958 | `f31471b4e5d5d69f36c741139d58b1c5a234a6ff50f10cae3a8648bfdb4e8ad4` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p06.tif` | 1924402 | `1fd5a373c282abfdfd2520d1278e560e92138d1fd74a88182cfc8c8f5a5bbb9d` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p07.fig` | 159277 | `10e7c6b4cd6e968e0d539213819b515e8922b7474eed61c7ee6fce44d2f3d0ca` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p07.tif` | 3720164 | `43921d76f7d68771a2b51d3794cdca911bde45f3682027d38f264e7003bc6b55` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p08.fig` | 39987 | `62917c7c5df2539cddf323862449277a4ae0edb91b383f5b7c5779d87f71416f` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p08.tif` | 1936366 | `9337b08351abe649e77698d68cc606dbcd79a00e4682f5b60a51a9a18ca8bc87` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p09.fig` | 159237 | `394cc5f54ff8b4503391d0f9a4e1ee252628762e0cebafc57510a578d35f3183` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p09.tif` | 3715742 | `e2781d397e1da5bdd4162f5f2d7d97aca3a103745fef50513c8b7b6e0eafea71` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p10.fig` | 39947 | `c75dc10485a2ef352d7aeaa9352d691df5fac524a6e7af896cc21cb0d0899f4b` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p10.tif` | 1924168 | `7212906d177a46599d3e0d75f889710aa75607fdcbe906d12719aca418e8e9ea` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p11.fig` | 159260 | `c6f9a93b56c767777856ccfb66f9e785d72ddad65cb2072045561387f727ef04` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p11.tif` | 3716426 | `e48e06505073d044e181f2ef920bda1890d36f41ce55f10f1d894491f28de8a6` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p12.fig` | 39983 | `22531595964f016357d64149ef3c650ff43561dd1534592bfc666fe737f487fa` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p12.tif` | 1936964 | `83f085457dfdef9535e38d72e0ce58234719f79072d2b09f42ade09c80bebf2f` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p13.fig` | 159228 | `825f15d35a1079e3c4fcff131290f724850f7e9a42aacde7615ca922ead25d78` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p13.tif` | 3741598 | `b0b4f151ef516a4270bb81e15840d2b160f107353383845a8d8676e4b3c2b406` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p14.fig` | 39962 | `0c5878fc4a5aa0a8514ca6b3c3c55cdc798570cf9474d997ec3ff604407e8615` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p14.tif` | 1931472 | `bfed39106730ea89db96069b2df38a9c9c4c5d28fa1d240b45bf52c318a952f1` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p15.fig` | 159249 | `d10eea518d3afe0c9facd46b482a9337303aa975f7e85e7d313c0220808eab8d` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p15.tif` | 3737666 | `ae533fe4217034e7c177b1a5a7cf592fd003d4959845f5b7c948dbc3f9455829` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p16.fig` | 39971 | `95642551425382525e6964caac5659c6d7f38329ac0d2efc2ce62f665f2be075` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p16.tif` | 1931498 | `1b5f6a2728520cd4ee2c2c814e46307791e3753a78fa30944ebbc104e52d2222` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p17.fig` | 159236 | `bd8b27329435cc7a4d055bd9b22f3769e62c5ce1de54966a9c9315f08c85b4d3` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p17.tif` | 3720526 | `2fc6cb7a5a145b8889c11289fc2945c1804b02edcbf2a69b94b62acdfbcb6f33` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p18.fig` | 39990 | `daf1b6d89c438b9bcb0ac165051584fd1b70c630eef52a1394daddc8600fce21` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p18.tif` | 1950544 | `46d3a76659adc95754095e25bc8232a3e26fc7ec167facb991b761e102c77335` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p19.fig` | 159183 | `3d04865ecc7de7d9fb0466f2130df80572f6ca47b065612f16c40dfb63ef653a` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p19.tif` | 3823318 | `242aa34eeff5da446a9dbb66d9247d128fccd540ab92faab2dbb44793bcc2e68` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p20.fig` | 39927 | `680b1bc84ad61b72b618ff721047d33c6536f57d6f01c221fa9d8939f650fd59` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p20.tif` | 1926264 | `770d022f554ad8be86443786db59289eebbdc2ea99c25055afe28c281a1cd60a` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p21.fig` | 158679 | `f38ef05515377f19d1c33edd354de58978c8a5017551cf64ef0c327c8396ceb3` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p21.tif` | 3507910 | `ef7c322cae5b67164b655661f04751dd2ae21d91c5db3e51892ca8ee751a2645` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p22.fig` | 39883 | `cd27e94f931f4ac719fd8944329c131253fb0a93f2112b333f9d311808c7d495` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p22.tif` | 1867368 | `309df1a69eeaa120528178d0cb30a5205c4515df8603a1f4ec32550af9c75929` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p23.fig` | 157262 | `43daa8f2af0d2c9ae8622cccd9dec12dc1a3fa5945595ca16c16878efd7ed0d3` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p23.tif` | 2788906 | `d67e25b40812c1bb395460e3390a0fe2d8a8a2d1dbb2615e1b816825fa1ab0a4` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p24.fig` | 39804 | `f276da2e4a47e755f26ed3778f363a4e4f5b09b27f68132308576caf0d3eb99a` |
| `figures_supp_v1/Figure_S2/pages/Figure_S2_v1_p24.tif` | 1690130 | `eb92e4e11a8512a88c72a81074457b362ce05e86b0d78c0d5ad198531a9c5c4e` |
| `figures_supp_v1/Figure_S3/Figure_S3_v1.pdf` | 527977 | `a883b1a07da8d0f4d95a7ca449cef76740d762ac1e7357db852340be0ae27bb7` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p01.fig` | 154710 | `f8a4d5713239ed24f68f06efab69db679f601359d8f7518c9b5ac77d24533f00` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p01.tif` | 2873854 | `83ba07b63b6489d8bd06bc2a359c08610b2fb697c20d14d10a514e6b331b1e33` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p02.fig` | 39056 | `bd6942d9974736bb30e0fd0a1a90d697a19d68696e5ff2f55b8a8c856c947924` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p02.tif` | 1867466 | `5e4e13835cf13a9244876d60e29ff6b32c42b64272358ef67a3a7ed74baace9d` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p03.fig` | 154713 | `5b466817352d3be4efd5fa47a31691fc25494f7b2f54a204a0526bbe9088fabe` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p03.tif` | 2840774 | `cec296c81723397d9d76877d9e33057510d5ec8e6b047afd7a9d463e7ad91720` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p04.fig` | 39076 | `52ace656dd755ec84ef2591fe3171e054f78e43588d45d5e1e54440faa8d5ead` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p04.tif` | 1897692 | `743d472ab46f78ee851d977b4357b34a59bce64939418cd753e41a4d597670b5` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p05.fig` | 154541 | `6ed97d28b4921a6397c94b8a65c2d8c1a5289ac5d8fcaa88521c0ce87c453e28` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p05.tif` | 2844238 | `d0ae098e5c6dfe7906ece1265aa98e211b6a1921fd52e5a222296dd22df81b53` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p06.fig` | 39043 | `7c5fbdcd7e34bebec9a5dfc1436ae008a09df2527b504c1affb342c02bc7776b` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p06.tif` | 1896458 | `545ed46bf66dff6846cd993bdc06c108a900e31f5bfafb010a062822ebeae4c2` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p07.fig` | 154541 | `05648b9c68cac7de5ad24e53a676121e1b2f3d59b4967c5d2380b0de043ebe8c` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p07.tif` | 2855826 | `618950c048e7a5a54f0a17ee80377d84e31c3b82aa9d14e9f306b5de89442aad` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p08.fig` | 39062 | `9c4b9916650752f57900ca6a005a19b45137fb5dd3009ac5760118b7257221f2` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p08.tif` | 1900008 | `da956a5719abbfa344965c7d387972f02c4dfc66cfaf2f348dbda554a7536448` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p09.fig` | 154521 | `4195dfbc8fd3e37b2f1cca43d2b49c05049ef960b5937fa0979e9efdc7078a21` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p09.tif` | 2887358 | `56d87090cad6542a071b10a90348e2eaa3cf0541c7a49507c592ad353be313bb` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p10.fig` | 39053 | `82251dcce33a7fc5f52fbf9348595432c7400b74f2acffac7a2955e0cf025ade` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p10.tif` | 1898316 | `9724c0b0c71264400199fe244565dfae861d797c79e39c974fde20ae5abe6a57` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p11.fig` | 154509 | `886e390d38080c08f16229295d547e247c4ae1ce9b1a8eab60724dae5595371d` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p11.tif` | 2889320 | `34a32476717105bf3d2c882dcd14e00770471c0d1f4471214715dc8becca072a` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p12.fig` | 39067 | `e6d7ab94b829332eb20adc733da2e3b21161beddbfe30b2c2a0a98c613c53c8a` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p12.tif` | 1898094 | `2d5663aa99339f40f0bc71ac35142569b59b8282aec4ee5bbb625e863d550889` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p13.fig` | 154544 | `e8f94c72a6e3c038bd93c969bf198172f1efffffb28a0512af443cae91d72670` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p13.tif` | 2859684 | `48ffdc1375d8a4ce20f43b8ae1f70f0d7f4c33ca249660a8780cc852574bb153` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p14.fig` | 39039 | `207397ba5c40f8ede4f51dccd008e4dbbd6bc01130ec4877a1c72bea4af7a359` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p14.tif` | 1895892 | `14395099d4ae10fa47dfc92ddd773945a65a8ccc66c6fcfc8b1e9820d0701c6d` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p15.fig` | 154532 | `be928e9c8f81a11f1f65f563a8d88c5a50a249cbcce7d9cfb3a15d5f89b4f2e6` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p15.tif` | 2872758 | `e6b72921aec14df4deb84129e17532e22b67a429e7eba1db82b1f1d70cb238a1` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p16.fig` | 39084 | `a6cf5407c488c88d6eff1e6756ac19737865b86d825f560ee7ad9e2d12ee5f30` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p16.tif` | 1898060 | `209ad95ea03f4d188d6b5f80172db7903276fcf0f4dc777142299f3f5496476c` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p17.fig` | 154555 | `61f4e4d7feda21dca62c15606dbbf5b335371c7fa44dcc07e5b728a818da4a2f` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p17.tif` | 2847970 | `185aba386ea3b4810f5ad2bf20cf4c741db9a68af82748437b484a7f1bb5d305` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p18.fig` | 39038 | `df876e2557d297a9d81d8b41f3e68dac6d8352d3b431e1a30e21dc0666e174cb` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p18.tif` | 1900920 | `d32d34fedaef6dfe746d02c70825831b518a76e201d7957d529a1f72a5ed67e6` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p19.fig` | 155340 | `d001f25a0d918e67914f332454a9f29c6837920edd3f2e82b9dd5ee177bd5b8d` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p19.tif` | 3275012 | `01b848228c25ec9d9d48b76d27500a6e07df860f85d1b983a23f950d95857cfa` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p20.fig` | 39124 | `d360f9085dc8026d35a1d083b6fd0711a1e6bb91bf8de917f903e294278807b5` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p20.tif` | 1905752 | `03230c300d3fa873bd913e71654e4a7a90ada1b449a2b25195707c85d6a376f1` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p21.fig` | 155316 | `1e9fbd0e853fa6833d6c39eb4f87c72ef88caa5b842204950b0f55ac1ec0af16` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p21.tif` | 3086786 | `9b1942e716ffdf072458ec97f0e512a70d71e78c00174ac794ead675a3443003` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p22.fig` | 39096 | `dc4836c5205f1fde6ba3b1ff70410022e07498be80e8b0a12563ac8ae3457e3e` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p22.tif` | 1873664 | `4ed22423a5dede01b45db1a156ddd87979b0a65bd3001adc9fa0c4eef330296b` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p23.fig` | 155103 | `09adfc57c611777006c336fa6914e3d444fc71ab39afc5d10aced7b6f1c2aaf8` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p23.tif` | 2715140 | `bfd31d3aff9f33d546b2d33b90562971d318ccf1f87c9961c228d1701dcbef48` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p24.fig` | 39047 | `db63b41454cb5b7304dee6962d7de9b23c68e05bb4f9137d7bcde3a09ac5b2f6` |
| `figures_supp_v1/Figure_S3/pages/Figure_S3_v1_p24.tif` | 1750972 | `d11e1500ebcbf75dbc852091c1d6f9f2d06b9d056b8ef0ce828b13f2218ddaee` |
| `figures_supp_v1/Figure_S4/Figure_S4_v1.fig` | 37658 | `3f102cc35a9478a8da59c9da2606b5054af0ae1ad636c7d1a9c2c093080a8979` |
| `figures_supp_v1/Figure_S4/Figure_S4_v1.pdf` | 22077 | `f452e619d472b280adb746adf9d3eedcf90e32cbf40fb34ccb77c18ef4fceef7` |
| `figures_supp_v1/Figure_S4/Figure_S4_v1.tif` | 3178902 | `aa27039b0bafc49af92bd0ff2df48064d311c01ffa3a4134a3242071489c6c94` |
| `figures_supp_v1/Figure_S5/Figure_S5_v1.pdf` | 202017 | `fd820b0e6fabeae59f740cdb2bc3d8e7be541f93ba1e6bd8e08f72598c0ee86a` |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p01.fig` | 76331 | `f94655d014f17c7701a8a8559346bf6813ac7ade3638417ec74584a62f113627` |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p01.tif` | 3779412 | `6b35b3d8d80d906564fe08eb05f4d519335d758ab73e02712af176a5e2db93b8` |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p02.fig` | 78298 | `a159672a2898cda409f43d1eb25628c91f4480d00b0e271016c690023abcfdb5` |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p02.tif` | 3453932 | `36951e418646be61d5777f3accb845d33ac0f2a7e3d4342cef6d81cc54789f10` |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p03.fig` | 78409 | `e94e3582f88ec409ed12aa5dd940125118fd5ffca8145849b2bdbd127da8fe83` |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p03.tif` | 3442916 | `84620386f1e6b403fe55a7390aa60a5a49d467ea10ca81ec8c77c227036cf142` |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p04.fig` | 78268 | `31bf4778a8ac8021760f0bc14bf9d2c3a07ee9152f8e4609f4b31cbe91c38a9f` |
| `figures_supp_v1/Figure_S5/pages/Figure_S5_v1_p04.tif` | 3446662 | `12e91283e41c9451e6b0415d4c13774d81c0e1b686082cf4aef1d98e824126bb` |
| `figures_supp_v1/Figure_S6/Figure_S6_v1.fig` | 63155 | `f291e0f689441127855035b3979ac8c91dfba8b676b484a8fac5ee6304ff85a6` |
| `figures_supp_v1/Figure_S6/Figure_S6_v1.pdf` | 19268 | `dd8181fbebb7793fc6cec6ada3580313f2db077666b04fc6c3ec9bcedf7542b9` |
| `figures_supp_v1/Figure_S6/Figure_S6_v1.tif` | 3596050 | `a9913f886188f309afad2c6a0e5ed4df5d55ecb4a274001e36e78f3123f3f6aa` |
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
| `tables/Table_S1_v1.csv` | 129 | `52f0ca30a7653f30bd1f23ebecee92255a62ff9a65d48abb85de4a2d906141c5` |
| `tables/Table_S1_v1.docx` | 37508 | `3deb13f5acd7bb57fa6c53df62fddbefe5d03e0791bd3abce755374da5c2f0b7` |
| `tables/Table_S1_v1.pdf` | 51124 | `7155cc24fd621bf941c5b2533350cc30903c8f1c8f4405491fadec75e252c211` |
| `tables/Table_S2_v1.csv` | 5468 | `2feca4d14f57cec04006f95b1d5faa0fb1588592d0989cbcaa242ed5a712d1f2` |
| `tables/Table_S2_v1.docx` | 40346 | `1fa1041605b3cf06f4a1582d1f8e874a29a1183081325586ec42ecaa51584992` |
| `tables/Table_S2_v1.pdf` | 145406 | `f3b24d354f474b2a6fad53ce70b92e96deb2b0f0059b7794b7aec50a33ff7f44` |
| `tables/Table_S3_v1.csv` | 3547 | `ce27866290385ebf25cd860ad47215825da3f6dd38b921419ce876e8249b782a` |
| `tables/Table_S3_v1.docx` | 39421 | `9ac8dbefc1b70577d180fdd3b967798d0b0742825853d2ce686af2af5784a7d6` |
| `tables/Table_S3_v1.pdf` | 170491 | `1dafb9aa28f8fa2772948eb25d075ce634efe3c025f4657379d52b5e059d1ab6` |
| `tables/Table_S4_v1.csv` | 1435 | `fe2f06229b1f75dc14d2a1c352b93961cfdb50da834bcbc1fbc93972b1df80c7` |
| `tables/Table_S4_v1.docx` | 38625 | `233c02e0d22569ddaed19fffd54f25a7e108ee15c20c21cd8f413e154f237d6d` |
| `tables/Table_S4_v1.pdf` | 86436 | `81e71f1c577566d248e26afe7ced14c7d00f804e7d279ef95b4cadbf6b8a7103` |
| `tables/Table_S5_v1.csv` | 3918 | `10d2ded8138209791bc04a201c88cf7a7e1a58530736a0500d974c7e64116172` |
| `tables/Table_S5_v1.docx` | 39294 | `ba3723ea73ad5be9b7cb0c8350e6c80abb3fdc5d9563d822a0eb8d7400faa800` |
| `tables/Table_S5_v1.pdf` | 161531 | `6c5c9c3c99f2633e038f8f9c64e67467d4124be5e72c2aac947fd91ce0a05f51` |
| `tables/Table_S5_v2.csv` | 5468 | `2feca4d14f57cec04006f95b1d5faa0fb1588592d0989cbcaa242ed5a712d1f2` |
| `tables/Table_S5_v2.docx` | 40346 | `6ae658ca5fef32401c84ec89b87937530ebc94c98bfa1ef2bdae27d61bf1a9a1` |
| `tables/Table_S5_v2.pdf` | 145365 | `7289939ac49f48fa113012e16b0e1cafdc35b3687576fa1b6a0e99ae389f1223` |
| `tables/Table_S6_v1.csv` | 1971 | `081e514289dc8856a612be2f46da11ca6d880409759517834cfee950a78cbcc7` |
| `tables/Table_S6_v1.docx` | 38749 | `fc2a1493bfcfbd577ee6397a77e5fead443e623120d58296638d93009fc22e32` |
| `tables/Table_S6_v1.pdf` | 130403 | `4263a5bc03d0d10b20f28cc910f1238c7f8b4d48b9096ae8548b1c7da9c927bb` |
