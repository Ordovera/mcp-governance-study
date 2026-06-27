/**
 * Draw a stratified random sample of N=1,000 from the canonical snapshot.
 *
 * Uses the same seeded PRNG (mulberry32) as the pilot but with:
 *   - Scaled-up stratum targets (from workplan Phase 4)
 *   - A different seed to avoid overlap with the pilot sample
 *   - Exclusion of the 10 non-MCP servers identified in Phase 2
 *
 * Usage: node draw-sample-1000.mjs [--seed N] [--output FILE]
 */

import { readFileSync, writeFileSync } from "node:fs";
import { drawSample, STRATA } from "../../packages/cc-mcp-audit/dist/sampler.js";

const args = process.argv.slice(2);
const seed = parseInt(args.find((_, i) => args[i - 1] === "--seed") || "20260512");
const outputFile = args.find((_, i) => args[i - 1] === "--output") || "sample-1000.json";

// Load canonical snapshot
const snapshot = JSON.parse(readFileSync("canonical-snapshot-2026-05-04.json", "utf8"));

// Exclude known non-MCP servers from Phase 2 verification
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
    (c) => !c.repositoryUrl || !NON_MCP_REPOS.has(c.repositoryUrl)
  ),
};

console.error(`Population: ${snapshot.candidates.length} -> ${filteredSnapshot.candidates.length} after excluding ${NON_MCP_REPOS.size} known non-MCP repos`);

// Phase 4 stratum targets (from workplan)
const STRATA_1000 = STRATA.map((s) => {
  const targets = {
    "npm+registry": 190,
    "npm-only": 220,
    "pypi+registry": 155,
    "pypi-only": 155,
    "other-ecosystem": 95,
    "remote-only": 185,
  };
  return { ...s, targetN: targets[s.name] ?? s.targetN };
});

const result = drawSample(filteredSnapshot, seed, STRATA_1000);

console.error(`\nSample drawn: ${result.totalN} servers (seed=${seed})`);
console.error("\nStratum breakdown:");
for (const s of result.strata) {
  console.error(`  ${s.name}: ${s.actualN}/${s.targetN} (population: ${s.populationSize})`);
}

// Also exclude pilot sample servers to get a fully independent draw
// (optional -- uncomment if desired for non-overlapping samples)
// const pilotSample = JSON.parse(readFileSync("sample-160.json", "utf8"));
// const pilotUrls = new Set(pilotSample.servers.map(s => s.candidate.repositoryUrl));

writeFileSync(outputFile, JSON.stringify(result, null, 2));
console.error(`\nWritten to ${outputFile}`);

// Print source-available vs remote-only counts
const sourceAvail = result.servers.filter((s) => s.candidate.repositoryUrl !== null).length;
const remoteOnly = result.servers.filter((s) => s.candidate.repositoryUrl === null).length;
console.error(`\nSource-available: ${sourceAvail}, Remote-only: ${remoteOnly}`);
