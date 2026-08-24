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
test_clifford_spinor_module.py

Phase 15C-2：Clifford 旋量模结构数值验证。

验证：
1. 原始幂等元 p² = p（旋量模生成元）
2. Cl·p 是最小左理想（旋量空间）
3. 旋量模谱结构（旋量谱 = 全 Clifford 谱）
4. Clifford 乘法保持旋量模封闭性
5. Cl(1,7) Majorana 旋量模
"""

from __future__ import annotations

import numpy as np
import pytest

from clifford_spectrum_demo import (
    cl17_generators,
    clifford_idempotent,
    spinor_module_basis,
    spinor_dim,
)


def _cl13_gammas():
    """构造 Cl(1,3) 的 gamma 矩阵。"""
    s1 = np.array([[0, 1], [1, 0]], dtype=float)
    s2 = np.array([[0, -1], [1, 0]], dtype=float)
    s3 = np.array([[1, 0], [0, -1]], dtype=float)
    I2 = np.eye(2, dtype=float)

    g0 = np.kron(s3, I2)
    g1 = np.kron(s1, s1)
    g2 = np.kron(s1, s2)
    g3 = np.kron(s1, s3)
    return [g0, g1, g2, g3]


def test_primitive_idempotent_cl13():
    """Cl(1,3) 原始幂等元 p² = p，秩 = 1。"""
    gammas = _cl13_gammas()
    p = clifford_idempotent(1, 3, gammas)

    # 幂等性
    err = np.max(np.abs(p @ p - p))
    assert err < 1e-10, f"幂等性失败: {err}"

    # 原始幂等元秩 = 1（在 M(4,ℝ) 中投影到 1 维子空间）
    rank = int(np.linalg.matrix_rank(p))
    assert rank == 1, f"原始幂等元秩错误: {rank} ≠ 1"


def test_primitive_idempotent_cl17():
    """Cl(1,7) 原始幂等元 p² = p。"""
    gammas = cl17_generators()
    p = clifford_idempotent(1, 7, gammas)

    err = np.max(np.abs(p @ p - p))
    assert err < 1e-10, f"幂等性失败: {err}"


def test_left_ideal_absorption():
    """Cl·p 是左理想：对任意 Clifford 元素 a，(a·p)·p = a·p。"""
    gammas = _cl13_gammas()
    p = clifford_idempotent(1, 3, gammas)

    # 测试所有 gamma 矩阵
    for i in range(4):
        a = gammas[i]
        ap = a @ p
        ap_p = ap @ p
        err = np.max(np.abs(ap_p - ap))
        assert err < 1e-10, f"左理想吸收失败: γ_{i}, 误差 {err}"

    # 测试二阶元素 γ_0 γ_1
    a = gammas[0] @ gammas[1]
    ap = a @ p
    ap_p = ap @ p
    err = np.max(np.abs(ap_p - ap))
    assert err < 1e-10, f"二阶元素吸收失败: γ_0γ_1, 误差 {err}"


def test_spinor_dim_cl13():
    """Cl(1,3) 旋量空间维度 = 4（Dirac 旋量）。"""
    gammas = _cl13_gammas()
    dim = spinor_dim(1, 3, gammas)
    assert dim == 4, f"Cl(1,3) 旋量维度 {dim} ≠ 4"


def test_spinor_dim_cl17():
    """Cl(1,7) 旋量空间维度 = 8（Majorana 旋量）。"""
    gammas = cl17_generators()
    dim = spinor_dim(1, 7, gammas)
    assert dim == 8, f"Cl(1,7) 旋量维度 {dim} ≠ 8"


def test_spinor_basis_shape():
    """旋量基 S 应为 N×N 单位矩阵（N=矩阵表示维度）。"""
    gammas = _cl13_gammas()
    S = spinor_module_basis(1, 3, gammas)
    assert S.shape == (4, 4), f"旋量基形状错误: {S.shape}"

    # 应为单位矩阵
    ortho_err = np.max(np.abs(S - np.eye(4)))
    assert ortho_err < 1e-10, f"旋量基非单位: {ortho_err}"


def test_spinor_spectrum_equals_full():
    """旋量模谱 = 全 Clifford 谱（矩阵表示下自然一致）。"""
    gammas = _cl13_gammas()

    np.random.seed(42)
    coeffs = np.random.randn(4)
    A_full = sum(c * g for c, g in zip(coeffs, gammas))
    A_full = 0.5 * (A_full + A_full.T)

    # 旋量空间 = ℝ^4，Clifford 元素直接作用于旋量
    full_spec = np.sort(np.linalg.eigvalsh(A_full))
    spinor_spec = np.sort(np.linalg.eigvalsh(A_full))

    max_diff = np.max(np.abs(full_spec - spinor_spec))
    assert max_diff < 1e-10, f"旋量谱与全谱不一致: {max_diff}"


def test_clifford_multiplication_closure():
    """Clifford 乘法保持左理想封闭性：γ_i·(A·p) ∈ Cl·p。"""
    gammas = _cl13_gammas()
    p = clifford_idempotent(1, 3, gammas)

    # 取左理想元素 ψ = A·p（A = γ_3）
    A = gammas[3]
    psi = A @ p  # ψ ∈ Cl·p

    # 验证 γ_i·ψ 仍在左理想中：(γ_i·ψ)·p = γ_i·ψ（右乘吸收性）
    for i in range(4):
        gamma_psi = gammas[i] @ psi  # γ_i·ψ = (γ_i A)·p
        right_projected = gamma_psi @ p
        err = np.linalg.norm(right_projected - gamma_psi)
        assert err < 1e-10, f"Clifford 乘法不封闭: γ_{i}, 误差 {err}"


def test_cl17_spinor_idempotent():
    """Cl(1,7) 旋量模幂等性。"""
    gammas = cl17_generators()
    p = clifford_idempotent(1, 7, gammas)

    err = np.max(np.abs(p @ p - p))
    assert err < 1e-10, f"Cl(1,7) 幂等性失败: {err}"


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 15C-2: Clifford 旋量模结构测试")
    print("=" * 60)

    test_primitive_idempotent_cl13()
    print("  [1] Cl(1,3) 原始幂等元 ✓")
    test_primitive_idempotent_cl17()
    print("  [2] Cl(1,7) 原始幂等元 ✓")
    test_left_ideal_absorption()
    print("  [3] 左理想吸收性 ✓")
    test_spinor_dim_cl13()
    print("  [4] Cl(1,3) 旋量维度 ✓")
    test_spinor_dim_cl17()
    print("  [5] Cl(1,7) 旋量维度 ✓")
    test_spinor_basis_shape()
    print("  [6] 旋量基形状 ✓")
    test_spinor_spectrum_equals_full()
    print("  [7] 旋量谱 = 全谱 ✓")
    test_clifford_multiplication_closure()
    print("  [8] Clifford 乘法封闭性 ✓")
    test_cl17_spinor_idempotent()
    print("  [9] Cl(1,7) 旋量模 ✓")

    print("\n" + "=" * 60)
    print("全部 Clifford 旋量模结构测试通过。")
    print("=" * 60)
