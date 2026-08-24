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
测试不同的连分数形式和单位制。

目标：找到能正确给出 Schwarzschild QNM 频率 (ω = 0.373672 - 0.088962i) 的连分数实现。
"""

import numpy as np
import cmath


def cf_residual_form1(omega, l, s=-2, M=1.0, max_iter=300):
    """形式1: β₀ - α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...))
    
    使用 Leaver 1991 的系数 (c=G=2M=1 单位制转换到 M=1)
    """
    # 转换到 2M=1 单位制
    omega_l = 2.0 * M * omega
    rho = -1j * omega_l
    epsilon = 3.0
    
    def alpha_n(n):
        return n**2 + (2.0 * rho + 2.0) * n + 2.0 * rho + 1.0
    
    def beta_n(n):
        return -(2.0 * n**2 + (8.0 * rho + 2.0) * n + 8.0 * rho**2 + 4.0 * rho + l * (l + 1.0) - epsilon)
    
    def gamma_n(n):
        return n**2 + 4.0 * rho * n + 4.0 * rho**2 - epsilon - 1.0
    
    # 计算连分数: f = α₁γ₂/(β₁ - α₂γ₃/(β₂ - ...))
    cf = 0.0j
    for n in range(max_iter, 0, -1):
        numer = alpha_n(n) * gamma_n(n + 1)
        denom = beta_n(n) - cf
        if abs(denom) < 1e-30:
            denom = 1e-30
        cf = numer / denom
    
    # 残差 = β₀ - α₀γ₁ / (β₁ - cf) ? 不对
    # 让我们用标准形式: 残差 = β₀ - α₀ * (γ₁ / (β₁ - α₁γ₂/(β₂ - ...)))
    # 但上面的 cf 是 α₁γ₂/(β₁ - ...)
    # 所以完整的连分数 = α₀γ₁ / (β₁ - α₁γ₂/(...)) = α₀γ₁ / (β₁ - cf) ? 不对
    
    # 让我们重新计算
    # cf_n = α_n γ_{n+1} / (β_n - cf_{n+1})
    # 我们从 n=N 向下算到 n=1, 得到 cf_1 = α₁γ₂/(β₁ - α₂γ₃/(...))
    
    # 现在要算 α₀γ₁/(β₀ - α₁γ₂/(β₁ - ...))
    # 这等于 α₀γ₁ / (β₀ - cf_1) ? 不对, 分母是 β₁ - ...
    
    # 等等, 连分数的标准形式是:
    # α₀ / (β₀ + α₁ / (β₁ + α₂ / (β₂ + ...)))
    # 或者对于三项递推:
    # β₀ + α₀γ₁ / (β₁ + α₁γ₂ / (β₂ + ...)) = 0
    
    # 让我们试试: residual = β₀ + α₀ * gamma_n(1) / (beta_n(1) - cf)
    # 不对, 让我们从定义重新推导
    
    # 对于递推 α_n a_{n+1} + β_n a_n + γ_n a_{n-1} = 0
    # 最小解的条件 (Pincherle):
    # 当连分数 α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...)) 收敛时
    # 且 β₀ = α₀γ₁/(β₁ - α₁γ₂/(β₂ - ...)) ?
    
    # 让我们尝试 Leaver 1985 的特征方程形式
    # residual = β₀ - α₀γ₁ / cf_total
    # 其中 cf_total = β₁ - α₁γ₂ / (β₂ - ...)
    
    # 我们上面的 cf 是 α₁γ₂ / (β₁ - α₂γ₃ / (...)) 
    # 所以 β₁ - cf = β₁ - α₁γ₂/(β₁ - ...) 不对...
    
    # 让我们直接从 n=0 开始重新计算
    # 计算: cf_total = α₀γ₁ / (β₁ - α₁γ₂/(β₂ - α₂γ₃/(...)))
    
    # 重新定义: 从 n=N 向下到 n=0
    cf2 = 0.0j
    for n in range(max_iter, -1, -1):
        numer = alpha_n(n) * gamma_n(n + 1)
        denom = beta_n(n + 1) - cf2  # 注意: 分母是 β_{n+1}
        if abs(denom) < 1e-30:
            denom = 1e-30
        cf2 = numer / denom
    
    # 现在 cf2 (n=0 时) = α₀γ₁ / (β₁ - α₁γ₂/(β₂ - ...))
    
    # 特征方程: β₀ - cf2 = 0 ?
    residual = beta_n(0) - cf2
    
    return residual


def cf_residual_form2(omega, l, s=-2, M=1.0, max_iter=300):
    """形式2: 使用乘积形式系数 (之前代码中的形式)"""
    r_plus = M + np.sqrt(M**2 - 0**2)
    r_minus = M - np.sqrt(M**2 - 0**2)
    sigma_plus = (omega * r_plus - 0 * 0) / (r_plus - r_minus)
    A_lm = l * (l + 1) - s * (s + 1)
    
    def alpha_n(n):
        return -2.0j * omega * (n + 1.0) * (n - 4.0j * sigma_plus)
    
    def beta_n(n):
        return n * (n + 1.0) + 4.0 * sigma_plus**2 - 8.0 * omega * sigma_plus - A_lm
    
    def gamma_n(n):
        return 2.0j * omega * (n - 4.0j * sigma_plus - 1.0)
    
    cf = 0.0j
    for n in range(max_iter, 0, -1):
        denom = beta_n(n) - alpha_n(n) * gamma_n(n + 1) * cf
        if abs(denom) < 1e-30:
            denom = 1e-30
        cf = 1.0 / denom
    
    residual = beta_n(0) - alpha_n(0) * gamma_n(1) * cf
    return residual


def find_root(residual_func, omega_guess, l, s=-2, M=1.0, max_iter=50):
    """Newton 法找根"""
    omega = complex(omega_guess)
    eps = 1e-7
    
    for i in range(max_iter):
        f = residual_func(omega, l, s, M)
        res = abs(f)
        
        if res < 1e-12:
            break
        
        f_re = residual_func(omega + eps, l, s, M)
        f_im = residual_func(omega + 1j * eps, l, s, M)
        df_dre = (f_re - f) / eps
        df_dim = (f_im - f) / eps
        
        jacobian = np.array([[df_dre.real, df_dim.real], [df_dre.imag, df_dim.imag]])
        rhs = -np.array([f.real, f.imag])
        
        try:
            delta = np.linalg.solve(jacobian, rhs)
            omega += complex(delta[0], delta[1])
        except np.linalg.LinAlgError:
            omega -= 0.01 * f
    
    return omega, abs(f)


def main():
    M = 1.0
    l = 2
    s = -2
    ref_omega = complex(0.373672, -0.088962)
    
    print("=" * 70)
    print("不同连分数形式的测试")
    print("=" * 70)
    print(f"参考频率: ω = {ref_omega.real:.6f} {ref_omega.imag:.6f}i")
    print(f"l = {l}, s = {s}, M = {M}")
    print()
    
    forms = [
        ("形式1: Leaver 1991 二次系数, β₀ - α₀γ₁/(β₁ - ...)", cf_residual_form1),
        ("形式2: 乘积形式系数, 1/(β - αγ*cf) 形式", cf_residual_form2),
    ]
    
    for name, func in forms:
        print(f"--- {name} ---")
        
        # 参考频率处的残差
        res_ref = func(ref_omega, l, s, M)
        print(f"  参考频率残差: {abs(res_ref):.2e}")
        
        # 从参考频率出发找根
        omega_root, res_root = find_root(func, ref_omega, l, s, M)
        print(f"  找到的根: ω = {omega_root.real:.8f} {omega_root.imag:.8f}i")
        print(f"  根的残差: {res_root:.2e}")
        print(f"  与参考值偏差: ΔRe = {abs(omega_root.real - ref_omega.real):.2e}, ΔIm = {abs(omega_root.imag - ref_omega.imag):.2e}")
        print()
    
    # 尝试不同的初始猜测
    print("--- 形式2: 不同初始猜测 ---")
    guesses = [
        complex(0.37, -0.09),
        complex(0.5, -0.1),
        complex(0.3, -0.05),
        complex(0.4, -0.15),
        complex(0.6, -0.08),
        complex(0.2, -0.04),
    ]
    
    for guess in guesses:
        omega_root, res_root = find_root(cf_residual_form2, guess, l, s, M)
        print(f"  初值 {guess.real:.2f}{guess.imag:+.2f}i -> ω = {omega_root.real:.6f} {omega_root.imag:.6f}i, 残差 = {res_root:.2e}")


if __name__ == "__main__":
    main()
