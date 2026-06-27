/**
 * Batch runner for LLM verification of the pilot corpus.
 * Runs verification on all cached source-available servers.
 *
 * Usage: node run-verify-batch.mjs [--concurrency N] [--output FILE]
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { verifyServer, extractVerifyRegions } from "./dist/verify.js";
import { selectProvider } from "./dist/screen-providers.js";

const args = process.argv.slice(2);
const concurrency = parseInt(args.find((_, i) => args[i - 1] === "--concurrency") || "4");
const outputFile = args.find((_, i) => args[i - 1] === "--output") || "verify-results-n151.json";

const paths = JSON.parse(readFileSync("verify-paths.json", "utf8"));
const provider = selectProvider("claude-code", "claude-opus-4-6");

console.error(`Verifying ${paths.length} servers with concurrency=${concurrency}`);
console.error(`Provider: ${provider.id} model: ${provider.model}`);
console.error(`Output: ${outputFile}`);
console.error();

// Resume support: skip already-verified servers
let completed = [];
if (existsSync(outputFile)) {
  try {
    completed = JSON.parse(readFileSync(outputFile, "utf8"));
    console.error(`Resuming: ${completed.length} already complete`);
  } catch {
    completed = [];
  }
}
const completedNames = new Set(completed.map((r) => r.name));
const remaining = paths.filter((p) => !completedNames.has(p.name));
console.error(`Remaining: ${remaining.length}`);
console.error();

async function processOne(entry, index, total) {
  const startTime = Date.now();
  try {
    const result = await verifyServer(entry.path, provider);
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    const status = result.isMcpServer ? "MCP" : "NOT-MCP";
    console.error(
      `[${index + 1}/${total}] ${entry.name} -> ${status} (${result.confidence}), ` +
      `${result.tools.length} tools, ${elapsed}s`
    );
    return {
      name: entry.name,
      source: entry.source,
      ...result,
    };
  } catch (err) {
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    console.error(`[${index + 1}/${total}] ${entry.name} -> ERROR: ${err.message} (${elapsed}s)`);
    return {
      name: entry.name,
      source: entry.source,
      isMcpServer: false,
      confidence: "low",
      evidence: `Verification error: ${err.message}`,
      tools: [],
      extractionNotes: "Verification failed",
      metadata: { model: provider.model, promptVersion: "v1", inputTokens: 0, outputTokens: 0, regionsIncluded: 0, totalCharsSubmitted: 0 },
    };
  }
}

// Run with limited concurrency
async function runBatch() {
  const results = [...completed];
  let nextIndex = 0;

  async function worker() {
    while (nextIndex < remaining.length) {
      const idx = nextIndex++;
      const entry = remaining[idx];
      const result = await processOne(entry, completed.length + idx, completed.length + remaining.length);
      results.push(result);

      // Save after each completion (resume support)
      if (results.length % 5 === 0) {
        writeFileSync(outputFile, JSON.stringify(results, null, 2));
      }
    }
  }

  const workers = Array.from({ length: Math.min(concurrency, remaining.length) }, () => worker());
  await Promise.all(workers);

  writeFileSync(outputFile, JSON.stringify(results, null, 2));
  console.error(`\nComplete: ${results.length} servers verified`);
  console.error(`Written to ${outputFile}`);

  // Summary
  const mcpCount = results.filter((r) => r.isMcpServer).length;
  const totalTools = results.reduce((n, r) => n + r.tools.length, 0);
  console.error(`\nMCP servers: ${mcpCount}/${results.length}`);
  console.error(`Total LLM-extracted tools: ${totalTools}`);
}

runBatch().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
