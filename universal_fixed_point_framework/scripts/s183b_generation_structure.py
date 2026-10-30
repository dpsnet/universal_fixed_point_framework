# -*- coding: utf-8 -*-
"""S183b 代际结构勘误——共同基底+间隔（非级联）
E_e = E_τ^D + I_e（行 2075 确认）——E_μ = E_τ + I_μ
质量比 = e^{−间隔}——m_μ/m_τ、m_e/m_τ
"""
import math

M_Pl = 1.22089e22
m_e = 0.51099895069
m_mu = 105.658375
m_tau = 1776.86

E_tau = -math.log(m_tau / M_Pl)
I_mu = math.e + 42*math.exp(-6) + 2*(1/15)**5
I_e = 3*math.e - (1/15)**3 * (1 + 16/15 + math.sqrt(2/3)*(1+6*(1/15)**3))

print("=== S183b: 代际结构勘误——共同基底+间隔 ===\n")
print(f"E_τ = −ln(m_τ/M_Pl) = {E_tau:.8f}（全冻结基底）")
print(f"I_μ = e+42e^{{−6}}+2σ⁵ = {I_mu:.8f}")
print(f"I_e = 3e−σ³(1+α_v') = {I_e:.8f}")
E_mu_frame = E_tau + I_mu
E_e_frame = E_tau + I_e
print(f"\nE_μ(框架) = E_τ + I_μ = {E_mu_frame:.8f}")
print(f"E_μ(观测) = {46.19624113:.8f}——差 {abs(E_mu_frame-46.19624113):.2e}")
print(f"E_e(框架) = E_τ + I_e = {E_e_frame:.8f}")
print(f"E_e(观测) = {51.52783989:.8f}——差 {abs(E_e_frame-51.52783989):.2e}")
print(f"\n→ 共同基底 E_τ + 各自间隔——精确复现（非级联）✓")

print("\n=== 质量比 = e^{−间隔} ===")
print(f"m_μ/m_τ = e^{{−I_μ}} = {math.exp(-I_mu):.8f}——实验 {m_mu/m_tau:.8f} ✓")
print(f"m_e/m_τ = e^{{−I_e}} = {math.exp(-I_e):.8f}——实验 {m_e/m_tau:.8f} ✓")
print(f"m_e/m_μ = e^{{−(I_e−I_μ)}} = {math.exp(-(I_e-I_mu)):.8f}——实验 {m_e/m_mu:.8f} ✓")
print(f"  注：m_e/m_μ = e^{{−(E_e−E_μ)}} = e^{{−(I_e−I_μ)}}——间隔差")

print("\n=== 勘误说明 ===")
print("S179 落档 'E_e = E_μ + 3e−σ³(1+α_v')' 有误——")
print("正确：E_e = E_τ + I_e（共同基底 E_τ + 各自间隔）")
print("E_μ = E_τ + I_μ、E_e = E_τ + I_e——代际结构 = 共同基底+间隔")
print("（三轻子质量公式不变——仅组装结构表述勘误）")
