# Progress log

## 2026-06-22 — Scope selection and initialization

- Read AGENTS.md, voila.md, research-philosophy.md, and inputs/submitted-proposal.pdf before taking research actions.
- Audited hardware, software, local model/dataset caches, and non-secret credential indicators.
- Extracted and read all ten pages of the submitted proposal. Its minimum viable experiment is GSM8K to ASDiv-Aug versus GSM8K to StrategyQA.
- Presented exactly three scored scopes; the user selected Scope 1.
- Created this one selected-spike directory and backfilled the pre-selection audit and session record.
- Locked the minimum comparisons in README.md.
- Inspected the official SoftCoT paper and public implementation without cloning or downloading the repository, datasets, models, or checkpoints.
- Wrote the pre-execution transfer protocol and an implementation-feasibility audit.
- Cloned an unmodified, shallow copy of the official implementation into code/softcot-upstream at commit fa7f537d1d0affa430851315edf68746d410b59c.
- Confirmed locally that the official evaluator supports the three selected task names, but the standard no-SoftCoT branch removes the thought slots rather than preserving a matched zero-vector intervention. A separate, documented control implementation will be needed.

### Current state

Preparation only. No experiment, dependency install, code/data/model download, model inference, cloud provisioning, external API call, or paid compute has occurred.

### Next safe actions

1. Identify an auditable SoftCoT implementation and its exact licensing, model, and hardware requirements.
2. Design fixed, source/target splits and compute-matched baseline protocol before executing a run.
3. Establish a costed hosted-GPU plan that cannot exceed the US$50.00 ceiling, if hosted compute is needed.
4. Resolve the initial literature-search access failure using a direct primary-source lookup before selecting an implementation.
5. Resolve access to a hosted NVIDIA GPU before any model/data download or run; the local laptop cannot execute the official method.

## 2026-06-22 — Lab server made available

The user provided an in-scope SSH endpoint for a lab server reported to have an NVIDIA A100 80GB and existing SoftCoT files. Pending a read-only SSH audit, this may remove the local-compute blocker without requiring commercial cloud provisioning.

### SSH status

The configured account was discovered as gaurav@172.30.1.70. A strict non-interactive probe reached the host but failed authentication before any remote command ran. The remaining blocker is passwordless credential provisioning to this Codex session. No password or private key was requested, read, or stored.

The user subsequently identified the existing remote source location as /data3/Aditya_Kishore369/SoftCoT. This location has not yet been accessed by Codex.

The user authorized an ephemeral keypair. It was generated locally and its public half is awaiting installation in the remote account's authorized_keys file. No remote authentication retry will be made until the user confirms installation.

## 2026-06-22 — Remote audit succeeded

Passwordless SSH now works. The reported A100-80GB, memory, disk capacity, and existing SoftCoT path were independently verified. At the audit time the GPU was at 100% utilization with 29.1 GiB allocated, so no model, installation, or experiment was launched. Read-only source/environment inspection may proceed without interfering with the active GPU workload.

The existing remote tree is at upstream commit fa7f537 but is materially dirty and contains prior experimental work. It will be preserved and not used as the mutable project worktree. The remote environment is available by an explicit Conda-prefix path, not by the softcot name in the non-interactive SSH context.

Read-only inventory found GSM8K source data and four pre-existing GSM8K-labelled projection checkpoints, but no local ASDiv-Aug or StrategyQA target data. The project will distinguish any engineering preflight that uses a provided checkpoint from a later documented source-training run.

An isolated fresh runtime clone was created at /data3/Aditya_Kishore369/lossfunk-autoresearch-runtime/gsm8k-asdiv-strategyqa-transfer, pinned to upstream commit fa7f537. Public Qwen2.5-7B-Instruct and Qwen2.5-1.5B-Instruct revision IDs were recorded but no weights downloaded. Official ASDiv-Aug test and StrategyQA dev evaluation files were downloaded to that runtime, validated, and hashed.

