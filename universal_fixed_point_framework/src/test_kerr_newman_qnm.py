"""
test_kerr_newman_qnm.py

Phase 15B-5: Kerr-Newman QNM 推广测试。
"""

from __future__ import annotations

import pytest

from kerr_newman_qnm import KerrNewmanBlackHole, KerrNewmanQNM
from physics_open_problems_advanced import FullTeukolskyQNM


def test_kerr_newman_basic():
    kn = KerrNewmanBlackHole(M=1.0, a=0.5, Q=0.3)
    assert kn.r_plus > kn.r_minus
    assert not kn.extremal_limit()

    qnm = KerrNewmanQNM(M=1.0, a=0.5, Q=0.3, s=-2)
    result = qnm.solve_full(l=2, m=0, n=0)
    assert result["converged"]
    assert result["omega"].imag < 0


def test_kerr_newman_vs_kerr():
    kerr = FullTeukolskyQNM(M=1.0, a=0.5, s=-2)
    kn_zero_q = KerrNewmanQNM(M=1.0, a=0.5, Q=0.0, s=-2)

    kerr_result = kerr.solve_full(l=2, m=0, n=0)
    kn_result = kn_zero_q.solve_full(l=2, m=0, n=0)

    diff = abs(kerr_result["omega"] - kn_result["omega"])
    assert diff < 0.01


def test_kerr_newman_charged():
    for Q in [0.1, 0.2, 0.3]:
        qnm = KerrNewmanQNM(M=1.0, a=0.3, Q=Q, s=-2)
        result = qnm.solve_full(l=2, m=0, n=0)
        assert result["converged"]
        assert result["omega"].imag < 0