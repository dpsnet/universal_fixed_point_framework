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

#!/usr/bin/env python3
"""
compute_cross_spin_scaling.py —— 跨自旋 III 型奇异纤维标度指数计算（v2.0）

方法：使用径向三对角矩阵条件数。

核心思路
--------
III 型奇异纤维在 a→1（极值 Kerr 极限）时出现，表现为径向三对角矩阵 M(ω) 
在某 QNM 频率 ω 处变得奇异（谱间隙闭合）。因此：

    条件数 κ(M(ω)) = ‖M‖·‖M⁻¹‖ → ∞  as  a → 1

定义谱间隙指示量 γ(a) = 1/κ(M(ω(a)))，其三体标度规律为：

    γ(a) ∝ (1-a)^β

本工具通过以下步骤计算跨自旋标度指数 β_G、β_EM、β_D：

1. 对每个自旋 s ∈ {-2, -1, -0.5} 和每个 a，构建径向三对角矩阵 M(ω)
2. 使用已知参考数据或扫描近似得到 ω(a)
3. 计算条件数 κ(M) = s_max/s_min（由 SVD 得到）
4. 对数-对数拟合 β

参考
----
- Cook & Zalutskiy (2014) Phys. Rev. D 90, 124021
- Berti, Cardoso, Starinets (2009) Class. Quant. Grav. 26, 163001
- Paper XXVII §12（电磁谱丛）、Paper XXIX §5（Dirac 跨自旋对比）
"""

from __future__ import annotations

import sys
import os
import numpy as np
from scipy.linalg import svd, eigvals
from scipy.interpolate import interp1d

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _spin_weight_coeff import (
    frobenius_index,
    alpha_n, beta_n, gamma_n,
    recurrence_coeffs,
    build_tridiagonal_matrix,
    approx_spheroidal_eigenvalue,
)


# ============================================================
# 1. ω(a) 参考数据与插值
# ============================================================

# Cook-Zalutskiy 自洽参考表（s=-2, l=2, m=2, 全自旋追踪）
GRAV_OMEGA_REF = {
    0.00: complex(0.373672, -0.088962),
    0.50: complex(0.464123, -0.085639),
    0.70: complex(0.532600, -0.080793),
    0.90: complex(0.671614, -0.064869),
    0.99: complex(0.870893, -0.029390),
}

# 电磁 s=-1, l=2, m=2 近似 QNM 频率（来自文献近似/推算）
EM_OMEGA_REF = {
    0.00: complex(0.3530, -0.0950),   # Schwarzschild 极限近似
    0.50: complex(0.4400, -0.0910),
    0.70: complex(0.5070, -0.0860),
    0.90: complex(0.6400, -0.0690),
    0.99: complex(0.8500, -0.0310),
}

# Dirac s=-0.5, l=2, m=2 近似 QNM 频率
DIRAC_OMEGA_REF = {
    0.00: complex(0.3420, -0.0970),   # Schwarzschild 极限近似
    0.50: complex(0.4270, -0.0930),
    0.70: complex(0.4930, -0.0880),
    0.90: complex(0.6250, -0.0710),
    0.99: complex(0.8400, -0.0320),
}


def build_omega_interpolator(ref_data: dict) -> callable:
    """从参考数据构建 ω(a) 的线性插值函数。"""
    a_vals = sorted(ref_data.keys())
    re_vals = [ref_data[a].real for a in a_vals]
    im_vals = [ref_data[a].imag for a in a_vals]
    
    re_interp = interp1d(a_vals, re_vals, kind='cubic', fill_value='extrapolate')
    im_interp = interp1d(a_vals, im_vals, kind='cubic', fill_value='extrapolate')
    
    def omega_of_a(a: float) -> complex:
        return complex(float(re_interp(a)), float(im_interp(a)))
    
    return omega_of_a


# 构建各自旋的 ω(a) 插值器
_omega_interp_G = build_omega_interpolator(GRAV_OMEGA_REF)
_omega_interp_EM = build_omega_interpolator(EM_OMEGA_REF)
_omega_interp_D = build_omega_interpolator(DIRAC_OMEGA_REF)


def get_omega_approx(s: float, a: float) -> complex:
    """获取给定自旋 s 在自旋 a 处的近似 QNM 频率 ω(a)。"""
    if s == -2:
        return _omega_interp_G(a)
    elif s == -1:
        return _omega_interp_EM(a)
    elif abs(s - (-0.5)) < 1e-10:
        return _omega_interp_D(a)
    else:
        raise ValueError(f"未知自旋 s={s}")


# ============================================================
# 2. 三对角矩阵谱近距指示量（最小奇异值）
# ============================================================

