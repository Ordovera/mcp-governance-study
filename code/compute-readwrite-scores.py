"""
Compute agreement metrics for the n=100 read/write validation (Section 3.5).

Reads validation-final-n100.json (per-tool heuristic / llm_reeval / human
read-write labels) and re-derives the three headline comparisons reported in the
paper's read/write validation table, with Cohen's kappa, agreement, a write-as-
positive confusion matrix, precision/recall/F1, and bootstrap 95% CIs.

The three comparisons (treating 'write' as the positive class):

  LLM (Opus) vs Human   n=100   agreement 97%   kappa 0.940
  Heuristic vs Human    n=75    agreement 76%   kappa 0.518
  Heuristic vs LLM      n=75    agreement 76%   kappa 0.520

The heuristic comparisons are n=75, not 100, because the deterministic keyword
heuristic abstains ('unknown') on 25 tools; rows are included in a comparison
only when BOTH labels are decisive read/write.

Output is a plain-text report on stdout. Stdlib only.

Usage:
  python3 compute-readwrite-scores.py
  python3 compute-readwrite-scores.py --bootstrap 10000 --seed 20260514
"""

import argparse
import json
import math
import random

from _repro import repo_data


DECISIVE = ("read", "write")
POSITIVE = "write"


def decisive_rows(rows, a_key, b_key):
    """Rows where both labels are decisive read/write (drops heuristic 'unknown')."""
    return [r for r in rows
            if r.get(a_key) in DECISIVE and r.get(b_key) in DECISIVE]


def confusion(rows, a_key, b_key):
    """Return (tp, fp, fn, tn) with a_key as predictor, b_key as reference,
    treating 'write' as the positive class."""
    tp = fp = fn = tn = 0
    for r in rows:
        a, b = r[a_key], r[b_key]
        if a == POSITIVE and b == POSITIVE:
            tp += 1
        elif a == POSITIVE and b != POSITIVE:
            fp += 1
        elif a != POSITIVE and b == POSITIVE:
            fn += 1
        else:
            tn += 1
    return tp, fp, fn, tn


def metrics(rows, a_key, b_key):
    tp, fp, fn, tn = confusion(rows, a_key, b_key)
    n = tp + fp + fn + tn
    if n == 0:
        return None
    p_o = (tp + tn) / n
    # marginals (Cohen's kappa, 2x2)
    p1_pos = (tp + fp) / n     # predictor's "write" rate
    p1_neg = (fn + tn) / n
    p2_pos = (tp + fn) / n     # reference's "write" rate
    p2_neg = (fp + tn) / n
    p_e = p1_pos * p2_pos + p1_neg * p2_neg
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


def bootstrap_ci(rows, a_key, b_key, B, rng, stratified=True):
    """Percentile CIs for kappa/agreement/precision/recall/f1. Stratified
    resampling holds the reference-label (b_key) class balance fixed."""
    if stratified:
        pos = [r for r in rows if r[b_key] == POSITIVE]
        neg = [r for r in rows if r[b_key] != POSITIVE]
        n_p, n_n = len(pos), len(neg)

        def resample():
            return ([pos[rng.randrange(n_p)] for _ in range(n_p)] +
                    [neg[rng.randrange(n_n)] for _ in range(n_n)])
    else:
        n = len(rows)

        def resample():
            return [rows[rng.randrange(n)] for _ in range(n)]

    keys = ["kappa", "agreement", "precision", "recall", "f1"]
    samples = {k: [] for k in keys}
    for _ in range(B):
        m = metrics(resample(), a_key, b_key)
        for k in keys:
            v = m.get(k)
            if v is not None:
                samples[k].append(v)

    ci = {}
    for k in keys:
        s = sorted(samples[k])
        if len(s) < B * 0.95:
            ci[k] = {"lo": None, "hi": None, "valid_b": len(s)}
        else:
            ci[k] = {
                "lo": round(percentile(s, 0.025), 4),
                "hi": round(percentile(s, 0.975), 4),
                "valid_b": len(s),
            }
    return ci


# (predictor_key, reference_key, label, stored-metadata key)
COMPARISONS = [
    ("llm_reeval", "human", "LLM (Opus) vs Human", "llm_vs_human"),
    ("heuristic", "human", "Heuristic vs Human", "heuristic_vs_human"),
    ("heuristic", "llm_reeval", "Heuristic vs LLM", "heuristic_vs_llm"),
]


