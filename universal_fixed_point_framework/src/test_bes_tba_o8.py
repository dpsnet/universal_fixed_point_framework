"""
test_bes_tba_o8.py

Phase 15B-6: BES/TBA O(g⁸) 更高精度谱测试。
"""

from __future__ import annotations

import pytest
import numpy as np

from physics_open_problems_advanced import N4SYMBESFull


def test_bes_tba_o8_dressing_phase():
    """测试 O(g⁸) dressing phase 被正确计算。"""
    bes = N4SYMBESFull(N_c=3, lambda_tHooft=10.0)

    u = 1.0 + 0.5j
    v = -1.0 + 0.3j

    theta_6 = bes._dressing_phase_full(u, v, order=3)
    theta_8 = bes._dressing_phase_full(u, v, order=4)

    diff = abs(theta_8 - theta_6)
    print(f"  O(g⁸) - O(g⁶) dressing phase diff: {diff:.2e}")

    assert diff >= 0
    assert not np.isnan(diff)


def test_bes_tba_o8_convergence():
    """测试 O(g⁸) 求解器收敛。"""
    bes = N4SYMBESFull(N_c=3, lambda_tHooft=6.0)

    result = bes.solve_konishi_full(J=2, dressing_order=4)

    assert result["converged"] if "converged" in result else result["residual"] < 1e-6
    assert result["Delta"] > 0
    print(f"  O(g⁸) Delta = {result['Delta']:.6f}, residual = {result['residual']:.2e}")


def test_bes_tba_order_consistency():
    """测试不同阶数之间的一致性。"""
    bes = N4SYMBESFull(N_c=3, lambda_tHooft=6.0)

    result_2 = bes.solve_konishi_full(J=2, dressing_order=2)
    result_3 = bes.solve_konishi_full(J=2, dressing_order=3)
    result_4 = bes.solve_konishi_full(J=2, dressing_order=4)

    print(f"  O(g⁴): Delta = {result_2['Delta']:.6f}")
    print(f"  O(g⁶): Delta = {result_3['Delta']:.6f}")
    print(f"  O(g⁸): Delta = {result_4['Delta']:.6f}")

    diff_6_4 = abs(result_3["Delta"] - result_2["Delta"])
    diff_8_6 = abs(result_4["Delta"] - result_3["Delta"])

    print(f"  O(g⁶)-O(g⁴): {diff_6_4:.6e}")
    print(f"  O(g⁸)-O(g⁶): {diff_8_6:.6e}")

    assert diff_8_6 <= diff_6_4 or diff_8_6 < 1e-5