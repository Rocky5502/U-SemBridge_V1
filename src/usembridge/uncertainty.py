from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Sequence


def disagreement(values: Sequence[Any]) -> float:
    if not values:
        return 1.0
    counts = Counter(map(repr, values))
    return 1.0 - max(counts.values()) / len(values)


def grounding_uncertainty(candidate_predicate_maps: Sequence[dict[str, Any]]) -> float:
    return disagreement(candidate_predicate_maps)


def structural_uncertainty(ast_signatures: Sequence[str]) -> float:
    return disagreement(ast_signatures)


def completeness_uncertainty(
    provenance_coverage: float,
    unresolved_count: int,
    required_slots: int,
) -> float:
    gap = 1.0 - max(0.0, min(1.0, provenance_coverage))
    unresolved = min(1.0, unresolved_count / max(1, required_slots))
    return 0.5 * gap + 0.5 * unresolved


def solver_sensitivity_uncertainty(outcomes: Sequence[str]) -> float:
    return disagreement(outcomes)


@dataclass(frozen=True)
class RiskComponents:
    grounding: float
    structural: float
    completeness: float
    solver_sensitivity: float

    def clipped(self) -> "RiskComponents":
        def clip(value: float) -> float:
            return max(0.0, min(1.0, float(value)))

        return RiskComponents(
            clip(self.grounding),
            clip(self.structural),
            clip(self.completeness),
            clip(self.solver_sensitivity),
        )


def aggregate_risk(
    components: RiskComponents,
    weights: Sequence[float] = (0.25, 0.25, 0.25, 0.25),
) -> float:
    if len(weights) != 4 or sum(weights) <= 0:
        raise ValueError("weights must contain four positive-total entries")
    c = components.clipped()
    vals = [c.grounding, c.structural, c.completeness, c.solver_sensitivity]
    total = sum(weights)
    return sum(w * v for w, v in zip(weights, vals)) / total
