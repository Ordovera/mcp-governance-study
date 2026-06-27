"""
Compute agreement metrics for the n=100 sensitivity validation.

Reads validation-sensitivity-n100.json (per-row det_sensitivity vs human_sensitivity)
and re-derives the headline numbers + adds bootstrap 95% confidence intervals and
a per-det-category breakdown.

Output is a plain-text report on stdout. Stdlib only.

Usage:
  python3 compute-sensitivity-scores.py
  python3 compute-sensitivity-scores.py --bootstrap 10000 --seed 20260514
"""

import argparse
import json
import math
import random
from collections import Counter

from _repro import repo_data


def confusion(rows):
    """Return (tp, fp, fn, tn) treating 'sensitive' as the positive class."""
    tp = fp = fn = tn = 0
    for r in rows:
        d, h = r["det_sensitivity"], r["human_sensitivity"]
        if d == "sensitive" and h == "sensitive":
            tp += 1
        elif d == "sensitive" and h == "non-sensitive":
            fp += 1
        elif d == "non-sensitive" and h == "sensitive":
            fn += 1
        elif d == "non-sensitive" and h == "non-sensitive":
            tn += 1
    return tp, fp, fn, tn


def metrics(rows):
    tp, fp, fn, tn = confusion(rows)
    n = tp + fp + fn + tn
    if n == 0:
        return None
    p_o = (tp + tn) / n
    # marginals
    p1_s = (tp + fp) / n    # det's "sensitive" rate
    p1_n = (fn + tn) / n
    p2_s = (tp + fn) / n    # human's "sensitive" rate
    p2_n = (fp + tn) / n
    p_e = p1_s * p2_s + p1_n * p2_n
    kappa = (p_o - p_e) / (1 - p_e) if p_e < 1 else 1.0
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    f1 = (2 * precision * recall / (precision + recall)
          if precision and recall and (precision + recall) else None)
    return {
        "n": n, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "agreement": p_o, "kappa": kappa,
        "precision": precision, "recall": recall, "f1": f1,
    }


def percentile(sorted_vals, p):
    """Linear-interp percentile. p in [0, 1]."""
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * p
    lo = math.floor(k)
    hi = math.ceil(k)
    if lo == hi:
        return sorted_vals[int(k)]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def bootstrap_ci(rows, B, rng, stratified=True):
    """Return dict of percentile CIs for kappa, agreement, precision, recall, f1."""
    if stratified:
        sens_rows = [r for r in rows if r["det_sensitivity"] == "sensitive"]
        nonsens_rows = [r for r in rows if r["det_sensitivity"] == "non-sensitive"]
        n_s, n_n = len(sens_rows), len(nonsens_rows)

        def resample():
            return ([sens_rows[rng.randrange(n_s)] for _ in range(n_s)] +
                    [nonsens_rows[rng.randrange(n_n)] for _ in range(n_n)])
    else:
        n = len(rows)

        def resample():
            return [rows[rng.randrange(n)] for _ in range(n)]

    keys = ["kappa", "agreement", "precision", "recall", "f1"]
    samples = {k: [] for k in keys}
    for _ in range(B):
        m = metrics(resample())
        for k in keys:
            v = m.get(k)
            if v is not None:
                samples[k].append(v)

    ci = {}
    for k in keys:
        s = sorted(samples[k])
        if len(s) < B * 0.95:
            # too many bootstrap samples lacked a finite value -- report n
            ci[k] = {"lo": None, "hi": None, "valid_b": len(s)}
        else:
            ci[k] = {
                "lo": round(percentile(s, 0.025), 4),
                "hi": round(percentile(s, 0.975), 4),
                "valid_b": len(s),
            }
    return ci


