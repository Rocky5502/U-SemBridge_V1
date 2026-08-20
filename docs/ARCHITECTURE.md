# Architecture

## Principle
A deterministic solver only guarantees properties of the formal object it receives. U-SemBridge therefore treats the translation boundary as a first-class object with provenance, uncertainty, and selective action.

## Stages
1. Source ingestion: rules, facts, query, provenance spans.
2. Candidate translation: generate K CIR candidates without silently resolving missing information.
3. CIR validation: schema + type/slot checks.
4. Uncertainty extraction: grounding, structure, completeness, solver sensitivity.
5. Calibration: validation-only mapping from signals to semantic-error probability.
6. Selective policy: VERIFY / COMPARE_REPAIR / CLARIFY / ABSTAIN.
7. Formal compilation and solver execution.
8. Audit record: source, translation, edits, risk components, action, solver result.

## Semantic safety invariant
Absence of evidence must not automatically become explicit negation. `not recorded(exception)` is not `not exception_applies` unless a justified domain rule licenses that inference.
