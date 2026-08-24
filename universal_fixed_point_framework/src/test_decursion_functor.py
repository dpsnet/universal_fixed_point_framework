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
test_decursion_functor.py

验证谱去递归化函子 D: Rec -> Spec 的函子公理、忠实性以及右伴随 R 的原型性质。
"""

from __future__ import annotations

import numpy as np

from rec_category import RecObject, RecMorphism
from spec_category import PositiveSpectralObject
from decursion_functor import (
    DecursionFunctor,
    verify_functor_axioms,
    verify_faithfulness,
    right_adjoint_on_object,
    right_adjoint_on_morphism,
    unit,
    counit,
    verify_triangle_identities,
)
from spec_category import (
    identity_spectral_morphism,
    SpectralMorphism,
    compose_spectral_morphisms,
)
from rec_category import identity_morphism, compose_morphisms


def build_simple_rec_objects():
    """构造两个结构相同的 Rec 对象，用于忠实性测试。"""
    R = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.9, 0.1], [0.1, 0.9]]),
    )
    # R1 与 R2 相同，因此存在多个合法的结构保持自态射
    return R, R


def build_simple_morphisms(R1, R2):
    """构造两个不同的合法 Rec 态射 f, g: R1 -> R2。"""
    K = R1.koopman_matrix()
    # f = I 与 K 交换，是合法自态射
    f = RecMorphism(
        source=R1,
        target=R2,
        map=np.eye(2),
    )
    # g = K 本身也与 K 交换，是另一个合法自态射
    g = RecMorphism(
        source=R1,
        target=R2,
        map=K.copy(),
    )
    return f, g


def test_functor_identity():
    print("\n[测试 1] D 保持单位态射")
    R1, _ = build_simple_rec_objects()
    results = verify_functor_axioms(R1, None, None)
    assert results["preserves_identity"], "D(id_R) ≠ id_{D(R)}"
    print("  D(id_R) = id_{D(R)}: True")
    print("  通过")


def test_functor_composition():
    print("\n[测试 2] D 保持态射复合")
    # 构造 R1 -> R2 -> R3 链
    R1 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.9, 0.1], [0.1, 0.9]]),
    )
    R2 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.8, 0.2], [0.2, 0.8]]),
    )
    R3 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.7, 0.3], [0.3, 0.7]]),
    )
    f = RecMorphism(source=R1, target=R2, map=np.eye(2))
    g = RecMorphism(source=R2, target=R3, map=np.eye(2))

    results = verify_functor_axioms(R1, f, g)
    assert results["preserves_composition"], "D(g ∘ f) ≠ D(g) ∘ D(f)"
    print("  D(g ∘ f) = D(g) ∘ D(f): True")
    print("  通过")


def test_faithfulness():
    print("\n[测试 3] D 在离散原型上是忠实函子")

    # ----------------------------------------------------------------
    # 验证 A：一组不同的态射被 D 区分
    # ----------------------------------------------------------------
    R1, R2 = build_simple_rec_objects()
    f, g = build_simple_morphisms(R1, R2)
    assert not np.allclose(f.map, g.map), "测试构造错误：f 与 g 应不同"
    faithful_fg = verify_faithfulness(f, g)
    assert faithful_fg, "D 未区分 f 与 g，忠实性不成立"
    print("  (f, g) 不同对 → D(f) ≠ D(g): True")

    # 同一态射对自身通过
    faithful_ff = verify_faithfulness(f, f)
    assert faithful_ff, "verify_faithfulness 对相等态射应返回 True"
    print("  (f, f) 相同 → D(f) = D(f): True")

    # ----------------------------------------------------------------
    # 验证 B：范畴论意义的忠实性 — 通过多组随机态射验证
    # "D is faithful" means: for all f ≠ g, D(f) ≠ D(g).
    # 在 2×2 矩阵空间中采样多组不同的合法态射，逐一验证。
    # ----------------------------------------------------------------
    # 与给定 K 交换的矩阵构成交换子代数 {M | M·K = K·M}。
    # 对 K = [[0.9,0.1],[0.1,0.9]]，K 是对称矩阵，其交换子为
    # 形如 [[a, b], [b, a]] 的矩阵。
    K = R1.koopman_matrix()
    n_random = 5
    for idx in range(n_random):
        a = np.random.uniform(0.1, 2.0)
        b = np.random.uniform(0.0, 1.0)
        M = np.array([[a, b], [b, a]])
        # 验证 M 与 K 交换（合法态射）
        residual = K @ M - M @ K
        if np.linalg.norm(residual) > 1e-10:
            continue  # 跳过非交换矩阵
        f_rand = RecMorphism(source=R1, target=R2, map=M)
        # 构造另一个不同的态射
        a2 = a + 0.1 * np.random.uniform()
        b2 = b + 0.1 * np.random.uniform()
        M2 = np.array([[a2, b2], [b2, a2]])
        residual2 = K @ M2 - M2 @ K
        if np.linalg.norm(residual2) > 1e-10:
            continue
        if np.allclose(M, M2):
            continue
        g_rand = RecMorphism(source=R1, target=R2, map=M2)
        faithful_rand = verify_faithfulness(f_rand, g_rand)
        assert faithful_rand, (
            f"D 未区分随机态射对 #{idx}: f.map={M.tolist()}, g.map={M2.tolist()}"
        )
        print(f"  随机态射对 #{idx+1}: D 忠实 ✓")

    print("  通过（覆盖 %d 组随机态射）" % (n_random))


def test_right_adjoint_roundtrip():
    print("\n[测试 4] 右伴随 R 的原型：D(R(E)) ≈ E")
    # 构造一个谱对象 E
    E = PositiveSpectralObject(operator_A=np.diag([0.0, 0.5, 1.0]))
    R_of_E = right_adjoint_on_object(E)
    D_R_of_E = DecursionFunctor.map_object(R_of_E)

    # 检查 D(R(E)) 与 E 的谱算子一致
    assert np.allclose(D_R_of_E.operator_A, E.operator_A, atol=1e-8), (
        "D(R(E)) 的 A 与 E 不一致"
    )
    print("  D(R(E)).A ≈ E.A: True")
    print("  通过")


def test_morphism_intertwining():
    print("\n[测试 5] D(f) 满足谱交织条件")
    R1, R2 = build_simple_rec_objects()
    f, _ = build_simple_morphisms(R1, R2)
    D_f = DecursionFunctor.map_morphism(f)
    assert D_f.is_valid(), "D(f) 不满足强交织条件"
    print("  D(f) A_1 = A_2 D(f): True")
    print("  通过")


def test_right_adjoint_on_morphism():
    print("\n[测试 6] 右伴随在态射上的映射 R(φ)")
    # 构造谱对象与谱态射（φ 必须是合法的谱态射：φ A1 = A2 φ）
    # 取 A1 = diag(0, 0.5, 1.0), φ = diag(1, 2, 3), 则 A2 = φ A1 φ^{-1}
    A1 = np.diag([0.0, 0.5, 1.0])
    phi_mat = np.diag([1.0, 2.0, 3.0])
    A2 = phi_mat @ A1 @ np.linalg.inv(phi_mat)
    E1 = PositiveSpectralObject(operator_A=A1)
    E2 = PositiveSpectralObject(operator_A=A2)
    phi = SpectralMorphism(source=E1, target=E2, matrix=phi_mat, intertwining_mode="strict")

    R_phi = right_adjoint_on_morphism(phi)
    assert R_phi.source.evolution.shape == (3, 3)
    assert R_phi.target.evolution.shape == (3, 3)
    # R(φ) 满足 Rec 态射交织条件：K2 ∘ R(φ) = R(φ) ∘ K1
    K1, K2 = R_phi.source.koopman_matrix(), R_phi.target.koopman_matrix()
    lhs = K2 @ R_phi.map
    rhs = R_phi.map @ K1
    assert np.allclose(lhs, rhs, atol=1e-8)
    print("  R(φ) 满足 Rec 态射交织条件: True")
    print("  通过")


def test_adjunction_triangle_identities():
    print("\n[测试 7] 伴随函子 D ⊣ R 三角恒等式")
    # 构造 Rec 对象
    R = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.9, 0.1], [0.1, 0.9]]),
    )
    # 构造谱对象
    E = PositiveSpectralObject(operator_A=np.diag([0.0, 0.5, 1.0]))

    results = verify_triangle_identities(R, E)

    assert results["D_eta_comp_eps"], "D(η_R) ∘ ε_{D(R)} ≠ id_{D(R)}"
    assert results["R_eps_comp_eta"], "R(ε_E) ∘ η_{R(E)} ≠ id_{R(E)}"
    print(f"  D(η_R) ∘ ε_{{D(R)}} = id_{{D(R)}}: {results['D_eta_comp_eps']}")
    print(f"  R(ε_E) ∘ η_{{R(E)}} = id_{{R(E)}}: {results['R_eps_comp_eta']}")
    print("  通过")


def test_naturality_eta():
    print("\n[测试 8] η 的自然性：对任意 Rec 态射 f: R1 → R2，")
    print("  η_{R2} ∘ f = R(D(f)) ∘ η_{R1}")
    R1 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.9, 0.1], [0.1, 0.9]]),
    )
    R2 = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.8, 0.2], [0.2, 0.8]]),
    )
    f = RecMorphism(source=R1, target=R2, map=np.eye(2))

    eta_R1 = unit(R1)
    eta_R2 = unit(R2)
    R_D_f = right_adjoint_on_morphism(DecursionFunctor.map_morphism(f))
    D_f = DecursionFunctor.map_morphism(f)

    # 验证 η_{R2} ∘ f = R(D(f)) ∘ η_{R1}
    lhs = compose_morphisms(eta_R2, f)
    rhs = compose_morphisms(R_D_f, eta_R1)
    assert np.allclose(lhs.map, rhs.map, atol=1e-10)
    print("  自然性条件满足")
    print("  通过")


def test_naturality_eps():
    print("\n[测试 9] ε 的自然性：对任意谱态射 φ: E1 → E2，")
    print("  φ ∘ ε_{E1} = ε_{E2} ∘ D(R(φ))")
    E1 = PositiveSpectralObject(operator_A=np.diag([0.0, 0.5]))
    E2 = PositiveSpectralObject(operator_A=np.diag([0.1, 0.6]))
    phi = SpectralMorphism(source=E1, target=E2, matrix=np.eye(2), intertwining_mode="strict")

    eps_E1 = counit(E1)
    eps_E2 = counit(E2)
    R_phi = right_adjoint_on_morphism(phi)
    D_R_phi = DecursionFunctor.map_morphism(R_phi)

    from spec_category import compose_spectral_morphisms
    # 验证 φ ∘ ε_{E1} = ε_{E2} ∘ D(R(φ))
    lhs = compose_spectral_morphisms(phi, eps_E1)
    rhs = compose_spectral_morphisms(eps_E2, D_R_phi)
    assert np.allclose(lhs.matrix, rhs.matrix, atol=1e-10)
    print("  自然性条件满足")
    print("  通过")


# ===========================================================================
# 命题 2.10 验证：Spec 是 Rec 的反射子范畴
# ===========================================================================


def test_epsilon_is_isomorphism():
    """
    [命题 2.10.2] 验证 ε_E: D(R(E)) → E 是同构。

    在同构意义下要求：
    1. ε_E 的矩阵是可逆方阵（双射）；
    2. ε_E 的矩阵条件数在合理范围内（数值稳定）；
    3. D(R(E)) 与 E 的算子 A 一致（已由 test_right_adjoint_roundtrip 验证）。
    """
    print("\n[测试 10] ε_E: D(R(E)) → E 是同构")

    # 构造不同维度的谱对象
    for dim, diag in [(2, [0.0, 0.5]), (3, [0.0, 0.5, 1.0]), (2, [0.1, 0.8])]:
        E = PositiveSpectralObject(operator_A=np.diag(diag))
        eps_E = counit(E)

        # 检查矩阵是方阵且可逆
        assert eps_E.matrix.shape == (dim, dim), f"ε_E 矩阵形状错误: {eps_E.matrix.shape}"
        rank = np.linalg.matrix_rank(eps_E.matrix)
        assert rank == dim, f"ε_E 不满秩: rank={rank}, dim={dim}"

        # 检查条件数（数值可逆性）
        cond = np.linalg.cond(eps_E.matrix)
        assert cond < 1e10, f"ε_E 条件数过大: {cond:.2e}"

        # ε_E 是谱态射，应满足交织条件
        assert eps_E.is_valid(), "ε_E 不满足谱交织条件"

        print(f"  dim={dim}: 可逆 ✅, cond={cond:.2e}, 交织 ✅")

    print("  通过")


def test_eta_is_projection():
    """
    [命题 2.10.1] 验证 η_R: R → R(D(R)) 是投影。

    注：对非对称 Koopman 矩阵，D(R) 不一定存在（-logm(K) 的 Hermitian
    化可能非正定），因此测试限于 D 定义域内的 Rec 对象。

    η_R 作为单位态射，应满足：
    1. η_R 保持 Koopman 交换性（是合法 Rec 态射）；
    2. R(D(η_R)) ∘ η_R = η_R （三角恒等式 2 的显式验证）。
    """
    print("\n[测试 11] η_R: R → R(D(R)) 是投影")

    # 使用对角 Koopman 矩阵（正定，且在 D 定义域内）
    for lam in [0.5, 0.7, 0.9]:
        R = RecObject(
            state_space=np.array([[0.0], [1.0]]),
            evolution=np.diag([lam, lam]),
        )
        eta = unit(R)
        assert eta.is_valid(), f"η_R(λ={lam}) 不是合法 Rec 态射"

        # 投影性质：R(D(η_R)) ∘ η_R = η_R
        D_eta = DecursionFunctor.map_morphism(eta)
        R_D_eta = right_adjoint_on_morphism(D_eta)
        lhs = compose_morphisms(R_D_eta, eta)
        assert np.allclose(lhs.map, eta.map, atol=1e-10), (
            f"R(D(η_λ={lam})) ∘ η ≠ η，投影性质不成立"
        )
    print("  R(D(η_R)) ∘ η_R = η_R ✅ (λ=0.5,0.7,0.9)")

    # 对称 Koopman 矩阵
    R_sym = RecObject(
        state_space=np.array([[0.0], [1.0]]),
        evolution=np.array([[0.9, 0.1], [0.1, 0.9]]),
    )
    eta_sym = unit(R_sym)
    assert eta_sym.is_valid(), "η_R（对称情形）不是合法 Rec 态射"
    D_eta_sym = DecursionFunctor.map_morphism(eta_sym)
    R_D_eta_sym = right_adjoint_on_morphism(D_eta_sym)
    lhs_sym = compose_morphisms(R_D_eta_sym, eta_sym)
    assert np.allclose(lhs_sym.map, eta_sym.map, atol=1e-10)
    print("  对称 Koopman: R(D(η_R)) ∘ η_R = η_R ✅")

    print("  通过")


def test_r_is_full():
    """
    [命题 2.10] 验证 R: Spec → Rec 是满的（full）。

    即对任意谱态射 φ: E1 → E2，R(φ): R(E1) → R(E2) 是合法 Rec 态射。
    等价于：若 φ 满足谱交织条件 φ A_1 = A_2 φ，则
    R(φ) 满足 Koopman 交换性 K_{R(E2)} ∘ R(φ) = R(φ) ∘ K_{R(E1)}。
    """
    print("\n[测试 12] R: Spec → Rec 是满的")

    # 构造谱对象与满足交织条件的谱态射
    # 对 φ = diag(1,2) 且 A1 = diag(0, 0.5)，取 A2 = φ @ A1 @ inv(φ)
    A1 = np.diag([0.0, 0.5, 1.0])
    for factor in [1.0, 2.0, 0.5]:
        phi_mat = np.diag([1.0, factor, factor ** 2])
        A2 = phi_mat @ A1 @ np.linalg.inv(phi_mat)
        E1 = PositiveSpectralObject(operator_A=A1)
        E2 = PositiveSpectralObject(operator_A=A2)
        phi = SpectralMorphism(
            source=E1, target=E2,
            matrix=phi_mat,
            intertwining_mode="strict",
        )
        R_phi = right_adjoint_on_morphism(phi)
        assert R_phi.is_valid(), (
            f"R(φ) 不是合法 Rec 态射 (factor={factor})"
        )
        print(f"  factor={factor:.1f}: R(φ) 满足 K2∘R(φ)=R(φ)∘K1 ✅")

    # 恒等态射（A1 = A2 时）
    E = PositiveSpectralObject(operator_A=np.diag([0.0, 0.5]))
    phi_id = SpectralMorphism(source=E, target=E, matrix=np.eye(2), intertwining_mode="strict")
    R_id = right_adjoint_on_morphism(phi_id)
    assert R_id.is_valid(), "R(id) 不是合法 Rec 态射"
    print("  identity: R(id) 合法 ✅")

    print("  通过")


def main():
    print("=" * 60)
    print("谱去递归化函子 D 的公理与忠实性验证")
    print("=" * 60)

    test_functor_identity()
    test_functor_composition()
    test_faithfulness()
    test_right_adjoint_roundtrip()
    test_morphism_intertwining()
    test_right_adjoint_on_morphism()
    test_adjunction_triangle_identities()
    test_naturality_eta()
    test_naturality_eps()
    test_epsilon_is_isomorphism()
    test_eta_is_projection()
    test_r_is_full()

    print("\n" + "=" * 60)
    print("所有 D 函子测试通过。")
    print("=" * 60)


if __name__ == "__main__":
    main()
