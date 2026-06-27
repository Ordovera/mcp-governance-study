"""
Audit the edge cases the paper must own:

  A. Source-available servers that extracted ZERO tools (paper-relevant
     because a reviewer will ask "why did your pipeline drop these?").
     Bucket each by warning taxonomy and cross-reference against LLM
     verification ground truth.

  B. Remote-only servers where RPC introspection SUCCEEDED (n=23).
     What can we say about governance for remote MCP when we get the
     tool list but not the source?

Output is a plain-text report on stdout. Stdlib only.
"""

import argparse
import json
from collections import Counter, defaultdict

from _repro import add_data_dir_arg, corpus_path

_args = add_data_dir_arg(argparse.ArgumentParser()).parse_args()
corpus = json.load(open(corpus_path("evidence_corpus_n1000.json", _args.data_dir)))
servers = corpus["servers"]
N = len(servers)

src = [s for s in servers if s.get("stratum") != "remote-only"]
rem = [s for s in servers if s.get("stratum") == "remote-only"]

src_notools = [s for s in src if not s.get("tools")]
rem_with_tools = [s for s in rem if s.get("tools")]
rem_notools = [s for s in rem if not s.get("tools")]


def classify_warnings(s):
    """Bucket a no-tool source-available server by why it has no tools."""
    warns = s.get("warnings", [])
    ws = " || ".join(warns)
    if not warns:
        return "no_warning"
    # MCP framework detected but no tools extracted -- registration pattern not covered
    if "MCP framework detected" in ws and "no tools were extracted" in ws:
        return "method_limitation_mcp_detected"
    # Not detected as MCP at all
    if "No tools extracted and no MCP framework imports detected" in ws:
        return "not_mcp_no_framework_detected"
    # Auth-walled (private API, requires credentials)
    if "Server requires authentication" in ws:
        return "access_barrier_auth_required"
    # Language detection failed -- pipeline couldn't reach extraction stage
    if "Could not detect primary language" in ws:
        return "language_unknown"
    # Remote-only branch leaked into source path
    if "no declared endpoint URL" in ws or "Remote-only" in ws:
        return "remote_misclassified"
    return "other_warning"


# ── A. Source-available, zero tools ─────────────────────────────────────
print("=" * 76)
print("A. SOURCE-AVAILABLE, ZERO TOOLS EXTRACTED")
print("=" * 76)
print(f"N = {len(src_notools)} (of {len(src)} source-available; "
      f"{len(src_notools)/len(src)*100:.1f}% of stratum)")
print()

buckets = defaultdict(list)
for s in src_notools:
    buckets[classify_warnings(s)].append(s)

# For each bucket: count + LLM ground-truth breakdown
print("Bucket breakdown:")
print(f"  {'bucket':<36} {'n':>4}  LLM ground truth (MCP / not-MCP / no LLM)")
print("  " + "-" * 86)
for bucket, group in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
    n = len(group)
    mcp = sum(1 for s in group
              if s.get("llmVerification", {}).get("isMcpServer") is True)
    notmcp = sum(1 for s in group
                 if s.get("llmVerification", {}).get("isMcpServer") is False)
    no_lv = sum(1 for s in group if not s.get("llmVerification"))
    print(f"  {bucket:<36} {n:>4}    {mcp:>3} / {notmcp:>3} / {no_lv:>3}")
print()

# The headline number: LLM-confirmed-MCP with zero deterministic tools
all_confirmed_mcp_zero = [
    s for s in src_notools
    if s.get("llmVerification", {}).get("isMcpServer") is True
]
print(f"** Headline: {len(all_confirmed_mcp_zero)} source-available servers are "
      f"LLM-confirmed MCP yet the deterministic pipeline extracted zero tools.")
print(f"   This is {len(all_confirmed_mcp_zero)}/{len(src)} = "
      f"{len(all_confirmed_mcp_zero)/len(src)*100:.1f}% of source-available servers.")
print(f"   These are genuine deterministic-pipeline false negatives that the paper "
      f"should own as a known limitation.")
print()

# How many tools did the LLM report on those false negatives?
llm_tools_recovered = sum(
    s.get("llmVerification", {}).get("toolCount", 0) or 0
    for s in all_confirmed_mcp_zero
)
mean_llm_tools = (llm_tools_recovered / len(all_confirmed_mcp_zero)
                  if all_confirmed_mcp_zero else 0)
print(f"   LLM reports {llm_tools_recovered} tools across these {len(all_confirmed_mcp_zero)} "
      f"servers (mean = {mean_llm_tools:.1f} tools/server).")
print()

