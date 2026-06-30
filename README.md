# Lossfunk Autoresearch Submission: SoftCoT Transfer Audit

This repository is the AI-produced artifact for the Lossfunk autoresearch stage.

The sprint tested a scoped question from the original proposal:

> If a SoftCoT projection is trained only on GSM8K, does it transfer more strongly to the related arithmetic target ASDiv-Aug than to the unrelated StrategyQA target?

The short answer from this artifact is: **no, not in this run**. Learned SoftCoT beat zero soft-thought controls, which suggests the learned projection contains signal. But the expected related-transfer pattern was not supported: the clearest learned-over-baseline gain appeared on StrategyQA, not ASDiv-Aug.

## Start here

- Paper PDF: [`paper/main.pdf`](paper/main.pdf)
- Paper source: [`paper/main.tex`](paper/main.tex)
- Build notes: [`paper/COMPILE_NOTES.md`](paper/COMPILE_NOTES.md)
- Source-trained projection checkpoints: [`checkpoints/softcot-projections/`](checkpoints/softcot-projections/)
- Submission checklist: [`notes/autoresearch-submission-checklist.md`](notes/autoresearch-submission-checklist.md)
- Reviewer pass: [`notes/conference-reviewer-pass.md`](notes/conference-reviewer-pass.md)

## Main result

Core 200-example, 3-seed mean accuracies:

| Task | Learned SoftCoT | Zero control | No-SoftCoT baseline |
|---|---:|---:|---:|
| GSM8K | 0.8250 | 0.7950 | 0.8683 |
| ASDiv-Aug | 0.8567 | 0.7950 | 0.8683 |
| StrategyQA | 0.6517 | 0.5867 | 0.5367 |

Full-target learned-vs-baseline extension:

| Task | Learned | Baseline | Delta |
|---|---:|---:|---:|
| StrategyQA full dev | 0.6405 | 0.5342 | +0.1063 |
| ASDiv-Aug full test | 0.8642 | 0.8776 | -0.0135 |

## Repository structure

- `paper/` - AI-authored first-draft paper, source, figures, and fallback PDF.
- `frozen-results/` - raw and frozen result archives plus extracted results.
- `checkpoints/` - small trained SoftCoT projection modules for seeds 41/42/43; full Qwen model weights are not included.
- `logs/` - environment, commands, costs, failures, prompts, progress, and human interventions.
- `scripts/` - experiment, resume, full-target, split-building, and analysis scripts.
- `code/` - upstream and modified SoftCoT code snapshots.
- `notes/` - data provenance, reviewer pass, implementation notes, and submission checklist.
- `external-guidance/` - fetched Lossfunk autoresearch-stage instructions.
- `data/` - fixed split manifest only, not full redistributed datasets.

## Important caveats

- This is an AI-authored first-draft artifact, not a polished human paper.
- The local machine did not have a TeX compiler, so `paper/main.pdf` is a fallback PDF generated from the same paper content with the bundled Python PDF runtime. `paper/main.tex` is the canonical source.
- Runs used a shared lab A100. Seeds 41 and 43 were contended; seed 43 used a lower-memory override.
- The repository includes only the small learned projection checkpoints, not the downloaded Qwen base/assistant model weights.
- The result does not prove that SoftCoT lacks reasoning. It only shows that the simple related-transfer hypothesis was not supported in this setup.

## Cost

Known billed cost: US$0.00. Compute used a user-provided shared lab server, so actual lab hardware cost is unpriced and no cloud billing receipt exists.
