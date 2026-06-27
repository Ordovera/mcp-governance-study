"""
Phase G: re-run cc-mcp-audit's extractTools on the residual false-negative
servers using the new Patterns Q (TS slot-3 wrapper) and L (ListTools arrays) plus the
comment/docstring guards in extract.ts.

Mirrors phase-c-rerun.py exactly (same FN filter, clone-or-cache, batch extract,
checkpoint, merge) but:
  - reads the post-Phase-E corpus as input
  - writes evidence_corpus_n1000_post_phasef.json (never overwrites the input)
  - uses a Phase-F checkpoint

Stdlib only.

Usage: python3 phase-f-rerun.py [--workers 8] [--resume]
"""

import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from tempfile import gettempdir


CLONE_BASE = Path(gettempdir()) / "cc-mcp-audit"
# Built extractor from the published instrument (cc-mcp-audit@1.0.1). Override
# with $CC_MCP_AUDIT_DIST (the package's dist/ directory); defaults to a local
# `npm i cc-mcp-audit@1.0.1` install. See ../../data/README.md.
DIST_EXTRACT = Path(
    os.environ.get("CC_MCP_AUDIT_DIST", "node_modules/cc-mcp-audit/dist")
) / "extract.js"
CHECKPOINT_FILE = Path("phase-g-checkpoint.json")
INPUT_CORPUS = "evidence_corpus_n1000_post_phasef.json"
OUTPUT_CORPUS = "evidence_corpus_n1000_post_phaseg.json"
TIMEOUT_CLONE = 60


def owner_repo(source: str):
    s = source.replace("git+https://github.com/", "")
    s = s.replace("https://github.com/", "")
    s = s.split("?")[0].rstrip("/")
    if s.endswith(".git"):
        s = s[:-4]
    parts = s.split("/")
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return None, None


def has_real_clone(dest: Path) -> bool:
    if not (dest / ".git" / "HEAD").exists():
        return False
    return any(
        (dest / m).exists()
        for m in ("package.json", "pyproject.toml", "setup.py", "go.mod", "Cargo.toml")
    )


def ensure_clone(server):
    src = server.get("source", "")
    owner, repo = owner_repo(src)
    if not owner:
        return (None, None, "bad_source_url")
    key = f"{owner}--{repo}"
    dest = CLONE_BASE / key
    if has_real_clone(dest):
        return (key, dest, "cached")
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    CLONE_BASE.mkdir(parents=True, exist_ok=True)
    url = src.replace("git+", "")
    try:
        r = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(dest)],
            capture_output=True, text=True, timeout=TIMEOUT_CLONE,
        )
    except subprocess.TimeoutExpired:
        return (key, None, "clone_timeout")
    if r.returncode != 0:
        return (key, None, f"clone_failed: {r.stderr.strip()[:120]}")
    return (key, dest, "cloned")


