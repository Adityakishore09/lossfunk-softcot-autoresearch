# Verified server inventory

Audit date: 2026-06-22. All observations were read-only.

## Environment

The actual SoftCoT environment executable is:

    /data2/anaconda3/envs/softcot/bin/python3.13

Observed package versions: Python 3.13.7, PyTorch 2.8.0, Transformers 4.57.3, datasets 4.1.1, accelerate 1.10.1, PEFT 0.13.2, and fastNLP 0.7.0.

These differ from the original SoftCoT README requirements (PyTorch 2.4.1 and Transformers 4.44.2). Compatibility must be verified with a minimal source sanity run before interpreting any result.

## Existing project state

The remote project is based on official commit fa7f537, but it is not clean: seven tracked implementation files have 641 additions and 235 deletions, alongside many untracked experiment artifacts. The current project will not be edited or used as the mutable worktree for this spike.

## Existing source-labelled checkpoints

The following files were present:

| Checkpoint path suffix | Size |
|---|---:|
| gsm8k_llama31.../projection.bin | 16,787,389 bytes |
| gsm8k_qwen25_softcot.../projection.bin | 11,019,197 bytes |
| qwen3_gsm8k_softcotpp_4_10.../projection.bin | 8,419,516 bytes |
| qwen3_gsm8k_softcotpp.../projection.bin | 8,401,084 bytes |

The Qwen2.5 checkpoint name indicates GSM8K training with Qwen2.5-7B-Instruct and Qwen2.5-1.5B-Instruct. Its provenance and compatibility are not yet verified; it may be used only as an engineering preflight if plainly labelled as a pre-existing provided checkpoint. It cannot silently substitute for a documented source-training run in the final experiment.

## Data state

Only GSM8K-style train/test data are present in the project data directory. No ASDiv-Aug or StrategyQA target data are currently present. Target data must be acquired, licensed, checksummed, split deterministically, and logged before evaluation.
