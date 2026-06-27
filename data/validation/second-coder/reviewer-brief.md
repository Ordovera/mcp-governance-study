# Reviewer Brief: Independent Classification of Developer Tool Definitions

Thank you for taking this on. This is a focused, well-defined coding task. You are
acting as an **independent second coder**: you classify each item yourself, from
the evidence provided, without reference to anyone else's answers.

## What you are doing

You will classify **200 software "tool" definitions** extracted from open-source
projects, across two separate tasks:

- **Task A -- Read/Write (100 items)**: does the tool change persistent state?
- **Task B -- Sensitivity (100 items)**: is the tool's data or action
  governance-relevant (would it be subject to access control, audit, or
  regulation in a well-run system)?

Each item gives you the tool name, a short description, and (for almost all) a
short source-code excerpt in Python, TypeScript/JavaScript, or Go. You do not need
to run anything. You do need to read the code and apply one rule -- and when the
excerpt alone is not enough to tell what the tool does, it is fine (and expected) to
open the project's repository and read the surrounding source for context. A few
items deliberately ship without a source excerpt; classify those from the name and
description.

## Files

| File | What it is |
|------|------------|
| `task-A-readwrite.md` | The 100 read/write items, each with source. Read it, answer inline, send it back. |
| `task-B-sensitivity.md` | The 100 sensitivity items, each with source. Read it, answer inline, send it back. |

Two files, no spreadsheet. The full decision rule and the allowed labels are
printed at the top of each `task-*.md` file. Read those headers before you start --
they are the whole specification.

## How to answer

You edit the task files directly. Under each tool you will find two lines:

```
ANSWER: 
NOTES: 
```

Type your label after `ANSWER:` and any note after `NOTES:`, in the same file. For
example:

```
ANSWER: write
NOTES: returns a value but also saves it to disk
```

Allowed labels:

- Task A: `read`, `write`, or `unknown` (use `unknown` only when there is genuinely
  too little context).
- Task B: `sensitive` or `non-sensitive`.

Keep the `ANSWER:` and `NOTES:` line prefixes exactly as they are -- just type after
them. Notes are optional: a few words on the cases you found genuinely hard are
valuable; you do not need to annotate the easy ones.

## What good work looks like

- Every item has an `ANSWER:`. No blanks.
- You applied the single stated rule consistently, not your own intuition about
  whether a tool is "important."
- For Task A, judge by **persistent effect**, not by whether the verb sounds
  active. A tool that "renders a preview" but saves nothing is `read`. A tool
  that "gets" something but writes it to disk is `write`.
- For Task B, remember it is **independent of read/write**. A read-only tool that
  returns credentials, personal data, financial, medical, or legal information is
  `sensitive`.
- Brief notes on the items you found hard.

## What to avoid

- Reading the source -- the excerpt, and the wider repository when you need more
  context -- is the work, and is encouraged. What is off-limits is outsourcing the
  *judgment*: do not try to find a pre-existing classification or answer key for
  these tools, and do not use an automated tool or AI to assign the labels for you.
  The point is your own reasoning from the evidence. We compare your answers to an
  existing set afterward; that agreement is the measurement, so your independence is
  the whole value.
- Do not collaborate with anyone else on the labels.

## Deliverable and turnaround

Return the two edited files (`task-A-readwrite.md`, `task-B-sensitivity.md`) with
your `ANSWER:` lines filled in, and any notes on the `NOTES:` line. Keep them as
plain text/markdown; do not change the structure or the headings. Target turnaround
is as separately agreed. If anything in the instructions is unclear, ask
before you start rather than guessing across all 200.
