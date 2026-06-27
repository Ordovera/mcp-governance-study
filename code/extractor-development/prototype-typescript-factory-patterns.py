"""
Prototype Patterns E, F, G, H -- TypeScript factory-server tool extractors.

These 4 patterns recover tools from servers that export `createServer()` but
use a non-SDK registration shape that the current extractor does not handle.

  Pattern E: defineTool(server, "literal_name", description, schema, handler, ...)
    Custom wrapper around server.registerTool. Match: any function call where
    the callee is `defineTool` (or `createTool`, `addTool`), first arg is
    identifier, second arg is string literal.
    Target: klodr--mercury-invoicing-mcp (35 tools across src/tools/*.ts)

  Pattern F: registerTool(server, TOOL_NAME, DESCRIPTION, schema, ...)
    Wrapper where tool name and description are const identifiers defined in
    same file. Match: `registerTool(arg1, IDENT, ...)` + same-file
    `const IDENT = "literal"`.
    Target: wearehoust--front-mcp (26 tools across src/tools/*.tool.ts)

  Pattern G: array-then-loop with imported identifiers
    Match in server.ts: `const tools = [{ name: IDENT, description: IDENT, ... }, ...]`
    followed by `for (...) server.tool(tool.name, ...)`. Resolve each IDENT
    cross-file via its `import { IDENT } from "<path>"` statement.
    Target: cyberash-dev--moex-mcp (20 tools across src/features/*/handler.ts)

  Pattern H: manifest-driven loop with record literal
    Match in server.ts: `const NAME: Record<string, X> = { key1: ..., ...spread }`
    + later `for (... of Object.entries(NAME)) ... .registerTool(VAR, ...)`.
    Resolve spreads to imported `export const NAME = { ... }` and extract
    keys.
    Target: listbee-dev--listbee-mcp (21 tools)

Each function returns a set of tool names found. Run as a script to validate
against the 4 cached clones; counts must match LLM-supplementary tool counts
(20, 21, 26, 35).

Stdlib only.
"""

import re
import sys
from pathlib import Path
from tempfile import gettempdir


CLONE_BASE = Path(gettempdir()) / "cc-mcp-audit"

TARGETS = {
    "cyberash-dev--moex-mcp":       ("G", 20),
    "listbee-dev--listbee-mcp":     ("H", 21),
    "wearehoust--front-mcp":        ("F", 26),
    "klodr--mercury-invoicing-mcp": ("E", 35),
}


# ── Shared helpers ────────────────────────────────────────────────────────

_IMPORT_RE = re.compile(
    r"""import\s*\{([^}]+)\}\s*from\s*["']([^"']+)["']""",
    re.DOTALL,
)
_CONST_LITERAL_RE = re.compile(
    r"""(?:export\s+)?const\s+(\w+)\s*(?::\s*[^=]+)?=\s*["']([^"']+)["']"""
)


def parse_imports(src: str):
    """Map each imported identifier to its source path.
    Returns: { ident: "./path" }"""
    out = {}
    for m in _IMPORT_RE.finditer(src):
        names_raw, path = m.group(1), m.group(2)
        for n in names_raw.split(","):
            n = n.strip()
            if not n:
                continue
            # Handle `as` aliases: keep the alias name
            if " as " in n:
                _, n = n.split(" as ")
                n = n.strip()
            # Strip "type" prefix
            if n.startswith("type "):
                n = n[5:].strip()
            out[n] = path
    return out


def parse_const_literals(src: str):
    """Map each top-level `const IDENT = "literal"` to its value.
    Returns: { ident: "literal_value" }"""
    out = {}
    for m in _CONST_LITERAL_RE.finditer(src):
        out[m.group(1)] = m.group(2)
    return out


def resolve_import_path(root: Path, importing_file: Path, import_spec: str):
    """Resolve a relative import to an absolute file path on disk.
    Handles common TS extension dropping (.js -> .ts)."""
    if not import_spec.startswith("."):
        return None
    base = (importing_file.parent / import_spec).resolve()
    candidates = [
        base,
        base.with_suffix(".ts"),
        base.with_suffix(".mts"),
        Path(str(base).replace(".js", ".ts")),
        Path(str(base).replace(".js", ".mts")),
        base / "index.ts",
        base / "index.mts",
    ]
    for c in candidates:
        if c.is_file():
            return c
    return None


