// make_Figure_1.js — Figure 1 (study schematic) for the JBI manuscript (figure template §15).
// Native vector shapes only (pptxgenjs 4.0.1); Arial; grayscale + navy #2B3D6B; integer point sizes.
// Every number comes from hash-guarded canonical JSON (canonical/schematic_values.json, canonical/table1.json);
// symbols follow NOTATION_REGISTRY.md (plain forms S, A, R, H for S_t, A_t, R_t, H_t: LibreOffice renders
// sub/superscript runs at 58 % size, below the 7 pt floor).
//   node figures/Figure_1/make_Figure_1.js   ->  figures/Figure_1/Figure_1.pptx

const path = require("path");
const fs = require("fs");
const crypto = require("crypto");
const ROOT = path.resolve(__dirname, "..", "..");
const pptxgen = require(path.join(ROOT, "node_modules", "pptxgenjs"));

function readCanonical(name) {
  const p = path.join(ROOT, "canonical", name + ".json");
  const sums = fs.readFileSync(path.join(ROOT, "canonical", "SHA256SUMS.txt"), "utf8").trim().split("\n");
  const want = sums.map((l) => l.split(/\s+/)).find((x) => x[1] === name + ".json");
  if (!want) throw new Error("no SHA-256 for " + name);
  const got = crypto.createHash("sha256").update(fs.readFileSync(p)).digest("hex");
  if (got !== want[0]) throw new Error("hash guard failed for " + name);
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

const V = readCanonical("schematic_values");
const T1 = readCanonical("table1");
// short model names from Table 1 (package table2_models.csv): text before the first comma, without a trailing
// parenthetical; a "<org>/<name> @<revision>" identifier is reduced to <name>
const models = Object.fromEntries(T1.models.map((m) => [m.arm.split(" ")[0],
  m.model.split(",")[0].replace(/ \(.*/, "").replace(/^.*\/([^ @]+).*$/, "$1")]));

// ------------------------------------------------------------------ geometry helpers (mm -> inch)
const MM = 1 / 25.4;
const W = 190, H = 162;
const NAVY = "2B3D6B", K = "1A1A1A", G4 = "4D4D4D", G6 = "6B6B6B", G8 = "8A8A8A", GB = "B3B3B3", FILL = "F2F2F2";
const pres = new pptxgen();
pres.defineLayout({ name: "JBI_FULL", width: W * MM, height: H * MM });
pres.layout = "JBI_FULL";
pres.author = "";
pres.company = "";
pres.title = "Figure 1";
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

function box(x, y, w, h, o = {}) {
  s.addShape(o.round ? pres.ShapeType.roundRect : pres.ShapeType.rect, {
    x: x * MM, y: y * MM, w: w * MM, h: h * MM,
    fill: { color: o.fill || "FFFFFF" },
    line: { color: o.line || G6, width: o.lw || 0.75, dashType: o.dash || "solid" },
    rectRadius: o.round ? 0.04 : undefined,
  });
}
function txt(x, y, w, h, runs, o = {}) {
  const arr = (Array.isArray(runs) ? runs : [runs]).map((r, i, a) => {
    const t = typeof r === "string" ? { text: r } : r;
    return {
      text: t.text,
      options: {
        bold: t.bold === true, color: t.color || o.color || K, fontSize: t.size || o.size || 8,
        breakLine: t.br === true || (o.lines === true && i < a.length - 1),
      },
    };
  });
  s.addText(arr, {
    x: x * MM, y: y * MM, w: w * MM, h: h * MM, fontFace: "Arial", margin: 0, fit: "none",
    align: o.align || "left", valign: o.valign || "top", lineSpacing: o.ls || 10, color: o.color || K,
  });
}
function line(x1, y1, x2, y2, o = {}) {
  s.addShape(pres.ShapeType.line, {
    x: Math.min(x1, x2) * MM, y: Math.min(y1, y2) * MM, w: Math.abs(x2 - x1) * MM, h: Math.abs(y2 - y1) * MM,
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: o.color || G6, width: o.lw || 0.75, dashType: o.dash || "solid",
            endArrowType: o.arrow ? "triangle" : undefined },
  });
}
function panel(label, heading, x, y) {
  txt(x + 0.8, y, 8, 5, [{ text: label, bold: true, size: 11 }]);
  txt(x + 8.6, y + 0.55, 110, 5, [{ text: heading, bold: true, size: 9 }]);
}

// ------------------------------------------------------------------ (A) data and analysis sets
const T0 = 0.8;                                    // top margin
panel("(A)", "Data and analysis sets", 0, T0);
box(2, T0 + 7, 64, 12.5, { fill: FILL, line: G6 });
txt(4, T0 + 8.2, 61, 11, [
  { text: `Representation set: ${V.n_representation} cases`, bold: true },
  { text: `Centres 2–5: ${V.centres_representation}` },
  { text: "E1, E3-site, PCA and LEACE fitting" }], { lines: true });
const kids = [
  { y: 22.5, t1: `Primary causal set (W = 30): ${V.n_primary} cases`, t2: V.centres_primary, prim: true },
  { y: 45.0, t1: `W = 5 set: ${V.n_W5} cases`, t2: `${V.centres_W5} · sensitivity` },
  { y: 55.5, t1: `W = 0 set: ${V.n_W0} cases`, t2: `${V.centres_W0} · sensitivity` },
];
const kh = 9;
line(6, T0 + 19.5, 6, T0 + kids[2].y + kh / 2, { color: G6 });
for (const k of kids) {
  line(6, T0 + k.y + kh / 2, 10, T0 + k.y + kh / 2, { color: G6 });
  box(10, T0 + k.y, 56, kh, { line: k.prim ? NAVY : G6, lw: k.prim ? 1.25 : 0.75 });
  txt(12, T0 + k.y + 0.95, 53, kh - 1, [{ text: k.t1, bold: true }, { text: k.t2 }], { lines: true });
}
line(14, T0 + 31.5, 14, T0 + 38.5, { color: G6 });
line(14, T0 + 38.5, 18, T0 + 38.5, { color: G6 });
box(18, T0 + 34, 48, kh, { line: G6 });
txt(20, T0 + 34.95, 45, kh - 1, [{ text: `Single-file subset: ${V.n_single} cases`, bold: true },
  { text: `${V.centres_single} · sensitivity` }], { lines: true });

// ------------------------------------------------------------------ (B) semi-synthetic design
panel("(B)", "Semi-synthetic design (one case, one replicate)", 72, T0);
const tx = 76, ty = T0 + 13, th = 8;
box(tx, ty, 28, th, { fill: FILL, line: G6 });
box(tx + 28, ty, 30, th, { fill: "FFFFFF", line: NAVY, lw: 1.25 });
box(tx + 58, ty, 26, th, { fill: FILL, line: G6 });
txt(tx, ty + 0.4, 28, th - 0.8, [{ text: "W pre-window" }, { text: "steps" }], { lines: true, align: "center", valign: "middle" });
txt(tx + 28, ty + 0.4, 30, th - 0.8, [{ text: "K window steps", bold: true, color: NAVY }, { text: "policy applied" }], { lines: true, align: "center", valign: "middle" });
txt(tx + 58, ty + 0.4, 26, th - 0.8, [{ text: "P post-window" }, { text: "steps" }], { lines: true, align: "center", valign: "middle" });
line(tx + 84, ty + th / 2, tx + 89, ty + th / 2, { color: G6, arrow: true });
box(tx + 89, ty + 1, 8, th - 2, { line: G6, dash: "dash" });
txt(tx + 89, ty + 1, 8, th - 2, [{ text: "Y", bold: true }], { align: "center", valign: "middle" });
txt(tx + 28, ty - 5.2, 70, 4.5, [{ text: `d(a) = δ·a, δ = ${V.delta}, at every window step`, color: NAVY }]);
txt(tx, ty + th + 1.2, 110, 4, [{ text: `1 step = ${V.step_seconds} s of video; W and P steps follow their natural course`, color: G4 }]);
txt(tx, ty + th + 6.4, 72, 33, [
  { text: "State S switches 0 → 1 at step s; window start" },
  { text: `w = s + O, site-stratified offset O: ${V.offsets}` },
  { text: `Grid: K: ${V.K} · P: ${V.P} · W: ${V.W}` },
  { text: `α (unmeasured confounding): ${V.alpha}` },
  { text: `γ (site loading): ${V.gamma}` },
  { text: `${V.n_cells_main} cells (+ ${V.phi_cells} with autoregressive actions)` },
  { text: `${V.M} synthetic replicates per cell; site` },
  { text: "loading c(C) permuted per replicate" }], { lines: true, ls: 10.5 });
// data-generating process (protocol §6): C -> A; S -> A, Y; U -> A, Y; A -> Y. C has no direct effect on Y.
const nd = { C: [155, 44], A: [170, 44], Y: [185, 44], S: [170, 31.5], U: [177.5, 56.5] };
const real = { C: true, S: true };
const R_ = 3.4;
function node(k) {
  const [cx, cy] = nd[k];
  s.addShape(pres.ShapeType.ellipse, { x: (cx - R_) * MM, y: (cy - R_) * MM, w: 2 * R_ * MM, h: 2 * R_ * MM,
    fill: { color: real[k] ? FILL : "FFFFFF" }, line: { color: real[k] ? K : G6, width: 0.75, dashType: real[k] ? "solid" : "dash" } });
  txt(cx - R_, cy - R_, 2 * R_, 2 * R_, [{ text: k, bold: true }], { align: "center", valign: "middle" });
}
function edge(a, b, col) {
  const [x1, y1] = nd[a], [x2, y2] = nd[b];
  const d = Math.hypot(x2 - x1, y2 - y1), ux = (x2 - x1) / d, uy = (y2 - y1) / d;
  line(x1 + ux * R_, y1 + uy * R_, x2 - ux * (R_ + 0.3), y2 - uy * (R_ + 0.3), { color: col || K, lw: 0.75, arrow: true });
}
edge("C", "A", NAVY); edge("S", "A"); edge("S", "Y"); edge("U", "A"); edge("U", "Y"); edge("A", "Y");
Object.keys(nd).forEach(node);
txt(149, 61.2, 40, 4, [{ text: "solid = data; dashed = synthetic", color: G4 }], { align: "right" });

// ------------------------------------------------------------------ (C) adjustment arms
const Y2 = 68.5;
panel("(C)", "Adjustment arms", 0, Y2);
const cols = [["C", 42], ["S", 51], ["U", 60], ["R", 69], ["R, site", 79.5]];
const hy = Y2 + 7.2;
for (const [c, x] of cols) txt(x - 6, hy, 12, 4, [{ text: c, bold: true }], { align: "center" });
txt(79.5 - 6.5, hy + 3.3, 13, 4, [{ text: "removed", bold: true }], { align: "center" });
txt(2, hy, 34, 4, [{ text: "Arm", bold: true }]);
line(0.8, hy + 7.4, 86, hy + 7.4, { color: K, lw: 0.75 });
const arms = [
  [["NV"], ""], [["SITE"], "C"], [["ORACLE−C"], "S"], [["ORACLE"], "SC"], [["FULL"], "SCU"],
  [["FM-P", "FM-S", "REF"], "R"], [["FM-P−C", "FM-S−C", "REF−C"], "X"], [["FM-P-nat"], "R"],
];
const armNames = new Set(T1.arms.flatMap((a) => a.arm.split(", ")));
const ry0 = hy + 8.1, rh = 3.45;
arms.forEach(([names, m], i) => {
  for (const a of names) if (!armNames.has(a)) throw new Error("arm not in protocol §8: " + a);
  const y = ry0 + i * rh;
  txt(2, y, 38, rh, [{ text: names.join(" · ") }], { valign: "middle" });
  const marks = { C: m.includes("C"), S: m.includes("S"), U: m.includes("U"), R: m === "R", "R, site": m === "X" };
  for (const [c, x] of cols) if (marks[c]) txt(x - 5, y, 10, rh, [{ text: "●" }], { align: "center", valign: "middle" });
  if (i === 4) line(0.8, y + rh, 86, y + rh, { color: GB, lw: 0.5 });
});
const tb = ry0 + arms.length * rh + 0.3;
line(0.8, tb, 86, tb, { color: K, lw: 0.75 });
txt(2, tb + 1.0, 84, 4, [{ text: "All arms also adjust for past synthetic actions H.", color: G4 }]);

// ------------------------------------------------------------------ (D) estimand, estimator, representations
panel("(D)", "Estimand, estimator and representations", 90, Y2);
txt(92, Y2 + 7.4, 97, 36, [
  { text: "Estimand. ", bold: true },
  { text: `Ψ(δ) − Ψ(1) for the multiplicative modified treatment policy d(a) = δ·a (δ = ${V.delta}) at each of the K window steps; true value exact for each replicate.`, br: true },
  { text: " ", size: 4, br: true },
  { text: "Estimator. ", bold: true },
  { text: `Sequentially doubly robust; nuisances cross-fitted over ${V.folds} case-level folds; 95% Wald intervals from the influence function.`, br: true },
  { text: " ", size: 4, br: true },
  { text: "Representations. ", bold: true },
  { text: `R = ${V.n_pcs} principal components per step from ${models["FM-P"]} (FM-P), ${models["FM-S"]} (FM-S) or ${models["REF"]} (REF); site removed by linear LEACE fitted on the ${V.n_representation}-case training folds; FM-P-nat uses native frames.` },
], { ls: 10.5 });

// ------------------------------------------------------------------ (E) workflow and registrations
const Y3 = 118.5;
panel("(E)", "Workflow and registrations", 0, Y3);
const steps = [
  ["Protocol frozen", V.protocol_frozen],
  ["Code lock", V.code_lock_date],
  ["Steps 4–5", "extraction; E1–E3", `records ${V.step5_record_date}`],
  ["Step 6: causal grid", `${V.step6_units} units`, `completed ${V.step6_completed}`],
  ["Step 7: family verdicts", `records ${V.step7_record_date}`],
];
const bw = 34.6, gap = 4.0, x0 = 0.4, by = Y3 + 11.0, bh = 12.2;
steps.forEach(([a, ...rest], i) => {
  const x = x0 + i * (bw + gap) - 0.2;
  box(x + 0.2, by, bw, bh, { line: i === 4 ? NAVY : G6, lw: i === 4 ? 1.25 : 0.75 });
  txt(x + 1.4, by + 1.0, bw - 2, bh - 1.2, [{ text: a, bold: true }, ...rest.map((t) => ({ text: t, color: G4 }))], { lines: true });
  if (i < 4) line(x + bw + 0.4, by + bh / 2, x + bw + gap - 0.2, by + bh / 2, { color: G6, arrow: true });
});
const ax0 = x0 + 2 * (bw + gap), ax1 = x0 + 4 * (bw + gap) + bw;
line(ax0, by - 2.2, ax1, by - 2.2, { color: G4, lw: 0.6 });
line(ax0, by - 2.2, ax0, by - 0.8, { color: G4, lw: 0.6 });
line(ax1, by - 2.2, ax1, by - 0.8, { color: G4, lw: 0.6 });
txt(ax0, by - 6.1, ax1 - ax0, 3.6, [{ text: "records committed automatically", color: G4 }], { align: "center" });
const ey = by + bh + 3.6, eh = 12.2;
txt(1.0, ey + 1.0, 2 * (bw + gap) + bw - 1, eh, [
  { text: "Exploratory analyses outside the protocol (dashed boxes);", color: G4 },
  { text: "plans registered on OSF: X1/X2 while step 6 was running,", color: G4 },
  { text: "before step-6 results were accessed; B after the step-7 verdicts", color: G4 }], { lines: true });
const xs = [x0 + 3 * (bw + gap), x0 + 4 * (bw + gap)];
const ex = [["X1/X2", V.x_plan_date, V.x_osf], ["B", V.b_plan_date, V.b_osf]];
ex.forEach(([a, d, u], i) => {
  box(xs[i], ey, bw, eh, { line: G6, dash: "dash" });
  txt(xs[i] + 1.2, ey + 1.0, bw - 2, eh - 1.2, [{ text: a, bold: true }, { text: `plan ${d}`, color: G4 },
    { text: u.replace("https://", ""), color: G4 }], { lines: true });
  line(xs[i] + bw / 2, by + bh, xs[i] + bw / 2, ey, { color: G6, dash: "dash", arrow: true });
});
if (ey + eh > H - 0.5) throw new Error("content below the canvas: " + (ey + eh));

pres.writeFile({ fileName: path.join(__dirname, "Figure_1.pptx") }).then((f) => console.log("written " + f));
