from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np
import pandas as pd
from scipy.stats import binomtest
from sklearn.metrics import roc_auc_score

from .metrics import aurc, expected_calibration_error


REQUIRED_PER_EXAMPLE = {
    "dataset",
    "model",
    "method",
    "example_id",
    "gold_label",
    "pred_label",
    "logical_equivalent",
    "semantic_error",
    "risk_score",
}

ERROR_CLASSES = (
    "predicate_grounding",
    "argument_type_binding",
    "quantifier_scope",
    "negation_exception",
    "temporal_numeric",
    "coreference_entity",
    "omission_hallucination",
    "unknown_to_false",
)

UQ_COLUMNS = (
    "u_grounding",
    "u_structural",
    "u_completeness",
    "u_solver_sensitivity",
)


@dataclass(frozen=True)
class BootstrapResult:
    delta: float
    ci_low: float
    ci_high: float
    n_pairs: int


def _require_columns(df: pd.DataFrame, required: Iterable[str]) -> None:
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")


def _as_binary(series: pd.Series) -> np.ndarray:
    if series.dtype == bool:
        return series.astype(int).to_numpy()
    values = pd.to_numeric(series, errors="raise").to_numpy(dtype=float)
    if not set(np.unique(values)).issubset({0.0, 1.0}):
        raise ValueError("binary outcome column must contain only 0/1 values")
    return values.astype(int)


def aggregate_summary(per_example: pd.DataFrame) -> pd.DataFrame:
    """Build one aggregate row per dataset/model/method/run from real outputs."""
    _require_columns(per_example, REQUIRED_PER_EXAMPLE)
    group_cols = [
        c
        for c in ("run_id", "dataset", "model", "method", "seed")
        if c in per_example
    ]
    rows: list[dict[str, object]] = []

    for keys, g in per_example.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        row = dict(zip(group_cols, keys))
        semantic_error = _as_binary(g["semantic_error"])
        risk = g["risk_score"].astype(float).clip(0, 1).to_numpy()
        logical_equivalent = _as_binary(g["logical_equivalent"])
        answer_correct = (
            g["pred_label"].astype(str) == g["gold_label"].astype(str)
        ).astype(int).to_numpy()

        row.update(
            n_examples=int(len(g)),
            le=float(logical_equivalent.mean()),
            answer_accuracy=float(answer_correct.mean()),
            semantic_error_rate=float(semantic_error.mean()),
            ece=float(
                expected_calibration_error(risk.tolist(), semantic_error.tolist())
            ),
            aurc=float(aurc(risk.tolist(), semantic_error.tolist())),
        )

        if "solver_executable" in g.columns:
            row["executable_rate"] = float(_as_binary(g["solver_executable"]).mean())
        else:
            row["executable_rate"] = np.nan

        if len(set(semantic_error.tolist())) > 1:
            row["error_auroc"] = float(roc_auc_score(semantic_error, risk))
        else:
            row["error_auroc"] = np.nan

        rows.append(row)

    return pd.DataFrame(rows)


def selective_policy_table(
    per_example: pd.DataFrame,
    coverages: Sequence[float] = (0.80, 0.90, 0.95),
    *,
    high_confidence_risk_threshold: float = 0.20,
) -> pd.DataFrame:
    """Compute matched-coverage metrics by accepting lowest-risk examples first."""
    _require_columns(per_example, REQUIRED_PER_EXAMPLE)
    if not 0 <= high_confidence_risk_threshold <= 1:
        raise ValueError("high_confidence_risk_threshold must lie in [0, 1]")
    group_cols = [
        c
        for c in ("run_id", "dataset", "model", "method", "seed")
        if c in per_example
    ]
    rows: list[dict[str, object]] = []

    for keys, g in per_example.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        base = dict(zip(group_cols, keys))
        g = g.sort_values("risk_score", kind="mergesort").reset_index(drop=True)
        n = len(g)
        for coverage in coverages:
            if not 0 < coverage <= 1:
                raise ValueError("coverage values must lie in (0, 1]")
            k = max(1, min(n, int(np.ceil(coverage * n))))
            accepted = g.iloc[:k]
            semantic_error = _as_binary(accepted["semantic_error"])
            answer_correct = (
                accepted["pred_label"].astype(str) == accepted["gold_label"].astype(str)
            ).astype(int).to_numpy()
            wrong = accepted[accepted["semantic_error"].astype(float) >= 0.5]
            high_conf_wrong = int(
                (
                    wrong["risk_score"].astype(float)
                    <= high_confidence_risk_threshold
                ).sum()
            )
            row = dict(base)
            row.update(
                target_coverage=float(coverage),
                realized_coverage=float(k / n),
                accepted_n=int(k),
                semantic_error_rate=float(semantic_error.mean()),
                answer_accuracy=float(answer_correct.mean()),
                high_confidence_wrong=high_conf_wrong,
                high_confidence_risk_threshold=float(
                    high_confidence_risk_threshold
                ),
            )
            rows.append(row)

    return pd.DataFrame(rows)


