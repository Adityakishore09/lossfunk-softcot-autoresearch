# Prompt and session ledger

This ledger captures human prompts/choices and any external-model prompts used for research. It is append-only.

## Current record

- Human instructions and scope choice are recorded verbatim in human-intervention.md.
- No external model, API, assistant-model, cloud-provider, or training prompt has been issued.
- No model completion or generated research result exists.

## Logging rule for future calls

Before each external-model call, append the provider/model/version, exact prompt, decoding settings, intended purpose, timestamp, and expected marginal cost. After the call, append the response identifier or local artifact path, actual token/compute use if available, actual cost evidence, and whether the output affected a research decision.

## 2026-06-24 — Training failure / restart record

- Human prompt and error transcript: recorded verbatim in `human-intervention.md` under “Seed-41 checkpoint failure and request to resume.”
- External model prompt: none. The failure arose during local Qwen/Trainer execution, not from an external model API call.
- Code decision: disable generic intermediate Trainer saves because only the custom final `projection.bin` is required; preserve epoch evaluation.
- Compute action: user-authorized fresh seed-41 restart in server tmux session `lossfunk_seed41_retry`; shared-lab USD cost is unknown and no result is available yet.

## 2026-06-30 — Paper drafting record

- Human prompt: “Draft the paper now.”
- Action: Codex drafted the AI-authored first-draft paper from logged artifacts and frozen results.
- External paid model prompts: none.
- Public metadata lookups: read-only arXiv API queries for citation metadata, plus an ACL Anthology lookup attempt for ASDiv that produced a false match and was not used as an ASDiv citation. These lookups did not affect scientific results and incurred no known cost.
- Output artifacts: `paper/main.tex`, `paper/references.bib`, `paper/main.pdf`, `paper/build_pdf.py`, `paper/figures/`, `paper/rendered/`, `paper/COMPILE_NOTES.md`.
- Human critique/reflection deck: not drafted, in accordance with `AGENTS.md`.
