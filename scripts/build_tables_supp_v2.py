#!/usr/bin/env python3
"""v7 revision of Supplementary Tables S3 and S4 (task CC_TASK_JBI_GA_and_tables_v7.md §2): Table_S3_v2 and
Table_S4_v2 = the v1 tables (build_tables_supp_v1.py) with only the five cells whose committed 3-decimal display is
"−0.000" shown with the decimals needed to display their sign (the Table 2 rule of v4; exact values and displays
frozen in canonical_supplement/validation.json → v7_negative_zero_S3_S4 by freeze_supplement.py), a footnote marker on
each of them, and the footnote: the Table 2 wording added; in S4 the v1 sentence about −0.000 removed. Every other cell,
rounding, width and footnote as v1 (checked by qa_tables_supp_v2.py).

    .venv/bin/python -I scripts/build_tables_supp_v2.py
"""
import sys

sys.dont_write_bytecode = True

import importlib.util  # noqa: E402
import json  # noqa: E402
from pathlib import Path  # noqa: E402

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build_tables_supp_v1", HERE / "build_tables_supp_v1.py")
b1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b1)
MINUS = "−"


def main():
    val = json.loads((b1.ROOT / "canonical_supplement" / "validation.json").read_text())
    hashes = dict(reversed(x.split()) for x in (b1.ROOT / "canonical_supplement/SHA256SUMS.txt").read_text().splitlines())
    import hashlib
    assert hashlib.sha256((b1.ROOT / "canonical_supplement/validation.json").read_bytes()).hexdigest() == hashes[
        "validation.json"], "hash guard failed: validation.json"
    nz = val["v7_negative_zero_S3_S4"]
    assert len(nz) == 5 and all(r["decimals"] == 4 for r in nz)
    f3_v1 = b1.f3
    used = []

    def f3_sign(s):
        """v1 formatting, except a value whose 3-decimal string is −0.000: its recorded sign-visible display + marker."""
        out = f3_v1(s)
        if out != MINUS + "0.000":
            return out
        x = float(s)
        hit = [r for r in nz if r["value"] == x and r["table"] == table]
        assert len(hit) == 1, (table, s)
        used.append((table, hit[0]["row"], hit[0]["field"]))
        return hit[0]["display"] + "{sup:a}"

    b1.f3 = f3_sign
    try:
        table = "S3"
        n3 = b1.table_s3(stem="Table_S3_v2", extra_notes=[
            "{sup:a}Mean Δ shown with 4 decimals so that its sign is visible (3 decimals would display −0.000); all other "
            "values have 3 decimals."])
        table = "S4"
        n4 = b1.table_s4(stem="Table_S4_v2", negzero_sentence="", extra_notes=[
            "{sup:a}Shown with 4 decimals so that its sign is visible (3 decimals would display −0.000); all other values "
            "have 3 decimals."])
    finally:
        b1.f3 = f3_v1
    assert sorted(used) == sorted((r["table"], r["row"], r["field"]) for r in nz), used
    print(f"Table_S3_v2: {n3} rows, Table_S4_v2: {n4} rows; sign-visible cells: {len(used)}")
    for t, r, f in used:
        print(f"  {t}: {r} [{f}]")


if __name__ == "__main__":
    main()
