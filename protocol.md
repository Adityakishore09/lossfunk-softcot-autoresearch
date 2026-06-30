# Pre-execution protocol for the minimum transfer test

Version 0.1, written before model/data download and before any run.

## Primary question

Does a GSM8K-only-trained SoftCoT component provide a larger accuracy increment over its matched no-SoftCoT baseline on ASDiv-Aug than on StrategyQA?

## Eligibility rule

The base LLM and assistant model are frozen. The relevant SoftCoT component may be trained only on GSM8K training examples. ASDiv-Aug and StrategyQA are evaluation-only: no parameter updates, prompt optimization, checkpoint selection, or threshold selection may use their labels.

## Conditions

For each dataset and recorded random seed, evaluate:

1. Standard no-SoftCoT baseline, using the same frozen base model and task template.
2. GSM8K-trained SoftCoT.
3. A zero-vector soft-thought control, if implementation permits four thought slots to be retained while their inserted vectors are zero. This is intended to preserve the added soft-thought position count while removing learned information.

If a zero-vector intervention cannot be implemented and verified, record the failure and use a documented random-vector control only if it can be made shape-, norm-, and compute-matched. Never silently substitute another control.

## Outcomes

For a target dataset d, let Acc(d, Soft) and Acc(d, Base) be exact-match accuracy under the SoftCoT and no-SoftCoT conditions. Define:

Delta_related = Acc(ASDiv-Aug, Soft) - Acc(ASDiv-Aug, Base)

Delta_unrelated = Acc(StrategyQA, Soft) - Acc(StrategyQA, Base)

D = Delta_related - Delta_unrelated

The descriptive pattern of interest is D greater than zero, with the GSM8K source sanity check reported separately. A non-positive D, no source improvement, or an unstable result does not support a related-transfer advantage. It is still a valid and reportable result.

## Pre-run controls and reporting

- Record immutable source, target, and evaluation sample IDs plus dataset checksums before the first run.
- Record model revisions, code revision, prompt templates, source-training subset, hyperparameters, seeds, candidate count, generation-token limit, elapsed time, GPU type, provider bill, and parsing failures.
- Use the same model, prompt scaffold, candidate count, and output-token limit within each target's compared conditions.
- Calculate per-condition accuracy, sample size, and bootstrap confidence intervals. If multiple independent source-training seeds are affordable, report every seed and the seed-level distribution rather than only a pooled score.
- Report source GSM8K, related ASDiv-Aug, and unrelated StrategyQA separately; do not average them into one score.
- Treat all small-sample or small-model findings as preliminary and implementation-specific.

## Pending decisions that must be fixed before running

1. Hosted GPU provider and actual cost ceiling.
2. Compatible, accessible model pair and precise revisions.
3. Dataset source, licence, and fixed deterministic split procedure.
4. Whether the zero-vector intervention can be implemented and unit-verified without changing any other condition.

No pending decision may be chosen after observing a target result.
