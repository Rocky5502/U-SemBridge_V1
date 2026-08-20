from usembridge.solvers.semantic_gap import run_semantic_gap_demo


def test_semantic_gap_demo():
    result = run_semantic_gap_demo()
    assert result.violation_possible
    assert result.no_violation_possible
    assert result.naive_mapping_forces_violation
