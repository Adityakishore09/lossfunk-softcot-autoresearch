# Source-trained SoftCoT projection checkpoints

This folder contains only the learned SoftCoT projection modules trained during the Lossfunk autoresearch sprint. It does **not** contain the Qwen2.5-7B or Qwen2.5-1.5B base/assistant model weights.

These files were copied from the isolated lab-server runtime:

```text
/data3/Aditya_Kishore369/lossfunk-autoresearch-runtime/gsm8k-asdiv-strategyqa-transfer/ckpt/
```

They correspond to the GSM8K-source-trained checkpoints used for the reported source, related-transfer, unrelated-transfer, and full-target evaluations. No target-task tuning was performed for ASDiv-Aug or StrategyQA.

| Seed | Relative file | Bytes | SHA-256 |
|---:|---|---:|---|
| 41 | `seed_41/projection.bin` | 11,019,197 | `D864A7302DAF554EA5309B08B348279A10481FD2E894A48845AE5CB7DFB1B7BB` |
| 42 | `seed_42/projection.bin` | 11,019,197 | `5BEA24DF89E88E55FF0D9987759F52B1E05F0A4FEA94F5059F2DE843B96B156C` |
| 43 | `seed_43/projection.bin` | 11,019,197 | `9F8E458170D39EC2549AB37D5A31A0A6A6224AFEA214FD8E64366B17E1B80441` |

To re-run evaluation from these projections, download the pinned public base/assistant model pair with `scripts/download_models.py`, then pass the relevant `projection.bin` as the SoftCoT projection parameter file. The exact server-side commands and run configurations are recorded in `logs/commands.md` and `frozen-results/**/run_config.txt`.
