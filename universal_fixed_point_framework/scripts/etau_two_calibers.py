# -*- coding: utf-8 -*-
"""E_τ 两种口径的 σ_score 对照（2026-10-26）

裸 E_τ^new = 16ln15+(7/10)ln(16/15) vs 体系 B''' E_τ = E_τ^new − 8ε_μ
"""
import math

M_Pl_MeV = 1.220890e22
m_tau_c = 1776.86
M_Pl_rel = 1.1e-5
d_tau_rel = 0.12/m_tau_c
sE = math.sqrt(M_Pl_rel**2 + d_tau_rel**2)
E_exp = math.log(M_Pl_MeV/m_tau_c)

E_new = 16*math.log(15) + (7/10)*math.log(16/15)
eps_mu = 144*math.exp(-16)*(1+6*(1/15)**3)
E_B = E_new - 8*eps_mu

print("=== E_τ 两种口径 σ_score 对照 ===")
print(f"E_exp = ln(M_Pl/m_τ) = {E_exp:.10f}、δE = {sE:.2e}")
print(f"裸 E_τ^new = {E_new:.10f}：σ_score = {abs(E_new-E_exp)/sE:.3f}（提示级）")
print(f"ε_μ = 144e^{{-16}}(1+6σ³) = {eps_mu:.10f}")
print(f"8ε_μ = {8*eps_mu:.6e}")
print(f"体系B E_τ = E_τ^new−8ε_μ = {E_B:.10f}：σ_score = {abs(E_B-E_exp)/sE:.3f}（达标）")
print()
print("→ 熵身份（16ln15 = 惊奇度和）针对裸 E_τ^new——其 σ_score = 1.916 提示级")
print("→ 体系 B''' 的 E_τ（−8ε_μ）σ_score = 0.018 达标——两个口径并存需区分")