def semantic_error_breakdown(per_example: pd.DataFrame) -> pd.DataFrame:
    _require_columns(per_example, REQUIRED_PER_EXAMPLE | {"error_class"})
    group_cols = [
        c
        for c in ("run_id", "dataset", "model", "method", "seed")
        if c in per_example
    ]
    rows: list[dict[str, object]] = []

    for keys, g in per_example.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        base = dict(zip(group_cols, keys))
        error_mask = g["semantic_error"].astype(float) >= 0.5
        denom = max(1, int(error_mask.sum()))
        counts = (
            g.loc[error_mask, "error_class"]
            .fillna("unclassified")
            .replace("", "unclassified")
            .value_counts()
        )
        for error_class, count in counts.items():
            row = dict(base)
            row.update(
                error_class=str(error_class),
                count=int(count),
                rate=float(count / denom),
            )
            rows.append(row)

    return pd.DataFrame(rows)


def uncertainty_component_auroc(per_example: pd.DataFrame) -> pd.DataFrame:
    _require_columns(per_example, REQUIRED_PER_EXAMPLE)
    available = [c for c in UQ_COLUMNS if c in per_example.columns]
    if not available:
        return pd.DataFrame(
            columns=["dataset", "model", "method", "component", "auroc"]
        )

    group_cols = [
        c
        for c in ("run_id", "dataset", "model", "method", "seed")
        if c in per_example
    ]
    rows: list[dict[str, object]] = []
    for keys, g in per_example.groupby(group_cols, dropna=False):
        if not isinstance(keys, tuple):
            keys = (keys,)
        base = dict(zip(group_cols, keys))
        y = _as_binary(g["semantic_error"])
        for component in available:
            x = g[component].astype(float).to_numpy()
            valid = np.isfinite(x)
            if valid.sum() < 2 or len(np.unique(y[valid])) < 2:
                score = np.nan
            else:
                score = float(roc_auc_score(y[valid], x[valid]))
            row = dict(base)
            row.update(component=component, auroc=score)
            rows.append(row)
    return pd.DataFrame(rows)


def _paired_frames(
    per_example: pd.DataFrame,
    *,
    method_a: str,
    method_b: str,
    metric: str,
) -> pd.DataFrame:
    """Return one-to-one paired rows; caller must prefilter to one evaluation slice."""
    _require_columns(per_example, {"example_id", "method", metric})
    a = per_example.loc[
        per_example["method"] == method_a, ["example_id", metric]
    ].rename(columns={metric: "a"})
    b = per_example.loc[
        per_example["method"] == method_b, ["example_id", metric]
    ].rename(columns={metric: "b"})
    if a["example_id"].duplicated().any() or b["example_id"].duplicated().any():
        raise ValueError(
            "paired analysis requires one row per example and method; filter to a "
            "single dataset/model/run/seed before comparing methods"
        )
    pairs = a.merge(b, on="example_id", how="inner", validate="one_to_one").dropna()
    if pairs.empty:
        raise ValueError("no paired examples found")
    return pairs


def paired_bootstrap_delta(
    per_example: pd.DataFrame,
    *,
    method_a: str,
    method_b: str,
    metric: str = "logical_equivalent",
    n_boot: int = 2000,
    seed: int = 42,
) -> BootstrapResult:
    """Paired bootstrap confidence interval for method A minus method B."""
    if n_boot <= 0:
        raise ValueError("n_boot must be positive")
    pairs = _paired_frames(
        per_example,
        method_a=method_a,
        method_b=method_b,
        metric=metric,
    )

    a_values = pairs["a"].astype(float).to_numpy()
    b_values = pairs["b"].astype(float).to_numpy()
    observed = float(np.mean(a_values - b_values))
    rng = np.random.default_rng(seed)
    n = len(pairs)
    draws = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        draws[i] = float(np.mean(a_values[idx] - b_values[idx]))
    low, high = np.quantile(draws, [0.025, 0.975])
    return BootstrapResult(observed, float(low), float(high), n)


def mcnemar_exact(
    per_example: pd.DataFrame,
    *,
    method_a: str,
    method_b: str,
    metric: str = "logical_equivalent",
) -> dict[str, float | int]:
    """Exact two-sided McNemar test for paired binary outcomes."""
    pairs = _paired_frames(
        per_example,
        method_a=method_a,
        method_b=method_b,
        metric=metric,
    )
    av = _as_binary(pairs["a"])
    bv = _as_binary(pairs["b"])
    b_only = int(np.sum((av == 0) & (bv == 1)))
    a_only = int(np.sum((av == 1) & (bv == 0)))
    discordant = a_only + b_only
    p_value = (
        1.0
        if discordant == 0
        else float(binomtest(min(a_only, b_only), discordant, 0.5).pvalue)
    )
    return {
        "a_only_correct": a_only,
        "b_only_correct": b_only,
        "discordant": discordant,
        "p_value": p_value,
        "n_pairs": int(len(pairs)),
    }
