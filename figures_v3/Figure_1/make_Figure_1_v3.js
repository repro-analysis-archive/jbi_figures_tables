// make_Figure_1_v3.js — Figure 1 (v4 revision): study design schematic, as v2 with less vertical space (task v4 §1.2).
// v4: height 232 -> 219 mm with every font size unchanged — tighter spacing between the panels ((A)-(B) 3 -> 2.5 mm,
// (B)-(C) 4.5 -> 2.5 mm, (C)-(D) 3.5 -> 2.5 mm), inside (A) (heading to the first box 2 mm less; gaps between the set
// boxes 2.5-2.75 -> 1.5 mm) and inside (D) (heading to the steps 1 mm less; steps to the exploratory boxes 0.5 mm
// less) and a 1.5 mm bottom margin (v2: 4 mm). Boxes, texts, arrows and their relative layout within each panel as v2.
// Native vector shapes (pptxgenjs 4.0.1); Arial; grayscale + navy #2B3D6B; integer point sizes at the final 190 mm
// width: body 14 pt, headings 15 pt bold, panel labels 16 pt bold (figure template §2-1 relative rule).
// Panels: (A) data and analysis sets, (B) time structure and data-generating process, (C) adjustment arms,
// (D) workflow and registrations (old panel D removed; old E relabelled D). Every number from hash-guarded canonical
// JSON; plain symbols as registered in NOTATION_REGISTRY.md.
//   node figures_v3/Figure_1/make_Figure_1_v3.js   ->  figures_v3/Figure_1/Figure_1_v3.pptx

const path = require("path");
const fs = require("fs");
const crypto = require("crypto");
const ROOT = path.resolve(__dirname, "..", "..");
const pptxgen = require(path.join(ROOT, "node_modules", "pptxgenjs"));

function readCanonical(name) {
  const p = path.join(ROOT, "canonical", name + ".json");
  const sums = fs.readFileSync(path.join(ROOT, "canonical", "SHA256SUMS.txt"), "utf8").trim().split("\n");
  const want = sums.map((l) => l.split(/\s+/)).find((x) => x[1] === name + ".json");
  const got = crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
  if (!want || got !== want[0]) throw new Error("hash guard failed for " + name);
  return JSON.parse(fs.readFileSync(p, "utf8"));
}
const V = readCanonical("schematic_values");
const T1 = readCanonical("table1");

const MM = 1 / 25.4;
const W = 190, H = 219;                                    // v2: 232
const NAVY = "2B3D6B", K = "1A1A1A", G4 = "4D4D4D", G6 = "6B6B6B", GB = "B3B3B3", FILL = "F2F2F2";
const BODY = 14, HEAD = 15, PANEL = 16, LS = 17;          // pt; line spacing 17 pt = 6.0 mm
const pres = new pptxgen();
pres.defineLayout({ name: "JBI_FULL", width: W * MM, height: H * MM });
pres.layout = "JBI_FULL";
pres.author = "";
pres.company = "";
pres.title = "Figure 1";
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

function box(x, y, w, h, o = {}) {
  s.addShape(pres.ShapeType.rect, { x: x * MM, y: y * MM, w: w * MM, h: h * MM, fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || G6, width: o.lw || 0.9, dashType: o.dash || "solid" } });
}
function txt(x, y, w, h, runs, o = {}) {
  const arr = runs.map((r, i, a) => ({ text: r.text, options: { bold: r.bold === true, color: r.color || o.color || K,
    fontSize: r.size || o.size || BODY, breakLine: r.br === true || (o.lines === true && i < a.length - 1) } }));
  s.addText(arr, { x: x * MM, y: y * MM, w: w * MM, h: h * MM, fontFace: "Arial", margin: 0, fit: "none",
    align: o.align || "left", valign: o.valign || "top", lineSpacing: o.ls || LS });
}
function line(x1, y1, x2, y2, o = {}) {
  s.addShape(pres.ShapeType.line, { x: Math.min(x1, x2) * MM, y: Math.min(y1, y2) * MM, w: Math.abs(x2 - x1) * MM,
    h: Math.abs(y2 - y1) * MM, flipH: x2 < x1, flipV: y2 < y1,
    line: { color: o.color || G6, width: o.lw || 0.9, dashType: o.dash || "solid", endArrowType: o.arrow ? "triangle" : undefined } });
}
function panel(label, heading, y) {
  txt(0.8, y, 11, 7, [{ text: label, bold: true, size: PANEL }]);
  txt(11.5, y + 0.45, 178, 7, [{ text: heading, bold: true, size: HEAD }]);
}

