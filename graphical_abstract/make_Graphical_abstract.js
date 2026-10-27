// make_Graphical_abstract.js — graphical abstract for the JBI manuscript (figure template §15; JBI: landscape,
// >= 1,328 px wide, readable at 13 cm). Native vector shapes (pptxgenjs 4.0.1); Arial 7–9 pt at 130 mm width;
// grayscale + navy. Numbers: only Table 2 values (canonical/ga_values.json, the same 3-decimal strings as Table 2).
// The exploratory block is outlined with a dashed line and labelled EXPLORATORY.
//   node graphical_abstract/make_Graphical_abstract.js  ->  graphical_abstract/Graphical_abstract.pptx

const path = require("path");
const fs = require("fs");
const crypto = require("crypto");
const ROOT = path.resolve(__dirname, "..");
const pptxgen = require(path.join(ROOT, "node_modules", "pptxgenjs"));

function readCanonical(name) {
  const p = path.join(ROOT, "canonical", name + ".json");
  const sums = fs.readFileSync(path.join(ROOT, "canonical", "SHA256SUMS.txt"), "utf8").trim().split("\n");
  const want = sums.map((l) => l.split(/\s+/)).find((x) => x[1] === name + ".json");
  const got = crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
  if (!want || got !== want[0]) throw new Error("hash guard failed for " + name);
  return JSON.parse(fs.readFileSync(p, "utf8"));
}
const G = readCanonical("ga_values");
const SV = readCanonical("schematic_values");

const MM = 1 / 25.4;
const W = 130, H = 52;
const NAVY = "2B3D6B", K = "1A1A1A", G4 = "4D4D4D", G6 = "6B6B6B", FILL = "F2F2F2";
const pres = new pptxgen();
pres.defineLayout({ name: "GA", width: W * MM, height: H * MM });
pres.layout = "GA";
pres.author = "";
pres.company = "";
pres.title = "Graphical abstract";
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

function box(x, y, w, h, o = {}) {
  s.addShape(pres.ShapeType.rect, { x: x * MM, y: y * MM, w: w * MM, h: h * MM, fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || G6, width: o.lw || 0.75, dashType: o.dash || "solid" } });
}
function txt(x, y, w, h, runs, o = {}) {
  const arr = runs.map((r, i, a) => ({ text: r.text, options: { bold: r.bold === true, color: r.color || o.color || K,
    fontSize: r.size || o.size || 8, breakLine: r.br === true || (o.lines === true && i < a.length - 1) } }));
  s.addText(arr, { x: x * MM, y: y * MM, w: w * MM, h: h * MM, fontFace: "Arial", margin: 0, fit: "none",
    align: o.align || "left", valign: o.valign || "top", lineSpacing: o.ls || 10 });
}
function arrow(x1, y1, x2, y2, col) {
  s.addShape(pres.ShapeType.line, { x: Math.min(x1, x2) * MM, y: Math.min(y1, y2) * MM, w: Math.abs(x2 - x1) * MM,
    h: Math.abs(y2 - y1) * MM, flipH: x2 < x1, flipV: y2 < y1, line: { color: col || G6, width: 0.75, endArrowType: "triangle" } });
}

// title strip
txt(1.2, 1.0, 127, 4.5, [{ text: "Site adjustment in a semi-synthetic sequential causal benchmark", bold: true, size: 9 }]);
txt(1.2, 5.3, 127, 4, [{ text: "Real clinical video; synthetic actions, outcomes and truth", color: G4, size: 7 }]);

const y0 = 10.4, bh = 40.4, bw = 41.4, gx = 1.9;
const X = [1.2, 1.2 + bw + gx, 1.2 + 2 * (bw + gx)];
// mini timeline icon: K window box (navy) and, optionally, the post-window box (gray)
function timeline(x, y, post) {
  box(x, y, 7, 2.6, { line: NAVY, lw: 1.0 });
  txt(x, y - 0.05, 7, 2.6, [{ text: "K", bold: true, color: NAVY, size: 7 }], { align: "center", valign: "middle" });
  if (post) {
    box(x + 7, y, 9, 2.6, { fill: FILL, line: G6 });
    txt(x + 7, y - 0.05, 9, 2.6, [{ text: "P > 0", size: 7 }], { align: "center", valign: "middle" });
  }
}

// block 1: confirmatory families (primary set)
box(X[0], y0, bw, bh, { line: NAVY, lw: 1.25 });
txt(X[0] + 1.6, y0 + 1.2, bw - 3, 4, [{ text: "Confirmatory", bold: true, color: NAVY }]);
timeline(X[0] + 1.6, y0 + 6.4, true);
txt(X[0] + 1.6, y0 + 10.0, bw - 3, 12, [
  { text: "Actions after the window" },
  { text: "With site: |bias| lower", bold: true },
  { text: `P1b-SITE mean D ${G["P1b-SITE"].D_bar_3dp}`, color: G4, size: 7 }], { lines: true });
timeline(X[0] + 1.6, y0 + 23.4, false);
txt(X[0] + 1.6, y0 + 27.0, bw - 3, 12, [
  { text: "One step, no later actions" },
  { text: "With site: |bias| higher", bold: true },
  { text: `P2-SITE mean D ${G["P2-SITE"].D_bar_3dp}`, color: G4, size: 7 }], { lines: true });

// block 2: protocol erasure check (linear probe, E3-site)
box(X[1], y0, bw, bh, { line: G6 });
txt(X[1] + 1.6, y0 + 1.2, bw - 3, 4, [{ text: "Linear site erasure", bold: true }]);
txt(X[1] + 1.6, y0 + 7.0, bw - 3, 8, [{ text: `Full ${SV.n_representation}-case set` }, { text: "passes", bold: true }], { lines: true, align: "center" });
arrow(X[1] + bw / 2, y0 + 15.0, X[1] + bw / 2, y0 + 18.2);
txt(X[1] + 1.6, y0 + 19.0, bw - 3, 8, [{ text: "Analysis windows" }, { text: "fails", bold: true }], { lines: true, align: "center" });
arrow(X[1] + bw / 2, y0 + 27.0, X[1] + bw / 2, y0 + 30.2);
txt(X[1] + 1.6, y0 + 31.0, bw - 3, 8, [{ text: "Representation families" }, { text: "not tested", bold: true }], { lines: true, align: "center" });

// block 3: exploratory X1 (outside the protocol; dashed outline)
box(X[2], y0, bw, bh, { line: G6, dash: "dash" });
txt(X[2] + 1.6, y0 + 1.2, bw - 3, 4, [{ text: "EXPLORATORY: X1", bold: true, color: G4 }]);
txt(X[2] + 1.6, y0 + 5.4, bw - 3, 4, [{ text: "OSF-registered; no verdict", color: G4, size: 7 }]);
txt(X[2] + 1.6, y0 + 9.6, bw - 3, 30, [
  { text: "Eraser refitted on the" },
  { text: "analysis windows" },
  { text: "MLP probe still decodes site", bold: true, br: true },
  { text: " ", size: 4, br: true },
  { text: "vs protocol eraser:", br: true },
  { text: "small Δ in |bias|", br: true },
  { text: "vs site retained:", br: true },
  { text: "larger |bias| (P1b-FM cells)" },
].map((r, i) => (i < 2 ? { ...r, br: true } : r)));

pres.writeFile({ fileName: path.join(__dirname, "Graphical_abstract.pptx") }).then((f) => console.log("written " + f));
