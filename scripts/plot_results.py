"""Generate manuscript-ready result plots from frozen U-SemBridge CSV outputs.

The script never synthesizes placeholder values. It exits when required real
result files are absent or empty.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "artifacts" / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)


def _require(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit(f"Missing real result file: {path}")
    df = pd.read_csv(path)
    if df.empty:
        raise SystemExit(f"Result file has no rows: {path}")
    return df


def _filter_slice(
    df: pd.DataFrame,
    *,
    dataset: str | None,
    model: str | None,
    run_id: str | None,
) -> pd.DataFrame:
    out = df.copy()
    for column, value in (("dataset", dataset), ("model", model), ("run_id", run_id)):
        if value is None:
            continue
        if column not in out.columns:
            raise SystemExit(f"Cannot filter on missing column: {column}")
        out = out[out[column].astype(str) == value]
    if out.empty:
        raise SystemExit("No result rows remain after plot filtering")

    identity = [c for c in ("dataset", "model", "run_id", "seed") if c in out.columns]
    if identity:
        combinations = out[identity].drop_duplicates()
        if len(combinations) > 1:
            raise SystemExit(
                "Plot input contains multiple evaluation slices. Pass --dataset, --model, "
                "and/or --run-id so manuscript curves do not mix unrelated runs."
            )
    return out


def risk_coverage(df: pd.DataFrame) -> None:
    required = {"method", "risk_score", "semantic_error"}
    if not required.issubset(df.columns):
        raise SystemExit(f"per_example.csv needs columns: {sorted(required)}")
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    for method, g in df.groupby("method"):
        g = g.dropna(subset=["risk_score", "semantic_error"]).sort_values("risk_score")
        if len(g) < 2:
            continue
        errors = g["semantic_error"].astype(float).to_numpy()
        coverage = np.arange(1, len(g) + 1) / len(g)
        risk = np.cumsum(errors) / np.arange(1, len(g) + 1)
        ax.plot(coverage, risk, label=str(method))
    ax.set_xlabel("Coverage")
    ax.set_ylabel("Semantic error risk")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "risk_coverage.pdf", bbox_inches="tight")
    plt.close(fig)


def reliability(df: pd.DataFrame, bins: int = 10) -> None:
    fig, ax = plt.subplots(figsize=(4.2, 3.4))
    for method, g in df.groupby("method"):
        g = g.dropna(subset=["risk_score", "semantic_error"])
        if len(g) < bins:
            continue
        cuts = pd.cut(
            g["risk_score"], bins=np.linspace(0, 1, bins + 1), include_lowest=True
        )
        grouped = g.groupby(cuts, observed=False)
        x = grouped["risk_score"].mean()
        y = grouped["semantic_error"].mean()
        ax.plot(x, y, marker="o", label=str(method))
    ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1)
    ax.set_xlabel("Predicted translation risk")
    ax.set_ylabel("Observed semantic-error frequency")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "risk_reliability.pdf", bbox_inches="tight")
    plt.close(fig)


def component_diagnostics(df: pd.DataFrame) -> None:
    columns = [
        "u_grounding",
        "u_structural",
        "u_completeness",
        "u_solver_sensitivity",
    ]
    available = [c for c in columns if c in df.columns]
    if not available:
        return
    fig, ax = plt.subplots(figsize=(5.4, 3.4))
    data = []
    labels = []
    for col in available:
        good = df.loc[
            df["semantic_error"].astype(float) < 0.5, col
        ].dropna().astype(float)
        bad = df.loc[
            df["semantic_error"].astype(float) >= 0.5, col
        ].dropna().astype(float)
        if len(good) == 0 or len(bad) == 0:
            continue
        data.extend([good.to_numpy(), bad.to_numpy()])
        short = col.removeprefix("u_").replace("_", " ")
        labels.extend([f"{short}\ncorrect", f"{short}\nerror"])
    if not data:
        plt.close(fig)
        return
    ax.boxplot(data, tick_labels=labels, showfliers=False)
    ax.set_ylabel("Uncertainty score")
    ax.tick_params(axis="x", labelrotation=25)
    fig.tight_layout()
    fig.savefig(FIGURES / "uncertainty_component_diagnostic.pdf", bbox_inches="tight")
    plt.close(fig)


def error_breakdown(df: pd.DataFrame) -> None:
    required = {"method", "error_class", "rate"}
    if not required.issubset(df.columns):
        raise SystemExit(f"semantic_errors.csv needs columns: {sorted(required)}")
    pivot = df.pivot_table(
        index="error_class", columns="method", values="rate", aggfunc="mean"
    )
    fig, ax = plt.subplots(figsize=(6.0, 3.6))
    im = ax.imshow(pivot.fillna(0).to_numpy(), aspect="auto")
    ax.set_xticks(
        range(len(pivot.columns)), labels=pivot.columns, rotation=30, ha="right"
    )
    ax.set_yticks(range(len(pivot.index)), labels=pivot.index)
    fig.colorbar(im, ax=ax, label="Error rate")
    fig.tight_layout()
    fig.savefig(FIGURES / "semantic_error_heatmap.pdf", bbox_inches="tight")
    plt.close(fig)


def cost_frontier(summary: pd.DataFrame, eff: pd.DataFrame) -> None:
    merge_keys = [
        c
        for c in ("run_id", "dataset", "model", "method", "seed")
        if c in summary.columns and c in eff.columns
    ]
    required_keys = {"dataset", "model", "method"}
    if not required_keys.issubset(merge_keys):
        raise SystemExit("Summary and efficiency tables need dataset/model/method keys")
    merged = summary.merge(eff, on=merge_keys, how="inner", validate="one_to_one")
    if "le" not in merged.columns or "latency_s" not in merged.columns:
        raise SystemExit("Need `le` and `latency_s` for cost frontier")
    fig, ax = plt.subplots(figsize=(5.0, 3.4))
    for _, row in merged.dropna(subset=["le", "latency_s"]).iterrows():
        ax.scatter(row["latency_s"], row["le"])
        ax.annotate(
            str(row["method"]), (row["latency_s"], row["le"]), fontsize=7
        )
    ax.set_xlabel("Latency per item (s)")
    ax.set_ylabel("Logical equivalence")
    fig.tight_layout()
    fig.savefig(FIGURES / "reliability_cost_frontier.pdf", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bins", type=int, default=10)
    parser.add_argument("--dataset")
    parser.add_argument("--model")
    parser.add_argument("--run-id")
    args = parser.parse_args()

    per = _filter_slice(
        _require(RESULTS / "per_example.csv"),
        dataset=args.dataset,
        model=args.model,
        run_id=args.run_id,
    )
    risk_coverage(per)
    reliability(per, bins=args.bins)
    component_diagnostics(per)

    if (RESULTS / "semantic_errors.csv").exists():
        semantic = _filter_slice(
            _require(RESULTS / "semantic_errors.csv"),
            dataset=args.dataset,
            model=args.model,
            run_id=args.run_id,
        )
        error_breakdown(semantic)

    if (
        (RESULTS / "summary_metrics.csv").exists()
        and (RESULTS / "efficiency.csv").exists()
    ):
        summary = _filter_slice(
            _require(RESULTS / "summary_metrics.csv"),
            dataset=args.dataset,
            model=args.model,
            run_id=args.run_id,
        )
        efficiency = _filter_slice(
            _require(RESULTS / "efficiency.csv"),
            dataset=args.dataset,
            model=args.model,
            run_id=args.run_id,
        )
        cost_frontier(summary, efficiency)
    print(f"Wrote manuscript figures to {FIGURES.resolve()}")


if __name__ == "__main__":
    main()
