from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Action(str, Enum):
    VERIFY = "VERIFY"
    COMPARE_REPAIR = "COMPARE_REPAIR"
    CLARIFY = "CLARIFY"
    ABSTAIN = "ABSTAIN"


@dataclass(frozen=True)
class PolicyThresholds:
    verify_max_risk: float = 0.25
    repair_max_risk: float = 0.55
    clarify_max_risk: float = 0.80

    def validate(self) -> None:
        if not 0 <= self.verify_max_risk <= self.repair_max_risk <= self.clarify_max_risk <= 1:
            raise ValueError("thresholds must satisfy 0 <= verify <= repair <= clarify <= 1")


def choose_action(
    risk: float,
    unresolved_critical: bool = False,
    thresholds: PolicyThresholds | None = None,
) -> Action:
    t = thresholds or PolicyThresholds()
    t.validate()
    risk = max(0.0, min(1.0, float(risk)))
    if unresolved_critical:
        return Action.CLARIFY if risk <= t.clarify_max_risk else Action.ABSTAIN
    if risk <= t.verify_max_risk:
        return Action.VERIFY
    if risk <= t.repair_max_risk:
        return Action.COMPARE_REPAIR
    if risk <= t.clarify_max_risk:
        return Action.CLARIFY
    return Action.ABSTAIN
