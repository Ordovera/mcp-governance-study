"""
Pilot: try to recover tool inventories from the 234 deterministic-pipeline false
negatives by building each repo locally and asking the server itself via MCP
`tools/list` over stdio.

Stratified 15-server pilot (8 npm + 5 pypi + 2 other-ecosystem) drawn from the
false-negative pool. For each server:

  1. Clone (skip if already in /tmp/cc-mcp-audit/owner--repo)
  2. Detect build system and install dependencies (npm install OR pip install -e .)
  3. Detect entry point (package.json bin/main; pyproject.toml [project.scripts])
  4. Spawn the server with stdio transport, send MCP handshake + tools/list
  5. Record success/failure + elapsed time + tool count

Output:
  pilot-local-build-results.json (machine-readable per-server outcomes)
  stdout: human-readable summary table + full-corpus extrapolation

WARNING: This script RUNS ARBITRARY CODE from random GitHub repos under hard
timeouts. cc-mcp-audit's existing pipeline only does static analysis on these
repos. Running them is incrementally risky. Inspect the targeted servers before
running on untrusted data.

Stdlib only. Usage: python3 pilot-local-build.py [--seed 20260521]
"""

import argparse
import json
import os
import random
import shutil
import signal
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from tempfile import gettempdir


CLONE_BASE = Path(gettempdir()) / "cc-mcp-audit"
TIMEOUT_CLONE = 30
TIMEOUT_INSTALL = 240   # accommodate npm devDeps + build step or uv Python download
TIMEOUT_BUILD = 120     # npm run build for TS projects
TIMEOUT_START = 10
TIMEOUT_RPC = 8
PY_VERSION = "3.12"     # uv will download if not present


def owner_repo(source_url):
    """Parse 'owner/repo' from various GitHub URL forms."""
    s = source_url.replace("git+https://github.com/", "")
    s = s.replace("https://github.com/", "")
    s = s.split("?")[0].rstrip("/")
    if s.endswith(".git"):
        s = s[:-4]
    parts = s.split("/")
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return None, None


def select_sample(servers, seed):
    """Pick 15 stratified false-negative servers: 8 npm-ish, 5 pypi, 2 other."""
    fn = [
        s for s in servers
        if s.get("stratum") != "remote-only"
        and not s.get("tools")
        and s.get("llmVerification", {}).get("isMcpServer") is True
    ]
    rng = random.Random(seed)
    rng.shuffle(fn)

    def lang_bucket(s):
        st = s.get("stratum", "")
        if st.startswith("npm"):
            return "npm"
        if st.startswith("pypi"):
            return "pypi"
        return "other"

    buckets = {"npm": [], "pypi": [], "other": []}
    for s in fn:
        buckets[lang_bucket(s)].append(s)

    sample = (
        buckets["npm"][:8] + buckets["pypi"][:5] + buckets["other"][:2]
    )
    return sample


def run_cmd(cmd, cwd=None, timeout=60, env=None):
    """Run a subprocess. Returns (returncode, stdout, stderr, elapsed, timed_out)."""
    start = time.time()
    try:
        r = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True,
            timeout=timeout, env=env,
        )
        return r.returncode, r.stdout, r.stderr, time.time() - start, False
    except subprocess.TimeoutExpired as e:
        return -1, e.stdout or "", e.stderr or "", time.time() - start, True
    except FileNotFoundError as e:
        return -1, "", str(e), time.time() - start, False


def _has_real_clone(dest):
    """A cached clone is only usable if it has BOTH .git/HEAD and at least one
    recognizable manifest. Existing /tmp/cc-mcp-audit clones from prior runs
    can be empty shells (directory structure but no file content)."""
    if not (dest / ".git" / "HEAD").exists():
        return False
    return any(
        (dest / m).exists()
        for m in ("package.json", "pyproject.toml", "setup.py", "go.mod", "Cargo.toml")
    )


