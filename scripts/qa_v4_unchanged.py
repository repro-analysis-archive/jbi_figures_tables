#!/usr/bin/env python3
"""v4 "do not change" check (task v4 §2): the v3-suffixed outputs differ from the v2-suffixed ones only by the three
items of task v4 §1. From the exported files:
  * Figures 2 and 4 — PDF text spans (text, font, size, position) identical; every non-marker vector path identical;
    marker paths (stroke + face, including the 'llll' white faces of squares / diamonds): same number, same x centres,
    y centres within 0.1 mm (a triangle grows about its anchor, so its box centre moves by 0.06 mm), only larger.
  * Figure 3 — PDF text spans identical in text, font and size; same number of non-marker paths of each kind; marker
    paths: same number, only larger; vertical geometry reported (row height is the v4 change).
  * Figure 1 — PPTX: same shapes and text runs in the same order, same text, font sizes, bold, colours, x positions,
    widths and heights; only y positions differ (vertical spacing is the v4 change), apart from the lengths of the
    vertical connector lines that join boxes whose spacing changed (listed).
Writes qa/v4_unchanged.json.

    .venv/bin/python -I scripts/qa_v4_unchanged.py
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import re  # noqa: E402
import zipfile  # noqa: E402
from collections import Counter  # noqa: E402
from pathlib import Path  # noqa: E402

import pymupdf  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
MM = 25.4 / 72


def is_marker(d):
    r = d["rect"]
    return 0.3 <= r.width * MM <= 3.0 and 0.3 <= r.height * MM <= 3.0 and "".join(i[0] for i in d["items"]) in (
        "cccc", "qu", "lll", "llll")


def pdf_parts(p):
    page = pymupdf.open(ROOT / p)[0]
    spans = []
    for b in page.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for s in ln["spans"]:
                spans.append((s["text"], s["font"], round(s["size"], 2), tuple(round(v * MM, 2) for v in s["bbox"])))
    other, marks = [], []
    for d in page.get_drawings():
        sig = (d.get("type"), str(d.get("fill")), str(d.get("color")), round(d.get("width") or 0, 3),
               "".join(i[0] for i in d["items"]))
        r = d["rect"]
        if is_marker(d):
            marks.append((sig, round((r.x0 + r.x1) / 2 * MM, 2), round((r.y0 + r.y1) / 2 * MM, 2),
                          round(r.width * MM, 3), round(r.height * MM, 3)))
        else:
            other.append(sig + (tuple(round(v * MM, 2) for v in r),))
    return spans, other, marks, (round(page.rect.width * MM, 2), round(page.rect.height * MM, 2))


def fig_check(n, same_geometry):
    s2, o2, m2, pg2 = pdf_parts(f"figures_v2/Figure_{n}/Figure_{n}_v2.pdf")
    s3, o3, m3, pg3 = pdf_parts(f"figures_v3/Figure_{n}/Figure_{n}_v3.pdf")
    res = dict(page_v2_mm=pg2, page_v3_mm=pg3, spans=len(s3), non_marker_paths=len(o3), marker_paths=len(m3))
    res["text_font_size_identical"] = sorted(x[:3] for x in s2) == sorted(x[:3] for x in s3)
    res["marker_count_identical"] = Counter(x[0] for x in m2) == Counter(x[0] for x in m3)
    k2 = sorted(m2, key=lambda x: (x[0], x[1], x[2])); k3 = sorted(m3, key=lambda x: (x[0], x[1], x[2]))
    res["markers_only_larger"] = all(b[3] > a[3] and b[4] > a[4] for a, b in zip(k2, k3)) and len(k2) == len(k3)
    if same_geometry:
        res["text_positions_identical"] = s2 == s3
        res["non_marker_paths_identical"] = o2 == o3
        res["marker_centres_identical"] = all(abs(a[1] - b[1]) <= 0.01 and abs(a[2] - b[2]) <= 0.1 for a, b in zip(k2, k3))
        res["marker_centre_max_shift_mm"] = [max(abs(a[1] - b[1]) for a, b in zip(k2, k3)),
                                             max(abs(a[2] - b[2]) for a, b in zip(k2, k3))]
        res["result"] = "PASS" if all(res[k] for k in ("text_font_size_identical", "marker_count_identical",
                                                         "markers_only_larger", "text_positions_identical",
                                                         "non_marker_paths_identical", "marker_centres_identical")) and \
            pg2 == pg3 else "FAIL"
    else:
        res["non_marker_path_kinds_identical"] = Counter(x[:5] for x in o2) == Counter(x[:5] for x in o3)
        res["result"] = "PASS" if all(res[k] for k in ("text_font_size_identical", "marker_count_identical",
                                                         "markers_only_larger", "non_marker_path_kinds_identical")) \
            else "FAIL"
    return res


def pptx_parts(p):
    xml = zipfile.ZipFile(ROOT / p).read("ppt/slides/slide1.xml").decode()
    shapes = re.findall(r"<p:(?:sp|cxnSp)>.*?</p:(?:sp|cxnSp)>", xml, re.S)
    out = []
    for s in shapes:
        off = re.search(r'<a:off x="(-?\d+)" y="(-?\d+)"/><a:ext cx="(\d+)" cy="(\d+)"/>', s)
        runs = re.findall(r'<a:rPr[^>]*?sz="(\d+)"[^>]*?(?:b="(\d)")?[^>]*>.*?<a:t>(.*?)</a:t>', s, re.S)
        cols = re.findall(r'srgbClr val="([0-9A-F]{6})"', s)
        geom = re.findall(r'prstGeom prst="(\w+)"', s)
        out.append(dict(x=int(off.group(1)), y=int(off.group(2)), cx=int(off.group(3)), cy=int(off.group(4)),
                        runs=runs, colours=cols, geom=geom))
    return out


def fig1_check():
    a, b = pptx_parts("figures_v2/Figure_1/Figure_1_v2.pptx"), pptx_parts("figures_v3/Figure_1/Figure_1_v3.pptx")
    same = len(a) == len(b)
    diffs, connectors = Counter(), []
    for i, (u, v) in enumerate(zip(a, b)):
        for k in ("x", "cx", "runs", "colours", "geom"):
            if u[k] != v[k]:
                diffs[k] += 1
        if u["cy"] != v["cy"]:
            if u["geom"] == ["line"] and u["cx"] == 0 == v["cx"]:
                connectors.append(dict(shape=i, x_mm=round(u["x"] / 36000, 2), length_v2_mm=round(u["cy"] / 36000, 2),
                                       length_v3_mm=round(v["cy"] / 36000, 2)))
            else:
                diffs["cy"] += 1
        if u["y"] != v["y"]:
            diffs["y"] += 1
    sizes = sorted({int(r[0]) / 100 for s in b for r in s["runs"]})
    texts_same = [r[2] for s in a for r in s["runs"]] == [r[2] for s in b for r in s["runs"]]
    res = dict(shapes_v2=len(a), shapes_v3=len(b), property_differences=dict(diffs), run_sizes_pt=sizes,
               texts_identical=texts_same, vertical_connectors_resized=connectors)
    res["result"] = "PASS" if same and texts_same and set(diffs) <= {"y"} else "FAIL"
    return res


def main():
    rep = {"Figure_1": fig1_check(), "Figure_2": fig_check(2, True), "Figure_3": fig_check(3, False),
           "Figure_4": fig_check(4, True)}
    for k, v in rep.items():
        print(k, v)
    (ROOT / "qa" / "v4_unchanged.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    ok = all(v["result"] == "PASS" for v in rep.values())
    print("V4-UNCHANGED", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
