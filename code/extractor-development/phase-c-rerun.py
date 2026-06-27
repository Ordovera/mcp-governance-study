"""
Phase C: re-run cc-mcp-audit's extractTools on the 234 false-negative servers
using the new Patterns A/B/C/D/Cr in extract.ts.

Steps:
  1. Identify 234 source-available FN servers (LLM-confirmed MCP, det tools = 0)
  2. Clone any missing or empty-shell repos (parallel, capped at 8)
  3. Batch-extract tools by spawning node + the built dist/extract.js
  4. Write per-server tool counts to a checkpoint JSON (resumable)
  5. Merge new tools into evidence_corpus_n1000.json (writes a sibling file
     evidence_corpus_n1000_post_phaseb.json -- never overwrites original)
  6. Print headline gap-pattern uplift estimate

Stdlib only.

Usage: python3 phase-c-rerun.py [--workers 8]
"""

import argparse
import concurrent.futures
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from tempfile import gettempdir


CLONE_BASE = Path(gettempdir()) / "cc-mcp-audit"
# Built extractor from the published instrument (cc-mcp-audit@1.0.1). Override
# with $CC_MCP_AUDIT_DIST (the package's dist/ directory); defaults to a local
# `npm i cc-mcp-audit@1.0.1` install. See ../../data/README.md.
DIST_EXTRACT = Path(
    os.environ.get("CC_MCP_AUDIT_DIST", "node_modules/cc-mcp-audit/dist")
) / "extract.js"
CHECKPOINT_FILE = Path("phase-c-checkpoint.json")
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
    """Clone the server's repo if not already a valid clone. Returns
    (owner_repo_key, clone_path | None, status)."""
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
    """Spawn a single node process to extract tools from every clone path.
    Returns dict[clone_path -> list[tool_dict]]."""
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
    # Write helper to a temp file (passing via --input-type=module + -e has
    # argv handling quirks)
    tmp_helper = Path(gettempdir()) / "phase-c-helper.mjs"
    tmp_helper.write_text(helper)
    args = ["node", str(tmp_helper)] + clone_paths
    r = subprocess.run(args, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"batch extract failed: {r.stderr[:500]}")
    return json.loads(r.stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="evidence_corpus_n1000.json")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--resume", action="store_true",
                    help="Reuse phase-c-checkpoint.json if present")
    args = ap.parse_args()

    if not DIST_EXTRACT.exists():
        print(f"ERROR: {DIST_EXTRACT} does not exist. Install the instrument "
              "(`npm i cc-mcp-audit@1.0.1`) or point $CC_MCP_AUDIT_DIST at its "
              "dist/ directory.")
        sys.exit(1)

    corpus = json.load(open(args.corpus))
    servers = corpus["servers"]
    fn = [
        s for s in servers
        if s.get("stratum") != "remote-only"
        and not s.get("tools")
        and s.get("llmVerification", {}).get("isMcpServer") is True
    ]
    print(f"Phase C target: {len(fn)} false-negative servers")

    # ── Stage 1: ensure clones ─────────────────────────────────────────────
    checkpoint = {}
    if args.resume and CHECKPOINT_FILE.exists():
        checkpoint = json.loads(CHECKPOINT_FILE.read_text())
        print(f"Resuming from checkpoint with {len(checkpoint)} entries")

    clone_results = {}
    to_clone = [s for s in fn if s.get("name") not in checkpoint]
    print(f"Cloning/verifying {len(to_clone)} servers "
          f"({args.workers}-way parallel)...")
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
    # Stats
    from collections import Counter
    statuses = Counter(v["status"].split(":")[0] for v in clone_results.values())
    print(f"  Clone outcomes: {dict(statuses)}")

    # ── Stage 2: batch extract ─────────────────────────────────────────────
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
        print(f"Batch extract failed: {e}")
        print("Falling back to per-server extraction...")
        extract_results = {}
        for _name, p in extractable:
            try:
                r = batch_extract([p])
                extract_results.update(r)
            except Exception:
                extract_results[p] = {"__error": "per_server_failure"}
    print(f"Extract done in {time.time()-t1:.0f}s")

    # Merge into checkpoint
    for name, p in extractable:
        result = extract_results.get(p, {})
        if isinstance(result, dict) and result.get("__error"):
            checkpoint[name] = {
                "clone_status": clone_results[name]["status"],
                "error": result["__error"],
                "tools": [],
            }
        else:
            checkpoint[name] = {
                "clone_status": clone_results[name]["status"],
                "tools": result or [],
            }
    # For servers that failed to clone, still record them
    for s in to_clone:
        if s["name"] not in checkpoint:
            checkpoint[s["name"]] = {
                "clone_status": clone_results[s["name"]]["status"],
                "tools": [],
            }
    CHECKPOINT_FILE.write_text(json.dumps(checkpoint, indent=2))
    print(f"Checkpoint saved: {CHECKPOINT_FILE}")

    # ── Stage 3: summarize ────────────────────────────────────────────────
    print(f"\n{'='*72}\nPER-SERVER UPLIFT SUMMARY\n{'='*72}")
    total_new = 0
    servers_recovered = 0
    for name, entry in checkpoint.items():
        nt = len(entry.get("tools", []))
        if nt > 0:
            total_new += nt
            servers_recovered += 1
    print(f"Servers with new tools: {servers_recovered}/{len(checkpoint)} "
          f"({servers_recovered/len(checkpoint)*100:.1f}%)")
    print(f"Total new tool extractions: {total_new}")
    print(f"Mean tools per recovered server: "
          f"{total_new/servers_recovered:.1f}" if servers_recovered else "n/a")

    # ── Stage 4: merge into corpus ────────────────────────────────────────
    new_corpus_path = args.corpus.replace(".json", "_post_phaseb.json")
    name_to_server = {s["name"]: s for s in servers}
    merged = 0
    for name, entry in checkpoint.items():
        if entry.get("tools"):
            srv = name_to_server.get(name)
            if srv:
                srv["tools"] = entry["tools"]
                merged += 1
    Path(new_corpus_path).write_text(json.dumps(corpus, indent=2))
    print(f"\nMerged {merged} servers' new tools into {new_corpus_path}")
    print(f"(Original {args.corpus} unchanged.)")


if __name__ == "__main__":
    main()
