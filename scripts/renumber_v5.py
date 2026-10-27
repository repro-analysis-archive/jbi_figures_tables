#!/usr/bin/env python3
"""v5 renumbering to the order of first citation in Results (task v5 §2): byte copies of the source figures under the
new numbers in figures_v4/Figure_N/ (files Figure_N_v4.*), checked by SHA-256. Only the file names differ; the copied
make_*.m / .js are byte-identical too, so running one of them re-creates its source-named outputs (the renumbered
files are produced by this script). Figure 6 (source Figure_5_v2) gets its TIF from its byte-copied vector PDF via
poppler (task v5 header: the poppler TIF is used for every TIF), so only that TIF differs from its source; its ink
identity with the PDF is checked by qa_tif_vs_pdf.py. The new Figure 5 is built by figures_v4/Figure_5/make_Figure_5_v4.m.
Writes qa/renumber_v5.json.

    .venv/bin/python -I scripts/renumber_v5.py
"""
import sys

sys.dont_write_bytecode = True

import hashlib  # noqa: E402
import json  # noqa: E402
import shutil  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
# new number: (source folder, source stem, source script, extensions)
MAP = {
    1: ("figures_v3/Figure_1", "Figure_1_v3", "make_Figure_1_v3.js", ("pdf", "pptx", "tif")),
    2: ("figures_v3/Figure_4", "Figure_4_v3", "make_Figure_4_v3.m", ("fig", "pdf", "tif")),
    3: ("figures_v3/Figure_2", "Figure_2_v3", "make_Figure_2_v3.m", ("fig", "pdf", "tif")),
    4: ("figures_v3/Figure_3", "Figure_3_v3", "make_Figure_3_v3.m", ("fig", "pdf", "tif")),
    6: ("figures_v2/Figure_5", "Figure_5_v2", "make_Figure_5_v2.m", ("fig", "pdf")),
}
CONTENT = {1: "Study design", 2: "Erasure evaluation (A step-5 E3; B, C exploratory B)",
           3: "Confirmatory families (forest)", 4: "Dependence on prior action history",
           5: "NEW: relative bias and coverage at the slice", 6: "Exploratory X1/X2"}
POPPLER = "/opt/homebrew/bin/pdftoppm"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    rep, ok = {}, True
    for n, (folder, stem, script, exts) in MAP.items():
        dst = ROOT / "figures_v4" / f"Figure_{n}"
        dst.mkdir(parents=True, exist_ok=True)
        files = [(f"{stem}.{e}", f"Figure_{n}_v4.{e}") for e in exts]
        files.append((script, f"make_Figure_{n}_v4{Path(script).suffix}"))
        rows = []
        for s, d in files:
            src, out = ROOT / folder / s, dst / d
            shutil.copyfile(src, out)
            same = sha(src) == sha(out)
            ok &= same
            rows.append(dict(source=f"{folder}/{s}", file=f"figures_v4/Figure_{n}/{d}", sha256=sha(out),
                             byte_identical=same))
        if n == 6:
            pdf = dst / "Figure_6_v4.pdf"
            subprocess.run([POPPLER, "-r", "1200", "-tiff", "-tiffcompression", "lzw", "-singlefile", str(pdf),
                            str(dst / "Figure_6_v4")], check=True)
            rows.append(dict(source=f"{folder}/{stem}.pdf (rasterised by poppler, 1,200 dpi)",
                             file=f"figures_v4/Figure_{n}/Figure_6_v4.tif", sha256=sha(dst / "Figure_6_v4.tif"),
                             byte_identical=None, note=f"differs from {folder}/{stem}.tif (MATLAB raster) by design"))
        rep[f"Figure_{n}"] = dict(content=CONTENT[n], source=f"{folder}/{stem}", files=rows)
        print(f"Figure_{n}_v4 <- {folder}/{stem}: " + ", ".join(
            f"{Path(r['file']).name} {'identical' if r['byte_identical'] else ('poppler' if r['byte_identical'] is None else 'DIFFERENT')}"
            for r in rows))
    rep["Figure_5"] = dict(content=CONTENT[5], source="new (figures_v4/Figure_5/make_Figure_5_v4.m)", files=[])
    rep = dict(sorted(rep.items()))
    (ROOT / "qa" / "renumber_v5.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    print("RENUMBER", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
