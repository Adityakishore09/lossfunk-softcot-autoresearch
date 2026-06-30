"""Download the pinned public Qwen pair into an isolated SoftCoT runtime."""

from pathlib import Path

from huggingface_hub import snapshot_download


ROOT = Path(__file__).resolve().parents[1]
MODELS = {
    "Qwen2.5-7B-Instruct": (
        "Qwen/Qwen2.5-7B-Instruct",
        "a09a35458c702b33eeacc393d103063234e8bc28",
    ),
    "Qwen2.5-1.5B-Instruct": (
        "Qwen/Qwen2.5-1.5B-Instruct",
        "989aa7980e4cf806f80c7fef2b1adb7bc71aa306",
    ),
}


def main() -> None:
    model_root = ROOT / "models"
    for directory, (repo_id, revision) in MODELS.items():
        destination = model_root / directory
        if destination.exists():
            raise FileExistsError(f"Refusing to overwrite {destination}")
        print("Downloading {} at {} into {}".format(repo_id, revision, destination))
        snapshot_download(repo_id=repo_id, revision=revision, local_dir=destination)


if __name__ == "__main__":
    main()
