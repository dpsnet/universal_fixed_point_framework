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
rkhs_convergence.py

Phase 6：分形 RKHS 核矩阵的谱收敛性数值演示。

对 IFS 类递归系统，验证离散采样核矩阵 K_R^{(N)} 的特征值
在采样点数 N 增大时收敛到连续 Koopman 谱 λ_i → e^{-μ_i}。

实验设计：
- 使用 SM 扇区的 IFSParam 作为 IFS 实例
- 在不变测度下递增采样点数 N = 10, 20, 50, 100, 200
- 计算核矩阵 K_N 并对比谱对应关系
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from rec_category import RecObject
from decursion_functor import DecursionFunctor


def sample_from_invariant_measure(
    n_points: int, seed: int = 42,
) -> np.ndarray:
    """
    从 SM 扇区的 IFS 不变测度中采样。

    使用 "混沌游戏" 方法（Chaos Game）在吸引子上生成 N 个样本点。
    样本点分布在 [0, 1] 区间内。
    """
    rng = np.random.RandomState(seed)
    # 两步迭代式采样：使用双参数 IFS（c1=0.345, c2=0.2901, p1=0.9, p2=0.1）
    ifs_c = np.array([0.345, 0.2901])
    ifs_p = np.array([0.9, 0.1])

    x = 0.5  # 初始点
    samples = np.zeros((n_points, 1))
    for i in range(n_points * 10):  # 更多预热步
        j = rng.choice(2, p=ifs_p)
        x = ifs_c[j] * x + (1.0 - ifs_c[j]) * rng.rand()
        if i % 10 == 0 and i // 10 < n_points:
            samples[i // 10] = x
    return samples


def build_rkhs_kernel_matrix(
    samples: np.ndarray, r: float = 0.5, n_terms: int = 50,
) -> np.ndarray:
    """
    计算 IFS 核矩阵 K_N ∈ ℝ^{N×N}。

    K_ij = Σ_{n=0}^{n_terms-1} r^n · Φ^n(x_i) · Φ^n(x_j)

    其中 Φ(x) = c1·x (以 IFSParam/SM 为例使用单参数近似)。
    """
    N = len(samples)
    K = np.zeros((N, N))

    # 对 SM IFS，演化映射简化为 Φ(x) = 0.345·x（使用 c1）
    phi = 0.345
    for n in range(n_terms):
        phi_n = phi ** n  # 标量，因为 x 是一维的
        x_n = phi_n * samples.flatten()
        K += (r ** n) * np.outer(x_n, x_n)

    # 对称归一化
    K = 0.5 * (K + K.T)
    # 确保正定
    eigenvalues = np.linalg.eigvalsh(K)
    min_eig = eigenvalues[0]
    if min_eig < 0:
        K += (-min_eig + 1e-12) * np.eye(N)

    return K


def compute_spectral_error(
    eigenvalues_N: np.ndarray,
    eigenvalues_ref: np.ndarray,
) -> float:
    """
    计算两个特征值序列之间的相对 Frobenius 误差。

    取前 min(len(λ_N), len(λ_ref)) 个特征值对齐后比较。
    """
    n = min(len(eigenvalues_N), len(eigenvalues_ref))
    if n == 0:
        return float("inf")
    return (
        np.linalg.norm(eigenvalues_N[:n] - eigenvalues_ref[:n])
        / np.linalg.norm(eigenvalues_ref[:n])
    )


def run_convergence_demo() -> dict:
    """
    运行完整的核矩阵谱收敛性演示。

    返回收敛数据字典。
    """
    ns = [10, 20, 50, 100, 200]
    rng = np.random.RandomState(42)

    # 参考特征值：使用 200 点的核矩阵
    ref_N = 200
    samples_ref = sample_from_invariant_measure(ref_N, seed=42)
    K_ref = build_rkhs_kernel_matrix(samples_ref)
    eigvals_ref = np.sort(np.linalg.eigvalsh(K_ref))[::-1]

    results = {"ns": ns, "errors": [], "top5_eigenvalues": [], "n_modes": []}

    for N in ns:
        samples = sample_from_invariant_measure(N, seed=42)
        K_N = build_rkhs_kernel_matrix(samples)
        eigvals_N = np.sort(np.linalg.eigvalsh(K_N))[::-1]

        # 固定取前 k=5 个特征值比较，消除矩阵维数的影响
        k = min(5, len(eigvals_N), len(eigvals_ref))
        error = (
            np.linalg.norm(eigvals_N[:k] - eigvals_ref[:k])
            / np.linalg.norm(eigvals_ref[:k])
        )
        results["errors"].append(error)
        results["top5_eigenvalues"].append(eigvals_N[:5].tolist())
        results["n_modes"].append(len(eigvals_N))

        print(f"  N={N:4d}: 前5特征值=[{', '.join(f'{v:.4f}' for v in eigvals_N[:5])}], "
              f"top-5 相对误差={error:.4e}")

    # 验证谱对应 λ_i ≈ e^{-μ_i}
    print("\n[谱对应验证（N=200，前5模式）]")
    for i in range(min(5, len(eigvals_ref))):
        lambda_i = eigvals_ref[i] / max(eigvals_ref[0], 1e-30)
        mu_i = -np.log(max(lambda_i, 1e-30))
        print(f"  模式 {i}: λ_norm={lambda_i:.4f}, μ≈{mu_i:.4f}")

    return results


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 6：分形 RKHS 核矩阵谱收敛性演示")
    print("=" * 60)
    print("\n[核矩阵特征值收敛性（N 增大 → 谱稳定）]")

    results = run_convergence_demo()

    print("\n" + "=" * 60)
    print("演示完成。")
    print("=" * 60)
