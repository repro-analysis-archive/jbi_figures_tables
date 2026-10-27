#!/usr/bin/env python3
"""Tables 1–3 for the JBI manuscript: editable Word (.docx) + CSV of the displayed cells, from hash-guarded canonical
JSON only (table template v1; Word rules template v4; JBI: editable tables, no vertical rules or shading).

Design: Arial 11 pt throughout; caption above the table with only "Table X." in bold; header row bold and repeated on
each page; borders = top rule, header-bottom rule and bottom rule only (no vertical rules, no shading); every paragraph
in Normal style (no Heading or list styles); abbreviations and definitions in footnotes below the table.
Typographic rule: Arial has no glyph for "∈" or "⌊ ⌋", so protocol text is rendered mechanically as "X = a, b or c" and
"floor(…)". 3-decimal strings are the canonical ones (canonical/fam_dbar.json) or the same f3 rule.

    .venv/bin/python -I scripts/build_tables.py
"""
import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

from docx import Document  # noqa: E402
from docx.enum.section import WD_ORIENT  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.oxml import OxmlElement  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docx.shared import Mm, Pt, RGBColor  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "tables"
FONT = "Arial"
SIZE = Pt(11)


def canonical(name):
    p = ROOT / "canonical" / f"{name}.json"
    sums = dict(reversed(line.split()) for line in (ROOT / "canonical" / "SHA256SUMS.txt").read_text().splitlines())
    assert hashlib.sha256(p.read_bytes()).hexdigest() == sums[f"{name}.json"], f"hash guard failed: {name}"
    return json.loads(p.read_text())


def f3(x):
    return f"{x:.3f}".replace("-", "−")


def ci(e, lo="lo", hi="hi"):
    return f"({f3(e[lo])} to {f3(e[hi])})"


def typo(t):
    """Arial-safe rendering of protocol text (no ∈, no floor brackets)."""
    def setlist(m):
        vals = [v.strip() for v in m.group(2).split(",")]
        return f"{m.group(1)} = " + (", ".join(vals[:-1]) + " or " + vals[-1] if len(vals) > 1 else vals[0])
    t = re.sub(r"(\b[A-Za-zα-ω]) ∈ \{([^}]*)\}", setlist, t)
    t = t.replace("⌊", "floor(").replace("⌋", ")").replace("{−15…15}", "−15, …, 15")
    t = re.sub(r"O = −15, …, 15", "O = −15, …, 15", t)
    return t


# ------------------------------------------------------------------------------------------------ docx helpers
def new_document(landscape):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = SIZE
    rpr = st.element.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    for k in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(k), FONT)
    pf = st.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = 1.0
    sec = doc.sections[0]
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = Mm(297), Mm(210)
    else:
        sec.page_width, sec.page_height = Mm(210), Mm(297)
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Mm(25))
    cp = doc.core_properties
    cp.author = ""
    cp.last_modified_by = ""
    cp.comments = ""
    cp.title = ""
    return doc


def rich(par, text, bold=False, color=None):
    """Add text with _x subscripts, ^(…) superscripts and {sup:…} markers as Word runs (Arial, 11 pt)."""
    tokens = re.split(r"(_[tjAF]\b|\^\(−C\)|\{sup:[^}]*\})", text)
    for tok in tokens:
        if not tok:
            continue
        if re.fullmatch(r"_[tjAF]", tok):
            r = par.add_run(tok[1:]); r.font.subscript = True
        elif tok == "^(−C)":
            r = par.add_run("(−C)"); r.font.superscript = True
        elif tok.startswith("{sup:"):
            r = par.add_run(tok[5:-1]); r.font.superscript = True
        else:
            r = par.add_run(tok)
        r.bold = bold
        r.font.name = FONT
        r.font.size = SIZE
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
    return par


def caption(doc, num, title):
    p = doc.add_paragraph()
    r = p.add_run(f"Table {num}."); r.bold = True; r.font.name = FONT; r.font.size = SIZE
    rich(p, " " + title)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    return p


