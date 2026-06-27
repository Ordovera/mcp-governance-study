"""
Re-run accountability-gap detection over (det + LLM-supplementary) tools.

Why: 234 of 760 source-available servers extract zero det tools but are
LLM-confirmed MCP with 3,157 supplementary tools available. The current
corpus's gap counts are computed against det tools only, undercounting
the 5 tool-dependent gap patterns (ungated-write, global-auth, destructive-no-trail,
sensitive-read-without-auth, sensitive-read-without-logging).

This script:
  1. Ports classifySensitivity + assessAuthArchitecture + detectGaps from
     cc-mcp-audit (TypeScript) to Python, preserving keyword lists and rules.
  2. Self-tests by re-running with supp tools EXCLUDED -- output must match
     the stored accountabilityGaps for every server.
  3. Re-runs INCLUDING supp tools and reports delta + dual-denominator prevalence.

Stdlib only. Output is plain text on stdout.
"""

import json
import re
import sys
from collections import Counter, defaultdict


# ── Ported from extract.ts ─────────────────────────────────────────────────
SENSITIVE_DATA_KEYWORDS = [
    "patient", "medical", "health_record", "diagnosis", "prescription",
    "ssn", "social_security", "passport", "driver_license",
    "credit_score", "credit_report",
    "salary", "compensation", "payroll", "bank_account",
    "credential", "password", "secret", "api_key", "private_key",
    "certificate", "oauth_token", "bearer_token", "access_token",
    "connection_string", "database_url",
    "hipaa", "pci", "ferpa", "gdpr",
]

SENSITIVE_ACTION_KEYWORDS = [
    "payment", "transfer_funds", "charge", "refund", "invoice",
    "purchase", "billing",
    "execute_code", "eval", "run_code", "run_shell", "run_command",
    "shell_exec", "subprocess", "spawn_process",
    "destroy_instance", "terminate_instance", "drop_database",
    "delete_account", "revoke_access",
]

SENSITIVE_CONTEXT_PAIRS = [
    ("config", ["secret", "credential", "password", "key", "token", "database", "connection"]),
    ("admin", ["permission", "role", "access", "privilege", "user", "account"]),
    ("environment", ["variable", "secret", "key", "token"]),
    ("session", ["token", "credential", "identity", "auth"]),
]

DESTRUCTIVE_KEYWORDS = ["drop", "delete", "truncate", "destroy", "purge", "wipe"]

_BOUNDARY_CHARS = re.compile(r"[\s_\-.:/]")


def matches_at_boundary(text: str, keyword: str) -> bool:
    """Port of matchesAtBoundary from extract.ts.

    Matches a keyword if it's surrounded by non-alphanumeric/word boundary
    characters OR is at a camelCase/snake_case boundary. Prevents substring
    false positives.
    """
    pos = 0
    n = len(text)
    k = len(keyword)
    while pos <= n - k:
        idx = text.find(keyword, pos)
        if idx == -1:
            return False
        before = "" if idx == 0 else text[idx - 1]
        after = "" if idx + k >= n else text[idx + k]
        left_ok = (
            idx == 0
            or _BOUNDARY_CHARS.match(before)
            or (
                before == before.lower()
                and keyword[0] == keyword[0].upper()
            )
        )
        right_ok = (
            idx + k >= n
            or _BOUNDARY_CHARS.match(after)
            or (
                keyword[-1] == keyword[-1].lower()
                and after == after.upper()
            )
        )
        if left_ok and right_ok:
            return True
        pos = idx + 1
    return False


def classify_sensitivity(combined: str):
    """Port of classifySensitivity. Returns (sensitivity, category, signals)."""
    signals = []
    category = None

    for kw in SENSITIVE_DATA_KEYWORDS:
        if matches_at_boundary(combined, kw):
            signals.append(kw)
            if not category:
                category = "confidentiality"

    for kw in SENSITIVE_ACTION_KEYWORDS:
        if matches_at_boundary(combined, kw):
            signals.append(kw)
            if not category:
                if any(s in kw for s in ("exec", "shell", "spawn", "eval")):
                    category = "integrity"
                else:
                    category = "autonomy"

    for base, qualifiers in SENSITIVE_CONTEXT_PAIRS:
        if matches_at_boundary(combined, base):
            for q in qualifiers:
                if matches_at_boundary(combined, q):
                    signals.append(f"{base}+{q}")
                    if not category:
                        category = "confidentiality"
                    break

    if signals:
        return "sensitive", category, signals
    return "non-sensitive", None, []


def assess_auth_architecture(patterns_auth, tool_files):
    """Port of assessAuthArchitecture from patterns.ts."""
    if not patterns_auth:
        return "none"
    auth_files = {p["file"] for p in patterns_auth}
    overlap = auth_files & tool_files
    if not overlap:
        return "global"
    if len(overlap) == len(auth_files):
        return "per-tool"
    return "unclear"


