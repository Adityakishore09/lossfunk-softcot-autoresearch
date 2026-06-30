"""Create immutable, label-independent evaluation subsets for the transfer study."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SELECTION_VERSION = "lossfunk-transfer-split-v1"


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def read_json(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, list):
        raise ValueError(f"Expected a JSON list in {path}")
    return payload


def input_identity(record: dict[str, Any], index: int) -> dict[str, Any]:
    """Return an identity that deliberately excludes answer labels and rationales."""
    if "question" not in record:
        raise KeyError(f"Record {index} has no question field")
    identity: dict[str, Any] = {"question": record["question"], "source_index": index}
    if "qid" in record:
        identity["qid"] = record["qid"]
    return identity


def choose_records(
    records: list[dict[str, Any]],
    sample_size: int,
    selection_seed: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if len(records) < sample_size:
        raise ValueError(f"Need {sample_size} records but found {len(records)}")

    ranked: list[tuple[str, int, dict[str, Any], dict[str, Any]]] = []
    for index, record in enumerate(records):
        identity = input_identity(record, index)
        identity_json = canonical_json(identity)
        rank = sha256_text(f"{selection_seed}\0{identity_json}")
        ranked.append((rank, index, record, identity))

    selected = sorted(ranked, key=lambda row: (row[0], row[1]))[:sample_size]
    selected_records = [record for _, _, record, _ in selected]
    manifest_records = [
        {
            "source_index": index,
            "qid": record.get("qid"),
            "input_identity_sha256": sha256_text(canonical_json(identity)),
            "record_sha256": sha256_text(canonical_json(record)),
        }
        for _, index, record, identity in selected
    ]
    return selected_records, manifest_records


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(canonical_json(record))
            handle.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", type=Path, required=True)
    parser.add_argument("--sample-size", type=int, default=200)
    parser.add_argument(
        "--selection-seed",
        default="lossfunk-gsm8k-asdiv-strategyqa-transfer-2026-06-22",
    )
    args = parser.parse_args()

    root = args.runtime_root.resolve()
    output_dir = root / "data" / "fixed"
    if output_dir.exists():
        raise FileExistsError(
            f"Refusing to overwrite existing fixed split directory: {output_dir}"
        )
    output_dir.mkdir(parents=True)

    sources = {
        "gsm8k_source_test": (
            root / "data" / "gsm8k" / "test_socratic.jsonl",
            read_jsonl,
        ),
        "asdiv_aug_target_test": (
            root / "data" / "external" / "asdiv-aug-test.jsonl",
            read_jsonl,
        ),
        "strategyqa_target_dev": (
            root / "data" / "external" / "strategyqa-dev.json",
            read_json,
        ),
    }

    manifest: dict[str, Any] = {
        "selection_version": SELECTION_VERSION,
        "selection_seed": args.selection_seed,
        "sample_size": args.sample_size,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "selection_uses_labels": False,
        "datasets": {},
    }

    for name, (source_path, reader) in sources.items():
        if not source_path.is_file():
            raise FileNotFoundError(source_path)
        source_records = reader(source_path)
        selected_records, selected_manifest = choose_records(
            source_records, args.sample_size, args.selection_seed
        )
        output_path = output_dir / f"{name}.jsonl"
        write_jsonl(output_path, selected_records)
        manifest["datasets"][name] = {
            "source_path": str(source_path.relative_to(root)),
            "source_sha256": sha256_file(source_path),
            "source_record_count": len(source_records),
            "selected_path": str(output_path.relative_to(root)),
            "selected_sha256": sha256_file(output_path),
            "selected_record_count": len(selected_records),
            "selected_records": selected_manifest,
        }

    manifest_path = output_dir / "manifest.json"
    with manifest_path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


if __name__ == "__main__":
    main()