def report_one(all_rows, a_key, b_key, label, args):
    rows = decisive_rows(all_rows, a_key, b_key)
    m = metrics(rows, a_key, b_key)

    print("-" * 64)
    print(f"{label}   (predictor={a_key}, reference={b_key})")
    print("-" * 64)
    dropped = len(all_rows) - len(rows)
    print(f"N = {m['n']}" + (f"  ({dropped} dropped: a label not read/write)"
                             if dropped else ""))
    print("Confusion matrix (rows=predictor, cols=reference; write=positive):")
    print(f"                 ref-write  ref-read")
    print(f"  pred-write     {m['tp']:>8}  {m['fp']:>8}")
    print(f"  pred-read      {m['fn']:>8}  {m['tn']:>8}")
    print()
    print(f"Agreement (p_o): {m['agreement']:.4f}")
    print(f"Cohen's kappa:   {m['kappa']:.4f}")
    if m["precision"] is not None:
        print(f"Precision:       {m['precision']:.4f}  (pred-write confirmed by reference)")
    if m["recall"] is not None:
        print(f"Recall:          {m['recall']:.4f}  (reference-write caught by predictor)")
    if m["f1"] is not None:
        print(f"F1:              {m['f1']:.4f}")
    print()

    if args.bootstrap > 0:
        rng = random.Random(args.seed)
        ci = bootstrap_ci(rows, a_key, b_key, args.bootstrap, rng,
                          stratified=not args.unstratified)
        print(f"Bootstrap 95% CIs (B={args.bootstrap}, "
              f"{'stratified' if not args.unstratified else 'simple'}, "
              f"seed={args.seed}):")
        for k in ["kappa", "agreement", "precision", "recall", "f1"]:
            c = ci[k]
            if c["lo"] is None:
                print(f"  {k:<10} CI=(undefined; only {c['valid_b']} valid samples)")
            else:
                print(f"  {k:<10} 95% CI = [{c['lo']:.4f}, {c['hi']:.4f}]")
        print()

    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default=None,
                    help="Validation sample JSON (default: the in-repo "
                         "data/validation/validation-final-n100.json)")
    ap.add_argument("--bootstrap", type=int, default=10000,
                    help="Number of bootstrap resamples (0 to skip)")
    ap.add_argument("--seed", type=int, default=20260514)
    ap.add_argument("--unstratified", action="store_true",
                    help="Use simple bootstrap instead of stratifying by reference class")
    args = ap.parse_args()

    input_path = args.input or repo_data("validation", "validation-final-n100.json")
    data = json.load(open(input_path))
    rows = data["tools"]

    print("=" * 64)
    print("READ/WRITE VALIDATION")
    print("=" * 64)
    print(f"Decision rule: {data.get('decisionRule', '(missing)')}")
    print(f"Sample: {data.get('sample', {})}")
    print()

    computed = {}
    for a_key, b_key, label, stored_key in COMPARISONS:
        computed[stored_key] = report_one(rows, a_key, b_key, label, args)

    # Cross-check against the stored agreement block.
    stored = data.get("agreement", {})
    if stored:
        print("=" * 64)
        print("Cross-check vs stored agreement metadata")
        print("=" * 64)
        for _, _, label, stored_key in COMPARISONS:
            s = stored.get(stored_key, {})
            m = computed[stored_key]
            if not s or m is None:
                continue
            checks = [("n", s.get("n"), m["n"]),
                      ("agreement", s.get("agreement"), m["agreement"]),
                      ("kappa", s.get("kappa"), m["kappa"])]
            parts = []
            ok_all = True
            for name, sv, cv in checks:
                if sv is None:
                    continue
                tol = 0 if name == "n" else 0.01
                ok = abs(sv - cv) <= tol
                ok_all = ok_all and ok
                cv_str = f"{cv}" if name == "n" else f"{cv:.4f}"
                parts.append(f"{name}: stored={sv} computed={cv_str}")
            mark = "OK" if ok_all else "MISMATCH"
            print(f"  {label:<22} {mark}")
            for p in parts:
                print(f"      {p}")


if __name__ == "__main__":
    main()
