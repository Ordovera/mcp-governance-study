"""
Prototype Pattern A: multi-line `server.tool(...)` / `.registerTool(...)` extractor.

Goal: measure how many tools we'd recover if cc-mcp-audit's TypeScript extractor
were extended to handle multi-line `.tool(` and `.registerTool(` calls (where
the call is opened on one line and the name appears on the next).

Run over the 15 pilot clones; report tools-per-server and aggregate yield.

Stdlib only.
"""

import json
import re
import sys
from pathlib import Path
from tempfile import gettempdir


CLONE_BASE = Path(gettempdir()) / "cc-mcp-audit"

# Current single-line patterns (subset of extract.ts; these are what cc-mcp-audit
# already extracts -- our prototype targets only the MISSED multi-line variant).
CURRENT_TOOL_RE = re.compile(r'\.tool\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']*)["\']')
CURRENT_TOOL_NO_DESC_RE = re.compile(r'\.tool\(\s*["\']([^"\']+)["\']\s*,')
CURRENT_REGISTER_RE = re.compile(r'\.registerTool\(\s*["\']([^"\']+)["\']')

# New: open-paren at end of line (multi-line continuation)
OPEN_TOOL_RE = re.compile(r'\.(?:tool|registerTool)\(\s*$')
QUOTED_NAME_RE = re.compile(r'^\s*["\']([^"\']+)["\']')


def is_test_file(path: Path) -> bool:
    name = path.name.lower()
    return ".test." in name or ".spec." in name or name.startswith("test_")


def find_ts_files(repo_dir: Path):
    skip_dirs = {"node_modules", ".git", "dist", "build", "__pycache__",
                 ".venv", "venv", ".venv-pilot", "out"}
    for p in repo_dir.rglob("*"):
        if p.is_file() and p.suffix in (".ts", ".js", ".mjs"):
            if not any(part in skip_dirs for part in p.parts):
                if not is_test_file(p):
                    yield p


def extract_current(file_path: Path, lines):
    """Mirror the patterns cc-mcp-audit already catches (one-line)."""
    tools = []
    for i, line in enumerate(lines):
        m = CURRENT_TOOL_RE.search(line)
        if m:
            tools.append((m.group(1), i + 1, "single_line_with_desc"))
            continue
        m = CURRENT_TOOL_NO_DESC_RE.search(line)
        if m:
            tools.append((m.group(1), i + 1, "single_line_no_desc"))
            continue
        m = CURRENT_REGISTER_RE.search(line)
        if m:
            tools.append((m.group(1), i + 1, "registerTool_single_line"))
            continue
    return tools


def extract_multiline_new(file_path: Path, lines):
    """Find tools registered with multi-line .tool( or .registerTool(."""
    tools = []
    for i, line in enumerate(lines):
        if OPEN_TOOL_RE.search(line):
            # Walk forward up to 3 non-blank lines looking for a quoted name
            for j in range(i + 1, min(i + 5, len(lines))):
                next_line = lines[j]
                if not next_line.strip():
                    continue
                m = QUOTED_NAME_RE.match(next_line)
                if m:
                    tools.append((m.group(1), i + 1, "multi_line"))
                    break
                # If line is something else (like a variable ref), stop
                break
    return tools


def analyze_repo(repo_dir: Path):
    current_total = []
    new_total = []
    for f in find_ts_files(repo_dir):
        try:
            content = f.read_text(errors="replace")
        except Exception:
            continue
        lines = content.split("\n")
        cur = extract_current(f, lines)
        new = extract_multiline_new(f, lines)
        # Filter out duplicates between current and new (same name in same file)
        cur_names = {n for n, _l, _k in cur}
        new_dedup = [(n, l, k) for n, l, k in new if n not in cur_names]
        current_total.extend((f, n, l, k) for n, l, k in cur)
        new_total.extend((f, n, l, k) for n, l, k in new_dedup)
    return current_total, new_total


def main():
    # The 15 pilot clones (owner--repo names)
    pilot_dirs = [
        "cyanheads--docwriter-mcp-server",
        "Pavelevich--llm-checker",
        "eutech-directory--legis-link-mcp",
        "adrianczuczka--mason",
        "hatip5656--telegram-mcp",
        "LumabyteCo--clarifyprompt-mcp",
        "GeiserX--pumperly-mcp",
        "SurgeEnterpriseAI--teams-mcp-server",
        "dgunning--edgartools",
        "IBM--ibm-watsonxdata-dl-retrieval-mcp-server",
        "KazKozDev--mcp-search-server",
        "zw008--VMware-Monitor",
        "jaspertvdm--mcp-server-jis",
        "Br0ski777--text-classifier-x402",
        "Br0ski777--email-send-x402",
    ]

    print(f"{'repo':<45} {'cur':>4} {'NEW':>5}  sample new tools")
    print("-" * 88)
    grand_cur = 0
    grand_new = 0
    for name in pilot_dirs:
        d = CLONE_BASE / name
        if not d.exists():
            print(f"{name:<45}  (no clone)")
            continue
        cur, new = analyze_repo(d)
        grand_cur += len(cur)
        grand_new += len(new)
        sample = ", ".join(n for _f, n, _l, _k in new[:3])
        if len(new) > 3:
            sample += f", ... +{len(new)-3}"
        print(f"{name:<45} {len(cur):>4} {len(new):>5}  {sample}")
    print("-" * 88)
    print(f"{'TOTAL':<45} {grand_cur:>4} {grand_new:>5}")
    print()
    print(f"Pattern A would recover {grand_new} additional tool extractions "
          f"across the 15 pilot servers (current extractor: {grand_cur}).")


if __name__ == "__main__":
    main()
