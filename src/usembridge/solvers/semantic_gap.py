from __future__ import annotations

from dataclasses import dataclass

from z3 import And, Bool, Implies, Not, Solver, sat


@dataclass(frozen=True)
class SemanticGapResult:
    violation_possible: bool
    no_violation_possible: bool
    naive_mapping_forces_violation: bool


def run_semantic_gap_demo() -> SemanticGapResult:
    valid = Bool("valid_request")
    deadline = Bool("deadline_passed")
    exception_applies = Bool("exception_applies")
    exception_recorded = Bool("exception_recorded")
    violation = Bool("violation")

    rule = Implies(And(valid, deadline, Not(exception_applies)), violation)

    s = Solver()
    s.add(rule, valid, deadline, Not(exception_recorded))
    s.push()
    s.add(violation)
    violation_possible = s.check() == sat
    s.pop()
    s.push()
    s.add(Not(violation))
    no_violation_possible = s.check() == sat
    s.pop()

    s2 = Solver()
    s2.add(rule, valid, deadline, Not(exception_recorded), Not(exception_applies))
    s2.push()
    s2.add(Not(violation))
    not_violation_sat = s2.check() == sat
    s2.pop()

    return SemanticGapResult(
        violation_possible=violation_possible,
        no_violation_possible=no_violation_possible,
        naive_mapping_forces_violation=not not_violation_sat,
    )
