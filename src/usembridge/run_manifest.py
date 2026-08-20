from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _git_commit(root: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            text=True,
            check=True,
            capture_output=True,
        )
        return out.stdout.strip()
    except Exception:
        return None


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_manifest(
    *,
    project_root: str | Path,
    run_id: str,
    dataset: dict[str, Any],
    model: dict[str, Any],
    prompt_text: str,
    decoding: dict[str, Any],
    solver: dict[str, Any],
    seed: int,
) -> dict[str, Any]:
    root = Path(project_root).resolve()
    return {
        "run_id": run_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(root),
        "dataset": dataset,
        "model": model,
        "prompt_sha256": sha256_text(prompt_text),
        "decoding": decoding,
        "solver": solver,
        "seed": int(seed),
    }


def write_manifest(path: str | Path, manifest: dict[str, Any]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
