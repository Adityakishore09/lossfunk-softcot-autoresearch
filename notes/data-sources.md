# Target-data provenance

All target data reside only in the isolated lab-server runtime. They will not be committed or redistributed with this artifact; this note and the acquisition command make them reproducible.

## ASDiv-Aug

- Source: xuyige/ASDiv-Aug on Hugging Face, the dataset linked by the official SoftCoT repository.
- File used: asdiv-aug-test.jsonl.
- Licence reported by the source card: CC BY-NC-ND 4.0.
- Download URL: https://huggingface.co/datasets/xuyige/ASDiv-Aug/resolve/main/asdiv-aug-test.jsonl
- Downloaded 2026-06-22 into the isolated runtime only.
- Record count: 1,038.
- Schema: question, answer.
- SHA-256: 8427da17b13ebe23d9da9433c8f04088ede2aa11e1cb1f305050f57cd2785001.

## StrategyQA

- Canonical source repository: eladsegal/strategyqa, described by its GitHub metadata as the official TACL 2021 code for "Did Aristotle Use a Laptop?" and licensed MIT.
- File used: data/strategyqa/dev.json from the canonical repository.
- Download URL: https://raw.githubusercontent.com/eladsegal/strategyqa/main/data/strategyqa/dev.json
- Downloaded 2026-06-22 into the isolated runtime only.
- Record count: 229.
- Schema: answer, decomposition, description, evidence, facts, qid, question, term.
- SHA-256: 0d94842ffb022db8fd5ecd2168b785d5cf67f6faf64f665476bad544a3eb9dde.

## Pre-registered evaluation selection

The planned fixed sample is 200 examples from each of GSM8K source test, ASDiv-Aug test, and StrategyQA dev. The selection will be made by a deterministic hash of each record's input identity (question, or question plus qid), never its answer/label. The selection script and manifest must be written and executed before any model result is observed.
