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
example_ifs.py

最小测试用例：将一维 IFS 表示为 Rec 对象，
应用谱去递归化函子 D 得到 Spec 对象，并验证 λ_i = exp(-μ_i) 的谱对应关系。

本测试采用对角 Koopman 矩阵，使谱对应在数值上精确成立。
"""

import numpy as np
from rec_category import RecObject, RecMorphism, identity_morphism
from spec_category import identity_spectral_morphism
from decursion_functor import DecursionFunctor
from fixed_point_solver import FixedPointSolver


def build_diagonal_ifs(n: int = 3, base: float = 0.8) -> RecObject:
    """
    构造一个对角 IFS：状态空间为 {0, 1, ..., n-1}，
    Koopman 矩阵为对角阵 K = diag(1, c, c^2, ..., c^{n-1})。

    该矩阵对应一个理想化的自相似系统：每个点是独立压缩的，
    压缩率按几何级数递减。最大特征值 1 对应不变测度。
    """
    state_space = np.arange(n).reshape(-1, 1).astype(float)
    eigenvalues = np.array([base ** i for i in range(n)])
    K = np.diag(eigenvalues)
    return RecObject(
        state_space=state_space,
        evolution=K,
        time_semigroup="N",
        metadata={
            "type": "IFS",
            "description": "diagonal contraction system",
            "base": base,
        },
    )


def main():
    print("=" * 60)
    print("最小测试：IFS -> 谱去递归化 -> 谱对象")
    print("=" * 60)

    # 1. 构造 Rec 对象
    R = build_diagonal_ifs(n=3, base=0.8)
    print(f"\n[Rec 对象] 状态空间: {R.state_space.flatten()}")
    print(f"[Rec 对象] Koopman 矩阵 K_R:\n{R.koopman_matrix()}")

    # 2. 应用谱去递归化函子 D
    D = DecursionFunctor()
    E = D(R)
    print(f"\n[Spec 对象] 维数: {E.dim}")
    print(f"[Spec 对象] 谱算子 A_R = -log(K_R):\n{E.operator_A}")
    print(f"[Spec 对象] 谱 σ(A_R): {E.spectrum}")

    # 3. 验证 λ_i = exp(-μ_i)
    mu = E.spectrum
    lambdas_from_exp = np.sort(np.exp(-mu))
    koopman_eigenvalues = np.sort(np.linalg.eigvalsh(R.koopman_matrix()))
    print(f"\n[谱对应验证]")
    print(f"  A_R 的特征值 μ_i        : {mu}")
    print(f"  exp(-μ_i)（排序后）     : {lambdas_from_exp}")
    print(f"  K_R 的特征值 λ_i（排序）: {koopman_eigenvalues}")
    diff = np.linalg.norm(lambdas_from_exp - koopman_eigenvalues)
    print(f"  差异 (Frobenius 范数)   : {diff:.2e}")
    assert diff < 1e-10, "谱对应 λ_i = exp(-μ_i) 未通过"

    # 4. 验证函子公理：D(id_R) = id_{D(R)}
    id_R = identity_morphism(R)
    D_id = D.map_morphism(id_R)
    id_E = identity_spectral_morphism(E)
    preserves_identity = np.allclose(D_id.matrix, id_E.matrix)
    print(f"\n[函子公理验证]")
    print(f"  D(id_R) == id_D(R)      : {preserves_identity}")
    assert preserves_identity, "函子未保持单位态射"

    # 5. 用不动点求解器验证 Hutchinson 不变测度
    print(f"\n[Hutchinson 不变测度]")
    K = R.koopman_matrix()
    result_mu = FixedPointSolver.solve_hutchinson_measure(
        K=K,
        mu0=np.ones(R.n_points) / R.n_points,
        tol=1e-12,
    )
    mu = result_mu.fixed_point
    print(f"  不动点测度 μ            : {mu}")
    print(f"  收敛                    : {result_mu.converged}")
    print(f"  迭代次数                : {result_mu.iterations}")
    print(f"  验证 K @ μ ≈ μ 误差     : {np.linalg.norm(K @ mu - mu):.2e}")
    assert result_mu.converged, "Hutchinson 测度未收敛"
    assert np.allclose(K @ mu, mu, atol=1e-10)
    assert mu[0] > 0.99, "不动点测度未集中在主吸引子"

    print("\n" + "=" * 60)
    print("所有断言通过。测试完成。")
    print("=" * 60)


if __name__ == "__main__":
    main()
