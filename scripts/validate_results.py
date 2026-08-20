from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from usembridge.results import REQUIRED_PER_EXAMPLE


PLACEHOLDERS = {"", "TBD", "NA_PLACEHOLDER", "RUN", "DATASET", "MODEL", "METHOD", "ID"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate real U-SemBridge per-example outputs")
    parser.add_argument("--input", default="results/per_example.csv")
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        raise SystemExit(f"Missing result file: {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise SystemExit("Result file is empty")

    missing = sorted(REQUIRED_PER_EXAMPLE - set(df.columns))
    if missing:
        raise SystemExit(f"Missing required columns: {missing}")

    key_cols = ["dataset", "model", "method", "example_id"]
    for col in key_cols:
        if df[col].isna().any():
            raise SystemExit(f"Null values found in key column: {col}")
        bad = df[col].astype(str).str.strip().isin(PLACEHOLDERS)
        if bad.any():
            raise SystemExit(f"Placeholder value found in key column {col}: row {bad.idxmax()}")

    duplicate_keys = [c for c in ("run_id", "dataset", "model", "method", "example_id", "seed") if c in df]
    if df.duplicated(duplicate_keys).any():
        raise SystemExit(f"Duplicate per-example keys found: {duplicate_keys}")

    risk = pd.to_numeric(df["risk_score"], errors="coerce")
    if risk.isna().any() or ((risk < 0) | (risk > 1)).any():
        raise SystemExit("risk_score must be numeric and lie in [0, 1]")

    for col in ("logical_equivalent", "semantic_error"):
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any() or not set(values.astype(int).unique()).issubset({0, 1}):
            raise SystemExit(f"{col} must contain only binary 0/1 values")

    for col in ("u_grounding", "u_structural", "u_completeness", "u_solver_sensitivity"):
        if col not in df:
            continue
        values = pd.to_numeric(df[col], errors="coerce")
        finite = values[np.isfinite(values)]
        if ((finite < 0) | (finite > 1)).any():
            raise SystemExit(f"{col} must lie in [0, 1] when present")

    print(f"Validated {len(df)} real per-example rows from {path.resolve()}")


if __name__ == "__main__":
    main()
