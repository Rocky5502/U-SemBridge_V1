from __future__ import annotations

import math
from typing import Sequence


def brier_score(prob_error: Sequence[float], is_error: Sequence[int]) -> float:
    if len(prob_error) != len(is_error) or not prob_error:
        raise ValueError("prob_error and is_error must be non-empty and equally sized")
    return sum((float(p) - int(y)) ** 2 for p, y in zip(prob_error, is_error)) / len(prob_error)


def expected_calibration_error(
    prob_error: Sequence[float],
    is_error: Sequence[int],
    n_bins: int = 10,
) -> float:
    if len(prob_error) != len(is_error) or not prob_error:
        raise ValueError("prob_error and is_error must be non-empty and equally sized")
    if n_bins <= 0:
        raise ValueError("n_bins must be positive")
    total = len(prob_error)
    ece = 0.0
    for b in range(n_bins):
        lo, hi = b / n_bins, (b + 1) / n_bins
        idx = [
            i
            for i, p in enumerate(prob_error)
            if (lo <= p < hi) or (b == n_bins - 1 and p == 1.0)
        ]
        if not idx:
            continue
        conf = sum(prob_error[i] for i in idx) / len(idx)
        freq = sum(is_error[i] for i in idx) / len(idx)
        ece += (len(idx) / total) * abs(conf - freq)
    return ece


def risk_coverage(prob_error: Sequence[float], is_error: Sequence[int]) -> list[tuple[float, float]]:
    if len(prob_error) != len(is_error) or not prob_error:
        raise ValueError("prob_error and is_error must be non-empty and equally sized")
    order = sorted(range(len(prob_error)), key=lambda i: prob_error[i])
    out: list[tuple[float, float]] = []
    errors = 0
    for k, i in enumerate(order, start=1):
        errors += int(is_error[i])
        out.append((k / len(order), errors / k))
    return out


def aurc(prob_error: Sequence[float], is_error: Sequence[int]) -> float:
    rc = risk_coverage(prob_error, is_error)
    if len(rc) < 2:
        return rc[0][1] if rc else math.nan
    area = 0.0
    prev_c, prev_r = 0.0, rc[0][1]
    for c, r in rc:
        area += (c - prev_c) * (r + prev_r) / 2.0
        prev_c, prev_r = c, r
    return area
