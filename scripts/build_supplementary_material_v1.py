#!/usr/bin/env python3
"""Supplementary_Material_v1.docx (task CC_TASK_JBI_supplement_v6.md §5): one Word document with, in order, the
Supplementary Methods (inputs/JBI_Supplementary_Methods_draft_v2.md, converted), Tables S1–S6 with their captions and
footnotes (the body of tables/Table_Sn_v1.docx copied element by element, each in its own section with the source
orientation and margins) and Figures S1–S6 with their captions (CAPTIONS_supplement_v1.md).

Word rules (manuscript template): Normal style only (bold headings, no Heading / list styles, no automatic numbering),
Arial, 11 pt, line spacing 1.5 for prose (tables keep the table template's single spacing), left aligned, 2.5-cm
margins for text and tables, continuous page numbers in the footer. Figure sections have 10-mm margins so that the
figures are pasted at 100% (Figures S4–S6, 189.8 mm wide; 600-dpi TIF rasterised from the vector PDF by poppler) and
the A4 heatmap pages of Figures S1–S3 at the page width (190 mm; the 600-dpi page TIFs, embedded as lossless PNG with
identical pixels — grayscale when every pixel is gray — to keep the document size practical).

Conversion of the draft (recorded in POST_RESULT_PRESENTATION_JBI.md §9; checked by qa_supplementary_docx_v1.py):
  * the HTML comment (editorial note for the auditor) is not rendered, as in Markdown; the title's " — draft v2" is
    dropped; Markdown markup is rendered (bold, italic, code as plain Arial, bullets as "•" / "–" / "·" with hanging
    indents, numbered items as literal numbers, pipe tables as Word tables with the table rules);
  * characters that Arial lacks are written with Arial: "∈" -> "in", ⌈x⌉ -> ceil(x), ⌊x⌋ -> floor(x), Unicode
    superscript / subscript digits and minus -> Word superscript / subscript runs; identifiers written x_y in the draft
    (S_t, T_i, s_i, O_i, w_i, n_i, duration_i, D_j, ε_Y, φ_A, bias_X, bias_step-6) -> base + subscript run;
  * supplementary item names of the draft -> the final v6 numbers (REPLACE below); everything else verbatim.

    .venv/bin/python -I scripts/build_supplementary_material_v1.py
"""
import sys

sys.dont_write_bytecode = True

import copy  # noqa: E402
import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402
import tempfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.section import WD_ORIENT, WD_SECTION  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Mm, Pt  # noqa: E402
from PIL import Image  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build_tables", HERE / "build_tables.py")
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
Image.MAX_IMAGE_PIXELS = None
ROOT = HERE.parent
DRAFT = (ROOT / "inputs" / "JBI_Supplementary_Methods_draft_v2.md",
         "7d0e1f7b776bfd1a616bf152f6b4b6226ec56f4162ba4975a27ef53f077a1843")
OUTDIR = ROOT / "supplementary"
FONT, SIZE = "Arial", Pt(11)
POPPLER = "/opt/homebrew/bin/pdftoppm"
REPLACE = [   # draft names of supplementary items -> final v6 numbering (CAPTIONS_supplement_v1.md)
    ("Supplementary Figure S4 / Table S4 (mask check) and the exploratory Tables X, X-E3, B, B-sens and Figures X, B",
     "Supplementary Figure S4 / Table S1 (mask check) and the exploratory Tables S3, S4, S5, S6 and Figures S5, S6"),
    ("(Supplementary Figure S4, Table S4)", "(Supplementary Figure S4, Table S1)"),
    ("Supplementary Figure S4 and Table S4", "Supplementary Figure S4 and Table S1"),
    ("Tables X and X-E3 and Supplementary Figure X", "Supplementary Tables S3 and S4 and Supplementary Figure S5"),
    ("Tables B and B-sens and Supplementary Figure B", "Supplementary Tables S5 and S6 and Supplementary Figure S6"),
]
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789−")
SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")
IDENT = re.compile(r"(?<![\w`/.\-])(duration|bias|[A-Za-zα-ωΑ-Ω])_(step-6|[A-Za-z0-9]+)(?![\w])")
TOKEN = re.compile(r"(\*\*.+?\*\*|`[^`]+`|(?<![\w*])\*[^*\s][^*]*?\*(?![\w*]))")


# ------------------------------------------------------------------------------------------------ text handling
def arial_safe(s):
    s = re.sub(r"⌈([^⌉]*)⌉", r"ceil(\1)", s)
    s = re.sub(r"⌊([^⌋]*)⌋", r"floor(\1)", s)
    return s.replace(" ∈ ", " in ")


def runs(par, text, bold=False, italic=False):
    """Inline Markdown (bold, italic, code) and the Arial-safe sub/superscript rules, as Arial 11-pt runs."""
    for tok in TOKEN.split(text):
        if not tok:
            continue
        b, i, code = bold, italic, False
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            tok, b = tok[2:-2], True
            if TOKEN.search(tok):
                runs(par, tok, True, italic)
                continue
        elif tok.startswith("`") and tok.endswith("`") and len(tok) > 1:
            tok, code = tok[1:-1], True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            tok, i = tok[1:-1], True
        pieces = [(tok, None)] if code else script_pieces(tok)
        for txt, kind in pieces:
            r = par.add_run(txt)
            r.bold, r.italic = b, i
            r.font.name, r.font.size = FONT, SIZE
            if kind == "sup":
                r.font.superscript = True
            elif kind == "sub":
                r.font.subscript = True


