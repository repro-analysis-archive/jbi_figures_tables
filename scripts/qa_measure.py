#!/usr/bin/env python3
"""Measure exported figures (template §7): page/TIF size, fonts, text sizes and colours, marker sizes, text overlaps,
edge clearance, rasterization. Writes qa/measure_<stem>.json and prints a short summary.

    .venv/bin/python -I scripts/qa_measure.py figures/Figure_2/Figure_2.pdf [--tif figures/Figure_2/Figure_2.tif]
"""
import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import json  # noqa: E402
import subprocess  # noqa: E402
from collections import defaultdict  # noqa: E402
from pathlib import Path  # noqa: E402

import pymupdf  # noqa: E402
from PIL import Image  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
MM = 25.4 / 72
ROOT = Path(__file__).resolve().parents[1]


def hexcol(c):
    if c is None:
        return None
    if isinstance(c, int):
        return f"#{c:06X}"
    return "#" + "".join(f"{round(v * 255):02X}" for v in c[:3])


def text_spans(page):
    spans = []
    d = page.get_text("rawdict", flags=pymupdf.TEXT_ACCURATE_BBOXES)
    for b in d["blocks"]:
        for ln in b.get("lines", []):
            for s in ln["spans"]:
                chars = s.get("chars", [])
                txt = "".join(c["c"] for c in chars)
                if not txt.strip():
                    continue
                xs = [c["bbox"] for c in chars if c["c"].strip()]
                x0 = min(b_[0] for b_ in xs); y0 = min(b_[1] for b_ in xs)
                x1 = max(b_[2] for b_ in xs); y1 = max(b_[3] for b_ in xs)
                spans.append(dict(text=txt, font=s["font"], size=round(s["size"], 2), color=hexcol(s["color"]),
                                  bbox_mm=[round(v * MM, 2) for v in (x0, y0, x1, y1)],
                                  dir=[round(v, 3) for v in ln["dir"]]))
    return spans


def overlaps(spans, tol=0.05):
    out = []
    for i in range(len(spans)):
        for j in range(i + 1, len(spans)):
            a, b = spans[i]["bbox_mm"], spans[j]["bbox_mm"]
            w = min(a[2], b[2]) - max(a[0], b[0])
            h = min(a[3], b[3]) - max(a[1], b[1])
            if w > tol and h > tol:
                out.append(dict(a=spans[i]["text"], b=spans[j]["text"], overlap_mm=[round(w, 2), round(h, 2)]))
    return out


def shape_of(d):
    kinds = [it[0] for it in d["items"]]
    if "c" in kinds:
        return "circle"
    if kinds == ["re"] or (kinds.count("l") == 4 and abs(d["rect"].width - d["rect"].height) < 0.05 and
                            _axis_aligned(d)):
        return "square"
    if kinds.count("l") == 3 or kinds.count("l") == 2:
        return "triangle"
    if kinds.count("l") == 4:
        return "diamond"
    return "other"


def _axis_aligned(d):
    for it in d["items"]:
        if it[0] == "l":
            p, q = it[1], it[2]
            if abs(p.x - q.x) > 0.01 and abs(p.y - q.y) > 0.01:
                return False
    return True


def markers(page):
    """Small closed paths (0.4–3 mm). MATLAB writes a marker's face (fill) and edge (stroke) as separate paths, so the
    outer size of a marker = edge-path bbox + edge line width (half on each side). Grouped by shape and colours."""
    g = defaultdict(list)
    for d in page.get_drawings():
        r = d["rect"]
        w, h = r.width * MM, r.height * MM
        if not (0.3 <= w <= 3.0 and 0.3 <= h <= 3.0):
            continue
        if d.get("type") == "s" and d.get("color") is not None:          # edge path
            lw = d.get("width") or 0.0
            key = ("edge", shape_of(d), hexcol(d.get("color")), round(lw, 2))
            g[key].append((round(w + lw * MM, 3), round(h + lw * MM, 3)))
        elif d.get("type") in ("f", "fs") and d.get("fill") is not None:
            key = ("face", shape_of(d), hexcol(d.get("fill")), 0.0)
            g[key].append((round(w, 3), round(h, 3)))
    out = []
    for (part, shp, col, lw), v in sorted(g.items()):
        ws = sorted(x[0] for x in v); hs = sorted(x[1] for x in v)
        out.append(dict(part=part, shape=shp, colour=col, edge_pt=lw, n=len(v),
                        outer_w_mm_median=ws[len(ws) // 2], outer_h_mm_median=hs[len(hs) // 2],
                        outer_w_mm_min=ws[0], outer_h_mm_min=hs[0]))
    return out


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf")
    ap.add_argument("--tif")
    a = ap.parse_args()
    pdf = Path(a.pdf)
    doc = pymupdf.open(pdf)
    page = doc[0]
    W, H = page.rect.width, page.rect.height
    spans = text_spans(page)
    sizes = sorted({s["size"] for s in spans})
    edge = []
    for s in spans:
        x0, y0, x1, y1 = s["bbox_mm"]
        m = min(x0, y0, W * MM - x1, H * MM - y1)
        if m < 0.3:
            edge.append(dict(text=s["text"], clearance_mm=round(m, 2)))
    rep = dict(
        pdf=str(pdf), pages=len(doc), page_mm=[round(W * MM, 2), round(H * MM, 2)], page_pt=[W, H],
        pdffonts=run(["pdffonts", str(pdf)]).strip().splitlines(),
        pdfimages=run(["pdfimages", "-list", str(pdf)]).strip().splitlines(),
        text_sizes_pt=sizes, min_text_pt=min(sizes) if sizes else None,
        text_colours=sorted({s["color"] for s in spans}), fonts=sorted({s["font"] for s in spans}),
        n_spans=len(spans), text_overlaps=overlaps(spans), edge_clearance_below_0p3mm=edge,
        markers=markers(page), metadata={k: v for k, v in doc.metadata.items() if v},
        bytes=pdf.stat().st_size, spans=spans)
    if a.tif:
        im = Image.open(a.tif)
        dpi = im.info.get("dpi")
        rep["tif"] = dict(path=a.tif, px=list(im.size), dpi=[float(x) for x in dpi] if dpi else None,
                          mm=[round(im.size[0] / dpi[0] * 25.4, 2), round(im.size[1] / dpi[1] * 25.4, 2)],
                          mode=im.mode, compression=im.info.get("compression"),
                          tags={k: str(v)[:80] for k, v in im.tag_v2.items() if k in (270, 305, 315, 33432)},
                          bytes=Path(a.tif).stat().st_size)
    out = ROOT / "qa" / f"measure_{pdf.stem}.json"
    out.write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    print(f"{pdf.name}: page {rep['page_mm'][0]} x {rep['page_mm'][1]} mm; fonts {rep['fonts']}; text sizes "
          f"{sizes}; min {rep['min_text_pt']} pt; colours {rep['text_colours']}; overlaps "
          f"{len(rep['text_overlaps'])}; edge<0.3mm {len(edge)}; images {max(0, len(rep['pdfimages']) - 2)}")
    for m in rep["markers"]:
        print("  marker", m)
    for o in rep["text_overlaps"]:
        print("  OVERLAP", o)
    for e in edge:
        print("  EDGE", e)
    if a.tif:
        t = rep["tif"]
        print(f"  TIF {t['px']} px @ {t['dpi']} dpi = {t['mm']} mm; {t['mode']} {t['compression']}; tags {t['tags']}")
    print("  pdffonts:", *rep["pdffonts"][2:], sep="\n    ")
    print("  metadata:", rep["metadata"])


if __name__ == "__main__":
    main()
