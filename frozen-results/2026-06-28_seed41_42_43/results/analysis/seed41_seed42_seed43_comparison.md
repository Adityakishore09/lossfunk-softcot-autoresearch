# Seed 41 vs Seed 42 vs Seed 43 comparison

Each value uses a completed 200-example fixed split. Seed 43 used the explicit lower-memory contended protocol (`min_gpu_free_mib=30000`).

| Task | Condition | Seed 41 | Seed 42 | Seed 43 | Mean |
|---|---|---:|---:|---:|---:|
| gsm8k | learned_softcot | 0.835 (167/200) | 0.760 (152/200) | 0.880 (176/200) | 0.825 |
| gsm8k | zero_control | 0.805 (161/200) | 0.775 (155/200) | 0.805 (161/200) | 0.795 |
| gsm8k | no_softcot_baseline | 0.855 (171/200) | 0.870 (174/200) | 0.880 (176/200) | 0.868 |
| asdiv-aug | learned_softcot | 0.850 (170/200) | 0.835 (167/200) | 0.885 (177/200) | 0.857 |
| asdiv-aug | zero_control | 0.770 (154/200) | 0.815 (163/200) | 0.800 (160/200) | 0.795 |
| asdiv-aug | no_softcot_baseline | 0.880 (176/200) | 0.885 (177/200) | 0.840 (168/200) | 0.868 |
| strategyqa | learned_softcot | 0.635 (127/200) | 0.655 (131/200) | 0.665 (133/200) | 0.652 |
| strategyqa | zero_control | 0.590 (118/200) | 0.605 (121/200) | 0.565 (113/200) | 0.587 |
| strategyqa | no_softcot_baseline | 0.530 (106/200) | 0.565 (113/200) | 0.515 (103/200) | 0.537 |
