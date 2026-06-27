/**
 * Read/write classification validation runner (Section 3.5).
 *
 * Re-evaluates the read/write validation sample (99 tools) with Claude Opus
 * using full context from the review doc (expanded docstrings, MCP
 * annotations), and compares the re-evaluation against the original LLM
 * classification and the human label. This run backs the kappa = 0.940
 * "LLM (Opus) vs Human" figure reported in Section 3.5 (n = 100 sample).
 *
 * The prompt is identical to ../prompts/v1/reeval_read_write.txt.
 *
 * This is a method record: it documents exactly how the `llm_reeval` labels were
 * generated. Those labels (with the `human` labels that back the kappa = 0.940
 * figure) ship in-repo in ../data/validation/validation-final-n100.json. The
 * runner's intermediate JSONs below are derivatives, not core data; they are read
 * from / written to the current directory and are not redistributed in this repo:
 *
 *   reeval-with-context.json  (input)  -- the 99 tools with source context
 *   reeval-results.json       (output) -- per-tool re-evaluation, resume-safe
 *
 * Requires the published analysis instrument:  npm i cc-mcp-audit@1.0.1
 * and the Claude Code CLI on PATH (provider "claude-code").
 *
 * Usage:
 *   cd <dir containing the Zenodo reeval-with-context.json>
 *   node /path/to/code/reeval-read-write.mjs
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { selectProvider } from "cc-mcp-audit/dist/screen-providers.js";

const tools = JSON.parse(readFileSync("reeval-with-context.json", "utf8"));
const provider = selectProvider("claude-code", "claude-opus-4-6");

console.error(`Re-evaluating ${tools.length} tools with ${provider.model}`);

// Resume support
let results = [];
if (existsSync("reeval-results.json")) {
  try {
    results = JSON.parse(readFileSync("reeval-results.json", "utf8"));
    console.error(`Resuming: ${results.length} already done`);
  } catch { results = []; }
}
const doneNums = new Set(results.map((r) => r.num));
const remaining = tools.filter((t) => !doneNums.has(t.num));
console.error(`Remaining: ${remaining.length}`);

const PROMPT = `You are classifying an MCP tool as "read" or "write" based on the persistent-effect rule:

- **read**: no persistent effect after the response is returned
- **write**: causes an effect that persists after the response is returned

If calling this tool twice produces a different world state than not calling it at all, classify as write.

Tool: \`{NAME}\`
Server: {REPO}
Description: {DESCRIPTION}
{ANNOTATIONS}

Source code:
\`\`\`
{CODE}
\`\`\`

Respond with ONLY a JSON object:
{
  "classification": "read" | "write",
  "rationale": "one sentence explaining why, citing the persistent effect or lack thereof"
}`;

async function classifyOne(tool) {
  const annLine = tool.annotations ? `MCP Annotations: ${tool.annotations}` : "";
  const prompt = PROMPT
    .replace("{NAME}", tool.name)
    .replace("{REPO}", tool.repo)
    .replace("{DESCRIPTION}", tool.description || "(none)")
    .replace("{ANNOTATIONS}", annLine)
    .replace("{CODE}", tool.code);

  const result = await provider.call(prompt);
  let text = result.text.trim();
  if (text.startsWith("```")) {
    text = text.replace(/^```(?:json)?\s*\n?/, "").replace(/\n?```\s*$/, "");
  }
  try {
    return JSON.parse(text);
  } catch {
    return { classification: "error", rationale: text.slice(0, 200) };
  }
}

for (let i = 0; i < remaining.length; i++) {
  const t = remaining[i];
  const start = Date.now();
  const r = await classifyOne(t);
  const elapsed = ((Date.now() - start) / 1000).toFixed(1);

  const changed = r.classification !== t.llm_original;
  const flag = changed ? " CHANGED" : "";
  const humanNote = t.human ? ` human=${t.human}` : "";

  console.error(
    `[${results.length + 1}/${tools.length}] #${t.num} ${t.name}: ` +
    `orig=${t.llm_original} -> reeval=${r.classification}${humanNote}${flag} (${elapsed}s)`
  );

  results.push({
    num: t.num,
    name: t.name,
    repo: t.repo,
    heuristic: t.heuristic,
    enhanced: t.enhanced || "",
    llm_original: t.llm_original,
    llm_reeval: r.classification,
    llm_rationale: r.rationale,
    human: t.human || "",
    annotations: t.annotations || "",
    changed: changed,
  });

  // Save after each
  if (results.length % 5 === 0) {
    writeFileSync("reeval-results.json", JSON.stringify(results, null, 2));
  }
}

writeFileSync("reeval-results.json", JSON.stringify(results, null, 2));

// Summary
const changed = results.filter((r) => r.changed);
const withHuman = results.filter((r) => r.human);
const origAgree = withHuman.filter((r) => r.llm_original === r.human);
const revalAgree = withHuman.filter((r) => r.llm_reeval === r.human);

console.error(`\n=== SUMMARY ===`);
console.error(`Total: ${results.length}`);
console.error(`LLM changed: ${changed.length}`);
if (withHuman.length > 0) {
  console.error(`With human classification: ${withHuman.length}`);
  console.error(`Original LLM agreed with human: ${origAgree.length}/${withHuman.length} (${Math.round(origAgree.length/withHuman.length*100)}%)`);
  console.error(`Re-eval LLM agrees with human: ${revalAgree.length}/${withHuman.length} (${Math.round(revalAgree.length/withHuman.length*100)}%)`);
}

// Show all changes
if (changed.length > 0) {
  console.error(`\nCHANGED CLASSIFICATIONS:`);
  for (const r of changed) {
    console.error(`  #${r.num} ${r.name}: ${r.llm_original} -> ${r.llm_reeval} (human: ${r.human || 'n/a'}) -- ${r.llm_rationale}`);
  }
}