def clone_if_needed(source_url, owner, repo):
    """Clone the repo into /tmp/cc-mcp-audit/owner--repo (re-cloning if the
    cached copy is an empty shell)."""
    dest = CLONE_BASE / f"{owner}--{repo}"
    if _has_real_clone(dest):
        return dest, "cached", 0
    # Nuke any half-built shell and re-clone fresh
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    CLONE_BASE.mkdir(parents=True, exist_ok=True)
    url = source_url.replace("git+", "")
    rc, _out, err, elapsed, timed_out = run_cmd(
        ["git", "clone", "--depth", "1", url, str(dest)],
        timeout=TIMEOUT_CLONE,
    )
    if timed_out:
        return None, f"clone_timeout({TIMEOUT_CLONE}s)", elapsed
    if rc != 0:
        return None, f"clone_failed: {err.strip()[:200]}", elapsed
    return dest, "ok", elapsed


def detect_build_system(repo_dir):
    """Return ('npm' | 'pypi' | None, extra_info_dict)."""
    if (repo_dir / "package.json").exists():
        return "npm", {"manifest": "package.json"}
    if (repo_dir / "pyproject.toml").exists():
        return "pypi", {"manifest": "pyproject.toml"}
    if (repo_dir / "setup.py").exists():
        return "pypi", {"manifest": "setup.py"}
    return None, {}


def install_npm(repo_dir):
    """npm install WITH devDependencies (build steps usually need them), then
    run `npm run build` if a build script is defined. Returns (ok, status, elapsed)."""
    total = 0.0
    rc, _out, err, elapsed, timed_out = run_cmd(
        ["npm", "install", "--no-audit", "--no-fund"],
        cwd=repo_dir, timeout=TIMEOUT_INSTALL,
    )
    total += elapsed
    if timed_out:
        return False, f"install_timeout({TIMEOUT_INSTALL}s)", total
    if rc != 0:
        return False, f"npm_install_failed: {err.strip()[:300]}", total

    # Run build if present
    try:
        pkg = json.loads((repo_dir / "package.json").read_text())
        scripts = pkg.get("scripts") or {}
    except Exception:
        scripts = {}
    if "build" in scripts:
        rc, _out, err, elapsed, timed_out = run_cmd(
            ["npm", "run", "build"], cwd=repo_dir, timeout=TIMEOUT_BUILD,
        )
        total += elapsed
        if timed_out:
            return False, f"build_timeout({TIMEOUT_BUILD}s)", total
        if rc != 0:
            return False, f"npm_build_failed: {err.strip()[:300]}", total
    return True, "ok", total


def install_pypi(repo_dir):
    """Create a Python 3.12 venv via uv and install the package into it.
    Returns (ok, status, elapsed)."""
    venv_dir = repo_dir / ".venv-pilot"
    if venv_dir.exists():
        shutil.rmtree(venv_dir, ignore_errors=True)
    total = 0.0
    # Create venv with target Python (uv downloads it if not present)
    rc, _out, err, elapsed, timed_out = run_cmd(
        ["uv", "venv", "--python", PY_VERSION, str(venv_dir)],
        cwd=repo_dir, timeout=60,
    )
    total += elapsed
    if rc != 0:
        return False, f"venv_create_failed: {err.strip()[:200]}", total

    # Install the package into the venv
    rc, _out, err, elapsed, timed_out = run_cmd(
        ["uv", "pip", "install", "--python", str(venv_dir / "bin" / "python"),
         "-e", "."],
        cwd=repo_dir, timeout=TIMEOUT_INSTALL,
    )
    total += elapsed
    if timed_out:
        return False, f"install_timeout({TIMEOUT_INSTALL}s)", total
    if rc != 0:
        return False, f"pip_install_failed: {err.strip()[:300]}", total
    return True, "ok", total


