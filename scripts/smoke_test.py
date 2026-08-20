from pathlib import Path

from usembridge.pipeline import decide
from usembridge.schema import load_and_validate
from usembridge.solvers.semantic_gap import run_semantic_gap_demo
from usembridge.uncertainty import RiskComponents

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    example = load_and_validate(ROOT / "examples" / "legal_deletion_request.cir.json")
    assert example["instance_id"]
    decision = decide(RiskComponents(0.10, 0.10, 0.30, 0.50), unresolved_critical=True)
    demo = run_semantic_gap_demo()
    assert demo.violation_possible and demo.no_violation_possible and demo.naive_mapping_forces_violation
    print(f"Schema: OK ({example['instance_id']})")
    print(f"Policy smoke decision: risk={decision.risk:.3f}, action={decision.action.value}")
    print("Semantic-gap demo: OK")
    print("U-SemBridge pre-run smoke test: PASS")


if __name__ == "__main__":
    main()
