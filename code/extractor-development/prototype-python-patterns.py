"""
Prototype Patterns B and C: extend cc-mcp-audit's Python extractor.

Pattern B: `@mcp.tool(annotations={...})` -- decorator with kwargs but no name.
  Current Python extractor requires a string-positional or name= kwarg in the
  decorator call; any other kwargs-only form falls through all three paths and
  is missed. Fix: when @<obj>.tool(...) is matched but no name string is found,
  search forward for `def <name>(...)` and use the function name as the tool name.

Pattern C: @app.list_tools() handler with inline Tool() constructors.
  Servers using the low-level MCP SDK declare a @list_tools handler that
  returns a list of Tool(name=..., description=...) constructors. The current
  extractor doesn't look inside list_tools handlers at all. Fix: when we see
  @<obj>.list_tools(), scan the function body for Tool(name="...") patterns.

Run over the 15 pilot clones; report tools-per-server and aggregate yield.
Mirrors prototype-multiline-extractor.py for TS.

Stdlib only.
"""

import re
from pathlib import Path
from tempfile import gettempdir


CLONE_BASE = Path(gettempdir()) / "cc-mcp-audit"

# ── Current patterns (subset of extract.ts extractPythonTools) ─────────────
# These are what cc-mcp-audit already catches; we mirror them so the prototype
# only counts NEW recoveries (not double-counts existing extractions).

# Single-line decorator with name string
CUR_DECORATOR_WITH_NAME_RE = re.compile(
    r'@\w+\.tool\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']'
)
# Bare decorator: @obj.tool()
CUR_BARE_DECORATOR_RE = re.compile(r'@(\w+)\.tool\(\s*\)\s*$')
# Multi-line decorator opening: @obj.tool(
CUR_MULTILINE_DECORATOR_RE = re.compile(r'@(\w+)\.tool\(\s*$')
# Call-style registration: server.tool("name", ...) on one line
CUR_CALL_REG_RE = re.compile(
    r'\b\w+\.tool\(\s*["\']([^"\']+)["\']'
)
# add_tool dynamic registration
CUR_ADD_TOOL_RE = re.compile(r'\.add_tool\(')

# ── New patterns ──────────────────────────────────────────────────────────

# Pattern B: @\w+\.tool( with content that is NOT a name string and NOT empty.
# We detect "tool(" opening; if no current pattern matches the line (or its
# multi-line continuation), and the call has kwargs-only content, find the
# next def/async def.
PATTERN_B_OPEN_RE = re.compile(r'@(\w+)\.tool\(')
# To recognize multi-line forms, look ahead to the matching close-paren.

DEF_LINE_RE = re.compile(r'^\s*(?:async\s+)?def\s+(\w+)\s*\(')

# Pattern C: @\w+\.list_tools() handler whose body has Tool(name="...") literals
# MULTILINE so $ matches end-of-line, not end-of-file (we scan whole-file text
# in has_registry_listtools_handler).
PATTERN_C_LIST_TOOLS_RE = re.compile(r'@(\w+)\.list_tools\(\s*\)\s*$', re.MULTILINE)

# Pattern D: bare decorator like `@tool(name="...", ...)` imported from a
# project base module. The decorator name is a single identifier (no `.`),
# matches one of a set of recognized words, and the call has `name=` kwarg.
PATTERN_D_OPEN_RE = re.compile(r'^\s*@(tool|register_tool|mcp_tool|server_tool)\(')
# Confirm the file imports the decorator name from somewhere.
# Two import shapes:
#   - single-line: from X import a, b, name, c
#   - multi-line parenthesized: from X import (\n  a,\n  name,\n  b,\n)
DECORATOR_IMPORT_RE_TEMPLATE = (
    r'from\s+[\w.]+\s+import\s+'
    r'(?:'
    r'(?:[^()\n]*\b{name}\b)'                   # single-line: ...name...
    r'|'
    r'\([^)]*\b{name}\b[^)]*\)'                 # multi-line: ( ...\n  name,\n )
    r')'
)
PATTERN_C_TOOL_CTOR_NAME_RE = re.compile(
    r'\bTool\s*\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']'
)


def is_test_file(p: Path) -> bool:
    name = p.name.lower()
    return (
        name.startswith("test_") or name.endswith("_test.py")
        or "/tests/" in str(p) or "/test/" in str(p)
    )


