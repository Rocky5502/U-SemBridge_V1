# U-SemBridge

**Uncertainty-Aware Neuro-Symbolic Translation for Explainable and Verifiable Decision Reasoning**

U-SemBridge studies a specific failure mode in neuro-symbolic reasoning: a formal solver can be sound while the natural-language-to-symbolic translation it receives is semantically wrong.

The project treats semantic translation as an uncertainty and assurance problem. It uses a Controlled Intermediate Representation (CIR), translation-risk signals, and a selective policy over **VERIFY**, **COMPARE/REPAIR**, **CLARIFY**, and **ABSTAIN**.

## Research target

Paper-in-progress for the IJUFKS special issue **Neuro-Symbolic Computing for Explainable, Ethical, and Interpretable Intelligent Systems**.

**Pre-experiment status:** the implementation scaffold, configs, data acquisition, tests, CI, reproducibility controls, and the V3 result-analysis pipeline are prepared. Numerical results remain intentionally TBD until real runs are completed.

## Core claim to test

**Translation-risk calibration should reduce high-confidence cases where a solver returns a formally valid result from a semantically incorrect formalization.**

This is not a claim that “LLM + solver” is novel. LINC and Logic-LM already establish that direction; U-SemBridge focuses on whether the semantic bridge itself is trustworthy.

## Quick start

### Windows PowerShell

```powershell
git clone https://github.com/Rocky5502/U-SemBridge_V1.git
cd U-SemBridge_V1
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
python -m usembridge doctor
pytest -q
python scripts\semantic_gap_demo.py
```

Optional local-LLM stack:

```powershell
pip install -e ".[llm]"
```

## Data and baselines

Raw third-party datasets are not vendored. This is intentional: it avoids silently redistributing external data and makes exact upstream provenance reproducible.

Fetch them locally:

```bash
python scripts/download_datasets.py --all
python scripts/fetch_baselines.py --all
```

Sources include the official FOLIO repository and the public LINC / Logic-LM repositories. Exact source commits are written to `data/manifests/`.

## Planned experiments

Primary: FOLIO, ProofWriter, ProofFOL where release terms permit, and a later expert-validated LegalBridge transfer set.

Initial open models:
- `mistralai/Mistral-7B-Instruct-v0.3`
- `Qwen/Qwen2.5-7B-Instruct`
- `meta-llama/Llama-3.1-8B-Instruct` if access/license permits

See `docs/EXPERIMENTS.md`, `docs/PROJECT_PLAN.md`, `docs/RESULTS_PROTOCOL.md`, and `configs/`.

## V3 result pipeline

The code mirrors the manuscript's RQ-oriented Results section. Every final table or figure must originate from frozen machine-readable outputs.

Primary result surfaces:
- benchmark table: logical equivalence, answer accuracy, solver-executable rate, ECE, AURC, semantic-error AUROC;
- selective-policy table at **80%, 90%, and 95% coverage**;
- semantic-error taxonomy table;
- ablation table;
- efficiency/intervention table;
- cross-model and cross-dataset calibration-transfer table;
- risk–coverage curve and translation-risk reliability diagram;
- uncertainty-component diagnostic figure;
- reliability–cost frontier.

After real runs create `results/per_example.csv`, use the complete analysis path:

```bash
python scripts/validate_results.py --input results/per_example.csv
python scripts/build_result_artifacts.py --input results/per_example.csv
pip install -e ".[plot]"
python scripts/plot_results.py
python scripts/export_latex_tables.py
```

Outputs are separated deliberately:
- `results/*.csv` — real machine-readable empirical outputs, kept local/release-archived until frozen;
- `results/*_template.csv` — versioned schemas for every manuscript table;
- `artifacts/figures/*.pdf` — manuscript-ready plots generated from real results;
- `artifacts/tables/*.tex` — LaTeX fragments exported from frozen result CSVs.

`src/usembridge/results.py` implements result aggregation, fixed-coverage evaluation, semantic-error breakdowns, component-level error-detection AUROC, paired bootstrap confidence intervals, and an exact McNemar test for paired binary outcomes.

No analysis script is allowed to manufacture missing performance values: absent empirical inputs should fail loudly rather than generate synthetic manuscript results.

## Reproducibility

Every reported run must record the git commit, dataset source commit/hash, model/tokenizer revision, prompt hash, decoding config, seed, solver version/timeouts, raw CIR candidates, compiled formula, solver output, uncertainty components, calibrated risk, policy action, and per-example metrics.

Final paper tables/figures must be generated programmatically from machine-readable results.

## Repository map

```text
configs/              model/dataset/experiment configs
schemas/              CIR + run-manifest schemas
data/                 manifests + ignored raw/processed data
docs/                 research, evidence, and reproducibility protocols
examples/             auditable CIR examples
paper/                manuscript synchronization notes during pre-results stage
results/              versioned schemas/templates + generated result contract
scripts/              setup/data/baseline/result/plot/table workflows
src/usembridge/       reusable implementation
tests/                unit tests
artifacts/figures/     generated manuscript-ready plots (ignored until frozen)
artifacts/tables/      generated LaTeX result fragments (ignored until frozen)
.github/workflows/    CPU CI
```

The full evolving manuscript remains in the dedicated Overleaf/paper package until results are frozen, to avoid maintaining a stale duplicate. At submission/release time, the exact manuscript source will be synchronized under `paper/` with the matching code commit.

## Evidence discipline

`docs/CLAIMS_AND_EVIDENCE.md` maps each manuscript claim to the empirical evidence required before it can be stated as a result. `docs/RESULTS_CHECKLIST.md` is the submission gate. Claims without evidence remain hypotheses or planned evaluations.

## Non-claims

Before real experiments, this repository does not claim superiority over baselines, legal correctness on real cases, calibrated uncertainty on unseen domains, successful human-expert evaluation, or final IJUFKS formatting.

## License status

A software license has **not** been selected yet. That is an intentional project-owner decision rather than something automated by this scaffold. Third-party data/code retain their upstream licenses; see `THIRD_PARTY.md`.

See `CITATION.cff` for provisional citation metadata.