The reproducible execution assets are now in the isolated runtime: build_fixed_splits.py (already executed), download_models.py, run_seed.sh, summarize_results.py, and RUNBOOK.md. The runner enforces idle-GPU, non-overwrite, source-only training, fixed targets, and logged controls. It has not been started because the GPU remains busy and the automated model-download request was rejected before execution.

## Shared-GPU decision

Current A100 state is 36.2 GiB free at 100% utilization. The official batch-8 7B-plus-1.5B source-training run will not be attempted concurrently. A later reduced-batch memory pilot is possible only in a scheduled/approved low-utilization window and must be labelled as a pilot before any full experiment is attempted.

The runner now accepts a batch-size argument. Batch 1 or 2 requires at least 50 GiB free and at most 10% utilization; batch 4 or 8 requires at least 70 GiB free. Every run writes this configuration to run_config.txt. No such run has been started.

A user attempt to start seed 41 at batch size 1 was safely refused because free memory was 52,043 MiB but utilization remained 100%. No model was loaded and no project run began.

## Autovoila workflow alignment audit

Completed:

1. Read the proposal and governing workflow materials.
2. Audited local and remote resources.
3. Presented exactly three scopes and obtained the user's selection.
4. Created one selected-spike directory with environment, cost, progress, intervention, command, failure, and prompt/session logs.
5. Locked source-only GSM8K training, fixed GSM8K/ASDiv-Aug/StrategyQA evaluation subsets, and no-SoftCoT plus zero-vector controls.
6. Prepared an isolated, reproducible server runtime without modifying the user's pre-existing SoftCoT worktree.

Still required:

1. Download the pinned public model pair after authorization.
2. Execute source-only training and all locked comparisons when the shared GPU is idle.
3. Collect raw results, latency, hardware state, costs, and failures.
4. Run the required conference-reviewer pass.
5. Produce the AI-authored LaTeX paper, compiled PDF, code, figures, raw-result appendix, requirements, and full session appendix.

The user's independent critique/reflection deck is explicitly out of scope for the agent.

All subsequent decisions, commands, failures, results, costs, prompts, and user interventions will be appended rather than rewritten.

## 2026-06-23 — GPU concurrency decision

The GPU has enough free memory for the reduced batch-size-one runner but is already at 99% compute utilization. CUDA may time-slice concurrent processes, but this would not constitute an idle-GPU, controlled run: it would introduce uncontrolled contention and invalidate recorded latency comparability. The runner remains intentionally blocked until utilization is at or below 10%, unless a revised experiment protocol is explicitly designed and authorized; that would not satisfy the currently locked minimum protocol.

## 2026-06-23 — User-authorized contended-GPU amendment

The user authorized removal of the utilization gate after observing `utilization=99%` and `free_memory=52043 MiB` for a batch-one run. The runner now proceeds when the appropriate memory threshold is met, writes pre-run utilization and free memory to `run_config.txt`, and flags `gpu_contention=contended` when utilization exceeds 10%. The source-only design, fixed data, conditions, seed plan, non-overwrite protection, and memory threshold remain unchanged. Results from this amended protocol cannot support latency or fair-throughput claims and must be described as preliminary under concurrent GPU contention.

## 2026-06-23 — Seed 41 started under contended-GPU protocol

User-provided live terminal evidence shows `bash scripts/run_seed.sh 41 1` passed the amended guard, warned that initial utilization was 99%, loaded all four checkpoint shards, initialized `EfficientSoftCoTFromSmallModel`, and began source GSM8K training. At screenshot time, progress was 154/74,730 at 1.78 it/s (displayed ETA 11:37:14). This is an in-progress run, not a result. The live process monitor showed approximately 55,634 MiB allocated in total across the four visible compute processes, leaving roughly 26 GiB of nominal VRAM; available VRAM is not equivalent to spare compute capacity.

## 2026-06-24 — Checkpoint fix and fresh seed-41 restart

