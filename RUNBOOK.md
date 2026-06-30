# Remote runbook

Use only the isolated runtime, never the existing dirty project:

    /data3/Aditya_Kishore369/lossfunk-autoresearch-runtime/gsm8k-asdiv-strategyqa-transfer

The fixed split manifest already exists. Do not rerun scripts/build_fixed_splits.py, regenerate target samples, alter source/target data, or run the legacy run_batch_softcot.sh.

## One-time, download-only setup

Run only if the isolated models directory is absent:

    /data2/anaconda3/envs/softcot/bin/python scripts/download_models.py

This downloads the pinned public Qwen2.5 7B/1.5B model pair. It does not run inference or training.

## Experiments

For each source-training seed, run:

    bash scripts/run_seed.sh 41
    bash scripts/run_seed.sh 42
    bash scripts/run_seed.sh 43

Run one seed at a time and wait for it to finish. Each seed:

1. trains only SoftCoT's projection component on GSM8K;
2. evaluates the source GSM8K fixed test set;
3. evaluates ASDiv-Aug and StrategyQA with no target-task tuning;
4. evaluates learned SoftCoT, zero-vector SoftCoT, and no-SoftCoT on every fixed set;
5. writes raw JSON results, logs, GPU snapshots, checksums, and the source checkpoint under results/raw/seed_SEED.

All runs use the fixed 200-example subsets, one candidate, four soft-thought tokens where applicable, and a 512-token generation limit. The output directories are non-overwriting by design.

### Reduced-memory fallback

When at least 50 GiB of GPU memory is free, a documented batch-1 memory-feasibility run is permitted, including under the user-authorized contended-GPU protocol:

    bash scripts/run_seed.sh 41 1

This is a reduced-batch configuration, not an official batch-8 reproduction. If it completes without an out-of-memory failure, use the same batch size for seeds 42 and 43:

    bash scripts/run_seed.sh 42 1
    bash scripts/run_seed.sh 43 1

The script records the batch size, pre-run GPU utilization, free memory, and `gpu_contention` status in each result directory. A contended-GPU run is preliminary evidence only: report its contention status and do not treat its latency as comparable with an idle-GPU run.

## Read-only monitoring

    watch -n 5 nvidia-smi

The runner permits user-authorized concurrent execution but retains the memory safety guard. If a run exits with code 75, free GPU memory before re-running the same command. Monitor the other workloads throughout the run.

## Result aggregation

Only after all planned seeds are complete, run:

    /data2/anaconda3/envs/softcot/bin/python scripts/summarize_results.py --runtime-root .

This writes results/analysis/summary.json without changing raw results. It reports condition-wise accuracy and latency plus the pre-registered difference of differences:

    (ASDiv-Aug learned minus baseline) minus (StrategyQA learned minus baseline)
