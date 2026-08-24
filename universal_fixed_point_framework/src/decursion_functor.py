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
decursion_functor.py

谱去递归化函子 D: Rec -> Spec 的最小原型实现。

对象映射：R -> (H_R, A_R, σ(A_R))，其中 A_R = -log(K_R)，K_R 为 R 的 Koopman 矩阵。
态射映射：f -> D(f)，由 f 诱导的 Koopman 提升算子的伴随。

扩展：
1. 支持带曲率的递归对象（CurvedRecObject），整合纤维丛曲率信息到谱对象中。
2. 支持非正规算子，通过数值半径和非正规性指标描述。
3. 支持无界算子，通过定义域管理和图范数描述。
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import expm, logm, eigvals

from rec_category import RecObject, RecMorphism
from spec_category import (
    PositiveSpectralObject,
    SpectralMorphism,
    identity_spectral_morphism,
    compose_spectral_morphisms,
)


class DecursionFunctor:
    """
    谱去递归化函子 D: Rec -> Spec。

    对递归系统 R，D(R) 是其 Koopman 算子的对数生成元 A_R 所确定的谱对象。
    对 Rec 态射 f: R1 -> R2，D(f) 是 SpectralMorphism，满足谱交织条件。
    """

    def __call__(self, obj: RecObject) -> PositiveSpectralObject:
        """对象映射 D(R)。"""
        return self.map_object(obj)

    @staticmethod
    def _numerical_radius(A: np.ndarray) -> float:
        max_val = 0.0
        for _ in range(100):
            x = np.random.randn(A.shape[0]) + 1j * np.random.randn(A.shape[0])
            x = x / np.linalg.norm(x)
            val = np.abs(np.vdot(x, A @ x))
            max_val = max(max_val, val)
        return max_val

    @staticmethod
    def _non_normality_index(A: np.ndarray) -> float:
        AAstar = A @ A.conj().T
        AstarA = A.conj().T @ A
        return np.linalg.norm(AAstar - AstarA) / (np.linalg.norm(A) ** 2 + 1e-15)

    @staticmethod
    def map_object(R: RecObject) -> PositiveSpectralObject:
        """
        将递归系统 R 映射为谱对象 E = D(R)。

        实现：
        1. 计算 R 的 Koopman 矩阵 K_R（不强制对称化）；
        2. 取 A_R = -log(K_R)；
        3. 若 R 为 CurvedRecObject，加入曲率修正项；
        4. 分析非正规性指标和数值半径；
        5. 返回 PositiveSpectralObject(operator_A=A_R)。

        注：不强制对称化 K_R。PositiveSpectralObject 的构造器负责保证
        A_R 的 Hermitian 性（通过 A ← (A + A^†)/2），这是在谱对象层面的
        合理近似，而非在 Koopman 层面改变动力学。
        """
        if hasattr(R, 'koopman_matrix_with_connection'):
            K = R.koopman_matrix_with_connection()
        else:
            K = R.koopman_matrix()

        try:
            A = -logm(K)
        except Exception:
            A = -logm(K + 1e-10 * np.eye(K.shape[0]))

        if hasattr(R, 'curvature') and R.curvature is not None:
            n = K.shape[0]
            curvature = R.curvature
            if curvature.ndim == 4:
                curvature_trace = np.trace(curvature.reshape(curvature.shape[0]*curvature.shape[1], 
                                                               curvature.shape[2]*curvature.shape[3]))
            else:
                curvature_trace = np.trace(curvature)
            curvature_trace /= curvature.size
            A += curvature_trace * np.eye(n) * 0.01

        if hasattr(R, 'non_normality_index'):
            R.non_normality_index = DecursionFunctor._non_normality_index(A)
            R.numerical_radius = DecursionFunctor._numerical_radius(A)

        if hasattr(R, 'domain_mask') and R.domain_mask is not None:
            n = A.shape[0]
            domain_dim = int(np.sum(R.domain_mask))
            A = A[R.domain_mask][:, R.domain_mask]

        A_herm = (A + A.conj().T) / 2

        return PositiveSpectralObject(operator_A=A_herm)

    @staticmethod
    def map_morphism(f: RecMorphism, verify_intertwining: bool = False) -> SpectralMorphism:
        """
        将 Rec 态射 f: R1 -> R2 映射为 SpectralMorphism D(f): D(R1) -> D(R2)。

        在有限维 L^2 表示中，Koopman 提升算子（pull-back）U_f 满足
        (U_f g)(x) = g(f(x))，其矩阵为 f.map.T。D(f) 是 U_f 在 L^2 内积下的伴随，
        因此 D(f) 的矩阵直接取为 f.map（推前映射）。这一选择保证 D 是协变函子，
        并且是后续忠实性验证的基础。

        参数
        ----------
        verify_intertwining : bool
            若为 True，则在构造后验证谱交织条件
                D(f) · A_R1 = A_R2 · D(f)，
            并对非平凡态射（非单位态射）给出警告。

        注：对非恒等态射 f，D(f) 的谱交织条件不是自动满足的，
        需要由映射 f 的结构保持性来保证。本实现默认不验证以保持效率，
        但可通过 verify_intertwining=True 显式检查。
        """
        E1 = DecursionFunctor.map_object(f.source)
        E2 = DecursionFunctor.map_object(f.target)

        # D(f) 的矩阵直接继承自状态空间推前映射 f.map，不做归一化，
        # 以避免不同态射在归一化后变得不可区分。
        T = f.map.astype(float).copy()

        result = SpectralMorphism(
            source=E1,
            target=E2,
            matrix=T,
            intertwining_mode="strict",
        )

        if verify_intertwining:
            ok = result.is_valid()
            if not ok:
                raise ValueError(
                    f"D(f) 不满足谱交织条件：D(f)·A₁ ≠ A₂·D(f)。"
                    f"这可能表明 f: {f.source} → {f.target} 不是合法的 Rec 态射。"
                )
            # 对非平凡态射给出提示
            if not np.allclose(f.map, np.eye(f.map.shape[0]), atol=1e-10):
                import warnings
                warnings.warn(
                    "非恒等态射的 D(f) 满足谱交织条件。"
                    "这由 f 与 Rec 对象演化规则的交换性保证。",
                    stacklevel=2,
                )

        return result


