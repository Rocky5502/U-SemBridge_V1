from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run(*args: str, cwd: Path | None = None) -> str:
    proc = subprocess.run(args, cwd=cwd, text=True, check=True, capture_output=True)
    return proc.stdout.strip()


def clone_or_update(url: str, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and (destination / ".git").exists():
        run("git", "fetch", "--all", "--tags", cwd=destination)
        run("git", "pull", "--ff-only", cwd=destination)
    else:
        run("git", "clone", "--depth", "1", url, str(destination))
    return run("git", "rev-parse", "HEAD", cwd=destination)


def write_manifest(path: Path, payload: dict) -> None:
    payload = dict(payload)
    payload["fetched_at_utc"] = datetime.now(timezone.utc).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
