# U-SemBridge Research Execution Plan

## Stage 0 — Lock claim
Test whether uncertainty over the semantic translation layer reduces high-confidence, formally valid but semantically wrong verified answers.

## Stage 1 — Reproduce baselines
FOLIO loading; ProofWriter; direct answer/CoT; LINC-style; Logic-LM-style; ProofFOL/CLOVER where reproducible. Do not continue to novelty claims until deviations from published baselines are documented.

## Stage 2 — CIR
Typed entities; predicates/argument types; quantifiers/scope; negation; exception/defeater fields; temporal/numeric constraints; unresolved assumptions; provenance spans.

## Stage 3 — Uncertainty
u_g grounding, u_s structure, u_c completeness/provenance, u_v solver outcome sensitivity. Calibrate on validation only.

## Stage 4 — Selective policy
VERIFY, COMPARE_REPAIR, CLARIFY, ABSTAIN. Tune thresholds against validation risk/coverage.

## Stage 5 — Main experiments
Mistral-7B-Instruct-v0.3, Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct if permitted; K={1,3,5}; low-temp primary; at least three seeds where randomness matters.

## Stage 6 — Ablations
No CIR, provenance, u_g, u_s, u_c, u_v, solver feedback, selective abstention; K comparison.

## Stage 7 — Error analysis
Manually classify a stratified sample using the frozen semantic-error taxonomy.

## Stage 8 — Legal transfer
Quantitative only with expert gold formalization. Otherwise 3–5 clearly qualitative cases.

## Stage 9 — Submission
Fill TBDs from machine-readable results; regenerate plots; statistical analysis; current World Scientific class; verify CFP metadata; citation/reference checks.
