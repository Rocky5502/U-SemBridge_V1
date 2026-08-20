import pandas as pd

from usembridge.results import (
    aggregate_summary,
    mcnemar_exact,
    paired_bootstrap_delta,
    selective_policy_table,
    uncertainty_component_auroc,
)


def _df():
    rows = []
    for method, vals in {
        "A": [(1, 0.1, 0), (1, 0.2, 0), (0, 0.8, 1), (0, 0.9, 1)],
        "B": [(1, 0.2, 0), (0, 0.7, 1), (0, 0.8, 1), (0, 0.9, 1)],
    }.items():
        for i, (le, risk, err) in enumerate(vals):
            rows.append(
                {
                    "run_id": "r1",
                    "dataset": "toy",
                    "model": "toy",
                    "method": method,
                    "example_id": str(i),
                    "gold_label": "T",
                    "pred_label": "T" if le else "F",
                    "logical_equivalent": le,
                    "semantic_error": err,
                    "risk_score": risk,
                    "solver_executable": 1,
                    "error_class": "predicate_grounding" if err else "",
                    "u_grounding": risk,
                    "u_structural": risk,
                    "u_completeness": risk,
                    "u_solver_sensitivity": risk,
                    "seed": 42,
                }
            )
    return pd.DataFrame(rows)


def test_summary_and_selective():
    df = _df()
    summary = aggregate_summary(df)
    assert set(summary["method"]) == {"A", "B"}
    assert summary.loc[summary["method"] == "A", "le"].iloc[0] == 0.5
    selective = selective_policy_table(df, coverages=(0.5,))
    assert len(selective) == 2
    assert selective["realized_coverage"].eq(0.5).all()


def test_component_auroc():
    out = uncertainty_component_auroc(_df())
    assert not out.empty
    assert out["auroc"].dropna().between(0, 1).all()


def test_paired_statistics():
    df = _df()
    boot = paired_bootstrap_delta(
        df, method_a="A", method_b="B", n_boot=100, seed=1
    )
    assert boot.n_pairs == 4
    test = mcnemar_exact(df, method_a="A", method_b="B")
    assert test["n_pairs"] == 4
    assert 0 <= test["p_value"] <= 1