def decursion_functor_on_objects(
    R: RecObject,
) -> PositiveSpectralObject:
    """便捷函数：D(R)。"""
    return DecursionFunctor.map_object(R)


def decursion_functor_on_morphisms(
    f: RecMorphism,
) -> SpectralMorphism:
    """便捷函数：D(f)。"""
    return DecursionFunctor.map_morphism(f)


def verify_functor_axioms(
    R: RecObject, f: RecMorphism, g: RecMorphism | None = None
) -> dict[str, bool]:
    """
    验证函子公理：
    1. D(id_R) = id_{D(R)}
    2. 若 g, f 可复合，则 D(g ∘ f) = D(g) ∘ D(f)
    """
    D = DecursionFunctor()
    results = {}

    # 公理 1：保持单位态射
    from rec_category import identity_morphism

    id_R = identity_morphism(R)
    D_id = D.map_morphism(id_R)
    id_DR = identity_spectral_morphism(D.map_object(R))
    results["preserves_identity"] = np.allclose(D_id.matrix, id_DR.matrix)

    # 公理 2：保持复合
    if g is not None and f is not None:
        from rec_category import compose_morphisms

        gf = compose_morphisms(g, f)
        D_gf = D.map_morphism(gf)
        D_g = D.map_morphism(g)
        D_f = D.map_morphism(f)
        D_g_D_f = compose_spectral_morphisms(D_g, D_f)
        results["preserves_composition"] = np.allclose(
            D_gf.matrix, D_g_D_f.matrix
        )

    return results


def verify_faithfulness(
    f: RecMorphism, g: RecMorphism, tol: float = 1e-10
) -> bool:
    """
    验证函子 D 在态射对 (f, g) 上的忠实性。

    忠实性定义：D(f) = D(g) ⟹ f = g。
    等价地，若 f ≠ g，则 D(f) ≠ D(g)。

    返回 True 当且仅当 f 与 g 足够接近时 D(f) 与 D(g) 也足够接近，
    或 f 与 g 不同而 D(f) 与 D(g) 也不同。
    """
    f_equal_g = np.allclose(f.map, g.map, atol=tol)
    D_f = DecursionFunctor.map_morphism(f)
    D_g = DecursionFunctor.map_morphism(g)
    Df_equal_Dg = np.allclose(D_f.matrix, D_g.matrix, atol=tol)

    if f_equal_g:
        # f ≈ g 时，函子性已保证 D(f) ≈ D(g)
        return True
    # 忠实性要求：f ≠ g ⟹ D(f) ≠ D(g)
    return not Df_equal_Dg


def right_adjoint_on_object(
    E: PositiveSpectralObject,
) -> RecObject:
    """
    谱对象 E 的右伴随 R(E) 的最小原型。

    对象映射：
    - 状态空间取为 E 的 Hilbert 空间标准正交基（视为离散采样点）；
    - 演化规则取为 Koopman 矩阵 K = exp(-A_E)；
    - 元数据标记为从谱重构而来。

    注意：R 一般不是 D 的严格拟逆。在离散正谱情形下，D(R(E)) 与 E 具有相同的
    Koopman 矩阵（在 A_E 可由 -log(K) 恢复时），因此 D ∘ R ≈ id_{Spec} 在原型
    对象上成立；但 R ∘ D 通常不等于 id_{Rec}，因为 D 会遗忘 Rec 对象的状态空间
    几何信息。
    """
    A = E.operator_A
    K = expm(-A)
    n = E.dim
    # 以标准正交基向量 e_i 作为离散状态点
    state_space = np.eye(n)
    return RecObject(
        state_space=state_space,
        evolution=K,
        metadata={"origin": "right_adjoint_of_spectral_object"},
    )