def set_border(cell, edge, sz=8):
    tcPr = cell._tc.get_or_add_tcPr()
    b = tcPr.find(qn("w:tcBorders"))
    if b is None:
        b = OxmlElement("w:tcBorders"); tcPr.append(b)
    e = OxmlElement(f"w:{edge}")
    e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(sz)); e.set(qn("w:space"), "0"); e.set(qn("w:color"), "000000")
    b.append(e)


def no_table_borders(table):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}"); e.set(qn("w:val"), "nil"); b.append(e)
    tblPr.append(b)


def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    h = OxmlElement("w:tblHeader"); h.set(qn("w:val"), "true"); trPr.append(h)


def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    c = OxmlElement("w:cantSplit"); c.set(qn("w:val"), "true"); trPr.append(c)


def add_table(doc, header, rows, widths_mm, align=None, spans=()):
    """rows: list of lists of str (\\n = line break inside a cell); spans: row indices rendered as one merged cell."""
    t = doc.add_table(rows=1 + len(rows), cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    no_table_borders(t)
    align = align or ["l"] * len(header)
    for j, w in enumerate(widths_mm):
        t.columns[j].width = Mm(w)
    allrows = [header] + rows
    for i, vals in enumerate(allrows):
        row = t.rows[i]
        cant_split(row)
        if i == 0:
            repeat_header(row)
        cells = row.cells
        if (i - 1) in spans:
            m = cells[0].merge(cells[-1])
            m.width = Mm(sum(widths_mm))
            p = m.paragraphs[0]
            rich(p, vals[0])
            p.paragraph_format.space_before = Pt(4)
            continue
        for j, v in enumerate(vals):
            c = cells[j]
            c.width = Mm(widths_mm[j])
            p = c.paragraphs[0]
            for k, line in enumerate(str(v).split("\n")):
                if k:
                    p.add_run().add_break()
                rich(p, line, bold=(i == 0))
            p.alignment = {"l": WD_ALIGN_PARAGRAPH.LEFT, "c": WD_ALIGN_PARAGRAPH.CENTER,
                           "r": WD_ALIGN_PARAGRAPH.RIGHT}[align[j]]
    for c in t.rows[0].cells:
        set_border(c, "top"); set_border(c, "bottom")
    for c in t.rows[-1].cells:
        set_border(c, "bottom")
    return t


def notes(doc, lines):
    first = True
    for ln in lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6 if first else 0)
        rich(p, ln)
        first = False


def write_csv(path, header, rows, spans=()):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([h.replace("\n", " ") for h in header])
        for i, r in enumerate(rows):
            w.writerow([r[0]] + [""] * (len(header) - 1) if i in spans else [str(v).replace("\n", " ") for v in r])


