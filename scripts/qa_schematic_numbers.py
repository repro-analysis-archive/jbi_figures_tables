#!/usr/bin/env python3
"""Schematic number QA (figure template §15-3): every number printed in Figure 1 and the graphical abstract must be a
canonical value (schematic_values.json, table1.json, ga_values.json) or a listed structural label with its source.

    .venv/bin/python -I scripts/qa_schematic_numbers.py
"""
import sys

sys.dont_write_bytecode = True

import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

import pymupdf  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NUM = re.compile(r"(?<![A-Za-z\d])[−-]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?")   # thousands groups only (73,200)

# structural labels (not data values): name -> source
STRUCTURAL = {
    "4": "protocol §14 step number (steps 4–5)", "5": "protocol §14 step number (steps 4–5); also step = 5 s",
    "6": "protocol §14 step number", "7": "protocol §14 step number",
    "2": "centre labels 2–5 (protocol §2)", "1": "check / family labels E1, P1a, P1b; d(a) at δ = 1 baseline Ψ(1); "
    "state 0 → 1", "0": "state S switches 0 → 1 (protocol §2); P > 0", "3": "check label E3",
    "95": "95% Wald intervals (protocol §9)", "8": "model name CV8x8x8 (Table 1 B)", "4ch": "model name LeanVAE-4ch",
}


def tokens_of(obj):
    out = set()
    if isinstance(obj, dict):
        for v in obj.values():
            out |= tokens_of(v)
    elif isinstance(obj, list):
        for v in obj:
            out |= tokens_of(v)
    else:
        out |= {t.replace("−", "-") for t in NUM.findall(str(obj))}
    return out


def main():
    canon = set()
    for n in ("schematic_values", "table1", "ga_values"):
        canon |= tokens_of(json.loads((ROOT / "canonical" / f"{n}.json").read_text()))
    report = {}
    ok = True
    v2 = "--v2" in sys.argv[1:]
    targets = ((("Figure_1_v2", "figures_v2/Figure_1/Figure_1_v2.pdf"),
                ("Graphical_abstract_v2", "graphical_abstract/Graphical_abstract_v2.pdf")) if v2 else
               (("Figure_1", "figures/Figure_1/Figure_1.pdf"),
                ("Graphical_abstract", "graphical_abstract/Graphical_abstract.pdf")))
    for name, pdf in targets:
        text = pymupdf.open(ROOT / pdf)[0].get_text()
        found = [t.replace("−", "-") for t in NUM.findall(text)]
        rows = []
        for t in sorted(set(found), key=lambda x: (len(x), x)):
            if t in canon:
                src = "canonical"
            elif t.lstrip("-") in STRUCTURAL:
                src = "structural: " + STRUCTURAL[t.lstrip("-")]
            else:
                src = "UNMATCHED"
                ok = False
            rows.append(dict(token=t, count=found.count(t), source=src))
        report[name] = rows
        un = [r["token"] for r in rows if r["source"] == "UNMATCHED"]
        print(f"{name}: {len(found)} numeric tokens, {len(rows)} distinct; canonical "
              f"{sum(r['source'] == 'canonical' for r in rows)}, structural "
              f"{sum(r['source'].startswith('structural') for r in rows)}, unmatched {un}")
    (ROOT / "qa" / ("schematic_numbers_v2.json" if v2 else "schematic_numbers.json")).write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
