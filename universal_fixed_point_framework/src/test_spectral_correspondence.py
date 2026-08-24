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
test_spectral_correspondence.py

验证 λ_i = e^{-μ_i} 作为范畴自然等价的离散原型。
"""

from __future__ import annotations

import numpy as np

from rec_category import RecObject, RecMorphism
from spectral_correspondence import (
    compression_spectrum,
    operator_spectrum,
    eta_R,
    verify_spectral_correspondence,
    verify_naturality,
)


def build_test_rec_objects():
    """构造测试用的 Rec 对象与合法态射。"""
    R1 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.9, 0.1], [0.1, 0.9]]),
    )
    # R2 与 R1 结构相同，因此恒等映射是合法态射
    R2 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.9, 0.1], [0.1, 0.9]]),
    )
    f = RecMorphism(source=R1, target=R2, map=np.eye(2))
    return R1, R2, f


def test_spectrum_shapes():
    print("\n[测试 1] M(R) 与 L(R) 的维度一致")
    R1, _, _ = build_test_rec_objects()
    mu = compression_spectrum(R1)
    lam = operator_spectrum(R1)
    assert mu.shape == lam.shape, "M(R) 与 L(R) 的谱长度不一致"
    print(f"  dim M(R) = dim L(R) = {len(mu)}")
    print("  通过")


def test_eta_is_bijection():
    print("\n[测试 2] η_R: M(R) -> L(R) 是双射（作为多重集合）")
    R1, _, _ = build_test_rec_objects()
    assert verify_spectral_correspondence(R1), "η_R 未将 M(R) 双射到 L(R)"
    print("  sorted(exp(-M(R))) ≈ sorted(L(R)): True")
    print("  通过")


def test_exponential_relation():
    print("\n[测试 3] 逐点指数关系 λ_i = e^{-μ_i}")
    R1, _, _ = build_test_rec_objects()
    mu = compression_spectrum(R1)
    lam = operator_spectrum(R1)
    lam_from_mu = eta_R(mu)
    # 多重集合相等
    assert np.allclose(np.sort(lam_from_mu), np.sort(lam), atol=1e-8)
    print("  exp(-μ) 与 L(R) 一致")
    print("  通过")


def test_naturality():
    print("\n[测试 4] η 对合法 Rec 态射满足自然性")
    _, _, f = build_test_rec_objects()
    assert verify_naturality(f), "η 的自然性不成立"
    print("  η_R2 ∘ M(f) = L(f) ∘ η_R1: True")
    print("  通过")


def main():
    print("=" * 60)
    print("谱自然等价 η: M ≅ L 的验证")
    print("=" * 60)

    test_spectrum_shapes()
    test_eta_is_bijection()
    test_exponential_relation()
    test_naturality()

    print("\n" + "=" * 60)
    print("所有谱自然等价测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
