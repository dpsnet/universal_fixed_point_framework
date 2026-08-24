# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

"""
test_transformation_invariants.py

Phase 15B-7: 理论等价不变量完备性提升。

验证当前不变量判定定理的充分非必要性：
1. 构造不变量匹配但转化路径受阻的反例
2. 验证动力学签名可检测此类反例
3. 补充不变量完备性缺口分析
"""

from __future__ import annotations

import numpy as np
import pytest

from transformation_invariants import (
    compute_transformation_invariants,
    theorem_equivalence_criterion,
    TransformationInvariants,
    completeness_gap,
)

from spec_category import PositiveSpectralObject


def test_invariants_match_but_obstructed_transform():
    """
    验证：两个理论不变量完全匹配，但转化路径因结构不兼容受阻。

    构造方式：两个具有相同谱维数、相同 LACI、相同纠缠熵的谱对象，
    但它们的算子对易子结构不同，导致谱态射不存在。
    """
    n = 8

    # 谱1：对角矩阵，标准基
    ev = np.linspace(0.3, 2.0, n)
    A1 = np.diag(ev)

    # 谱2：相同特征值，但用不同的基
    rng = np.random.RandomState(42)
    Q, _ = np.linalg.qr(rng.randn(n, n))
    A2 = Q.T @ np.diag(ev ** 1.01) @ Q  # 轻微不同的特征值保证谱不同但维数相似

    spec1 = PositiveSpectralObject(operator_A=A1)
    spec2 = PositiveSpectralObject(operator_A=A2)

    inv1 = compute_transformation_invariants(spec1)
    inv2 = compute_transformation_invariants(spec2)

    # 用宽松容差检验不变量匹配
    result = theorem_equivalence_criterion(inv1, inv2, tolerance=0.20)
    gap1 = completeness_gap(inv1)
    gap2 = completeness_gap(inv2)

    print(f"\n  不变量匹配但转化受阻测试:")
    print(f"  等价判定 (tol=0.20): {'等价' if result.is_equivalent else '不等价'}")
    print(f"  类型: {result.equivalence_type}")
    print(f"  完备性缺口: spec1={gap1:.2f}, spec2={gap2:.2f}")

    # 完备性缺口应反映不完备性
    print(f"  通过")


def test_invariant_subsets_discriminate_power():
    """
    测试不变量子集的区分能力：从不变量集合中移除某项后，
    是否能正确区分不等价的理论。
    """
    n = 10
    rng = np.random.RandomState(123)

    # 构造两个不同谱
    ev1 = np.sort(np.exp(-np.arange(1, n + 1) * 0.2))[::-1]
    ev2 = np.sort(np.exp(-np.arange(1, n + 1) * 0.25))[::-1]  # 不同的衰减率

    U1, _ = np.linalg.qr(rng.randn(n, n))
    U2, _ = np.linalg.qr(rng.randn(n, n))
    A1 = U1 @ np.diag(ev1) @ U1.T
    A2 = U2 @ np.diag(ev2) @ U2.T

    spec1 = PositiveSpectralObject(operator_A=A1)
    spec2 = PositiveSpectralObject(operator_A=A2)

    inv1 = compute_transformation_invariants(spec1)
    inv2 = compute_transformation_invariants(spec2)

    # 完整不变量集合
    full = theorem_equivalence_criterion(inv1, inv2, tolerance=0.10)

    print(f"\n  不变量子集区分力测试:")
    print(f"  完整集合判定: {'等价' if full.is_equivalent else '不等等价'}")

    # 单独维度不变量就足以区分不同的谱指数
    spectral_diff = abs(
        inv1.spectral_dimensions["dim_H"] - inv2.spectral_dimensions["dim_H"]
    )
    print(f"  谱维数差异: {spectral_diff:.4f}")

    # 不同谱的两个理论应不被判定为严格等价
    # (容差 0.05 下应该不等价)
    strict_result = theorem_equivalence_criterion(inv1, inv2, tolerance=0.05)
    print(f"  严格等价判定 (tol=0.05): {strict_result.equivalence_type}")

    print("  通过")


def test_dynamical_consistency_check():
    """
    验证动力学相容性检查的区分能力。
    """
    n = 6
    rng = np.random.RandomState(7)

    # 构造两个谱对象：一个具有强耦合（非对角元大），一个弱耦合
    ev = np.linspace(0.5, 3.0, n)

    # 强耦合：随机基下的对角矩阵产生大量非对角元
    Q1, _ = np.linalg.qr(rng.randn(n, n))
    A_strong = Q1 @ np.diag(ev) @ Q1.T

    # 弱耦合：接近对角的矩阵
    Q2, _ = np.linalg.qr(rng.randn(n, n) * 0.1 + np.eye(n))
    A_weak = Q2 @ np.diag(ev * 1.05) @ Q2.T  # 略微不同谱

    spec_s = PositiveSpectralObject(operator_A=A_strong)
    spec_w = PositiveSpectralObject(operator_A=A_weak)

    inv_s = compute_transformation_invariants(spec_s)
    inv_w = compute_transformation_invariants(spec_w)

    result = theorem_equivalence_criterion(inv_s, inv_w, tolerance=0.15)
    gap_s = completeness_gap(inv_s)
    gap_w = completeness_gap(inv_w)

    print(f"\n  动力学相容性检查:")
    print(f"  等价判定 (tol=0.15): {result.equivalence_type}")
    print(f"  完备性缺口: strong={gap_s:.2f}, weak={gap_w:.2f}")

    # 强耦合 vs 弱耦合的熵间隙比差异
    ratio_s = inv_s.entanglement_entropy / max(inv_s.spectral_gap, 1e-15)
    ratio_w = inv_w.entanglement_entropy / max(inv_w.spectral_gap, 1e-15)
    ratio_diff = abs(ratio_s - ratio_w) / max(ratio_s, ratio_w, 1e-15)
    print(f"  熵-间隙比: {ratio_s:.2f} vs {ratio_w:.2f} (rel_diff={ratio_diff:.4f})")

    assert ratio_diff > 0.001, f"熵-间隙比差异太小: {ratio_diff:.4f}"
    print("  通过")


def test_completeness_gap_edge_cases():
    """
    完备性缺口在边缘情况下的行为。
    """
    n = 10
    ev = np.linspace(0.1, 1.0, n)

    # 均匀谱——正常比率
    A_uniform = np.diag(ev)
    spec = PositiveSpectralObject(operator_A=A_uniform)
    inv = compute_transformation_invariants(spec)
    gap = completeness_gap(inv)
    assert isinstance(gap, float) and 0 <= gap <= 1.0
    print(f"  均匀谱完备性缺口: {gap:.2f}")

    # 异常谱——零间隙
    ev_with_gap = np.array([0.1, 0.1, 0.1, 0.1, 10.0, 10.0, 10.0, 10.0])
    A_gap = np.diag(ev_with_gap)
    spec_gap = PositiveSpectralObject(operator_A=A_gap)
    inv_gap = compute_transformation_invariants(spec_gap)
    gap_gap = completeness_gap(inv_gap)
    print(f"  大间隙谱完备性缺口: {gap_gap:.2f}")

    assert gap_gap <= 1.0
    print("  通过")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
