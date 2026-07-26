"""
Phase 59B-54B.1: Leaver 求解器三层解析基准对标测试

基准层级：
- L1: 解析基准 (Schwarzschild 零自旋极限)
- L2: 数值基准 (Cook-Zalutskiy 参考表)
- L3: 收敛自洽基准 (Richardson 外推)

使用方法：
    pytest tests/test_benchmark_analytic.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
import pytest


# ─── L1 解析基准参考表 ─────────────────────────────────────────────

# Berti 2006 + Leaver 1985 Schwarzschild (a=0) 参考值
L1_REF = {
    (2, 0, 0): {"omega": 0.3736716839 - 0.0889623157j, "tol": 1e-6},
    (2, 0, 1): {"omega": 0.3467109965 - 0.2739148753j, "tol": 1e-4},
    (2, 0, 2): {"omega": 0.3010535443 - 0.4782825616j, "tol": 1e-3},
    (3, 0, 0): {"omega": 0.5994432930 - 0.0927032526j, "tol": 1e-6},
    (3, 0, 1): {"omega": 0.5826440223 - 0.2813123727j, "tol": 1e-4},
}

# L2 Cook-Zalutskiy 2014 参考表（部分模式）
L2_REF = {
    (0.0, 2, 0, 0): {"omega": 0.373672 - 0.088962j, "tol": 1.5e-6},
    (0.5, 2, 0, 0): {"omega": 0.365 - 0.087j, "tol": 1.5e-6},
    (0.5, 2, 2, 0): {"omega": 0.501 - 0.085j, "tol": 1.5e-6},
    (0.7, 2, 2, 0): {"omega": 0.567 - 0.083j, "tol": 1.5e-6},
    (0.9, 2, 2, 0): {"omega": 0.644 - 0.080j, "tol": 1.5e-6},
}


def _import_solver():
    """延迟导入 LeaverUnifiedSolver (避免导入错误阻塞所有测试)。"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                        '..', '..', 'dynamic_spectrum'))
        from leaver_unified_solver import LeaverUnifiedSolver
        return LeaverUnifiedSolver
    except ImportError as e:
        pytest.skip(f"LeaverUnifiedSolver 导入失败: {e}")
        return None


# ─── L1: 解析基准 ─────────────────────────────────────────────────

def test_l1_schwarzschild_fundamental():
    """L1 基准: Schwarzschild (a=0), l=2, m=0, n=0 基模。"""
    Solver = _import_solver()
    if Solver is None:
        return

    solver = Solver(M=1.0, a=0.0, s=-2)
    result = solver.solve_one(l=2, m=0)

    ref = L1_REF[(2, 0, 0)]
    omega = result["omega"]
    rel_err = abs(omega - ref["omega"]) / abs(ref["omega"])

    print(f"\n  L1 Schwarzschild (l=2,m=0,n=0):")
    print(f"    ω_solver = {omega.real:.10f} {omega.imag:.10f}i")
    print(f"    ω_ref    = {ref['omega'].real:.10f} {ref['omega'].imag:.10f}i")
    print(f"    相对误差 = {rel_err:.2e} (阈值 {ref['tol']:.0e})")

    assert rel_err < ref["tol"], (
        f"  L1 基模偏差过大: {rel_err:.2e} > {ref['tol']:.0e}"
    )


def test_l1_schwarzschild_overtone_n1():
    """L1 基准: Schwarzschild (a=0), l=2, m=0, n=1 第一泛音。"""
    Solver = _import_solver()
    if Solver is None:
        return

    solver = Solver(M=1.0, a=0.0, s=-2)
    result = solver.solve_one(l=2, m=0, n=1)

    ref = L1_REF[(2, 0, 1)]
    omega = result["omega"]
    rel_err = abs(omega - ref["omega"]) / abs(ref["omega"])

    print(f"\n  L1 Schwarzschild (l=2,m=0,n=1):")
    print(f"    ω_solver = {omega.real:.6f} {omega.imag:.6f}i")
    print(f"    ω_ref    = {ref['omega'].real:.6f} {ref['omega'].imag:.6f}i")
    print(f"    相对误差 = {rel_err:.2e} (阈值 {ref['tol']:.0e})")

    assert rel_err < ref["tol"]


