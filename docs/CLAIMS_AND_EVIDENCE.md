# Claims and Evidence Map

This file is a guardrail against overclaiming.

## C1 - CIR improves semantic fidelity
Evidence required:
- FOLIO logical-equivalence improvement over direct NL->FOL translation;
- confidence interval and paired statistical comparison;
- error taxonomy showing where gains occur.
Status: UNTESTED.

## C2 - Translation uncertainty predicts semantic failures
Evidence required:
- AUROC for semantic-error detection;
- Brier/ECE;
- reliability diagram;
- cross-model and cross-dataset calibration.
Status: UNTESTED.

## C3 - Selective action reduces high-confidence semantic errors
Evidence required:
- risk-coverage curves;
- risk at 80/90/95% coverage;
- count of high-confidence wrong formalizations;
- ablation without abstention/clarification.
Status: UNTESTED.

## C4 - Expert-steerable CIR reduces correction burden
Evidence required:
- approved human-study protocol;
- qualified participants;
- correction time and success rate;
- comparison against low-level FOL/SMT editing.
Status: FUTURE / OPTIONAL unless a real study is run.

## C5 - Fuzzy representation helps intrinsically graded predicates
Evidence required:
- explicitly graded transfer cases;
- crisp-threshold baseline;
- sensitivity analysis for membership functions.
Status: OPTIONAL EXTENSION, not a core claim yet.

## Manuscript result surfaces
- C1 is reported in the primary benchmark table + semantic-error breakdown + ablation table.
- C2 is reported in the reliability/risk-coverage figure + calibration-transfer table + component diagnostic figure.
- C3 is reported in the fixed-coverage selective-policy table and high-confidence-wrong counts.
- C4, if conducted, is reported only with real qualified participants and explicit expert-time measurements.
- Reliability/cost claims are supported by the efficiency table and measured Pareto frontier, never estimated prices or synthetic latency.
