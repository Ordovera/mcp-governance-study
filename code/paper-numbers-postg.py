"""
Recompute every paper-outline number on the post-G corpus, side-by-side with the
outline's current (pre-extractor) values, so the reconciliation is mechanical.

- Gaps + sensitivity are RECOMPUTED on the merged tool set via the validated
  rerun-gap-detection.py port (stored accountabilityGaps/sensitivity are stale
  after tool merges; merged tools also lack a sensitivity field).
- Governance indicators (auth/logging/gates/...) are pattern-file-based and
  independent of tool extraction -> read from stored `indicators` (stable).

Stdlib only. Plain text to stdout.
"""

import argparse
import json
import math
from collections import Counter

from _repro import add_data_dir_arg, corpus_path, load_rgd

_args = add_data_dir_arg(argparse.ArgumentParser()).parse_args()
rgd = load_rgd()

CORPUS = "evidence_corpus_n1000_post_phaseg.json"
corpus = json.load(open(corpus_path(CORPUS, _args.data_dir)))
servers = corpus["servers"]
N = len(servers)
source = [s for s in servers if s.get("stratum") != "remote-only"]
remote = [s for s in servers if s.get("stratum") == "remote-only"]
NSRC = len(source)


def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 0, 0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / d
    return (p * 100, max(0, c - h) * 100, min(1, c + h) * 100)


def chi2_2x2(a, b, c, d):
    # a,b = group1 (gap, no-gap); c,d = group2
    n = a + b + c + d
    if n == 0:
        return 0.0, 0.0
    row1, row2 = a + b, c + d
    col1, col2 = a + c, b + d
    chi = 0.0
    for obs, (r, col) in zip([a, b, c, d], [(row1, col1), (row1, col2), (row2, col1), (row2, col2)]):
        exp = r * col / n
        if exp > 0:
            chi += (obs - exp) ** 2 / exp
    # odds ratio (group1 gap-odds / group2 gap-odds)
    orr = (a * d) / (b * c) if b * c else float("inf")
    return chi, orr


# Recompute gaps (det-only) with det tools AUGMENTED for sensitivity. Merged
# tools (from phase reruns) carry name/description/classification but NO
# sensitivity field, so the two sensitive-read gaps must be recomputed on
# augmented tools to stay consistent with the recomputed sensitivity counts.
# (Non-sensitive gaps depend only on classification and are unaffected.)
def run_augmented():
    out = []
    for s in servers:
        if s.get("stratum") == "remote-only":
            out.append([])
            continue
        det = [rgd.augment_tool(t) for t in (s.get("tools") or [])]
        patterns = s.get("patterns", {}) or {}
        tool_files = {t.get("sourceFile") for t in det if t.get("sourceFile")}
        auth_arch = rgd.assess_auth_architecture(patterns.get("auth", []), tool_files)
        has_attr = bool(s.get("flags", {}).get("hasAttributedLogging"))
        out.append(rgd.detect_gaps(det, patterns, auth_arch, has_attr))
    return out

per_server = run_augmented()
gapsets = [set(g["pattern"] for g in gs) for gs in per_server]

print("=" * 72)
print(f"POST-G RECONCILIATION  (N={N}, source-available={NSRC}, remote={len(remote)})")
print("=" * 72)

# ---- Table 1: gaps on source-available (paper denominator) ----
print("\n[Table 1] Gap prevalence (source-available N=%d)  outline -> post-G" % NSRC)
OUTLINE_T1 = {
    "__any__": (488, "64.2%"),
    "auth-without-actor-logging": (303, "39.9%"),
    "global-auth-over-sensitive-tools": (218, "28.7%"),
    "ungated-write": (152, "20.0%"),
    "destructive-without-audit-trail": (71, "9.3%"),
    "sensitive-read-without-logging": (46, "6.1%"),
    "logging-without-attribution": (43, "5.7%"),
    "sensitive-read-without-auth": (3, "0.4%"),
}
src_idx = [i for i, s in enumerate(servers) if s.get("stratum") != "remote-only"]
pat = Counter()
anyg = 0
for i in src_idx:
    if gapsets[i]:
        anyg += 1
    for p in gapsets[i]:
        pat[p] += 1
