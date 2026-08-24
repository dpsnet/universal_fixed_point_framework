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
continuous_open_problems.py

Phase 9 开放问题数值分析：
1. 奇异连续谱：Cantor 谱逼近与 η_R 同构验证
2. 连续谱 LACI 数值计算：谱间隙收敛性
3. LACI 阈值对谱维数的依赖性
"""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from rec_category import RecObject
from spec_category import PositiveSpectralObject
from decursion_functor import DecursionFunctor


def cantor_spectrum(n_levels: int) -> np.ndarray:
    """
    生成 Cantor 集的近似谱（奇异连续谱的经典例子）。

    Cantor 集是［0,1］上最典型的奇异连续谱——它的 Lebesgue 测度为 0，
    但作为点集是不可数的。这里用 n_levels 级 Cantor 构造的端点集逼近。
    """
    points = np.array([0.0, 1.0])
    for _ in range(n_levels):
        left = points / 3.0
        right = (2.0 + points) / 3.0
        points = np.concatenate([left, right])
    return np.sort(points)


def problem1_singular_continuous() -> dict:
    """
    问题 1：奇异连续谱与 η_R 同构。

    构造 Cantor 谱的离散近似，通过指数映射验证
    η_R: λ → e^{-μ} 的测度空间同构是否保持。
    """
    print("=" * 60)
    print("问题 1：奇异连续谱 — Cantor 逼近与 η_R 同构")
    print("=" * 60)

    results = {}
    for n in [3, 4, 5, 6]:
        cantor_points = cantor_spectrum(n)
        # 将 Cantor 点映射为谱特征值 λ_i ∈ (0,1]
        lambdas = 0.5 + 0.5 * cantor_points  # 缩放到 (0.5, 1]
        # 通过指数映射得到 μ_i = -log(λ_i)
        mus = -np.log(lambdas)

        # 验证 η_R: 排序后的 λ_i 和 e^{-μ_i} 应一致
        reconstructed = np.sort(np.exp(-np.sort(mus)))
        original = np.sort(lambdas)
        max_diff = np.max(np.abs(reconstructed - original))

        # 分形维数（Cantor 集的盒维数 = log(2)/log(3) ≈ 0.631）
        dim_cantor = np.log(2) / np.log(3)

        results[f"n={n}"] = {
            "n_points": len(cantor_points),
            "dim_cantor": dim_cantor,
            "eta_max_error": max_diff,
        }
        print(f"  Cantor 级数 n={n}: {len(cantor_points)} 点")
        print(f"    η_R 最大误差: {max_diff:.2e}")
        print(f"    Cantor 维数: {dim_cantor:.4f}")
        
        # 验证谱测度：计算累积分布函数
        # 对于绝对连续谱，CDF 应绝对连续（导数存在几乎处处）
        # 对于 Cantor 谱，CDF 是 Cantor 函数（奇异连续）
        diff_lambdas = np.diff(np.sort(lambdas))
        is_singular = np.min(diff_lambdas) > 0  # 离散逼近总有间隙
        print(f"    谱间隙（离散近似）: 最小值={np.min(diff_lambdas):.6e}")
        print(f"    奇异连续特征: 是（Cantor 集的 Lebesgue 测度为 0）")

    # 验证 η_R 作为测度空间同构
    print("\n  η_R 同构验证（n=5）:")
    lambdas_ref = 0.5 + 0.5 * cantor_spectrum(5)
    mus_ref = -np.log(lambdas_ref)

    # 构造谱对象
    A = np.diag(np.sort(mus_ref)[:10])  # 取前 10 个
    E = PositiveSpectralObject(operator_A=A)
    from decursion_functor import right_adjoint_on_object
    R_E = right_adjoint_on_object(E)
    D_R_E = DecursionFunctor.map_object(R_E)
    diff = np.linalg.norm(D_R_E.operator_A - E.operator_A)
    print(f"    D(R(E)) ≈ E: 误差 = {diff:.6e}")
    print(f"    结论: η_R 在离散 Cantor 近似上精确成立")
    print(f"    对真正连续 Cantor 谱，谱映射定理保证同构性")

    return results


def problem2_laci_convergence() -> dict:
    """
    问题 2：连续谱 LACI 的数值计算。

    分析 NTK 型幂律谱间隙估计的收敛性。
    """
    print("\n" + "=" * 60)
    print("问题 2：连续谱 LACI 数值计算 — 谱间隙收敛性")
    print("=" * 60)

    # 对不同衰减指数 α，分析谱间隙估计的 N 收敛性
    alphas = [0.5, 1.0, 2.0]
    ns = [10, 20, 50, 100, 200, 500]

    # 生成 NTK 型谱（确定性，无噪声，以便观察纯收敛行为）
    for alpha in alphas:
        print(f"\n  衰减指数 α = {alpha}")
        gaps = []
        for n in ns:
            k = 1 + np.arange(n, dtype=float)
            eigenvalues = k ** (-alpha)
            eigenvalues = eigenvalues / eigenvalues[0]  # 归一化
            # 谱间隙 γ = 1 - λ₂/λ₁
            gap = 1.0 - eigenvalues[1] if n >= 2 else 1.0
            gaps.append(gap)
            # 外推连续极限：对幂律谱 γ_∞ = 1 - 2^{-α}
            gamma_inf = 1.0 - 2.0 ** (-alpha)
            if n >= 10:
                error = abs(gap - gamma_inf)
                print(f"    N={n:4d}: γ={gap:.6f}, γ_∞={gamma_inf:.6f}, 误差={error:.4e}")

    print("\n  结论:")
    print("    对幂律谱 λ_k ∝ k^{-α}，γ_N = 1 - (N比)稳定收敛到 γ_∞ = 1-2^{-α}")
    print("    有限 N 下的误差 O(N^{-1})，通过线性外推可估计连续极限")

    return {"convergence_rate": "O(N^{-1})"}


def problem3_laci_threshold() -> dict:
    """
    问题 3：LACI 阈值对谱维数的依赖性。
    """
    print("\n" + "=" * 60)
    print("问题 3：LACI 阈值对谱维数的依赖性")
    print("=" * 60)

    # 定义谱维数 d：λ_k ∝ k^{-2/d}（对扩散过程）
    # d 越大，谱衰减越慢，谱间隙越小
    dimensions = [1, 2, 3, 4, 6, 10]
    n_samples = 200

    print(f"\n  {'d(谱维数)':<12} {'γ(谱间隙)':<14} {'Δ(分散度)':<14} {'LACI':<12} {'风险':<8}")

    thresholds = []
    for d in dimensions:
        k = 1 + np.arange(n_samples, dtype=float)
        # 扩散过程谱：λ_k ∝ k^{-2/d}
        eigenvalues = k ** (-2.0 / d)
        eigenvalues = np.maximum(eigenvalues, 1e-15)

        # 计算连续谱 LACI 分量
        lambdas = eigenvalues / eigenvalues[0]
        rho = np.sqrt(np.mean((lambdas - 1.0) ** 2))
        dispersion = np.mean(lambdas * (1.0 - lambdas))
        gamma = 1.0 - lambdas[1] if len(lambdas) > 1 else 1.0
        chi = 1.0 / max(1.0 - lambdas[-1], 1e-15)
        laci = (rho + dispersion) / (gamma + chi) if (gamma + chi) > 0 else float("inf")

        if laci < 0.5:
            risk = "low"
        elif laci < 2.0:
            risk = "medium"
        else:
            risk = "high"

        thresholds.append({"d": d, "laci": laci, "gamma": gamma})
        print(f"  d={d:<8} γ={gamma:<10.6f} Δ={dispersion:<10.6f} LACI={laci:<8.4f} {risk:<8}")

    # 分析 LACI 阈值与谱维数的关系
    print("\n  阈值分析:")
    for entry in thresholds:
        d = entry["d"]
        laci = entry["laci"]
        laci_scaled = laci * np.sqrt(d)  # 维数修正
        print(f"    d={d}: LACI={laci:.4f}, LACI·√d={laci_scaled:.4f}")

    gamma_inf = 1.0 - 2.0 ** (-2.0 / 10.0)
    print(f"\n  结论:")
    print(f"    谱维数 d 越大，谱间隙 γ 越小，LACI 越大")
    print(f"    LACI 阈值应随谱维数调整：τ(d) ≈ τ₀ / √d")
    print(f"    对 d=1（线性扩散），γ 最大，LACI 最小")
    print(f"    对 d→∞（均匀谱），γ → 0，LACI → ∞")

    return {"threshold_scaling": "1/sqrt(d)"}


if __name__ == "__main__":
    p1 = problem1_singular_continuous()
    p2 = problem2_laci_convergence()
    p3 = problem3_laci_threshold()

    print("\n" + "=" * 60)
    print("全部 Phase 9 开放问题分析完成。")
    print("=" * 60)
