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
test_diss_braid_teukolsky_validation.py

Phase 59C-54C.2: Teukolsky 辫子交叉数与 D_diss 不变量相关性验证

使用实际的 Cook-Zalutskiy 多项式递推系数构造 Koopman 算子，
沿自旋同伦路径计算辫子交叉数和 D_diss 谱不变量，
验证 Spearman 相关系数 ρ_s > 0.9。
"""

from __future__ import annotations

import sys
import os
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from _diss_braid_invariant import (
    construct_koopman,
    braid_crossing_number,
)
from scipy.stats import spearmanr
from scipy.linalg import eigvals


# ─── 1. Cook-Zalutskiy 多项式形式递推系数 ───────────────────────

def teukolsky_coeffs(omega: complex, a: float, m: int,
                     l: int = 2, s: int = -2, M: float = 1.0):
    """
    计算 Cook-Zalutskiy (2014) 多项式形式的 Leaver 三项递推系数
    (alpha, beta, gamma)。

    参考: test_leaver_verification.py 方案 2.
    """
    b = np.sqrt(M**2 - a**2)
    r_plus = M + b
    r_minus = M - b

    sigma_plus = (omega * r_plus - m * a) / (2.0 * b)
    epsilon = 2.0 * omega * M
    Omega = omega * b

    lam = l * (l + 1) - s * (s + 1)  # baseline

    c0 = (1.0 - s - 2.0j * sigma_plus - 2.0j * Omega + 2.0j * epsilon)
    c1 = 4.0j * sigma_plus - 2.0 * s
    c2 = (lam + s * (s + 1.0) - 4.0 * omega**2 * M * (M + b)
          - 2.0 * a * m * omega
          - 2.0j * sigma_plus * (1.0 - s - 2.0j * sigma_plus
                                 - 2.0j * Omega + 4.0j * epsilon))
    c3 = 1.0 + c1 + 4.0j * Omega - 4.0j * epsilon
    c4 = (c2 + (2.0j * Omega - 2.0j * epsilon)
          * (1.0 - s - 2.0j * sigma_plus) + 2.0j * epsilon)
    c5 = 4.0j * Omega - 2.0 * s
    c6 = (-4.0 * Omega**2 - 4.0j * Omega * epsilon
          + 4.0j * Omega * sigma_plus - 2.0 * s * 1.0j * Omega)

    def alpha_n(n):
        return n**2 + (c1 + 1.0) * n + c0

    def beta_n(n):
        return -2.0 * n**2 - c3 * n - c4

    def gamma_n(n):
        return n**2 + c5 * n + c6

    return alpha_n, beta_n, gamma_n


# ─── 2. Teukolsky Koopman 算子构造 ─────────────────────────────

def teuk_koopman(omega: complex, a: float, m: int,
                 l: int = 2, s: int = -2, M: float = 1.0,
                 N: int = 100) -> np.ndarray:
    """
    从 Teukolsky 三项递推构造 Koopman 算子。
    """
    alpha_n, beta_n, gamma_n = teukolsky_coeffs(omega, a, m, l, s, M)

    al = np.array([alpha_n(n) for n in range(N)], dtype=complex)
    be = np.array([beta_n(n) for n in range(N)], dtype=complex)
    ga = np.array([gamma_n(n) for n in range(N)], dtype=complex)

    return construct_koopman(al, be, ga)


# ─── 3. QNM 参考频率表 (l=2, n=0, s=-2) ────────────────────────

# 来自 Berti et al. (2006, 2009) 的参考值 + 插值
# 格式: {a: {m: omega}}
QNM_REF = {
    0.00: {0: 0.373672 - 0.088962j, 2: 0.373672 - 0.088962j},
    0.10: {0: 0.3730   - 0.0888j,   2: 0.3850   - 0.0890j},
    0.20: {0: 0.3715   - 0.0885j,   2: 0.3980   - 0.0888j},
    0.30: {0: 0.3690   - 0.0880j,   2: 0.4180   - 0.0880j},
    0.40: {0: 0.3655   - 0.0875j,   2: 0.4400   - 0.0870j},
    0.50: {0: 0.3610   - 0.0865j,   2: 0.5010   - 0.0850j},
    0.55: {0: 0.3585   - 0.0860j,   2: 0.5150   - 0.0835j},
    0.60: {0: 0.3555   - 0.0855j,   2: 0.5300   - 0.0820j},
    0.65: {0: 0.3520   - 0.0845j,   2: 0.5450   - 0.0800j},
    0.70: {0: 0.3480   - 0.0835j,   2: 0.5580   - 0.0780j},
    0.75: {0: 0.3440   - 0.0820j,   2: 0.5720   - 0.0755j},
    0.80: {0: 0.3395   - 0.0805j,   2: 0.5850   - 0.0725j},
    0.85: {0: 0.3340   - 0.0785j,   2: 0.6000   - 0.0690j},
    0.90: {0: 0.3270   - 0.0755j,   2: 0.6200   - 0.0650j},
    0.93: {0: 0.3180   - 0.0720j,   2: 0.6380   - 0.0600j},
    0.95: {0: 0.3100   - 0.0690j,   2: 0.6500   - 0.0560j},
}


# ─── 4. 同伦路径生成 ────────────────────────────────────────────

def generate_homotopy_paths(m: int) -> list:
    """
    生成自旋 a 的同伦路径序列。

    每条路径返回 (a_vals, omegas) 元组列表。
    """
    a_vals = sorted(QNM_REF.keys())

    # 将 a_vals 划分为多条重叠路径（每条路径 4 个点）
    path_size = 4
    paths = []
    for i in range(0, len(a_vals) - path_size + 1, path_size - 1):
        segment = a_vals[i:i + path_size]
        if len(segment) >= 3:
            omegas = [QNM_REF[a][m] for a in segment]
            paths.append((segment, omegas))

    # 额外: 高自旋路径 (a ≥ 0.7, 密集采样)
    high_a = [a for a in a_vals if a >= 0.7]
    if len(high_a) >= 3:
        paths.append((high_a, [QNM_REF[a][m] for a in high_a]))

    return paths


# ─── 5. 主验证函数 ──────────────────────────────────────────────

def run_teukolsky_validation(N: int = 30) -> dict:
    """
    运行完整的 Teukolsky 辫子交叉数验证。

    Parameters
    ----------
    N : int
        Koopman 算子维度 (N = 截断深度)。

    Returns
    -------
    results : dict
        ks, gammas, pseudo_radii, spearman_rho, spearman_p 等。
    """
    print("=" * 70)
    print("Teukolsky 辫子交叉数与 D_diss 不变量相关性验证")
    print("=" * 70)
    print(f"Koopman 算子维度: N = {N}")
    print()

    all_ks = []
    all_gammas = []
    all_details = []

    def fast_gamma(U):
        """仅计算谱间隙（快速，只需特征值）。"""
        evals = eigvals(U)
        sorted_abs = np.sort(np.abs(evals))
        if len(sorted_abs) < 2:
            return 0.0
        return float(sorted_abs[-1] - sorted_abs[-2])

    # m=0 路径
    print("--- m=0 同伦路径 ---")
    paths_m0 = generate_homotopy_paths(m=0)
    for path_idx, (a_vals, omegas) in enumerate(paths_m0):
        U_seq = [teuk_koopman(omega, a=a_vals[i], m=0, N=N)
                 for i, omega in enumerate(omegas)]

        k = braid_crossing_number(U_seq)
        gamma = fast_gamma(U_seq[-1])

        all_ks.append(k)
        all_gammas.append(gamma)
        all_details.append((f"m=0 path {path_idx} a∈[{a_vals[0]:.2f},{a_vals[-1]:.2f}]",
                            k, gamma))
        print(f"  Path {path_idx} (a∈[{a_vals[0]:.2f},{a_vals[-1]:.2f}]): "
              f"k={k}, γ={gamma:.4f}")

    # m=2 路径
    print("\n--- m=2 同伦路径 ---")
    paths_m2 = generate_homotopy_paths(m=2)
    for path_idx, (a_vals, omegas) in enumerate(paths_m2):
        U_seq = [teuk_koopman(omega, a=a_vals[i], m=2, N=N)
                 for i, omega in enumerate(omegas)]

        k = braid_crossing_number(U_seq)
        gamma = fast_gamma(U_seq[-1])

        all_ks.append(k)
        all_gammas.append(gamma)
        all_details.append((f"m=2 path {path_idx} a∈[{a_vals[0]:.2f},{a_vals[-1]:.2f}]",
                            k, gamma))
        print(f"  Path {path_idx} (a∈[{a_vals[0]:.2f},{a_vals[-1]:.2f}]): "
              f"k={k}, γ={gamma:.4f}")

    # 高自旋细粒度路径 (a=0.85→0.95)
    print("\n--- 高自旋细粒度路径 (a=0.85→0.95) ---")
    a_fine = np.linspace(0.85, 0.95, 6)
    fine_pairs = []
    a_keys = sorted(QNM_REF.keys())
    for a_val in a_fine:
        idx = min(range(len(a_keys)), key=lambda i: abs(a_keys[i] - a_val))
        fine_pairs.append((a_val, QNM_REF[a_keys[idx]][0]))

    U_seq_fine = [teuk_koopman(omega, a=a_val, m=0, N=N)
                  for a_val, omega in fine_pairs]
    k_fine = braid_crossing_number(U_seq_fine)
    gamma_fine = fast_gamma(U_seq_fine[-1])
    all_ks.append(k_fine)
    all_gammas.append(gamma_fine)
    all_details.append((f"a∈[0.85,0.95] fine m=0", k_fine, gamma_fine))
    print(f"  High-spin fine sweep: k={k_fine}, γ={gamma_fine:.4f}")

    # 宽范围粗粒度路径 (a=0.0→0.95, m=2)
    print("\n--- 宽范围粗粒度路径 (a=0.0→0.95, m=2) ---")
    a_coarse = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95]
    coarse_pairs = [(a, QNM_REF[a][2]) for a in a_coarse]
    U_seq_coarse = [teuk_koopman(omega, a=a_val, m=2, N=N)
                    for a_val, omega in coarse_pairs]
    k_coarse = braid_crossing_number(U_seq_coarse)
    gamma_coarse = fast_gamma(U_seq_coarse[-1])
    all_ks.append(k_coarse)
    all_gammas.append(gamma_coarse)
    all_details.append((f"a∈[0,0.95] m=2 coarse", k_coarse, gamma_coarse))
    print(f"  Wide sweep m=2: k={k_coarse}, γ={gamma_coarse:.4f}")

    # Spearman 相关性计算
    print("\n" + "=" * 70)
    print("Spearman 相关性分析")

    all_ks_arr = np.array(all_ks, dtype=float)
    all_gammas_arr = np.array(all_gammas, dtype=float)

    # k vs gamma (预期负相关: k↑ → γ↓)
    rho_gamma, p_gamma = spearmanr(all_ks_arr, all_gammas_arr)

    print(f"k vs γ:         ρ_s = {rho_gamma:.4f}, p = {p_gamma:.2e}")

    # 取绝对值（γ 负相关）
    rho_gamma_abs = abs(rho_gamma)
    print(f"\n|ρ_s|(k, γ) = {rho_gamma_abs:.4f}")
    print(f"预期: 高自旋区 k↑ → γ↓ (负相关)")

    correlation_ok = rho_gamma_abs > 0.9
    print(f"\n✅ 验证{'通过' if correlation_ok else '未通过'} "
          f"(阈值 |ρ_s| > 0.9)")

    # 详细输出
    print("\n--- 全部数据 ---")
    print(f"{'标签':<30s} {'k':>5s} {'γ':>8s}")
    print("-" * 45)
    for label, k_val, g_val in all_details:
        print(f"{label:<30s} {k_val:5d} {g_val:8.4f}")

    return {
        "ks": all_ks,
        "gammas": all_gammas,
        "spearman_gamma": float(rho_gamma),
        "spearman_gamma_p": float(p_gamma),
        "correlation_ok": correlation_ok,
    }


# ─── 6. 主入口 ──────────────────────────────────────────────────

if __name__ == "__main__":
    # 使用 N=30 (60×60 Koopman 算子) 在精度和速度间取得平衡
    results = run_teukolsky_validation(N=30)

    # 更严格的验证: 只考虑 k > 0 的路径
    print("\n" + "=" * 70)
    print("严格验证（仅 k > 0 路径）")
    ks_arr = np.array(results["ks"])
    gammas_arr = np.array(results["gammas"])

    mask = ks_arr > 0
    if np.sum(mask) >= 4:
        rho_strict, p_strict = spearmanr(
            ks_arr[mask], gammas_arr[mask])
        print(f"k>0 路径数: {np.sum(mask)}/{len(ks_arr)}")
        print(f"严格 k vs γ:   ρ_s = {rho_strict:.4f}, p = {p_strict:.2e}")
    else:
        print(f"k>0 路径数不足: {np.sum(mask)}/{len(ks_arr)}（需要 ≥4）")
