# Preflight (2026-10-27)

| item | result |
|---|---|
| MATLAB | 25.2.0.2998904 (R2025b) (`/Applications/MATLAB_R2025b.app/bin/matlab`; not on PATH) |
| Arial in MATLAB `listfonts` |  (1 = available; figure template §2-1 preflight) |
| Arial font files | /System/Library/Fonts/Supplemental/Arial.ttf, Arial Bold.ttf |
| Python (project venv `.venv`, --copies, exFAT) | Python 3.12.8; packages in `requirements.lock.txt` |
| Node | v25.4.0; pptxgenjs 4.0.1 in project `node_modules` (`package.json`, `package-lock.json`) |
| poppler | pdffonts version 26.04.0 |
| LibreOffice | LibreOffice 26.2.2.2 1f77d10d6938fd34972958f64b2bcfa54f8b1ba5 |
| Package manifest | `shasum -a 256 -c MANIFEST_SHA256.txt` in `/Volumes/ADDATA/医療動画/SS_DS203_manuscript_20261020`: 248 / 248 OK (exit 0); 249 files incl. the manifest |

Nothing was installed into system or base environments. Templates copied into `templates/` from `~/Desktop/` (SHA-256 in `templates/SHA256SUMS.txt`).
`SS_DS203_JBI_manuscript_plan_v3.md` was not provided and was not found (Spotlight, ~/Downloads, ~/Desktop, ADDATA/医療動画): the element definitions of the task §5 (which cite plan v3 §4) are used; recorded in `POST_RESULT_PRESENTATION_JBI.md`.
