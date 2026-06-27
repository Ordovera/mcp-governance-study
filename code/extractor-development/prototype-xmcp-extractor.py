"""
Prototype Pattern I: xmcp framework extractor.

xmcp is a TypeScript MCP server framework where each tool lives in its own
file under a configured directory (default: src/tools), with the tool's name
declared in an exported metadata constant:

    export const metadata: ToolMetadata = {
      name: "create-app-store-version",
      description: "Create a new App Store version ...",
      annotations: { ... },
    };

Gate:
  - package.json declares "xmcp" dependency, AND
  - repo root contains xmcp.config.ts (or .js/.mts/.mjs)
The tools directory comes from xmcp.config.ts's `paths.tools` field, with
fallback to "src/tools".

Targets:
  beautyfree/appstore-connect-mcp (69 tools)
  matiasngf/mcp-fetch (5 tools)

Stdlib only.
"""

import json
import re
import sys
from pathlib import Path
from tempfile import gettempdir


CLONE_BASE = Path(gettempdir()) / "cc-mcp-audit"

TARGETS = {
    "beautyfree--appstore-connect-mcp": 69,
    "matiasngf--mcp-fetch": 5,
}

_PATHS_TOOLS_RE = re.compile(r"""tools\s*:\s*['"]([^'"]+)['"]""")
_METADATA_RE = re.compile(
    r"""export\s+const\s+metadata\s*(?::\s*ToolMetadata\s*)?=\s*\{([\s\S]*?)\n\}""",
    re.MULTILINE,
)
_NAME_FIELD_RE = re.compile(r"""\bname\s*:\s*['"]([^'"]+)['"]""")
_DESC_FIELD_RE = re.compile(r"""\bdescription\s*:\s*['"]([^'"]+)['"]""")


def has_xmcp(repo: Path):
    """Gate: xmcp dependency in package.json AND xmcp.config.* at root."""
    pkg = repo / "package.json"
    if not pkg.is_file():
        return False
    try:
        pkg_data = json.loads(pkg.read_text())
    except Exception:
        return False
    deps = {**(pkg_data.get("dependencies") or {}), **(pkg_data.get("devDependencies") or {})}
    if "xmcp" not in deps:
        return False
    for ext in ("ts", "mts", "js", "mjs"):
        if (repo / f"xmcp.config.{ext}").is_file():
            return True
    return False


def find_tools_dir(repo: Path) -> str:
    """Read xmcp.config.* for `paths.tools: "..."`. Default to "src/tools"."""
    for ext in ("ts", "mts", "js", "mjs"):
        cfg = repo / f"xmcp.config.{ext}"
        if cfg.is_file():
            src = cfg.read_text(errors="ignore")
            m = _PATHS_TOOLS_RE.search(src)
            if m:
                return m.group(1)
    return "src/tools"


def extract_xmcp_tools(repo: Path):
    """Return list of (name, description, source_file) tuples."""
    if not has_xmcp(repo):
        return []
    tools_dir = repo / find_tools_dir(repo)
    if not tools_dir.is_dir():
        return []
    found = []
    for f in sorted(tools_dir.glob("*.ts")):
        try:
            src = f.read_text(errors="ignore")
        except Exception:
            continue
        m = _METADATA_RE.search(src)
        if not m:
            continue
        body = m.group(1)
        nm = _NAME_FIELD_RE.search(body)
        if not nm:
            continue
        dm = _DESC_FIELD_RE.search(body)
        found.append((nm.group(1), dm.group(1) if dm else "", str(f.relative_to(repo))))
    return found


def main():
    print(f"Clone base: {CLONE_BASE}\n")
    grand_found = 0
    grand_expected = 0
    for slug, expected in TARGETS.items():
        repo = CLONE_BASE / slug
        if not repo.is_dir():
            print(f"  MISSING: {slug}")
            continue
        tools = extract_xmcp_tools(repo)
        n = len(tools)
        grand_found += n
        grand_expected += expected
        status = "OK " if n == expected else ("LOW" if n < expected else "HI ")
        print(f"  [{status}] {slug:<40s}  found={n:>3}  expected={expected}")
        if n != expected or n <= 6:
            for name, desc, f in tools[:5]:
                print(f"        {name}  ({f})")
            if n > 5:
                print(f"        ... and {n - 5} more")
    print()
    print(f"Total found:     {grand_found}")
    print(f"Total expected:  {grand_expected}")
    if grand_found < grand_expected:
        sys.exit(1)


if __name__ == "__main__":
    main()
