from __future__ import annotations

import argparse
from pathlib import Path

from _git_helpers import clone_or_update, write_manifest

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "external"
MANIFESTS = ROOT / "data" / "manifests"

BASELINES = {
    "linc": "https://github.com/benlipkin/linc.git",
    "logiclm": "https://github.com/teacherpeterpan/Logic-LLM.git",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--baseline", choices=sorted(BASELINES))
    args = parser.parse_args()
    if not args.all and not args.baseline:
        parser.error("choose --all or --baseline NAME")
    names = BASELINES if args.all else [args.baseline]
    for name in names:
        sha = clone_or_update(BASELINES[name], EXT / name)
        write_manifest(
            MANIFESTS / f"baseline_{name}.json",
            {"name": name, "url": BASELINES[name], "commit": sha},
        )
        print(f"{name}: {sha}")


if __name__ == "__main__":
    main()
