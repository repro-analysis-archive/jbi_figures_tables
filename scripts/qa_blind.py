#!/usr/bin/env python3
"""Metadata / blinding scan of the submission files (figure template §8-3): AI-tool traces, e-mail addresses,
user names / local paths / affiliation strings, and document metadata. Writes qa/blind_scan.json.

    .venv/bin/python -I scripts/qa_blind.py
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import re  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import pymupdf  # noqa: E402
from PIL import Image  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
ROOT = Path(__file__).resolve().parents[1]
FILES = [f"figures/Figure_1/Figure_1.{e}" for e in ("pdf", "pptx", "tif")] + \
        [f"figures/Figure_{n}/Figure_{n}.{e}" for n in (2, 3, 4) for e in ("pdf", "tif")] + \
        [f"graphical_abstract/Graphical_abstract.{e}" for e in ("pdf", "pptx", "tif")] + \
        [f"tables/Table_{n}.{e}" for n in (1, 2, 3) for e in ("docx", "csv")] + ["CAPTIONS.md"]
PAT = {"ai": re.compile(rb"claude|anthropic|openai|chatgpt|gpt-4|copilot", re.I),
       "email": re.compile(rb"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
       "user/path/affiliation": re.compile(rb"/Users/|nakanohisashi|nakano|nuhw|niigata", re.I)}


FILES_V2 = [f"figures_v2/Figure_1/Figure_1_v2.{e}" for e in ("pdf", "pptx", "tif")] + \
           [f"figures_v2/Figure_{n}/Figure_{n}_v2.{e}" for n in (2, 3, 4, 5) for e in ("pdf", "tif")] + \
           [f"graphical_abstract/Graphical_abstract_v2.{e}" for e in ("pdf", "pptx", "tif")] + \
           [f"tables/Table_{n}_v2.{e}" for n in ("1", "2", "S5") for e in ("docx", "csv")] + ["CAPTIONS_v2.md"]


FILES_V3 = [f"figures_v3/Figure_1/Figure_1_v3.{e}" for e in ("pdf", "pptx", "tif")] + \
           [f"figures_v3/Figure_{n}/Figure_{n}_v3.{e}" for n in (2, 3, 4) for e in ("pdf", "tif")] + \
           [f"tables/Table_2_v3.{e}" for e in ("docx", "csv")]


FILES_V4 = [f"figures_v4/Figure_1/Figure_1_v4.{e}" for e in ("pdf", "pptx", "tif")] + \
           [f"figures_v4/Figure_{n}/Figure_{n}_v4.{e}" for n in (2, 3, 4, 5, 6) for e in ("pdf", "tif")] + \
           ["CAPTIONS_v4.md"]


def main():
    v2 = "--v2" in sys.argv[1:]
    v4 = "--v4" in sys.argv[1:]
    v3 = "--v3" in sys.argv[1:] or v4          # v4 uses the v3 TIF scan (pixel strips excluded)
    out, ok = {}, True
    for f in (FILES_V4 if v4 else FILES_V3 if v3 else FILES_V2 if v2 else FILES):
        p = ROOT / f
        blobs = [p.read_bytes()]
        meta = {}
        if p.suffix in (".docx", ".pptx"):
            z = zipfile.ZipFile(p)
            blobs = [z.read(n) for n in z.namelist()]
            core = z.read("docProps/core.xml").decode()
            for t in ("dc:creator", "cp:lastModifiedBy", "dc:title"):
                m = re.search(rf"<{t}>(.*?)</{t}>", core)
                meta[t] = m.group(1) if m else ""
        elif p.suffix == ".pdf":
            meta = {k: v for k, v in pymupdf.open(p).metadata.items() if v and k in ("author", "creator", "producer", "title")}
        elif p.suffix == ".tif":
            im = Image.open(p)
            meta = {str(k): str(v)[:40] for k, v in im.tag_v2.items() if k in (270, 305, 315, 33432)}
            if v3:   # scan every byte except the compressed pixel strips (random LZW bytes matched the e-mail pattern)
                raw = bytearray(blobs[0])
                for off, n in zip(im.tag_v2[273], im.tag_v2[279]):
                    raw[off:off + n] = bytes(n)
                blobs = [bytes(raw)]
                meta["scanned"] = "all bytes except pixel strips"
        hits = {k: sum(len(r.findall(b)) for b in blobs) for k, r in PAT.items()}
        ok &= not any(hits.values()) and not meta.get("author") and not meta.get("dc:creator") and not meta.get("cp:lastModifiedBy")
        out[f] = dict(hits=hits, metadata=meta)
        print(f, hits, meta)
    (ROOT / "qa" / ("blind_scan_v4.json" if v4 else "blind_scan_v3.json" if v3 else "blind_scan_v2.json" if v2 else
                    "blind_scan.json")).write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print("BLIND", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
