/**
 * Re-evaluate all 99 validation sample tools with Opus using full context
 * from the updated review doc (expanded docstrings, annotations).
 * Compares original LLM classification against re-evaluation.
 */

import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { selectProvider } from "../../packages/cc-mcp-audit/dist/screen-providers.js";

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
