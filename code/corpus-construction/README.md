# Corpus construction pipeline (provenance — NOT turnkey)

These eleven `.mjs` scripts are the **corpus-construction** pipeline: how the
study went from the population snapshot to the evidence corpus (draw the
stratified sample, draw replacements for dead repos, clone/analyze/verify each
server, introspect remote-only servers, and run the read/write re-evaluation).

They are distinct from the scripts in `code/` and `code/extractor-development/`,
which compute the paper's numbers *from* the finished corpus. These build the
corpus itself.

## Important: archival record, not a one-command rerun

These scripts were authored **inside the `cc-mcp-audit` monorepo** and import the
tool's internal modules by relative path, e.g.:

```
import { drawSample, STRATA } from "../../packages/cc-mcp-audit/dist/sampler.js";
import { verifyServer }       from "../../packages/cc-mcp-audit/dist/verify.js";
import { analyzeServerRemote } from "../../packages/cc-mcp-audit/dist/analyze.js";
```

Those paths reach **internal** modules of the instrument (sampler, discover-registry,
analyze, indicators, report, verify, extract), several of which are deeper than the
published package's API surface. They are preserved here for **transparency and
provenance**, not as a turnkey reproduction step.

To actually re-run them you would need to:

1. Use the pinned instrument **`cc-mcp-audit@1.0.1` (git `881b817`)** — the same
   version recorded in `data/README.md` and used to produce the deposited corpus.
2. Repoint the `../../packages/cc-mcp-audit/dist/...` imports at that checkout (or
   rewrite them to the installed package where the module is exported; cf.
   `code/reeval-read-write.mjs`, which uses the bare `cc-mcp-audit/...` specifier).
3. Supply the population snapshot (`canonical-snapshot-2026-05-04.json`, on Zenodo)
   and network access to clone ~1,000 source repositories.

Because the corpus is already built and archived on Zenodo, re-running is not
required to reproduce any reported number — those derive from the finished corpus
via the scripts in `code/`. This directory documents *how the corpus was made*.

## Scripts by stage

| Stage | Script |
|-------|--------|
| Sampling | `draw-sample-1000.mjs`, `draw-replacements.mjs` |
| Corpus / path assembly | `build-corpus-1000.mjs`, `build-verify-paths-1000.mjs` |
| Remote discovery | `fetch-remote-endpoints.mjs` |
| Analysis & verification runners | `run-analysis-1000.mjs`, `run-verify-1000.mjs`, `run-verify-batch.mjs`, `run-remote-1000.mjs`, `run-reeval.mjs` |
| Extraction guard check | `revalidate-comment-guard.mjs` |
