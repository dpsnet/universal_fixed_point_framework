#!/usr/bin/env python3
"""
Paper XXXIX 补缺: N_{R⁴} 精确闭式验证 (2026-08-04)
====================================================

问题:
  paper39 定理 3.2 中 N_{R⁴} 仅为量级估计 |N_{R⁴}| ≲ 0.1。
  本脚本推导并验证 N_{R⁴} 的精确闭式:

  谱势 R⁴ 修正 (Phase 42):
    V(φ) = V₀ (1 - e^{-bφ})² · (1 + δ₂·e^{-2bφ} + ...),  δ₂ = c₃/c₁²
  对慢滚积分 N_e = ∫ (V/V') dφ 的一阶 δ₂ 贡献:

    N_{R⁴} = (3δ₂/4)·[ ln(x_cmb/x_end) - 2(x_cmb - x_end) + (x_cmb² - x_end²)/2 ]

  其中 x = e^{-bφ}, x_end = e^{-bφ_end} = √3/(2+√3), x_cmb = e^{-bφ_cmb},
  φ_cmb 由 N_e(φ_cmb) = 55 闭式确定。

  验证方式: 闭式 vs 数值积分 ∫ (V_R4 - V_0)/... 直接积分。
"""

import numpy as np
from math import sqrt, log, exp

# 谱参数 (Phase 42 / Phase 36)
c1 = 25.1948   # R² 系数
c3 = 4.7240    # R⁴ 系数
b = sqrt(2.0/3.0)   # Starobinsky 斜率
N_target = 55.0     # CMB 尺度 e 折叠数

# δ₂: R⁴ 修正相对强度 (注释: δ_n ∝ c_{n+1}/c₁^n)
delta2 = c3 / (c1**2)

# 暴胀结束 (命题 2.1): e^{-bφ_end} = √3/(2+√3)
x_end = sqrt(3.0) / (2.0 + sqrt(3.0))
phi_end = -log(x_end) / b

# φ_cmb: 闭式 (3/4)(e^{bφ} - bφ) = N_target + N_end
N_end = 0.75 * (exp(b*phi_end) - b*phi_end)

def F(phi):
    return 0.75 * (exp(b*phi) - b*phi)

# 数值解 φ_cmb
phi_cmb = 1.0
for _ in range(60):
    phi_cmb = phi_cmb - (F(phi_cmb) - (N_target + N_end)) / (0.75 * (b*exp(b*phi_cmb) - b))
x_cmb = exp(-b*phi_cmb)

# ---- 精确闭式 ----
N_R4_closed = (3*delta2/4.0) * (log(x_cmb/x_end) - 2*(x_cmb - x_end) + (x_cmb**2 - x_end**2)/2.0)

# ---- 数值积分验证 ----
# V = V₀(1-x)²(1+δ₂x²);  e 折叠数 N = ∫ V/V' dφ
# V/V' 精确 (含 δ₂): (1-x)(1+δ₂x²) / [2b·x·(1-δ₂x+2δ₂x²)]
# N_{R⁴} = ∫ [V_R4/V_R4' - V_0/V_0'] dφ 在 [φ_cmb, φ_end]

def integrand_diff(phi):
    x = exp(-b*phi)
    # R⁴ 势的 V/V'
    rr4 = (1-x)*(1+delta2*x**2) / (2*b*x*(1 - delta2*x + 2*delta2*x**2))
    # 纯 R² 势的 V/V'
    r0 = (1-x) / (2*b*x)
    return rr4 - r0

# 高斯积分 (足够精度)
N = 4000
phis = np.linspace(phi_cmb, phi_end, N)
vals = np.array([integrand_diff(p) for p in phis])
N_R4_numeric = np.trapz(vals, phis)

print("="*70)
print("  N_{R⁴} 精确闭式验证 (Paper XXXIX 补缺)")
print("="*70)
print(f"  b            = {b:.6f}")
print(f"  c₁ (R²)      = {c1:.4f}")
print(f"  c₃ (R⁴)      = {c3:.4f}")
print(f"  δ₂ = c₃/c₁²  = {delta2:.6f}")
print(f"  φ_end        = {phi_end:.6f}")
print(f"  φ_cmb        = {phi_cmb:.6f}  (N_e = {N_target})")
print(f"  x_end        = {x_end:.6f}")
print(f"  x_cmb        = {x_cmb:.6f}")
print("-"*70)
print(f"  N_R4 闭式 (解析)   = {N_R4_closed:+.8f}")
print(f"  N_R4 数值积分     = {N_R4_numeric:+.8f}")
print(f"  相对偏差               = {abs(N_R4_closed - N_R4_numeric)/abs(N_R4_numeric)*100:.4f}%")
print("-"*70)
print(f"  |N_R4| 量级: 精确闭式 {abs(N_R4_closed):.4f}  (原估计 ≲ 0.1)")
print(f"  对 N_e 相对影响: {abs(N_R4_closed)/N_target*100:.4f}%")

# 主导项检查: (3δ₂/4)·ln(x_cmb/x_end)
N_R4_leading = (3*delta2/4.0)*log(x_cmb/x_end)
print("-"*70)
print(f"  主导项 (3δ₂/4)ln(x_cmb/x_end) = {N_R4_leading:+.8f}")
print(f"  次主导修正占比 = {abs(N_R4_closed-N_R4_leading)/abs(N_R4_closed)*100:.4f}%")

ok = abs(N_R4_closed - N_R4_numeric)/abs(N_R4_numeric) < 1e-3
print("-"*70)
print(f"  检验: {'✅ PASS (闭式与数值一致，相对偏差 < 0.1%)' if ok else '❌ FAIL'}")
