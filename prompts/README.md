# LLM verification prompts

The study's LLM verification pass (Section 3.3) and the read/write validation
exercise (Section 3.5) both ran through the `cc-mcp-audit` instrument via the
Claude Code CLI. This directory pins the exact prompt text used, so every
LLM-assisted step is independently re-executable as promised in the paper's
Data Availability statement.

Instrument version: **`cc-mcp-audit@1.0.1` (git `881b817`)**, recorded in
`../data/README.md`. Prompt template version: **v1** (matches the
`promptVersion: "v1"` stamped on every verification record).

## The prompts

### `v1/verify_mcp_server.txt` — production verification prompt

One combined prompt drives the entire Section 3.3 verification pass. It is sent
once per source-available server, receives MCP-relevance-prioritized code
regions (dependency manifests, MCP-importing files, entry points) within a
~30,000-token budget, and returns a single JSON object covering all three
outputs the paper enumerates:

1. **MCP server confirmation** — `isMcpServer` + `confidence` + `evidence`
   (Section 3.3 output 1)
2. **Supplementary tool extraction** — the `tools[]` array, capturing
   registration patterns the deterministic regex extractor did not (output 2)
3. **Read/write classification with cited rationale** — each tool's
   `classification` and `writeRationale` (output 3)

The three TODO items below ("MCP-confirmation", "supplementary-tool-extraction",
"read/write classification") are the three *outputs of this one prompt*, not
three separate files. The `{{REGIONS}}` placeholder is filled by
`buildVerifyPrompt()` in `cc-mcp-audit/src/verify.ts`.

### `v1/reeval_read_write.txt` — read/write validation prompt

A separate, single-purpose per-tool prompt used only for the human-validation
exercise that produced the **kappa = 0.940** LLM-vs-human agreement figure
(Section 3.5, "LLM (Opus) vs Human"). It applies the persistent-effect rule to
one tool at a time, given the tool name, server, description, optional MCP
annotations, and source code. Placeholders (`{NAME}`, `{REPO}`, `{DESCRIPTION}`,
`{ANNOTATIONS}`, `{CODE}`) are substituted per tool. This prompt was not part of
the `cc-mcp-audit` package; it lived inline in the validation runner, which is
ported into this repository as `../code/reeval-read-write.mjs`. The per-tool
labels it produced (`llm_reeval` vs `human`) that back the kappa = 0.940 figure
ship in-repo in `../data/validation/validation-final-n100.json`; the runner's
intermediate input/output JSONs are method-record derivatives and are not core
data.

Out of scope: `cc-mcp-audit` also ships `domain5_*.txt` screening prompts
(self-modification, sub-agent authority, permission boundary). Those drive a
separate screening feature and are **not** part of this paper's verification
layer, so they are intentionally not exported here.

## Model and CLI invocation

- **Model id:** `claude-opus-4-6`
- **Provider:** Claude Code CLI (`ClaudeCodeProvider` in
  `cc-mcp-audit/src/screen-providers.ts`)
- **Invocation:** `claude -p "<prompt>" --output-format json --model claude-opus-4-6`
- **Per-call limits:** 120 s timeout, 10 MB max output buffer
- **Throughput (production pass, Section 3.6 item 1):** one server in flight at a
  time, 5-second inter-request delay, three retries on transient failures
- **Coverage:** 664 of 760 source-available servers (87%); the remaining 96 hit
  CLI timeouts on large repositories and fell back to deterministic-only analysis

The CLI returns `{ type: "result", result: "<JSON string>", total_cost_usd?,
usage? }`; the instrument strips any markdown code fences and parses the inner
JSON.

TODO before release:

- [x] Export the MCP-confirmation prompt (`v1/verify_mcp_server.txt`, output 1)
- [x] Export the supplementary-tool-extraction prompt (`v1/verify_mcp_server.txt`, output 2)
- [x] Export the read/write classification prompt (`v1/verify_mcp_server.txt` output 3, production; `v1/reeval_read_write.txt`, validation)
- [x] Note the model id (`claude-opus-4-6`) and CLI invocation parameters
