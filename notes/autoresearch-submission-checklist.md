# Lossfunk autoresearch submission checklist

Source inspected: `external-guidance/autoresearch-stage.md`, fetched from `https://raw.githubusercontent.com/paraschopra/lossfunk-prompts/main/autoresearch-stage.md` on 2026-06-30.

## What Lossfunk asks you to submit

Submit exactly two things:

1. A GitHub repository containing the AI-produced autoresearch artifact.
2. A presentation/deck PDF written by you, covering your judgment and critique.

## Repository checklist

- [ ] Include the AI-produced artifact without human cleanup or polishing.
- [ ] Include the paper draft:
  - [ ] `paper/main.pdf`
  - [ ] `paper/main.tex`
  - [ ] `paper/references.bib`
  - [ ] `paper/COMPILE_NOTES.md`
- [ ] Include raw and frozen results:
  - [ ] `frozen-results/2026-06-28_seed41_42_43/`
  - [ ] `frozen-results/2026-06-29_full_target_extension/`
- [ ] Include result analysis files:
  - [ ] core seed comparison
  - [ ] full-target summary
  - [ ] item-level agreement analysis
- [ ] Include code and scripts used to run the experiments:
  - [ ] `code/`
  - [ ] `scripts/`
  - [ ] `RUNBOOK.md`
  - [ ] `protocol.md`
- [ ] Include logs:
  - [ ] `logs/environment.md`
  - [ ] `logs/progress.md`
  - [ ] `logs/human-intervention.md`
  - [ ] `logs/commands.md`
  - [ ] `logs/costs.md`
  - [ ] `logs/failures.md`
  - [ ] `logs/prompt-session.md`
- [ ] Include notes:
  - [ ] `notes/conference-reviewer-pass.md`
  - [ ] `notes/data-sources.md`
  - [ ] `notes/autoresearch-submission-checklist.md`
- [ ] Include the official autoresearch-stage guidance copy:
  - [ ] `external-guidance/autoresearch-stage.md`
- [ ] Do not hide embarrassing failures.
- [ ] Do not delete failed runs.
- [ ] Do not rewrite the paper to make it sound more human or more successful.
- [ ] Make clear that the paper is AI-authored and that the critique/deck is human-authored.

## Deck checklist

The deck should be a PDF. It should be your own judgment, not AI-written.

- [ ] Starting research question / claim.
- [ ] Autoresearch flow:
  - [ ] What tool/system you used.
  - [ ] How you set it up.
  - [ ] What you customized.
  - [ ] What human interventions were needed.
- [ ] Summary of AI-found results.
- [ ] What you learned about your research question.
- [ ] Critique of the AI-generated artifact:
  - [ ] What is genuinely correct/useful.
  - [ ] What is plausible-looking but weak.
  - [ ] What is missing.
  - [ ] What is overclaimed.
  - [ ] What a senior researcher would immediately object to.
- [ ] Reflection on the limits of current autoresearch systems:
  - [ ] What Codex did well.
  - [ ] Where Codex failed.
  - [ ] What kinds of questions it would handle better.
  - [ ] What kinds of questions still need human taste.
- [ ] Revised research plan:
  - [ ] What changed from the original proposal.
  - [ ] Why the question is sharper now.
  - [ ] How the next experiments should change.

## This project's recommended deck thesis

The artifact is useful because it falsified the simple version of the proposal. The original expectation was that GSM8K-trained SoftCoT would transfer better to ASDiv-Aug than StrategyQA. Instead, learned SoftCoT beat zero controls, but the clearest learned-over-baseline gain appeared on StrategyQA. This suggests the revised research question should study whether SoftCoT gains follow reasoning type, answer format, dataset identity, or prompt-steering behavior.

## Submission format

- [ ] GitHub repo link.
- [ ] Deck as PDF.

Lossfunk explicitly says they are reading for judgment, not polish. The critique is the real test.