def min_singular_value(M: np.ndarray) -> float:
    """
    计算矩阵的最小奇异值 σ_min。
    
    σ_min → 0 意味着矩阵接近奇异（III 型奇异纤维）。
    该指标比条件数更鲁棒，因为 σ_max 的变化不会影响指示。
    """
    try:
        s = svd(M, compute_uv=False)
        valid = s[s > 1e-300]
        if len(valid) == 0:
            return 0.0
        return float(valid[-1])
    except Exception:
        return 0.0


def build_shifted_tridiagonal(s: float, N: int, omega: complex, lam: complex,
                              a: float, m: int, M_mass: float = 1.0,
                              n_start: int = 0) -> np.ndarray:
    """
    构建跳过前 n_start 项的修整三对角矩阵。
    
    对 s=-2，α₁=0 和 α₃=0 导致标准三对角矩阵具有块分离结构。
    跳过前 n_start=4 项可避开所有零超对角元素，获得良态矩阵。
    
    n_start=0 时等同于 build_tridiagonal_matrix。
    """
    if n_start == 0:
        return build_tridiagonal_matrix(s, N, omega, lam, a, m, M_mass)
    
    N_eff = N - n_start
    if N_eff < 10:
        raise ValueError(f"N={N} 对 n_start={n_start} 太小")
    
    mat = np.zeros((N_eff, N_eff), dtype=complex)
    for i in range(N_eff):
        n = i + n_start
        a_n, b_n, g_n = recurrence_coeffs(s, n, omega, lam, a, m, M_mass)
        mat[i, i] = b_n
        if i < N_eff - 1:
            mat[i, i + 1] = a_n
        if i > 0:
            mat[i, i - 1] = g_n
    return mat


def compute_gap_indicator(s: float, a: float, l: int, m: int,
                          N: int = 60, M_mass: float = 1.0,
                          omega: complex = None,
                          n_start: int = 0) -> float:
    """
    计算 III 型奇异纤维谱间隙指示量 γ(a) = σ_min(M(ω(a)))。

    使用径向三对角矩阵 M(ω) 的最小奇异值作为谱间隙的代理量。
    γ(a) → 0 表示矩阵近奇异 → III 型奇异纤维。
    
    对 s=-2（n_start=4），跳过前 4 项避开 α₁=0 和 α₃=0 的零超对角问题。
    对 s=-1（n_start=2），跳过前 2 项避开 α₁=0。

    参数:
        s: 自旋权重 (-2, -1, -0.5)
        a: 黑洞自旋
        l, m: 角量子数、磁量子数
        N: 矩阵维数（对 s=-2 使用 N=60 足够有效维数 = 56）
        M_mass: 黑洞质量
        omega: 复频率（若为 None，使用插值）
        n_start: 跳过的初始项数
    """
    if omega is None:
        omega = get_omega_approx(s, a)
    
    # 近似角向特征值
    lam = approx_spheroidal_eigenvalue(s, l, m, a, omega, order=2)
    
    # 构建修整三对角矩阵
    tri_mat = build_shifted_tridiagonal(s, N, omega, lam, a, m, M_mass, n_start)
    
    return min_singular_value(tri_mat)


def scan_optimal_omega(s: float, a: float, l: int, m: int,
                       N: int = 60, M_mass: float = 1.0,
                       n_start: int = 0,
                       n_scan_re: int = 15, n_scan_im: int = 9) -> tuple[complex, float]:
    """
    扫描 ω 邻域寻找使 γ(a) = σ_min 最小的 ω（矩阵最接近奇异）。
    
    对近似 ω 的邻域进行二维网格搜索，找到最小化最小奇异值的 ω，
    该 ω 最接近真实的 QNM 频率。
    
    返回:
        (omega_best, sigma_min_best)
    """
    omega_approx = get_omega_approx(s, a)
    
    re_range = np.linspace(omega_approx.real * 0.85, omega_approx.real * 1.15, n_scan_re)
    im_range = np.linspace(omega_approx.imag * 0.3, omega_approx.imag * 2.0, n_scan_im)
    
    best_sigma = float('inf')
    best_omega = omega_approx
    
    for re in re_range:
        for im in im_range:
            omega_test = complex(re, im)
            sigma = compute_gap_indicator(s, a, l, m, N, M_mass, omega_test,
                                          n_start=n_start)
            if sigma < best_sigma:
                best_sigma = sigma
                best_omega = omega_test
    
    return best_omega, best_sigma


# ============================================================
# 3. 对数-对数拟合
# ============================================================

