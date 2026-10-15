"""Precomputed composite alternatives for PSAI (Phase 3 reviewer aid).

For every state, prints the composite and tier under:
  published   - published weights 30/28/22/15/5, zeros kept (as in the workbook)
  zero_dropped- states with a 0 in one dimension: that dimension dropped, weights rescaled
  equal       - equal weights (20 each), zeros kept
  drop_D1..D5 - each dimension dropped in turn, remaining weights rescaled

Usage: python3 alternatives.py > alternatives.csv   (standard library only)
Reuses load(), tier() and the published weights from robustness.py.
"""
import csv, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from robustness import load, tier, comp, comp_excl, W

data = load(pathlib.Path(__file__).with_name("PSAI_CompositeScores_Rebuilt.xlsx"))
cols = ["state", "d1", "d2", "d3", "d4", "d5", "published", "published_tier", "zero_dropped", "zero_dropped_tier",
        "equal_weights", "equal_weights_tier"]
for i in range(1, 6):
    cols += [f"drop_D{i}", f"drop_D{i}_tier"]
w = csv.writer(sys.stdout, lineterminator="\n")
w.writerow(cols)
for s in sorted(data):
    v = data[s]
    pub = comp(v, W)
    has_zero = any(x in (None, 0.0) for x in v)
    zd = comp_excl(v, W) if has_zero else None
    eq = comp(v, [0.2] * 5)
    row = [s] + [f"{x:.1f}" if x is not None else "" for x in v]
    row += [f"{pub:.1f}", tier(pub), f"{zd:.1f}" if zd is not None else "", tier(zd) if zd is not None else "",
            f"{eq:.1f}", tier(eq)]
    for i in range(5):
        ww = [x if j != i else 0 for j, x in enumerate(W)]
        t = sum(ww)
        d = sum(a * b for a, b in zip(ww, v) if b is not None) / t
        row += [f"{d:.1f}", tier(d)]
    w.writerow(row)