The first seed-41 attempt failed at the first epoch checkpoint because generic Trainer safetensors serialization cannot serialize Qwen's tied assistant-model weights. `train_softcot.py` was amended to use `save_strategy='no'`: epoch evaluation remains enabled, but intermediate generic full-model checkpoints are disabled. The pre-existing final line `model.save_pretrained(save_model_dir)` remains and saves only the required `projection.bin` (the frozen base and assistant models are not tuned). The patch compiled locally and on the lab server. The failed evidence was archived without deletion, and a fresh seed-41 run began in tmux session `lossfunk_seed41_retry` at 100% initial GPU utilization under the authorized contended-GPU protocol. The displayed shard load reached 2/4 when launch verification ended. No scientific result exists yet.

## 2026-06-25 — Seed-41 training completed; evaluation resume required

Read-only inspection after the user reported the tmux session was gone showed that seed-41 source training completed under the user-authorized contended-GPU protocol and saved the expected projection checkpoint. The run then exited during the first evaluation because `evaluate_softcot.py` attempted dict-style `.get()` metadata access on a FastNLP `Instance`. The first evaluation log contains one correct GSM8K example but no completed JSON output, so no accuracy result should be reported yet.

The evaluator has been patched locally and in the isolated server runtime to make optional metadata access robust. Next action: resume only the missing evaluations for seed 41 using the saved checkpoint; do not rerun seed-41 training or start seed 42 until seed-41 evaluations complete.

## 2026-06-25 — Eval resume delayed by GPU memory pressure

The user attempted to launch `tmux new-session -d -s lossfunk_seed41_eval 'bash scripts/resume_seed_evals.sh 41 50000'`, but the tmux session vanished before attachment. Read-only server inspection showed the script and patch are present, but only 9,032 MiB of A100 memory was free while the resume script requires 50,000 MiB. The launch therefore exited at the resource guard before loading a model or writing new results. Seed-41 still needs evaluation resume when enough memory is available.

The 50,000 MiB threshold should be treated as a safety margin, not a proven minimum. If the user accepts the risk of a possible OOM/setup failure, evaluation resume can be attempted with a lower threshold once substantially more than 9 GiB is free; this would remain under the already disclosed contended-GPU protocol and must be logged.

## 2026-06-25 — Seed-41 evaluation is running

The user supplied live terminal output from the resumed evaluation. At the snapshot, the current condition had processed 69/200 examples, with `Correct Count: 58/69` after the previous example and a displayed rate of about 18.08 seconds per item. This indicates the patched evaluator is running and computing correctness. It is preliminary live progress only; no result should be claimed until the corresponding JSON file is completed and checksummed.

## 2026-06-26 — Six seed-41 evaluation JSONs completed; StrategyQA loader patched

The user's terminal output reported a completed condition with `Final Accuracy: 0.880000 (176/200)` immediately before the StrategyQA crash. Server inspection showed six completed seed-41 JSON result files:

- `gsm8k_learned.json`
- `gsm8k_zero.json`
- `gsm8k_baseline.json`
- `asdiv-aug_learned.json`
- `asdiv-aug_zero.json`
- `asdiv-aug_baseline.json`

The run then failed before `strategyqa_learned.json` because the StrategyQA loader expected a JSON array while the fixed split is JSONL. `data_loader.py` has been patched locally and on the isolated server runtime. A smoke test verified `strategyqa_fixed_len 200` and boolean labels. GPU inspection after the patch showed 41,861 MiB free, enough for the 30,000 MiB resume threshold, but the agent-side tmux launch was not approved, so the user should resume manually or approve a launch in a later turn.

## 2026-06-26 — StrategyQA learned evaluation resumed in existing tmux

After explicit user authorization, the patched resume command was sent into the existing attached `lossfunk_seed41_eval` tmux session. The script skipped the six completed GSM8K/ASDiv JSON files, archived the stale incomplete `strategyqa_learned.log`, loaded the projection checkpoint, and began StrategyQA learned evaluation. A follow-up status snapshot showed active processes for `resume_seed_evals.sh` and `evaluate_softcot.py`; the pane had advanced past the former JSONL crash and had processed 4/200 StrategyQA examples. This is in-progress evidence only; no StrategyQA accuracy should be reported until JSON files are written.