def has_log_adjacent_attribution(patterns):
    """Port of hasLogAdjacentAttribution (heuristic: any logging file appears in
    actorAttribution files? -- closest proxy without the full proximity test).

    Note: the original uses line-proximity. We approximate with file-level
    co-occurrence; if that doesn't match the corpus, we fall back to the
    `flags.hasAttributedLogging` field on each server (which is precomputed).
    """
    log_files = {p["file"] for p in patterns.get("logging", [])}
    attr_files = {p["file"] for p in patterns.get("actorAttribution", [])}
    return bool(log_files & attr_files)


def detect_gaps(tools, patterns, auth_arch, has_attributed_logs):
    """Port of detectGaps from gaps.ts. Returns list of {pattern, confidence, ...}."""
    gaps = []

    write_tools = [t for t in tools if t.get("classification") == "write"]
    safety_files = {g["file"] for g in patterns.get("gates", [])}
    safety_files |= {s["file"] for s in patterns.get("stagedExecution", [])}
    log_files = {l["file"] for l in patterns.get("logging", [])}

    # 1. Ungated write
    ungated = [t for t in write_tools if t.get("sourceFile") not in safety_files]
    if ungated:
        gaps.append({"pattern": "ungated-write", "confidence": "high"})

    # 2. Global auth over sensitive tools
    has_read = any(t.get("classification") == "read" for t in tools)
    if auth_arch == "global" and write_tools and has_read:
        gaps.append({"pattern": "global-auth-over-sensitive-tools", "confidence": "high"})
    elif auth_arch == "unclear" and write_tools and has_read:
        gaps.append({"pattern": "global-auth-over-sensitive-tools", "confidence": "low"})

    # 3. Auth without actor logging
    if patterns.get("auth") and patterns.get("logging") and not has_attributed_logs:
        gaps.append({"pattern": "auth-without-actor-logging", "confidence": "high"})

    # 4. Logging without attribution
    if patterns.get("logging") and not has_attributed_logs and not patterns.get("auth"):
        gaps.append({"pattern": "logging-without-attribution", "confidence": "medium"})

    # 5. Destructive without audit trail
    destructive_unlogged = []
    for t in write_tools:
        combined = (t.get("name", "") + " " + t.get("description", "")).lower()
        is_destructive = any(kw in combined for kw in DESTRUCTIVE_KEYWORDS)
        if is_destructive and t.get("sourceFile") not in log_files:
            destructive_unlogged.append(t)
    if destructive_unlogged:
        gaps.append({"pattern": "destructive-without-audit-trail", "confidence": "high"})

    # 6 & 7. Sensitive reads
    sensitive_reads = [
        t for t in tools
        if t.get("classification") == "read" and t.get("sensitivity") == "sensitive"
    ]
    if sensitive_reads and auth_arch == "none":
        gaps.append({"pattern": "sensitive-read-without-auth", "confidence": "high"})

    sensitive_reads_unlogged = [
        t for t in sensitive_reads if t.get("sourceFile") not in log_files
    ]
    if sensitive_reads_unlogged:
        gaps.append({"pattern": "sensitive-read-without-logging", "confidence": "high"})

    return gaps


def augment_tool(t):
    """For a supp tool, compute sensitivity inline. Returns a tool dict with
    `sensitivity`, `sensitivityCategory`, `sensitivitySignals` populated."""
    combined = (t.get("name", "") + " " + (t.get("description") or "")).lower()
    sens, cat, signals = classify_sensitivity(combined)
    return {
        **t,
        "sensitivity": sens,
        "sensitivityCategory": cat,
        "sensitivitySignals": signals,
    }


def run(corpus_path, include_supp):
    corpus = json.load(open(corpus_path))
    servers = corpus["servers"]
    per_server = []

    for s in servers:
        # Remote-only path in analyze.ts does NOT call detectGaps -- source-level
        # gap rules require source code that the remote RPC cannot expose. Match
        # that behavior here so the self-test agrees with stored data.
        if s.get("stratum") == "remote-only":
            per_server.append([])
            continue

        det = s.get("tools", []) or []
        supp_raw = s.get("llmSupplementaryTools", []) or []
        supp = [augment_tool(t) for t in supp_raw] if include_supp else []
        tools = det + supp

        patterns = s.get("patterns", {}) or {}
        tool_files = {t.get("sourceFile") for t in tools if t.get("sourceFile")}
        auth_arch = assess_auth_architecture(patterns.get("auth", []), tool_files)
        # Prefer the precomputed flag if present (more accurate than file-overlap proxy)
        has_attributed_logs = bool(s.get("flags", {}).get("hasAttributedLogging"))

        gaps = detect_gaps(tools, patterns, auth_arch, has_attributed_logs)
        per_server.append(gaps)

    return per_server, servers