def find_py_files(repo_dir: Path):
    skip_dirs = {
        "node_modules", ".git", "dist", "build", "__pycache__",
        ".venv", "venv", ".venv-pilot", "out", ".tox", ".mypy_cache",
        "site-packages",
    }
    for p in repo_dir.rglob("*.py"):
        if not p.is_file():
            continue
        if any(part in skip_dirs for part in p.parts):
            continue
        if is_test_file(p):
            continue
        yield p


def find_close_paren(lines, start_line, start_col):
    """Track paren depth to find the matching close paren for an open at
    (start_line, start_col). Returns (line_idx, col_idx) of the close, or None.

    Scans up to 200 lines forward -- decorator bodies in MCP servers can be
    long because of multi-line descriptions + params schemas."""
    depth = 0
    started = False
    for li in range(start_line, min(start_line + 200, len(lines))):
        text = lines[li]
        start = start_col if li == start_line else 0
        for ci in range(start, len(text)):
            ch = text[ci]
            if ch == "(":
                depth += 1
                started = True
            elif ch == ")":
                depth -= 1
                if started and depth == 0:
                    return li, ci
        if started and depth == 0:
            return None
    return None


def find_def_after(lines, after_idx):
    """Scan forward from after_idx (inclusive) for a `def name(` line.
    Returns the function name, or None. Skips lines starting with @ (decorators)
    and blank lines."""
    for i in range(after_idx, min(after_idx + 10, len(lines))):
        s = lines[i].strip()
        if not s or s.startswith("@"):
            continue
        m = DEF_LINE_RE.match(lines[i])
        if m:
            return m.group(1), i
        return None, -1  # something else interrupted -- give up
    return None, -1


def has_name_in_decorator_call(call_body: str) -> bool:
    """Returns True if the call body (text inside the parens of @obj.tool(...))
    contains a positional string name or `name=` kwarg."""
    # Strip outer whitespace
    body = call_body.strip()
    if not body:
        return False
    # Check for positional string as first arg
    if re.match(r'^["\']', body):
        return True
    # Check for name= kwarg
    if re.search(r'\bname\s*=\s*["\']', body):
        return True
    return False


def extract_current(file_path: Path, lines):
    """Approximate what cc-mcp-audit's Python extractor already captures.
    Returns list of (name, line_idx, kind)."""
    tools = []
    skip_until = 0
    for i, line in enumerate(lines):
        if i < skip_until:
            continue
        m = CUR_DECORATOR_WITH_NAME_RE.search(line)
        if m:
            tools.append((m.group(1), i + 1, "current_decorator_with_name"))
            continue
        m = CUR_BARE_DECORATOR_RE.search(line)
        if m:
            fname, _ = find_def_after(lines, i + 1)
            if fname:
                tools.append((fname, i + 1, "current_bare_decorator"))
            continue
        m = CUR_MULTILINE_DECORATOR_RE.search(line)
        if m:
            # Multi-line decorator; cc-mcp-audit reads the body for name=/description= kwargs
            close = find_close_paren(lines, i, line.index("("))
            if close:
                body = "\n".join([lines[i][line.index("(") + 1:]]
                                 + lines[i + 1:close[0]]
                                 + [lines[close[0]][:close[1]]])
                m2 = re.search(r'\bname\s*=\s*["\']([^"\']+)["\']', body)
                if m2:
                    tools.append((m2.group(1), i + 1,
                                  "current_multiline_decorator_name_kwarg"))
                else:
                    fname, _ = find_def_after(lines, close[0] + 1)
                    if fname:
                        tools.append((fname, i + 1,
                                      "current_multiline_decorator_def_after"))
            skip_until = (close[0] + 1) if close else (i + 1)
            continue
        m = CUR_CALL_REG_RE.search(line)
        if m and not line.lstrip().startswith("@"):
            tools.append((m.group(1), i + 1, "current_call_style"))
    return tools


