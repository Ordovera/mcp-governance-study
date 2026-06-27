"""
Negation/context-aware sensitivity variant (DOWNGRADE-ONLY).

Alternative-regime sensitivity analysis for the SoD/MCP paper. This is the
exact analog of the strict-auth-detection regime already reported (Section 4.3
/ Section 6.1 item 3): a clearly-labelled alternative regime, NOT a retuning of
the primary keyword classifier.

The primary deterministic classifier (ported in rerun-gap-detection.py) flags a
tool `sensitive` if ANY signal keyword matches at a word boundary. Human
validation (n=100, FINAL labels) surfaced a small set of false-positive modes in
which the matched term is negated or names an access gate rather than the tool's
data. This pass re-derives the sensitive set after DOWNGRADING any tool whose
matched signal(s) all sit in such a non-governance context.

Four downgrade guards (each only REMOVES a false positive; nothing is ever
added to the sensitive set, so every recomputed count is a conservative lower
bound):

  1. Negation proximity   -- matched term preceded by a negator (no/not/without/
                             never/cannot) or "free" within a short window.
  2. Access-gate context  -- a payment/purchase/billing match inside a gating
                             phrase (requires / subscription / unlock / to use):
                             the cost to USE the tool, not the tool's action.
  3. Name-only / masked    -- description says the values are masked / redacted /
                             not revealed / name-or-metadata-only near the match.
  4. Generic config/key    -- a config/environment/session + key/variable pair
                             matched on generic key-value / "budget config" /
                             store wording with no co-occurring secret-ish term.

A tool is downgraded only if EVERY one of its sensitive signals is neutralised by
a guard; a single genuine signal keeps the tool sensitive. The known false
negative (klaviyo_events_get_profile) is deliberately out of scope -- adding
sensitivity is the over-claiming direction this analysis does not take.

Reports raw (primary) vs variant counts as a range. Stdlib only.
"""

import argparse
import json
import re
from collections import Counter

from _repro import add_data_dir_arg, corpus_path, load_rgd

rgd = load_rgd()

CORPUS = "evidence_corpus_n1000_post_phaseg.json"

# ── Guard vocabulary ────────────────────────────────────────────────────────
NEGATORS = {
    "no", "not", "without", "never", "cannot", "can't", "cant",
    "dont", "don't", "doesn't", "doesnt", "neither", "none", "free",
}
# Purchase-gate cues: a cost term sitting near one of these names the price to
# USE the tool, not the tool's action. Deliberately PURCHASE-specific -- a bare
# "requires" (e.g. "REQUIRES AGENT KEY") is an auth requirement, not a paywall,
# and must NOT neutralise a genuine payment tool.
GATE_CUES = [
    "subscription", "subscribe", "to use", "to unlock", "to access",
    "upgrade", "premium", "paid plan", "tier", "purchase the",
    "purchase a", "must purchase", "must buy",
    "requires payment", "requires a payment", "required to use",
    "in order to use",
]
# A price token like "$0.005" adjacent to a cost term also marks a paywall.
_PRICE = re.compile(r"\$\s?\d")
# Word-boundary matcher for gate cues, so "purchase a" matches "purchase a plan"
# but NOT "purchase articles" (substring collision).
_GATE_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(g) for g in [
        "subscription", "subscribe", "to use", "to unlock", "to access",
        "upgrade", "premium", "paid plan", "tier", "purchase the",
        "purchase a", "must purchase", "must buy",
        "requires payment", "requires a payment", "required to use",
        "in order to use", "sub or",
    ]) + r")\b"
)
# Action verbs that, when they appear in the TOOL NAME, mark the tool as a
# genuine sensitive action -- never downgrade these regardless of phrasing.
PROTECTED_NAME_VERBS = {
    "pay", "buy", "withdraw", "deposit", "transfer", "send", "zap", "charge",
    "refund", "swap", "trade", "login", "ssh", "auth", "mfa", "sign",
    "execute", "exec", "deploy", "provision", "rotate", "revoke", "grant",
}
# Description-level signals that the tool returns only names/metadata, not values.
MASK_PHRASES = [
    "masked", "names only", "name only", "does not reveal", "doesn't reveal",
    "do not reveal", "not reveal", "redacted", "without revealing",
    "not the value", "not the actual value", "metadata only",
    "names and timestamps", "name and timestamp", "obfuscated",
]
# Terms that, if present, mean a config/key match is genuinely secret-bearing.
SECRETISH = [
    "secret", "token", "credential", "api_key", "apikey", "api key",
    "password", "private_key", "passphrase", "oauth", "bearer",
]
# Generic-store wording that makes a config/key match a plain key-value store.
GENERIC_STORE = [
    "key-value", "key value", "keyvalue", "kv store", "kv-store",
    "generic", "budget config", "arbitrary", "scratchpad", "memory store",
    "store a value", "store value", "cache",
]

