/**
 * LLM verification batch runner for the N=1,000 corpus.
 *
 * Adapts run-verify-batch.mjs for the larger sample with:
 *   - Configurable input/output files
 *   - Default concurrency of 4
 *   - Resume support (reads existing output file)
 *   - Per-completion saves every 5 completions
 *
 * Usage: node run-verify-1000.mjs [--concurrency N] [--input FILE] [--output FILE]
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { verifyServer } from "../../packages/cc-mcp-audit/dist/verify.js";
import { selectProvider } from "../../packages/cc-mcp-audit/dist/screen-providers.js";

const args = process.argv.slice(2);
const concurrency = parseInt(args.find((_, i) => args[i - 1] === "--concurrency") || "4");
const inputFile = args.find((_, i) => args[i - 1] === "--input") || "verify-paths-1000.json";
const outputFile = args.find((_, i) => args[i - 1] === "--output") || "verify-results-1000.json";

const paths = JSON.parse(readFileSync(inputFile, "utf8"));
const provider = selectProvider("claude-code", "claude-opus-4-6");

console.error(`Verifying ${paths.length} servers with concurrency=${concurrency}`);
console.error(`Provider: ${provider.id} model: ${provider.model}`);
console.error(`Input: ${inputFile}`);
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

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function processOne(entry, index, total, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
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
        stratum: entry.stratum,
        ...result,
      };
    } catch (err) {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      if (attempt < maxRetries) {
        const backoff = attempt * 5000; // 5s, 10s
        console.error(
          `[${index + 1}/${total}] ${entry.name} -> RETRY ${attempt}/${maxRetries}: ${err.message.slice(0, 80)} (${elapsed}s, wait ${backoff / 1000}s)`
        );
        await sleep(backoff);
        continue;
      }
      console.error(`[${index + 1}/${total}] ${entry.name} -> FAILED after ${maxRetries} attempts: ${err.message.slice(0, 80)} (${elapsed}s)`);
      return {
        name: entry.name,
        source: entry.source,
        stratum: entry.stratum,
        isMcpServer: false,
        confidence: "low",
        evidence: `Verification error after ${maxRetries} attempts: ${err.message}`,
        tools: [],
        extractionNotes: "Verification failed",
        metadata: {
          model: provider.model,
          promptVersion: "v1",
          inputTokens: 0,
          outputTokens: 0,
          regionsIncluded: 0,
          totalCharsSubmitted: 0,
        },
      };
    }
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

      // Save after every 5 completions (resume support)
      if (results.length % 5 === 0) {
        writeFileSync(outputFile, JSON.stringify(results, null, 2));
      }

      // Pause between calls to avoid rate limiting (5s baseline)
      if (concurrency === 1) await sleep(5000);
    }
  }

  const workers = Array.from(
    { length: Math.min(concurrency, remaining.length) },
    () => worker()
  );
  await Promise.all(workers);

  writeFileSync(outputFile, JSON.stringify(results, null, 2));
  console.error(`\nComplete: ${results.length} servers verified`);
  console.error(`Written to ${outputFile}`);

  // Summary
  const mcpCount = results.filter((r) => r.isMcpServer).length;
  const notMcpCount = results.filter((r) => !r.isMcpServer).length;
  const totalTools = results.reduce((n, r) => n + r.tools.length, 0);
  console.error(`\nMCP servers: ${mcpCount}/${results.length}`);
  console.error(`Not MCP: ${notMcpCount}`);
  console.error(`Total LLM-extracted tools: ${totalTools}`);

  // Per-stratum summary
  const byStratum = {};
  for (const r of results) {
    const s = r.stratum || "unknown";
    if (!byStratum[s]) byStratum[s] = { total: 0, mcp: 0, tools: 0 };
    byStratum[s].total++;
    if (r.isMcpServer) byStratum[s].mcp++;
    byStratum[s].tools += r.tools.length;
  }
  console.error("\nPer-stratum:");
  for (const [stratum, stats] of Object.entries(byStratum)) {
    console.error(`  ${stratum}: ${stats.mcp}/${stats.total} MCP, ${stats.tools} tools`);
  }
}

runBatch().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
