// One-off: re-extract tools from every cached corpus clone and record the
// per-clone tool-name list. Run twice (with/without CC_MCP_NO_STRIP) to isolate
// the effect of the comment/docstring stripping guards. Gitignored research dir.
import { extractTools } from "../../packages/cc-mcp-audit/dist/extract.js";
import { readdirSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";

const root = join(tmpdir(), "cc-mcp-audit");
const out = process.argv[2];
if (!out) {
  console.error("usage: node revalidate-comment-guard.mjs <out.json>");
  process.exit(1);
}

const clones = readdirSync(root).filter((e) => {
  try {
    return statSync(join(root, e)).isDirectory();
  } catch {
    return false;
  }
});

const result = {};
let done = 0;
for (const c of clones) {
  try {
    const tools = extractTools(join(root, c));
    result[c] = tools.map((t) => t.name).sort();
  } catch (e) {
    result[c] = { error: String(e?.message ?? e) };
  }
  if (++done % 200 === 0) console.error(`  ...${done}/${clones.length}`);
}

writeFileSync(out, JSON.stringify(result, null, 0));
const totalTools = Object.values(result).reduce(
  (n, v) => n + (Array.isArray(v) ? v.length : 0),
  0
);
console.error(`wrote ${out}: ${clones.length} clones, ${totalTools} total tools`);