# Cost/purchase action keywords (guard 2 applies to these).
COST_SIGNALS = {"payment", "purchase", "billing", "charge", "invoice", "refund"}
# Negation (guard 1) is applied only to the signals whose documented FP mode is
# negation-blindness: cost terms ("no payment required") and "secret"
# ("scan without secret detection"). Credential/password/key FPs are handled by
# the masked / generic-store guards instead, so a tool that genuinely manages a
# password (its prose merely negates around it) is NOT downgraded.
NEGATION_SIGNALS = COST_SIGNALS | {"secret"}

_BOUNDARY = re.compile(r"[\s_\-.:/]")


def _boundary_positions(text, keyword):
    """Yield start indices where `keyword` occurs at a word boundary in `text`.

    Mirrors rgd.matches_at_boundary's boundary rule (text is already lowercased,
    so the camelCase arm is inert here -- matches rgd's behavior on lowercased
    combined text)."""
    pos, n, k = 0, len(text), len(keyword)
    while pos <= n - k:
        idx = text.find(keyword, pos)
        if idx == -1:
            return
        before = "" if idx == 0 else text[idx - 1]
        after = "" if idx + k >= n else text[idx + k]
        left_ok = idx == 0 or bool(_BOUNDARY.match(before))
        right_ok = idx + k >= n or bool(_BOUNDARY.match(after))
        if left_ok and right_ok:
            yield idx
        pos = idx + 1


def _tokens_before(text, idx, window=4):
    """Return the up-to-`window` whitespace tokens immediately preceding idx."""
    prefix = text[:idx]
    toks = re.findall(r"[a-z']+", prefix)
    return toks[-window:]


def _all_occurrences_negated(text, keyword):
    """True iff keyword occurs at least once AND EVERY boundary occurrence has a
    negator within the 2 immediately-preceding tokens.

    The all-occurrences rule protects genuine action tools: a payment tool that
    settles funds mentions 'payment' un-negated somewhere, so a single negated
    'without payment headers' clause does not neutralise it."""
    found = False
    for idx in _boundary_positions(text, keyword):
        found = True
        if not (NEGATORS & set(_tokens_before(text, idx, window=4))):
            return False
    return found


def _all_cost_occurrences_gated(text, keyword):
    """True iff the cost keyword occurs at least once AND EVERY occurrence sits in
    a purchase-gate context (a GATE_CUE within ~30 chars, or an adjacent price
    token). Genuine payment actions ('Lightning payment', 'settle in USDC') are
    not gate-cued, so any un-gated occurrence keeps the tool sensitive."""
    found = False
    for idx in _boundary_positions(text, keyword):
        found = True
        window = text[max(0, idx - 50): idx + len(keyword) + 35]
        if _GATE_RE.search(window) or _PRICE.search(window):
            continue
        return False
    return found


def _masked(text):
    return any(p in text for p in MASK_PHRASES)


def _has_secretish(text):
    return any(rgd.matches_at_boundary(text, s) if "_" in s or " " not in s
               else s in text for s in SECRETISH)


