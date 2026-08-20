# Results Checklist — MUST BE COMPLETE BEFORE SUBMISSION

## Table 1 — Primary benchmark results
- [ ] FOLIO logical equivalence (LE)
- [ ] FOLIO downstream answer accuracy
- [ ] solver-executable rate
- [ ] ECE and AURC
- [ ] ProofWriter/ProofFOL corresponding metrics

## Table 2 — Selective policy
- [ ] semantic error at 95% coverage
- [ ] semantic error at 90% coverage
- [ ] semantic error at 80% coverage
- [ ] answer accuracy at matched coverage
- [ ] high-confidence-wrong accepted cases
- [ ] oracle-risk upper bound

## Table 3 — Semantic error breakdown
- [ ] predicate grounding
- [ ] argument/type binding
- [ ] quantifier/scope
- [ ] negation/exception
- [ ] temporal/numeric
- [ ] coreference/entity
- [ ] omission/hallucination
- [ ] unknown→false collapse

## Table 4 — Ablations
- [ ] remove CIR
- [ ] remove provenance
- [ ] remove each UQ component (ug/us/uc/uv)
- [ ] remove candidate disagreement
- [ ] K=1/3/5
- [ ] remove abstention/clarification

## Table 5 — Efficiency and intervention
- [ ] LLM calls
- [ ] solver calls
- [ ] wall-clock latency
- [ ] input/output tokens
- [ ] peak memory
- [ ] optional expert correction time only if real qualified study exists

## Table 6 — Calibration transfer
- [ ] Mistral→Qwen
- [ ] Qwen→Llama if access allows
- [ ] FOLIO→ProofWriter
- [ ] ProofWriter→FOLIO
- [ ] logic benchmark→LegalBridge only if LegalBridge is expert validated

## Figures
- [ ] risk–coverage curves
- [ ] translation-risk reliability diagram
- [ ] uncertainty-component diagnostic plot
- [ ] semantic-error heatmap/bar chart if sufficiently populated
- [ ] reliability–cost Pareto plot

## Statistical evidence
- [ ] paired bootstrap confidence intervals
- [ ] McNemar or appropriate paired tests for primary binary comparisons
- [ ] effect sizes
- [ ] correction for multiple primary comparisons if testing several hypotheses

## Reproducibility
- [ ] exact model revisions
- [ ] prompts and prompt hash
- [ ] decoding parameters
- [ ] solver versions/timeouts
- [ ] random seeds
- [ ] per-example raw predictions
- [ ] run manifests
- [ ] result CSV files
- [ ] plot/table generation scripts
- [ ] environment lockfile

## Integrity
- [ ] no placeholder `TBD` remains
- [ ] no simulated value is presented as experiment
- [ ] all legal/medical examples labeled illustrative unless expert validated
- [ ] manuscript values are generated from frozen machine-readable outputs
