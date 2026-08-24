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
_optimize_D.py —— 对 s=-0.5 数值优化 D₀-D₄ 系数

方法：对 s=-0.5, a=0，已知 ω_ref 和 λ，优化 D₀-D₄ 
使连分数残差 |R₀(ω_ref)| 最小。

然后用优化得到的 D 系数反推 sigma_D 中的正确 ω² 项。
"""

import numpy as np
from scipy.optimize import minimize
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 从 _fit_Dcoeffs.py 导入工具函数
from _fit_Dcoeffs import (
    D_from_coeffs, polynomial_alpha, polynomial_beta, polynomial_gamma,
    cf_from_D, cf_product, alpha_product, beta_product, gamma_product
)


def objective_from_D(params, omega, lam, m):
    """
    目标函数：给定 D 参数，计算 |R₀(ω)|。
    
    params = [D₀_re, D₀_im, D₁_re, D₁_im, D₂_re, D₂_im, D₃_re, D₃_im, D₄_re, D₄_im]
    """
    D = np.array([
        params[0] + 1j*params[1],
        params[2] + 1j*params[3],
        params[4] + 1j*params[5],
        params[6] + 1j*params[7],
        params[8] + 1j*params[9],
    ], dtype=complex)
    r = cf_from_D(omega, lam, m, D, max_iter=300)
    return abs(r)


def optimize_D_for_sigma(omega_ref, lam, m=0.5, s=-0.5):
    """
    用优化方法找到使 |R₀(ω_ref)| = 0 的 D₀-D₄。
    
    然后用 D[3] 反推 sigma_D 中的正确 ω² 系数。
    """
    print("=" * 70)
    print(f"数值优化 D₀-D₄: s={s}, ω_ref={omega_ref:.8f}, λ={lam:.2f}")
    print("=" * 70)
    
    # 先用理论公式计算初始猜测
    from _dirac_polynomial_solver import DiracPolynomialSolver
    solver = DiracPolynomialSolver(M=1.0, a=0.0, s=s)
    D_init = solver._D_coeffs(omega_ref, lam, m)
    print(f"初始 D (理论公式): {D_init}")
    print(f"初始 |R₀| = {abs(cf_from_D(omega_ref, lam, m, D_init)):.6e}")
    
    # 优化参数（固定 D₀ 和 D₄ 以保持 αₙ 正确）
    # 对 a=0, Schwarzschild，多项式形式应当有确定解
    # 用 D_from_coeffs 中的乘积形式反推作为起点
    D_prod = D_from_coeffs(s, omega_ref, lam, a=0.0, m=m, method='product')
    print(f"乘积形式反推 D: {D_prod}")
    print(f"初始 |R₀| (乘积 D) = {abs(cf_from_D(omega_ref, lam, m, D_prod)):.6e}")
    
    # 优化方法：只优化 D₁, D₂, D₃, D₄（固定 D₀ = α₀）
    # 用 (D₀_re, D₀_im) 作为已知量，优化剩下的 8 个实参数
    # 但更好的方法：对每一个 D 参数加一个微扰搜索
    
    # 方法：用 "正确" 的 D₀ = α₀ 并在此基础上搜索剩余的 D 参数
    D0_target = alpha_product(s, 0, omega_ref, 0.0, m)
    
    print(f"\n目标 D₀ = α₀ = {D0_target:.10f}")
    print(f"理论公式 D₀ = {D_init[0]:.10f}")
    print(f"乘积反推 D₀ = {D_prod[0]:.10f}")
    
    # 以理论公式为起点，做局部优化
    def objective_full(params_flat):
        """优化所有 10 个实参数。"""
        D_full = np.array([
            params_flat[0] + 1j*params_flat[1],
            params_flat[2] + 1j*params_flat[3],
            params_flat[4] + 1j*params_flat[5],
            params_flat[6] + 1j*params_flat[7],
            params_flat[8] + 1j*params_flat[9],
        ], dtype=complex)
        return abs(cf_from_D(omega_ref, lam, m, D_full))
    
    # 用理论公式作为初始点
    x0 = np.array([
        D_init[0].real, D_init[0].imag,
        D_init[1].real, D_init[1].imag,
        D_init[2].real, D_init[2].imag,
        D_init[3].real, D_init[3].imag,
        D_init[4].real, D_init[4].imag,
    ])
    
    result = minimize(objective_full, x0, method='Nelder-Mead',
                      options={'maxiter': 10000, 'xatol': 1e-14, 'fatol': 1e-14})
    
    D_opt = np.array([
        result.x[0] + 1j*result.x[1],
        result.x[2] + 1j*result.x[3],
        result.x[4] + 1j*result.x[5],
        result.x[6] + 1j*result.x[7],
        result.x[8] + 1j*result.x[9],
    ], dtype=complex)
    
    r_opt = cf_from_D(omega_ref, lam, m, D_opt)
    
    print(f"\n优化结果:")
    print(f"D₀-D₄ = {D_opt}")
    print(f"|R₀| = {abs(r_opt):.2e}")
    print(f"迭代次数: {result.nit}")
    print(f"收敛: {result.success}")
    
    # 从 D[3] 反推 sigma_D 中的 ω² 系数
    # 计算理论公式中的参数
    root = np.sqrt(max(0.0, 1.0 - 0.0**2))  # a=0
    r_p = 1.0 + root
    r_m = 1.0 - root
    sigma_p = (2.0 * omega_ref * r_p) / (2.0 * root)  # a=0, m=0.5 但这里简化
    sigma_p = (2.0 * omega_ref * r_p - 0.0 * m) / (2.0 * root)
    sigma_m = (2.0 * omega_ref * r_m - 0.0 * m) / (2.0 * root)
    zeta = 1.0j * omega_ref
    xi = -s - 1.0j * sigma_p
    eta = -1.0j * sigma_m
    p_val = root * zeta
    alpha = 1.0 + s + xi + eta - 2.0 * zeta + s
    gamma_coef = 1.0 + s + 2.0 * eta
    delta = 1.0 + s + 2.0 * xi
    
    # 从优化的 D[3] 反推 sigma_D
    # D[3] = alpha·(4p - delta) - sigma_D
    sigma_D_opt = alpha * (4.0 * p_val - delta) - D_opt[3]
    
    # sigma_base 不含 ω² 项
    sigma_base = (lam + 0.0 + p_val * (2.0 * alpha + gamma_coef - delta)
                  + (1.0 + s - 0.5 * (gamma_coef + delta))
                  * (s + 0.5 * (gamma_coef + delta)))
    
    C_omega2 = (sigma_D_opt - sigma_base) / (omega_ref**2)
    print(f"\n从优化 D[3] 反推:")
    print(f"  sigma_base = {sigma_base:.10f}")
    print(f"  sigma_D_opt = {sigma_D_opt:.10f}")
    print(f"  ω² 系数 C = {C_omega2:.6f}")
    print(f"  对比: 4s = {4*s:.1f}")
    
    # 也对理论公式的 D 做同样的反推
    D_th = solver._D_coeffs(omega_ref, lam, m)
    sigma_D_th = alpha * (4.0 * p_val - delta) - D_th[3]
    C_th = (sigma_D_th - sigma_base) / (omega_ref**2)
    print(f"  理论公式 ω² 系数 C_th = {C_th:.6f}")
    
    return D_opt


def scan_omega2_coefficient():
    """
    扫描 sigma_D 中不同的 ω² 系数 C，观察 |R₀(ω_ref)| 的变化。
    """
    print("\n" + "=" * 70)
    print("扫描 sigma_D 中 ω² 系数 C")
    print("=" * 70)
    
    # 对 s=-0.5 和 s=-2
    for s, l, m, omega_ref, lam, name in [
        (-0.5, 0.5, 0.5, 0.378721 - 0.096458j, 1.0, "Dirac"),
        (-2, 2, 0, 0.373672 - 0.088962j, 4.0, "引力"),
    ]:
        print(f"\n[{name} s={s}]")
        print(f"{'C':>12} {'|R₀(C)|':>16}")
        
        # 基准：用 LeaverResidual 计算基准 D 系数
        from leaver_unified_solver import LeaverResidual as LR
        solver = LR(M=1.0, a=0.0, s=int(s), max_iter=300)
        if abs(s + 2) < 0.1:
            D_th = solver._D_coeffs(omega_ref, lam, int(m))
        else:
            from _dirac_polynomial_solver import DiracPolynomialSolver as DPS
            solver2 = DPS(M=1.0, a=0.0, s=s)
            D_th = solver2._D_coeffs(omega_ref, lam, m)
        
        # 计算 sigma_D 的分量
        root = np.sqrt(1.0)
        sigma_p = 2.0 * omega_ref * (1.0 + 1.0) / 2.0  # a=0
        sigma_m = 2.0 * omega_ref * (1.0 - 1.0) / 2.0
        zeta = 1.0j * omega_ref
        xi = -s - 1.0j * sigma_p
        eta = -1.0j * sigma_m
        p_val = zeta
        alpha_p = 1.0 + s + xi + eta - 2.0 * zeta + s
        gamma_coef = 1.0 + s + 2.0 * eta
        delta = 1.0 + s + 2.0 * xi
        
        sigma_base = (lam + 0.0 + p_val * (2.0 * alpha_p + gamma_coef - delta)
                      + (1.0 + s - 0.5 * (gamma_coef + delta))
                      * (s + 0.5 * (gamma_coef + delta)))
        
        for C in np.linspace(-15, 5, 21):
            # 构造 sigma_D = sigma_base + C·ω²
            sigma_D = sigma_base + C * omega_ref**2
            
            # 从 sigma_D 重构 D[3]
            D_test = D_th.copy()
            D_test[3] = alpha_p * (4.0 * p_val - delta) - sigma_D
            
            r = cf_from_D(omega_ref, lam, m if abs(s+2) > 0.1 else int(m), D_test)
            print(f"{C:12.4f} {abs(r):16.6e}")
        
        # 显示理论值位置
        if abs(s+2) < 0.1:
            print(f"  {'(理论 C=-8)':12} {'':>16}")
        else:
            print(f"  {'(理论 C=-8)':12} {'':>16}")


if __name__ == "__main__":
    # 1. 扫描 ω² 系数
    scan_omega2_coefficient()
    
    # 2. 数值优化 D 系数
    print("\n\n")
    D_best = optimize_D_for_sigma(0.378721 - 0.096458j, 1.0, m=0.5)
    
    # 3. 用优化得到的 D 系数测试 Müller 法
    print("\n" + "=" * 70)
    print("用优化 D 系数测试 Müller 法")
    print("=" * 70)
    
    from _dirac_polynomial_solver import DiracPolynomialSolver
    
    # 创建修改版的求解器
    class CustomDiracSolver(DiracPolynomialSolver):
        """使用优化的 D 系数的求解器。"""
        def __init__(self, D_opt, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.D_opt = D_opt
        
        def _D_coeffs(self, omega, lam, m):
            return self.D_opt
    
    solver = CustomDiracSolver(D_best, M=1.0, a=0.0, s=-0.5, max_iter=300)
    
    for l, m, omega_guess in [
        (0.5, 0.5, 0.378721 - 0.096458j),
        (1.5, 1.5, 0.522988 - 0.089964j),
        (2.5, 2.5, 0.640418 - 0.091694j),
    ]:
        result = solver.find_qnm(l, m, n=0, max_iter=50, tol=1e-10)
        status = "✓" if result['converged'] else "✗"
        print(f"  l={l:.1f} m={m:+.1f}: ω = {result['omega'].real:.10f} {result['omega'].imag:+.10f}i "
              f"|R₀| = {result['cf_residual']:.2e} {status}")