def extract_pattern_b(file_path: Path, lines, already_caught_lines):
    """Pattern B: @<obj>.tool(<kwargs only, no name>) followed by def <name>."""
    tools = []
    for i, line in enumerate(lines):
        if i + 1 in already_caught_lines:
            continue
        m = PATTERN_B_OPEN_RE.search(line)
        if not m:
            continue
        # Find the close paren of the decorator call
        open_col = line.index("(", m.end() - 1)
        close = find_close_paren(lines, i, open_col)
        if close is None:
            continue
        # Reconstruct the call body
        if close[0] == i:
            body = line[open_col + 1:close[1]]
        else:
            parts = [line[open_col + 1:]]
            for li in range(i + 1, close[0]):
                parts.append(lines[li])
            parts.append(lines[close[0]][:close[1]])
            body = "\n".join(parts)
        # If the body has a name string or name= kwarg, this is handled by current
        # patterns -- skip to avoid double-counting.
        if has_name_in_decorator_call(body):
            continue
        # Find the def after the close-paren line
        fname, _ = find_def_after(lines, close[0] + 1)
        if fname:
            tools.append((fname, i + 1, "pattern_B_kwargs_only_decorator"))
    return tools


def extract_pattern_c(file_path: Path, lines):
    """Pattern C (narrow): @<obj>.list_tools() handler with INLINE
    Tool(name="...") body. For registry-mediated cases, see
    extract_pattern_c_registry."""
    tools = []
    for i, line in enumerate(lines):
        if not PATTERN_C_LIST_TOOLS_RE.search(line):
            continue
        fname, def_line = find_def_after(lines, i + 1)
        if not fname or def_line < 0:
            continue
        def_indent = len(lines[def_line]) - len(lines[def_line].lstrip())
        body_start = def_line + 1
        body_end = body_start
        for j in range(body_start, len(lines)):
            stripped = lines[j].strip()
            if not stripped:
                body_end = j + 1
                continue
            indent = len(lines[j]) - len(lines[j].lstrip())
            if indent <= def_indent:
                break
            body_end = j + 1
        body_text = "\n".join(lines[body_start:body_end])
        for m in PATTERN_C_TOOL_CTOR_NAME_RE.finditer(body_text):
            tools.append((m.group(1), i + 1, "pattern_C_list_tools_inline"))
    return tools


# ── Pattern C-registry (wider) ─────────────────────────────────────────────
# When a server uses @list_tools() returning a runtime registry, find tool
# definitions anywhere in the repo. Two complementary heuristics:
#   1. Tool(name="...") / Tool(name=...) constructors anywhere in the package
#   2. types.Tool(name="...") (MCP SDK qualified form)
#   3. register_*_tool() / @mcp.tool / @app.tool decorators in tool modules
#
# The risk: false positives from test data or mock tools. We mitigate by:
#   - Skipping test files (already done)
#   - Requiring the file to import from `mcp` or live under a `tools/` dir
#     (heuristic for "this is a real tool definition")
TOOL_CTOR_VARIANTS_RE = re.compile(
    r'\b(?:types\.)?Tool\s*\(\s*(?:name\s*=\s*)?["\']([^"\']+)["\']'
)
MCP_IMPORT_RE = re.compile(r'(?:from\s+mcp\b|import\s+mcp\b)')
TOOLS_DIR_RE = re.compile(r'(?:^|/)tools?(?:/|$)')


def has_registry_listtools_handler(repo_dir: Path) -> bool:
    """Return True if the repo has any @<x>.list_tools() handler -- the trigger
    for activating Pattern C-registry. Limits the wider repo-grep to projects
    that actually use the registry pattern."""
    for f in find_py_files(repo_dir):
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        if PATTERN_C_LIST_TOOLS_RE.search(text):
            return True
    return False


def extract_pattern_c_registry(repo_dir: Path):
    """Wider scan: any Tool(name=...) constructor in a file that either
    imports from mcp or lives under a tools/ directory. Returns list of
    (file, name, line, kind).

    Only catches STATIC literal names (Tool(name="literal", ...)). Servers
    that build Tool() with variable names (Tool(name=tool.name, ...)) leave
    no static signal here -- see extract_pattern_c_registry_via_all for
    those cases."""
    found = []
    seen = set()
    for f in find_py_files(repo_dir):
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        in_tools_dir = bool(TOOLS_DIR_RE.search(str(f.relative_to(repo_dir))))
        has_mcp_import = bool(MCP_IMPORT_RE.search(text))
        if not (in_tools_dir or has_mcp_import):
            continue
        for m in TOOL_CTOR_VARIANTS_RE.finditer(text):
            name = m.group(1)
            key = (name, str(f))
            if key in seen:
                continue
            seen.add(key)
            line_no = text[:m.start()].count("\n") + 1
            found.append((f, name, line_no, "pattern_C_registry_repo_tool_ctor"))
    return found


