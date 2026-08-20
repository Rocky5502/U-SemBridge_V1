from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = ROOT / "artifacts" / "tables"

TABLES = {
    "summary_metrics.csv": "primary_benchmark.tex",
    "selective_policy.csv": "selective_policy.tex",
    "semantic_errors.csv": "semantic_errors.tex",
    "ablation_metrics.csv": "ablations.tex",
    "efficiency.csv": "efficiency.tex",
    "calibration_transfer.csv": "calibration_transfer.tex",
    "component_diagnostics.csv": "component_diagnostics.tex",
}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    written = 0
    for csv_name, tex_name in TABLES.items():
        path = RESULTS / csv_name
        if not path.exists():
            continue
        df = pd.read_csv(path)
        if df.empty:
            continue
        tex = df.to_latex(
            index=False,
            escape=True,
            na_rep="--",
            float_format=lambda value: f"{value:.3f}",
        )
        (OUT / tex_name).write_text(tex, encoding="utf-8")
        written += 1
        print(f"wrote {OUT / tex_name}")

    if written == 0:
        raise SystemExit(
            "No non-empty frozen result CSVs were found. Run real experiments and "
            "build result artifacts before exporting manuscript tables."
        )


if __name__ == "__main__":
    main()