## 2026-06-27 — Seed-41 evaluation complete and summarized

The user reported the final terminal line `Final Accuracy: 0.530000 (106/200)`, after which the shell prompt returned. Server verification found all nine expected seed-41 JSON result files and ran `scripts/summarize_results.py --runtime-root .`, producing `results/analysis/summary.json`.

Seed-41 accuracies on 200-example fixed splits:

| Task | Condition | Accuracy | Correct |
|---|---|---:|---:|
| GSM8K | learned SoftCoT | 0.835 | 167/200 |
| GSM8K | zero soft-thought control | 0.805 | 161/200 |
| GSM8K | no-SoftCoT baseline | 0.855 | 171/200 |
| ASDiv-Aug | learned SoftCoT | 0.850 | 170/200 |
| ASDiv-Aug | zero soft-thought control | 0.770 | 154/200 |
| ASDiv-Aug | no-SoftCoT baseline | 0.880 | 176/200 |
| StrategyQA | learned SoftCoT | 0.635 | 127/200 |
| StrategyQA | zero soft-thought control | 0.590 | 118/200 |
| StrategyQA | no-SoftCoT baseline | 0.530 | 106/200 |

Preliminary interpretation: for this single contended seed, learned SoftCoT improves over the zero control on all three tasks and over the no-SoftCoT baseline on StrategyQA, but it underperforms the no-SoftCoT baseline on GSM8K and ASDiv-Aug. This is not yet a robust multi-seed claim; it is one seed under a disclosed contended-GPU protocol.

## 2026-06-27 — Seed-42 launch prepared but not started

With seed 41 complete, the next planned action is seed 42 using the same batch-size-one protocol. A read-only server check confirmed the A100 was idle (`17 MiB` used, `81135 MiB` free, `0%` utilization), no seed-42 result directory existed, and no project SoftCoT process was active. An attempted automated launch did not start because the process guard matched the SSH wrapper command itself. A retry request was rejected, so seed 42 remains not started by the agent. The user should run `bash scripts/run_seed.sh 42 1` in tmux, or approve a future agent launch.

The user asked whether seed 42 can be run with batch size 2 because the GPU is empty. Technically yes, but the current seed plan is comparable only if seed 42 uses the same batch size as seed 41. Recommended main-protocol command remains `bash scripts/run_seed.sh 42 1`; `bash scripts/run_seed.sh 42 2` should be used only if the user accepts a speed-oriented protocol amendment.

## 2026-06-27 — Seed-42 evaluation complete

The user reported the final terminal line `Final Accuracy: 0.565000 (113/200)`. Remote verification found all nine expected seed-42 JSON result files plus `gpu_after.csv` and `checksums.sha256`. This means seed 42 completed training and all locked evaluations under the batch-size-one protocol. The agent requested permission to rerun `scripts/summarize_results.py --runtime-root .`, but that request was rejected, so `results/analysis/summary.json` was not updated in this turn.

Seed-42 accuracies on 200-example fixed splits:

| Task | Condition | Accuracy | Correct |
|---|---|---:|---:|
| GSM8K | learned SoftCoT | 0.760 | 152/200 |
| GSM8K | zero soft-thought control | 0.775 | 155/200 |
| GSM8K | no-SoftCoT baseline | 0.870 | 174/200 |
| ASDiv-Aug | learned SoftCoT | 0.835 | 167/200 |
| ASDiv-Aug | zero soft-thought control | 0.815 | 163/200 |
| ASDiv-Aug | no-SoftCoT baseline | 0.885 | 177/200 |
| StrategyQA | learned SoftCoT | 0.655 | 131/200 |
| StrategyQA | zero soft-thought control | 0.605 | 121/200 |
| StrategyQA | no-SoftCoT baseline | 0.565 | 113/200 |

Preliminary two-seed pattern: learned SoftCoT remains above zero and baseline on StrategyQA, but below baseline on GSM8K and ASDiv-Aug. On GSM8K seed 42, learned SoftCoT is also below the zero control. These results narrow the claim substantially: the strongest observed signal is not broad related-transfer improvement, but a possible StrategyQA-specific gain relative to the prompt-only baseline.