# ── Pattern D: bare-name decorators (`@tool(...)`) imported from a base module
def extract_pattern_d(repo_dir: Path):
    """Find @tool / @register_tool / etc. decorators where the decorator is a
    bare imported function (not `@obj.tool`). Gated to files that import the
    decorator from somewhere AND a fellow file imports from mcp -- avoids
    false positives in unrelated projects."""
    found = []
    # First, gate: does the repo have any mcp import anywhere?
    has_mcp = False
    for f in find_py_files(repo_dir):
        try:
            if MCP_IMPORT_RE.search(f.read_text(errors="replace")):
                has_mcp = True
                break
        except Exception:
            continue
    if not has_mcp:
        return found

    for f in find_py_files(repo_dir):
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        # Check if this file uses one of our recognized decorator names
        used_decorators = set()
        for dec_name in ("tool", "register_tool", "mcp_tool", "server_tool"):
            imp_re = re.compile(
                DECORATOR_IMPORT_RE_TEMPLATE.format(name=dec_name)
            )
            if imp_re.search(text):
                used_decorators.add(dec_name)
        if not used_decorators:
            continue

        lines = text.split("\n")
        for i, line in enumerate(lines):
            m = PATTERN_D_OPEN_RE.match(line)
            if not m or m.group(1) not in used_decorators:
                continue
            # Find close paren
            open_col = line.index("(", m.end() - 1)
            close = find_close_paren(lines, i, open_col)
            if close is None:
                continue
            # Reconstruct body
            if close[0] == i:
                body = line[open_col + 1:close[1]]
            else:
                parts = [line[open_col + 1:]]
                for li in range(i + 1, close[0]):
                    parts.append(lines[li])
                parts.append(lines[close[0]][:close[1]])
                body = "\n".join(parts)
            # Prefer explicit name= kwarg
            mn = re.search(r'\bname\s*=\s*["\']([^"\']+)["\']', body)
            if mn:
                found.append((f, mn.group(1), i + 1, f"pattern_D_decorator_{m.group(1)}"))
                continue
            # Fall back to the def name on the next non-decorator line
            fname, _ = find_def_after(lines, close[0] + 1)
            if fname:
                found.append((f, fname, i + 1, f"pattern_D_decorator_{m.group(1)}_def"))
    return found


# ── Pattern C-registry via __all__ ─────────────────────────────────────────
# Servers like kazkozdev/mcp-search-server expose tool functions via __all__
# in tools/__init__.py. The list of names in __all__ IS the tool name list.
ALL_LIST_RE = re.compile(
    r'__all__\s*[+]?=\s*\[(.*?)\]',
    re.DOTALL,
)
NAME_LITERAL_IN_LIST_RE = re.compile(r'["\']([a-zA-Z_][a-zA-Z0-9_]*)["\']')


def extract_pattern_c_registry_via_all(repo_dir: Path):
    """Read __all__ from any tools/__init__.py (or tools.py) and treat each
    listed name as a tool. False-positive risk: __all__ may include helpers.

    Returns list of (file, name, line, kind). Only activates if the repo also
    has a @list_tools() handler (gate inherited from caller)."""
    found = []
    seen = set()
    for f in find_py_files(repo_dir):
        rel = str(f.relative_to(repo_dir))
        if not (TOOLS_DIR_RE.search(rel) and f.name == "__init__.py"):
            continue
        try:
            text = f.read_text(errors="replace")
        except Exception:
            continue
        for m in ALL_LIST_RE.finditer(text):
            list_body = m.group(1)
            base_line = text[:m.start()].count("\n") + 1
            for n_match in NAME_LITERAL_IN_LIST_RE.finditer(list_body):
                name = n_match.group(1)
                key = (name, str(f))
                if key in seen:
                    continue
                seen.add(key)
                found.append((f, name, base_line, "pattern_C_via_all_export"))
    return found