def find_npm_entry(repo_dir):
    """Returns the command (as list) to start the MCP server, or None.

    Resolution order:
      1. package.json `bin` (string or first dict value) — these are usually
         compiled paths (dist/...) already
      2. If `main` is .ts, look for compiled equivalent under dist/build/lib
      3. package.json `main` (if .js)
      4. Fallback: dist/index.js, build/index.js, lib/index.js
    """
    pkg = json.loads((repo_dir / "package.json").read_text())
    bin_entry = pkg.get("bin")
    candidate_paths = []
    if isinstance(bin_entry, str):
        candidate_paths.append(bin_entry)
    elif isinstance(bin_entry, dict) and bin_entry:
        candidate_paths.append(next(iter(bin_entry.values())))

    main = pkg.get("main")
    if main:
        if main.endswith(".ts"):
            # Map src/index.ts -> dist/index.js (common TS convention)
            for out_dir in ("dist", "build", "lib", "out"):
                guess = main.replace("src/", f"{out_dir}/").replace(".ts", ".js")
                candidate_paths.append(guess)
        else:
            candidate_paths.append(main)

    # Generic fallbacks
    for out_dir in ("dist", "build", "lib", "out"):
        for fname in ("index.js", "server.js", "main.js"):
            candidate_paths.append(f"{out_dir}/{fname}")

    for cp in candidate_paths:
        p = repo_dir / cp
        if p.exists() and p.is_file():
            return ["node", str(p)]
    return None


def find_pypi_entry(repo_dir):
    """Returns the command to start the MCP server, or None.

    Resolution order:
      1. pyproject.toml [project.scripts] (or tool.poetry.scripts) first entry
      2. python -m <pkg> where <pkg> has __main__.py
    """
    venv_python = repo_dir / ".venv-pilot" / "bin" / "python"
    pp = repo_dir / "pyproject.toml"
    if pp.exists():
        text = pp.read_text()
        in_section = False
        scripts = {}
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                in_section = (stripped in ("[project.scripts]", "[tool.poetry.scripts]"))
                continue
            if in_section and "=" in stripped:
                k, _eq, v = stripped.partition("=")
                k = k.strip().strip('"').strip("'")
                v = v.strip().strip('"').strip("'")
                if k and v:
                    scripts[k] = v
        if scripts:
            entry_name = next(iter(scripts))
            return [str(repo_dir / ".venv-pilot" / "bin" / entry_name)]

    # Fallback: find a package with __main__.py and run it
    for entry in repo_dir.iterdir():
        if entry.is_dir() and (entry / "__main__.py").exists():
            return [str(venv_python), "-m", entry.name]
    return None


