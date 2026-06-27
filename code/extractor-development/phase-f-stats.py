"""
Phase F stats: recompute the deterministic-analyzable base and det-only
accountability-gap counts for the post-E and post-F corpora, and print the
Phase F delta.

Reuses the validated Python port of detectGaps from rerun-gap-detection.py
(imported, not reimplemented) so the numbers are comparable to prior phases.
det-only = run(corpus, include_supp=False); this reflects the tools currently
merged into each corpus (so Phase F's newly merged tools move tool-dependent
gaps).

Stdlib only.
"""

import importlib.util
from collections import Counter

spec = importlib.util.spec_from_file_location("rgd", "rerun-gap-detection.py")
rgd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rgd)

CORPORA = [
    ("post-E", "evidence_corpus_n1000_post_phasee.json"),
    ("post-F", "evidence_corpus_n1000_post_phasef.json"),
]

# Expected post-E numbers from project memory (sanity check on methodology).
EXPECTED_POST_E = {
    "auth-without-actor-logging": 303,
    "global-auth-over-sensitive-tools": 290,
    "ungated-write": 206,
    "destructive-without-audit-trail": 98,
    "sensitive-read-without-logging": 46,
    "logging-without-attribution": 43,
    "sensitive-read-without-auth": 3,
}


def analyze(path):
    per_server, servers = rgd.run(path, include_supp=False)
    pat = Counter()
    for gaps in per_server:
        for g in gaps:
            pat[g["pattern"]] += 1
    src_with_det = sum(
        1 for s in servers if s.get("stratum") != "remote-only" and s.get("tools")
    )
    rem = sum(
        1 for s in servers if s.get("stratum") == "remote-only" and s.get("tools")
    )
    return pat, src_with_det, rem


results = {}
for label, path in CORPORA:
    pat, src, rem = analyze(path)
    results[label] = {"pat": pat, "src": src, "rem": rem, "base": src + rem}

e, f = results["post-E"], results["post-F"]

print("=" * 70)
print("DETERMINISTIC-ANALYZABLE BASE")
print("=" * 70)
print(f"  post-E: {e['src']} source + {e['rem']} remote = {e['base']}")
print(f"  post-F: {f['src']} source + {f['rem']} remote = {f['base']}")
print(f"  delta : +{f['base'] - e['base']} servers")
print()

print("=" * 70)
print("DET-ONLY GAP COUNTS (N=945)   post-E -> post-F")
print("=" * 70)
order = [
    "auth-without-actor-logging",
    "global-auth-over-sensitive-tools",
    "ungated-write",
    "destructive-without-audit-trail",
    "sensitive-read-without-logging",
    "logging-without-attribution",
    "sensitive-read-without-auth",
]
print(f"{'pattern':<38}{'post-E':>7}{'post-F':>8}{'Δ':>5}")
print("-" * 58)
for p in order:
    pe, pf = e["pat"].get(p, 0), f["pat"].get(p, 0)
    print(f"{p:<38}{pe:>7}{pf:>8}{pf - pe:>+5}")
print()

print("=" * 70)
print("SANITY: post-E recompute vs memory's recorded post-E numbers")
print("=" * 70)
ok = True
for p, exp in EXPECTED_POST_E.items():
    got = e["pat"].get(p, 0)
    mark = "OK" if got == exp else "MISMATCH"
    if got != exp:
        ok = False
    print(f"  {p:<38} expected {exp:>4}  got {got:>4}  [{mark}]")
print()
print("  base expected 642, got", e["base"], "[OK]" if e["base"] == 642 else "[MISMATCH]")
print()
print("METHODOLOGY VALIDATED" if (ok and e["base"] == 642)
      else "WARNING: post-E recompute does not match memory; investigate before trusting post-F")
