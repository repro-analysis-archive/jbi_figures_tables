#!/usr/bin/env python3
"""QA of supplementary/Supplementary_Material_v1.docx (supplement v6 §6): opens with python-docx and converts with
LibreOffice (PDF without image downsampling: page count, fonts Arial only); Word rules (every paragraph, also in table
cells, in Normal style; no automatic numbering; no Heading style); order of the items (Supplementary Methods SM 1–7,
then Tables S1–S6, then Figures S1–S6; every caption number exactly once as a caption); images (64: 10 / 24 / 24 / 1 /
4 / 1 between the figure captions; widths 190 mm for the heatmap pages and the figure width for S4–S6); no character
that Arial lacks; and the Supplementary Methods text equal to the draft after the recorded conversion (Markdown markup
removed, the renumbering and Arial-safe rules of build_supplementary_material_v1.py applied). Writes
qa/supplementary_docx_v1.json.

    .venv/bin/python -I scripts/qa_supplementary_docx_v1.py
"""
import sys

sys.dont_write_bytecode = True

import importlib.util  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
from pathlib import Path  # noqa: E402

from docx import Document  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("bsm", HERE / "build_supplementary_material_v1.py")
bsm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bsm)
ROOT = HERE.parent
DOCX = ROOT / "supplementary" / "Supplementary_Material_v1.docx"
PDF = DOCX.with_suffix(".pdf")
EXPORT = 'pdf:writer_pdf_Export:{"ReduceImageResolution":{"type":"boolean","value":"false"}}'


def norm(s):
    return " ".join(s.split())


def source_text():
    md = re.sub(r"<!--.*?-->\n?", "", bsm.DRAFT[0].read_text(encoding="utf-8"), flags=re.S)
    for a, b in bsm.REPLACE:
        md = md.replace(a, b)
    out = []
    for ln in md.splitlines():
        s = ln.strip()
        if not s or re.fullmatch(r"\|[-:| ]+\|", s):
            continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
        else:
            s = re.sub(r"^#+ ", "", s).replace(" — draft v2", "")
            s = re.sub(r"^\* ", "", s)
            cells = [s]
        for c in cells:
            c = bsm.arial_safe(c)
            c = re.sub(r"\*\*(.+?)\*\*", r"\1", c)
            c = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"\1", c)
            parts = re.split(r"(`[^`]+`)", c)         # code spans stay verbatim (no sub/superscript rules)
            c = "".join(x[1:-1] if x.startswith("`") else bsm.IDENT.sub(r"\1\2", x.translate(bsm.SUP).translate(bsm.SUB))
                        for x in parts)
            out.append(c)
    return norm(" ".join(out))


def body_items(doc):
    """Body paragraphs and tables in order: ('p', paragraph) or ('t', table)."""
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    for el in doc.element.body:
        if el.tag == qn("w:p"):
            yield "p", Paragraph(el, doc)
        elif el.tag == qn("w:tbl"):
            yield "t", Table(el, doc)