## 2026-06-27 — Combined two-seed summary and separate comparison files

The user asked to keep seed 42 separate from seed 41 while showing the difference. The agent created:

- `results/analysis/seed_level_results.csv`
- `results/analysis/seed41_seed42_comparison.csv`
- `results/analysis/seed41_seed42_comparison.md`

The comparison file keeps the seeds separate and reports seed42-minus-seed41 deltas for each task/condition. The combined `results/analysis/summary.json` was regenerated after archiving the pre-existing analysis directory; it now aggregates 18 source JSON files (2 seeds × 3 tasks × 3 conditions).

Two-seed mean accuracies from the regenerated summary:

| Task/condition | Seed count | Mean | Min | Max |
|---|---:|---:|---:|---:|
| GSM8K learned | 2 | 0.7975 | 0.7600 | 0.8350 |
| GSM8K zero | 2 | 0.7900 | 0.7750 | 0.8050 |
| GSM8K baseline | 2 | 0.8625 | 0.8550 | 0.8700 |
| ASDiv-Aug learned | 2 | 0.8425 | 0.8350 | 0.8500 |
| ASDiv-Aug zero | 2 | 0.7925 | 0.7700 | 0.8150 |
| ASDiv-Aug baseline | 2 | 0.8825 | 0.8800 | 0.8850 |
| StrategyQA learned | 2 | 0.6450 | 0.6350 | 0.6550 |
| StrategyQA zero | 2 | 0.5975 | 0.5900 | 0.6050 |
| StrategyQA baseline | 2 | 0.5475 | 0.5300 | 0.5650 |

## 2026-06-27 — Next planned action

Recommended next experiment: run seed 43 using the same protocol as seeds 41 and 42 (`bash scripts/run_seed.sh 43 1`) if the A100 is available. Do not change the batch size for seed 43 if the goal is a clean three-seed estimate. After seed 43 completes, rerun summary generation, preserve seed-level comparisons, copy raw results/analysis artifacts, then proceed to the required conference-reviewer pass and AI-authored paper.

The first seed-43 attempt was refused by the runner because only 30,850 MiB was free. Seed 43 remains not started; wait for at least 50,000 MiB free or stop at seeds 41 and 42.

## 2026-06-27 — Seed-43 started under explicit 30 GiB memory-override protocol

After user authorization, the runner was amended to permit an explicit `MIN_GPU_FREE_MIB_OVERRIDE` environment variable. This is a protocol amendment: seed 43 keeps batch size 1, fixed splits, and conditions, but starts under a lower memory guard than seeds 41 and 42. The remote run config records the override:

~~~text
seed=43
batch_size=1
min_gpu_free_mib=30000
min_gpu_free_mib_source=override
gpu_utilization_before_percent=92
gpu_memory_free_before_mib=30850
gpu_contention=contended
~~~

The first tmux-send attempt left the shell at a continuation prompt; it was cancelled with `Ctrl-C` and resent without quoting the path. Seed 43 then loaded model shards, initialized `EfficientSoftCoTFromSmallModel`, preprocessed GSM8K train/test data, and reached 53/74,730 training steps in the captured pane. Current caveat: this seed is not directly identical to seeds 41/42 in resource protocol, and if it completes it must be flagged as a lower-memory contended run.

## 2026-06-28 — Seed-43 complete and three-seed analysis regenerated

Seed 43 completed training and all nine locked evaluations. The final terminal output reported `strategyqa_baseline` accuracy 0.515000 (103/200). Server verification found all expected seed-43 files, including `gpu_after.csv` and `checksums.sha256`. The analysis directory was archived to `results/analysis_archive_before_seed43_2026-06-28_150407`, then regenerated from all 27 raw JSON files. New files:

- `results/analysis/summary.json`
- `results/analysis/seed_level_results.csv`
- `results/analysis/seed41_seed42_seed43_comparison.csv`
- `results/analysis/seed41_seed42_seed43_comparison.md`

