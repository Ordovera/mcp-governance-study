/**
 * Analyze remote-only servers via MCP RPC introspection.
 *
 * Reads remote-endpoints-1000.json and runs analyzeServerRemote for each.
 * Also creates minimal reports for remote servers with no endpoint.
 *
 * Usage: node run-remote-1000.mjs [--concurrency N] [--timeout MS]
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { analyzeServerRemote } from "../../packages/cc-mcp-audit/dist/analyze.js";
import { deriveIndicators } from "../../packages/cc-mcp-audit/dist/indicators.js";
import { buildServerReport } from "../../packages/cc-mcp-audit/dist/report.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const concurrency = parseInt(args.find((_, i) => args[i - 1] === "--concurrency") || "4");
const timeoutMs = parseInt(args.find((_, i) => args[i - 1] === "--timeout") || "15000");
const outputFile = resolve(__dirname, "evidence_1000_remote.json");

// Load endpoints and sample
const endpoints = JSON.parse(readFileSync(resolve(__dirname, "remote-endpoints-1000.json"), "utf8"));
const sample = JSON.parse(readFileSync(resolve(__dirname, "sample-1000.json"), "utf8"));
const remoteServers = sample.servers.filter((s) => s.candidate.repositoryUrl === null);

console.error(`Remote servers: ${remoteServers.length}`);
console.error(`With endpoints: ${endpoints.length}`);
console.error(`Without endpoints: ${remoteServers.length - endpoints.length}`);
console.error(`Concurrency: ${concurrency}, Timeout: ${timeoutMs}ms`);
console.error();

const endpointMap = new Map(endpoints.map((e) => [e.name, e]));

// Resume support
let completed = [];
if (existsSync(outputFile)) {
  try {
    const existing = JSON.parse(readFileSync(outputFile, "utf8"));
    completed = existing.servers ?? [];
    console.error(`Resuming: ${completed.length} already complete`);
  } catch { completed = []; }
}
const completedNames = new Set(completed.map((s) => s.name));

async function processOne(server, index, total) {
  const key = server.candidate.key;
  const ep = endpointMap.get(key);

  if (!ep) {
    // No endpoint -- create opaque report
    const emptyPatterns = {
      auth: [], logging: [], gates: [], stagedExecution: [],
      actorAttribution: [], rateLimit: [], leastPrivilege: [],
    };
    const report = buildServerReport(
      key, key, "unknown", [], emptyPatterns,
      ["Remote-only server with no declared endpoint URL. All indicators Indeterminate."],
      null
    );
    report.indicators = deriveIndicators(report);
    // Override all to Indeterminate
    for (const k of Object.keys(report.indicators)) {
      report.indicators[k] = "Indeterminate";
    }
    report.stratum = "remote-only";
    console.error(`[${index + 1}/${total}] ${key} -> NO ENDPOINT (opaque)`);
    return report;
  }

  const startTime = Date.now();
  try {
    const report = await analyzeServerRemote(ep.url, {
      name: key,
      transport: ep.type,
      timeoutMs,
    });
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    const toolCount = report.tools?.length ?? 0;
    console.error(`[${index + 1}/${total}] ${key} -> ${toolCount} tools (${elapsed}s)`);
    report.stratum = "remote-only";
    return report;
  } catch (err) {
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    console.error(`[${index + 1}/${total}] ${key} -> ERROR: ${err.message} (${elapsed}s)`);
    const emptyPatterns = {
      auth: [], logging: [], gates: [], stagedExecution: [],
      actorAttribution: [], rateLimit: [], leastPrivilege: [],
    };
    const report = buildServerReport(
      key, ep.url, "unknown", [], emptyPatterns,
      [`RPC introspection failed: ${err.message}`],
      null
    );
    report.indicators = deriveIndicators(report);
    for (const k of Object.keys(report.indicators)) {
      report.indicators[k] = "Indeterminate";
    }
    report.stratum = "remote-only";
    return report;
  }
}

async function runBatch() {
  const remaining = remoteServers.filter((s) => !completedNames.has(s.candidate.key));
  console.error(`Remaining: ${remaining.length}`);

  const results = [...completed];
  let nextIndex = 0;

  async function worker() {
    while (nextIndex < remaining.length) {
      const idx = nextIndex++;
      const server = remaining[idx];
      const report = await processOne(server, completed.length + idx, completed.length + remaining.length);
      results.push(report);

      if (results.length % 10 === 0) {
        writeFileSync(outputFile, JSON.stringify({ servers: results }, null, 2));
      }
    }
  }

  const workers = Array.from(
    { length: Math.min(concurrency, remaining.length) },
    () => worker()
  );
  await Promise.all(workers);

  writeFileSync(outputFile, JSON.stringify({ servers: results }, null, 2));
  console.error(`\nComplete: ${results.length} remote servers`);

  // Summary
  const withTools = results.filter((r) => (r.tools?.length ?? 0) > 0);
  const totalTools = results.reduce((n, r) => n + (r.tools?.length ?? 0), 0);
  const opaque = results.filter((r) =>
    r.warnings?.some((w) => w.includes("no declared endpoint"))
  );
  const rpcFailed = results.filter((r) =>
    r.warnings?.some((w) => w.includes("RPC introspection failed"))
  );

  console.error(`With tools: ${withTools.length}`);
  console.error(`Total tools: ${totalTools}`);
  console.error(`Opaque (no endpoint): ${opaque.length}`);
  console.error(`RPC failures: ${rpcFailed.length}`);
}

runBatch().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