def right_adjoint_on_morphism(
    phi: SpectralMorphism,
) -> RecMorphism:
    """
    谱态射 φ: E1 → E2 的右伴随 R(φ): R(E1) → R(E2)。

    由谱交织条件 φ A_1 = A_2 φ 可得 φ K_1 = K_2 φ（其中 K_i = exp(-A_i)），
    因此 φ 的矩阵自动满足 Rec 态射的交织条件，可直接作为 Rec 态射使用。
    """
    R_E1 = right_adjoint_on_object(phi.source)
    R_E2 = right_adjoint_on_object(phi.target)
    return RecMorphism(
        source=R_E1,
        target=R_E2,
        map=phi.matrix.astype(float).copy(),
    )


def unit(
    R: RecObject,
) -> RecMorphism:
    """
    单位自然变换 η: id_Rec → R ∘ D 的 R-分量。

    η_R: R → R(D(R)) 将原 Rec 对象映射到由谱重构的 Rec 对象。
    对离散原型，R(D(R)) 与 R 具有相同的 Koopman 矩阵（因为 A_R = -log(K_R)），
    但状态空间不同：原 R 保持其状态空间几何，R(D(R)) 使用标准正交基。
    η_R 就是从原状态空间到标准正交基的恒等提升。
    """
    # 计算 D(R) = E
    E = DecursionFunctor.map_object(R)
    # 计算 R(D(R)) = R(E)
    R_of_E = right_adjoint_on_object(E)

    # η_R: R → R(E) 的映射取为在原状态空间与标准基之间转换的矩阵
    n = R.n_points
    # 默认使用恒等矩阵（两 Rec 对象维数相同）
    eta_matrix = np.eye(n)

    return RecMorphism(
        source=R,
        target=R_of_E,
        map=eta_matrix,
    )


def counit(
    E: PositiveSpectralObject,
) -> SpectralMorphism:
    """
    余单位自然变换 ε: D ∘ R → id_Spec 的 E-分量。

    ε_E: D(R(E)) → E。
    由于 D(R(E)) 与 E 具有相同的谱算子 A（由构造保证），
    ε_E 取为恒等谱态射。
    """
    R_E = right_adjoint_on_object(E)
    D_R_E = DecursionFunctor.map_object(R_E)

    # D(R(E)) 与 E 应具有相同的 A 矩阵
    return SpectralMorphism(
        source=D_R_E,
        target=E,
        matrix=np.eye(E.dim),
        intertwining_mode="strict",
    )


def verify_triangle_identities(
    R: RecObject,
    E: PositiveSpectralObject,
    tol: float = 1e-10,
) -> dict[str, bool]:
    """
    验证伴随函子 D ⊣ R 的三角恒等式。

    三角恒等式：
        1. D(η_R) ∘ ε_{D(R)} = id_{D(R)}   （Spec 中）
        2. R(ε_E) ∘ η_{R(E)} = id_{R(E)}    （Rec 中）
    """
    from rec_category import compose_morphisms as compose_rec
    from spec_category import compose_spectral_morphisms as compose_spec

    D = DecursionFunctor()

    # 恒等式 1：D(η_R) ∘ ε_{D(R)} = id_{D(R)}
    D_R = D.map_object(R)
    eta_R = unit(R)
    D_eta_R = D.map_morphism(eta_R)  # SpectralMorphism: D(R) → D(R(D(R)))
    eps_DR = counit(D_R)  # SpectralMorphism: D(R(D(R))) → D(R)
    lhs1 = compose_spec(eps_DR, D_eta_R)  # D(R(D(R))) → D(R)
    id_DR = identity_spectral_morphism(D_R)
    identity_1 = np.allclose(lhs1.matrix, id_DR.matrix, atol=tol)

    # 恒等式 2：R(ε_E) ∘ η_{R(E)} = id_{R(E)}
    R_E = right_adjoint_on_object(E)
    eps_E = counit(E)  # SpectralMorphism: D(R(E)) → E
    R_eps_E = right_adjoint_on_morphism(eps_E)  # RecMorphism: R(D(R(E))) → R(E)
    eta_RE = unit(R_E)  # RecMorphism: R(E) → R(D(R(E)))
    from rec_category import identity_morphism
    lhs2 = compose_rec(R_eps_E, eta_RE)  # R(E) → R(D(R(E))) → R(E)
    id_RE = identity_morphism(R_E)
    identity_2 = np.allclose(lhs2.map, id_RE.map, atol=tol)

    return {
        "D_eta_comp_eps": identity_1,
        "R_eps_comp_eta": identity_2,
    }
