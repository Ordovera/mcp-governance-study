/**
 * Draw replacement servers for dead repos and non-MCP exclusions.
 *
 * Reads failed_servers_1000.json and verify-results-1000.json to identify
 * servers needing replacement, then draws from the same strata using a
 * different seed offset.
 *
 * Usage: node draw-replacements.mjs [--output FILE]
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { drawSample, STRATA } from "../../packages/cc-mcp-audit/dist/sampler.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const outputFile = args.find((_, i) => args[i - 1] === "--output") || "replacements-1000.json";

// Load the original sample to know which servers are already drawn
const sample = JSON.parse(readFileSync(join(__dirname, "sample-1000.json"), "utf8"));
const originalKeys = new Set(sample.servers.map((s) => s.candidate.key));

// Identify servers needing replacement
const needsReplacement = new Map(); // stratum -> count

// 1. Failed servers (dead repos, clone failures)
const failedFile = join(__dirname, "failed_servers_1000.json");
if (existsSync(failedFile)) {
  const failed = JSON.parse(readFileSync(failedFile, "utf8"));
  for (const f of failed) {
    const stratum = f.stratum || "unknown";
    needsReplacement.set(stratum, (needsReplacement.get(stratum) || 0) + 1);
  }
}

// 2. Non-MCP servers from LLM verification
const verifyFile = join(__dirname, "verify-results-1000.json");
if (existsSync(verifyFile)) {
  const verified = JSON.parse(readFileSync(verifyFile, "utf8"));
  for (const v of verified) {
    if (!v.isMcpServer && v.confidence !== "low") {
      const stratum = v.stratum || "unknown";
      needsReplacement.set(stratum, (needsReplacement.get(stratum) || 0) + 1);
    }
  }
}

if (needsReplacement.size === 0) {
  console.error("No replacements needed.");
  process.exit(0);
}

console.error("Replacements needed per stratum:");
let totalNeeded = 0;
for (const [stratum, count] of needsReplacement.entries()) {
  console.error(`  ${stratum}: ${count}`);
  totalNeeded += count;
}
console.error(`Total: ${totalNeeded}`);

// Load canonical snapshot (excluding known non-MCP repos from Phase 2)
const snapshot = JSON.parse(readFileSync(join(__dirname, "canonical-snapshot-2026-05-04.json"), "utf8"));

const NON_MCP_REPOS = new Set([
  "https://github.com/lithtrix/api",
  "https://github.com/Summit53/mcp-server",
  "https://github.com/yjcho9317/mcp-fence",
  "https://github.com/agentailor/create-mcp-server",
  "https://github.com/digital-defiance/ai-capabilities-suite",
  "https://github.com/nexus-lab-zen/nexus-lab",
  "https://github.com/PengSpirit/mcp-probe",
  "https://github.com/onikora/mcp-registry",
  "https://github.com/feedoracle/feedoracle-managed-agents",
  "https://github.com/devopness/devopness",
]);

const filteredSnapshot = {
  ...snapshot,
  candidates: snapshot.candidates.filter(
    (c) => !originalKeys.has(c.key) && (!c.repositoryUrl || !NON_MCP_REPOS.has(c.repositoryUrl))
  ),
};

console.error(`\nEligible candidates (excluding original sample + known non-MCP): ${filteredSnapshot.candidates.length}`);

// Draw replacements per stratum with offset seed
const replacementSeed = 20260512 + 1000; // Offset from original seed
const replacementStrata = STRATA.map((s) => ({
  ...s,
  targetN: needsReplacement.get(s.name) || 0,
}));

const result = drawSample(filteredSnapshot, replacementSeed, replacementStrata);

console.error(`\nReplacement draw: ${result.totalN} servers (seed=${replacementSeed})`);
for (const s of result.strata) {
  if (s.targetN > 0) {
    console.error(`  ${s.name}: ${s.actualN}/${s.targetN}`);
  }
}

writeFileSync(resolve(__dirname, outputFile), JSON.stringify(result, null, 2));
console.error(`\nWritten to ${outputFile}`);