Seed-43 accuracies on 200-example fixed splits:

| Task | Condition | Accuracy | Correct |
|---|---|---:|---:|
| GSM8K | learned SoftCoT | 0.880 | 176/200 |
| GSM8K | zero soft-thought control | 0.805 | 161/200 |
| GSM8K | no-SoftCoT baseline | 0.880 | 176/200 |
| ASDiv-Aug | learned SoftCoT | 0.885 | 177/200 |
| ASDiv-Aug | zero soft-thought control | 0.800 | 160/200 |
| ASDiv-Aug | no-SoftCoT baseline | 0.840 | 168/200 |
| StrategyQA | learned SoftCoT | 0.665 | 133/200 |
| StrategyQA | zero soft-thought control | 0.565 | 113/200 |
| StrategyQA | no-SoftCoT baseline | 0.515 | 103/200 |

Three-seed mean accuracies:

| Task | Learned | Zero | Baseline |
|---|---:|---:|---:|
| GSM8K | 0.8250 | 0.7950 | 0.8683 |
| ASDiv-Aug | 0.8567 | 0.7950 | 0.8683 |
| StrategyQA | 0.6517 | 0.5867 | 0.5367 |

Interpretation to carry forward: learned SoftCoT consistently improves over the zero control on average, and consistently improves over baseline on StrategyQA, but it does not beat the no-SoftCoT baseline on GSM8K and only narrowly underperforms baseline on ASDiv-Aug in the three-seed mean. Seed 43 must be caveated as a lower-memory contended run.

## 2026-06-28 — Experiment phase complete; analysis/artifact phase next

The core minimum comparison is now complete for three seeds: GSM8K source sanity, ASDiv-Aug related transfer, StrategyQA unrelated transfer, no-SoftCoT baseline, and zero soft-thought control. The next step is to freeze and package raw results, generate final tables/figures, run the required conference-reviewer pass, and draft the AI-authored paper. No Router, Verifier, Memory, or extra exploratory module should be added unless the core artifact is already complete and time remains.

## 2026-06-28 — Frozen archive copied locally and reviewer pass started

The remote archive `lossfunk_results_seed41_42_43.tar.gz` was verified at 3.2 MiB with SHA-256 `0e331230d33b09da8d87ab0000f17d1861a5ea8ced308c90bc573590b89afd8b`. It contains all three raw seed directories, analysis outputs, failures, scripts, and code files. The archive was copied into `frozen-results/2026-06-28_seed41_42_43/`, locally checksum-verified, and extracted.

The required conference-reviewer pass was drafted at `notes/conference-reviewer-pass.md`. Its verdict is mixed/negative: the artifact is viable only if framed as a disciplined preliminary transfer audit, not as confirmation that SoftCoT improves related transfer.

## 2026-06-28 — Additional-experiment planning

The user asked whether more experiments can strengthen the proposal. Recommended next experiments, if any, should be small and diagnostic: larger evaluation subsets/full target-dev evaluation using existing checkpoints, item-level paired significance/error-overlap analysis, and prompt-format/token-budget controls. Expensive new modules or target-tuned training should remain out of scope unless the core paper artifact is already secure.

## 2026-06-28 — Item-level analysis completed; full-target runner prepared

The item-level agreement/error analysis was completed locally from the frozen 3-seed raw results. Outputs:

- `frozen-results/2026-06-28_seed41_42_43/results/extended-analysis/item_agreement_summary.csv`
- `frozen-results/2026-06-28_seed41_42_43/results/extended-analysis/item_agreement_summary.md`
- `frozen-results/2026-06-28_seed41_42_43/results/extended-analysis/item_agreement_detail.json`

Aggregate paired findings across 600 task examples (3 seeds × 200 fixed examples):

