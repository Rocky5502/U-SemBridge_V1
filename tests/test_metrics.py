from usembridge.metrics import aurc, brier_score, expected_calibration_error


def test_metrics_basic():
    p = [0.1, 0.2, 0.8, 0.9]
    y = [0, 0, 1, 1]
    assert 0 <= brier_score(p, y) <= 1
    assert 0 <= expected_calibration_error(p, y, n_bins=2) <= 1
    assert 0 <= aurc(p, y) <= 1
