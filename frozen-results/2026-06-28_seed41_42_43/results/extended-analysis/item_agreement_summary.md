# Item-level agreement/error analysis

Counts are paired by fixed-split index when present, otherwise by qid or question SHA-256. Positive Δ means the first condition has more correct items than the second condition on the same examples.

| Task | Comparison | Paired N | First-only correct | Second-only correct | Δ accuracy |
|---|---|---:|---:|---:|---:|
| gsm8k | learned_softcot_vs_no_softcot_baseline | 600 | 36 | 62 | -0.0433 |
| gsm8k | learned_softcot_vs_zero_control | 600 | 82 | 64 | +0.0300 |
| gsm8k | zero_control_vs_no_softcot_baseline | 600 | 36 | 80 | -0.0733 |
| asdiv-aug | learned_softcot_vs_no_softcot_baseline | 600 | 23 | 30 | -0.0117 |
| asdiv-aug | learned_softcot_vs_zero_control | 600 | 61 | 24 | +0.0617 |
| asdiv-aug | zero_control_vs_no_softcot_baseline | 600 | 21 | 65 | -0.0733 |
| strategyqa | learned_softcot_vs_no_softcot_baseline | 600 | 117 | 48 | +0.1150 |
| strategyqa | learned_softcot_vs_zero_control | 600 | 106 | 67 | +0.0650 |
| strategyqa | zero_control_vs_no_softcot_baseline | 600 | 97 | 67 | +0.0500 |
