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
测试复 nu0 乘积形式在 Dirac 参考频率处的连分数残差。
"""
import numpy as np

def nu0_correct(s, omega, a=0.0, m=0.0, M=1.0):
    root = np.sqrt(max(0.0, M*M - a*a))
    r_p = M + root
    r_m = M - root
    return -s - 1j * (omega * r_p - a * m) / (r_p - r_m)

def alpha_product(n, nu0):
    return (n + 1) * (n + 2*nu0 + 1)

def beta_product(n, omega, lam, a, m, nu0):
    t1 = -lam - n*(n + 2*nu0 + 1) + omega**2
    denom = n + nu0
    t2 = a*m*(m + 2*nu0)/denom if abs(denom) > 1e-15 else 0j
    t3 = 2.0*a*omega*m
    denom2 = 2.0*n + 2.0*nu0 + 1.0
    t4 = -2.0*a*m*omega*(n+nu0)/denom2 if abs(denom2) > 1e-15 else 0j
    return t1 + t2 + t3 + t4

def gamma_product(n, omega, a, M, nu0):
    root = np.sqrt(max(0.0, M*M - a*a))
    r_p = M + root
    r_m = M - root
    kappa = (r_p - r_m) / (2.0*(r_p**2 + a**2))
    return -2j*omega*kappa*(n + nu0)

def continued_fraction(omega, lam, a, m, M=1.0, N_max=300):
    s = -0.5
    nu0 = nu0_correct(s, omega, a, m, M)

    a0 = alpha_product(0, nu0)
    n_start = 1 if abs(a0) < 1e-30 else 0

    r = 0.0j
    for n in range(N_max, n_start, -1):
        a_n = alpha_product(n, nu0)
        b_n = beta_product(n, omega, lam, a, m, nu0)
        g_n = gamma_product(n, omega, a, M, nu0)
        if abs(a_n) < 1e-30: continue
        denom = b_n - a_n * r
        if abs(denom) < 1e-30: denom = 1e-30j
        r = g_n / denom

    a_s = alpha_product(n_start, nu0)
    b_s = beta_product(n_start, omega, lam, a, m, nu0)
    return b_s - a_s * r


print("复 nu0 乘积形式连分数在 Dirac 参考频率处:")
print(f"{'k':<4} {'l':<6} {'|R0|(N=100)':<16} {'|R0|(N=300)':<16}")
print("-" * 42)

ref_table = {
    1: (0.378721 - 0.096458j, 1.0),
    2: (0.522988 - 0.089964j, 4.0),
    3: (0.640418 - 0.091694j, 9.0),
    4: (0.743499 - 0.092667j, 16.0),
}

for kappa, (omega_ref, lam) in ref_table.items():
    r100 = continued_fraction(omega_ref, lam, 0.0, 0.5, N_max=100)
    r300 = continued_fraction(omega_ref, lam, 0.0, 0.5, N_max=300)
    print(f"  {kappa:<4d} {kappa-0.5:<+4.1f}  {abs(r100):<16.6e} {abs(r300):<16.6e}")

# 另外：测试简并 nu0=-s 的差异
print()
print("对比 nu0=-s (简单) vs nu0 复 (正确):")
for kappa, (omega_ref, lam) in ref_table.items():
    nu0_s = 0.5  # -(-0.5)
    nu0_c = nu0_correct(-0.5, omega_ref, 0.0, 0.5)
    print(f"  k={kappa}: nu0_simple={nu0_s}, nu0_complex={nu0_c}")
