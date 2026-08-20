# V3 Results Protocol

This document is the code-side contract for the IJUFKS V3 results section. It prevents the manuscript, analysis scripts, and raw runs from drifting apart.

## Source of truth

`results/per_example.csv` is the primary empirical artifact. One row must correspond to one evaluated example under one dataset/model/method/run. All aggregate tables and plots are generated from that file or from explicitly documented efficiency/ablation files.

The core fields are:
- gold and predicted decision label;
- logical-equivalence indicator;
- semantic-error indicator and error class;
- calibrated translation-risk score;
- U-SemBridge action (`VERIFY`, `COMPARE_REPAIR`, `CLARIFY`, or `ABSTAIN`);
- solver executability;
- the four uncertainty components (`u_grounding`, `u_structural`, `u_completeness`, `u_solver_sensitivity`);
- latency, tokens, solver calls, seed, run ID, dataset, model, and method.

## Semantic-error definition

A semantic error is a translation that changes decision-relevant meaning relative to the benchmark gold formalization or a qualified expert reference. Parser failure alone is not a semantic error, and solver success does not imply semantic correctness.

Error classes are frozen before the main analysis:
1. predicate grounding;
2. argument/type binding;
3. quantifier/scope;
4. negation/exception;
5. temporal/numeric;
6. coreference/entity;
7. omission/hallucination;
8. unknown-to-false collapse.

## Translation risk

`risk_score` is interpreted as the estimated probability/risk of a semantic translation failure. Lower-risk cases are accepted first for selective prediction. Calibration is measured against the binary semantic-error target using ECE/Brier; ranking quality is measured using semantic-error AUROC and AURC.

## Fixed selective-policy evaluation

The primary matched-coverage operating points are frozen at:
- 80% coverage;
- 90% coverage;
- 95% coverage.

Report semantic-error rate, downstream answer accuracy, and high-confidence-wrong accepted cases at each operating point. Thresholds must not be selected on the test set.

## RQ-to-artifact mapping

- **RQ1 — semantic fidelity:** primary benchmark table, logical equivalence, downstream accuracy, semantic-error taxonomy, paired confidence intervals.
- **RQ2 — uncertainty calibration:** ECE, Brier, error-detection AUROC, AURC, reliability diagram, cross-model/dataset transfer.
- **RQ3 — failure localization:** error taxonomy and uncertainty-component diagnostics.
- **RQ4 — reliability/intervention cost:** selective-policy table, ablations, latency/tokens/solver calls, and reliability-cost frontier.

## Statistical plan

For paired method comparisons on the same examples:
- paired bootstrap confidence intervals for metric deltas;
- exact McNemar test for primary paired binary outcomes when appropriate;
- report effect size together with uncertainty, not only p-values;
- correct for multiple primary comparisons if several hypotheses are tested simultaneously.

Seeds, prompts, model revisions, solver versions, and source dataset commits must be fixed in run manifests.

## Reproduction commands

After real runs produce `results/per_example.csv`:

```bash
python scripts/build_result_artifacts.py --input results/per_example.csv
pip install -e ".[plot]"
python scripts/plot_results.py
```

Generated figures are written to `artifacts/figures/` and should be copied into the final manuscript only after the corresponding result CSV and run manifest are frozen.

## Integrity rule

No script in this repository should manufacture placeholder performance numbers. Missing empirical inputs must cause analysis/plot generation to stop rather than silently creating synthetic results. Manuscript `TBD` cells are replaced only from frozen, machine-readable outputs.
