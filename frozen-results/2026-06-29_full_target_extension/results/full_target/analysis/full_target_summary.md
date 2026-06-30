# Full-target evaluation summary

Extension results using existing GSM8K-trained checkpoints. These are separate from the frozen 200-example core result. Conditions run: learned SoftCoT and no-SoftCoT baseline.

| Task | Condition | Seeds | Sample size per seed | Mean accuracy | Min | Max |
|---|---|---:|---:|---:|---:|---:|
| strategyqa | learned | 3 | 229 | 0.6405 | 0.6288 | 0.6550 |
| strategyqa | baseline | 3 | 229 | 0.5342 | 0.5197 | 0.5546 |
| asdiv-aug | learned | 3 | 1038 | 0.8642 | 0.8237 | 0.9075 |
| asdiv-aug | baseline | 3 | 1038 | 0.8776 | 0.8574 | 0.8902 |

## Learned minus baseline by seed

| Seed | Task | Learned | Baseline | Δ |
|---:|---|---:|---:|---:|
| 41 | strategyqa | 0.6288 (144/229) | 0.5197 (119/229) | +0.1092 |
| 41 | asdiv-aug | 0.8613 (894/1038) | 0.8902 (924/1038) | -0.0289 |
| 42 | strategyqa | 0.6376 (146/229) | 0.5546 (127/229) | +0.0830 |
| 42 | asdiv-aug | 0.8237 (855/1038) | 0.8854 (919/1038) | -0.0617 |
| 43 | strategyqa | 0.6550 (150/229) | 0.5284 (121/229) | +0.1266 |
| 43 | asdiv-aug | 0.9075 (942/1038) | 0.8574 (890/1038) | +0.0501 |

## Mean learned-minus-baseline contrast

| Task | Mean Δ | Deltas |
|---|---:|---|
| strategyqa | +0.1063 | +0.1092, +0.0830, +0.1266 |
| asdiv-aug | -0.0135 | -0.0289, -0.0617, +0.0501 |
