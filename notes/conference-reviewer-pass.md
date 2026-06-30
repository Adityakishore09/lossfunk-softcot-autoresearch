# Conference-reviewer pass

Date: 2026-06-28

This pass is deliberately skeptical. It checks the completed Lossfunk autoresearch run for unsupported claims, confounds, missing baselines, statistics, reproducibility gaps, and references or artifact risks before paper drafting.

## Evidence inspected

- Frozen local archive: `frozen-results/2026-06-28_seed41_42_43/lossfunk_results_seed41_42_43.tar.gz`
- Archive SHA-256: `0e331230d33b09da8d87ab0000f17d1861a5ea8ced308c90bc573590b89afd8b`
- Raw results: 27 JSON files = 3 seeds × 3 tasks × 3 conditions.
- Comparison table: `frozen-results/2026-06-28_seed41_42_43/results/analysis/seed41_seed42_seed43_comparison.md`
- Summary file: `frozen-results/2026-06-28_seed41_42_43/results/analysis/summary.json`
- Full-target extension archive: `frozen-results/2026-06-29_full_target_extension/lossfunk_full_target_extension_seed41_42_43.tar.gz`
- Full-target extension SHA-256: `7d8ddf85d2dda16bdecc4465860c39c821a9878f9816f170e78ba9bae9c5cfad`
- Full-target extension summary: `frozen-results/2026-06-29_full_target_extension/results/full_target/analysis/full_target_summary.md`

## Main claim that is supported

The completed run supports only a narrow preliminary claim:

> In this three-seed, 200-example-per-condition run, a GSM8K-trained SoftCoT projection improved over the zero soft-thought control on average for GSM8K, ASDiv-Aug, and StrategyQA, and improved over the no-SoftCoT baseline on StrategyQA. It did not improve over the no-SoftCoT baseline on GSM8K and did not improve over the no-SoftCoT baseline on ASDiv-Aug in the three-seed mean.

Three-seed mean accuracies:

| Task | Learned SoftCoT | Zero control | No-SoftCoT baseline |
|---|---:|---:|---:|
| GSM8K | 0.8250 | 0.7950 | 0.8683 |
| ASDiv-Aug | 0.8567 | 0.7950 | 0.8683 |
| StrategyQA | 0.6517 | 0.5867 | 0.5367 |

Full-target learned-vs-baseline extension:

| Task | Learned SoftCoT | No-SoftCoT baseline | Mean learned-minus-baseline |
|---|---:|---:|---:|
| StrategyQA full dev (229 examples/seed) | 0.6405 | 0.5342 | +0.1063 |
| ASDiv-Aug full test (1038 examples/seed) | 0.8642 | 0.8776 | -0.0135 |

## Claims that are not supported

1. **Do not claim broad transfer improvement.** Learned SoftCoT does not beat the no-SoftCoT baseline on GSM8K or ASDiv-Aug in the three-seed mean.
2. **Do not claim the proposal's related-transfer distinction is confirmed.** The related target (ASDiv-Aug) does not show a learned-over-baseline gain on average, while the unrelated target (StrategyQA) does.
3. **Do not claim robust statistical significance.** There are only three seeds and 200 examples per task/condition. The bootstrap in `summary.json` is over seed means, not a substitute for a larger independent evaluation.
4. **Do not claim latency or throughput improvements.** Runs occurred under shared/contended GPU conditions, and seed 43 used an explicit lower-memory override.
5. **Do not claim this is a faithful full SoftCoT reproduction beyond the scoped fork.** The implementation was adapted for Qwen models, fixed subsets, and timeboxed resource constraints.

## Confounds and caveats

1. **Seed 43 resource protocol differs from seeds 41 and 42.** Seed 43 started with `MIN_GPU_FREE_MIB_OVERRIDE=30000`, `gpu_utilization_before_percent=92`, and `gpu_contention=contended`. Batch size remained 1, but the resource protocol was not identical.
2. **Shared GPU contention affects runtime and possibly stability.** The results can support accuracy observations, but latency comparisons should be treated as non-comparable.
3. **Baseline label in raw JSON is implementation-derived.** Baseline result files use `num_thought_tokens=0`; some payload metadata still reports `soft_thought_control: learned`. Tables must identify baseline from file/condition and `num_thought_tokens`, not only from that field.
4. **StrategyQA answer parsing is simple.** The evaluator searches for final yes/no tokens in decoded output. Ambiguous generations may become `None`. This should be disclosed.
5. **Fixed 200-example subsets reduce cost but limit generality.** The paper should call results preliminary and subset-based.
6. **ASDiv-Aug and GSM8K are both arithmetic-style; StrategyQA is boolean commonsense/strategy reasoning.** The observed StrategyQA gain may reflect answer-format or prompting interactions rather than the intended transfer geometry.
7. **The full-target extension still omits full zero-control runs.** It strengthens the learned-vs-baseline comparison, but the zero-control full-target comparison remains only on the fixed 200-example core subsets.

## Missing or weak baselines

The minimum required baselines are present:

- source-task GSM8K sanity check;
- related ASDiv-Aug transfer;
- unrelated StrategyQA transfer;
- no-SoftCoT baseline;
- zero soft-thought control.

Still missing for a stronger paper:

- full-dataset evaluation;
- more seeds;
- alternative base/assistant model pairs;
- target-trained upper bound;
- random learned projection control distinct from zero;
- prompt-only baselines with matched token budget;
- significance tests over item-level paired predictions.

These are follow-up work, not required for the current seven-day minimum artifact.

## Reproducibility risks

1. The remote Conda environment is on `/data2/anaconda3/envs/softcot`; a precise package export should be included if possible.
2. The frozen results archive currently contains code, logs, failures, scripts, and raw/analysis results, but not the model weights. The paper should state that public Qwen model IDs and pinned commits were used rather than redistributing weights.
3. Several setup failures occurred and must remain visible: tied-weight checkpoint serialization, FastNLP `Instance.get`, StrategyQA JSONL loader mismatch, summary overwrite refusal, and lower-memory seed-43 protocol amendment.
4. The original user-owned `/data3/Aditya_Kishore369/SoftCoT` tree was not the canonical artifact; the isolated runtime path is.

## Suggested framing for the paper

Use a negative/mixed-results framing:

> A small transfer audit of GSM8K-trained SoftCoT finds that learned soft thoughts are not a universal improvement over direct prompting. They consistently outperform a zero-vector soft-thought control, suggesting that the learned projection contains signal, but the signal does not reliably beat the no-SoftCoT baseline on arithmetic-style source/related targets. Surprisingly, the clearest learned-over-baseline gain appears on StrategyQA, the nominally unrelated target.

This is more honest and more interesting than forcing the original hypothesis.

## Required paper limitations section

The limitations section must include:

- three-seed, 200-example fixed subsets;
- shared/contended A100;
- seed 43 lower-memory override;
- Qwen-specific implementation changes;
- no target-task tuning;
- no latency claims;
- no full-dataset or multi-model generalization claim;
- baseline metadata caveat;
- all setup failures preserved.

## Verdict

The artifact is viable as an honest first-draft AI research report if it emphasizes a falsifying/mixed result rather than a success story. The strongest contribution is the disciplined transfer audit and the surprising StrategyQA-only learned-over-baseline gain, not a proof that SoftCoT improves related transfer.