def main():
    rep, ok = {}, True
    doc = Document(DOCX)
    subprocess.run(["soffice", "--headless", "--convert-to", EXPORT, "--outdir", str(DOCX.parent), str(DOCX)],
                   capture_output=True, check=True)
    info = subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True).stdout
    fonts = subprocess.run(["pdffonts", str(PDF)], capture_output=True, text=True).stdout.strip().splitlines()[2:]
    imgs = [ln.split() for ln in subprocess.run(["pdfimages", "-list", str(PDF)], capture_output=True,
                                                 text=True).stdout.strip().splitlines()[2:]]
    rep["pdf"] = dict(pages=int(re.search(r"Pages:\s+(\d+)", info).group(1)),
                      fonts=sorted({f.split()[0].split("+")[-1] for f in fonts}),
                      images=sum(1 for x in imgs if x[2] == "image"),
                      image_px=sorted({(int(x[3]), int(x[4])) for x in imgs if x[2] == "image"}))
    ok &= set(rep["pdf"]["fonts"]) <= {"ArialMT", "Arial-BoldMT", "Arial-ItalicMT", "Arial-BoldItalicMT"}
    # ---- Word rules
    allp = list(doc.paragraphs) + [p for t in doc.tables for r in t.rows for c in r.cells for p in c.paragraphs]
    styles = sorted({p.style.name for p in allp})
    numbered = sum(1 for p in allp if p._p.find(qn("w:pPr")) is not None and p._p.pPr.find(qn("w:numPr")) is not None)
    rep["word"] = dict(paragraph_styles=styles, numbered_paragraphs=numbered, sections=len(doc.sections),
                       author=doc.core_properties.author, last_modified_by=doc.core_properties.last_modified_by)
    ok &= styles == ["Normal"] and numbered == 0 and not doc.core_properties.author
    # ---- order of items, captions once, images per figure
    seq, pics, cur, methods_txt, in_methods = [], {}, None, [], True
    for kind, it in body_items(doc):
        if kind == "p":
            txt = it.text
            m = re.match(r"^((?:Table|Figure) S\d)\.", txt)
            first_bold = bool(it.runs) and it.runs[0].bold
            if m and first_bold:
                seq.append(m.group(1)); cur = m.group(1); in_methods = False
            elif re.match(r"^(SM \d\.|Supplementary Methods|Supplementary Material|Provenance$|X1 / X2$|B$)", txt) \
                    and first_bold and in_methods:
                seq.append(txt.split(".")[0] if txt.startswith("SM ") else txt)
            n = len(it._p.findall(".//" + qn("w:drawing")))
            if n:
                ext = it._p.find(".//" + qn("wp:extent"))
                pics.setdefault(cur, []).append(round(int(ext.get("cx")) / 36000, 2))
            if in_methods and txt.strip() and txt != "Supplementary Material":
                methods_txt.append(re.sub(r"^[•–·]\t|^(\d+\.)\t", lambda q: (q.group(1) + " ") if q.group(1) else "", txt))
        elif in_methods:
            for r in it.rows:
                for c in r.cells:
                    methods_txt.append(c.text)
    want = (["Supplementary Material", "Supplementary Methods (SM 1–7)"] + [f"SM {n}" for n in range(1, 6)] +
            ["SM 6", "X1 / X2", "B", "SM 7"])
    want_full = ["Supplementary Material", "Supplementary Methods (SM 1–7)", "SM 1", "Provenance", "SM 2", "SM 3",
                 "SM 4", "SM 5", "SM 6", "X1 / X2", "B", "SM 7"] + [f"Table S{n}" for n in range(1, 7)] + \
                [f"Figure S{n}" for n in range(1, 7)]
    rep["order"] = seq
    rep["order_ok"] = seq == want_full
    caps = [s for s in seq if s.startswith(("Table S", "Figure S"))]
    rep["captions_once"] = all(caps.count(c) == 1 for c in want_full[-12:]) and len(caps) == 12
    rep["images_per_figure"] = {k: len(v) for k, v in pics.items()}
    rep["image_widths_mm"] = {k: sorted(set(v)) for k, v in pics.items()}
    exp_n = {"Figure S1": 10, "Figure S2": 24, "Figure S3": 24, "Figure S4": 1, "Figure S5": 4, "Figure S6": 1}
    rep["images_ok"] = rep["images_per_figure"] == exp_n and all(
        set(v) == ({190.0} if k in ("Figure S1", "Figure S2", "Figure S3") else {189.82}) for k, v in pics.items())
    ok &= rep["order_ok"] and rep["captions_once"] and rep["images_ok"] and rep["pdf"]["images"] == 64
    del want
    # ---- text: Arial-safe, methods equal to the converted draft
    full = "\n".join(p.text for p in allp)
    rep["arial_missing_chars_in_docx"] = sorted({c for c in full if c in "∈⌈⌉⌊⌋⁴⁷⁻₀"})
    src = source_text()
    got = norm(" ".join(methods_txt))
    rep["methods_text_equal"] = src == got
    if not rep["methods_text_equal"]:
        i = next((k for k in range(min(len(src), len(got))) if src[k] != got[k]), min(len(src), len(got)))
        rep["methods_first_difference"] = dict(source=src[max(0, i - 60):i + 60], docx=got[max(0, i - 60):i + 60])
    rep["methods_chars"] = len(got)
    raw = re.sub(r"<!--.*?-->", "", bsm.DRAFT[0].read_text(encoding="utf-8"), flags=re.S)   # comment not rendered
    rep["placeholders"] = {"[REF:": [raw.count("[REF:"), full.count("[REF:")],
                           "[TO FILL": [raw.count("[TO FILL"), full.count("[TO FILL")]}
    ok &= not rep["arial_missing_chars_in_docx"] and rep["methods_text_equal"] and \
        all(a == b for a, b in rep["placeholders"].values())
    rep["result"] = "PASS" if ok else "FAIL"
    (ROOT / "qa" / "supplementary_docx_v1.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in rep.items() if k not in ("order",)}, ensure_ascii=False, indent=1)[:2500])
    print("order:", rep["order"])
    print("SUPPLEMENTARY-DOCX", rep["result"])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