def _generic_store(text):
    return any(g in text for g in GENERIC_STORE)


def _signal_base(signal):
    """For a context-pair signal 'base+qualifier', return (base, qualifier);
    otherwise (signal, None)."""
    if "+" in signal:
        base, qual = signal.split("+", 1)
        return base, qual
    return signal, None


def neutralised(signal, text):
    """Return a guard label if this signal is a non-governance match, else None."""
    base, qual = _signal_base(signal)

    # Guard 1: negation proximity. Applied only to cost/secret signals (the
    # documented negation-blind FP mode). For a pair signal the BASE must be
    # negated -- negating only a qualifier (e.g. 'without ... connection details'
    # while 'ssh_config' is genuinely present) does not neutralise the pair.
    if base in NEGATION_SIGNALS and _all_occurrences_negated(text, base):
        return "negation"

    # Guard 2: access-gate context for cost/purchase signals.
    if base in COST_SIGNALS and _all_cost_occurrences_gated(text, base):
        return "access-gate"

    # Guard 3: name-only / masked values (confidentiality-style signals).
    is_conf_like = base in {"credential", "password", "secret", "api_key",
                            "private_key", "access_token", "oauth_token",
                            "bearer_token", "connection_string", "database_url",
                            "config", "environment", "session", "admin"}
    if is_conf_like and _masked(text):
        return "masked"

    # Guard 4: generic config/key pair matched on plain key-value / semantic-store
    # wording with no secret-ish co-occurrence (the memory_store case). Scoped to
    # the `config` base only: `environment+*` matches on env-var *writes* are NOT
    # downgraded here, because creating env vars genuinely sets secret-bearing
    # config; the env-var FP mode is masked *reads* (guard 3), handled above.
    if base == "config" and qual in {"key", "token", "credential", "secret",
                                     "password", "connection", "database"}:
        if not _has_secretish(text) and _generic_store(text):
            return "generic-store"

    return None


def _name_protected(tool_name):
    """A tool whose NAME contains a sensitive action verb is never downgraded."""
    parts = set(re.split(r"[_\-.\s]+", (tool_name or "").lower()))
    return bool(parts & PROTECTED_NAME_VERBS)


def downgrade_reason(tool):
    """If `tool` is primary-sensitive but all signals are neutralised, return a
    dict of {signal: guard}; else None."""
    aug = rgd.augment_tool(tool)
    if aug["sensitivity"] != "sensitive":
        return None
    if _name_protected(tool.get("name")):
        return None
    signals = aug.get("sensitivitySignals") or []
    text = (tool.get("name", "") + " " + (tool.get("description") or "")).lower()
    reasons = {}
    for sig in signals:
        g = neutralised(sig, text)
        if g is None:
            return None  # a genuine signal survives -> keep sensitive
        reasons[sig] = g
    return reasons if signals else None