// ------------------------------------------------------------------ (A) data and analysis sets
panel("(A)", "Data and analysis sets", 0.8);
box(1, 20, 75, 21.5, { fill: FILL });                       // v2: y 24 (centred on the set stack)
txt(3, 21.6, 72, 19, [{ text: `Representation set: ${V.n_representation} cases`, bold: true },
  { text: `Centres 2–5: ${V.centres_representation}` }, { text: "E1, E3-site, PCA, LEACE" }], { lines: true });
const kids = [
  { y: 8, h: 14, t: [{ text: `Primary causal set (W = 30): ${V.n_primary} cases`, bold: true }, { text: V.centres_primary }], prim: true },
  { y: 33, h: 8, t: [{ text: `W = 5 set: ${V.n_W5} cases (sensitivity)` }] },     // v2: y 10, 37.5, 48
  { y: 42.5, h: 8, t: [{ text: `W = 0 set: ${V.n_W0} cases (sensitivity)` }] },
];
line(76, 30.75, 80, 30.75);
line(80, kids[0].y + kids[0].h / 2, 80, kids[2].y + kids[2].h / 2);
for (const k of kids) {
  line(80, k.y + k.h / 2, 84, k.y + k.h / 2);
  box(84, k.y, 105, k.h, { line: k.prim ? NAVY : G6, lw: k.prim ? 1.5 : 0.9 });
  txt(86.5, k.y + 1.0, 101, k.h - 1.2, k.t, { lines: true, valign: k.prim ? "top" : "middle" });
}
line(89, 22, 89, 27.5);
line(89, 27.5, 94, 27.5);
box(94, 23.5, 95, 8);                                       // v2: y 26.75
txt(96.5, 24.05, 91, 7, [{ text: `Single-file: ${V.n_single} cases (sensitivity)` }], { valign: "middle" });

// ------------------------------------------------------------------ (B) time structure and causal diagram
const YB = 53;                                              // v2: 59
panel("(B)", "Time structure and data-generating process", YB);
const ty = YB + 16, th = 13;
box(1, ty, 36, th, { fill: FILL });
box(37, ty, 42, th, { line: NAVY, lw: 1.5 });
box(79, ty, 36, th, { fill: FILL });
txt(1, ty, 36, th, [{ text: "W pre-window" }, { text: "steps" }], { lines: true, align: "center", valign: "middle" });
txt(37, ty, 42, th, [{ text: "K window steps", bold: true, color: NAVY }, { text: "policy applied" }], { lines: true, align: "center", valign: "middle" });
txt(79, ty, 36, th, [{ text: "P post-window" }, { text: "steps" }], { lines: true, align: "center", valign: "middle" });
line(115, ty + th / 2, 120, ty + th / 2, { arrow: true });
box(120, ty + 2, 11, th - 4, { dash: "dash" });
txt(120, ty + 2, 11, th - 4, [{ text: "Y", bold: true }], { align: "center", valign: "middle" });
txt(37, ty - 7.2, 80, 6.5, [{ text: `d(a) = δ·a, δ = ${V.delta}`, color: NAVY }]);
txt(1, ty + th + 2.2, 134, 19, [
  { text: `1 step = ${V.step_seconds} s of video` },
  { text: `Window start w = s + O, O = ${V.offsets}` },
  { text: "s: step at which S switches 0 → 1" }], { lines: true });