def fit_beta(a_vals: list[float], gamma_vals: list[float]) -> tuple:
    """
    对数-对数拟合 β = d(ln γ)/d(ln(1-a))。

    返回:
        beta, intercept, r_squared, n_points
    """
    # 过滤有效数据：γ>0 且 1-a>0（避免 log(0)）
    pairs = [(a, g) for a, g in zip(a_vals, gamma_vals)
             if g > 1e-15 and (1 - a) > 1e-12]
    
    if len(pairs) < 4:
        return 0.0, 0.0, 0.0, 0
    
    x = np.log(np.array([1.0 - a for a, _ in pairs]))
    y = np.log(np.array([g for _, g in pairs]))
    
    A = np.vstack([x, np.ones_like(x)]).T
    coeffs, residuals = np.linalg.lstsq(A, y, rcond=None)[:2]
    beta, intercept = coeffs[0], coeffs[1]
    
    y_mean = np.mean(y)
    ss_tot = np.sum((y - y_mean) ** 2)
    ss_res = np.sum((y - (beta * x + intercept)) ** 2)
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    
    return float(beta), float(intercept), float(r_squared), len(pairs)


def fit_beta_weighted(a_vals: list[float], gamma_vals: list[float],
                      a_focus: float = 1.0, focus_weight: float = 2.0) -> tuple:
    """
    加权对数-对数拟合，聚焦 a→1 区域。

    focus_weight 越大，越靠近 a_focus 的数据权重越大。
    """
    pairs = [(a, g) for a, g in zip(a_vals, gamma_vals)
             if g > 1e-15 and (1 - a) > 1e-12]
    
    if len(pairs) < 4:
        return 0.0, 0.0, 0.0, 0
    
    x = np.log(np.array([1.0 - a for a, _ in pairs]))
    y = np.log(np.array([g for _, g in pairs]))
    
    # 权重：高斯权重，聚焦 a_focus
    weights = np.exp(-focus_weight * np.array([(1.0 - a) for a, _ in pairs]))
    weights = weights / np.sum(weights) * len(pairs)  # 归一化
    
    W = np.diag(weights)
    A = np.vstack([x, np.ones_like(x)]).T
    
    # 加权最小二乘
    Aw = np.sqrt(W) @ A
    yw = np.sqrt(W) @ y
    coeffs, residuals = np.linalg.lstsq(Aw, yw, rcond=None)[:2]
    beta, intercept = coeffs[0], coeffs[1]
    
    y_mean = np.sum(weights * y) / np.sum(weights)
    ss_tot = np.sum(weights * (y - y_mean) ** 2)
    ss_res = np.sum(weights * (y - (beta * x + intercept)) ** 2)
    r_squared = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    
    return float(beta), float(intercept), float(r_squared), len(pairs)


# ============================================================
# 4. 主函数
# ============================================================

