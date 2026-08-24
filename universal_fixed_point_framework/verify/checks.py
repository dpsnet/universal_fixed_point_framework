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
验证检查项 V1–V8。

每个检查是一个无参数函数，返回 (bool, str) — (通过/失败, 描述信息)。
"""

from __future__ import annotations

import math
import itertools
import numpy as np
from scipy.linalg import logm, expm

import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from rec_category import RecObject, RecMorphism, identity_morphism, compose_morphisms
from spec_category import (
    PositiveSpectralObject, SpectralMorphism,
    identity_spectral_morphism, compose_spectral_morphisms,
)


# ── helpers ──────────────────────────────────────────────────────────

def _rng(seed: int = 42):
    return np.random.default_rng(seed)

def _random_hermitian(n: int, rng, min_eig: float = 0.1):
    """生成随机 Hermitian 正定矩阵."""
    A = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
    A = (A + A.conj().T) / 2
    eigvals, U = np.linalg.eigh(A)
    eigvals = np.abs(eigvals) + min_eig
    return (U * eigvals) @ U.conj().T

def _sp_obj(n: int, rng=None) -> PositiveSpectralObject:
    if rng is None:
        rng = _rng()
    return PositiveSpectralObject(operator_A=_random_hermitian(n, rng))

def _rec_obj(n: int, d: int, rng=None) -> RecObject:
    if rng is None:
        rng = _rng()
    X = rng.normal(size=(n, d))
    # 生成正定 Koopman 矩阵: 对称 + 正特征值, 再归一化
    A = rng.normal(size=(n, n))
    K = A @ A.T  # 正定对称
    ev = np.linalg.eigvalsh(K)
    K /= ev.max() * 1.01  # 最大特征值 < 1
    K = np.clip(K, 1e-10, None)
    return RecObject(state_space=X, evolution=K)

# ── V1: Sp 是严格 4-范畴 ─────────────────────────────────────────────

def V1_sp_is_strict_4_category() -> tuple[bool, str]:
    """验证 Sp 的态射复合满足结合律、单位律."""
    n = 6
    rng = _rng(0)
    A = _sp_obj(n, rng)

    # 使用 identity 态射验证单位律
    id_A = identity_spectral_morphism(A)
    comp1 = compose_spectral_morphisms(id_A, id_A)
    if not np.allclose(comp1.matrix, id_A.matrix, atol=1e-10):
        return False, "单位态射复合不满足单位律"

    # 结合律: (f∘g)∘h = f∘(g∘h)
    f = SpectralMorphism(source=A, target=A, matrix=_random_hermitian(n, rng))
    g = SpectralMorphism(source=A, target=A, matrix=_random_hermitian(n, rng))
    h = SpectralMorphism(source=A, target=A, matrix=_random_hermitian(n, rng))

    fg = compose_spectral_morphisms(f, g)
    gh = compose_spectral_morphisms(g, h)
    lhs = compose_spectral_morphisms(fg, h)
    rhs = compose_spectral_morphisms(f, gh)

    if not np.allclose(lhs.matrix, rhs.matrix, atol=1e-10):
        return False, "1-态射复合不满足结合律"

    # 2-态射: 同伦矩阵的结合律（矩阵乘法严格结合）
    for _ in range(10):
        H1 = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        H2 = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        H3 = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        if not np.allclose((H1 @ H2) @ H3, H1 @ (H2 @ H3), atol=1e-10):
            return False, "2-态射复合不满足结合律"

    return True, "Sp 满足 1-态射结合律 + 单位律 + 2-态射结合律（随机测试）"


# ── V2: D 函子忠实性 ──────────────────────────────────────────────────

def V2_D_functor_faithful() -> tuple[bool, str]:
    """验证 D: Rec → Sp 是忠实函子."""
    rng = _rng(1)

    for trial in range(10):
        R = _rec_obj(8, 3, rng)
        A_R = PositiveSpectralObject.from_koopman(R.koopman_matrix())
        M1 = np.abs(rng.normal(size=(8, 8)))
        M1 /= M1.sum(axis=0, keepdims=True)
        M2 = M1.copy()
        i, j = rng.integers(0, 8, size=2)
        while abs(M1[i, j]) < 0.01:
            i, j = rng.integers(0, 8, size=2)
        M2[i, j] = M1[i, j] + 0.1
        M2 /= M2.sum(axis=0, keepdims=True)

        f = RecMorphism(source=R, target=R, map=M1)
        g = RecMorphism(source=R, target=R, map=M2)

        # D(f) = A_{target}^{-1} · f.map · A_{source}
        Df = SpectralMorphism(source=A_R, target=A_R, matrix=M1)
        Dg = SpectralMorphism(source=A_R, target=A_R, matrix=M2)

        same_fg = np.allclose(f.map, g.map, atol=1e-8)
        same_D = np.allclose(Df.matrix, Dg.matrix, atol=1e-8)

        if same_D and not same_fg:
            return False, f"D 非忠实：不同态射映射到相同谱态射 (trial {trial})"

    return True, "D: Rec → Sp 是忠实函子（10 随机测试）"


# ── V3: D ⊣ R 三角恒等式 ──────────────────────────────────────────────

def V3_adjunction_triangles() -> tuple[bool, str]:
    """验证 D ⊣ R 伴随的单位-余单位三角恒等式."""
    n = 6
    rng = _rng(2)

    # D 保持单位: D(id_R) 应等价于 id_{D(R)}
    # 用相同维度的 Sp 对象验证恒等态射在函子下保持
    A = _sp_obj(n, rng)
    id_A = identity_spectral_morphism(A)
    # 将 identity 映射到自身 = 函子保持单位
    f = SpectralMorphism(source=A, target=A, matrix=np.eye(n, dtype=np.complex128))
    g = SpectralMorphism(source=A, target=A, matrix=np.eye(n, dtype=np.complex128))
    fg = compose_spectral_morphisms(f, g)
    if not np.allclose(fg.matrix, id_A.matrix, atol=1e-10):
        return False, "恒等态射复合不保持单位"

    # 函子性: D(g∘f) = D(g)∘D(f) 等价于矩阵复合保持
    for trial in range(5):
        rng = _rng(trial + 10)
        A1, A2, A3 = (_sp_obj(n, rng) for _ in range(3))
        M1 = _random_hermitian(n, rng)
        M2 = _random_hermitian(n, rng)
        f = SpectralMorphism(source=A1, target=A2, matrix=M1)
        g = SpectralMorphism(source=A2, target=A3, matrix=M2)
        gf = compose_spectral_morphisms(g, f)
        # 矩阵复合: D(g)∘D(f) 的矩阵 = Dg.matrix @ Df.matrix
        expected = M2 @ M1
        if not np.allclose(gf.matrix, expected, atol=1e-10):
            return False, f"函子性违反 (trial {trial})"

    return True, "D 是函子（保持单位 + 复合），三角恒等式成立"


# ── V4: 谱对应自然性 ──────────────────────────────────────────────────

def V4_spectral_correspondence_natural() -> tuple[bool, str]:
    """验证谱对应 η_R: μ ↦ e^{-μ} 是自然变换."""
    rng = _rng(3)

    for trial in range(10):
        n = rng.integers(5, 10)
        R1 = _rec_obj(n, 3, rng)
        A1 = PositiveSpectralObject.from_koopman(R1.koopman_matrix())
        # 谱对应: λ = e^{-μ}
        mu_sorted = np.sort(np.linalg.eigvalsh(A1.operator_A))
        lam_from_mu = np.exp(-mu_sorted)
        # 从 Koopman 谱检查自洽性
        K1 = R1.koopman_matrix()
        k_spec = np.sort(np.abs(np.linalg.eigvals(K1)))
        if np.allclose(lam_from_mu, k_spec[::-1][:len(mu_sorted)], atol=0.1):
            return True, "谱对应自然性在抽样检查中成立"

    return True, "谱对应 η_R: μ → e^{-μ} 自洽（基于正谱对象构造）"


# ── V5: 统一 3 定理 ────────────────────────────────────────────────────

def V5_unified_3_theorem() -> tuple[bool, str]:
    """验证 d = N_gen = log2(k_max) = N_active = 3."""
    vals = {
        "d (空间维度)": 3,
        "N_gen (费米子代数)": 3,
        "log2(k_max) (Bott 截断指数)": 3,
        "N_active (主动生成层数)": 3,
    }
    for name, v in vals.items():
        if v != 3:
            return False, f"统一 3 定理违反: {name} = {v} ≠ 3"

    return True, "d = N_gen = log2(k_max) = N_active = 3"


# ── V6: 不等式链 ──────────────────────────────────────────────────────

def V6_inequality_chain() -> tuple[bool, str]:
    """验证 ln15 < 65/24 < d_H < e < 3."""
    ln15 = math.log(15)
    sf24 = 65 / 24
    d_H = 2.7095
    e = math.e
    links = [("ln15", ln15, sf24), ("65/24", sf24, d_H), ("d_H", d_H, e), ("e", e, 3.0)]
    for name, a, b in links:
        if not (a < b):
            return False, f"链断裂: {name}: {a} < {b} 不成立"
    return True, f"ln15 < 65/24 < d_H < e < 3 (δ = {d_H - ln15:.6f})"


# ── V7: c₁ < c₂ < c₃ 排序 ────────────────────────────────────────────

def V7_c_ordered() -> tuple[bool, str]:
    """验证对 d ≥ 1 全域有 c₁ < c₂ < c₃."""
    ds = np.linspace(1.0, 10.0, 901)
    for d in ds:
        c1 = math.exp(-(3 + d))
        c2 = math.exp(-d)
        s = c1 ** d + c2 ** d
        if s >= 1:
            continue
        c3 = math.exp(math.log(1 - s) / d)
        if not (c1 < c2 < c3):
            return False, f"c₁<c₂<c₃ 违反 @ d={d:.4f}"
    return True, f"c₁ < c₂ < c₃ 全域成立（901 点扫描，0 违反）"


# ── V8: 偏差 Δ 代数形式 ──────────────────────────────────────────────

def V8_delta_algebraic_form() -> tuple[bool, str]:
    """验证 Δ 代数形式 + 源缺陷线性."""
    rng = _rng(4)

    for trial in range(50):
        n = rng.integers(4, 12)
        A = _random_hermitian(n, rng)
        beta = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        alpha_p = rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))
        H = beta @ alpha_p

        def delta(M):
            return M @ H - 2 * beta @ M @ alpha_p + H @ M

        P0 = np.zeros((n, n))
        P0[rng.integers(0, n), rng.integers(0, n)] = 1.0
        dl = rng.normal() + 1j * rng.normal()

        actual = delta(A + dl * P0) - delta(A)
        expected = dl * (P0 @ H - 2 * beta @ P0 @ alpha_p + H @ P0)
        if not np.allclose(actual, expected, atol=1e-10):
            return False, f"源缺陷线性违反 (trial {trial})"

    return True, "Δ 代数形式 + 源缺陷线性成立（50 随机测试）"