def main():
    args = add_data_dir_arg(argparse.ArgumentParser()).parse_args()
    resolved = corpus_path(CORPUS, args.data_dir)
    corpus = json.load(open(resolved))
    servers = corpus["servers"]

    def log_files(s):
        return {l["file"] for l in (s.get("patterns", {}) or {}).get("logging", [])}

    raw = {"sens": 0, "sread": 0}
    var = {"sens": 0, "sread": 0}
    cat_raw, cat_var = Counter(), Counter()
    raw_sread_servers, var_sread_servers = set(), set()
    raw_srwl, var_srwl = set(), set()
    downgraded = []  # (server, tool, signals->guard, classification)

    for s in servers:
        lf = log_files(s)
        name = s.get("name")
        for t in s.get("tools", []) or []:
            aug = rgd.augment_tool(t)
            if aug["sensitivity"] != "sensitive":
                continue
            is_read = t.get("classification") == "read"
            unlogged = t.get("sourceFile") not in lf
            src = s.get("stratum") != "remote-only"

            # raw tallies
            raw["sens"] += 1
            cat_raw[aug["sensitivityCategory"]] += 1
            if is_read:
                raw["sread"] += 1
                if src:
                    raw_sread_servers.add(name)
                    if unlogged:
                        raw_srwl.add(name)

            reasons = downgrade_reason(t)
            if reasons is not None:
                downgraded.append((name, t.get("name"), reasons,
                                   t.get("classification")))
                continue  # downgraded -> excluded from variant sensitive set

            # variant tallies (survivors)
            var["sens"] += 1
            cat_var[aug["sensitivityCategory"]] += 1
            if is_read:
                var["sread"] += 1
                if src:
                    var_sread_servers.add(name)
                    if unlogged:
                        var_srwl.add(name)

    def pctline(label, rawc, varc, denom_raw=None, denom_var=None):
        if denom_raw:
            print(f"  {label:<42} {rawc:>5} ({rawc/denom_raw*100:4.1f}%)"
                  f"  ->  {varc:>5} ({varc/denom_var*100:4.1f}%)")
        else:
            print(f"  {label:<42} {rawc:>5}  ->  {varc:>5}")

    print("=" * 78)
    print("SENSITIVITY: primary (raw) vs negation/context-aware variant (downgrade-only)")
    print("=" * 78)
    print(f"  corpus: {resolved}")
    print(f"  tools downgraded: {len(downgraded)}")
    print()
    pctline("sensitive tools (all extracted)", raw["sens"], var["sens"])
    print(f"    by category raw: {dict(cat_raw)}")
    print(f"    by category var: {dict(cat_var)}")
    pctline("sensitive-read tools", raw["sread"], var["sread"])
    rs, vs = len(raw_sread_servers), len(var_sread_servers)
    pctline("source-available servers w/ sensitive-read", rs, vs)
    rl, vl = len(raw_srwl), len(var_srwl)
    print()
    print("  sensitive-read-without-logging (source-available):")
    print(f"    raw:     {rl}/{rs} = {rl/rs*100:.1f}%")
    print(f"    variant: {vl}/{vs} = {vl/vs*100:.1f}%")
    print()

    # ── downgrade breakdown + acceptance sanity check ─────────────────────────
    by_guard = Counter()
    for _, _, reasons, _ in downgraded:
        for g in set(reasons.values()):
            by_guard[g] += 1
    print("  downgrades by guard (a tool may trigger >1):")
    for g, c in by_guard.most_common():
        print(f"    {g:<14} {c}")
    print()
    print(f"  all {len(downgraded)} downgraded tools:")
    for srv, tool, reasons, cls in sorted(downgraded, key=lambda x: x[1]):
        rs_str = ", ".join(f"{k}:{v}" for k, v in reasons.items())
        print(f"    [{cls:<5}] {tool:<42} ({srv})  -> {rs_str}")

    # ── Acceptance check (against the canonical FINAL false-positive items and
    #    the genuine positives the plan says must stay sensitive) ──────────────
    down_names = {t for _, t, _, _ in downgraded}
    must_downgrade = {
        "board_read", "security_quick_scan", "generate_social_kit",
        "memory_store", "list_global_environment_variables", "credentials_list",
    }
    must_keep = {  # genuine actions / value-bearing tools -- never downgrade
        "nostr_zap", "pay_l402_api", "withdraw", "ssh_login", "buy_domain",
        "create_user", "verify_session_factor", "create_smart_hook_env_vars",
        "credentials_set", "set_secret",
    }
    print()
    print("  ACCEPTANCE:")
    miss = sorted(must_downgrade - down_names)
    leak = sorted(must_keep & down_names)
    print(f"    documented FPs downgraded: {sorted(must_downgrade & down_names)}")
    if miss:
        print(f"    FAIL -- documented FP NOT downgraded: {miss}")
    if leak:
        print(f"    FAIL -- genuine positive downgraded: {leak}")
    if not miss and not leak:
        print("    PASS -- all documented FPs downgraded; all genuine positives kept")


if __name__ == "__main__":
    main()
