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

"""验证二次多项式系数的正确性 - 比较不同公式"""
import cmath
import numpy as np

M = 1.0
a = 0.0
s = -2
l = 2
omega = complex(0.373672, -0.088962)
epsilon_grav = 3.0  # 引力扰动

b = cmath.sqrt(M**2 - a**2)
r_plus = M + b
r_minus = M - b

print("=" * 60)
print("比较不同的二次系数公式")
print("=" * 60)
print(f"omega = {omega.real:.6f} {omega.imag:.6f}i")
print(f"a = {a}, M = {M}, s = {s}, l = {l}")
print()

# 方案1: Leaver 1991 (Schwarzschild)
print("--- 方案1: Leaver 1991 (Schwarzschild) ---")
omega_leaver = 2.0 * M * omega
rho = -1j * omega_leaver

def alpha_1991(n):
    return n**2 + (2.0 * rho + 2.0) * n + 2.0 * rho + 1.0

def beta_1991(n):
    return -(2.0 * n**2 + (8.0 * rho + 2.0) * n + 8.0 * rho**2 + 4.0 * rho + l * (l + 1.0) - epsilon_grav)

def gamma_1991(n):
    return n**2 + 4.0 * rho * n + 4.0 * rho**2 - epsilon_grav - 1.0

print(f"Leaver 单位制: omega_leaver = {omega_leaver.real:.6f} {omega_leaver.imag:.6f}i")
print(f"rho = {rho.real:.6f} {rho.imag:.6f}i")
print()

# 方案2: 总结中的 c0-c6 公式
print("--- 方案2: 总结中的 c0-c6 公式 ---")
sigma_plus = (omega * r_plus - s * a) / (2.0 * b)  # 不对, 应该是 m?
sigma_plus = (omega * r_plus - 0 * a) / (2.0 * b)  # m=0
epsilon = 2.0 * omega * M
Omega = omega * b

A_lm = l * (l + 1) - s * (s + 1)

c0 = 1.0 - s - 2.0j * sigma_plus - 2.0j * Omega + 2.0j * epsilon
c1 = 4.0j * sigma_plus - 2.0 * s
c2 = (A_lm + s * (s + 1.0) - 4.0 * omega**2 * M * (M + b)
      - 2.0 * a * 0 * omega  # m=0
      - 2.0j * sigma_plus * (1.0 - s - 2.0j * sigma_plus - 2.0j * Omega + 4.0j * epsilon))
c3 = 1.0 + c1 + 4.0j * Omega - 4.0j * epsilon
c4 = c2 + (2.0j * Omega - 2.0j * epsilon) * (1.0 - s - 2.0j * sigma_plus) + 2.0j * epsilon
c5 = 4.0j * Omega - 2.0 * s
c6 = -4.0 * Omega**2 - 4.0j * Omega * epsilon + 4.0j * Omega * sigma_plus - 2.0 * s * 1.0j * Omega

def alpha_c(n):
    return n**2 + (c1 + 1.0) * n + c0

def beta_c(n):
    return -2.0 * n**2 - c3 * n - c4

def gamma_c(n):
    return n**2 + c5 * n + c6

print(f"sigma_plus = {sigma_plus.real:.6f} {sigma_plus.imag:.6f}i")
print(f"epsilon = {epsilon.real:.6f} {epsilon.imag:.6f}i")
print(f"Omega = {Omega.real:.6f} {Omega.imag:.6f}i")
print(f"A_lm = {A_lm}")
print()
print(f"c0 = {c0.real:.6f} {c0.imag:.6f}i")
print(f"c1 = {c1.real:.6f} {c1.imag:.6f}i")
print(f"c2 = {c2.real:.6f} {c2.imag:.6f}i")
print(f"c3 = {c3.real:.6f} {c3.imag:.6f}i")
print(f"c4 = {c4.real:.6f} {c4.imag:.6f}i")
print(f"c5 = {c5.real:.6f} {c5.imag:.6f}i")
print(f"c6 = {c6.real:.6f} {c6.imag:.6f}i")
print()

# 比较系数
print("--- 系数比较 ---")
for n in [0, 1, 2, 5]:
    print(f"n = {n}:")
    
    a1 = alpha_1991(n)
    a2 = alpha_c(n)
    print(f"  alpha: 1991={a1.real:.4f}{a1.imag:+.4f}i, c_form={a2.real:.4f}{a2.imag:+.4f}i, 比值={abs(a1/a2):.4f}")
    
    b1 = beta_1991(n)
    b2 = beta_c(n)
    print(f"  beta:  1991={b1.real:.4f}{b1.imag:+.4f}i, c_form={b2.real:.4f}{b2.imag:+.4f}i, 比值={abs(b1/b2):.4f}")
    
    g1 = gamma_1991(n)
    g2 = gamma_c(n)
    print(f"  gamma: 1991={g1.real:.4f}{g1.imag:+.4f}i, c_form={g2.real:.4f}{g2.imag:+.4f}i, 比值={abs(g1/g2):.4f}")
    print()

# 计算连分数残差
print("--- 连分数残差比较 ---")
max_iter = 300

# 方案1的残差
cf1 = 0.0j
for n in range(max_iter, -1, -1):
    numer = alpha_1991(n) * gamma_1991(n + 1)
    denom = beta_1991(n + 1) - cf1
    if abs(denom) < 1e-30:
        denom = 1e-30
    cf1 = numer / denom
res1 = beta_1991(0) - cf1
print(f"方案1 (Leaver 1991) 残差: {abs(res1):.2e}")

# 方案2的残差
cf2 = 0.0j
for n in range(max_iter, -1, -1):
    numer = alpha_c(n) * gamma_c(n + 1)
    denom = beta_c(n + 1) - cf2
    if abs(denom) < 1e-30:
        denom = 1e-30
    cf2 = numer / denom
res2 = beta_c(0) - cf2
print(f"方案2 (c0-c6公式) 残差: {abs(res2):.2e}")

# 方案1 + 方案2的比值
print()
print(f"残差比值 (方案2/方案1): {abs(res2/res1):.4f}")