// data-generating process (protocol §6): C -> A; S -> A, Y; U -> A, Y; A -> Y (C has no direct effect on Y)
const nd = { S: [165, YB + 9], C: [146, YB + 24], A: [165, YB + 24], Y: [184, YB + 24], U: [174.5, YB + 39] };
const real = { C: true, S: true };
const R_ = 4.6;
function node(k) {
  const [cx, cy] = nd[k];
  s.addShape(pres.ShapeType.ellipse, { x: (cx - R_) * MM, y: (cy - R_) * MM, w: 2 * R_ * MM, h: 2 * R_ * MM,
    fill: { color: real[k] ? FILL : "FFFFFF" }, line: { color: real[k] ? K : G6, width: 0.9, dashType: real[k] ? "solid" : "dash" } });
  txt(cx - R_, cy - R_, 2 * R_, 2 * R_, [{ text: k, bold: true }], { align: "center", valign: "middle" });
}
function edge(a, b, col) {
  const [x1, y1] = nd[a], [x2, y2] = nd[b];
  const d = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / d, uy = (y2 - y1) / d;
  line(x1 + ux * R_, y1 + uy * R_, x2 - ux * (R_ + 0.3), y2 - uy * (R_ + 0.3), { color: col || K, arrow: true });
}
edge("C", "A", NAVY); edge("S", "A"); edge("S", "Y"); edge("U", "A"); edge("U", "Y"); edge("A", "Y");
Object.keys(nd).forEach(node);
// key: solid outline = from the data, dashed = synthetic
const kyy = YB + 49.5;
s.addShape(pres.ShapeType.ellipse, { x: 141 * MM, y: (kyy - 2.2) * MM, w: 4.4 * MM, h: 4.4 * MM, fill: { color: FILL }, line: { color: K, width: 0.9 } });
txt(147, kyy - 3, 14, 6, [{ text: "data" }], { valign: "middle" });
s.addShape(pres.ShapeType.ellipse, { x: 161 * MM, y: (kyy - 2.2) * MM, w: 4.4 * MM, h: 4.4 * MM, fill: { color: "FFFFFF" }, line: { color: G6, width: 0.9, dashType: "dash" } });
txt(167, kyy - 3, 22, 6, [{ text: "synthetic" }], { valign: "middle" });

// ------------------------------------------------------------------ (C) adjustment arms
const YC = YB + 55;                                         // v2: 116 (= YB + 57)
panel("(C)", "Adjustment arms (each also adjusts for past actions H)", YC);
const armNames = new Set(T1.arms.flatMap((a) => a.arm.split(", ")));
function matrix(x0, x1, cols, arms, y0, hh) {
  const hy = y0, rh = 6.3;
  line(x0, hy - 0.5, x1, hy - 0.5, { color: K, lw: 0.9 });
  txt(x0 + 1, hy + 0.5, 30, 6, [{ text: "Arm", bold: true }]);
  for (const [c, x] of cols) {
    const parts = c.split("|");
    txt(x - 12, hy + 0.5, 24, 12, parts.map((t) => ({ text: t, bold: true })), { lines: true, align: "center" });
  }
  line(x0, hy + hh, x1, hy + hh, { color: K, lw: 0.9 });
  arms.forEach(([names, m], i) => {
    for (const a of names) if (!armNames.has(a)) throw new Error("arm not in protocol §8: " + a);
    const y = hy + hh + 0.6 + i * rh;
    txt(x0 + 1, y, x1 - x0, rh, [{ text: names.join(" · ") }], { valign: "middle" });
    for (const [c, x] of cols) if (m.includes(c.split("|")[0])) txt(x - 5, y, 10, rh, [{ text: "●" }], { align: "center", valign: "middle" });
  });
  const yb = hy + hh + 0.6 + arms.length * rh + 0.4;
  line(x0, yb, x1, yb, { color: K, lw: 0.9 });
  return yb;
}
const ybL = matrix(0.8, 84, [["C", 50], ["S", 62], ["U", 74]],
  [[["NV"], []], [["SITE"], ["C"]], [["ORACLE−C"], ["S"]], [["ORACLE"], ["S", "C"]], [["FULL"], ["S", "C", "U"]]], YC + 9, 7.0);
