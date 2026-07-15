"""
验证 Schwarzschild QNM 频率的连分数残差。

使用已知的参考值来测试不同的连分数系数公式，
找到能给出正确残差（接近零）的实现。
"""

import numpy as np
import cmath


def test_schwarzschild_residual():
    M = 1.0
    a = 0.0
    s = -2
    l = 2
    m = 0
    b = cmath.sqrt(M**2 - a**2)
    r_plus = M + b
    r_minus = M - b
    
    ref_omega = complex(0.373672, -0.088962)
    
    print("=" * 60)
    print("Schwarzschild QNM 连分数残差验证")
    print("=" * 60)
    print(f"参考频率: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
    print(f"l={l}, m={m}, s={s}, a={a}")
    print()
    
    lam = l * (l + 1.0) - s * (s + 1.0)
    print(f"球谐本征值: A = {lam}")
    print()
    
    print("--- 方案1: 乘积形式系数 ---")
    sigma_plus = (ref_omega * r_plus - m * a) / (r_plus - r_minus)
    print(f"σ₊ = {sigma_plus.real:.6f} {sigma_plus.imag:.6f}i")
    
    def alpha_n1(n):
        return -2.0j * ref_omega * (n + 1.0) * (n - 4.0j * sigma_plus)
    
    def beta_n1(n):
        return (n * (n + 1.0) + 4.0 * sigma_plus**2 - 8.0 * ref_omega * sigma_plus - lam)
    
    def gamma_n1(n):
        return 2.0j * ref_omega * (n - 4.0j * sigma_plus - 1.0)
    
    max_iter = 300
    cf = complex(0.0, 0.0)
    for n in range(max_iter, 0, -1):
        denom = beta_n1(n) - alpha_n1(n) * gamma_n1(n + 1) * cf
        if abs(denom) < 1e-30:
            denom = complex(1e-30, 0.0)
        cf = 1.0 / denom
    
    residual1 = beta_n1(0) - alpha_n1(0) * gamma_n1(1) * cf
    print(f"残差: {abs(residual1):.2e}")
    print(f"残差 (复): {residual1.real:.2e} {residual1.imag:.2e}i")
    print()
    
    print("--- 方案2: Leaver 二次多项式系数 ---")
    sigma_plus2 = (ref_omega * r_plus - m * a) / (2.0 * b)
    epsilon = 2.0 * ref_omega * M
    Omega = ref_omega * b
    
    print(f"σ₊ = {sigma_plus2.real:.6f} {sigma_plus2.imag:.6f}i")
    print(f"ε = {epsilon.real:.6f} {epsilon.imag:.6f}i")
    print(f"Ω = {Omega.real:.6f} {Omega.imag:.6f}i")
    
    c0 = 1.0 - s - 2.0j * sigma_plus2 - 2.0j * Omega + 2.0j * epsilon
    c1 = 4.0j * sigma_plus2 - 2.0 * s
    c2 = (lam + s * (s + 1.0) - 4.0 * ref_omega**2 * M * (M + b)
          - 2.0 * a * m * ref_omega
          - 2.0j * sigma_plus2 * (1.0 - s - 2.0j * sigma_plus2 - 2.0j * Omega + 4.0j * epsilon))
    c3 = 1.0 + c1 + 4.0j * Omega - 4.0j * epsilon
    c4 = c2 + (2.0j * Omega - 2.0j * epsilon) * (1.0 - s - 2.0j * sigma_plus2) + 2.0j * epsilon
    c5 = 4.0j * Omega - 2.0 * s
    c6 = -4.0 * Omega**2 - 4.0j * Omega * epsilon + 4.0j * Omega * sigma_plus2 - 2.0 * s * 1.0j * Omega
    
    print(f"c0 = {c0.real:.6f} {c0.imag:.6f}i")
    print(f"c1 = {c1.real:.6f} {c1.imag:.6f}i")
    print(f"c2 = {c2.real:.6f} {c2.imag:.6f}i")
    print(f"c3 = {c3.real:.6f} {c3.imag:.6f}i")
    print(f"c4 = {c4.real:.6f} {c4.imag:.6f}i")
    print(f"c5 = {c5.real:.6f} {c5.imag:.6f}i")
    print(f"c6 = {c6.real:.6f} {c6.imag:.6f}i")
    
    def alpha_n2(n):
        return n**2 + (c1 + 1.0) * n + c0
    
    def beta_n2(n):
        return -2.0 * n**2 - c3 * n - c4
    
    def gamma_n2(n):
        return n**2 + c5 * n + c6
    
    cf2 = complex(0.0, 0.0)
    for n in range(max_iter, 0, -1):
        denom = beta_n2(n) - alpha_n2(n) * gamma_n2(n + 1) * cf2
        if abs(denom) < 1e-30:
            denom = complex(1e-30, 0.0)
        cf2 = 1.0 / denom
    
    residual2 = beta_n2(0) - alpha_n2(0) * gamma_n2(1) * cf2
    print(f"残差: {abs(residual2):.2e}")
    print(f"残差 (复): {residual2.real:.2e} {residual2.imag:.2e}i")
    print()
    
    print("--- 方案3: 另一种连分数形式 (β₀ - α₀γ₁/β₁ - α₁γ₂/β₂ - ...) ---")
    cf3 = complex(0.0, 0.0)
    for n in range(max_iter, 0, -1):
        cf3 = alpha_n1(n) * gamma_n1(n + 1) / (beta_n1(n) - cf3)
    
    residual3 = beta_n1(0) - cf3
    print(f"残差 (乘积形式, 另一种迭代): {abs(residual3):.2e}")
    print()
    
    print("--- 方案4: 二次多项式, 另一种连分数形式 ---")
    cf4 = complex(0.0, 0.0)
    for n in range(max_iter, 0, -1):
        cf4 = alpha_n2(n) * gamma_n2(n + 1) / (beta_n2(n) - cf4)
    
    residual4 = beta_n2(0) - cf4
    print(f"残差 (二次形式, 另一种迭代): {abs(residual4):.2e}")
    print()
    
    print("--- 方案5: 调整 A（分离常数）使残差为零 ---")
    A_test = lam
    best_A = A_test
    best_res = float('inf')
    
    for delta_A in np.linspace(-2, 2, 41):
        A_curr = lam + delta_A
        
        def alpha_n_test(n):
            return -2.0j * ref_omega * (n + 1.0) * (n - 4.0j * sigma_plus)
        
        def beta_n_test(n):
            return (n * (n + 1.0) + 4.0 * sigma_plus**2 - 8.0 * ref_omega * sigma_plus - A_curr)
        
        def gamma_n_test(n):
            return 2.0j * ref_omega * (n - 4.0j * sigma_plus - 1.0)
        
        cf_test = complex(0.0, 0.0)
        for n in range(max_iter, 0, -1):
            denom = beta_n_test(n) - alpha_n_test(n) * gamma_n_test(n + 1) * cf_test
            if abs(denom) < 1e-30:
                denom = complex(1e-30, 0.0)
            cf_test = 1.0 / denom
        
        res_test = abs(beta_n_test(0) - alpha_n_test(0) * gamma_n_test(1) * cf_test)
        
        if res_test < best_res:
            best_res = res_test
            best_A = A_curr
    
    print(f"最优 A = {best_A:.6f}")
    print(f"对应残差: {best_res:.2e}")
    print(f"与球谐值的偏差: {best_A - lam:.6f}")


if __name__ == "__main__":
    test_schwarzschild_residual()