order = ["__any__", "auth-without-actor-logging", "global-auth-over-sensitive-tools",
         "ungated-write", "destructive-without-audit-trail", "sensitive-read-without-logging",
         "logging-without-attribution", "sensitive-read-without-auth"]
counts = {"__any__": anyg, **pat}
for p in order:
    k = counts.get(p, 0)
    pp, lo, hi = wilson(k, NSRC)
    oc, op = OUTLINE_T1[p]
    print(f"  {p:<36} {oc:>4}({op:>6}) -> {k:>4}({pp:>5.1f}%) [{lo:.1f},{hi:.1f}]  Δ{k-oc:+d}")
# full-corpus any-gap (the "52%" figure)
anyg_full = sum(1 for gs in gapsets if gs)
pp, lo, hi = wilson(anyg_full, N)
print(f"  {'(any-gap / full N=945)':<36} {'488(51.6%)':>11} -> {anyg_full:>4}({pp:>5.1f}%)")

# ---- 4.1 corpus / tool counts ----
det_tools = sum(len(s.get("tools", [])) for s in servers)
llm_supp = sum(len(s.get("llmSupplementaryTools", [])) for s in servers)
src_with = sum(1 for s in source if s.get("tools"))
print("\n[4.1 / 4.8] Tool extraction")
print(f"  heuristic(det) tools:   outline 10,335 -> post-G {det_tools}")
print(f"  LLM supplementary:      outline  4,124 -> post-G {llm_supp}")
print(f"  source w/ det tools:    {src_with}/{NSRC} = {src_with/NSRC*100:.0f}%  (outline 'extraction rate 63%')")
print(f"  source w/ ZERO tools:   {NSRC-src_with}/{NSRC} = {(NSRC-src_with)/NSRC*100:.0f}%  (outline '37% no extractable tools')")
langs = Counter(s.get("language", "unknown") for s in source)
print("  language dist (source): " + ", ".join(f"{l} {c/NSRC*100:.0f}%" for l, c in langs.most_common()))

# ---- 4.5 sensitivity (recomputed on merged tools) ----
all_tools = [rgd.augment_tool(t) for s in servers for t in s.get("tools", [])]
sens = [t for t in all_tools if t["sensitivity"] == "sensitive"]
sread = [t for t in sens if t.get("classification") == "read"]
swrite = [t for t in sens if t.get("classification") == "write"]
cat = Counter(t.get("sensitivityCategory") for t in sens)
servers_sread = sum(1 for s in servers if any(
    rgd.augment_tool(t)["sensitivity"] == "sensitive" and t.get("classification") == "read"
    for t in s.get("tools", [])))
print("\n[4.5] Sensitivity (recomputed on merged tools)  outline -> post-G")
print(f"  sensitive tools:        236 -> {len(sens)}")
print(f"  sensitive-read:         120 -> {len(sread)}  (write {len(swrite)})")
print(f"  servers w/ sens-read:    57 -> {servers_sread}")
print(f"  categories: " + ", ".join(f"{k} {v}" for k, v in cat.most_common()))
srwl = sum(1 for i in src_idx if "sensitive-read-without-logging" in gapsets[i])
print(f"  sens-read servers lacking co-located logging: {srwl}/{servers_sread} = "
      f"{srwl/servers_sread*100:.0f}%  (abstract said 81%)")

# ---- Table 2: MCP annotation adoption (policy-authoring proxy), N=760 ----
def _has_annotation(t):
    a = t.get("annotations")
    return isinstance(a, dict) and len(a) > 0
ann_servers = sum(1 for s in source if any(_has_annotation(t) for t in s.get("tools", [])))
ann_tools = sum(1 for s in source for t in s.get("tools", []) if _has_annotation(t))
src_tools_total = sum(len(s.get("tools", [])) for s in source)
print("\n[Table 2] MCP annotation adoption (PAP proxy, source-available N=%d)" % NSRC)
print(f"  servers w/ >=1 annotated tool: {ann_servers}/{NSRC} = {ann_servers/NSRC*100:.1f}%"
      f"  (S5.1 had ~6% pilot)")
