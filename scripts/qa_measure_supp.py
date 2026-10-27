#!/usr/bin/env python3
"""Measurement of the supplementary figures (supplement v6; template §7), every page: page size (mm), fonts
(pdffonts), text sizes and minimum, text overlaps / near pairs (< 0.5 mm), edge clearance (< 0.3 mm), raster objects;
per-page TIF: px, dpi, mm, and pixel identity with a fresh poppler rendering of the same PDF page (the TIF is made from
the vector PDF, so the two must be identical). Text measurement functions from qa_measure.py. The subscript A of
"φ_A" in the page titles and the subscript c of "m_c(ρ)" and "ρ_c" in the Figure S4 key touch their base glyphs by
design and are not counted as overlaps (counted separately).
Writes qa/measure_supp_v6.json.

    .venv/bin/python -I scripts/qa_measure_supp.py
"""
import sys

sys.dont_write_bytecode = True

import importlib.util  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pymupdf  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("qa_measure", HERE / "qa_measure.py")
qm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qm)
Image.MAX_IMAGE_PIXELS = None
ROOT = HERE.parent
MM = 25.4 / 72
FIGS = {"S1": 10, "S2": 24, "S3": 24, "S4": 1, "S5": 4, "S6": 1}
SUBSCRIPT = ((lambda a, b: a.endswith("φ") and b == "A"), (lambda a, b: a.endswith(("m", "ρ")) and b == "c"),
             (lambda a, b: a == "c" and b.startswith("(ρ)")))           # TeX subscripts touching their base glyph


def tif_of(n, p):
    d = ROOT / "figures_supp_v1" / f"Figure_{n}"
    return d / f"Figure_{n}_v1.tif" if n in ("S4", "S6") else d / "pages" / f"Figure_{n}_v1_p{p:02d}.tif"


def main():
    rep, ok = {}, True
    for n, npages in FIGS.items():
        pdf = ROOT / "figures_supp_v1" / f"Figure_{n}" / f"Figure_{n}_v1.pdf"
        doc = pymupdf.open(pdf)
        assert len(doc) == npages, (n, len(doc))
        fonts = qm.run(["pdffonts", str(pdf)]).strip().splitlines()[2:]
        images = qm.run(["pdfimages", "-list", str(pdf)]).strip().splitlines()[2:]
        pages = []
        for i, page in enumerate(doc):
            sp = qm.text_spans(page)
            W, H = page.rect.width, page.rect.height
            edge = [s["text"] for s in sp if min(s["bbox_mm"][0], s["bbox_mm"][1], W * MM - s["bbox_mm"][2],
                                                  H * MM - s["bbox_mm"][3]) < 0.3]
            allov = qm.overlaps(sp)
            sub = [o for o in allov if any(f(o["a"], o["b"]) for f in SUBSCRIPT)]
            ov = [o for o in allov if o not in sub]
            tif = tif_of(n, i + 1)
            im = Image.open(tif)
            dpi = float(im.info["dpi"][0])
            with tempfile.TemporaryDirectory() as d:
                subprocess.run(["pdftoppm", "-r", str(round(dpi)), "-f", str(i + 1), "-l", str(i + 1), "-tiff",
                                "-tiffcompression", "lzw", "-singlefile", str(pdf), f"{d}/r"], check=True)
                same = np.array_equal(np.asarray(Image.open(f"{d}/r.tif")), np.asarray(im))
            pg = dict(page=i + 1, page_mm=[round(W * MM, 2), round(H * MM, 2)],
                      text_sizes_pt=sorted({s["size"] for s in sp}), min_text_pt=min(s["size"] for s in sp),
                      fonts=sorted({s["font"] for s in sp}), n_spans=len(sp), overlaps=ov, subscript_pairs=len(sub),
                      edge_below_0p3mm=edge,
                      tif=dict(file=str(tif.relative_to(ROOT)), px=list(im.size), dpi=dpi,
                               mm=[round(im.size[0] / dpi * 25.4, 2), round(im.size[1] / dpi * 25.4, 2)],
                               identical_to_pdf_page=same))
            ok &= not ov and not edge and same and set(pg["fonts"]) <= {"ArialMT", "Arial-BoldMT"}
            pages.append(pg)
        rep[f"Figure_{n}"] = dict(pdf=str(pdf.relative_to(ROOT)), pages=len(pages), pdffonts=fonts,
                                  raster_objects=len(images), page_sizes_mm=sorted({tuple(p["page_mm"]) for p in pages}),
                                  min_text_pt=min(p["min_text_pt"] for p in pages),
                                  text_sizes_pt=sorted({s for p in pages for s in p["text_sizes_pt"]}),
                                  overlaps=sum(len(p["overlaps"]) for p in pages),
                                  subscript_pairs=sum(p["subscript_pairs"] for p in pages),
                                  edge_issues=sum(len(p["edge_below_0p3mm"]) for p in pages),
                                  tif_dpi=sorted({p["tif"]["dpi"] for p in pages}),
                                  tif_identical_pages=sum(p["tif"]["identical_to_pdf_page"] for p in pages),
                                  per_page=pages)
        ok &= not images and all(("Arial" in f and " yes " in f) for f in fonts)
        r = rep[f"Figure_{n}"]
        print(f"Figure_{n}: {r['pages']} pages {r['page_sizes_mm']} mm; fonts {sorted({f.split()[0] for f in fonts})}; "
              f"text {r['text_sizes_pt']} (min {r['min_text_pt']}); overlaps {r['overlaps']}; edge {r['edge_issues']}; "
              f"raster {r['raster_objects']}; TIF {r['tif_dpi']} dpi, identical {r['tif_identical_pages']}/{r['pages']}")
    (ROOT / "qa" / "measure_supp_v6.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    print("MEASURE-SUPP", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
