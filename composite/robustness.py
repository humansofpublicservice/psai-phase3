"""Composite-level robustness analysis for PSAI (Phase 3 reviewer aid).

Reads PSAI_CompositeScores_Rebuilt.xlsx (stdlib only), then:
  1. recomputes the composite with the published weights 30/28/22/15/5;
  2. for the states with a 0 in any dimension, recomputes with that dimension
     excluded and the remaining weights rescaled (the two bounds in Question 01);
  3. perturbs every weight by a random factor in [1-P, 1+P], renormalizes, and
     reports each state's rank interval and tier stability.

Usage: python3 robustness.py [--perturb 0.3] [--draws 2000] [--seed 20260801]
Prints JSON to stdout. Zeros are treated as scores, exactly as in the published
file; this script does not decide whether they should be.
"""
import argparse, json, random, re, statistics, zipfile, pathlib

W = [0.30, 0.28, 0.22, 0.15, 0.05]
TIERS = [(62.0, "Leading"), (57.0, "Strong"), (52.0, "Developing"), (47.0, "Emerging"), (-1e9, "Critical")]
# Tier cut points are the Dossier's published ones, applied to every scenario.


def load(path):
    x = zipfile.ZipFile(path).read("xl/worksheets/sheet1.xml").decode()
    out = {}
    for row in re.findall(r"<row[^>]*>(.*?)</row>", x, flags=re.S)[1:]:
        cells = dict((m[0], m[1]) for m in re.findall(r'<c r="([A-F])\d+"[^>]*>(?:<is><t[^>]*>([^<]*)</t></is>|<v>([^<]*)</v>)', row) and
                     [(a, b or c) for a, b, c in re.findall(r'<c r="([A-F])\d+"[^>]*>(?:<is><t[^>]*>([^<]*)</t></is>|<v>([^<]*)</v>)?', row)])
        out[cells["A"]] = [float(cells[k]) if cells.get(k) not in (None, "") else None for k in "BCDEF"]
    return out


def tier(s):
    return next(n for c, n in TIERS if s >= c)


def comp(v, w):
    return sum(a * b for a, b in zip(w, v))


def comp_excl(v, w):
    pairs = [(a, b) for a, b in zip(w, v) if b not in (None, 0.0)]
    return sum(a * b for a, b in pairs) / sum(a for a, _ in pairs)


def ranks(scores):
    order = sorted(scores, key=scores.get, reverse=True)
    return {s: i + 1 for i, s in enumerate(order)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perturb", type=float, default=0.3)
    ap.add_argument("--draws", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20260801)
    a = ap.parse_args()
    data = load(pathlib.Path(__file__).with_name("PSAI_CompositeScores_Rebuilt.xlsx"))
    states = sorted(data)
    base = {s: comp(data[s], W) for s in states}
    base_rank = ranks(base)
    base_tier = {s: tier(base[s]) for s in states}

    zero_cases = []
    for s in states:
        zs = [f"D{i+1}" for i, x in enumerate(data[s]) if x == 0.0]
        if zs:
            r = comp_excl(data[s], W)
            zero_cases.append({"state": s, "zero_dims": zs, "zero_fill": round(base[s], 1), "tier_zero_fill": base_tier[s],
                               "renormalized": round(r, 1), "tier_renormalized": tier(r)})

    rng = random.Random(a.seed)
    rk = {s: [] for s in states}
    same_tier = {s: 0 for s in states}
    for _ in range(a.draws):
        w = [x * rng.uniform(1 - a.perturb, 1 + a.perturb) for x in W]
        t = sum(w); w = [x / t for x in w]
        sc = {s: comp(data[s], w) for s in states}
        r = ranks(sc)
        for s in states:
            rk[s].append(r[s])
            same_tier[s] += tier(sc[s]) == base_tier[s]

    def pct(v, p):
        v = sorted(v); return v[min(len(v) - 1, int(p * len(v)))]

    per_state = [{"state": s, "composite": round(base[s], 1), "rank": base_rank[s], "tier": base_tier[s],
                  "rank_p5": pct(rk[s], .05), "rank_p95": pct(rk[s], .95), "rank_min": min(rk[s]), "rank_max": max(rk[s]),
                  "pct_draws_same_tier": round(100 * same_tier[s] / a.draws)} for s in sorted(states, key=base_rank.get)]

    # equal weights and influence
    eq = ranks({s: comp(data[s], [0.2] * 5) for s in states})
    n = len(states)
    rho = 1 - 6 * sum((base_rank[s] - eq[s]) ** 2 for s in states) / (n * (n * n - 1))
    infl = []
    for i in range(5):
        vals = [data[s][i] for s in states if data[s][i] is not None]
        infl.append({"dim": f"D{i+1}", "weight": W[i], "mean": round(statistics.mean(vals), 1), "sd": round(statistics.pstdev(vals), 1),
                     "weight_x_sd": round(W[i] * statistics.pstdev(vals), 2)})
    def corr(x, y):
        mx, my = statistics.mean(x), statistics.mean(y)
        return sum((p - mx) * (q - my) for p, q in zip(x, y)) / (sum((p - mx) ** 2 for p in x) * sum((q - my) ** 2 for q in y)) ** .5
    cm = [[round(corr([data[s][i] for s in states], [data[s][j] for s in states]), 2) for j in range(5)] for i in range(5)]
    print(json.dumps({"settings": vars(a), "zero_cases": zero_cases, "equal_weights_spearman": round(rho, 2),
                      "median_rank_range_p5_p95": statistics.median(p["rank_p95"] - p["rank_p5"] for p in per_state),
                      "median_pct_same_tier": statistics.median(p["pct_draws_same_tier"] for p in per_state),
                      "influence": infl, "correlations": cm, "per_state": per_state}, indent=1))

main()
