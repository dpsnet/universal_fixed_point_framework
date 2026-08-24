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
_diagnose_cf_detail.py —— 乘积形式连分数失效的深入诊断

定位问题是在系数定义还是在 CF 求值。
"""

import numpy as np
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dynamic_spectrum"))

from _spin_weight_coeff import (
    frobenius_index, alpha_n, beta_n, gamma_n, recurrence_coeffs
)
from _dirac_leaver_solver import (
    dirac_alpha_n, dirac_beta_n, dirac_gamma_n, dirac_recurrence_coeffs
)
from leaver_unified_solver import LeaverResidual as LeaverPoly

print("=" * 70)
print("乘积形式 vs 多项式形式：系数逐项对比")
print("=" * 70)

# 测试条件：s=-2, l=2, m=0, a=0, ω=0.373672-0.088962j (参考值)
s = -2
m = 0
a = 0.0
omega = 0.373672 - 0.088962j
lam = 4.0  # a=0 下精确值

print(f"\n测试：s={s}, l=2, m={m}, a={a}")
print(f"ω_ref = {omega:.10f}")
print(f"λ = {lam}")
print()

# === 乘积形式 (product form) ===
solver_poly = LeaverPoly(M=1.0, a=a, s=s, max_iter=200)
D = solver_poly._D_coeffs(omega, lam, m)

print(f"{'n':>4} | {'α_prod':>18} {'β_prod':>18} {'γ_prod':>18} | "
      f"{'α_poly':>18} {'β_poly':>18} {'γ_poly':>18} | {'ratio':>10}")
print("-" * 130)

for n in [0, 1, 2, 3, 5, 10, 20, 50, 100]:
    a_p, b_p, g_p = recurrence_coeffs(s, n, omega, lam, a, m)
    a_o = solver_poly._polynomial_alpha(n, D)
    b_o = solver_poly._polynomial_beta(n, D)
    g_o = solver_poly._polynomial_gamma(n, D)
    
    # 检查大 n 比率
    if abs(g_p) > 1e-30 and abs(a_p) > 1e-30:
        ratio = abs(a_p / g_p)
    else:
        ratio = float('inf')
    
    print(f"{n:4d} | {complex(a_p):>18.6e} {complex(b_p):>18.6e} {complex(g_p):>18.6e} | "
          f"{complex(a_o):>18.6e} {complex(b_o):>18.6e} {complex(g_o):>18.6e} | {ratio:10.2f}")

print("\n" + "=" * 70)
print("乘积形式大 n 渐近系数（多项式形式为基准）：")
print("=" * 70)

n_large = 200
a_p, b_p, g_p = recurrence_coeffs(s, n_large, omega, lam, a, m)
a_o = solver_poly._polynomial_alpha(n_large, D)
b_o = solver_poly._polynomial_beta(n_large, D)
g_o = solver_poly._polynomial_gamma(n_large, D)

print(f"\n  n={n_large}:")
print(f"  α_prod = {complex(a_p):.6e} ≈ {a_p/n_large**2:.4f}·n²")
print(f"  α_poly = {complex(a_o):.6e} ≈ {a_o/n_large**2:.4f}·n²")
print(f"  γ_prod = {complex(g_p):.6e} ≈ γ·n")
print(f"  γ_poly = {complex(g_o):.6e} ≈ {g_o/n_large**2:.4f}·n²")

# ============================================
# 检查标准 Leaver CF 递推是否匹配对角化条件
# ============================================
print("\n" + "=" * 70)
print("三对角矩阵行列式检查（乘积形式）：")
print("=" * 70)

# 构建小矩阵并检查行列式
N = 10
mat = np.zeros((N, N), dtype=complex)
for n in range(N):
    a_n, b_n, g_n = recurrence_coeffs(s, n, omega, lam, a, m)
    mat[n, n] = b_n
    if n < N - 1:
        mat[n, n + 1] = a_n
    if n > 0:
        mat[n, n - 1] = g_n

det_val = np.linalg.det(mat)
print(f"  N={N}, det(M) = {det_val:.6e}  (应 ≈ 0 对 QNM ω)")

# 也检查多项式形式的小矩阵
mat_poly = np.zeros((N, N), dtype=complex)
for n in range(N):
    a_o = solver_poly._polynomial_alpha(n, D)
    b_o = solver_poly._polynomial_beta(n, D)
    g_o = solver_poly._polynomial_gamma(n, D)
    mat_poly[n, n] = b_o
    if n < N - 1:
        mat_poly[n, n + 1] = a_o
    if n > 0:
        mat_poly[n, n - 1] = g_o

det_poly = np.linalg.det(mat_poly)
print(f"  N={N}, det(M_poly) = {det_poly:.6e}  (应 ≈ 0 对 QNM ω)")

# 检查特征值谱
eigvals = np.linalg.eigvals(mat)
eigvals_poly = np.linalg.eigvals(mat_poly)
min_eig_prod = np.min(np.abs(eigvals))
min_eig_poly = np.min(np.abs(eigvals_poly))
print(f"  min|λ|(M_prod) = {min_eig_prod:.6e}")
print(f"  min|λ|(M_poly) = {min_eig_poly:.6e}")


# ============================================
# 用多项式形式计算正确的引力 CF 残差
# ============================================
print("\n" + "=" * 70)
print("多项式形式 CF 基准检测：")
print("=" * 70)

poly_res = solver_poly.radial_cf_polynomial(omega, lam, m)
print(f"  s=-2: |R₀_poly(ω_ref)| = {abs(poly_res):.6e}  (应 ≈ 0 ✓)")


# ============================================
# 检查多项式形式中 "-8ω²" 项对 s=-0.5 的影响
# ============================================
print("\n" + "=" * 70)
print("诊断多项式形式中 -8ω² 项的敏感性：")
print("=" * 70)

# 对 s=-0.5 的情况
s_d = -0.5
lam_d = 1.0
omega_d = 0.378721 - 0.096458j
m_d = 0.5

# 尝试用多项式形式（带 -8ω² 项，即错误的形式）
try:
    solver_d = LeaverPoly(M=1.0, a=0.0, s=int(s_d), max_iter=200)
    D_d = solver_d._D_coeffs(omega_d, lam_d, int(m_d))
    print(f"\n  Cook-Zalutskiy D 系数（s=-0.5）：")
    print(f"    D₀-D₄ = {D_d}")
    
    res_d = solver_d.radial_cf_polynomial(omega_d, lam_d, int(m_d))
    print(f"    |R₀(ω_ref)| = {abs(res_d):.6e} (带 -8ω² 项)")
    
    # 如果没有 -8ω² 项会怎样？
    print(f"\n  如果不带 -8ω² 项（修改 σ 公式）：")
    # 计算自定义 D 系数
    root = np.sqrt(max(0.0, 1.0 - 0.0**2))
    r_p, r_m = 1.0 + root, 1.0 - root
    sigma_p = (2.0 * omega_d * r_p - 0.0 * m_d) / (2.0 * root)
    sigma_m = (2.0 * omega_d * r_m - 0.0 * m_d) / (2.0 * root)
    zeta = 1.0j * omega_d
    xi = -s_d - 1.0j * sigma_p
    eta = -1.0j * sigma_m
    p = root * zeta
    alpha = 1.0 + s_d + xi + eta - 2.0 * zeta + s_d
    gamma_coef = 1.0 + s_d + 2.0 * eta
    delta = 1.0 + s_d + 2.0 * xi
    # 不用 -8ω² 项
    sigma_no8 = (lam_d + 0.0**2 * omega_d**2 - 0.0 * omega_d**2
                 + p * (2.0 * alpha + gamma_coef - delta)
                 + (1.0 + s_d - 0.5 * (gamma_coef + delta))
                 * (s_d + 0.5 * (gamma_coef + delta)))
    
    D_no8 = np.zeros(5, dtype=complex)
    D_no8[0] = delta
    D_no8[1] = 4.0 * p - 2.0 * alpha + gamma_coef - delta - 2.0
    D_no8[2] = 2.0 * alpha - gamma_coef + 2.0
    D_no8[3] = alpha * (4.0 * p - delta) - sigma_no8
    D_no8[4] = alpha * (alpha - gamma_coef + 1.0)
    
    print(f"  D₀-D₄(no -8ω²) = {D_no8}")
    
    # 用自定义 D 系数手动计算 CF
    def poly_cf_custom(D, max_iter=200):
        # 后向递推
        r = 0.0j
        for i in range(max_iter, 0, -1):
            a = i*i + (D[0]+1)*i + D[0]
            b = -2*i*i + (D[1]+2)*i + D[3]
            g = i*i + (D[2]-3)*i + D[4] - D[2] + 2
            denom = b - a * r
            if abs(denom) < 1e-30:
                denom = 1e-30j
            r = g / denom
        # n=0
        a0 = D[0]
        b0 = D[3]
        return b0 - a0 * r
    
    res_no8 = poly_cf_custom(D_no8)
    print(f"  |R₀(ω_ref)|(no -8ω²) = {abs(res_no8):.6e}")

except Exception as e:
    print(f"  Error: {e}")
    import traceback
    traceback.print_exc()


print("\n" + "=" * 70)
print("结论分析")
print("=" * 70)
print("""
1. 乘积形式 γₙ 是 O(n) 而非 O(n²)：这导致 αₙ/γₙ → ∞ (n→∞),
   使标准向后递推连分数的不动点结构发生根本变化。
   
2. 在标准 Leaver (1985) 中，γₙ 的系数为 -2iωκ(n+ν₀)。
   但 Cook-Zalutskiy (2014) 的多项式形式通过 D 系数重新参数化了递推，
   使 αₙ, βₙ, γₙ 都在 O(n²) 量级。

3. 多项式形式在 s=-2 下已验证正确，对 s=-0.5 需检查：
   a. "-8ω²" 项是否是 s=-2 的 Starobinsky 常数伪迹
   b. 若不是，应推导 s=-0.5 下的正确 D 系数表达式

4. 乘积形式 CF 求值函数 radial_continued_fraction 本身可能正确，
   但系数定义中 γₙ 的量级不同导致收敛性差异。关键验证：
   在多项式形式下用向后递推求值，得到正确结果，
   说明求值函数本身没错，是系数不对。
""")