# ------------------------------------------------------------------------------------------------ Table 1
def table1():
    T = canonical("table1")
    sv = canonical("schematic_values")
    doc = new_document(landscape=True)
    caption(doc, 1, "Data and analysis sets, representations and adjustment arms.")
    # (A) sets
    p = doc.add_paragraph(); rich(p, "(A) Data and analysis sets"); p.paragraph_format.space_after = Pt(3)
    hdrA = ["Set", "Cases", "Cases per centre\n(2 / 3 / 4 / 5)", "Definition", "Design cells", "Arms run"]
    rowsA = []
    for r in T["sets"]:
        name = r["set"].replace("representation set (E1, E3-site, PCA / LEACE)", "Representation set{sup:a}")
        name = name[0].upper() + name[1:]
        cpc = r["centres_2_3_4_5"].replace("all 278 full-length cases of centres 2–5", sv["centres_representation"])
        rowsA.append([name, str(r["cases"]), cpc, typo(r["definition"]),
                      str(r["design_cells"]) if r["design_cells"] != "" else "—",
                      str(r["arms_run"]) if r["arms_run"] != "" else "—"])
    wA = [48, 16, 38, 103, 22, 18]
    add_table(doc, hdrA, rowsA, wA, align=["l", "r", "l", "l", "r", "r"])
    # (B) representations
    p = doc.add_paragraph(); rich(p, "(B) Representations (models and checkpoints)")
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(3)
    hdrB = ["Arm", "Model and checkpoint", "Kind", "Input", "Representation", "Reduction", "Selection{sup:b}"]
    # model identifiers: one component per line; zero-width break opportunities after "/" and "_" (U+200B)
    rowsB = [[r["arm"], re.sub(r"([/_])", "\\1\u200b", r["model"]).replace(", ", "\n"), r["kind"], r["input"],
              r["representation"], r["reduction"], r["selection"]] for r in T["models"]]
    wB = [30, 58, 24, 31, 40, 25, 38]
    add_table(doc, hdrB, rowsB, wB)
    # (C) arms
    p = doc.add_paragraph(); rich(p, "(C) Adjustment arms (protocol §8)")
    p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(3)
    hdrC = ["Arm", "Adjustment set at window step t"]
    rowsC = [[r["arm"], r["adjustment_set"]] for r in T["arms"]]
    wC = [40, 203]
    add_table(doc, hdrC, rowsC, wC)
    runs = {}
    for r in T["sets"]:
        if r["arms"]:
            runs[r["set"]] = r["arms"].replace(" ", ", ")
    notes(doc, [
        "Cases are full-length DS203 videos of centres 2–5. Design cells are the grid cells run in that set (each "
        "with 200 synthetic replicates); arms run: "
        + "; ".join(f"{k}, {v}" for k, v in runs.items()) + ".",
        "{sup:a}Used for E1, E3-site, principal component analysis (PCA) and LEACE fitting; no causal grid is run on it.",
        "{sup:b}Model selection under protocol §4.1 (ranking and tie-breaks); the reference model is fixed by "
        "Decision 005.",
        "Z: the trajectory-constant factor of the theory maps to which the explicit site C corresponds (protocol "
        "§12.1). H_t, past synthetic actions; C, centre (site); S_t, content state (appendix visible); U, synthetic "
        "unmeasured confounder; R_t, 64-component representation; R_t^(−C), R_t after linear site removal (LEACE).",
        "Abbreviations: FM-P, FM-S, REF, primary, secondary and reference representation arms; −C, linearly "
        "site-removed; nat, native acquisition; NV, no video; s, switch step of S; n, number of 5-s steps of the "
        "video; O, window offset; PCA, principal component analysis.",
    ])
    doc.save(OUT / "Table_1.docx")
    # CSV: the three blocks in sequence
    with open(OUT / "Table_1.csv", "w", newline="") as f:
        w = csv.writer(f)
        for title, h, rows in (("(A)", hdrA, rowsA), ("(B)", hdrB, rowsB), ("(C)", hdrC, rowsC)):
            w.writerow([title]); w.writerow([x.replace("\n", " ") for x in h])
            for r in rows:
                w.writerow([str(x).replace("\n", " ") for x in r])
    return dict(A=rowsA, B=rowsB, C=rowsC)


# ------------------------------------------------------------------------------------------------ Table 2
def status(r):
    """Display status of a family row, mechanically from its record fields (see the Table 2 footnotes)."""
    if not r["tested"]:
        return "Not tested (§13)"
    if r["set"] == "primary":
        return f"Verdict: {r['locked_verdict'].lower()}"
    return "Reported separately"


