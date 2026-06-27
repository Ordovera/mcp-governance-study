"""
Compute governance posture scores for the N=945 corpus.

Model A: Simple additive (Present=1, Absent=0, Indeterminate=excluded). Score 0-10.
Model C: Plane subscores (Enforcement 1x, Evidence 2x). Plus overall weighted.
"""

import argparse
import json
import math
from collections import Counter

from _repro import add_data_dir_arg, corpus_path

_args = add_data_dir_arg(argparse.ArgumentParser()).parse_args()
corpus = json.load(open(corpus_path("evidence_corpus_n1000.json", _args.data_dir)))
servers = corpus["servers"]
source = [s for s in servers if s.get("stratum") != "remote-only"]

ENFORCEMENT = [
    "authentication", "perToolAuth", "confirmationGates",
    "stagedExecution", "rateLimiting", "leastPrivilege",
]
EVIDENCE = ["auditLogging", "actorAttribution"]
ALL_SCORED = ENFORCEMENT + EVIDENCE


def score_additive(indicators):
    present = sum(1 for k in ALL_SCORED if indicators.get(k) == "Present")
    assessable = sum(1 for k in ALL_SCORED if indicators.get(k) in ("Present", "Absent"))
    return round(present / assessable * 10, 2) if assessable > 0 else None


def score_planes(indicators):
    def plane_score(keys):
        p = sum(1 for k in keys if indicators.get(k) == "Present")
        a = sum(1 for k in keys if indicators.get(k) in ("Present", "Absent"))
        return round(p / a * 10, 2) if a > 0 else None

    enf = plane_score(ENFORCEMENT)
    evi = plane_score(EVIDENCE)

    if enf is not None and evi is not None:
        wp = sum(1 for k in ENFORCEMENT if indicators.get(k) == "Present") + \
             sum(1 for k in EVIDENCE if indicators.get(k) == "Present") * 2
        wt = sum(1 for k in ENFORCEMENT if indicators.get(k) in ("Present", "Absent")) + \
             sum(1 for k in EVIDENCE if indicators.get(k) in ("Present", "Absent")) * 2
        overall = round(wp / wt * 10, 2) if wt > 0 else None
    else:
        overall = enf
    return {"enforcement": enf, "evidence": evi, "overall": overall}


# Compute all scores
results = []
for s in source:
    ind = s.get("indicators", {})
    a = score_additive(ind)
    p = score_planes(ind)
    results.append({"additive": a, **p, "stratum": s.get("stratum"),
                     "has_gap": len(s.get("accountabilityGaps", [])) > 0})

scored = [r for r in results if r["additive"] is not None]