def mcp_introspect(cmd, cwd):
    """Spawn the server with stdio (as its own process group), send
    initialize + tools/list. Returns (tools, error). On failure, error
    includes a stderr snippet (first 500 chars) to aid diagnosis.

    The server is spawned in a new process group (start_new_session=True)
    so we can kill the whole group on cleanup -- otherwise a node/python
    wrapper that fork-spawns a Go or other binary will keep stderr open
    and block subsequent reads indefinitely."""
    proc = None
    try:
        proc = subprocess.Popen(
            cmd, cwd=cwd,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1,
            start_new_session=True,
        )
    except FileNotFoundError as e:
        return None, f"spawn_failed: {e}"

    def hard_kill_group():
        """Kill the entire process group so orphaned children release pipes."""
        if proc.poll() is not None:
            return
        try:
            pgid = os.getpgid(proc.pid)
        except ProcessLookupError:
            return
        try:
            os.killpg(pgid, signal.SIGTERM)
        except ProcessLookupError:
            return
        try:
            proc.wait(timeout=2)
            return
        except subprocess.TimeoutExpired:
            pass
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            return
        try:
            proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            pass

    def grab_stderr_snippet():
        """Bounded stderr drain: kill the process group, then read stderr
        with a hard 2s cap using select (so even an orphaned writer can't
        hang us)."""
        hard_kill_group()
        # Close stdin to be safe
        try:
            if proc.stdin and not proc.stdin.closed:
                proc.stdin.close()
        except Exception:
            pass
        import select as _select
        deadline = time.time() + 2.0
        chunks = []
        if proc.stderr:
            while time.time() < deadline:
                ready, _, _ = _select.select([proc.stderr], [], [], 0.2)
                if not ready:
                    break
                try:
                    chunk = proc.stderr.read(4096)
                except Exception:
                    break
                if not chunk:
                    break
                chunks.append(chunk)
                if sum(len(c) for c in chunks) > 8192:
                    break
        snippet = "".join(chunks).strip().replace("\n", " | ")[:500]
        return f" [stderr: {snippet}]" if snippet else ""

    def send(payload):
        proc.stdin.write(json.dumps(payload) + "\n")
        proc.stdin.flush()

    def recv_jsonrpc(deadline):
        """Read stdout lines until we get a JSON-RPC response with the desired id."""
        while True:
            if time.time() > deadline:
                return None, "rpc_timeout"
            # Block-read one line with the remaining time
            remaining = max(0.1, deadline - time.time())
            try:
                # Use a simple sentinel: readline with no timeout, rely on outer SIGALRM
                line = _readline_with_timeout(proc.stdout, remaining)
            except TimeoutError:
                return None, "rpc_timeout"
            if line is None:
                return None, "rpc_eof"
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue  # MCP servers may print non-JSON banners
            return msg, None

    try:
        send({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "pilot", "version": "0.1"},
            },
        })
        deadline = time.time() + TIMEOUT_START
        init_resp, err = recv_jsonrpc(deadline)
        if err:
            # process is likely dead -- read its stderr for the real cause
            try:
                proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                pass
            return None, f"init_{err}{grab_stderr_snippet()}"
        if "error" in (init_resp or {}):
            return None, f"init_error: {init_resp['error'].get('message', '?')[:120]}"

        send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        deadline = time.time() + TIMEOUT_RPC
        while True:
            resp, err = recv_jsonrpc(deadline)
            if err:
                return None, f"tools_list_{err}{grab_stderr_snippet()}"
            if resp.get("id") == 2:
                if "error" in resp:
                    return None, f"tools_list_error: {resp['error'].get('message', '?')[:120]}"
                tools = (resp.get("result") or {}).get("tools", [])
                return tools, None
    finally:
        if proc and proc.poll() is None:
            hard_kill_group()


def _readline_with_timeout(stream, timeout):
    """Read a single line from a subprocess stdout with a hard timeout.

    Uses select for portability on POSIX (we're on macOS)."""
    import select
    end = time.time() + timeout
    line_chars = []
    while True:
        remaining = end - time.time()
        if remaining <= 0:
            raise TimeoutError()
        ready, _, _ = select.select([stream], [], [], remaining)
        if not ready:
            raise TimeoutError()
        ch = stream.read(1)
        if ch == "":
            return None  # EOF
        if ch == "\n":
            return "".join(line_chars)
        line_chars.append(ch)


