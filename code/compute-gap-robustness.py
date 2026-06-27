"""
Robustness checks on the accountability-gap pattern counts.

The existing compute-statistics.py reports gap prevalence with Wilson 95% CIs.
Wilson assumes iid observations -- but the corpus has multiple servers per owner,
and a single owner with many forks can inflate apparent prevalence. This script
adds three reviewer-facing robustness measurements:

  1. Owner-cluster bootstrap 95% CIs on each gap pattern's prevalence
     (more honest than Wilson when ownership clusters matter)
  2. Concentration: top-5 owner share of each gap pattern + Gini coefficient
     (answers "is this headline driven by one publisher?")
  3. Pattern co-occurrence: Jaccard similarity between server sets
     (answers "are these 7 patterns measuring 7 different things?")

Servers with unparseable owners (e.g., bare remote URLs) are treated as their
own singleton cluster -- the most conservative choice for the bootstrap.

Stdlib only. Output is plain text on stdout.

Usage:
  python3 compute-gap-robustness.py
  python3 compute-gap-robustness.py --bootstrap 10000 --seed 20260520
"""

import argparse
import json
import math
import random
from collections import Counter, defaultdict

from _repro import add_data_dir_arg, corpus_path, load_rgd


def owner_of(server):
    """Extract owner slug from source URL. Returns (owner, is_real_cluster).
    Servers without a parseable owner get a unique synthetic id so they
    cluster as singletons in the bootstrap."""
    src = server.get("source") or ""
    src = src.replace("git+https://github.com/", "").replace("https://github.com/", "")
    src = src.split("?")[0].rstrip("/")
    parts = src.split("/")
    if len(parts) >= 2 and parts[0] and not parts[0].startswith("http"):
        return parts[0].lower(), True
    # synthetic singleton id keyed off the server name
    return f"__singleton__::{server.get('name', src)}", False