def analyze_repo(repo_dir: Path):
    current_total = []
    pattern_b_total = []
    pattern_c_total = []
    pattern_c_reg_total = []
    pattern_d_total = []
    for f in find_py_files(repo_dir):
        try:
            content = f.read_text(errors="replace")
        except Exception:
            continue
        lines = content.split("\n")

        cur = extract_current(f, lines)
        cur_caught_lines = {l for _n, l, _k in cur}

        b = extract_pattern_b(f, lines, cur_caught_lines)
        c = extract_pattern_c(f, lines)

        cur_names = {n for n, _l, _k in cur}
        b = [(n, l, k) for n, l, k in b if n not in cur_names]
        c = [(n, l, k) for n, l, k in c if n not in cur_names]

        current_total.extend((f, n, l, k) for n, l, k in cur)
        pattern_b_total.extend((f, n, l, k) for n, l, k in b)
        pattern_c_total.extend((f, n, l, k) for n, l, k in c)

    # Pattern D: bare decorators (`@tool(name="...")`) imported from base
    seen_names = (
        {n for _f, n, _l, _k in current_total}
        | {n for _f, n, _l, _k in pattern_b_total}
        | {n for _f, n, _l, _k in pattern_c_total}
    )
    d = extract_pattern_d(repo_dir)
    d = [(f, n, l, k) for f, n, l, k in d if n not in seen_names]
    pattern_d_total.extend(d)
    seen_names |= {n for _f, n, _l, _k in pattern_d_total}

    # Pattern C-registry: repo-wide. Only activated when the repo has a
    # @list_tools() handler (gate against false positives).
    if has_registry_listtools_handler(repo_dir):
        # Sub-pattern 1: static Tool(name="literal", ...) constructors
        c_reg = extract_pattern_c_registry(repo_dir)
        c_reg = [(f, n, l, k) for f, n, l, k in c_reg if n not in seen_names]
        pattern_c_reg_total.extend(c_reg)
        seen_names |= {n for _f, n, _l, _k in pattern_c_reg_total}
        # Sub-pattern 2: __all__ exports in tools/__init__.py
        c_reg_all = extract_pattern_c_registry_via_all(repo_dir)
        c_reg_all = [(f, n, l, k) for f, n, l, k in c_reg_all if n not in seen_names]
        pattern_c_reg_total.extend(c_reg_all)

    return (current_total, pattern_b_total, pattern_c_total,
            pattern_c_reg_total, pattern_d_total)


def main():
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

    print(f"{'repo':<45} {'cur':>4} {'B':>3} {'C':>3} {'D':>3} {'Cr':>4}  sample new")
    print("-" * 96)
    grand_cur = grand_b = grand_c = grand_creg = grand_d = 0
    for name in pilot_dirs:
        d = CLONE_BASE / name
        if not d.exists():
            print(f"{name:<45}  (no clone)")
            continue
        cur, b, c, c_reg, d_pat = analyze_repo(d)
        grand_cur += len(cur)
        grand_b += len(b)
        grand_c += len(c)
        grand_creg += len(c_reg)
        grand_d += len(d_pat)
        new_names = (
            [n for _f, n, _l, _k in b]
            + [n for _f, n, _l, _k in c]
            + [n for _f, n, _l, _k in d_pat]
            + [n for _f, n, _l, _k in c_reg]
        )
        sample = ", ".join(new_names[:3])
        if len(new_names) > 3:
            sample += f", ... +{len(new_names)-3}"
        print(f"{name:<45} {len(cur):>4} {len(b):>3} {len(c):>3} {len(d_pat):>3} {len(c_reg):>4}  {sample}")
    print("-" * 96)
    print(f"{'TOTAL':<45} {grand_cur:>4} {grand_b:>3} {grand_c:>3} {grand_d:>3} {grand_creg:>4}")
    print()
    total_new = grand_b + grand_c + grand_d + grand_creg
    print(f"Patterns B + C + D + C-registry would recover "
          f"{total_new} additional tool extractions "
          f"in the 15 pilot servers (current Python: {grand_cur}).")
    print()
    print("Legend:")
    print("  cur = approximation of current extractor's recoveries")
    print("  B   = @mcp.tool(annotations=...) kwargs-only decorator")
    print("  C   = @list_tools handler with INLINE Tool() constructors")
    print("  D   = bare decorator like @tool(name=...) imported from base module")
    print("  Cr  = registry-mediated: repo-wide Tool() ctor scan or __all__ exports")


if __name__ == "__main__":
    main()