def stats(vals):
    s = sorted(vals)
    n = len(s)
    return {"n": n, "mean": round(sum(s)/n, 2), "median": s[n//2],
            "q1": s[n//4], "q3": s[3*n//4], "min": s[0], "max": s[-1],
            "sd": round(math.sqrt(sum((x - sum(s)/n)**2 for x in s) / n), 2)}


# ─── Model A ──────────────────────────────────────────────────
print("=" * 60)
print("MODEL A: SIMPLE ADDITIVE (0-10)")
print("=" * 60)
a_vals = [r["additive"] for r in scored]
st = stats(a_vals)
print(f"N={st['n']}, Mean={st['mean']}, SD={st['sd']}")
print(f"Median={st['median']}, IQR=[{st['q1']}, {st['q3']}]")
print(f"Range=[{st['min']}, {st['max']}]")

print("\nHistogram (1-point bins):")
bins = [0] * 11
for v in a_vals:
    bins[min(10, int(v))] += 1
max_bar = max(bins)
for i, count in enumerate(bins):
    bar = "#" * int(count / max(1, max_bar) * 40)
    print(f"  {i:>2}: {count:>4} ({count/len(a_vals)*100:>4.0f}%) {bar}")

# Tercile clusters
low = sum(1 for v in a_vals if v <= 2.5)
mid = sum(1 for v in a_vals if 2.5 < v <= 5.0)
high = sum(1 for v in a_vals if v > 5.0)
print(f"\nClusters: Low(0-2.5)={low} ({low/len(a_vals)*100:.0f}%), "
      f"Mid(2.5-5)={mid} ({mid/len(a_vals)*100:.0f}%), "
      f"High(5-10)={high} ({high/len(a_vals)*100:.0f}%)")


# ─── Model C ──────────────────────────────────────────────────
print(f"\n{'=' * 60}")
print("MODEL C: PLANE SUBSCORES")
print("=" * 60)

for label, key in [("Enforcement", "enforcement"), ("Evidence", "evidence"),
                    ("Overall (evidence 2x)", "overall")]:
    vals = [r[key] for r in scored if r[key] is not None]
    if not vals:
        continue
    st = stats(vals)
    print(f"\n{label} (N={st['n']}):")
    print(f"  Mean={st['mean']}, SD={st['sd']}, Median={st['median']}")
    print(f"  IQR=[{st['q1']}, {st['q3']}], Range=[{st['min']}, {st['max']}]")

# Evidence histogram
print("\nEvidence score distribution:")
evi_vals = [r["evidence"] for r in scored if r["evidence"] is not None]
evi_bins = [0] * 11
for v in evi_vals:
    evi_bins[min(10, int(v))] += 1
for i, count in enumerate(evi_bins):
    bar = "#" * int(count / max(1, max(evi_bins)) * 40)
    print(f"  {i:>2}: {count:>4} ({count/len(evi_vals)*100:>4.0f}%) {bar}")


# ─── Enforcement vs Evidence cross-tab ────────────────────────
print(f"\n{'=' * 60}")
print("ENFORCEMENT vs EVIDENCE CROSS-TAB")
print("=" * 60)

def tier(v):
    if v <= 3.3: return "Low"
    if v <= 6.6: return "Mid"
    return "High"

cross = Counter()
for r in scored:
    if r["enforcement"] is None or r["evidence"] is None:
        continue
    cross[(tier(r["enforcement"]), tier(r["evidence"]))] += 1

print(f"\n{'':>12} Evi-Low  Evi-Mid Evi-High")
for et in ["Low", "Mid", "High"]:
    row = f"  Enf-{et:>4}"
    for evt in ["Low", "Mid", "High"]:
        row += f" {cross.get((et, evt), 0):>8}"
    print(row)


# ─── By stratum ──────────────────────────────────────────────
print(f"\n{'=' * 60}")
print("SCORES BY STRATUM")
print("=" * 60)

by_stratum = {}
for r in scored:
    st = r["stratum"]
    if st not in by_stratum:
        by_stratum[st] = {"a": [], "enf": [], "evi": []}
    by_stratum[st]["a"].append(r["additive"])
    if r["enforcement"] is not None:
        by_stratum[st]["enf"].append(r["enforcement"])
    if r["evidence"] is not None:
        by_stratum[st]["evi"].append(r["evidence"])

print(f"\n{'Stratum':<20} {'N':>4} {'Add':>6} {'Enf':>6} {'Evi':>6}")
print("-" * 46)
for st in sorted(by_stratum):
    v = by_stratum[st]
    n = len(v["a"])
    a = sum(v["a"])/n if n else 0
    e = sum(v["enf"])/len(v["enf"]) if v["enf"] else 0
    ev = sum(v["evi"])/len(v["evi"]) if v["evi"] else 0
    print(f"{st:<20} {n:>4} {a:>6.2f} {e:>6.2f} {ev:>6.2f}")


# ─── Score vs gap presence ────────────────────────────────────
print(f"\n{'=' * 60}")
print("SCORE vs GAP PRESENCE")
print("=" * 60)
gap_scores = [r["additive"] for r in scored if r["has_gap"]]
nogap_scores = [r["additive"] for r in scored if not r["has_gap"]]
if gap_scores and nogap_scores:
    print(f"With gaps (N={len(gap_scores)}): mean={sum(gap_scores)/len(gap_scores):.2f}")
    print(f"Without gaps (N={len(nogap_scores)}): mean={sum(nogap_scores)/len(nogap_scores):.2f}")
