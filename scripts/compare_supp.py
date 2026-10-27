#!/usr/bin/env python3
"""Clean-rebuild comparison of the supplement v6 outputs (template §4-0): canonical_supplement bytes, every figure PDF
(text spans + vector paths of all pages, compare_builds.pdf_sig), every TIF (pixels), the table .docx (document XML),
.csv (bytes) and .pdf (text + paths). Writes qa/REBUILD_TEST_supp_v6.md and exits non-zero on any difference.

    .venv/bin/python -I scripts/compare_supp.py <before_dir>
"""
import sys

sys.dont_write_bytecode = True

import importlib.util  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("compare_builds", HERE / "compare_builds.py")
cb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cb)
ROOT = HERE.parent


def main():
    before = Path(sys.argv[1])
    rows, ok = [], True

    def add(name, what, same):
        nonlocal ok
        rows.append((name, what, "identical" if same else "DIFFERENT"))
        ok &= same

    for f in sorted((before / "canonical_supplement").iterdir()):
        add(f"canonical_supplement/{f.name}", "bytes", cb.sha(f) == cb.sha(ROOT / "canonical_supplement" / f.name))
    for f in sorted((before / "figures_supp_v1").rglob("*")):
        rel = f.relative_to(before)
        if f.suffix == ".pdf":
            sb, n = cb.pdf_sig(f)
            sa, _ = cb.pdf_sig(ROOT / rel)
            add(str(rel), f"text + vector paths ({n} items)", sb == sa)
        elif f.suffix == ".tif":
            eq, shape = cb.tif_eq(f, ROOT / rel)
            add(str(rel), f"pixels {shape[1]} x {shape[0]}", eq)
    for n in range(1, 7):
        stem = f"tables/Table_S{n}_v1"
        add(f"{stem}.docx", "document XML", cb.zip_member(before / f"{stem}.docx", "word/document.xml") ==
            cb.zip_member(ROOT / f"{stem}.docx", "word/document.xml"))
        add(f"{stem}.csv", "bytes", cb.sha(before / f"{stem}.csv") == cb.sha(ROOT / f"{stem}.csv"))
        add(f"{stem}.pdf", "text + vector paths", cb.pdf_sig(before / f"{stem}.pdf")[0] == cb.pdf_sig(ROOT / f"{stem}.pdf")[0])
    d = "supplementary/Supplementary_Material_v1"
    add(f"{d}.docx", "document XML", cb.zip_member(before / f"{d}.docx", "word/document.xml") ==
        cb.zip_member(ROOT / f"{d}.docx", "word/document.xml"))
    import zipfile
    zb, za = zipfile.ZipFile(before / f"{d}.docx"), zipfile.ZipFile(ROOT / f"{d}.docx")
    media = sorted(n for n in zb.namelist() if n.startswith("word/media/"))
    add(f"{d}.docx", f"embedded images ({len(media)})", media == sorted(n for n in za.namelist() if n.startswith(
        "word/media/")) and all(zb.read(n) == za.read(n) for n in media))
    add(f"{d}.pdf", "text + vector paths (LibreOffice rendering)", cb.pdf_sig(before / f"{d}.pdf")[0] ==
        cb.pdf_sig(ROOT / f"{d}.pdf")[0])
    L = ["# Clean rebuild test (template §4-0) — supplement v6", "",
         "The supplement outputs and `canonical_supplement/` were moved out of the repository; the canonical data were "
         "re-frozen from the package (`freeze_supplement.py`) and every supplementary figure was rebuilt from its `.m` in its "
         "own `matlab -batch` session (no existing `.fig` opened), the tables from `build_tables_supp_v1.py`; the rebuilt "
         "files were compared with the previous build. The `.fig` files are checked by `verify_plotted_supp_v6.m` on the "
         "rebuilt figures; PDF creation dates differ by construction and are not compared.", "",
         "| file | compared | result |", "|---|---|---|"] + [f"| `{a}` | {b} | {c} |" for a, b, c in rows] + \
        ["", f"**Result: {'PASS' if ok else 'FAIL'}** ({sum(r[2] == 'identical' for r in rows)} / {len(rows)} identical)."]
    (ROOT / "qa" / "REBUILD_TEST_supp_v6.md").write_text("\n".join(L) + "\n")
    bad = [r for r in rows if r[2] != "identical"]
    print(f"compared {len(rows)}; different {len(bad)}", *[f"\n  {b}" for b in bad])
    print("REBUILD-SUPP", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
