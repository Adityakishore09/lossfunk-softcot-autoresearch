"""Item-level agreement/error analysis for frozen SoftCoT transfer results."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def condition_from_path(path: Path) -> str:
    stem = path.stem
    if stem.endswith("_learned"):
        return "learned_softcot"
    if stem.endswith("_zero"):
        return "zero_control"
    if stem.endswith("_baseline"):
        return "no_softcot_baseline"
    return stem.rsplit("_", 1)[-1]


def load_results(raw_root: Path) -> dict[tuple[str, str, str], dict[str, Any]]:
    loaded: dict[tuple[str, str, str], dict[str, Any]] = {}
    for result_file in sorted(raw_root.glob("seed_*/*.json")):
        seed = result_file.parent.name.removeprefix("seed_")
        with result_file.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        key = (seed, payload["task_name"], condition_from_path(result_file))
        loaded[key] = payload
    return loaded


def row_id(row: dict[str, Any]) -> str:
    index = row.get("index_in_fixed_split")
    if index is not None:
        return f"index:{index}"
    qid = row.get("qid")
    if qid not in {None, ""}:
        return f"qid:{qid}"
    return f"sha256:{row['question_sha256']}"


def paired_counts(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    a_rows = {row_id(row): row for row in a["results"]}
    b_rows = {row_id(row): row for row in b["results"]}
    common_ids = sorted(set(a_rows) & set(b_rows))
    only_a_correct = []
    only_b_correct = []
    both_correct = []
    both_wrong = []
    for item_id in common_ids:
        ar = a_rows[item_id]
        br = b_rows[item_id]
        ac = bool(ar["correct"])
        bc = bool(br["correct"])
        record = {
            "item_id": item_id,
            "question_sha256": ar.get("question_sha256"),
            "reference_answer": ar.get("reference_answer"),
            "a_prediction": ar.get("prediction"),
            "b_prediction": br.get("prediction"),
        }
        if ac and bc:
            both_correct.append(record)
        elif ac and not bc:
            only_a_correct.append(record)
        elif (not ac) and bc:
            only_b_correct.append(record)
        else:
            both_wrong.append(record)
    total = len(common_ids)
    return {
        "paired_n": total,
        "both_correct": len(both_correct),
        "both_wrong": len(both_wrong),
        "a_only_correct": len(only_a_correct),
        "b_only_correct": len(only_b_correct),
        "a_accuracy_on_common": (
            (len(both_correct) + len(only_a_correct)) / total if total else None
        ),
        "b_accuracy_on_common": (
            (len(both_correct) + len(only_b_correct)) / total if total else None
        ),
        "a_minus_b_accuracy": (
            (len(only_a_correct) - len(only_b_correct)) / total if total else None
        ),
        "a_only_examples": only_a_correct[:20],
        "b_only_examples": only_b_correct[:20],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    results = load_results(args.raw_root)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    pair_specs = [
        ("learned_softcot", "no_softcot_baseline"),
        ("learned_softcot", "zero_control"),
        ("zero_control", "no_softcot_baseline"),
    ]

    summary_rows = []
    detail: dict[str, Any] = {}
    seeds = sorted({seed for seed, _, _ in results}, key=int)
    tasks = sorted({task for _, task, _ in results})
    task_order = {"gsm8k": 0, "asdiv-aug": 1, "strategyqa": 2}
    tasks.sort(key=lambda task: task_order.get(task, 99))

    for seed in seeds:
        for task in tasks:
            for a_cond, b_cond in pair_specs:
                a = results.get((seed, task, a_cond))
                b = results.get((seed, task, b_cond))
                if not a or not b:
                    continue
                counts = paired_counts(a, b)
                comparison_key = f"{seed}/{task}/{a_cond}_vs_{b_cond}"
                detail[comparison_key] = counts
                summary_rows.append(
                    {
                        "seed": seed,
                        "task": task,
                        "comparison": f"{a_cond}_vs_{b_cond}",
                        "paired_n": counts["paired_n"],
                        "both_correct": counts["both_correct"],
                        "both_wrong": counts["both_wrong"],
                        "first_only_correct": counts["a_only_correct"],
                        "second_only_correct": counts["b_only_correct"],
                        "first_accuracy_on_common": counts["a_accuracy_on_common"],
                        "second_accuracy_on_common": counts["b_accuracy_on_common"],
                        "first_minus_second_accuracy": counts["a_minus_b_accuracy"],
                    }
                )

    with (args.out_dir / "item_agreement_summary.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "seed",
                "task",
                "comparison",
                "paired_n",
                "both_correct",
                "both_wrong",
                "first_only_correct",
                "second_only_correct",
                "first_accuracy_on_common",
                "second_accuracy_on_common",
                "first_minus_second_accuracy",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    with (args.out_dir / "item_agreement_detail.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(detail, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    aggregate = defaultdict(lambda: defaultdict(int))
    for row in summary_rows:
        key = (row["task"], row["comparison"])
        aggregate[key]["paired_n"] += int(row["paired_n"])
        aggregate[key]["first_only_correct"] += int(row["first_only_correct"])
        aggregate[key]["second_only_correct"] += int(row["second_only_correct"])
        aggregate[key]["both_correct"] += int(row["both_correct"])
        aggregate[key]["both_wrong"] += int(row["both_wrong"])

    with (args.out_dir / "item_agreement_summary.md").open(
        "w", encoding="utf-8"
    ) as handle:
        handle.write("# Item-level agreement/error analysis\n\n")
        handle.write(
            "Counts are paired by fixed-split index when present, otherwise by qid or question SHA-256. "
            "Positive Δ means the first condition has more correct items than the second condition on the same examples.\n\n"
        )
        handle.write("| Task | Comparison | Paired N | First-only correct | Second-only correct | Δ accuracy |\n")
        handle.write("|---|---|---:|---:|---:|---:|\n")
        for (task, comparison), counts in sorted(
            aggregate.items(), key=lambda item: (task_order.get(item[0][0], 99), item[0][1])
        ):
            paired_n = counts["paired_n"]
            delta = (
                (counts["first_only_correct"] - counts["second_only_correct"]) / paired_n
                if paired_n
                else 0.0
            )
            handle.write(
                f"| {task} | {comparison} | {paired_n} | "
                f"{counts['first_only_correct']} | {counts['second_only_correct']} | {delta:+.4f} |\n"
            )


if __name__ == "__main__":
    main()
