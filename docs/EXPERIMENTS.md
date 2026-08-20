# Experiment Protocol

## Main hypothesis
At matched coverage, U-SemBridge should reduce high-confidence semantic translation failures compared with direct neuro-symbolic translation while preserving competitive task accuracy.

## Baselines
- direct LLM answer
- chain-of-thought
- LINC-style semantic parser + FOL prover
- Logic-LM-style translation + solver-feedback refinement
- ProofFOL verifier/correction when code/license permits
- U-SemBridge + ablations

## Datasets
### FOLIO
Use official upstream data for translation and entailment fidelity. Preserve original text and gold logical forms. Any derived split must be deterministic and documented.

### ProofWriter
Use open-world data and report True / False / Unknown separately; report by reasoning depth.

### LegalBridge
Only quantitative after expert-reviewed annotations exist. Until then, qualitative cases only.

## Models
Initial open-model matrix: Mistral-7B-Instruct-v0.3, Qwen2.5-7B-Instruct, and Llama-3.1-8B-Instruct if access/license permits. Run K in {1,3,5}; deterministic/low-temperature primary plus one sampling condition for disagreement.

## Calibration
Tune only on validation data. Test data may not influence feature weights, thresholds, demonstrations, decoding settings, or repair rounds.

## Metrics
Semantic/logical equivalence, answer accuracy/macro-F1, executable rate, Brier, ECE, AUROC for semantic-error detection, risk-coverage, AURC, solver calls, and latency.

## Error taxonomy
Predicate grounding; argument/type binding; quantifier/scope; negation/exception; temporal/numeric; coreference; omitted premise; hallucinated premise; logically equivalent surface variation.

## Statistics
Use paired instance-level comparisons and bootstrap confidence intervals for primary deltas and risk-coverage metrics. Freeze multiple-comparison handling before test evaluation.

## Freeze rule
Create a git tag before main runs. Any post-hoc change requires a new config ID and explicit reporting.