def wilson_ci(successes, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return (p, max(0.0, center - margin), min(1.0, center + margin))


def percentile(sorted_vals, p):
    if not sorted_vals:
        return None
    k = (len(sorted_vals) - 1) * p
    lo = math.floor(k)
    hi = math.ceil(k)
    if lo == hi:
        return sorted_vals[int(k)]
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (k - lo)


def gini(counts):
    """Gini coefficient on a list of non-negative counts. 0 = uniform, ~1 = concentrated."""
    if not counts:
        return 0.0
    sorted_c = sorted(counts)
    n = len(sorted_c)
    s = sum(sorted_c)
    if s == 0:
        return 0.0
    cum = sum((i + 1) * v for i, v in enumerate(sorted_c))
    return (2 * cum) / (n * s) - (n + 1) / n


def cluster_bootstrap(servers_by_owner, owners, gap_patterns_per_server,
                      pattern, B, rng):
    """Resample owners with replacement; recompute prevalence per resample.

    servers_by_owner: dict[owner -> list of server indices]
    owners: list of owner ids (preserves the multiset of cluster sizes)
    gap_patterns_per_server: dict[server_idx -> set of patterns]
    pattern: pattern to compute prevalence for
    """
    n_owners = len(owners)
    samples = []
    for _ in range(B):
        # resample owners; concatenate their servers
        hits = 0
        total = 0
        for _ in range(n_owners):
            o = owners[rng.randrange(n_owners)]
            members = servers_by_owner[o]
            total += len(members)
            for s_idx in members:
                if pattern in gap_patterns_per_server[s_idx]:
                    hits += 1
        if total > 0:
            samples.append(hits / total)
    samples.sort()
    return samples


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="evidence_corpus_n1000.json")
    add_data_dir_arg(ap)
    ap.add_argument("--bootstrap", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20260520)
    ap.add_argument(
        "--recompute-gaps",
        action="store_true",
        help="Compute gaps from current tools via rerun-gap-detection.py instead "
             "of reading the stored accountabilityGaps snapshot. Use this on the "
             "post-PhaseB corpus, whose stored snapshot is stale for the 137 "
             "servers that gained tools.",
    )
    ap.add_argument(
        "--include-supp",
        action="store_true",
        help="When --recompute-gaps is set, also include LLM-supplementary tools "
             "in gap detection (otherwise det-only).",
    )
    args = ap.parse_args()

    resolved = corpus_path(args.input, args.data_dir)
    corpus = json.load(open(resolved))
    servers = corpus["servers"]
    N = len(servers)

    # Optional: source gaps from rerun-gap-detection.py in-process
    recomputed_gaps = None
    if args.recompute_gaps:
        rgd = load_rgd()
        replayed, _ = rgd.run(resolved, include_supp=args.include_supp)
        recomputed_gaps = replayed

    # Owner -> list of server indices
    servers_by_owner = defaultdict(list)
    real_cluster_count = 0
    for i, s in enumerate(servers):
        o, real = owner_of(s)
        servers_by_owner[o].append(i)
        if real:
            real_cluster_count += 1
    owners = list(servers_by_owner.keys())

    # Per-server set of gap patterns
    gap_patterns_per_server = {}
    pattern_to_servers = defaultdict(set)
    for i, s in enumerate(servers):
        if recomputed_gaps is not None:
            ps = {g["pattern"] for g in recomputed_gaps[i]}
        else:
            ps = {g["pattern"] for g in s.get("accountabilityGaps", [])}
        gap_patterns_per_server[i] = ps
        for p in ps:
            pattern_to_servers[p].add(i)

    # Pattern counts (servers exhibiting each pattern at least once)
    pattern_counts = {p: len(v) for p, v in pattern_to_servers.items()}
    sorted_patterns = sorted(pattern_counts, key=lambda p: -pattern_counts[p])

    print("=" * 72)
    print("GAP-PATTERN ROBUSTNESS CHECKS")
    print("=" * 72)
    print(f"Corpus: {args.input}")
    print(f"N servers: {N}")
    if recomputed_gaps is not None:
        supp_note = "det + LLM-supplementary tools" if args.include_supp else "det tools only"
        print(f"Gap source: recomputed via rerun-gap-detection.py ({supp_note})")
    else:
        print("Gap source: stored accountabilityGaps snapshot (pre-PhaseB if input is pre-PhaseB corpus)")
    print(f"Distinct owner clusters: {len(owners)} ({real_cluster_count} real, "
          f"{len(owners) - real_cluster_count} singleton/unparseable)")
    print()

    # ── 1. Cluster bootstrap vs Wilson ────────────────────────────────────
    print("=" * 72)
    print("1. CLUSTER-BOOTSTRAP 95% CI vs WILSON 95% CI")
    print("=" * 72)
    print("(Cluster resamples whole owners; Wilson assumes iid servers.)")
    print()
    rng = random.Random(args.seed)
    header = (f"{'pattern':<35} {'count':>6} "
              f"{'prev':>6} {'Wilson 95% CI':>17} {'Cluster 95% CI':>17}")
    print(header)
    print("-" * len(header))
    for p in sorted_patterns:
        c = pattern_counts[p]
        prev, wlo, whi = wilson_ci(c, N)
        samples = cluster_bootstrap(servers_by_owner, owners,
                                    gap_patterns_per_server,
                                    p, args.bootstrap, rng)
        if samples:
            clo = percentile(samples, 0.025)
            chi = percentile(samples, 0.975)
            cluster_str = f"[{clo*100:5.1f}%,{chi*100:5.1f}%]"
        else:
            cluster_str = "[--]"
        wilson_str = f"[{wlo*100:5.1f}%,{whi*100:5.1f}%]"
        print(f"{p:<35} {c:>6} {prev*100:>5.1f}% {wilson_str:>17} {cluster_str:>17}")
    print()

    # ── 2. Concentration: top-5 owners + Gini ─────────────────────────────
    print("=" * 72)
    print("2. OWNER CONCENTRATION PER GAP PATTERN")
    print("=" * 72)
    print("(Top-5 share answers: is the headline driven by one publisher?)")
    print("(Gini: 0 = spread evenly across owners; ~1 = concentrated.)")
    print()
    for p in sorted_patterns:
        owner_counts = Counter()
        for s_idx in pattern_to_servers[p]:
            o, _ = owner_of(servers[s_idx])
            owner_counts[o] += 1
        total = sum(owner_counts.values())
        if total == 0:
            continue
        top5 = owner_counts.most_common(5)
        top5_share = sum(c for _, c in top5) / total
        g = gini(list(owner_counts.values()))
        distinct = len(owner_counts)
        print(f"{p}  (n={total} servers across {distinct} owners)")
        print(f"  Top-5 share: {top5_share*100:.1f}%   Gini: {g:.3f}")
        for o, c in top5:
            label = o if not o.startswith("__singleton__::") else "(unparseable)"
            print(f"    {label:<30} {c:>3}  ({c/total*100:.1f}% of {p})")
        print()

    # ── 3. Co-occurrence Jaccard matrix ───────────────────────────────────
    print("=" * 72)
    print("3. PATTERN CO-OCCURRENCE (Jaccard similarity of server sets)")
    print("=" * 72)
    print("(0 = patterns flag disjoint servers; 1 = identical sets.)")
    print()
    pats = sorted_patterns
    # short labels for column headers
    short = {p: (p[:14] + "..") if len(p) > 16 else p for p in pats}
    header = f"{'':<35} " + " ".join(f"{short[p]:>16}" for p in pats)
    print(header)
    for p1 in pats:
        s1 = pattern_to_servers[p1]
        cells = []
        for p2 in pats:
            s2 = pattern_to_servers[p2]
            union = s1 | s2
            if not union:
                cells.append("    --")
            else:
                j = len(s1 & s2) / len(union)
                cells.append(f"{j:>5.2f}")
        print(f"{p1:<35} " + " ".join(f"{c:>16}" for c in cells))
    print()

    # Pairs with high co-occurrence
    print("Highest non-self Jaccard pairs (top 5):")
    pairs = []
    for i, p1 in enumerate(pats):
        for p2 in pats[i + 1:]:
            s1 = pattern_to_servers[p1]
            s2 = pattern_to_servers[p2]
            union = s1 | s2
            if not union:
                continue
            j = len(s1 & s2) / len(union)
            pairs.append((j, p1, p2, len(s1 & s2), len(union)))
    pairs.sort(reverse=True)
    for j, p1, p2, inter, union in pairs[:5]:
        print(f"  J={j:.2f}  {p1} ∩ {p2}: {inter} / {union}")


if __name__ == "__main__":
    main()
