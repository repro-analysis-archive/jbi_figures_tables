#!/usr/bin/env python3
"""Whole-image TIF ↔ PDF ink check (v4 finding: MATLAB `print -dtiff` at 1,200 dpi renders in 4,000-px tiles and
clips markers that straddle a tile boundary; the vector PDF is correct). The PDF is rasterised at the TIF resolution
(poppler) and aligned by the best whole-pixel shift; ink (gray < 128) present in one image and absent within 6 px
(0.13 mm at 1,200 dpi) in the other is counted per 64-px block, and blocks with ≥ 120 such pixels are listed in mm.
A thinner TIF stroke alone is not reported. Writes qa/tif_vs_pdf_<stem>.json.

    .venv/bin/python -I scripts/qa_tif_vs_pdf.py figures_v3/Figure_2/Figure_2_v3 [more stems] [--tif-suffix _x]
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from PIL import Image, ImageFilter  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]
BLOCK, MIN_PX, RAD = 64, 120, 6


def mask(img):
    return np.asarray(img.convert("L")) < 128


def dilate(m):
    im = Image.fromarray((m * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.MaxFilter(2 * RAD + 1))) > 0


def blocks(miss, px_per_mm):
    h, w = miss.shape
    out = []
    for y in range(0, h, BLOCK):
        for x in range(0, w, BLOCK):
            n = int(miss[y:y + BLOCK, x:x + BLOCK].sum())
            if n >= MIN_PX:
                out.append(dict(x_mm=round((x + BLOCK / 2) / px_per_mm, 1), y_mm=round((y + BLOCK / 2) / px_per_mm, 1),
                                px=n))
    return out


def check(stem, tif_path):
    pdf = ROOT / f"{stem}.pdf"
    tim = Image.open(tif_path)
    dpi = float(tim.info["dpi"][0])
    T = mask(tim)
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", str(round(dpi)), "-png", "-singlefile", str(pdf), f"{d}/r"], check=True)
        R = mask(Image.open(f"{d}/r.png"))
    # align on a 4x-reduced grid first, then refine at full resolution
    best = None
    for dy in range(-3, R.shape[0] - T.shape[0] + 4):
        for dx in range(-3, R.shape[1] - T.shape[1] + 4):
            ys, xs = max(0, dy), max(0, dx)
            h = min(T.shape[0] + min(0, dy), R.shape[0] - ys); w = min(T.shape[1] + min(0, dx), R.shape[1] - xs)
            s = int((T[ys - dy:ys - dy + h:4, xs - dx:xs - dx + w:4] ^ R[ys:ys + h:4, xs:xs + w:4]).sum())
            if best is None or s < best[0]:
                best = (s, dx, dy)
    _, dx, dy = best
    ys, xs = max(0, dy), max(0, dx)
    h = min(T.shape[0] + min(0, dy), R.shape[0] - ys); w = min(T.shape[1] + min(0, dx), R.shape[1] - xs)
    Tc, Rc = T[ys - dy:ys - dy + h, xs - dx:xs - dx + w], R[ys:ys + h, xs:xs + w]
    px_per_mm = dpi / 25.4
    pdf_not_in_tif = blocks(Rc & ~dilate(Tc), px_per_mm)
    tif_not_in_pdf = blocks(Tc & ~dilate(Rc), px_per_mm)
    rep = dict(stem=stem, tif=str(tif_path), dpi=dpi, tif_px=list(T.shape[::-1]), pdf_raster_px=list(R.shape[::-1]),
               shift_px=[dx, dy], block_px=BLOCK, min_px=MIN_PX, dilation_px=RAD,
               pdf_ink_missing_in_tif=pdf_not_in_tif, tif_ink_missing_in_pdf=tif_not_in_pdf,
               result="PASS" if not pdf_not_in_tif and not tif_not_in_pdf else "FAIL")
    name = Path(tif_path).stem
    (ROOT / "qa" / f"tif_vs_pdf_{name}.json").write_text(json.dumps(rep, indent=1) + "\n")
    print(f"{name}: shift {dx},{dy}; PDF ink missing in TIF: {len(pdf_not_in_tif)} blocks "
          f"{[(b['x_mm'], b['y_mm'], b['px']) for b in pdf_not_in_tif]}; TIF ink not in PDF: {len(tif_not_in_pdf)} "
          f"blocks {[(b['x_mm'], b['y_mm'], b['px']) for b in tif_not_in_pdf]} -> {rep['result']}")
    return rep["result"] == "PASS"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    suf = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--tif-suffix=")), "")
    ok = all([check(s, ROOT / f"{s}{suf}.tif") for s in args])
    print("TIF-VS-PDF", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
