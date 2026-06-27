/**
 * Batch analysis runner for the N=1,000 sample.
 *
 * Splits source-available servers into batches of 20,
 * runs cc-mcp-audit in evidence format, and supports resume.
 * Remote-only servers are handled in a separate pass.
 *
 * Usage: node run-analysis-1000.mjs [--batch-size N] [--start-batch N]
 */

import { readFileSync, writeFileSync, existsSync, unlinkSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const cliPath = resolve(__dirname, "../../packages/cc-mcp-audit/dist/cli.js");

const args = process.argv.slice(2);
const batchSize = parseInt(args.find((_, i) => args[i - 1] === "--batch-size") || "20");
const startBatch = parseInt(args.find((_, i) => args[i - 1] === "--start-batch") || "1");
const sampleFile = args.find((_, i) => args[i - 1] === "--sample") || "sample-1000.json";

const sample = JSON.parse(readFileSync(sampleFile, "utf8"));

// Split into source-available and remote-only
const sourceServers = sample.servers.filter((s) => s.candidate.repositoryUrl !== null);
const remoteServers = sample.servers.filter((s) => s.candidate.repositoryUrl === null);

console.error(`Total: ${sample.totalN} servers`);
console.error(`Source-available: ${sourceServers.length}`);
console.error(`Remote-only: ${remoteServers.length}`);
console.error(`Batch size: ${batchSize}`);

// Create batches
const batches = [];
for (let i = 0; i < sourceServers.length; i += batchSize) {
  batches.push(sourceServers.slice(i, i + batchSize));
}

console.error(`Total batches: ${batches.length}`);
console.error();

// Process each batch
let totalProcessed = 0;
let totalFailed = 0;
const failedServers = [];

for (let batchIdx = 0; batchIdx < batches.length; batchIdx++) {
  const batchNum = batchIdx + 1;
  const outputFile = resolve(__dirname, `evidence_1000_batch${batchNum}.json`);

  // Resume support: skip already-completed batches
  if (batchNum < startBatch) {
    console.error(`[Batch ${batchNum}/${batches.length}] Skipped (before start-batch)`);
    continue;
  }

  if (existsSync(outputFile)) {
    try {
      const existing = JSON.parse(readFileSync(outputFile, "utf8"));
      const count = existing.envelopes?.length ?? 0;
      console.error(`[Batch ${batchNum}/${batches.length}] Already complete (${count} servers)`);
      totalProcessed += count;
      continue;
    } catch {
      // Corrupted file, re-run
    }
  }

  const batch = batches[batchIdx];

  // Write batch candidates file
  const candidatesFile = resolve(__dirname, `batch_1000_input_${batchNum}.json`);
  const candidates = batch.map((s) => ({
    source: s.candidate.repositoryUrl,
    name: s.candidate.key,
  }));
  writeFileSync(candidatesFile, JSON.stringify(candidates, null, 2));

  console.error(`[Batch ${batchNum}/${batches.length}] Processing ${batch.length} servers...`);
  const startTime = Date.now();

  try {
    execFileSync("node", [cliPath, "-c", candidatesFile, "-f", "evidence", "-o", outputFile], {
      stdio: ["pipe", "pipe", "inherit"],
      timeout: 600_000, // 10 min per batch
      cwd: __dirname,
    });

    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);

    // Count results -- evidence format uses envelopes[], each with fullReport
    const result = JSON.parse(readFileSync(outputFile, "utf8"));
    const envelopes = result.envelopes ?? [];
    const serverCount = envelopes.length;
    const failCount = envelopes.filter(
      (e) => e.fullReport?.warnings?.some((w) => w.startsWith("Analysis failed:"))
    ).length;

    totalProcessed += serverCount;
    totalFailed += failCount;

    if (failCount > 0) {
      const failed = envelopes
        .filter((e) => e.fullReport?.warnings?.some((w) => w.startsWith("Analysis failed:")))
        .map((e) => ({
          name: e.fullReport?.name ?? e.subject?.name,
          source: e.fullReport?.source ?? e.subject?.source,
          stratum: batch.find((b) => b.candidate.key === (e.fullReport?.name ?? e.subject?.name))?.stratum,
        }));
      failedServers.push(...failed);
    }

    console.error(
      `[Batch ${batchNum}/${batches.length}] Done: ${serverCount} servers, ${failCount} failed, ${elapsed}s`
    );
  } catch (err) {
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
    console.error(
      `[Batch ${batchNum}/${batches.length}] BATCH FAILED after ${elapsed}s: ${err.message}`
    );
    // Mark all servers in this batch as failed
    for (const s of batch) {
      failedServers.push({
        name: s.candidate.key,
        source: s.candidate.repositoryUrl,
        stratum: s.stratum,
        error: "batch_timeout",
      });
    }
    totalFailed += batch.length;
  }

  // Clean up input file
  try { unlinkSync(candidatesFile); } catch { /* ignore */ }
}

console.error(`\n--- Analysis Complete ---`);
console.error(`Processed: ${totalProcessed}`);
console.error(`Failed: ${totalFailed}`);

if (failedServers.length > 0) {
  const failedFile = resolve(__dirname, "failed_servers_1000.json");
  writeFileSync(failedFile, JSON.stringify(failedServers, null, 2));
  console.error(`Failed servers written to failed_servers_1000.json`);
}

// Write stratum mapping for later use
const stratumMap = {};
for (const s of sample.servers) {
  stratumMap[s.candidate.key] = {
    stratum: s.stratum,
    repositoryUrl: s.candidate.repositoryUrl,
    packageEcosystems: s.candidate.packageEcosystems,
    sources: s.candidate.sources.map((src) => src.type),
  };
}
const mapFile = resolve(__dirname, "stratum-map-1000.json");
writeFileSync(mapFile, JSON.stringify(stratumMap, null, 2));
console.error("Stratum mapping written to stratum-map-1000.json");
