from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .policy import Action, PolicyThresholds, choose_action
from .uncertainty import RiskComponents, aggregate_risk


@dataclass(frozen=True)
class Decision:
    risk: float
    action: Action
    components: RiskComponents


def decide(
    components: RiskComponents,
    unresolved_critical: bool = False,
    thresholds: PolicyThresholds | None = None,
    weights: Sequence[float] = (0.25, 0.25, 0.25, 0.25),
) -> Decision:
    risk = aggregate_risk(components, weights)
    action = choose_action(
        risk,
        unresolved_critical=unresolved_critical,
        thresholds=thresholds,
    )
    return Decision(risk=risk, action=action, components=components)
