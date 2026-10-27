#!/usr/bin/env python3
"""Marker sizes before (v2 suffix) and after (v3 suffix) the v4 revision (task v4 §1.1, §4), measured from the vector
PDFs. MATLAB writes each marker as a fill path and a stroke path; the outer size is the stroke-path bbox + the stroke
width. Markers are grouped by their path signature (cccc circle, qu square / diamond by aspect, lll triangle), stroke
colour and width, so that the diamond is not merged with the square (it was in the v3 report's "other" median).
Writes qa/markers_v4.json.

    .venv/bin/python -I scripts/qa_markers_v4.py
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
from collections import defaultdict  # noqa: E402
from pathlib import Path  # noqa: E402

import pymupdf  # noqa: E402

MM = 25.4 / 72
ROOT = Path(__file__).resolve().parents[1]
FIGS = {n: (f"figures_v2/Figure_{n}/Figure_{n}_v2.pdf", f"figures_v3/Figure_{n}/Figure_{n}_v3.pdf") for n in (2, 3, 4)}
FIGS[5] = ("figures_v2/Figure_5/Figure_5_v2.pdf", None)          # not changed in v4 (POST_RESULT §7)
FACE = {(0.17, 0.24, 0.42): "navy filled", (1.0, 1.0, 1.0): "white (hollow)"}


def shape(sig, w, h):
    if sig == "cccc":
        return "circle"
    if sig == "lll":
        return "triangle"
    if sig == "qu":
        return "square" if abs(w - h) < 0.01 else "diamond"
    return "other:" + sig


def measure(pdf):
    page = pymupdf.open(ROOT / pdf)[0]
    faces = []
    g = defaultdict(list)
    for d in page.get_drawings():
        r = d["rect"]
        w, h = r.width * MM, r.height * MM
        if not (0.3 <= w <= 3.0 and 0.3 <= h <= 3.0):
            continue
        sig = "".join(it[0] for it in d["items"])
        if d.get("type") in ("f", "fs") and d.get("fill") is not None:
            faces.append((r, tuple(round(v, 2) for v in d["fill"])))
        if d.get("type") == "s" and d.get("color") is not None:
            lw = d.get("width") or 0.0
            ow, oh = round(w + lw * MM, 3), round(h + lw * MM, 3)
            face = next((FACE.get(c, str(c)) for fr, c in faces if fr.contains(r.tl + (r.br - r.tl) * 0.5) and
                         abs(fr.width - r.width) < 0.5), "?")
            g[(shape(sig, ow, oh), face, "#" + "".join(f"{round(v * 255):02X}" for v in d["color"]), round(lw, 2))].append(
                (ow, oh))
    out = []
    for (shp, face, col, lw), v in sorted(g.items()):
        ws = sorted(x[0] for x in v); hs = sorted(x[1] for x in v)
        out.append(dict(shape=shp, face=face, edge_colour=col, edge_pt=lw, n=len(v), outer_w_mm=ws[len(ws) // 2],
                        outer_h_mm=hs[len(hs) // 2], spread_w_mm=round(ws[-1] - ws[0], 3),
                        spread_h_mm=round(hs[-1] - hs[0], 3)))
    return out


def main():
    rep = {}
    for n, (before, after) in FIGS.items():
        b = measure(before)
        a = measure(after) if after else None
        rep[f"Figure_{n}"] = dict(before=before, after=after, markers_before=b, markers_after=a)
        print(f"Figure_{n}")
        for i, m in enumerate(b):
            line = f"  {m['shape']:8s} {m['face']:15s} edge {m['edge_pt']} pt  n {m['n']:3d}  before {m['outer_w_mm']} x {m['outer_h_mm']} mm"
            if a:
                x = a[i]
                assert (x["shape"], x["face"], x["edge_pt"], x["n"]) == (m["shape"], m["face"], m["edge_pt"], m["n"]), (x, m)
                line += f"  ->  after {x['outer_w_mm']} x {x['outer_h_mm']} mm (x{x['outer_w_mm'] / m['outer_w_mm']:.3f})"
            print(line)
    (ROOT / "qa" / "markers_v4.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
