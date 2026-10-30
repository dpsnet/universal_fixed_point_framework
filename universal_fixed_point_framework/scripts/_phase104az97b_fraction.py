# -*- coding: utf-8 -*-
"""104az-97 复核：两处 False 用精确有理数（Fraction）判别——排除 Decimal 舍入假阴性"""
from fractions import Fraction

Ngen = 3
kmax = 8
sigma = Fraction(1, 15)
silent = kmax - 3
b0 = Fraction(11*3 - 2*3, 3)
d1 = sigma**2 / Ngen
d2 = sigma**3 * silent

print("[A] beta0*delta = N_gen*sigma^2 = 1/(N_gen*静默^2)?")
v1 = b0 * d1
v2 = Fraction(1, Ngen * silent**2)
print(f"  {v1} == {v2}? {v1 == v2}  (=1/75)")

print("[B] 319/648000 = sigma^2/N_gen^2 * (1-1/320)?")
r = Fraction(319, 648000)
c1 = sigma**2 / Ngen**2 * (1 - Fraction(1, 320))
print(f"  {r} == {c1}? {r == c1}")

print("[C] 复核 delta 双身份 + 织-修连接")
print(f"  sigma^2/N_gen == sigma^3*静默? {sigma**2/Ngen == sigma**3*silent}")
print(f"  beta0*delta == N_gen*sigma^2? {b0*d1 == Fraction(Ngen)*sigma**2}")

print("[D] 层级规则数值核对")
print(f"  F_np 修正 675 = N_gen^3*静默^2 = {Fraction(Ngen)**3*silent**2}")
print(f"  m_s/T_c 修正 320 = 静默*k_max^2 = {silent*kmax**2}")
print(f"  648000 = 320*2025 = 静默·k_max² × (N_gen·σ⁻¹)² = {5*64}×{45**2} = {5*64*45**2}")
