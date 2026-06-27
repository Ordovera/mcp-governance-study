/**
 * Fetch remote endpoint URLs from MCP Registry for remote-only servers.
 *
 * Uses the cc-mcp-audit pullMcpRegistry function (proper pagination)
 * to find remote endpoints for our 185 remote-only sample servers.
 *
 * Usage: node fetch-remote-endpoints.mjs
 */

import { readFileSync, writeFileSync } from "node:fs";
import { pullMcpRegistry } from "../../packages/cc-mcp-audit/dist/discover-registry.js";

const sample = JSON.parse(readFileSync("sample-1000.json", "utf8"));
const remoteServers = sample.servers.filter((s) => s.candidate.repositoryUrl === null);

console.error(`Remote-only servers to look up: ${remoteServers.length}`);

async function main() {
  console.error("Fetching MCP Registry (full pagination)...");
  const { entries, totalRaw } = await pullMcpRegistry((n) => {
    if (n % 300 === 0) console.error(`  ${n} entries fetched...`);
  });
  console.error(`Total registry entries: ${totalRaw} raw, ${entries.length} processed`);

  // Build lookup by registryName
  const byName = new Map();
  for (const entry of entries) {
    byName.set(entry.registryName, entry);
  }

  // Build lookup from our remote sample's keys (registryName should match)
  const remoteKeys = new Set(remoteServers.map((s) => s.candidate.key));

  // Also try matching by candidate registryName field
  const remoteRegistryNames = new Map();
  for (const s of remoteServers) {
    remoteRegistryNames.set(s.candidate.registryName ?? s.candidate.key, s.candidate.key);
  }

  const endpoints = [];
  let matched = 0;
  let withEndpoint = 0;

  for (const s of remoteServers) {
    const key = s.candidate.key;
    const registryName = s.candidate.registryName ?? key;

    const entry = byName.get(registryName) ?? byName.get(key);
    if (!entry) continue;
    matched++;

    if (entry.remoteEndpoints.length === 0) continue;
    withEndpoint++;

    endpoints.push({
      name: key,
      url: entry.remoteEndpoints[0].url,
      type: entry.remoteEndpoints[0].type ?? "streamable-http",
      allEndpoints: entry.remoteEndpoints,
    });
  }

  console.error(`\nMatched to registry: ${matched}/${remoteServers.length}`);
  console.error(`With remote endpoints: ${withEndpoint}`);

  writeFileSync("remote-endpoints-1000.json", JSON.stringify(endpoints, null, 2));
  console.error(`Written to remote-endpoints-1000.json`);

  // Also report how many registry entries have remote endpoints at all
  const allWithEp = entries.filter((e) => e.remoteEndpoints.length > 0);
  console.error(`\nRegistry entries with any remote endpoint: ${allWithEp.length}/${entries.length}`);
}

main().catch((err) => {
  console.error("Fatal:", err);
  process.exit(1);
});