def category_breakdown(rows):
    """Per-det-category precision (within the rows det classified as sensitive)."""
    sens = [r for r in rows if r["det_sensitivity"] == "sensitive"]
    by_cat = {}
    for r in sens:
        cat = r.get("det_category") or "unspecified"
        by_cat.setdefault(cat, []).append(r)

    report = {}
    for cat, group in by_cat.items():
        confirmed = sum(1 for r in group if r["human_sensitivity"] == "sensitive")
        n = len(group)
        report[cat] = {
            "n_det_predicted": n,
            "n_human_confirmed": confirmed,
            "precision_within_category": round(confirmed / n, 4) if n else None,
        }
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=None,
                    help="Validation sample JSON (default: the in-repo "
                         "data/validation/validation-sensitivity-n100.json)")
    ap.add_argument("--bootstrap", type=int, default=10000,
                    help="Number of bootstrap resamples (0 to skip)")
    ap.add_argument("--seed", type=int, default=20260514)
    ap.add_argument("--unstratified", action="store_true",
                    help="Use simple bootstrap instead of stratifying by det class")
    args = ap.parse_args()

    input_path = args.input or repo_data("validation", "validation-sensitivity-n100.json")
    data = json.load(open(input_path))
    rows = data["tools"]

    print("=" * 64)
    print(f"SENSITIVITY VALIDATION  --  {args.input}")
    print("=" * 64)
    print(f"Decision rule: {data.get('decisionRule', '(missing)')}")
    print()

    m = metrics(rows)
    print(f"N = {m['n']}")
    print(f"  Det predicted sensitive:     {m['tp'] + m['fp']}")
    print(f"  Det predicted non-sensitive: {m['fn'] + m['tn']}")
    print(f"  Human said sensitive:        {m['tp'] + m['fn']}")
    print(f"  Human said non-sensitive:    {m['fp'] + m['tn']}")
    print()
    print("Confusion matrix (rows=det, cols=human):")
    print(f"                 hum-sens  hum-nonsens")
    print(f"  det-sens       {m['tp']:>8}  {m['fp']:>11}")
    print(f"  det-nonsens    {m['fn']:>8}  {m['tn']:>11}")
    print()
    print(f"Agreement (p_o): {m['agreement']:.4f}")
    print(f"Cohen's kappa:   {m['kappa']:.4f}")
    print(f"Precision:       {m['precision']:.4f}  (det-sens correctly flagged)")
    print(f"Recall:          {m['recall']:.4f}  (human-sens caught by det)")
    print(f"F1:              {m['f1']:.4f}")
    print()

    # Bootstrap CIs
    if args.bootstrap > 0:
        rng = random.Random(args.seed)
        print(f"Bootstrap 95% CIs (B={args.bootstrap}, "
              f"{'stratified' if not args.unstratified else 'simple'}, "
              f"seed={args.seed}):")
        ci = bootstrap_ci(rows, args.bootstrap, rng, stratified=not args.unstratified)
        for k in ["kappa", "agreement", "precision", "recall", "f1"]:
            c = ci[k]
            if c["lo"] is None:
                print(f"  {k:<10} CI=(undefined; only {c['valid_b']} valid samples)")
            else:
                print(f"  {k:<10} 95% CI = [{c['lo']:.4f}, {c['hi']:.4f}]")
        print()

    # Per-category breakdown
    print("Per det-category precision (within det-sensitive predictions):")
    cats = category_breakdown(rows)
    print(f"  {'category':<18} {'n_det':>6} {'confirmed':>10} {'precision':>10}")
    for cat in sorted(cats):
        row = cats[cat]
        p = row["precision_within_category"]
        p_str = f"{p:.4f}" if p is not None else "--"
        print(f"  {cat:<18} {row['n_det_predicted']:>6} "
              f"{row['n_human_confirmed']:>10} {p_str:>10}")
    print()

    # Cross-check against stored metadata
    stored = data.get("agreement", {}).get("deterministic_vs_human", {})
    if stored:
        print("Cross-check vs stored metadata:")
        for k, v in [("kappa", "kappa"), ("agreement", "agreement"),
                     ("precision", "precision"), ("recall", "recall")]:
            sv = stored.get(v)
            cv = m.get(k)
            if sv is None or cv is None:
                continue
            ok = abs(sv - cv) < 0.01
            mark = "OK" if ok else "MISMATCH"
            print(f"  {k:<10} stored={sv}  computed={cv:.4f}  {mark}")


if __name__ == "__main__":
    main()