def batch_extract(clone_paths):
    helper = f"""
import {{ extractTools }} from '{DIST_EXTRACT}';
const paths = process.argv.slice(1);
const results = {{}};
for (const p of paths) {{
  try {{
    const tools = extractTools(p);
    results[p] = tools.map(t => ({{
      name: t.name,
      description: t.description,
      classification: t.classification,
      sourceFile: t.sourceFile,
      sourceLine: t.sourceLine,
    }}));
  }} catch (err) {{
    results[p] = {{ __error: String(err).slice(0, 300) }};
  }}
}}
process.stdout.write(JSON.stringify(results));
"""
    tmp_helper = Path(gettempdir()) / "phase-g-helper.mjs"
    tmp_helper.write_text(helper)
    args = ["node", str(tmp_helper)] + clone_paths
    r = subprocess.run(args, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"batch extract failed: {r.stderr[:500]}")
    return json.loads(r.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default=INPUT_CORPUS)
    ap.add_argument("--out", default=OUTPUT_CORPUS)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    if not DIST_EXTRACT.exists():
        print(f"ERROR: {DIST_EXTRACT} does not exist. Run `npm run build` first.")
        sys.exit(1)

    corpus = json.load(open(args.corpus))
    servers = corpus["servers"]
    fn = [
        s for s in servers
        if s.get("stratum") != "remote-only"
        and not s.get("tools")
        and s.get("llmVerification", {}).get("isMcpServer") is True
    ]
    print(f"Phase G target: {len(fn)} residual false-negative servers")

    checkpoint = {}
    if args.resume and CHECKPOINT_FILE.exists():
        checkpoint = json.loads(CHECKPOINT_FILE.read_text())
        print(f"Resuming from checkpoint with {len(checkpoint)} entries")

    clone_results = {}
    to_clone = [s for s in fn if s.get("name") not in checkpoint]
    print(f"Cloning/verifying {len(to_clone)} servers ({args.workers}-way)...")
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(ensure_clone, s): s for s in to_clone}
        done = 0
        for f in concurrent.futures.as_completed(futures):
            s = futures[f]
            key, path, status = f.result()
            clone_results[s["name"]] = {
                "key": key,
                "clone_path": str(path) if path else None,
                "status": status,
            }
            done += 1
            if done % 20 == 0:
                print(f"  {done}/{len(to_clone)} ({time.time()-t0:.0f}s)")
    print(f"Cloning done in {time.time()-t0:.0f}s")
    statuses = Counter(v["status"].split(":")[0] for v in clone_results.values())
    print(f"  Clone outcomes: {dict(statuses)}")

    extractable = [
        (s["name"], clone_results[s["name"]]["clone_path"])
        for s in to_clone
        if clone_results[s["name"]]["clone_path"]
    ]
    if not extractable:
        print("No extractable clones; nothing to do.")
        return

    print(f"\nBatch-extracting from {len(extractable)} clones via node...")
    t1 = time.time()
    paths = [p for _name, p in extractable]
    try:
        extract_results = batch_extract(paths)
    except Exception as e:
        print(f"Batch extract failed: {e}\nFalling back to per-server...")
        extract_results = {}
        for _name, p in extractable:
            try:
                extract_results.update(batch_extract([p]))
            except Exception:
                extract_results[p] = {"__error": "per_server_failure"}
    print(f"Extract done in {time.time()-t1:.0f}s")

    for name, p in extractable:
        result = extract_results.get(p, {})
        if isinstance(result, dict) and result.get("__error"):
            checkpoint[name] = {"clone_status": clone_results[name]["status"],
                                "error": result["__error"], "tools": []}
        else:
            checkpoint[name] = {"clone_status": clone_results[name]["status"],
                                "tools": result or []}
    for s in to_clone:
        if s["name"] not in checkpoint:
            checkpoint[s["name"]] = {"clone_status": clone_results[s["name"]]["status"],
                                     "tools": []}
    CHECKPOINT_FILE.write_text(json.dumps(checkpoint, indent=2))
    print(f"Checkpoint saved: {CHECKPOINT_FILE}")

    # ── Summary ───────────────────────────────────────────────────────────
    print(f"\n{'='*72}\nPER-SERVER UPLIFT SUMMARY\n{'='*72}")
    total_new = 0
    recovered = []
    for name, entry in checkpoint.items():
        nt = len(entry.get("tools", []))
        if nt > 0:
            total_new += nt
            recovered.append((name, nt))
    recovered.sort(key=lambda x: -x[1])
    print(f"Servers with new tools: {len(recovered)}/{len(checkpoint)}")
    print(f"Total new tool extractions: {total_new}")
    for name, nt in recovered:
        print(f"  {nt:>4}  {name}")

    # ── Merge into corpus ─────────────────────────────────────────────────
    name_to_server = {s["name"]: s for s in servers}
    merged = 0
    for name, entry in checkpoint.items():
        if entry.get("tools"):
            srv = name_to_server.get(name)
            if srv:
                srv["tools"] = entry["tools"]
                merged += 1
    Path(args.out).write_text(json.dumps(corpus, indent=2))
    print(f"\nMerged {merged} servers' new tools into {args.out}")
    print(f"(Input {args.corpus} unchanged.)")


if __name__ == "__main__":
    main()