def repo_ts_files(root: Path):
    """All .ts/.mts files in the repo excluding common non-source dirs."""
    out = []
    for p in root.rglob("*.ts"):
        s = str(p)
        if any(seg in s for seg in ("/node_modules/", "/dist/", "/build/", "/.git/", "/coverage/")):
            continue
        out.append(p)
    for p in root.rglob("*.mts"):
        s = str(p)
        if any(seg in s for seg in ("/node_modules/", "/dist/", "/build/", "/.git/", "/coverage/")):
            continue
        out.append(p)
    return out


# ── Pattern E: defineTool(server, "literal", ...) ────────────────────────

_E_RE = re.compile(
    r"""\b(?:defineTool|createTool|addTool)\s*\(\s*\w+\s*,\s*["']([^"']+)["']""",
)


def extract_pattern_e(root: Path):
    """Find defineTool(...) / createTool(...) / addTool(...) calls anywhere
    in the repo's TS files that take server-identifier + literal name."""
    found = set()
    for p in repo_ts_files(root):
        try:
            src = p.read_text(errors="ignore")
        except Exception:
            continue
        for m in _E_RE.finditer(src):
            found.add(m.group(1))
    return found


# ── Pattern F: registerTool(server, IDENT, IDENT_DESC, ...) ──────────────

_F_RE = re.compile(
    r"""\bregisterTool\s*\(\s*\w+\s*,\s*(\w+)\s*,""",
)


def extract_pattern_f(root: Path):
    """Find local-wrapper registerTool(server, IDENT, ...) calls where IDENT
    resolves to a same-file `const IDENT = "literal"` declaration.

    Restricted to calls where `registerTool` is imported from a LOCAL path
    (not from @modelcontextprotocol/sdk) — otherwise this would shadow the
    SDK pattern which the current extractor already handles.
    """
    found = set()
    for p in repo_ts_files(root):
        try:
            src = p.read_text(errors="ignore")
        except Exception:
            continue
        imports = parse_imports(src)
        if "registerTool" in imports and not imports["registerTool"].startswith("."):
            continue  # SDK-import, leave to existing extractor
        consts = parse_const_literals(src)
        for m in _F_RE.finditer(src):
            ident = m.group(1)
            if ident in consts:
                found.add(consts[ident])
    return found


# ── Pattern G: array-then-loop with imported identifiers ─────────────────

_G_ARRAY_RE = re.compile(
    r"""const\s+\w+\s*=\s*\[(.*?)\]""",
    re.DOTALL,
)
_G_NAME_FIELD_RE = re.compile(r"""\bname\s*:\s*(\w+)\b""")
_G_LOOP_RE = re.compile(
    r"""\bfor\s*\(\s*const\s+\w+\s+of\s+\w+\s*\)\s*\{[^}]*?\.(?:tool|registerTool)\s*\(\s*\w+\.name""",
    re.DOTALL,
)


def extract_pattern_g(root: Path):
    """Find `const tools = [{ name: IDENT, ... }, ...]` followed by a
    `for (... of tools) server.tool(tool.name, ...)` loop. Resolve each
    IDENT to a literal by following the import to the source file's
    `export const IDENT = "literal"`."""
    found = set()
    for p in repo_ts_files(root):
        try:
            src = p.read_text(errors="ignore")
        except Exception:
            continue
        # Quick reject: no loop pattern
        if not _G_LOOP_RE.search(src):
            continue
        imports = parse_imports(src)
        for m in _G_ARRAY_RE.finditer(src):
            body = m.group(1)
            for nm in _G_NAME_FIELD_RE.finditer(body):
                ident = nm.group(1)
                # Resolve via local consts first (in case in-file)
                local_consts = parse_const_literals(src)
                if ident in local_consts:
                    found.add(local_consts[ident])
                    continue
                # Cross-file: follow the import
                if ident not in imports:
                    continue
                target = resolve_import_path(root, p, imports[ident])
                if target is None:
                    continue
                try:
                    target_src = target.read_text(errors="ignore")
                except Exception:
                    continue
                target_consts = parse_const_literals(target_src)
                if ident in target_consts:
                    found.add(target_consts[ident])
    return found


# ── Pattern H: manifest-driven loop with record-literal + spread ─────────

_H_RECORD_RE = re.compile(
    r"""const\s+(\w+)\s*(?::\s*Record\s*<\s*string\s*,[^>]+>)?\s*=\s*\{(.*?)\n\}""",
    re.DOTALL,
)
_H_LOOP_RE = re.compile(
    r"""for\s*\(\s*const\s+\[\s*(\w+)[\s,].*?Object\.entries\s*\(\s*(\w+)\s*\)\s*\).*?\.(?:tool|registerTool)\s*\(\s*\1""",
    re.DOTALL,
)
_H_KEY_RE = re.compile(r"""^\s*["']?(\w+)["']?\s*:""", re.MULTILINE)
_H_SPREAD_RE = re.compile(r"""\.\.\.(\w+)\b""")