def script_pieces(s):
    """Split a text segment into (text, None|'sup'|'sub') pieces: Unicode super/subscripts and x_y identifiers."""
    out = []
    pos = 0
    pat = re.compile(r"([⁰¹²³⁴⁵⁶⁷⁸⁹⁻]+)|([₀₁₂₃₄₅₆₇₈₉]+)|" + IDENT.pattern)
    for m in pat.finditer(s):
        if m.start() > pos:
            out.append((s[pos:m.start()], None))
        if m.group(1):
            out.append((m.group(1).translate(SUP), "sup"))
        elif m.group(2):
            out.append((m.group(2).translate(SUB), "sub"))
        else:
            out.append((m.group(3), None))
            out.append((m.group(4), "sub"))
        pos = m.end()
    if pos < len(s):
        out.append((s[pos:], None))
    return out


def para(doc, text="", bold=False, italic=False, left_mm=0.0, hang_mm=0.0, before=0, after=0, spacing=1.5,
         keep_next=False):
    p = doc.add_paragraph()
    f = p.paragraph_format
    f.left_indent, f.first_line_indent = Mm(left_mm), Mm(-hang_mm)
    f.space_before, f.space_after, f.line_spacing = Pt(before), Pt(after), spacing
    f.keep_with_next = keep_next
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if text:
        runs(p, text, bold, italic)
    return p


def md_table(doc, lines, width_mm):
    cells = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines]
    hdr, sep, body = cells[0], cells[1], cells[2:]
    align = ["r" if s.endswith(":") and not s.startswith(":") else "l" for s in sep]
    n = len(hdr)
    lens = [max(len(re.sub(r"[`*]", "", r[j])) for r in [hdr] + body) for j in range(n)]
    w = [max(14.0, width_mm * L / sum(lens)) for L in lens]
    w = [x * width_mm / sum(w) for x in w]
    t = doc.add_table(rows=1 + len(body), cols=n)
    t.autofit = False
    bt.no_table_borders(t)
    for j, x in enumerate(w):
        t.columns[j].width = Mm(x)
    for i, vals in enumerate([hdr] + body):
        row = t.rows[i]
        bt.cant_split(row)
        if i == 0:
            bt.repeat_header(row)
        for j, v in enumerate(vals):
            c = row.cells[j]
            c.width = Mm(w[j])
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            runs(p, arial_safe(v), bold=(i == 0))
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if align[j] == "r" else WD_ALIGN_PARAGRAPH.LEFT
    for c in t.rows[0].cells:
        bt.set_border(c, "top"); bt.set_border(c, "bottom")
    for c in t.rows[-1].cells:
        bt.set_border(c, "bottom")
    para(doc, spacing=1.0)          # space after the table


# ------------------------------------------------------------------------------------------------ methods
def methods(doc, md, log):
    md = re.sub(r"<!--.*?-->\n?", "", md, flags=re.S)
    for a, b in REPLACE:
        k = md.count(a)
        assert k == 1, (a, k)
        md = md.replace(a, b)
        log.append(f"renumbered: '{a}' -> '{b}'")
    lines = md.splitlines()
    i = 0
    width = 160.0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("|"):
            block = []
            while i < len(lines) and lines[i].startswith("|"):
                block.append(lines[i]); i += 1
            md_table(doc, block, width)
            continue
        m = re.match(r"^(#+) (.*)$", ln)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            if lvl == 1:
                txt = txt.replace(" — draft v2", "")
            para(doc, arial_safe(txt), bold=True, before=0 if lvl == 1 else 12, after=6, keep_next=True)
            i += 1
            continue
        ind = len(ln) - len(ln.lstrip(" "))
        s = ln.strip()
        lvl = ind // 2
        mb = re.match(r"^\* (.*)$", s)
        mn = re.match(r"^(\d+)\. (.*)$", s)
        if mb:
            sym = "•–·"[min(lvl, 2)]
            para(doc, f"{sym}\t" + arial_safe(mb.group(1)), left_mm=6 + 6 * lvl, hang_mm=4.5)
        elif mn:
            para(doc, f"{mn.group(1)}.\t" + arial_safe(mn.group(2)), left_mm=6 + 6 * lvl, hang_mm=5.5)
        else:
            para(doc, arial_safe(s), left_mm=6 * lvl)
        i += 1


# ------------------------------------------------------------------------------------------------ sections
def new_section(doc, landscape, margins_mm):
    sec = doc.add_section(WD_SECTION.NEW_PAGE)
    sec.orientation = WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
    sec.page_width, sec.page_height = (Mm(297), Mm(210)) if landscape else (Mm(210), Mm(297))
    for k, v in zip(("left_margin", "right_margin", "top_margin", "bottom_margin"), margins_mm):
        setattr(sec, k, Mm(v))
    sec.footer_distance = Mm(min(8, margins_mm[3] - 2))
    return sec


