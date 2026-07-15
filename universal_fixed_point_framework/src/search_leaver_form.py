"""
通过搜索找到正确的连分数系数形式。

使用已知的 Schwarzschild QNM 参考值，
通过系统搜索来确定正确的连分数系数参数化方式。
"""

import numpy as np
import cmath


def compute_cf_residual(omega, A_l, s, sigma_plus, max_iter=300):
    """通用连分计算 - 使用标准形式 β₀ - α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...))"""
    
    def alpha_n(n):
        return -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)
    
    def beta_n(n):
        return n * (n + 1.0) + 4.0 * sigma_plus**2 - 8.0 * omega * sigma_plus - A_l
    
    def gamma_n(n):
        return 2.0j * omega * (n - 4.0j * sigma_plus - 1.0)
    
    cf = complex(0.0, 0.0)
    for n in range(max_iter, 0, -1):
        denom = beta_n(n) - alpha_n(n) * gamma_n(n + 1) * cf
        if abs(denom) < 1e-30:
            denom = complex(1e-30, 0.0)
        cf = 1.0 / denom
    
    residual = beta_n(0) - alpha_n(0) * gamma_n(1) * cf
    return residual


def search_correct_form():
    """搜索正确的参数化形式。"""
    M = 1.0
    a = 0.0
    s = -2
    l = 2
    m = 0
    b = np.sqrt(M**2 - a**2)
    r_plus = M + b
    r_minus = M - b
    
    ref_omega = complex(0.373672, -0.088962)
    
    print("=" * 70)
    print("搜索正确的 Leaver 连分数参数化")
    print("=" * 70)
    print(f"参考频率: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
    print()
    
    A_lm = l * (l + 1) - s * (s + 1)
    print(f"球谐分离常数 (a=0): A_lm = {A_lm}")
    print()
    
    print("--- 方案1: 标准 σ₊ = (ω r₊ - a m) / (r₊ - r₋) ---")
    sigma_plus_1 = (ref_omega * r_plus - a * m) / (r_plus - r_minus)
    print(f"σ₊ = {sigma_plus_1.real:.6f} {sigma_plus_1.imag:.6f}i")
    
    best_A = None
    best_res = float('inf')
    
    for delta_A in np.linspace(-10, 10, 201):
        A_test = A_lm + delta_A
        res = compute_cf_residual(ref_omega, A_test, s, sigma_plus_1)
        if abs(res) < best_res:
            best_res = abs(res)
            best_A = A_test
    
    print(f"最优 A = {best_A:.4f}, 残差 = {best_res:.2e}")
    print(f"与球谐值的差: {best_A - A_lm:.4f}")
    print()
    
    print("--- 方案2: σ₊ = (ω r₊ - a m) / (2b) ---")
    sigma_plus_2 = (ref_omega * r_plus - a * m) / (2.0 * b)
    print(f"σ₊ = {sigma_plus_2.real:.6f} {sigma_plus_2.imag:.6f}i")
    
    best_A2 = None
    best_res2 = float('inf')
    
    for delta_A in np.linspace(-10, 10, 201):
        A_test = A_lm + delta_A
        res = compute_cf_residual(ref_omega, A_test, s, sigma_plus_2)
        if abs(res) < best_res2:
            best_res2 = abs(res)
            best_A2 = A_test
    
    print(f"最优 A = {best_A2:.4f}, 残差 = {best_res2:.2e}")
    print(f"与球谐值的差: {best_A2 - A_lm:.4f}")
    print()
    
    print("--- 方案3: 改变 αₙ 和 γₙ 的形式 ---")
    print("测试不同的系数前因子...")
    
    # 尝试不同的前因子
    best_overall = float('inf')
    best_params = None
    
    for pre_alpha in [1.0, -1.0, 2.0, -2.0, 0.5, -0.5]:
        for pre_gamma in [1.0, -1.0, 2.0, -2.0, 0.5, -0.5]:
            for sigma_factor in [1.0, 2.0, 0.5, 4.0, 0.25]:
                sigma_test = sigma_plus_1 * sigma_factor
                
                for delta_A in np.linspace(-5, 5, 51):
                    A_test = A_lm + delta_A
                    
                    def alpha_n(n):
                        return pre_alpha * 1.0j * omega * (n + 1.0) * (n - 4.0j * sigma_test)
                    
                    def beta_n(n):
                        return n * (n + 1.0) + 4.0 * sigma_test**2 - 8.0 * omega * sigma_test - A_test
                    
                    def gamma_n(n):
                        return pre_gamma * 1.0j * omega * (n - 4.0j * sigma_test - 1.0)
                    
                    omega = ref_omega
                    cf = 0j
                    for n in range(200, 0, -1):
                        denom = beta_n(n) - alpha_n(n) * gamma_n(n + 1) * cf
                        if abs(denom) < 1e-30:
                            denom = 1e-30
                        cf = 1.0 / denom
                    res = abs(beta_n(0) - alpha_n(0) * gamma_n(1) * cf)
                    
                    if res < best_overall:
                        best_overall = res
                        best_params = (pre_alpha, pre_gamma, sigma_factor, A_test)
    
    print(f"最优组合: pre_alpha={best_params[0]}, pre_gamma={best_params[1]}")
    print(f"  sigma_factor={best_params[2]}, A={best_params[3]:.4f}")
    print(f"  残差: {best_overall:.2e}")
    print()
    
    print("--- 方案4: 完全不同的 βₙ 形式 ---")
    print("测试 βₙ = -2n² + ... 形式")
    
    omega = ref_omega
    sigma_plus = sigma_plus_1
    best_res4 = float('inf')
    best_params4 = None
    
    for c2 in np.linspace(-5, 5, 21):
        for c1 in np.linspace(-5, 5, 21):
            for c0 in np.linspace(-5, 5, 21):
                def alpha_n(n):
                    return n**2 + c2 * n + c1
                
                def beta_n(n):
                    return -2.0 * n**2 + c1 * n + c0
                
                def gamma_n(n):
                    return n**2 + c2 * n + c0
                
                cf = 0j
                try:
                    for n in range(100, 0, -1):
                        denom = beta_n(n) - alpha_n(n) * gamma_n(n + 1) * cf
                        if abs(denom) < 1e-30:
                            denom = 1e-30
                        cf = 1.0 / denom
                    res = abs(beta_n(0) - alpha_n(0) * gamma_n(1) * cf)
                    
                    if res < best_res4:
                        best_res4 = res
                        best_params4 = (c2, c1, c0)
                except Exception:
                    pass
    
    print(f"最优参数: c2={best_params4[0]}, c1={best_params4[1]}, c0={best_params4[2]}")
    print(f"  残差: {best_res4:.2e}")


if __name__ == "__main__":
    search_correct_form()
