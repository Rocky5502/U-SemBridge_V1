# U-SemBridge

**Uncertainty-Aware Neuro-Symbolic Translation for Explainable and Verifiable Decision Reasoning**

U-SemBridge studies a specific failure mode in neuro-symbolic reasoning: a formal solver can be sound while the natural-language-to-symbolic translation it receives is semantically wrong.

The project treats semantic translation as an uncertainty and assurance problem. It uses a Controlled Intermediate Representation (CIR), translation-risk signals, and a selective policy over **VERIFY**, **COMPARE/REPAIR**, **CLARIFY**, and **ABSTAIN**.

## Research target

Paper-in-progress for the IJUFKS special issue **Neuro-Symbolic Computing for Explainable, Ethical, and Interpretable Intelligent Systems**.

**Pre-experiment status:** code, configs, data acquisition, tests, CI, and paper source are prepared. Numerical results remain intentionally TBD until real runs are completed.

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

Raw third-party datasets are not vendored. Fetch them reproducibly:

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

See `docs/EXPERIMENTS.md`, `docs/PROJECT_PLAN.md`, and `configs/`.

## Reproducibility

Every reported run must record the git commit, dataset source commit/hash, model/tokenizer revision, prompt hash, decoding config, seed, solver version/timeouts, raw CIR candidates, compiled formula, solver output, uncertainty components, calibrated risk, policy action, and per-example metrics.

Final paper tables/figures must be generated programmatically from machine-readable results.

## Repository map

```text
configs/              model/dataset/experiment configs
schemas/              CIR JSON schema
data/                 manifests + ignored raw/processed data
docs/                 research and reproducibility protocol
examples/             auditable CIR examples
paper/                IJUFKS manuscript source
scripts/              setup/data/baseline/smoke workflows
src/usembridge/       reusable implementation
tests/                unit tests
.github/workflows/    CPU CI
```

## Non-claims

Before real experiments, this repository does not claim superiority over baselines, legal correctness on real cases, calibrated uncertainty on unseen domains, successful human-expert evaluation, or final IJUFKS formatting.

See `THIRD_PARTY.md` for dataset/baseline handling and `CITATION.cff` for citation metadata.
