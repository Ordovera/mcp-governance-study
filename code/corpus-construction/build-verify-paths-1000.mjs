/**
 * Build verify-paths-1000.json from completed analysis batches.
 *
 * Scans evidence_1000_batch*.json files, extracts server names and
 * local clone paths, and writes verify-paths-1000.json for the
 * LLM verification batch runner.
 *
 * Usage: node build-verify-paths-1000.mjs
 */

import { readFileSync, writeFileSync, readdirSync, existsSync } from "node:fs";
import { resolve, dirname, join } from "node:path";
import { tmpdir } from "node:os";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));

// Find all completed batch files
const batchFiles = readdirSync(__dirname)
  .filter((f) => f.match(/^evidence_1000_batch\d+\.json$/))
  .sort((a, b) => {
    const na = parseInt(a.match(/\d+/)?.[0] ?? "0");
    const nb = parseInt(b.match(/\d+/)?.[0] ?? "0");
    return na - nb;
  });

console.error(`Found ${batchFiles.length} batch files`);

// Load stratum map for metadata
const stratumMap = existsSync(join(__dirname, "stratum-map-1000.json"))
  ? JSON.parse(readFileSync(join(__dirname, "stratum-map-1000.json"), "utf8"))
  : {};

const cloneBase = join(tmpdir(), "cc-mcp-audit");
const paths = [];
const seen = new Set();

for (const file of batchFiles) {
  const data = JSON.parse(readFileSync(join(__dirname, file), "utf8"));
  const envelopes = data.envelopes ?? [];

  for (const envelope of envelopes) {
    const server = envelope.fullReport ?? {};
    const name = server.name ?? envelope.subject?.name;
    const source = server.source ?? envelope.subject?.source;

    // Skip servers that failed to clone
    if (server.warnings?.some((w) => w.startsWith("Analysis failed:"))) continue;
    // Skip duplicates
    if (!name || seen.has(name)) continue;
    seen.add(name);

    // Determine local path from source URL
    // cc-mcp-audit clones to os.tmpdir()/cc-mcp-audit/owner--repo/
    // Sources may be https://github.com/... or git+https://github.com/...
    const normalized = source?.replace(/^git\+/, "") ?? "";
    if (!normalized.startsWith("https://github.com/")) continue;

    const parts = normalized.replace("https://github.com/", "").replace(/\.git$/, "").split("/");
    if (parts.length < 2) continue;
    const owner = parts[0];
    const repo = parts[1];
    const localDir = join(cloneBase, `${owner}--${repo}`);

    if (!existsSync(localDir)) {
      console.error(`  SKIP ${name}: clone dir not found at ${localDir}`);
      continue;
    }

    paths.push({
      name,
      source,
      path: localDir,
      stratum: stratumMap[name]?.stratum ?? "unknown",
    });
  }
}

console.error(`\nVerify paths: ${paths.length} servers`);

const outputFile = resolve(__dirname, "verify-paths-1000.json");
writeFileSync(outputFile, JSON.stringify(paths, null, 2));
console.error(`Written to verify-paths-1000.json`);
