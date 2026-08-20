# Results artifact contract

This folder is intentionally free of empirical claims before experiments.

## Required machine-readable inputs

- `per_example.csv`: one row per evaluated example with semantic-error labels, uncertainty components, estimated translation risk, policy action, solver status, and resource measurements.
- `summary_metrics.csv`: generated one row per dataset/model/method/run aggregate.
- `selective_policy.csv`: generated semantic risk and answer accuracy at fixed coverage.
- `semantic_errors.csv`: generated normalized counts by semantic error category.
- `component_diagnostics.csv`: generated AUROC for each uncertainty component.
- `ablation_metrics.csv`: one row per ablation configuration.
- `efficiency.csv`: LLM calls, solver calls, latency, tokens, memory, and optional qualified-expert time.
- `calibration_transfer.csv`: source/target model and dataset transfer calibration.

Templates are versioned here. Real result CSVs are ignored by Git and should be archived as release artifacts with their run manifests.

## Build derived artifacts

```bash
python scripts/validate_results.py --input results/per_example.csv
python scripts/build_result_artifacts.py --input results/per_example.csv
pip install -e ".[plot]"
python scripts/plot_results.py
python scripts/export_latex_tables.py
```

The validator rejects placeholders, duplicate per-example keys, malformed binary labels, and out-of-range uncertainty/risk values. Analysis scripts stop when empirical inputs are missing instead of creating synthetic numbers.

## Planned manuscript surfaces

1. Primary benchmark table: logical equivalence, downstream answer accuracy, solver-executable rate, ECE, AURC, and semantic-error AUROC.
2. Selective-policy table at 80%, 90%, and 95% coverage.
3. Semantic-error taxonomy table.
4. Ablation table.
5. Efficiency/intervention table.
6. Cross-model and cross-dataset calibration-transfer table.
7. Risk-coverage curve and translation-risk reliability diagram.
8. Uncertainty-component diagnostic figure.
9. Semantic-error heatmap/bar chart when sufficiently populated.
10. Reliability-cost frontier.

Generated plots go to `artifacts/figures/`; generated LaTeX fragments go to `artifacts/tables/`.

## Integrity rule

Every final table or figure must be reproducible from a frozen result CSV plus the matching run manifest and Git commit. Do not type result values manually into the manuscript.
