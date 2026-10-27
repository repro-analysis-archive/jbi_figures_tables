# Audit bundle

| file | bytes | SHA-256 |
|---|---|---|
| `AUDIT_JBI_figures_tables_20261027-0947.zip` (work folder and ~/Desktop/) | 4906900 | `c6b3ea0c5afb37afec1d69f9c3ea4970e4a8d6524cf7cbf872a5ecf42d1d776a` |

Contents: `git archive` of commit 1c43406 (all tracked outputs, canonical data, scripts, documents, QA), `GIT_LOG.txt`, `GIT_LOG_ONELINE.txt`, `AUDIT_README.txt` and `AUDIT_MANIFEST_SHA256.txt` (89 files, all verified OK after packing). The zip itself is not tracked (`.gitignore`).

## v3 revision bundle

| file | bytes | SHA-256 |
|---|---|---|
| `AUDIT_JBI_figures_tables_v3_20261027-1031.zip` (work folder and ~/Desktop/) | 10586465 | `6ed048ab66ebf049d41b8f43ecfbcef5c11d7d45de593945d5497a350406b854` |

Contents: `git archive` of commit e20277a (v3 outputs with the `_v2` suffix, the unchanged earlier outputs, canonical data, scripts, records, QA), `GIT_LOG.txt`, `GIT_LOG_ONELINE.txt`, `AUDIT_README.txt`, `AUDIT_MANIFEST_SHA256.txt` (147 files, all verified OK after packing).

## v4 revision bundle

| file | bytes | SHA-256 |
|---|---|---|
| `AUDIT_JBI_figures_tables_v4_20261027-1119.zip` (work folder and ~/Desktop/) | 16058997 | `e60b19f552597e98880fb040347bc9d15df46ab488d5d761be989a2d74ea63be` |

Contents: `git archive` of commit ce95897 (v4 outputs with the `_v3` suffix, the unchanged earlier outputs, canonical data, scripts, records, QA), `GIT_LOG.txt`, `GIT_LOG_ONELINE.txt`, `AUDIT_README.txt`, `AUDIT_MANIFEST_SHA256.txt` (202 files, all verified OK after packing and again after unzipping the Desktop copy). The two earlier bundles were copied to ~/Desktop/ again on 2026-10-27 (SHA-256 unchanged).

## v5 revision bundle

| file | bytes | SHA-256 |
|---|---|---|
| `AUDIT_JBI_figures_tables_v5_20261027-1146.zip` (work folder and ~/Desktop/) | 25544288 | `ad9e7a16c2cc6d481ace110f9d645391c4de1d4271d22b514e70ae6d0bbb55c1` |

Contents: `git archive` of commit f71cfb3 (v5 outputs `figures_v4/` and `CAPTIONS_v4.md`, the unchanged tables and graphical abstract, all earlier outputs, canonical data, scripts, records, QA), `GIT_LOG.txt`, `GIT_LOG_ONELINE.txt`, `AUDIT_README.txt`, `AUDIT_MANIFEST_SHA256.txt` (256 files, all verified OK after packing and again after unzipping the Desktop copy).

## Supplement v6 bundle

| file | bytes | SHA-256 |
|---|---|---|
| `AUDIT_JBI_supplement_v6_20261027-1419.zip` (work folder and ~/Desktop/) | 133485177 | `0b78293c9d09f22cb6194dacc7041362ea259845dbb28ced43d47dee965fc63c` |

Contents: `git archive` of commit 49b7a0e (supplement outputs `figures_supp_v1/`, `tables/Table_S*_v1.*`, `CAPTIONS_supplement_v1.md`, `supplementary/Supplementary_Material_v1.docx`, `canonical_supplement/`, `inputs/`, the unchanged main set and earlier outputs, scripts, records, QA), `GIT_LOG.txt`, `GIT_LOG_ONELINE.txt`, `AUDIT_README.txt`, `AUDIT_MANIFEST_SHA256.txt` (468 files, all verified OK after packing and again after unzipping the Desktop copy).

## v7 bundle (graphical abstract v3, Supplementary Tables S3/S4 v2)

| file | bytes | SHA-256 |
|---|---|---|
| `AUDIT_JBI_GA_tables_v7_20261027-1635.zip` (work folder, `ZIP_ARCHIVE/current/`, ~/Desktop/) | 1256024 | `ad4406a639c83d5f8e851730bf008e19e6e5a80a031dd28190681b9bb6f94971` |

Contents: the v7 files of commit 1443c31 (GA v3 .pdf / .pptx / .tif / .js; Tables S3 and S4 v2 .docx / .pdf / .csv;
`canonical_supplement/validation.json`, `SHA256SUMS.txt`, `inputs_sha256.json`; POST_RESULT, CAPTIONS_supplement_v2,
QA JSON; scripts), `GIT_LOG.txt`, `GIT_LOG_ONELINE.txt`, `AUDIT_README.txt` (with the GA text extracted from the PDF),
`AUDIT_MANIFEST_SHA256.txt` (28 files, verified after packing and after unzipping the Desktop copy).

## v8 bundle and handoff (Supplementary Table S2 v2; auditor's Word update v2)

| file | bytes | SHA-256 |
|---|---|---|
| `AUDIT_JBI_tableS2_v8_20261027-1704.zip` (work folder, `ZIP_ARCHIVE/current/`, ~/Desktop/) | 162393 | `86c965130318f1941bc9584bf3042fefaa67d0ac1025c57c30392f1c54439950` |
| `HANDOFF_JBI_word_update_v2_20261027-1700.zip` (work folder, `ZIP_ARCHIVE/current/`, ~/Desktop/) | 1336235 | `06eef46acd743f416abc68e5c19b17af37b580715788cd71b246333f50328086` |

Audit bundle contents: the v8 files of commit 8b12f70 (Table S2 v2 .docx / .pdf / .csv; `canonical_supplement/validation.json`,
`SHA256SUMS.txt`, `inputs_sha256.json`; POST_RESULT, CAPTIONS_supplement_v3, `qa/tables_qa_supp_v2.json`; scripts
build_table_S2_v2.py, build_tables.py, freeze_supplement.py, qa_tables_supp_v2.py), `GIT_LOG.txt`, `GIT_LOG_ONELINE.txt`,
`AUDIT_README.txt` (the three exact values and displays, the S2 v2 / S4 v2 cross-check, QA results, the handoff zip's
SHA-256, file SHA-256), `AUDIT_MANIFEST_SHA256.txt` (16 files, verified after packing and after unzipping the Desktop copy).

Handoff contents (18 files in `HANDOFF_JBI_word_update_v2_20261027-1700/`): `README.md` (changes since the auditor's
deliverables of 2026-10-27, the four asks verbatim, file SHA-256); `01_text/` the investigator's manuscript v6, the
v5 → v6 change list (25 rows) and Supplementary Methods draft v4 (copied unchanged from ~/Downloads, SHA-256 equal);
`02_figures_tables/` GA v3 .pdf / .tif, Tables S2–S4 v2 .docx / .pdf / .csv, `CAPTIONS_supplement_v3.md`;
`03_validation/` `validation.json` and POST_RESULT sections 10–11 verbatim. Every file verified against the README
after unzipping the Desktop copy (17 / 17). `HANDOFF_*.zip` added to `.gitignore` (the work-folder copy is not tracked).