def page_number_footer(sec):
    p = sec.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    rf = OxmlElement("w:rFonts")
    for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(k), FONT)
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), "22")
    rpr.append(rf); rpr.append(sz); r.append(rpr)
    t = OxmlElement("w:t"); t.text = "1"; r.append(t)
    fld.append(r)
    p._p.append(fld)


def copy_table_doc(doc, path):
    src = Document(path)
    s = src.sections[0]
    land = s.orientation == WD_ORIENT.LANDSCAPE
    new_section(doc, land, [s.left_margin.mm, s.right_margin.mm, s.top_margin.mm, s.bottom_margin.mm])
    anchor = doc.element.body.sectPr
    n = 0
    for el in src.element.body:
        if el.tag == qn("w:sectPr"):
            continue
        anchor.addprevious(copy.deepcopy(el))
        n += 1
    return n


def caption_paragraph(doc, cap):
    m = re.match(r"\*\*(Figure S\d\.)\*\* (.*)", cap, re.S)
    p = para(doc, spacing=1.5, after=6)
    r = p.add_run(m.group(1)); r.bold = True; r.font.name, r.font.size = FONT, SIZE
    runs(p, " " + arial_safe(" ".join(m.group(2).split())))
    return p


def picture(doc, path, width_mm):
    p = para(doc, spacing=1.0)
    p.add_run().add_picture(str(path), width=Mm(width_mm))
    return p


def figure_images(n, tmp):
    """600-dpi images for the Word document: S1–S3 page TIFs as lossless PNG (pixels identical; 'L' when gray);
    S4–S6 the PDF pages rasterised by poppler at 600 dpi (TIF)."""
    d = ROOT / "figures_supp_v1" / f"Figure_S{n}"
    out = []
    if n in (1, 2, 3):
        for f in sorted((d / "pages").glob(f"Figure_S{n}_v1_p*.tif")):
            a = np.asarray(Image.open(f).convert("RGB"))
            gray = bool((a[..., 0] == a[..., 1]).all() and (a[..., 1] == a[..., 2]).all())
            png = tmp / (f.stem + ".png")
            (Image.fromarray(a[..., 0]) if gray else Image.fromarray(a)).save(png, optimize=True)
            assert np.array_equal(np.asarray(Image.open(png).convert("RGB")), a), f
            out.append((png, 190.0, "PNG L" if gray else "PNG RGB"))
    else:
        pdf = d / f"Figure_S{n}_v1.pdf"
        npages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True,
                                                                  text=True).stdout).group(1))
        for p in range(1, npages + 1):
            stem = tmp / f"Figure_S{n}_v1_600_p{p:02d}"
            subprocess.run([POPPLER, "-r", "600", "-f", str(p), "-l", str(p), "-tiff", "-tiffcompression", "lzw",
                            "-singlefile", str(pdf), str(stem)], check=True)
            im = Image.open(f"{stem}.tif")
            out.append((Path(f"{stem}.tif"), im.size[0] / im.info["dpi"][0] * 25.4, "TIF 600 dpi, 100%"))
    return out


def main():
    raw = DRAFT[0].read_bytes()
    assert hashlib.sha256(raw).hexdigest() == DRAFT[1], "draft differs from the file provided (SHA-256)"
    caps = {m.group(1): m.group(0) for m in re.finditer(r"^\*\*(Figure S\d)\.\*\* .*?(?=\n\n|\Z)",
                                                        (ROOT / "CAPTIONS_supplement_v1.md").read_text(), re.S | re.M)}
    OUTDIR.mkdir(exist_ok=True)
    doc = bt.new_document(landscape=False)
    st = doc.styles["Normal"]
    st.paragraph_format.line_spacing = 1.0
    page_number_footer(doc.sections[0])
    doc.sections[0].footer_distance = Mm(12)
    log = []
    para(doc, "Supplementary Material", bold=True, after=12)
    methods(doc, raw.decode("utf-8"), log)
    ntab = {}
    for n in range(1, 7):
        ntab[n] = copy_table_doc(doc, ROOT / "tables" / f"Table_S{n}_v1.docx")
    nimg = {}
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        for n in range(1, 7):
            new_section(doc, False, [10, 10, 10, 10])
            caption_paragraph(doc, caps[f"Figure S{n}"])
            imgs = figure_images(n, tmp)
            for path, wmm, kind in imgs:
                picture(doc, path, wmm)
            nimg[n] = (len(imgs), sorted({k for _, _, k in imgs}), sorted({round(w, 2) for _, w, _ in imgs}))
        cp = doc.core_properties
        cp.author = cp.last_modified_by = cp.comments = ""
        cp.title = "Supplementary Material"
        doc.save(OUTDIR / "Supplementary_Material_v1.docx")
    print("written supplementary/Supplementary_Material_v1.docx")
    print("  conversions:", *log, sep="\n    ")
    print("  table elements copied:", ntab)
    print("  images:", nimg)


if __name__ == "__main__":
    main()