def table2():
    F = canonical("fam_dbar")["rows"]
    gs = canonical("gsite")
    doc = new_document(landscape=True)
    caption(doc, 2, "Family verdicts in the primary set (protocol §12.3) and the same families in the sensitivity "
                    "sets (§10.3).")
    hdr = ["Family", "Comparison\n(with C vs without C)", "Cells", "Mean D (95% CI)", "Share of cells\nwith D_j > 0",
           "Direction rule", "Conditions failed (§13)", "Reported as"]
    order = [("primary", "Primary set, 158 cases (enters family verdicts)"),
             ("W0", "W = 0 set, 204 cases (sensitivity; reported separately)"),
             ("W5", "W = 5 set, 201 cases (sensitivity; reported separately)"),
             ("single_file", "Single-file set, 123 cases (sensitivity; reported separately)")]
    rows, spans = [], []
    for s, label in order:
        sub = [r for r in F if r["set"] == s and not r["role"].startswith("exploratory")]
        spans.append(len(rows)); rows.append([label] + [""] * 7)
        for r in sub:
            rows.append([r["family"], r["comparison"], str(r["n_cells"]), f"{r['D_bar_3dp']} ({r['ci_3dp']})",
                         r["share_2dp"], r["rule_verdict"].capitalize(),
                         "None" if r["conditions_failed"] == "none" else r["conditions_failed"], status(r)])
    excluded = [r for r in F if r["role"].startswith("exploratory")]
    w = [24, 37, 15, 49, 26, 27, 27, 42]
    add_table(doc, hdr, rows, w, align=["l", "l", "r", "l", "r", "l", "l", "l"], spans=spans)
    fam_def = [r for r in F if r["set"] == "primary"]
    notes(doc, [
        "D_j = (|bias| without C − |bias| with C) / mean truth for P1 families and (|bias| with C − |bias| without C) "
        "/ mean truth for P2 families (positive = as predicted); |bias| = |mean over the 200 replicates of (estimate − "
        "truth)|. Mean D = unweighted mean of D_j over the family's cells (D̄_F in the protocol). D is a dimensionless "
        "relative difference in absolute bias.",
        "95% CI: percentile interval of a paired bootstrap (2,000 resamples of the 200 synthetic replicates within "
        "each cell, the same indices for both arms and the truth; cells fixed; seed 20261008). It expresses "
        "simulation (Monte Carlo) uncertainty, not real-data sampling uncertainty.",
        "Direction rule (§12.3): supported if the lower bound > 0 and D_j > 0 in at least 75% of the cells; "
        "contradicted if the upper bound < 0 or D_j > 0 in at most 25% of the cells; inconclusive otherwise. Only the "
        "primary set yields verdicts; a supported verdict is reported as consistent with the theory-motivated "
        "direction, not as a confirmation of the theory maps. A family whose §13 conditions fail is not tested and is "
        "reported descriptively (FM-P vs FM-P−C families). Sensitivity-set results are reported separately and never "
        "enter verdicts.",
        "Family cells and predictions (protocol §12.2): " + "; ".join(
            f"{r['family']}, {typo(r['cells_definition'])}, predicted {r['prediction']}" for r in fam_def) + ".",
        f"G-SITE (η² of S at the window start on C; gate ≤ 0.01): primary set {gs['primary']:.4f}, W = 0 set "
        f"{gs['W0']:.4f}, W = 5 set {gs['W5']:.4f}; no single-file value exists (the locked code applies the primary "
        "value). E3-site failed on the 158-case set for all three representations (Table 3).",
        "The W = 0 set also yields P1a (" + ", ".join(f"{r['n_cells']} cells" for r in excluded) + ") because both "
        "arms were run there; P1a is outside the §10.3 scope, is labelled exploratory in the results report and is "
        "not shown here.",
        "Abbreviations: C, site (centre); NV, no video; ORACLE, exact content state S and C; ORACLE−C, S without C; "
        "FM-P, primary representation; FM-P−C, FM-P after linear site removal.",
    ])
    doc.save(OUT / "Table_2.docx")
    write_csv(OUT / "Table_2.csv", hdr, rows, spans)
    return rows


