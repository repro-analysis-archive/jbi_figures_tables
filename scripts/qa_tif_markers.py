#!/usr/bin/env python3
"""TIF ↔ PDF marker completeness: every marker drawn in the vector PDF must also be complete in the MATLAB TIF.
The PDF is rasterised at the TIF resolution (poppler), the two images are aligned by the best whole-pixel shift, and
for each marker (stroke path from the PDF) the dark-ink pixels inside its box are counted in both images. A marker
whose PDF ink is not covered by TIF ink within 6 px (0.13 mm at 1,200 dpi) for more than 10 % of its pixels is
reported (a missing side or face); a thinner TIF stroke alone (MATLAB rasterises marker edges thinner than poppler)
is not a defect. Writes qa/tif_markers_<stem>.json.

    .venv/bin/python -I scripts/qa_tif_markers.py figures_v3/Figure_2/Figure_2_v3 [more stems]
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pymupdf  # noqa: E402
from PIL import Image  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]
MM = 25.4 / 72
RAD = 6                                               # px at 1,200 dpi = 0.13 mm


def gray(p):
    return np.asarray(Image.open(p).convert("L"), dtype=np.int16)


def check(stem):
    pdf, tif = ROOT / f"{stem}.pdf", ROOT / f"{stem}.tif"
    dpi = float(Image.open(tif).info["dpi"][0])
    T = gray(tif)
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", str(round(dpi)), "-png", "-singlefile", str(pdf), f"{d}/r"], check=True)
        R = gray(f"{d}/r.png")
    # best whole-pixel shift (TIF origin in raster coordinates), searched on dark-pixel masks
    tb, rb = T < 128, R < 128
    best = None
    for dy in range(0, R.shape[0] - T.shape[0] + 3):
        for dx in range(0, R.shape[1] - T.shape[1] + 3):
            h = min(T.shape[0], R.shape[0] - dy); w = min(T.shape[1], R.shape[1] - dx)
            s = int((tb[:h, :w] ^ rb[dy:dy + h, dx:dx + w]).sum())
            if best is None or s < best[0]:
                best = (s, dx, dy)
    _, dx, dy = best
    px = dpi / 72
    page = pymupdf.open(pdf)[0]
    out, flagged = [], []
    for dr in page.get_drawings():
        r = dr["rect"]
        if not (0.3 <= r.width * MM <= 3.0 and 0.3 <= r.height * MM <= 3.0):
            continue
        if dr.get("type") != "s" or dr.get("color") is None:
            continue
        lw = (dr.get("width") or 0) * px
        x0, y0 = int(r.x0 * px - lw) - 1, int(r.y0 * px - lw) - 1
        x1, y1 = int(r.x1 * px + lw) + 2, int(r.y1 * px + lw) + 2
        P = rb[y0:y1, x0:x1]
        Tm = tb[y0 - dy - RAD:y1 - dy + RAD, x0 - dx - RAD:x1 - dx + RAD]
        near = np.zeros_like(P)
        for a in range(2 * RAD + 1):                  # TIF ink dilated by a (2 RAD + 1)^2 window
            for b in range(2 * RAD + 1):
                near |= Tm[a:a + P.shape[0], b:b + P.shape[1]]
        miss = int((P & ~near).sum())
        rec = dict(centre_mm=[round((r.x0 + r.x1) / 2 * MM, 2), round((r.y0 + r.y1) / 2 * MM, 2)],
                   size_mm=[round(r.width * MM, 3), round(r.height * MM, 3)], ink_pdf=int(P.sum()),
                   ink_tif=int(tb[y0 - dy:y1 - dy, x0 - dx:x1 - dx].sum()), uncovered=miss,
                   uncovered_frac=round(miss / max(1, int(P.sum())), 3))
        out.append(rec)
        if rec["uncovered_frac"] > 0.10:
            flagged.append(rec)
    rep = dict(stem=stem, dpi=dpi, shift_px=[dx, dy], markers=len(out), flagged=flagged,
               uncovered_frac_max=max(r["uncovered_frac"] for r in out))
    (ROOT / "qa" / f"tif_markers_{Path(stem).name}.json").write_text(json.dumps(rep, indent=1) + "\n")
    print(f"{Path(stem).name}: markers {len(out)}; shift {dx},{dy} px; max uncovered PDF ink {rep['uncovered_frac_max']}; "
          f"flagged {len(flagged)}", *[f"\n   {f}" for f in flagged])
    return not flagged


def main():
    ok = all([check(s) for s in sys.argv[1:]])
    print("TIF-MARKERS", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
