"""
ar_positivity_test.py

Phase 7：非正规 Koopman 算子的对数生成元 A_R 的正性数值验证。

对自伴与非对称 Koopman 矩阵分别验证：
1. A_R = -log(K_R) 的正性 / 增生性
2. 谱对应 λ_i = exp(-μ_i)
3. 零模截断处理
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
from scipy.linalg import logm, expm

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from rec_category import RecObject
from spec_category import PositiveSpectralObject
from decursion_functor import DecursionFunctor


def test_self_adjoint_koopman():
    """自伴对称转移矩阵的 A_R 正性。"""
    K = np.array([[0.9, 0.1], [0.1, 0.9]])
    A = -logm(K)
    eigenvalues = np.linalg.eigvalsh(A)
    is_positive = np.all(eigenvalues >= -1e-10)
    print(f"  特征值: {eigenvalues}")
    print(f"  正性: {is_positive}")
    # 验证谱对应
    lambdas = np.linalg.eigvalsh(K)
    mu_from_K = -np.log(np.maximum(lambdas, 1e-30))
    print(f"  λ_i={np.round(lambdas, 6)}, -log(λ_i)={np.round(mu_from_K, 6)}")
    assert is_positive
    assert np.allclose(np.sort(eigenvalues), np.sort(mu_from_K), atol=1e-10)
    print("  通过")


def test_non_symmetric_koopman():
    """非对称转移矩阵的 A_R 增生性。"""
    K = np.array([[0.9, 0.1, 0.0],
                  [0.0, 0.8, 0.2],
                  [0.0, 0.0, 0.7]])  # 上三角
    A = -logm(K)
    # 增生性：A + A^* 正半定（对有限维算子）
    accretive_check = np.all(np.linalg.eigvalsh(A + A.T) >= -1e-10)
    # 谱对应
    lambdas = np.sort(np.linalg.eigvals(K))[::-1]
    mu_from_K = -np.log(np.maximum(np.real(lambdas), 1e-30))
    eigenvalues_A = np.sort(np.linalg.eigvals(A))
    print(f"  A 的特征值: {np.round(eigenvalues_A, 6)}")
    print(f"  -log(λ_i)  : {np.round(np.sort(mu_from_K), 6)}")
    print(f"  增生性 (A+A*>=0): {accretive_check}")
    assert accretive_check
    assert np.allclose(np.sort(np.real(eigenvalues_A)), np.sort(mu_from_K), atol=1e-8)
    print("  通过")


def test_jordan_block_koopman():
    """Jordan 块的 A_R（非对角化：谱对应成立但可能非增生）"""
    K = np.array([[0.8, 1.0],
                  [0.0, 0.8]])  # Jordan 块
    A = -logm(K)
    eigenvalues = np.linalg.eigvals(A)
    accretive = np.all(np.linalg.eigvalsh(A + A.T) >= -1e-10)
    print(f"  A 的特征值: {np.round(eigenvalues, 6)}")
    print(f"  A+A^* 正半定: {accretive}（非对角化矩阵不保证增生性）")
    # Jordan 块下谱对应依然成立：特征值 λ=0.8 给出 μ=-log(0.8)≈0.223
    mu_expected = -np.log(0.8)
    print(f"  期望 μ = -log(0.8) = {mu_expected:.6f}")
    assert abs(eigenvalues[0] - mu_expected) < 1e-6
    # Jordan 块不保证增生性（非正规），只验证谱对应
    print("  (谱对应成立，增生性不保证 — Phase 7 开放问题)")
    print("  通过")


def test_zero_mode_truncation():
    """零模截断处理。"""
    K = np.array([[1.0, 0.0],
                  [0.0, 0.5]])  # 零模：特征值 1
    epsilon = 1e-10
    A = -logm(K + epsilon * np.eye(2))
    eigenvalues = np.linalg.eigvalsh(A)
    # 含零模时最小特征值应为 -log(1+ε) ≈ -ε（小负值，随 ε→0 趋近于 0）
    min_eig = eigenvalues[0]
    negativity_artifact = abs(min(min_eig, 0))
    print(f"  A 的特征值（ε={epsilon:.0e}）: {np.round(eigenvalues, 6)}")
    print(f"  负值伪迹: {negativity_artifact:.2e}（ε={epsilon:.0e} 量级，可接受）")
    # 验证恢复关系（这是更重要的性质）
    U_recovered = expm(-A)
    K_plus_eps = K + epsilon * np.eye(2)
    print(f"  exp(-A) ≈ K+εI: {np.allclose(U_recovered, K_plus_eps, atol=1e-6)}")
    assert negativity_artifact < 10 * epsilon, f"负值伪迹过大: {negativity_artifact:.2e}"
    assert np.allclose(U_recovered, K_plus_eps, atol=1e-6)
    print("  通过")


def test_rec_object_roundtrip_non_symmetric():
    """非对称 Koopman 的 RecObject → Spec 往返。"""
    K = np.array([[0.8, 0.2],
                  [0.1, 0.7]])  # 非对称
    R = RecObject(state_space=np.eye(2), evolution=K)
    # 对称化处理已在 D 函子中实现
    spec = DecursionFunctor.map_object(R)
    A = spec.operator_A
    is_positive = np.all(np.linalg.eigvalsh(A) >= -1e-10)
    print(f"  D(R).A 正性: {is_positive}")
    print(f"  D(R).A 特征值: {np.diag(A)}")
    assert is_positive
    print("  通过")


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 7：非正规 Koopman 算子 A_R 正性验证")
    print("=" * 60)

    print("\n[测试 1] 自伴对称转移矩阵")
    test_self_adjoint_koopman()

    print("\n[测试 2] 非对称转移矩阵")
    test_non_symmetric_koopman()

    print("\n[测试 3] Jordan 块")
    test_jordan_block_koopman()

    print("\n[测试 4] 零模截断")
    test_zero_mode_truncation()

    print("\n[测试 5] RecObject 往返（非对称）")
    test_rec_object_roundtrip_non_symmetric()

    print("\n" + "=" * 60)
    print("全部测试通过。")
    print("=" * 60)