| Task | Comparison | First-only correct | Second-only correct | Δ accuracy |
|---|---|---:|---:|---:|
| GSM8K | learned vs baseline | 36 | 62 | -0.0433 |
| GSM8K | learned vs zero | 82 | 64 | +0.0300 |
| ASDiv-Aug | learned vs baseline | 23 | 30 | -0.0117 |
| ASDiv-Aug | learned vs zero | 61 | 24 | +0.0617 |
| StrategyQA | learned vs baseline | 117 | 48 | +0.1150 |
| StrategyQA | learned vs zero | 106 | 67 | +0.0650 |

This strengthens the existing interpretation: the StrategyQA learned-over-baseline gain is broad at the item level, while GSM8K and ASDiv-Aug do not show a learned-over-baseline advantage.

The agent also prepared `scripts/run_full_target_evals.sh` for larger/full target evaluation under `results/full_target/`. Remote execution is pending because SSH to the lab server timed out.

## 2026-06-28 — Full-target runner synced; GPU watcher launched

SSH became reachable again. The server has the full target files `data/external/asdiv-aug-test.jsonl` and `data/external/strategyqa-dev.json`, and projection checkpoints for seeds 41, 42, and 43. The GPU was still occupied, so the full-target runner was copied to the isolated runtime, syntax-checked, and a watcher tmux session `lossfunk_full_target_eval` was launched. It waits for at least 30,000 MiB free and then runs:

~~~bash
TASKS="strategyqa asdiv-aug" CONDITIONS="learned baseline" bash scripts/run_full_target_evals.sh 41 30000
TASKS="strategyqa asdiv-aug" CONDITIONS="learned baseline" bash scripts/run_full_target_evals.sh 42 30000
TASKS="strategyqa asdiv-aug" CONDITIONS="learned baseline" bash scripts/run_full_target_evals.sh 43 30000
~~~

Outputs will be separate from the frozen core results under `results/full_target/seed_41`, `results/full_target/seed_42`, and `results/full_target/seed_43`. Initial watcher observation: only 12,750 MiB free and 100% utilization, so no model evaluation had started yet.

## 2026-06-28 — Full-target evaluation started

The user reported that at least 30 GiB was free and asked to start the process. The watcher had already started at its next polling interval when free memory reached 31,952 MiB. A status check showed active `evaluate_softcot.py` for seed 41, full StrategyQA dev (`data/external/strategyqa-dev.json`), learned SoftCoT condition. The pane showed `START_FULL_TARGET_SEED_41`, checkpoint load, model initialization, and progress at 0/229. Outputs are under `results/full_target/seed_41/`.

## 2026-06-29 — Full-target extension complete

The user showed the final pane with `FULL_TARGET_ALL_DONE`. Server verification found all 12 expected full-target JSON files: 3 seeds × 2 tasks (StrategyQA full dev, ASDiv-Aug full test) × 2 conditions (learned, baseline). Summary files were generated under `results/full_target/analysis/` and archived as `lossfunk_full_target_extension_seed41_42_43.tar.gz`.

Full-target mean accuracies:

| Task | Learned | Baseline | Learned − baseline |
|---|---:|---:|---:|
| StrategyQA full dev | 0.6405 | 0.5342 | +0.1063 |
| ASDiv-Aug full test | 0.8642 | 0.8776 | -0.0135 |

Per-seed learned-minus-baseline deltas:

| Seed | StrategyQA | ASDiv-Aug |
|---:|---:|---:|
| 41 | +0.1092 | -0.0289 |
| 42 | +0.0830 | -0.0617 |
| 43 | +0.1266 | +0.0501 |

This extension strengthens the final interpretation: the StrategyQA gain is stable on full dev, while ASDiv-Aug remains mixed/slightly negative on average. The proposal's related-transfer hypothesis is therefore not supported by the extension.

## 2026-06-30 — Artifact-completion phase

The attached Lossfunk interview process, AutoVoila deck, and original proposal were inspected to align the remaining work. The experiment phase should now close unless a concrete reviewer-blocking gap is found. Remaining work is to draft the AI-authored paper, compile and verify the PDF, package code/results/logs, include the prompt/session appendix, and have the human independently prepare the critique/reflection deck. The final framing should emphasize a mixed/negative transfer audit: learned SoftCoT contains signal relative to the zero control, but the related-transfer hypothesis was not supported; the clearest learned-over-baseline gain appeared on StrategyQA.

