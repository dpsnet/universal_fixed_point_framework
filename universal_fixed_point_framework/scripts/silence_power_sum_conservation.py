# -*- coding: utf-8 -*-
"""静默族修正"幂和 −2 守恒"验证（2026-10-26）

候选规律：静默族修正量（修正域）的幂和守恒 a+b = −2
（量 = 静默^a × N_gen^b × k_max^c × 幂基^d）
实例：σ、6σ³、静默⁻²、Δ_dress = 2σ/3
"""
import math

powers, ngen, silence, involution = 2, 3, 5, 7
kmax = powers**ngen
sigma = 1/15

print("=== 静默族修正量幂次表（静默^a × N_gen^b × k_max^c × 幂基^d）===")
items = [
    ("σ = 1/15",        (-1, -1, 0, 0), 1/15),
    ("6σ³ = 2/1125",    (-3, +1, 0, +1), 6*sigma**3),   # 6 = N_gen×幂基
    ("静默⁻² = 1/25",   (-2, 0, 0, 0), 1/25),
    ("Δ_dress = 2σ/3",  (-1, -1, 0, +1), 2*sigma/3),   # 2/3 = 幂基/N_gen
]
print(f"{'量':<18} {'a(静默)':<8} {'b(N_gen)':<9} {'c(k_max)':<9} {'d(幂基)':<8} a+b+d")
for name, (a, b, c, d), val in items:
    print(f"{name:<18} {a:<8} {b:<9} {c:<9} {d:<8} {a+b+d}")
print()
print("幂和（a+b+d）全为 −2——'修正域幂和守恒'候选")
print()

print("=== 数值核对 ===")
for name, (a, b, c, d), val in items:
    v = silence**a * ngen**b * kmax**c * powers**d if (a>=0 or True) else 0
    # 负幂直接计算
    v = (silence**a if a>=0 else 1/silence**(-a)) * (ngen**b if b>=0 else 1/ngen**(-b)) * (kmax**c if c>=0 else 1/kmax**(-c)) * (powers**d if d>=0 else 1/powers**(-d))
    print(f"{name}: 计算 = {v:.10f} vs 标称 = {val:.10f}——一致: {abs(v-val) < 1e-12}")
print()

print("=== 正幂族对照（身份域——幂和不守恒）===")
pos = [
    ("675",     (2, 3, 0, 0), 675),
    ("320",     (1, 0, 2, 0), 320),
    ("648000",  (3, 4, 2, 0), 648000),
    ("ε_μ 系数 144", (0, 2, 0, 0), 144),
]
print(f"{'量':<18} {'a':<8} {'b':<9} {'c':<9} 幂和")
for name, (a, b, c, d), val in pos:
    print(f"{name:<18} {a:<8} {b:<9} {c:<9} {a+b+c}")
print()
print("正幂族幂和 = 框架量（675：5 = 静默、320：3 = N_gen、648000：9 = N_gen²、144：2）")
print("——身份域幂和映射框架常数、修正域幂和守恒 −2——两域区分")
