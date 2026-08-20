from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def default_schema_path() -> Path:
    return Path(__file__).resolve().parents[2] / "schemas" / "cir.schema.json"


def load_schema(path: str | Path | None = None) -> dict[str, Any]:
    schema_path = Path(path) if path else default_schema_path()
    with schema_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_cir(instance: dict[str, Any], schema_path: str | Path | None = None) -> None:
    validator = Draft202012Validator(load_schema(schema_path))
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        formatted = "\n".join(
            f"- {'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in errors
        )
        raise ValueError(f"Invalid CIR:\n{formatted}")


def load_and_validate(path: str | Path, schema_path: str | Path | None = None) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        instance = json.load(handle)
    validate_cir(instance, schema_path)
    return instance