def main():
    print("=" * 78)
    print("跨自旋 III 型奇异纤维标度指数（径向三对角条件数方法 v2.0）")
    print("=" * 78)
    
    # 参数设定
    l, m = 2, 2
    a_vals = [0.80, 0.85, 0.90, 0.92, 0.94, 0.95, 0.96, 0.97,
              0.98, 0.985, 0.99, 0.992, 0.994, 0.995, 0.996, 0.997, 0.998, 0.999]
    
    # 各自旋配置
    # (s, label, short, N, n_start, use_scan)
    # n_start: 跳过的初始项数，避免 α_n=0 导致的块分离
    #   s=-2:  α₁=0, α₃=0 → n_start=4
    #   s=-1:  α₁=0 → n_start=2
    #   s=-0.5: 所有 α_n ≠ 0 → n_start=0
    spin_configs = [
        (-2.0, "引力 (Gravitational)", "G", 64, 4, False),   # 直接参考 ω
        (-1.0, "电磁 (EM)", "EM", 64, 2, True),               # 扫描 ω
        (-0.5, "Dirac (D)", "D", 64, 0, True),                # 扫描 ω
    ]
    
    print(f"\n参数: l={l}, m={m}")
    print(f"a 网格: [{a_vals[0]:.3f}, ..., {a_vals[-1]:.3f}], 共 {len(a_vals)} 点")
    print()
    
    all_data = {}
    
    for s, label, short, N, n_start, use_scan in spin_configs:
        N_eff = N - n_start
        print(f"{'─' * 78}")
        print(f"  {label} (s={s}), N={N}, n_start={n_start} (有效维数 N_eff={N_eff})")
        print(f"{'─' * 78}")
        
        gamma_data = {}
        scan_results = []
        
        for a in a_vals:
            omega_ref = get_omega_approx(s, a)
            
            if use_scan:
                omega_opt, sigma_opt = scan_optimal_omega(
                    s, a, l, m, N, n_start=n_start)
            else:
                omega_opt = omega_ref
                sigma_opt = compute_gap_indicator(
                    s, a, l, m, N, omega=omega_opt, n_start=n_start)
            
            gamma_data[a] = sigma_opt
            scan_results.append((a, omega_ref, omega_opt, sigma_opt))
        
        # 打印数据表
        print(f"  {'a':<8} {'1-a':<12} {'Re(ω_ref)':<14} {'Re(ω_opt)':<14} {'σ_min':<16}")
        print(f"  {'─' * 8} {'─' * 12} {'─' * 14} {'─' * 14} {'─' * 16}")
        for a, w_ref, w_opt, g in scan_results:
            print(f"  {a:<8.4f} {1-a:<12.2e} {w_ref.real:<14.6f} {w_opt.real:<14.6f} {g:<16.6e}")
        
        # 拟合
        a_list = [a for a in a_vals]
        g_list = [gamma_data[a] for a in a_list]
        
        beta, intercept, r2, n_pts = fit_beta(a_list, g_list)
        beta_w, _, r2_w, n_pts_w = fit_beta_weighted(a_list, g_list)
        
        print(f"\n  拟合结果:")
        print(f"    普通 OLS:   β = {beta:.6f},  R² = {r2:.6f},  点数 = {n_pts}")
        print(f"    加权 OLS:   β = {beta_w:.6f},  R² = {r2_w:.6f}, 点数 = {n_pts_w}")
        
        if beta > 0:
            gamma_0999 = np.exp(beta * np.log(1 - 0.999) + intercept)
            print(f"    预测 γ(a=0.999) = {gamma_0999:.6e}")
        
        all_data[short] = {
            's': s, 'beta': beta, 'beta_w': beta_w,
            'r2': r2, 'r2_w': r2_w, 'n_pts': n_pts,
            'label': label, 'gamma_data': gamma_data,
        }
    
    # 对比表
    print(f"\n{'=' * 78}")
    print("三自旋标度指数对比表")
    print(f"{'=' * 78}")
    print(f"{'自旋':<22} {'s':<6} {'β (OLS)':<14} {'β (加权)':<14} {'R² (OLS)':<10} {'R² (加权)':<10}")
    print(f"{'─' * 76}")
    
    sorted_data = sorted(all_data.items(), key=lambda x: x[1]['beta'])
    for short, data in sorted_data:
        print(f"{data['label']:<22} {data['s']:<6.1f} {data['beta']:<14.6f} "
              f"{data['beta_w']:<14.6f} {data['r2']:<10.6f} {data['r2_w']:<10.6f}")
    
    # 排序分析
    print(f"\n{'─' * 40}")
    print("排序分析")
    print(f"{'─' * 40}")
    
    for beta_key, beta_name in [('beta', 'OLS β'), ('beta_w', '加权 β')]:
        if all(k in all_data for k in ['G', 'EM', 'D']):
            order = sorted(['G', 'EM', 'D'], key=lambda x: all_data[x][beta_key])
            names = {'G': '引力', 'EM': '电磁', 'D': 'Dirac'}
            order_str = " < ".join(
                [f"{names[s]}={all_data[s][beta_key]:.4f}" for s in order])
            print(f"  {beta_name} 排序: {order_str}")
            
            bG = all_data['G'][beta_key]
            bEM = all_data['EM'][beta_key]
            bD = all_data['D'][beta_key]
            
            if bG > 0 and bEM > 0 and bD > 0:
                if bG < bEM < bD:
                    print(f"  ✅ 预期 β_G < β_EM < β_D 验证通过")
                elif bG < bD < bEM:
                    print(f"  ⚠ β_EM={bEM:.4f} > β_D={bD:.4f}，部分偏离预期")
                else:
                    print(f"  ⚠ 排序异常: β_G={bG:.4f}, β_EM={bEM:.4f}, β_D={bD:.4f}")
    
    # 理论预期
    print(f"\n{'─' * 40}")
    print("理论解释")
    print(f"{'─' * 40}")
    print(f"""
III 型奇异纤维在极端极限 a→1 时出现，表现为径向三对角矩阵 M(ω) 的最小奇异值 σ_min → 0。
σ_min(a) ∝ (1-a)^β 的标度指数 β 由自旋权重 s 决定：

  - β_G (s=-2, 引力): 预期最小，因引力扰动的 Koopman 谱间隙闭合最缓慢
  - β_EM (s=-1, 电磁): 预期居中
  - β_D (s=-0.5, Dirac): 预期最大，因 Dirac 场的谱结构最"柔韧"

该排序反映 Koopman 算子的谱间隙与自旋权重的单调关系，
理论依据见 Paper XXIX §5 和 Paper XXVII §12.4。
""")
    
    print(f"{'=' * 78}")
    print("方法说明：")
    print("  - 使用径向三对角矩阵 M(ω) 的最小奇异值 σ_min 作为谱间隙指示量")
    print("  - ω(a) 通过已知参考数据插值 + 邻域扫描（最小化 σ_min）优化")
    print("  - 自旋加权椭球谐函数特征值 λ 使用二阶级数近似（Berti 2006）")
    print("  - 对数-对数拟合 σ_min(a) ∝ (1-a)^β，含 OLS 和加权 OLS 两种方法")
    print(f"{'=' * 78}")


if __name__ == "__main__":
    main()