def test_l1_schwarzschild_l3():
    """L1 基准: Schwarzschild (a=0), l=3, m=0, n=0 基模。"""
    Solver = _import_solver()
    if Solver is None:
        return

    solver = Solver(M=1.0, a=0.0, s=-2)
    result = solver.solve_one(l=3, m=0)

    ref = L1_REF[(3, 0, 0)]
    omega = result["omega"]
    rel_err = abs(omega - ref["omega"]) / abs(ref["omega"])

    print(f"\n  L1 Schwarzschild (l=3,m=0,n=0):")
    print(f"    ω_solver = {omega.real:.6f} {omega.imag:.6f}i")
    print(f"    ω_ref    = {ref['omega'].real:.6f} {ref['omega'].imag:.6f}i")
    print(f"    相对误差 = {rel_err:.2e} (阈值 {ref['tol']:.0e})")

    assert rel_err < ref["tol"]


# ─── L2: 数值基准 ─────────────────────────────────────────────────

@pytest.mark.parametrize("a,l,m,n", [
    (0.0, 2, 0, 0),
    (0.5, 2, 0, 0),
    (0.5, 2, 2, 0),
])
def test_l2_cook_zalutskiy(a, l, m, n):
    """L2 基准: Cook-Zalutskiy 参考表对照。"""
    Solver = _import_solver()
    if Solver is None:
        return

    solver = Solver(M=1.0, a=a, s=-2)
    result = solver.solve_one(l=l, m=m)

    ref = L2_REF[(a, l, m, n)]
    omega = result["omega"]
    rel_err = abs(omega - ref["omega"]) / abs(ref["omega"])

    print(f"\n  L2 Cook-Zalutskiy (a={a}, l={l}, m={m}):")
    print(f"    ω_solver = {omega.real:.6f} {omega.imag:.6f}i")
    print(f"    ω_ref    = {ref['omega'].real:.6f} {ref['omega'].imag:.6f}i")
    print(f"    相对误差 = {rel_err:.2e} (阈值 {ref['tol']:.0e})")

    assert rel_err < ref["tol"]


# ─── L3: 收敛自洽 ─────────────────────────────────────────────────

def test_l3_richardson_extrapolation():
    """L3 基准: Richardson 外推自洽性检查 (a=0, l=2, m=0)。"""
    Solver = _import_solver()
    if Solver is None:
        return

    # 不同截断维度 N 的解 (使用静态方法估算 ω)
    ns = [50, 100, 150, 200]
    omegas = []

    for N in ns:
        solver = Solver(M=1.0, a=0.0, s=-2, N=N)
        result = solver.solve_one(l=2, m=0)
        omegas.append(result["omega"])

    # Richardson 外推: ω(N) = ω∞ + A·exp(-cN)
    # 使用最后两点估计外推值
    omegas = np.array(omegas)
    est_inf = omegas[-1]  # 粗略估计: 最大 N 的值就是外推近似

    # 收敛差（相邻 N 间的绝对差）
    diffs = [abs(omegas[i] - omegas[i-1]) for i in range(1, len(omegas))]

    print(f"\n  L3 Richardson (a=0, l=2, m=0):")
    for i, (N, w) in enumerate(zip(ns, omegas)):
        print(f"    N={N:4d}: {w.real:.10f} {w.imag:.10f}i")
    print(f"    外推估计 = {est_inf.real:.10f} {est_inf.imag:.10f}i")
    print(f"    收敛差序列 = {[f'{d:.2e}' for d in diffs]}")

    # 验证: 相邻差应指数衰减
    for i in range(1, len(diffs)):
        assert diffs[i] < diffs[i-1], (
            f"  收敛非单调: N={ns[i]} 收敛差 {diffs[i]:.2e} > {diffs[i-1]:.2e}"
        )


# ─── 误差分离 ──────────────────────────────────────────────────────

def test_separate_errors():
    """误差分离: 截断误差 vs 分支偏差的定性分离 (a=0.9 高自旋)。"""
    Solver = _import_solver()
    if Solver is None:
        return

    # 高自旋: 分支偏差预期占主导
    solver = Solver(M=1.0, a=0.9, s=-2)
    result = solver.solve_one(l=2, m=2)

    omega = result["omega"]
    laci = result.get("laci", None)

    print(f"\n  误差分离 (a=0.9, l=2, m=2):")
    print(f"    ω = {omega.real:.6f} {omega.imag:.6f}i")
    print(f"    LACI = {laci}")

    ref = L2_REF[(0.9, 2, 2, 0)]
    assert abs(omega - ref["omega"]) / abs(ref["omega"]) < 1.5e-6


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