## 2026-06-30 — AI-authored first-draft paper created

The first-draft paper has been created under `paper/`:

- `paper/main.tex`: canonical CAISc-style LaTeX source.
- `paper/references.bib`: checked bibliography.
- `paper/main.pdf`: fallback generated PDF for review.
- `paper/build_pdf.py`: fallback PDF builder.
- `paper/figures/`: generated figures.
- `paper/rendered/`: rendered page PNGs used for visual QA.
- `paper/COMPILE_NOTES.md`: transparent note that no local TeX compiler was installed.

Local TeX tools (`pdflatex`, `xelatex`, `lualatex`, `latexmk`, `tectonic`, `pandoc`) were unavailable, so the PDF was generated with the bundled Python/reportlab runtime while preserving `main.tex` as the canonical source. Poppler rendering of the fallback PDF succeeded via the direct executable and all four rendered pages were visually inspected. SHA-256:

- `main.pdf`: `E2639F36159E2ADF8BBD47FDDCEE48CB8805FA4D7F9081156AC65581F2660D02`
- `main.tex`: `FBB61FCF65F42C7BEB287306D706C9FE15D83607DC45930C3E5F58E327B5AD9F`
- `references.bib`: `3F54CEFA19DC0A36A0338AA2C4583B7DF2C8BE8B127B75C0E926B0C152603511`

The paper frames the sprint as a mixed/negative audit: the related-transfer hypothesis was not supported, learned SoftCoT beat zero controls, and StrategyQA showed the clearest learned-over-baseline gain.

## 2026-06-30 — Official autoresearch-stage checklist captured

The official Lossfunk `autoresearch-stage.md` guidance was fetched after user confirmation and saved at `external-guidance/autoresearch-stage.md`. A local checklist was created at `notes/autoresearch-submission-checklist.md`. The required submission is two-part: (1) the AI-produced artifact in a GitHub repository, unpolished and transparent, and (2) a human-authored deck PDF focused on starting question, autoresearch flow, results, learning, critique, reflection on autoresearch limits, and revised research plan.

## 2026-06-30 — GitHub-ready submission folder prepared

A clean local repository-ready copy was prepared at `github-submission/lossfunk-softcot-autoresearch`. It contains the selected spike's paper, code, fixed data files, frozen result archives/extractions, logs, external Lossfunk guidance snapshot, runbook, and submission checklist. Nested upstream `.git` directories copied from code snapshots were removed so the folder could be initialized as a single standalone repository. No model weights or private SSH keys were included. A local Git repository was initialized on branch `main` and committed. Because the GitHub CLI is not installed in the local environment, repository creation and push require the user to create `Adityakishore09/lossfunk-softcot-autoresearch` on GitHub and then push the prepared local commit.

## 2026-06-30 — Server artifact audit and projection checkpoints added

A read-only inventory of `/data3/Aditya_Kishore369/lossfunk-autoresearch-runtime/gsm8k-asdiv-strategyqa-transfer` showed that the server's result JSONs, logs, summary files, failure folders, scripts, and tar archives were already represented in the frozen result folders. The remaining essential server-side artifacts not yet present locally were the source-trained SoftCoT projection checkpoints for seeds 41, 42, and 43. These are small projection modules, not full model weights, and were copied into `checkpoints/softcot-projections/` with SHA-256 hashes and provenance notes. The full `models/` directory, full target data files, and server `.git` directory were intentionally not copied.

## 2026-06-30 — GitHub repository pushed

The user successfully pushed the prepared submission repository to GitHub:

```text
https://github.com/Adityakishore09/lossfunk-softcot-autoresearch
```

The remote branch `main` was created and set as the upstream for the local branch. The final remaining submission work is a human-authored critique/reflection deck PDF and a final manual check that the GitHub repository renders the paper, README, logs, frozen results, and checkpoints as expected.
