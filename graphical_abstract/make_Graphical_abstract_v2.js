// make_Graphical_abstract_v2.js — graphical abstract (v3 revision, task v3 §3): 130 × 52 mm (5 × 13 cm), all text
// ≥ 10 pt (title 11 pt); "evaluation" replaces "benchmark"; the P1b statement carries its scope (no prior action
// history, W = 0); the P2 result is "slightly higher"; one descriptive line on W = 30. Numbers only from Table 2 (the
// same 3-decimal strings, canonical/ga_values.json). The exploratory block is dashed and labelled EXPLORATORY.
// Native vector shapes (pptxgenjs 4.0.1); Arial; grayscale + navy.
//   node graphical_abstract/make_Graphical_abstract_v2.js  ->  graphical_abstract/Graphical_abstract_v2.pptx

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

const MM = 1 / 25.4;
const W = 130, H = 52;
const NAVY = "2B3D6B", K = "1A1A1A", G4 = "4D4D4D", G6 = "6B6B6B";
const SZ = 10, LS = 11;
const pres = new pptxgen();
pres.defineLayout({ name: "GA", width: W * MM, height: H * MM });
pres.layout = "GA";
pres.author = "";
pres.company = "";
pres.title = "Graphical abstract";
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

function box(x, y, w, h, o = {}) {
  s.addShape(pres.ShapeType.rect, { x: x * MM, y: y * MM, w: w * MM, h: h * MM, fill: { color: "FFFFFF" },
    line: { color: o.line || G6, width: o.lw || 0.75, dashType: o.dash || "solid" } });
}
// lines: array of lines; each line is an array of [text, bold, colour]
function para(x, y, w, h, lines, o = {}) {
  const runs = [];
  lines.forEach((ln, i) => ln.forEach(([t, b, c], j) => runs.push({ text: t, options: { bold: !!b, color: c || K,
    fontSize: o.size || SZ, breakLine: j === ln.length - 1 && i < lines.length - 1 } })));
  s.addText(runs, { x: x * MM, y: y * MM, w: w * MM, h: h * MM, fontFace: "Arial", margin: 0, fit: "none",
    align: o.align || "left", valign: "top", lineSpacing: o.ls || LS });
}

// title
para(1.0, 0.6, 128, 5, [[["Site adjustment in a semi-synthetic sequential causal evaluation", true]]], { size: 11, ls: 12 });

// row 1: confirmatory (primary set)
const y1 = 5.6, h1 = 20.3;
box(0.6, y1, 128.8, h1, { line: NAVY, lw: 1.25 });
para(1.9, y1 + 0.55, 126, 4.5, [[["Confirmatory (primary set)", true, NAVY]]]);
para(1.9, y1 + 0.55 + 3.88, 62, 16, [
  [["No prior action history (W = 0),"]],
  [["later actions (P > 0): with site,"]],
  [["|bias| lower", true]],
  [[`P1b-SITE mean D ${G["P1b-SITE"].D_bar_3dp}`, false, G4]]]);
para(66.0, y1 + 0.55 + 3.88, 62, 16, [
  [["One step, no later actions"]],
  [["(K = 1, P = 0): with site,"]],
  [["|bias| slightly higher", true]],
  [[`P2-SITE mean D ${G["P2-SITE"].D_bar_3dp}`, false, G4]]]);

// row 2: protocol erasure check | exploratory X1
const y2 = y1 + h1 + 0.6, h2 = 20.45, wA = 57.0;
box(0.6, y2, wA, h2);
para(1.9, y2 + 0.55, wA - 2.6, h2 - 1, [
  [["Linear site erasure", true]],
  [["Full set: passes"]],
  [["Analysis windows: fails"]],
  [["Representation families not tested"]]]);
const x3 = 0.6 + wA + 1.2, w3 = 129.4 - x3;
box(x3, y2, w3, h2, { dash: "dash" });
para(x3 + 1.3, y2 + 0.55, w3 - 2.6, h2 - 1, [
  [["EXPLORATORY: X1", true, G4], [" (no verdict)", false, G4]],
  [["Eraser refitted on the analysis windows"]],
  [["MLP probe still decodes site", true]],
  [["|bias| vs protocol eraser: small change"]],
  [["vs site retained: larger (P1b-FM cells)"]]]);

// bottom line: descriptive result of Figure 3 (no number)
para(1.0, y2 + h2 + 0.45, 128, 4.5, [[["With 30 steps of prior actions, adding site changed |bias| little (descriptive)"]]]);
if (y2 + h2 + 0.45 + 3.9 > H - 0.3) throw new Error("content below the canvas");

pres.writeFile({ fileName: path.join(__dirname, "Graphical_abstract_v2.pptx") }).then((f) => console.log("written " + f));
