# -*- coding: utf-8 -*-
"""静默族修正体系全链一致性验证（2026-10-26）

轻子全链在"主导项 + 静默族修正"下的 σ 表：
  I_e  = 3e − σ³(1 + 16/15 + √(2/3)(1+6σ³))          （α_v 静默修正——局域假设 D）
  I_μ  = ln16 + e^{−3} + 144e^{−16}                   （ε_μ 静默修正）
  E_τ  = 16ln15 + (7/10)ln(16/15) − 8·144e^{−16}      （ε_μ 普适性——k=8 候选）
判别：体系一致性 vs 各链独立修正（过拟合权衡）。
"""
import math

sigma = 1/15; s3 = sigma**3; s4 = sigma**4
m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86
rel_e, rel_mu, rel_tau = 2.935e-8, 2.177e-8, 6.753e-5
G_N_rel = 2.2e-5; M_Pl_rel = G_N_rel/2; M_Pl_MeV = 1.220890e22
sE = math.sqrt(M_Pl_rel**2 + rel_tau**2)
rel_cross = math.sqrt(rel_e**2+rel_mu**2)

def grade(s):
    return "✓ 达标" if s <= 1 else ("～ 提示" if s <= 3 else "✗ 不达标")

# ---- 实验 ----
I_e_exp = math.log(m_tau_c/m_e_c)
I_mu_exp = math.log(m_tau_c/m_mu_c)
I_em_exp = math.log(m_mu_c/m_e_c)
E_exp = math.log(M_Pl_MeV/m_tau_c)

# ---- 体系 A：主导项（无修正）----
I_e0 = 3*math.e - s3*(1+16/15+math.sqrt(2/3))
I_mu0 = math.log(16) + math.e**(-3)
E0 = 16*math.log(15) + (7/10)*math.log(16/15)
print("=== 体系 A：主导项（无静默族修正）===")
print(f"  m_e/m_τ：σ_score = {abs(I_e0-I_e_exp)/rel_e:.3f} {grade(abs(I_e0-I_e_exp)/rel_e)}")
print(f"  m_μ/m_τ：σ_score = {abs(I_mu0-I_mu_exp)/rel_mu:.0f} {grade(abs(I_mu0-I_mu_exp)/rel_mu)}")
print(f"  E_τ：σ_score = {abs(E0-E_exp)/sE:.3f} {grade(abs(E0-E_exp)/sE)}")
print(f"  m_e/m_μ（无 m_τ）：σ_score = {abs((I_e0-I_mu0)-I_em_exp)/rel_cross:.0f} {grade(abs((I_e0-I_mu0)-I_em_exp)/rel_cross)}")
print()

# ---- 体系 B：静默族修正（α_v 修正 + ε_μ 两处）----
I_eB = 3*math.e - s3*(1+16/15+math.sqrt(2/3)*(1+6*s3))
I_muB = math.log(16) + math.e**(-3) + 144*math.e**(-16)
E_B = 16*math.log(15) + (7/10)*math.log(16/15) - 8*144*math.e**(-16)
print("=== 体系 B：静默族修正（α_v 6σ³ + ε_μ 144e^{−16}，k=8）===")
print(f"  m_e/m_τ：σ_score = {abs(I_eB-I_e_exp)/rel_e:.3f} {grade(abs(I_eB-I_e_exp)/rel_e)}")
print(f"  m_μ/m_τ：σ_score = {abs(I_muB-I_mu_exp)/rel_mu:.3f} {grade(abs(I_muB-I_mu_exp)/rel_mu)}")
print(f"  E_τ：σ_score = {abs(E_B-E_exp)/sE:.3f} {grade(abs(E_B-E_exp)/sE)}")
print(f"  m_e/m_μ（无 m_τ）：σ_score = {abs((I_eB-I_muB)-I_em_exp)/rel_cross:.2f} {grade(abs((I_eB-I_muB)-I_em_exp)/rel_cross)}")
print(f"  m_τ 绝对（M_Pl·e^{{−E_τ'}}）：{M_Pl_MeV*math.exp(-E_B):.2f} MeV vs {m_tau_c}")
print()

# ---- 体系 C：只用 ε_μ（不动 α_v）----
I_eC = I_e0
I_muC = I_mu0 + 144*math.e**(-16)
E_C = E0 - 8*144*math.e**(-16)
print("=== 体系 C：仅 ε_μ 修正（α_v 不动）===")
print(f"  m_e/m_τ：σ_score = {abs(I_eC-I_e_exp)/rel_e:.3f} {grade(abs(I_eC-I_e_exp)/rel_e)}")
print(f"  m_μ/m_τ：σ_score = {abs(I_muC-I_mu_exp)/rel_mu:.3f} {grade(abs(I_muC-I_mu_exp)/rel_mu)}")
print(f"  E_τ：σ_score = {abs(E_C-E_exp)/sE:.3f} {grade(abs(E_C-E_exp)/sE)}")
print(f"  m_e/m_μ（无 m_τ）：σ_score = {abs((I_eC-I_muC)-I_em_exp)/rel_cross:.2f} {grade(abs((I_eC-I_muC)-I_em_exp)/rel_cross)}")
print()

print("=== 判别 ===")
print("B vs A：所有链 σ 全面改善（除 m_e/m_μ 残余 12.6σ_score 在 I_e 侧）——但含 2 个修正参数")
print("C vs A：仅 ε_μ（1 参数）改善 m_μ/E_τ/m_e-m_μ——I_e 侧残余不变（12.6σ_score）")
print("诚实：B 的 α_v 修正（6σ³）是后验拟合——'改善'不能作为'验证'——需机制导出或独立预言")
