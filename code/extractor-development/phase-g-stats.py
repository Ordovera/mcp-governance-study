"""
Phase G stats: recompute the deterministic-analyzable base and det-only
accountability-gap counts for the post-F and post-G corpora, and print the
Phase G delta. Reuses the validated detectGaps port from rerun-gap-detection.py.

Sanity check: the post-F recompute must reproduce the post-F numbers recorded
after Phase F (base 666; global-auth 306, ungated-write 218, destructive 103).
"""

import importlib.util
from collections import Counter

spec = importlib.util.spec_from_file_location("rgd", "rerun-gap-detection.py")
rgd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rgd)

CORPORA = [
    ("post-F", "evidence_corpus_n1000_post_phasef.json"),
    ("post-G", "evidence_corpus_n1000_post_phaseg.json"),
]

EXPECTED_POST_F = {
    "auth-without-actor-logging": 303,
    "global-auth-over-sensitive-tools": 306,
    "ungated-write": 218,
    "destructive-without-audit-trail": 103,
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
    src = sum(1 for s in servers if s.get("stratum") != "remote-only" and s.get("tools"))
    rem = sum(1 for s in servers if s.get("stratum") == "remote-only" and s.get("tools"))
    return pat, src, rem


results = {label: analyze(path) for label, path in CORPORA}
(ef, esrc, erem) = results["post-F"]
(gf, gsrc, grem) = results["post-G"]

print("=" * 70)
print("DETERMINISTIC-ANALYZABLE BASE")
print("=" * 70)
print(f"  post-F: {esrc} source + {erem} remote = {esrc + erem}")
print(f"  post-G: {gsrc} source + {grem} remote = {gsrc + grem}")
print(f"  delta : +{(gsrc + grem) - (esrc + erem)} servers")
print()

order = [
    "auth-without-actor-logging",
    "global-auth-over-sensitive-tools",
    "ungated-write",
    "destructive-without-audit-trail",
    "sensitive-read-without-logging",
    "logging-without-attribution",
    "sensitive-read-without-auth",
]
print("=" * 70)
print("DET-ONLY GAP COUNTS (N=945)   post-F -> post-G")
print("=" * 70)
print(f"{'pattern':<38}{'post-F':>7}{'post-G':>8}{'Δ':>5}")
print("-" * 58)
for p in order:
    a, b = ef.get(p, 0), gf.get(p, 0)
    print(f"{p:<38}{a:>7}{b:>8}{b - a:>+5}")
print()

print("=" * 70)
print("SANITY: post-F recompute vs recorded post-F numbers")
print("=" * 70)
ok = (esrc + erem) == 666
for p, exp in EXPECTED_POST_F.items():
    got = ef.get(p, 0)
    mark = "OK" if got == exp else "MISMATCH"
    if got != exp:
        ok = False
    print(f"  {p:<38} expected {exp:>4}  got {got:>4}  [{mark}]")
print(f"  base expected 666, got {esrc + erem}")
print()
print("METHODOLOGY VALIDATED" if ok else "WARNING: post-F recompute mismatch; investigate before trusting post-G")