# Which bucket contributes the most LLM-confirmed false negatives?
print("Per-bucket: how many are LLM-confirmed MCP (the false-negative subset)?")
print(f"  {'bucket':<36} {'total':>6} {'LLM=MCP':>9} {'rate':>6}")
print("  " + "-" * 66)
for bucket, group in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
    n = len(group)
    mcp = sum(1 for s in group
              if s.get("llmVerification", {}).get("isMcpServer") is True)
    rate = f"{mcp / n * 100:.0f}%" if n else "--"
    print(f"  {bucket:<36} {n:>6} {mcp:>9} {rate:>6}")
print()

# Sample servers per bucket for inspection
print("Sample false-negative servers (LLM=MCP, deterministic tools=0):")
print(f"  {'bucket':<36} {'name':<55} {'LLM_tools'}")
shown = 0
seen_buckets = set()
for bucket, group in sorted(buckets.items(), key=lambda kv: -len(kv[1])):
    mcps = [s for s in group
            if s.get("llmVerification", {}).get("isMcpServer") is True]
    for s in mcps[:3]:
        lt = s.get("llmVerification", {}).get("toolCount", 0)
        name = (s.get("name", "")[:54])
        print(f"  {bucket:<36} {name:<55} {lt}")
        shown += 1
    if mcps:
        seen_buckets.add(bucket)
print()

# ── B. Remote-only with tools ────────────────────────────────────────────
print("=" * 76)
print("B. REMOTE-ONLY WITH TOOLS (RPC INTROSPECTION SUCCEEDED)")
print("=" * 76)
print(f"N = {len(rem_with_tools)} (of {len(rem)} remote-only; "
      f"{len(rem_with_tools)/len(rem)*100:.1f}% RPC success rate)")
print()

tool_counts = sorted((len(s.get("tools", [])) for s in rem_with_tools), reverse=True)
print(f"Tools-per-server distribution:")
print(f"  total tools:  {sum(tool_counts)}")
print(f"  max:          {tool_counts[0] if tool_counts else 0}")
print(f"  median:       {tool_counts[len(tool_counts)//2] if tool_counts else 0}")
print(f"  min:          {tool_counts[-1] if tool_counts else 0}")
print()

# Governance indicators on remote-with-tools: how many are Determined vs Indeterminate?
indicator_keys = ["authentication", "perToolAuth", "confirmationGates",
                  "stagedExecution", "rateLimiting", "leastPrivilege",
                  "auditLogging", "actorAttribution"]
print("Governance indicator status across the 23 remote-with-tools servers:")
print(f"  {'indicator':<22} {'Present':>8} {'Absent':>8} {'Indet':>8}")
print("  " + "-" * 52)
for k in indicator_keys:
    counts = Counter()
    for s in rem_with_tools:
        v = s.get("indicators", {}).get(k)
        counts[v] += 1
    print(f"  {k:<22} {counts.get('Present', 0):>8} "
          f"{counts.get('Absent', 0):>8} {counts.get('Indeterminate', 0):>8}")
print()

# Gap patterns
gap_counts = Counter()
remote_with_gaps = 0
for s in rem_with_tools:
    gaps = s.get("accountabilityGaps", [])
    if gaps:
        remote_with_gaps += 1
    for g in gaps:
        gap_counts[g["pattern"]] += 1
print(f"Servers with at least one gap pattern: {remote_with_gaps}/{len(rem_with_tools)}")
if gap_counts:
    print("Gap patterns observed in remote-with-tools:")
    for p, c in gap_counts.most_common():
        print(f"  {p}: {c}")
else:
    print("(No gap patterns triggered in this group.)")
print()

# Server list (for the paper appendix)
print(f"All 23 remote-with-tools servers:")
print(f"  {'name':<55} {'tools':>5} {'gaps':>5} {'tools/server'}")
print("  " + "-" * 70)
for s in sorted(rem_with_tools, key=lambda x: -len(x.get("tools", []))):
    n_tools = len(s.get("tools", []))
    n_gaps = len(s.get("accountabilityGaps", []))
    print(f"  {s.get('name', '')[:54]:<55} {n_tools:>5} {n_gaps:>5}")
print()

# Cross-check: among the 162 remote-only WITHOUT tools, what's the warning taxonomy?
print("=" * 76)
print("C. (Context) REMOTE-ONLY WITHOUT TOOLS")
print("=" * 76)
rem_warn_buckets = Counter()
for s in rem_notools:
    warns = " || ".join(s.get("warnings", []))
    if not warns:
        rem_warn_buckets["no_warning"] += 1
    elif "RPC introspection failed" in warns:
        rem_warn_buckets["rpc_failed"] += 1
    elif "no declared endpoint URL" in warns:
        rem_warn_buckets["no_endpoint_url"] += 1
    elif "requires authentication" in warns:
        rem_warn_buckets["auth_required"] += 1
    else:
        rem_warn_buckets["other"] += 1
print(f"N = {len(rem_notools)}")
for k, v in rem_warn_buckets.most_common():
    print(f"  {k}: {v}")
