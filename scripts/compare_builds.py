#!/usr/bin/env python3
"""Compare a previous build (directory with the same relative layout) with the current one for the clean-rebuild
test (template §4-0): canonical bytes, TIF pixels, PDF text spans + vector-path signatures, PPTX slide XML, DOCX body
XML. Writes qa/REBUILD_TEST.md and exits non-zero on any difference.

    .venv/bin/python -I scripts/compare_builds.py <before_dir>
"""
import sys

sys.dont_write_bytecode = True

import hashlib  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pymupdf  # noqa: E402
from PIL import Image  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def pdf_sig(p):
    doc = pymupdf.open(p)
    sig = []
    for page in doc:
        sig.append(("page", round(page.rect.width, 3), round(page.rect.height, 3)))
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for s in ln["spans"]:
                    sig.append(("t", s["text"], s["font"], round(s["size"], 2), tuple(round(v, 2) for v in s["bbox"]),
                                s["color"]))
        for d in page.get_drawings():
            sig.append(("d", d.get("type"), str(d.get("fill")), str(d.get("color")), round(d.get("width") or 0, 3),
                        tuple(round(v, 2) for v in d["rect"])))
    return hashlib.sha256(repr(sig).encode()).hexdigest(), len(sig)


def tif_eq(a, b):
    A, B = np.asarray(Image.open(a)), np.asarray(Image.open(b))
    return A.shape == B.shape and bool((A == B).all()), A.shape


def zip_member(p, name):
    return zipfile.ZipFile(p).read(name)


STEMS_V1 = ("figures/Figure_1/Figure_1", "figures/Figure_2/Figure_2", "figures/Figure_3/Figure_3",
            "figures/Figure_4/Figure_4", "graphical_abstract/Graphical_abstract", "tables/Table_1",
            "tables/Table_2", "tables/Table_3")
STEMS_V2 = ("figures_v2/Figure_1/Figure_1_v2", "figures_v2/Figure_2/Figure_2_v2", "figures_v2/Figure_3/Figure_3_v2",
            "figures_v2/Figure_4/Figure_4_v2", "figures_v2/Figure_5/Figure_5_v2",
            "graphical_abstract/Graphical_abstract_v2", "tables/Table_1_v2", "tables/Table_2_v2", "tables/Table_S5_v2")


STEMS_V3 = ("figures_v3/Figure_1/Figure_1_v3", "figures_v3/Figure_2/Figure_2_v3", "figures_v3/Figure_3/Figure_3_v3",
            "figures_v3/Figure_4/Figure_4_v3", "tables/Table_2_v3")


def main():
    before = Path(sys.argv[1])
    v2 = "--v2" in sys.argv[2:]
    v3 = "--v3" in sys.argv[2:]
    rows, ok = [], True
    for f in sorted((before / "canonical").iterdir()):
        same = sha(f) == sha(ROOT / "canonical" / f.name)
        rows.append((f"canonical/{f.name}", "bytes", "identical" if same else "DIFFERENT"))
        ok &= same
    for stem in (STEMS_V3 if v3 else STEMS_V2 if v2 else STEMS_V1):
        b, a = before / stem, ROOT / stem
        sb, nb = pdf_sig(f"{b}.pdf")
        sa, na = pdf_sig(f"{a}.pdf")
        rows.append((f"{stem}.pdf", f"text + vector paths ({na} items)", "identical" if sb == sa else "DIFFERENT"))
        ok &= sb == sa
        if Path(f"{b}.tif").exists():
            eq, shape = tif_eq(f"{b}.tif", f"{a}.tif")
            rows.append((f"{stem}.tif", f"pixels {shape[1]} x {shape[0]}", "identical" if eq else "DIFFERENT"))
            ok &= eq
        if Path(f"{b}.pptx").exists():
            same = zip_member(f"{b}.pptx", "ppt/slides/slide1.xml") == zip_member(f"{a}.pptx", "ppt/slides/slide1.xml")
            rows.append((f"{stem}.pptx", "slide XML", "identical" if same else "DIFFERENT"))
            ok &= same
        if Path(f"{b}.docx").exists():
            same = zip_member(f"{b}.docx", "word/document.xml") == zip_member(f"{a}.docx", "word/document.xml")
            rows.append((f"{stem}.docx", "document XML", "identical" if same else "DIFFERENT"))
            ok &= same
    L = ["# Clean rebuild test (template §4-0)" + (" — v4 revision outputs" if v3 else " — v3 revision outputs" if v2 else ""), "",
         "All generated outputs were moved out of the repository; canonical data were re-frozen from the package and "
         "every figure, the graphical abstract and the tables were rebuilt from their scripts (each MATLAB figure in "
         "its own `matlab -batch \"close all force; clear; run(...)\"` session; no existing `.fig` was opened). "
         "The rebuilt files were compared with the previous build.", "",
         "| file | compared | result |", "|---|---|---|"]
    L += [f"| `{r[0]}` | {r[1]} | {r[2]} |" for r in rows]
    L += ["", f"**Result: {'PASS' if ok else 'FAIL'}** ({sum(r[2] == 'identical' for r in rows)} / {len(rows)} identical). "
          "The `.fig` files are checked by `verify_plotted.m` on the rebuilt figures (qa/plotted_vs_canonical.json); "
          "PDF creation dates differ by construction and are not part of the comparison."]
    (ROOT / "qa" / ("REBUILD_TEST_v4.md" if v3 else "REBUILD_TEST_v3.md" if v2 else "REBUILD_TEST.md")).write_text("\n".join(L) + "\n")
    print("\n".join(f"{r[2]:>10}  {r[0]}  ({r[1]})" for r in rows))
    print("REBUILD", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
