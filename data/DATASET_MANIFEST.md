# Dataset Manifest

## Primary benchmarks

### FOLIO
Role: primary natural-language -> first-order-logic semantic fidelity benchmark.
Use: gold logical structure, entailment classification, translation-error analysis.

### ProofWriter
Role: controlled rule/fact reasoning with explicit True / False / Unknown cases.
Use: open-world semantics, missing-fact stress tests, depth robustness.

### ProofFOL
Role: NL-to-FOL translation-error baseline and verifier comparison.
Use only if the released data/code license permits the intended reproduction.

## Transfer study

### LegalBridge (planned; not an existing public dataset)
Quantitative claims are forbidden until expert-reviewed formalizations exist.
Recommended protocol: select compact rule-oriented cases; independently annotate; adjudicate; record ambiguity/provenance; separate factual uncertainty from normative ambiguity.

## Data integrity rules
- No hidden evaluation-set tuning.
- Record dataset version/commit/hash.
- Record license and redistribution restrictions.
- Store only derived IDs/metadata when redistribution is disallowed.
- Keep raw data immutable and preprocessing deterministic.
