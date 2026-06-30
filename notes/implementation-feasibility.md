# Official implementation feasibility audit

Audit date: 2026-06-22. This is a pre-execution audit, not an experimental result.

## Primary sources inspected

- Xu, Guo, Zeng, and Miao, "SoftCoT: Soft Chain-of-Thought for Efficient Reasoning with LLMs," ACL 2025 / arXiv:2502.12134v2. The public PDF was read from arXiv and removed from the temporary directory afterward.
- Official repository: https://github.com/xuyige/SoftCoT, inspected through GitHub's API at the repository's then-current main branch.

## What the paper and code establish

SoftCoT keeps an assistant model and the backbone LLM frozen by default, inserts assistant final-layer hidden states into reserved thought positions after a learned projection, and learns the projection plus learned assistant-thought embeddings with a language-modeling objective. The paper describes the learned projection as task-specific soft prompt tuning and reports evaluations after per-task training; it does not report the source-trained, no-target-tuning transfer test selected for this spike.

The paper's Appendix A reports training on one NVIDIA A100-80G GPU, ten epochs, with batch size 8 for Qwen and 16 for LLaMA. The official README demonstrates LLaMA-3.1-8B-Instruct with LLaMA-3.2-1B-Instruct, or Qwen2.5-7B-Instruct with Qwen2.5-1.5B-Instruct. The code is single-GPU.

The official repository contains GSM8K-style train and test files only. Its loaders name ASDiv-Aug and StrategyQA, but expect external files at paths such as aug-train.jsonl, aug-dev.jsonl, and strategyqa_train.json. The README links to an ASDiv-Aug dataset and separate reproduction logs/checkpoints; neither has been downloaded.

The official training script contains a literal placeholder for a Hugging Face token. This machine has no corresponding credential indicator and the LLaMA paths may require gated-model access. The Qwen route could avoid that particular access issue, but it remains unvalidated for the selected transfer protocol.

The public repository is licensed for non-commercial use under the NTUITIVE licence; its GitHub metadata has no SPDX identifier. Any local use, modification, or redistribution must preserve the licence and its restrictions.

## Feasibility conclusion

An untouched, paper-scale reproduction is not feasible on this laptop and is not responsibly promised within this seven-day, US$50.00 sprint. A defensible preliminary version would require a hosted NVIDIA GPU, an openly downloadable compatible model pair or documented public checkpoint, and explicitly labelled deviations such as a smaller model, reduced source-only training set, fewer epochs, and smaller fixed evaluation samples. None of those choices has been executed or paid for.