def pilot_one(s):
    """Run the full pilot pipeline for one server. Returns a result dict."""
    name = s.get("name", "?")
    source = s.get("source", "")
    owner, repo = owner_repo(source)
    if not owner:
        return {"name": name, "outcome": "bad_source_url"}

    t0 = time.time()
    timings = {}

    print(f"  [{name}] cloning...", flush=True)
    repo_dir, clone_status, t = clone_if_needed(source, owner, repo)
    timings["clone"] = round(t, 1)
    if not repo_dir:
        return {"name": name, "owner": owner, "repo": repo,
                "outcome": clone_status, "timings": timings,
                "total_s": round(time.time() - t0, 1)}

    build_kind, _info = detect_build_system(repo_dir)
    if build_kind is None:
        return {"name": name, "owner": owner, "repo": repo,
                "outcome": "no_build_system", "timings": timings,
                "total_s": round(time.time() - t0, 1)}

    print(f"  [{name}] installing ({build_kind})...", flush=True)
    if build_kind == "npm":
        ok, status, t = install_npm(repo_dir)
    else:
        ok, status, t = install_pypi(repo_dir)
    timings["install"] = round(t, 1)
    if not ok:
        return {"name": name, "owner": owner, "repo": repo,
                "build_kind": build_kind, "outcome": status,
                "timings": timings, "total_s": round(time.time() - t0, 1)}

    if build_kind == "npm":
        cmd = find_npm_entry(repo_dir)
    else:
        cmd = find_pypi_entry(repo_dir)
    if cmd is None:
        return {"name": name, "owner": owner, "repo": repo,
                "build_kind": build_kind, "outcome": "no_entry_point",
                "timings": timings, "total_s": round(time.time() - t0, 1)}

    print(f"  [{name}] introspecting via stdio: {' '.join(cmd)[:80]}...", flush=True)
    rpc_start = time.time()
    tools, err = mcp_introspect(cmd, str(repo_dir))
    timings["rpc"] = round(time.time() - rpc_start, 1)
    if tools is None:
        return {"name": name, "owner": owner, "repo": repo,
                "build_kind": build_kind, "outcome": err,
                "timings": timings, "total_s": round(time.time() - t0, 1),
                "cmd": cmd}

    return {
        "name": name, "owner": owner, "repo": repo,
        "build_kind": build_kind, "outcome": "success",
        "tool_count": len(tools),
        "tool_names": [t.get("name") for t in tools[:10]],
        "timings": timings,
        "total_s": round(time.time() - t0, 1),
        "cmd": cmd,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", default="evidence_corpus_n1000.json")
    ap.add_argument("--seed", type=int, default=20260521)
    ap.add_argument("--out", default="pilot-local-build-results.json")
    args = ap.parse_args()

    corpus = json.load(open(args.corpus))
    sample = select_sample(corpus["servers"], args.seed)
    print(f"Pilot sample: {len(sample)} servers")
    for s in sample:
        print(f"  [{s.get('stratum')}/{s.get('language')}] {s.get('name')}")
    print()

    results = []
    for i, s in enumerate(sample, 1):
        print(f"--- {i}/{len(sample)} ---")
        try:
            r = pilot_one(s)
        except Exception as e:
            r = {"name": s.get("name"), "outcome": f"crash: {e}",
                 "total_s": None}
        results.append(r)
        print(f"  -> outcome={r.get('outcome')}  "
              f"tools={r.get('tool_count', '-')}  total_s={r.get('total_s')}")
        # Incremental persist so we don't lose progress on crash/timeout
        Path(args.out).write_text(json.dumps(results, indent=2))

    print(f"\nResults saved to {args.out}\n")

    # Summary
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    outcomes = Counter(r.get("outcome", "?").split(":")[0].split("(")[0]
                       for r in results)
    for k, v in outcomes.most_common():
        print(f"  {k}: {v}")
    successes = [r for r in results if r.get("outcome") == "success"]
    if successes:
        print(f"\nSuccess rate: {len(successes)}/{len(results)} "
              f"({len(successes)/len(results)*100:.0f}%)")
        total_tools = sum(r.get("tool_count", 0) for r in successes)
        mean_tools = total_tools / len(successes)
        print(f"Total tools recovered: {total_tools} "
              f"(mean {mean_tools:.1f}/success)")
        times = [r["total_s"] for r in successes if r.get("total_s")]
        if times:
            print(f"Time/success: median {sorted(times)[len(times)//2]:.0f}s, "
                  f"max {max(times):.0f}s")

    # Extrapolation
    total_attempted = sum(r.get("total_s", 0) or 0 for r in results)
    if results:
        mean_time = total_attempted / len(results)
        full_serial = mean_time * 234
        print(f"\nExtrapolation to full 234 servers:")
        print(f"  Mean time/server (this pilot): {mean_time:.0f}s")
        print(f"  Serial full-corpus: {full_serial/60:.0f} min")
        print(f"  Parallel x4 (rough): {full_serial/60/4:.0f} min")
        if successes:
            extrapolated_recoveries = round(len(successes) / len(results) * 234)
            print(f"  Expected recoveries: ~{extrapolated_recoveries} servers")


if __name__ == "__main__":
    main()
