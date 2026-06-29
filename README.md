# Measuring Agent Governance Posture

Reproduction package for *Measuring Agent Governance Posture: Accountability Gaps in MCP Servers and Implications for Single- and Multi-Agent Governance* — an empirical study of governance posture across 945 Model Context Protocol (MCP) servers drawn from a population of 17,563.

- **Paper:** Zenodo DOI 10.5281/zenodo.20972251 (manuscript deposit). Optional mirror: arXiv:XXXX.XXXXX (if/when submitted).
- **Data:** Zenodo DOI 10.5281/zenodo.20970604 (evidence corpus + artifacts; a separate Zenodo deposit — see `data/README.md`).
- **Code:** this GitHub repository, referenced by URL + release tag; not archived to Zenodo.
- **Analysis instrument:** [`cc-mcp-audit`](https://www.npmjs.com/package/cc-mcp-audit) (npm) — the deterministic + LLM-verified MCP analysis pipeline used to produce the evidence corpus. This repository consumes its output; it does not vendor the tool. Pin the version used for the study in `data/README.md`.

## Repository layout

```
paper/      Pointer to the manuscript's Zenodo version of record (paper/README.md);
            the manuscript itself lives in its own deposit, not in this repo.
code/       Analysis scripts that reproduce every number reported in the paper.
            extractor-development/  Methodology record: extractor prototypes and
                                    per-phase rerun/stat scripts (optional to run).
prompts/    LLM verification prompts used by the cc-mcp-audit pass (see prompts/README.md).
data/
  validation/  Human-validation samples (read/write and sensitivity, n=100 each),
               the canonical FINAL sensitivity labels, and the residual-server taxonomy.
  results/     Generated text outputs cited in the paper.
  README.md    How to obtain the heavy evidence corpus (Zenodo) + SHA-256 checksums.
```

The evidence corpus itself (the per-server JSON, ~80 MB per snapshot) is **not** stored in git; it is archived on Zenodo. See `data/README.md`.

## Reproducing the headline numbers

1. Download the corpus from Zenodo (see `data/README.md`) into a directory of your choice — call it `$CORPUS_DIR`.
2. Run the canonical generators from any working directory, pointing them at the corpus with `--data-dir` (or set `MCP_DATA_DIR` once):

   ```bash
   export MCP_DATA_DIR="$CORPUS_DIR"             # or pass --data-dir to each script

   python3 code/paper-numbers-postg.py          # Tables 1-4, indicators, scores
   python3 code/sensitivity-negation-variant.py # downgrade-only sensitivity bound (Section 4.5)
   python3 code/compute-gap-robustness.py --recompute-gaps  # owner-cluster bootstrap, Gini, Jaccard
   python3 code/compute-sensitivity-scores.py   # sensitivity validation (uses in-repo data/validation/)
   python3 code/compute-readwrite-scores.py     # read/write validation, kappa (uses in-repo data/validation/)
   ```

   Stdlib Python 3 only; no external dependencies.

> **Path handling:** the heavy corpus is located via `--data-dir` / `$MCP_DATA_DIR` (default: current directory). The small validation samples ship in `data/validation/` and are resolved relative to the repo, so `compute-sensitivity-scores.py` and `compute-readwrite-scores.py` need no `--data-dir`. Scripts import `rerun-gap-detection.py` from their own directory, so they run correctly from any working directory. See `code/_repro.py`.

## Licensing

- **Code** (`code/`): MIT — see `LICENSE`.
- **Data** (`data/`): CC-BY-4.0 — see `LICENSE-DATA`. Attribution required. The manuscript (also CC-BY-4.0) is published as its own Zenodo deposit; `paper/` here is only a pointer.

## Citation

See `CITATION.cff`. Please cite the preprint and the Zenodo dataset DOI.