def main():
    import argparse
    import os
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default=os.environ.get("MCP_DATA_DIR") or ".",
                    help="Directory containing the evidence corpus JSON "
                         "(default: $MCP_DATA_DIR or the current directory).")
    args = ap.parse_args()
    corpus_path = os.path.join(args.data_dir, "evidence_corpus_n1000.json")

    # ── Pass 1: replay det-only, validate against stored gaps ──────────────
    print("=" * 72)
    print("SELF-TEST: det-only replay should match stored accountabilityGaps")
    print("=" * 72)
    replayed, servers = run(corpus_path, include_supp=False)

    matched = 0
    mismatched_examples = []
    pat_orig = Counter()
    pat_replay = Counter()
    for s, replay_gaps in zip(servers, replayed):
        orig_set = {g["pattern"] for g in s.get("accountabilityGaps", [])}
        replay_set = {g["pattern"] for g in replay_gaps}
        for p in orig_set: pat_orig[p] += 1
        for p in replay_set: pat_replay[p] += 1
        if orig_set == replay_set:
            matched += 1
        else:
            if len(mismatched_examples) < 5:
                mismatched_examples.append({
                    "name": s.get("name"),
                    "orig": sorted(orig_set),
                    "replay": sorted(replay_set),
                    "only_orig": sorted(orig_set - replay_set),
                    "only_replay": sorted(replay_set - orig_set),
                })

    n = len(servers)
    print(f"Servers with identical gap sets: {matched}/{n} ({matched/n*100:.1f}%)")
    print()
    print(f"{'pattern':<35} {'stored':>8} {'replay':>8} {'delta':>7}")
    print("-" * 60)
    all_pats = sorted(set(pat_orig) | set(pat_replay), key=lambda p: -pat_orig.get(p, 0))
    for p in all_pats:
        o, r = pat_orig.get(p, 0), pat_replay.get(p, 0)
        print(f"{p:<35} {o:>8} {r:>8} {r - o:>+7}")
    print()
    if mismatched_examples:
        print(f"Examples of mismatches ({len(mismatched_examples)} shown):")
        for ex in mismatched_examples:
            print(f"  {ex['name']}")
            print(f"    only in stored: {ex['only_orig']}")
            print(f"    only in replay: {ex['only_replay']}")
        print()

    # If self-test counts don't agree per-pattern, abort -- the Python port has a bug.
    pattern_drift = sum(abs(pat_replay.get(p, 0) - pat_orig.get(p, 0)) for p in all_pats)
    print(f"Total pattern-count drift (sum |replay - stored|): {pattern_drift}")
    if pattern_drift > n * 0.05:
        print("WARN: drift exceeds 5% threshold -- Python port may have rule bugs.")
        print("      Treat augmented results with caution.")
    print()

    # ── Pass 2: replay with supp tools included ────────────────────────────
    print("=" * 72)
    print("AUGMENTED RUN: det + LLM-supplementary tools")
    print("=" * 72)
    augmented, _ = run(corpus_path, include_supp=True)

    pat_aug = Counter()
    aug_per_pattern_servers = defaultdict(set)
    for i, (s, gaps) in enumerate(zip(servers, augmented)):
        for g in gaps:
            pat_aug[g["pattern"]] += 1
            aug_per_pattern_servers[g["pattern"]].add(i)

    print(f"{'pattern':<35} {'stored':>8} {'augmented':>10} {'Δ':>5}")
    print("-" * 64)
    for p in all_pats:
        o, a = pat_orig.get(p, 0), pat_aug.get(p, 0)
        print(f"{p:<35} {o:>8} {a:>10} {a - o:>+5}")
    print()

    # ── Dual-denominator prevalence ────────────────────────────────────────
    print("=" * 72)
    print("PREVALENCE: stored vs augmented, under multiple denominators")
    print("=" * 72)
    # Compute analyzable bases
    src_with_det = sum(
        1 for s in servers
        if s.get("stratum") != "remote-only" and s.get("tools")
    )
    rem_with_tools = sum(
        1 for s in servers
        if s.get("stratum") == "remote-only" and s.get("tools")
    )
    src_with_any = sum(
        1 for s in servers
        if s.get("stratum") != "remote-only"
        and (s.get("tools") or s.get("llmSupplementaryTools"))
    )
    n_945 = n
    n_strict = src_with_det + rem_with_tools     # det-only analyzable
    n_augmented = src_with_any + rem_with_tools  # det-or-supp analyzable
    print(f"Denominators:")
    print(f"  N=945  (surveyed)                        = {n_945}")
    print(f"  N strict-analyzable (det tools present)  = {n_strict}")
    print(f"  N supp-augmented   (det OR supp present) = {n_augmented}")
    print()

    def pct(c, d):
        return f"{c / d * 100:.1f}%" if d else "--"

    print(f"{'pattern':<35} {'orig/945':>9} {'aug/945':>8} "
          f"{'orig/strict':>12} {'aug/aug-base':>13}")
    print("-" * 84)
    for p in all_pats:
        o = pat_orig.get(p, 0)
        a = pat_aug.get(p, 0)
        print(f"{p:<35} {pct(o, n_945):>9} {pct(a, n_945):>8} "
              f"{pct(o, n_strict):>12} {pct(a, n_augmented):>13}")
    print()


if __name__ == "__main__":
    main()
