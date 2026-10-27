#!/usr/bin/env python3
"""Marker sizes of the new Figure 5 (v5 revision), measured from the vector PDF with the method of qa_markers_v4.py
(outer size = stroke-path bbox + stroke width; grouped by path signature, face, edge colour and width). Writes
qa/markers_v5.json.

    .venv/bin/python -I scripts/qa_markers_v5.py
"""
import sys

sys.dont_write_bytecode = True

import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("qa_markers_v4", HERE / "qa_markers_v4.py")
m4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m4)
m4.FACE.update({(0.42, 0.42, 0.42): "#6B6B6B filled", (0.54, 0.54, 0.54): "#8A8A8A filled",
                (0.3, 0.3, 0.3): "#4D4D4D filled"})
ROOT = HERE.parent


NAMES = {"other:llllllllll": "pentagram", "other:llllllllllll": "hexagram"}


def main():
    pdf = "figures_v4/Figure_5/Figure_5_v4.pdf"
    agg = {}
    for m in m4.measure(pdf):     # faces are not used: with overlapping markers the face match is ambiguous
        k = (NAMES.get(m["shape"], m["shape"]), m["edge_colour"], m["edge_pt"])
        a = agg.setdefault(k, dict(shape=k[0], edge_colour=k[1], edge_pt=k[2], n=0, outer_w_mm=m["outer_w_mm"],
                                   outer_h_mm=m["outer_h_mm"]))
        assert (a["outer_w_mm"], a["outer_h_mm"]) == (m["outer_w_mm"], m["outer_h_mm"]), (k, a, m)
        a["n"] += m["n"]
    ms = sorted(agg.values(), key=lambda a: (a["edge_pt"], a["shape"], a["edge_colour"]))
    for m in ms:
        kind = "filled (edge 0.5 pt #1A1A1A)" if m["edge_pt"] == 0.5 else "open (edge 0.8 pt, group colour)"
        m["kind"] = kind
        print(f"  {m['shape']:10s} {kind:34s} edge {m['edge_colour']}  n {m['n']:3d}  {m['outer_w_mm']} x {m['outer_h_mm']} mm")
    (ROOT / "qa" / "markers_v5.json").write_text(json.dumps(dict(pdf=pdf, markers=ms), indent=1) + "\n")


if __name__ == "__main__":
    main()
