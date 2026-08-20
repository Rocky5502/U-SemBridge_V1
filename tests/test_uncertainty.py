from usembridge.uncertainty import RiskComponents, aggregate_risk, completeness_uncertainty, disagreement


def test_disagreement():
    assert disagreement(["a", "a", "b", "a"]) == 0.25
    assert disagreement([]) == 1.0


def test_completeness():
    assert completeness_uncertainty(1.0, 0, 4) == 0.0
    assert completeness_uncertainty(0.0, 4, 4) == 1.0


def test_aggregate_risk():
    c = RiskComponents(0.0, 0.2, 0.4, 0.6)
    assert abs(aggregate_risk(c) - 0.3) < 1e-9
