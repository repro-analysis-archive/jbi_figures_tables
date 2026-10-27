#!/usr/bin/env python3
"""v8 revision of Supplementary Table S2 (task CC_TASK_JBI_tableS2_and_handoff_v8.md §1): Table_S2_v2 = Table_S2_v1
(build_tables.table3 with the number S2) with only the three cells whose 3-decimal display is "−0.000" shown as in
Table S4 v2 (the decimals needed to display the sign; exact values from checks.json / x1_e3.json, frozen in
canonical_supplement/validation.json → v8_negative_zero_S2) and the footnote of Table S4 v2's footnote a. Table S2
already uses the footnote letters a–i (a = the single-file set), so the same footnote carries the next letter, j.
Every other cell, rounding and footnote as v1 (checked by qa_tables_supp_v2.py).

    .venv/bin/python -I scripts/build_table_S2_v2.py
"""
import sys

sys.dont_write_bytecode = True

import hashlib  # noqa: E402
import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build_tables", HERE / "build_tables.py")
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
MINUS = "−"
NOTE = ("{sup:j}Shown with 4 decimals so that its sign is visible (3 decimals would display −0.000); all other values "
        "have 3 decimals.")


def main():
    vp = bt.ROOT / "canonical_supplement" / "validation.json"
    sums = dict(reversed(x.split()) for x in (bt.ROOT / "canonical_supplement/SHA256SUMS.txt").read_text().splitlines())
    assert hashlib.sha256(vp.read_bytes()).hexdigest() == sums["validation.json"], "hash guard failed: validation.json"
    s2 = json.loads(vp.read_text())["v8_negative_zero_S2"]
    assert len(s2) == 3 and all(r["decimals"] == 4 for r in s2)
    f3_v1, used = bt.f3, []

    def f3_sign(x):
        out = f3_v1(x)
        if out != MINUS + "0.000":
            return out
        hit = [r for r in s2 if r["value"] == x]
        assert len(hit) == 1, x
        used.append(hit[0]["row"])
        return hit[0]["display"] + "{sup:j}"

    bt.f3 = f3_sign
    try:
        rows = bt.table3(num="S2", stem="Table_S2_v2", extra_notes=[NOTE])
    finally:
        bt.f3 = f3_v1
    assert sorted(used) == sorted(r["row"] for r in s2), used
    print(f"Table_S2_v2: {len(rows)} rows; sign-visible cells: {used}")


if __name__ == "__main__":
    main()
