# -*- coding: utf-8 -*-
"""S143 冻结乘法级联完整指数化——数值先证伪（模式 8）
Ω_τ = e^{E_τ^D} = 15^16 · (16/15)^{7/10} · e^{−8ε_μ} · e^{−(σ⁵−e^{−16})} · e^{−2σ⁸(1+σ)}
ε_μ = 144·e^{−16}(1+6σ³)——E_τ^D 四阶截断——断言：exp(E_τ^D) = 乘法级联"""
import numpy as np

σ = 1/15
ε_μ = 144 * np.exp(-16) * (1 + 6*σ**3)
σ5 = σ**5
e16 = np.exp(-16)
σ8 = σ**8

E_main = 16*np.log(15) + (7/10)*np.log(16/15)
E_D = E_main - 8*ε_μ - (σ5 - e16) - 2*σ8*(1+σ)

print("=== 组件 ===")
print(f"ε_μ        = {ε_μ:.15e}")
print(f"σ⁵         = {σ5:.15e}")
print(f"e^-16      = {e16:.15e}")
print(f"σ⁵-e^-16   = {σ5-e16:.15e}")
print(f"2σ⁸(1+σ)   = {2*σ8*(1+σ):.15e}")
print(f"16ln15     = {16*np.log(15):.15f}")
print(f"(7/10)ln(16/15) = {(7/10)*np.log(16/15):.15f}")
print(f"E_main     = {E_main:.15f}")
print(f"E_τ^D      = {E_D:.15f}")

print("\n=== 指数 vs 级联 ===")
lhs = np.exp(E_D)
rhs = (15.0**16) * (16/15)**(7/10) * np.exp(-8*ε_μ) * np.exp(-(σ5-e16)) * np.exp(-2*σ8*(1+σ))
print(f"e^{{E_τ^D}}      = {lhs:.15e}")
print(f"级联        = {rhs:.15e}")
print(f"残差(lhs-rhs) = {lhs-rhs:.3e}")
print(f"相对残差     = {(lhs-rhs)/lhs:.3e}")

print("\n=== 逐因子核对 ===")
f1 = 15.0**16
f2 = (16/15)**(7/10)
f3 = np.exp(-8*ε_μ)
f4 = np.exp(-(σ5-e16))
f5 = np.exp(-2*σ8*(1+σ))
print(f"15^16          = {f1:.15e}")
print(f"(16/15)^(7/10) = {f2:.15e}")
print(f"e^-8ε_μ        = {f3:.15e}")
print(f"e^-(σ⁵-e^-16)  = {f4:.15e}")
print(f"e^-2σ⁸(1+σ)    = {f5:.15e}")
print(f"级联乘积       = {f1*f2*f3*f4*f5:.15e}")
print(f"Ω_τ(S131)      = 6.871053e18 (对照)")

print("\n=== 分块 exp 核对（与 Lean 目标右侧同形） ===")
rhs_lean_form = f1 * np.exp((7/10)*np.log(16/15)) * np.exp(-8*ε_μ) * np.exp(-(σ5-e16)) * np.exp(-2*σ8*(1+σ))
print(f"exp 形式级联   = {rhs_lean_form:.15e}")
print(f"残差           = {lhs-rhs_lean_form:.3e}")
rel = abs(lhs-rhs_lean_form)/lhs
print(f"相对残差       = {rel:.3e}")
print(f"PASS = {rel < 1e-12}  (相对容差——1e18 量级用绝对容差无意义)")