print(f"  annotated tools:               {ann_tools}/{src_tools_total} = "
      f"{ann_tools/src_tools_total*100:.2f}%")

# ---- Table 4 association (recomputed) ----
print("\n[Table 4] Association with gap presence (source-available, recomputed)")
def assoc(label, pred):
    a = b = c = d = 0
    for i in src_idx:
        s = servers[i]
        has_gap = bool(gapsets[i])
        if pred(s):
            a += has_gap; b += not has_gap
        else:
            c += has_gap; d += not has_gap
    chi, orr = chi2_2x2(a, b, c, d)
    g1 = a / (a + b) * 100 if a + b else 0
    g2 = c / (c + d) * 100 if c + d else 0
    print(f"  {label:<34} {g1:>5.0f}% vs {g2:>4.0f}%   chi2={chi:>6.1f}  OR={orr:>5.2f}")

def n_tools(s):
    return len(s.get("tools", []))
def has_sens(s):
    return any(rgd.augment_tool(t)["sensitivity"] == "sensitive" for t in s.get("tools", []))
assoc("tool count >10 vs 1-10", lambda s: n_tools(s) > 10) # note: among with-tools
assoc("has tools vs zero", lambda s: n_tools(s) > 0)
assoc("has sensitive tools", has_sens)
assoc("has authentication", lambda s: s.get("flags", {}).get("hasAuth"))
assoc("registry presence", lambda s: s.get("stratum") in ("npm+registry", "pypi+registry"))
assoc("TypeScript vs Python", lambda s: s.get("language") == "typescript")

# ---- 4.4 strata ----
print("\n[4.4] Per-stratum (source-available)  N / tools/server / gap-rate")
strata = {}
for i in src_idx:
    s = servers[i]
    st = s.get("stratum", "?")
    d = strata.setdefault(st, {"n": 0, "tools": 0, "gap": 0})
    d["n"] += 1
    d["tools"] += len(s.get("tools", []))
    d["gap"] += bool(gapsets[i])
for st in sorted(strata):
    v = strata[st]
    print(f"  {st:<18} N={v['n']:>4}  {v['tools']/v['n']:>5.1f}/srv  gap {v['gap']/v['n']*100:>4.0f}%")

# ---- 4.7 governance score by gap presence (Model A additive) ----
# Scores are indicator-based (identical post-G); only the gap PARTITION changed.
_ENF = ["authentication", "perToolAuth", "confirmationGates", "stagedExecution", "rateLimiting", "leastPrivilege"]
_EVI = ["auditLogging", "actorAttribution"]
_ALL = _ENF + _EVI
def _score_additive(ind):
    p = sum(1 for k in _ALL if ind.get(k) == "Present")
    a = sum(1 for k in _ALL if ind.get(k) in ("Present", "Absent"))
    return round(p / a * 10, 2) if a else None
g_scores, ng_scores = [], []
for i in src_idx:
    sc = _score_additive(servers[i].get("indicators", {}) or {})
    if sc is None:
        continue
    (g_scores if gapsets[i] else ng_scores).append(sc)
print("\n[4.7] Model-A governance score by gap presence  outline -> post-G")
print(f"  gap servers:    mean 5.34 -> {sum(g_scores)/len(g_scores):.2f} (n={len(g_scores)})")
print(f"  no-gap servers: mean 3.02 -> {sum(ng_scores)/len(ng_scores):.2f} (n={len(ng_scores)})")
print("  (Model A/C distributions and Figure 1 cross-tab are indicator-based -> unchanged.)")

# ---- indicators note ----
print("\n[Table 2 indicators] pattern-file-based -> STABLE (read from stored, unchanged).")
print("  Exceptions (tool-derived) to verify by analyze re-run: readWriteSeparation, sensitiveReadProtection.")
print("\nDONE")
