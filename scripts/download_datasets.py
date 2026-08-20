from __future__ import annotations

import argparse
from pathlib import Path

from _git_helpers import clone_or_update, write_manifest

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFESTS = ROOT / "data" / "manifests"

SOURCES = {
    "folio": {
        "url": "https://github.com/Yale-LILY/FOLIO.git",
        "dest": RAW / "FOLIO",
        "note": "Official FOLIO repository; expected data under data/v0.0.",
    },
    "logiclm_data": {
        "url": "https://github.com/teacherpeterpan/Logic-LLM.git",
        "dest": RAW / "Logic-LLM",
        "note": "Reference preprocessed FOLIO/ProofWriter data used by Logic-LM; preserve upstream license/citation.",
    },
}


def fetch(name: str) -> None:
    item = SOURCES[name]
    sha = clone_or_update(item["url"], item["dest"])
    write_manifest(
        MANIFESTS / f"{name}.json",
        {"name": name, "url": item["url"], "commit": sha, "note": item["note"]},
    )
    print(f"{name}: {sha}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--source", choices=sorted(SOURCES))
    args = parser.parse_args()
    if not args.all and not args.source:
        parser.error("choose --all or --source NAME")
    for name in (SOURCES if args.all else [args.source]):
        fetch(name)


if __name__ == "__main__":
    main()
