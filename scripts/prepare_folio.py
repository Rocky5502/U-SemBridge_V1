from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    source = root / "data" / "raw" / "FOLIO" / "data" / "v0.0"
    out = root / "data" / "processed" / "folio"
    out.mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=["train", "validation", "all"], default="all")
    args = parser.parse_args()
    splits = ["train", "validation"] if args.split == "all" else [args.split]
    manifest = {}
    for split in splits:
        inp = source / f"folio-{split}.jsonl"
        if not inp.exists():
            raise FileNotFoundError(
                f"Missing {inp}. Run: python scripts/download_datasets.py --source folio"
            )
        target = out / f"{split}.jsonl"
        target.write_bytes(inp.read_bytes())
        manifest[split] = {
            "source": str(inp.relative_to(root)),
            "output": str(target.relative_to(root)),
            "sha256": sha256(target),
        }
    (out / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
