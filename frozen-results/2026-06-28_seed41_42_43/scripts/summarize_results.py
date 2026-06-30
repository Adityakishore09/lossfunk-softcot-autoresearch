"""Aggregate non-overwriting raw transfer results into a reviewable summary."""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from statistics import fmean, stdev
from typing import Any


def load_payloads(results_root: Path) -> list[tuple[str, Path, dict[str, Any]]]:
    payloads = []
    for result_file in sorted(results_root.glob("seed_*/*.json")):
        with result_file.open(encoding="utf-8") as handle:
            payload = json.load(handle)
        seed = result_file.parent.name.removeprefix("seed_")
        payloads.append((seed, result_file, payload))
    if not payloads:
        raise FileNotFoundError(f"No raw result JSON files found under {results_root}")
    return payloads


def metric_summary(values: list[float]) -> dict[str, float | int | None]:
    return {
        "count": len(values),
        "mean": fmean(values),
        "sample_std": stdev(values) if len(values) > 1 else None,
        "minimum": min(values),
        "maximum": max(values),
    }


def bootstrap_seed_mean(values: list[float], draws: int, seed: int) -> dict[str, float]:
    rng = random.Random(seed)
    means = [
        fmean([values[rng.randrange(len(values))] for _ in values])
        for _ in range(draws)
    ]
    means.sort()
    return {
        "bootstrap_draws": draws,
        "bootstrap_seed": seed,
        "bootstrap_mean_ci95_low": means[math.floor(0.025 * (draws - 1))],
        "bootstrap_mean_ci95_high": means[math.floor(0.975 * (draws - 1))],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--bootstrap-draws", type=int, default=10_000)
    parser.add_argument("--bootstrap-seed", type=int, default=20260622)
    args = parser.parse_args()

    root = args.runtime_root.resolve()
    raw_root = root / "results" / "raw"
    output_dir = root / "results" / "analysis"
    output_file = output_dir / "summary.json"
    if output_file.exists():
        raise FileExistsError(f"Refusing to overwrite {output_file}")

    grouped: dict[tuple[str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    source_files = []
    for seed, path, payload in load_payloads(raw_root):
        key = (payload["task_name"], "baseline" if payload["num_thought_tokens"] == 0 else payload["soft_thought_control"])
        if key[1] not in {"baseline", "learned", "zero"}:
            raise ValueError(f"Unknown condition in {path}: {key[1]}")
        if seed in grouped[key]:
            raise ValueError(f"Duplicate task/condition/seed result: {key}, {seed}")
        grouped[key][seed] = payload
        source_files.append(str(path.relative_to(root)))

    condition_summary: dict[str, Any] = {}
    for (task, condition), per_seed in sorted(grouped.items()):
        accuracies = [payload["accuracy"] for _, payload in sorted(per_seed.items())]
        mean_latencies = [
            fmean(row["generation_elapsed_seconds"] for row in payload["results"])
            for _, payload in sorted(per_seed.items())
        ]
        condition_summary[f"{task}/{condition}"] = {
            "accuracy": metric_summary(accuracies),
            "mean_generation_latency_seconds": metric_summary(mean_latencies),
            "seeds": sorted(per_seed),
            "sample_sizes": {
                seed: payload["sample_size"] for seed, payload in sorted(per_seed.items())
            },
        }

    transfer_contrasts = {}
    available_seeds = sorted(
        set(grouped[("asdiv-aug", "learned")])
        & set(grouped[("asdiv-aug", "baseline")])
        & set(grouped[("strategyqa", "learned")])
        & set(grouped[("strategyqa", "baseline")])
    )
    if available_seeds:
        related_minus_unrelated = []
        per_seed = {}
        for seed in available_seeds:
            related = (
                grouped[("asdiv-aug", "learned")][seed]["accuracy"]
                - grouped[("asdiv-aug", "baseline")][seed]["accuracy"]
            )
            unrelated = (
                grouped[("strategyqa", "learned")][seed]["accuracy"]
                - grouped[("strategyqa", "baseline")][seed]["accuracy"]
            )
            difference = related - unrelated
            related_minus_unrelated.append(difference)
            per_seed[seed] = {
                "related_delta_accuracy": related,
                "unrelated_delta_accuracy": unrelated,
                "difference_of_differences": difference,
            }
        transfer_contrasts["learned_vs_baseline"] = {
            "per_seed": per_seed,
            "difference_of_differences": {
                **metric_summary(related_minus_unrelated),
                **bootstrap_seed_mean(
                    related_minus_unrelated, args.bootstrap_draws, args.bootstrap_seed
                ),
            },
        }

    output_dir.mkdir(parents=True, exist_ok=False)
    output = {
        "source_files": source_files,
        "condition_summary": condition_summary,
        "transfer_contrasts": transfer_contrasts,
        "interpretation_guardrail": (
            "The difference-of-differences is a preliminary implementation-specific "
            "pattern, not proof that soft thoughts are general reasoning states."
        ),
    }
    with output_file.open("x", encoding="utf-8") as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


if __name__ == "__main__":
    main()
