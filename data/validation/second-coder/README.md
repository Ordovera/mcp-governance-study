# Second-coder reliability exercise

This directory holds the independent second-coder material behind the
inter-coder agreement reported in Section 3.5 of the paper. To test the
reproducibility of the first author's classifications, an independent coder
re-coded both validation samples (read/write and sensitivity, n = 100 each),
blind to the first author's labels and to the automated heuristic, LLM, and
deterministic outputs.

Reported inter-coder agreement (Cohen's kappa):

| Sample            | n   | Kappa | Interpretation                  |
|-------------------|-----|-------|---------------------------------|
| Read/write        | 100 | 0.840 | almost perfect                  |
| Sensitivity       | 100 | 0.568 | moderate, 95% CI [0.40, 0.71]   |

## Files

| File                                 | Role                                                        |
|--------------------------------------|-------------------------------------------------------------|
| `reviewer-brief.md`                  | The brief given to the coder: the task, decision rules, and answer format. |
| `task-A-readwrite.md`                | Task A as sent -- 100 read/write items with source excerpts, blank `ANSWER:`/`NOTES:` lines. |
| `task-B-sensitivity.md`              | Task B as sent -- 100 sensitivity items, blank answer lines. |
| `task-A-readwrite.REDACTED.md`       | Task A as returned -- the coder's `read`/`write`/`unknown` answers and notes, filled in. |
| `task-B-sensitivity.REDACTED.md`     | Task B as returned -- the coder's `sensitive`/`non-sensitive` answers and notes. |

The coder edited the task files in place (one answer per item, no spreadsheet),
so each returned file is the corresponding sent file with the `ANSWER:` and
`NOTES:` lines completed.

## Coder identity

The paper credits the second coder by name. In this released data set the coder's
name is redacted (shown as `REDACTED`, including in the returned filenames); the
file contents carry no personal identifying information.

## Scope and what is withheld

These files are the coding *instrument* and the coder's *raw returns* -- released
for transparency so the second-coder task can be inspected directly. They are
not, on their own, a recompute pipeline for the kappa figures above: aligning
the coder's answers against the first author's labels requires the blind-item
key, the first author's labels, and the scoring script, which are withheld
because they include unblinding keys and private adjudication of disagreements.
The kappa values are reported in the paper as the result of that scoring.

## Licensing

CC-BY-4.0, consistent with the rest of `data/` (see `../../../LICENSE-DATA`).
Attribution required.
