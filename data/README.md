# Data

This directory holds the small, in-repo artifacts. The heavy evidence corpus is
archived separately on Zenodo (it is too large for git and exceeds GitHub's
file-size limits).

## In this repository

- `validation/validation-sensitivity-n100.json` — sensitivity human-validation
  sample (n=100), with the canonical FINAL labels propagated.
- `validation/validation-final-n100.json` — read/write human-validation sample (n=100).
- `validation/validation-sensitivity-review-full-FINAL.md` — the canonical
  FINAL sensitivity labels (source of truth for the n=100 sensitivity validation).
- `validation/residual-86-categorized-v2.json` — causal taxonomy of the residual
  unextracted servers.
- `validation/residual-84-servers.json` — per-server metadata for the residual set.
- `validation/second-coder/` — the independent second-coder reliability material
  (Section 3.5 inter-coder agreement): the reviewer brief, the two coding tasks as
  sent, and the coder's raw returns. The coder's name is redacted in the returned
  filenames; the blind keys and scoring pipeline are withheld. See its `README.md`.
- `results/` — generated text outputs cited in the paper (gap robustness,
  post-G reconciliation, sensitivity negation-variant bound, paper statistics).

## On Zenodo (data deposit; DOI 10.5281/zenodo.20970604)

This is the **data** deposit — a separate Zenodo record from the paper deposit
(DOI `zenodo.20972251`). Reserve this data DOI first so the paper's Data
Availability statement can cite it; the code itself stays on GitHub.

The reproduction bundle archived on Zenodo contains the full evidence corpus and
supporting snapshots, which the analysis scripts in `code/` consume:

- `evidence_corpus_n1000_post_phaseg.json` — **canonical** corpus (945 servers,
  post-Phase-G extraction). This is the file every headline number is computed from.
- `evidence_corpus_n1000.json` — original pre-extractor corpus (for the A->G arc).
- `canonical-snapshot-2026-05-04.json` — the population snapshot the sample was drawn from.
- LLM verification raw outputs and the sampling artifacts.

### Checksums (SHA-256)

Populate on release so reproducers can verify integrity:

```bash
72be39a8af280a06912acdca32cdb6e5a7e8e91b8962cef967cb776a1b2578ad  evidence_corpus_n1000_post_phaseg.json
2d7cfa24df1b884863360b3af11923565e5208c995d4ad77eb4a9870aaedd826  evidence_corpus_n1000.json
f16a5ec15e4ba3e813f5528a70e210ffe98cefe2699baeee0de1a6491030816b  canonical-snapshot-2026-05-04.json
```

### Analysis instrument version

The corpus was produced by `cc-mcp-audit` (npm). Record the exact version/commit
used for the study here so the pipeline is reproducible:

```bash
cc-mcp-audit@1.0.1  (git 881b817; npm gitHead, tag cc-mcp-audit@1.0.1)
```

The LLM verification prompts pinned to this version are exported in
`../prompts/v1/` (see `../prompts/README.md`).

## Reproducing

Download the canonical corpus from Zenodo into any directory, then point the
scripts at it with `--data-dir <dir>` (or `export MCP_DATA_DIR=<dir>`) and run
the generators in `code/`. See the top-level README.