def extract_keys_from_record_body(body: str):
    """Extract top-level string keys from a record literal body, ignoring
    nested objects.

    A key `foo:` is "top-level" if it appears while brace depth is 0 — i.e.
    BEFORE we descend into a nested object literal. We snapshot the depth
    at the start of each line: if start-of-line depth is 0, the `KEY:` at
    line start is a top-level key regardless of what nesting opens later
    on that same line (e.g. `upload_file: z.object({ ... })`).
    """
    out = set()
    spreads = []
    depth = 0
    in_str = False
    str_ch = None
    line_buf = []
    line_start_depth = 0
    for ch in body:
        if in_str:
            if ch == str_ch:
                in_str = False
            line_buf.append(ch)
            continue
        if ch in ('"', "'", "`"):
            in_str = True
            str_ch = ch
            line_buf.append(ch)
            continue
        if ch == "\n":
            if line_start_depth == 0:
                line = "".join(line_buf)
                km = _H_KEY_RE.match(line)
                if km:
                    out.add(km.group(1))
                for sm in _H_SPREAD_RE.finditer(line):
                    spreads.append(sm.group(1))
            line_buf = []
            line_start_depth = depth  # next line's starting depth
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        line_buf.append(ch)
    if line_buf and line_start_depth == 0:
        line = "".join(line_buf)
        km = _H_KEY_RE.match(line)
        if km:
            out.add(km.group(1))
        for sm in _H_SPREAD_RE.finditer(line):
            spreads.append(sm.group(1))
    return out, spreads


def extract_pattern_h(root: Path):
    """Find record literals iterated via Object.entries + .registerTool(VAR, ...)
    inside the loop body. Extract keys; recursively resolve spreads to imported
    record literals.
    """
    found = set()
    for p in repo_ts_files(root):
        try:
            src = p.read_text(errors="ignore")
        except Exception:
            continue
        # Find loop with VAR + RECORD pair
        loop_match = _H_LOOP_RE.search(src)
        if not loop_match:
            continue
        var_name, record_name = loop_match.group(1), loop_match.group(2)
        # Find the record literal
        for rm in _H_RECORD_RE.finditer(src):
            if rm.group(1) != record_name:
                continue
            keys, spreads = extract_keys_from_record_body(rm.group(2))
            found |= keys
            # Resolve spreads
            imports = parse_imports(src)
            for sp in spreads:
                if sp not in imports:
                    continue
                target = resolve_import_path(root, p, imports[sp])
                if target is None:
                    continue
                try:
                    tsrc = target.read_text(errors="ignore")
                except Exception:
                    continue
                for trm in _H_RECORD_RE.finditer(tsrc):
                    if trm.group(1) == sp:
                        sk, _ = extract_keys_from_record_body(trm.group(2))
                        found |= sk
    return found


# ── Driver ─────────────────────────────────────────────────────────────────


EXTRACTORS = {
    "E": extract_pattern_e,
    "F": extract_pattern_f,
    "G": extract_pattern_g,
    "H": extract_pattern_h,
}


def main():
    print(f"Clone base: {CLONE_BASE}\n")
    grand_found = 0
    grand_expected = 0
    for slug, (pattern_letter, expected) in TARGETS.items():
        repo = CLONE_BASE / slug
        if not repo.is_dir():
            print(f"  MISSING: {slug}")
            continue
        extractor = EXTRACTORS[pattern_letter]
        tools = extractor(repo)
        n = len(tools)
        grand_found += n
        grand_expected += expected
        status = "OK " if n >= expected else "LOW"
        print(f"  [{pattern_letter}] {status} {slug:<40s}  found={n:>3}  expected={expected}")
        if n != expected and n < 50:
            for t in sorted(tools)[:10]:
                print(f"        {t}")
            if n > 10:
                print(f"        ... and {n - 10} more")
        elif n > 0:
            for t in sorted(tools)[:3]:
                print(f"        {t}")
            print(f"        ... ({n - 3} more)")
    print()
    print(f"Total found:     {grand_found}")
    print(f"Total expected:  {grand_expected}")
    if grand_found < grand_expected:
        print("WARN: some patterns under-recovered. Inspect output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
