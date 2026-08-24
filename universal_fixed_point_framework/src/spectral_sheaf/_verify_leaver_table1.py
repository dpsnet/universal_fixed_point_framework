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
_verify_leaver_table1.py —— 验证乘积形式系数 vs Leaver (1985) Table 1

Leaver Table 1 (Schwarzschild a=0):

    s=-2:  α₀=0, α₁=-4,  αₙ=n²-2n-3 (n≥2)
           βₙ=-λ-2n²+4n-1
           γₙ=-2iω(n-2)

    s=-1:  α₀=0, α₁=-2,  αₙ=n²-1 (n≥2)
           βₙ=-λ-2n²+1
           γₙ=-2iω(n-1)

    s=0:   α₀=0, α₁=0,   αₙ=n²+2n+1 (n≥2)
           βₙ=-λ-2n²-2n
           γₙ=-2iωn

比较 _spin_weight_coeff.py 和 _dirac_leaver_solver.py 的实现。
"""

import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _spin_weight_coeff import (
    frobenius_index, alpha_n, beta_n, gamma_n, recurrence_coeffs
)
from _dirac_leaver_solver import (
    dirac_alpha_n, dirac_beta_n, dirac_gamma_n, dirac_recurrence_coeffs
)

M = 1.0
a = 0.0
omega = 0.373672 - 0.088962j  # s=-2 参考值
lam_g = 4.0  # s=-2, l=2

print("=" * 80)
print("验证 1: α₀ 在 Leaver 原文中定义为 0（对所有 s）")
print("=" * 80)

for s_label, s_val, src_func in [
    ("s=-2 (spin_weight)", -2, alpha_n),
    ("s=-1 (spin_weight)", -1, alpha_n),
    ("s=0  (spin_weight)", 0, alpha_n),
    ("s=-0.5 (dirac)", -0.5, dirac_alpha_n),
]:
    a0 = src_func(s_val, 0)
    status = "✓ α₀=0" if abs(a0) < 1e-15 else f"✗ α₀={a0} (应为 0, Leaver 明文定义)"
    print(f"  {s_label:25s}: fν₀={frobenius_index(s_val):5.1f} → α₀={complex(a0):.1f}  {status}")

print("\n" + "=" * 80)
print("验证 2: s=-2, a=0 的系数 vs Leaver Table 1")
print("=" * 80)

ref_coeffs = {
    # n: (α_ref, β_ref, γ_ref)
    0: (0, -lam_g - 1, -2j*omega*(-2)),
    1: (-4, -lam_g - 2 + 4 - 1, -2j*omega*(-1)),
    2: (1-1, -lam_g - 8 + 8 - 1, -2j*omega*(0)),
    3: (9-6-3, -lam_g - 18 + 12 - 1, -2j*omega*(1)),
    5: (25-10-3, -lam_g - 50 + 20 - 1, -2j*omega*(3)),
}

print(f"  {'n':>3} | {'α(code)':>15} {'α(Table1)':>15} {'diff':>10} | "
      f"{'β(code)':>20} {'β(Table1)':>20} {'diff':>12} | "
      f"{'γ(code)':>15} {'γ(Table1)':>15} {'diff':>10}")
print("  " + "-" * 110)

for n in [0, 1, 2, 3, 5]:
    a_code, b_code, g_code = recurrence_coeffs(-2, n, omega, lam_g, a, 0, M)
    a_ref, b_ref, g_ref = ref_coeffs[n]
    
    da = abs(a_code - a_ref)
    db = abs(b_code - b_ref)
    dg = abs(g_code - g_ref)
    
    print(f"  {n:3d} | {complex(a_code):>15.6f} {a_ref:>15.1f} {da:>10.2e} | "
          f"{complex(b_code):>20.10f} {b_ref:>20.10f} {db:>12.2e} | "
          f"{complex(g_code):>15.6f} {g_ref:>15.6f} {dg:>10.2e}")

print("\n" + "=" * 80)
print("验证 3: s=-0.5, a=0 的系数——确认公式结构是否与 Table 1 模式一致")
print("=" * 80)

s_d = -0.5
lam_d = 1.0  # l=1/2, s=-1/2 → a=0 值
omega_d = 0.378721 - 0.096458j

# 基于 Leaver 模式的预期系数（外推）
# β_pattern: Leaver 中 βₙ ~ -λ - 2n² + C₁n + C₂
# 对 s=-2: βₙ = -λ - 2n² + 4n - 1
# 对 s=-1: βₙ = -λ - 2n² + 0n + 1
# 对 s=0:  βₙ = -λ - 2n² - 2n + 0
# 线性外推: s=ν₀ 时 C₁ = 2-2ν₀, C₂ = 2ν₀-1? 

print(f"\n  {'n':>3} | {'α(dirac)':>15} | {'β(dirac)':>25} | {'γ(dirac)':>20}")
print("  " + "-" * 65)

for n in range(6):
    a_n, b_n, g_n = dirac_recurrence_coeffs(s_d, n, omega_d, lam_d, a, 0.5, M)
    print(f"  {n:3d} | {complex(a_n):>15.6f} | {complex(b_n):>25.15f} | {complex(g_n):>20.10f}")

# N 收敛性测试：Dirac CF 在参考频率处的残差
print("\n" + "=" * 80)
print("验证 4: Dirac CF 的 N 收敛性")
print("=" * 80)

def radial_cf_general(nu0_func, alpha_func, beta_func, gamma_func,
                      s, omega, lam, a, m, M, N_max=200):
    """通用径向 CF 求值器，支持自定义系数函数。"""
    nu0 = nu0_func(s, omega, a, m, M)
    # α₀ = 0 是 Leaver 定义（对所有 s）
    # 但实际上 α₀ 由公式给出，我们按公式计算
    # 但 α₀ 应该始终为 0（Leaver 定义）
    a_0 = alpha_func(s, 0, omega, a, m, M)
    alpha0_zero = abs(a_0) < 1e-15
    
    n_start = 1 if alpha0_zero else 0
    
    r = 0.0j
    for n in range(N_max, n_start, -1):
        a_n = alpha_func(s, n, omega, a, m, M)
        b_n = beta_func(s, n, omega, lam, a, m, M)
        g_n = gamma_func(s, n, omega, a, m, M)
        
        if abs(a_n) < 1e-30:
            continue
        denom = b_n - a_n * r
        if abs(denom) < 1e-30:
            denom = 1e-30j
        r = g_n / denom
    
    a_s = alpha_func(s, n_start, omega, a, m, M)
    b_s = beta_func(s, n_start, omega, lam, a, m, M)
    return b_s - a_s * r


for nu0_label, nu0_func in [
    ("ν₀=-s (real, _spin_weight)", 
     lambda s, o, a, m, M: frobenius_index(s)),
    ("ν₀=-s-i(ωr₊-am)/(r₊-r₋) (complex)", 
     lambda s, o, a, m, M: -s - 1j*(o*max(M, (M+np.sqrt(max(0,M**2-a**2)))) - a*m)/max(1e-15, 2*np.sqrt(max(0,M**2-a**2)))),
]:
    for s_test, lam_test, m_test, omega_test, label in [
        (-2, 4.0, 0, 0.373672 - 0.088962j, "s=-2"),
        (-0.5, 1.0, 0.5, 0.378721 - 0.096458j, "s=-0.5"),
    ]:
        r100 = radial_cf_general(
            nu0_func,
            lambda s,n,o,a,m,M: (n+1)*(n+2*nu0_func(s,o,a,m,M)+1),
            lambda s,n,o,l,a,m,M: -l - n*(n+2*nu0_func(s,o,a,m,M)+1) + o**2,
            lambda s,n,o,a,m,M: -2j*o*(max(M, np.sqrt(max(0,M**2-a**2))) - M)/(2*(max(M, np.sqrt(max(0,M**2-a**2)))**2 + a**2))*(n+nu0_func(s,o,a,m,M)),
            s_test, omega_test, lam_test, 0.0, m_test, M, N_max=100
        )
        r300 = radial_cf_general(
            nu0_func,
            lambda s,n,o,a,m,M: (n+1)*(n+2*nu0_func(s,o,a,m,M)+1),
            lambda s,n,o,l,a,m,M: -l - n*(n+2*nu0_func(s,o,a,m,M)+1) + o**2,
            lambda s,n,o,a,m,M: -2j*o*(max(M, np.sqrt(max(0,M**2-a**2))) - M)/(2*(max(M, np.sqrt(max(0,M**2-a**2)))**2 + a**2))*(n+nu0_func(s,o,a,m,M)),
            s_test, omega_test, lam_test, 0.0, m_test, M, N_max=300
        )
        print(f"  [{label}] {nu0_label}")
        print(f"    |R₀(ω_ref)|(N=100) = {abs(r100):.6e}")
        print(f"    |R₀(ω_ref)|(N=300) = {abs(r300):.6e}")

if __name__ == "__main__":
    pass