# ------------------------------------------------------------------------------------------------ Table 3
def table3():
    T = canonical("table3")["rows"]
    by = {r["key"]: r for r in T}
    keys = ["P", "S", "REF", "P-nat"]
    doc = new_document(landscape=True)
    caption(doc, 3, "Representation diagnostics: step-5 checks (protocol §5) and, separately, the exploratory X1 eraser "
                    "on the 158-case analysis region.")
    hdr = ["Check", "Set (cases)", "FM-P", "FM-S", "REF", "FM-P-nat"]
    rows, spans = [], []

    def est_ci(e, status=None):
        if e is None:
            return "—"
        s = f3(e["est"]) + (f", {status}" if status else "") + f"\n{ci(e)}"
        return s

    def st_pass(e, key="passed", yes="pass", no="fail"):
        return yes if e.get(key) else no

    def add(label, setl, f):
        rows.append([label, setl] + [f(by[k]) for k in keys])

    spans.append(len(rows)); rows.append(["Step-5 checks (protocol §5)"] + [""] * 5)
    for s, setl in (("278", "278, all steps"), ("158", "158, analysis region"),
                    ("123", "123, single-file{sup:a}")):
        add("E1: site BA, linear probe{sup:b}", setl, lambda r, s=s: est_ci(r[f"E1_linear_{s}"], st_pass(r[f"E1_linear_{s}"])))
    for s, setl in (("158", "158, analysis region"), ("123", "123, single-file{sup:a}")):
        add("E2: ΔAUC before removal{sup:c}", setl,
            lambda r, s=s: est_ci(r[f"E2_{s}"], "met" if r[f"E2_{s}"]["met"] else "not met"))
        add("E2: ΔAUC after protocol removal{sup:c}", setl,
            lambda r, s=s: est_ci(r[f"E2_after_{s}"], "met" if r[f"E2_after_{s}"]["met"] else "not met")
            if r[f"E2_after_{s}"] else "—")
    for probe, pl in (("linear", "linear"), ("mlp", "MLP")):
        for s, setl in (("278", "278, all steps"), ("158", "158, analysis region"),
                        ("123", "123, single-file{sup:a}")):
            add(f"E3-site: site BA after removal, {pl} probe", setl,
                lambda r, s=s, probe=probe: est_ci(r[f"E3site_{probe}_{s}"]))
            if probe == "linear":
                add("E3-site: one-sided 95% upper bound, linear{sup:d}", setl,
                    lambda r, s=s: "—" if r[f"E3site_linear_{s}"] is None else
                    f"{f3(r[f'E3site_linear_{s}']['upper'])}, {'pass' if r[f'E3site_linear_{s}']['passed'] else 'fail'}")
            else:
                add("E3-site: one-sided 95% upper bound, MLP{sup:d}", setl,
                    lambda r, s=s: "—" if r[f"E3site_mlp_{s}"] is None else
                    f"{f3(r[f'E3site_mlp_{s}']['upper'])}, "
                    f"{'> 0.35' if r[f'E3site_mlp_{s}']['exceeds_0p35'] else '≤ 0.35'}")

    def state(e):
        if e is None:
            return "—"
        if not e.get("applicable"):
            return "not applicable{sup:e}"
        return f"{f3(e['retained_fraction'])}, {'pass' if e['pass_'] else 'fail'}"
    for s, setl in (("158", "158, analysis region"), ("123", "123, single-file{sup:a}")):
        add("E3-state: retained fraction of ΔAUC{sup:f}", setl, lambda r, s=s: state(r.get(f"E3state_{s}")))

    spans.append(len(rows)); rows.append(["Reported only (no criterion)"] + [""] * 5)
    for s, setl in (("278", "278, all steps"), ("158", "158, analysis region"),
                    ("123", "123, single-file{sup:a}")):
        add("E1: site BA, MLP probe (before removal)", setl, lambda r, s=s: est_ci(r[f"E1_mlp_{s}"]))
    for f, lab_, setl in (("E2_278", "E2: ΔAUC, all steps", "278, all steps"),
                          ("E2_278_normtime", "E2: ΔAUC, normalized-time base{sup:g}", "278, all steps"),
                          ("E2_primary_normtime", "E2: ΔAUC, normalized-time base{sup:g}", "158, analysis region"),
                          ("E2_single_file_normtime", "E2: ΔAUC, normalized-time base{sup:g}",
                           "123, single-file{sup:a}"),
                          ("E2_primary_history", "E2: ΔAUC, base with past actions{sup:h}",
                           "158, analysis region")):
        add(lab_, setl, lambda r, f=f: est_ci(r[f]))

    spans.append(len(rows)); rows.append(["Exploratory X1 (outside the protocol; eraser refitted on the 158-case "
                                          "analysis region){sup:i}"] + [""] * 5)
    xs = "158, analysis region"
    add("X1 E3-site: site BA after removal, linear probe", xs, lambda r: est_ci(r.get("X1_E3site_linear_158")))
    add("X1 E3-site: one-sided 95% upper bound, linear", xs,
        lambda r: f"{f3(r['X1_E3site_linear_158']['upper'])}" if r.get("X1_E3site_linear_158") else "—")
    add("X1 E3-site: site BA after removal, MLP probe", xs, lambda r: est_ci(r.get("X1_E3site_mlp_158")))
    add("X1 E3-site: one-sided 95% upper bound, MLP", xs,
        lambda r: (f"{f3(r['X1_E3site_mlp_158']['upper'])}, "
                   f"{'> 0.35' if r['X1_E3site_mlp_158']['exceeds_0p35'] else '≤ 0.35'}")
        if r.get("X1_E3site_mlp_158") else "—")
    add("X1 E2: ΔAUC after X1 removal{sup:c}", xs,
        lambda r: est_ci(r["X1_E2_after_158"], "met" if r["X1_E2_after_158"]["met"] else "not met")
        if r.get("X1_E2_after_158") else "—")
    add("X1 E3-state: retained fraction of ΔAUC{sup:f}", xs, lambda r: state(r.get("X1_E3state_158")))

    w = [64, 36, 36.5, 36.5, 36.5, 36.5]
    add_table(doc, hdr, rows, w, align=["l", "l", "l", "l", "l", "l"], spans=spans)
    notes(doc, [
        "Values: estimate (95% interval); balanced accuracy (BA) of the case-level four-centre site probe (chance "
        "0.25); intervals are case-level bootstrap intervals stratified by site (2,000 resamples, seed 20261008; "
        "percentile 2.5–97.5). Step-5 values from the step-5 record; X1 values from the X1/X2 record. FM-P-nat has no "
        "site-removed arm (—).",
        "{sup:a}§10.3 single-file sensitivity set (123 cases of the primary set).",
        "{sup:b}E1 criterion: BA ≥ 0.50 with lower bound > 0.35.",
        "{sup:c}ΔAUC = held-out AUC for S_t of base + R_t minus base (elapsed-time spline); criterion ΔAUC ≥ 0.05 "
        "with the interval excluding 0.",
        "{sup:d}E3-site criterion (linear probe): one-sided 95% upper bound (95th percentile of the bootstrap) ≤ 0.35 "
        "on both the 278-case and the 158-case set; the MLP probe is compared with 0.35 for the claim ceiling only.",
        "{sup:e}E2 before removal not met, so retention of state information could not be assessed.",
        "{sup:f}ΔAUC after removal / ΔAUC before removal; criterion ≥ 0.50.",
        "{sup:g}Normalized time (step / case length) uses future information and is not a valid baseline (protocol "
        "§5.2).",
        "{sup:h}Base = elapsed time + past synthetic actions in one reference cell (K = 5, P = 0, W = 5, α = 0.5, "
        "γ = 1, φ_A = 0, replicate 1).",
        "{sup:i}Exploratory (plan registered on OSF, osf.io/5c627): the X1 eraser is fitted on training folds and "
        "evaluated on held-out folds of the same population; its linear E3-site value is a check of the procedure "
        "and does not gate any comparison. No verdict.",
        "Abbreviations: AUC, area under the receiver operating characteristic curve; MLP, two-layer perceptron "
        "probe; FM-P, FM-S, REF, primary, secondary and reference representations; nat, native acquisition.",
    ])
    doc.save(OUT / "Table_3.docx")
    write_csv(OUT / "Table_3.csv", hdr, rows, spans)
    return rows


def main():
    OUT.mkdir(exist_ok=True)
    t1 = table1()
    t2 = table2()
    t3 = table3()
    print(f"Table_1: {len(t1['A'])}+{len(t1['B'])}+{len(t1['C'])} rows; Table_2: {len(t2)} rows; Table_3: {len(t3)} rows")


if __name__ == "__main__":
    main()
