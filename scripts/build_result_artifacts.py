from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from usembridge.results import (
    aggregate_summary,
    semantic_error_breakdown,
    selective_policy_table,
    uncertainty_component_auroc,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build U-SemBridge result artifacts from per-example outputs"
    )
    parser.add_argument("--input", default="results/per_example.csv")
    parser.add_argument("--outdir", default="results")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Missing real per-example file: {input_path}")
    df = pd.read_csv(input_path)
    if df.empty:
        raise SystemExit(f"Per-example file is empty: {input_path}")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    aggregate_summary(df).to_csv(outdir / "summary_metrics.csv", index=False)
    selective_policy_table(df).to_csv(outdir / "selective_policy.csv", index=False)
    semantic_error_breakdown(df).to_csv(outdir / "semantic_errors.csv", index=False)
    uncertainty_component_auroc(df).to_csv(
        outdir / "component_diagnostics.csv", index=False
    )

    print(f"Wrote result artifacts to {outdir.resolve()}")


if __name__ == "__main__":
    main()
