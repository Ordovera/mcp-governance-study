/**
 * Build the final evidence corpus from analysis batches + LLM verification.
 *
 * Merges:
 *   1. Deterministic analysis (evidence_1000_batch*.json)
 *   2. LLM verification (verify-results-1000.json)
 *   3. Remote-only RPC results (evidence_1000_remote.json)
 *   4. Stratum metadata (stratum-map-1000.json)
 *
 * Produces evidence_corpus_n1000.json with:
 *   - LLM verification status (isMcpServer, confidence)
 *   - Merged tool list (heuristic + LLM supplementary)
 *   - Per-server stratum labels
 *   - Dead repo / non-MCP exclusion counts
 *
 * Usage: node build-corpus-1000.mjs [--output FILE]
 */

import { readFileSync, writeFileSync, readdirSync, existsSync } from "node:fs";
import { resolve, dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const outputFile = args.find((_, i) => args[i - 1] === "--output") || "evidence_corpus_n1000.json";

// 1. Load all analysis batches
const batchFiles = readdirSync(__dirname)
  .filter((f) => f.match(/^evidence_1000_batch\d+\.json$/))
  .sort((a, b) => {
    const na = parseInt(a.match(/\d+/)?.[0] ?? "0");
    const nb = parseInt(b.match(/\d+/)?.[0] ?? "0");
    return na - nb;
  });

const analysisServers = new Map();
for (const file of batchFiles) {
  const data = JSON.parse(readFileSync(join(__dirname, file), "utf8"));
  for (const envelope of data.envelopes ?? []) {
    const report = envelope.fullReport ?? {};
    const name = report.name ?? envelope.subject?.name;
    if (name) analysisServers.set(name, report);
  }
}
// Also load replacement analysis
const replFile = join(__dirname, "evidence_1000_replacements.json");
if (existsSync(replFile)) {
  const data = JSON.parse(readFileSync(replFile, "utf8"));
  for (const envelope of data.envelopes ?? []) {
    const report = envelope.fullReport ?? {};
    const name = report.name ?? envelope.subject?.name;
    if (name && !analysisServers.has(name)) analysisServers.set(name, report);
  }
}
console.error(`Analysis batches: ${batchFiles.length} files + replacements, ${analysisServers.size} servers`);

// 2. Load LLM verification results
const verifyFile = join(__dirname, "verify-results-1000.json");
const verifyResults = new Map();
if (existsSync(verifyFile)) {
  const data = JSON.parse(readFileSync(verifyFile, "utf8"));
  for (const r of data) {
    verifyResults.set(r.name, r);
  }
  console.error(`LLM verification: ${verifyResults.size} servers`);
} else {
  console.error("WARNING: verify-results-1000.json not found -- skipping LLM merge");
}

// Also load replacement verification
const replVerifyFile = join(__dirname, "verify-results-replacements.json");
if (existsSync(replVerifyFile)) {
  const data = JSON.parse(readFileSync(replVerifyFile, "utf8"));
  for (const r of data) {
    if (!verifyResults.has(r.name)) verifyResults.set(r.name, r);
  }
  console.error(`LLM verification after replacements: ${verifyResults.size} servers`);
}

// 3. Load remote-only results
const remoteFile = join(__dirname, "evidence_1000_remote.json");
const remoteServers = new Map();
if (existsSync(remoteFile)) {
  const data = JSON.parse(readFileSync(remoteFile, "utf8"));
  // Remote evidence may be in envelope or flat format
  if (data.envelopes) {
    for (const envelope of data.envelopes) {
      const report = envelope.fullReport ?? {};
      const name = report.name ?? envelope.subject?.name;
      if (name) remoteServers.set(name, report);
    }
  } else if (data.servers) {
    for (const server of data.servers) {
      remoteServers.set(server.name, server);
    }
  }
  console.error(`Remote-only: ${remoteServers.size} servers`);
} else {
  console.error("WARNING: evidence_1000_remote.json not found -- remote-only servers will be missing");
}

// 4. Load stratum map
const stratumMap = existsSync(join(__dirname, "stratum-map-1000.json"))
  ? JSON.parse(readFileSync(join(__dirname, "stratum-map-1000.json"), "utf8"))
  : {};

// 5. Load sample + replacements for full server list
const sample = JSON.parse(readFileSync(join(__dirname, "sample-1000.json"), "utf8"));
const replSampleFile = join(__dirname, "replacements-1000.json");
if (existsSync(replSampleFile)) {
  const repl = JSON.parse(readFileSync(replSampleFile, "utf8"));
  sample.servers.push(...repl.servers);
  console.error(`Sample after replacements: ${sample.servers.length} servers`);
}

// Build merged corpus
const corpus = [];
const exclusions = { deadRepo: 0, notMcp: 0, cloneFailed: 0 };

for (const sampled of sample.servers) {
  const key = sampled.candidate.key;
  const stratum = sampled.stratum;
  const isRemoteOnly = sampled.candidate.repositoryUrl === null;

  // Get analysis result
  const analysis = isRemoteOnly
    ? remoteServers.get(key)
    : analysisServers.get(key);

  // Get verification result (source-available only)
  const verification = verifyResults.get(key);

  // Check for dead repos / clone failures
  if (!isRemoteOnly && !analysis) {
    exclusions.deadRepo++;
    continue;
  }

  if (analysis?.warnings?.some((w) => w.startsWith("Analysis failed:"))) {
    const failMsg = analysis.warnings.find((w) => w.startsWith("Analysis failed:"));
    if (failMsg?.includes("clone") || failMsg?.includes("ENOENT") || failMsg?.includes("not found")) {
      exclusions.deadRepo++;
    } else {
      exclusions.cloneFailed++;
    }
    continue;
  }

  // Check LLM verification -- exclude confirmed non-MCP servers
  if (verification && !verification.isMcpServer && verification.confidence !== "low") {
    exclusions.notMcp++;
    continue;
  }

  // Merge analysis + verification
  const entry = {
    name: key,
    source: sampled.candidate.repositoryUrl ?? sampled.candidate.key,
    stratum,
    ...(analysis ?? {}),
  };

  // Add LLM verification metadata
  if (verification) {
    entry.llmVerification = {
      isMcpServer: verification.isMcpServer,
      confidence: verification.confidence,
      evidence: verification.evidence,
      toolCount: verification.tools?.length ?? 0,
      extractionNotes: verification.extractionNotes,
      metadata: verification.metadata,
    };

    // Merge LLM-extracted tools with heuristic tools
    if (verification.tools?.length > 0) {
      const heuristicNames = new Set((entry.tools ?? []).map((t) => t.name));
      const supplementary = verification.tools.filter((t) => !heuristicNames.has(t.name));

      if (supplementary.length > 0) {
        entry.llmSupplementaryTools = supplementary.map((t) => ({
          name: t.name,
          description: t.description,
          classification: t.classification,
          writeRationale: t.writeRationale,
          sourceFile: t.sourceFile || "[llm-extracted]",
          sourceLine: t.sourceLine || 0,
        }));
      }
    }
  }

  corpus.push(entry);
}

// Summary
const totalTools = corpus.reduce((n, s) => n + (s.tools?.length ?? 0), 0);
const totalLlmSupp = corpus.reduce((n, s) => n + (s.llmSupplementaryTools?.length ?? 0), 0);
const withGaps = corpus.filter((s) => s.accountabilityGaps?.length > 0).length;

console.error(`\n--- Corpus Summary ---`);
console.error(`Servers in corpus: ${corpus.length}`);
console.error(`Excluded: ${exclusions.deadRepo} dead repos, ${exclusions.notMcp} non-MCP, ${exclusions.cloneFailed} clone failures`);
console.error(`Total heuristic tools: ${totalTools}`);
console.error(`Total LLM supplementary tools: ${totalLlmSupp}`);
console.error(`Servers with accountability gaps: ${withGaps}`);

// Per-stratum counts
const byStratum = {};
for (const s of corpus) {
  if (!byStratum[s.stratum]) byStratum[s.stratum] = 0;
  byStratum[s.stratum]++;
}
console.error("\nPer-stratum:");
for (const [stratum, count] of Object.entries(byStratum).sort()) {
  console.error(`  ${stratum}: ${count}`);
}

// Write corpus
const output = {
  generatedAt: new Date().toISOString(),
  schemaVersion: "0.2.0",
  methodology: {
    snapshotDate: sample.snapshotDate,
    populationSize: 17563,
    populationWithRepo: 13308,
    sampleSeed: sample.seed,
    targetN: 1000,
    actualN: corpus.length,
    exclusions,
    strata: sample.strata,
    sources: ["registry.modelcontextprotocol.io", "npmjs.org", "pypi.org"],
    analysisMethod: {
      sourceAvailable: "static source code analysis via cc-mcp-audit + LLM verification (Claude Opus)",
      remoteOnly: "MCP tools/list RPC introspection",
    },
  },
  servers: corpus,
};

writeFileSync(resolve(__dirname, outputFile), JSON.stringify(output, null, 2));
console.error(`\nWritten to ${outputFile}`);