const ybR = matrix(91, 189.2, [["R", 160], ["R, site|removed", 177.3]],
  [[["FM-P", "FM-S", "REF"], ["R"]], [["FM-P−C", "FM-S−C", "REF−C"], ["R, site"]], [["FM-P-nat"], ["R"]]], YC + 9, 12.5);

// ------------------------------------------------------------------ (D) workflow and registrations
const YD = Math.max(ybL, ybR) + 2.5;                        // v2: + 3.5
panel("(D)", "Workflow and registrations", YD);
const steps = [
  [["Protocol", true], ["frozen", true], [V.protocol_frozen, false]],
  [["Code lock", true], [V.code_lock_date, false]],
  [["Steps 4–5", true], ["E1–E3 checks", false], [V.step5_record_date, false]],
  [["Step 6", true], ["causal grid", false], [`to ${V.step6_completed}`, false]],
  [["Step 7", true], ["verdicts", false], [V.step7_record_date, false]],
];
const bw = 35.4, gap = 3.0, x0 = 0.4, by = YD + 15.5, bh = 20.0;   // v2: by = YD + 16.5
steps.forEach((lines, i) => {
  const x = x0 + i * (bw + gap);
  box(x, by, bw, bh, { line: i === 4 ? NAVY : G6, lw: i === 4 ? 1.5 : 0.9 });
  txt(x + 1.3, by + 1.0, bw - 2, bh - 1.2, lines.map(([t, b]) => ({ text: t, bold: b, color: b ? K : G4 })), { lines: true });
  if (i < 4) line(x + bw + 0.15, by + bh / 2, x + bw + gap - 0.15, by + bh / 2, { arrow: true });
});
const ax0 = x0 + 2 * (bw + gap), ax1 = x0 + 4 * (bw + gap) + bw;
line(ax0, by - 2.4, ax1, by - 2.4, { color: G4, lw: 0.8 });
line(ax0, by - 2.4, ax0, by - 0.8, { color: G4, lw: 0.8 });
line(ax1, by - 2.4, ax1, by - 0.8, { color: G4, lw: 0.8 });
txt(ax0, by - 8.6, ax1 - ax0, 6.5, [{ text: "records committed automatically", color: G4 }], { align: "center" });   // v2: by - 9.2
const ey = by + bh + 3.5, eh = 19.5;                        // v2: + 4.0
txt(1.0, ey + 1.0, 2 * (bw + gap) + bw + 2, eh, [
  { text: "Exploratory, outside the protocol", bold: true, color: G4 },
  { text: "(dashed); plans registered on OSF:", color: G4 },
  { text: "X1/X2 during step 6, B after step 7", color: G4 }], { lines: true });
const xs = [x0 + 3 * (bw + gap), x0 + 4 * (bw + gap)];
[["X1/X2 plan", V.x_plan_date, V.x_osf], ["B plan", V.b_plan_date, V.b_osf]].forEach(([a, d, u], i) => {
  box(xs[i], ey, bw, eh, { dash: "dash" });
  txt(xs[i] + 1.3, ey + 1.0, bw - 2, eh - 1.2, [{ text: a, bold: true }, { text: d, color: G4 },
    { text: u.replace("https://", ""), color: G4 }], { lines: true });
  line(xs[i] + bw / 2, by + bh, xs[i] + bw / 2, ey, { dash: "dash", arrow: true });
});
if (Math.abs(H - (ey + eh) - 1.5) > 1e-9) throw new Error("bottom margin is not 1.5 mm: " + (H - ey - eh));
console.log("panel D ends at " + (ey + eh).toFixed(1) + " mm of " + H);

pres.writeFile({ fileName: path.join(__dirname, "Figure_1_v3.pptx") }).then((f) => console.log("written " + f));
