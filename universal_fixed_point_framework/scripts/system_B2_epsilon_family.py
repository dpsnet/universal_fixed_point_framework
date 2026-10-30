# -*- coding: utf-8 -*-
"""体系 B''：ε_μ 家族修正验证（2026-10-26）

竞争判别：I_e 失配（−4.32e-7）的归因
  候选 X（α_v 修正）：√(2/3)(1+6σ³)——贡献 4.300e-7（残余 −0.46%）
  候选 Y（ε_e 修正）：I_e += −ε_μ×2/75——贡献 4.329e-7（残余 −0.21%——更准）
体系 B''（ε_μ 家族统一修正，α_v 不动）：
  I_e = 3e − σ³(1+16/15+√(2/3)) − ε_μ·(幂基/(N_gen·静默²))
  I_μ = ln16 + e^{−3} + ε_μ
  E_τ = 16ln15 + (7/10)ln(16/15) − 8ε_μ
  ε_μ = 144e^{−16}(1+6σ³)
系数谱：+1（I_μ）/ −2/75（I_e）/ −8（E_τ）——框架量（单位元/幂基/(N_gen·静默²)/k_max）
"""
import math

sigma = 1/15; s3 = sigma**3
m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86
rel_e, rel_mu, rel_tau = 2.935e-8, 2.177e-8, 6.753e-5
M_Pl_MeV = 1.220890e22
sE = math.sqrt((2.2e-5/2)**2 + rel_tau**2)
rel_cross = math.sqrt(rel_e**2+rel_mu**2)

def grade(s):
    return "✓ 达标" if s <= 1 else ("～ 提示" if s <= 3 else "✗ 不达标")

I_e_exp = math.log(m_tau_c/m_e_c)
I_mu_exp = math.log(m_tau_c/m_mu_c)
I_em_exp = math.log(m_mu_c/m_e_c)
E_exp = math.log(M_Pl_MeV/m_tau_c)

eps_mu = 144*math.e**(-16)*(1+6*s3)

# 体系 A 主导项
I_e0 = 3*math.e - s3*(1+16/15+math.sqrt(2/3))
I_mu0 = math.log(16) + math.e**(-3)
E0 = 16*math.log(15) + (7/10)*math.log(16/15)

# 竞争归因对比
alpha_contrib = s3*math.sqrt(2/3)*6*s3
print(f"α_v 修正贡献（候选 X）：6σ⁶√(2/3) = {alpha_contrib:.6e}——残余 {(alpha_contrib-4.319777e-7)/4.319777e-7*100:+.4f}%")
print(f"ε_e 修正贡献（候选 Y）：ε_μ×2/75 = {eps_mu*2/75:.6e}——残余 {(eps_mu*2/75-4.319777e-7)/4.319777e-7*100:+.4f}%")
print(f"判别：Y 更准（0.21% vs 0.46%）——但 Y 纯后验、X 有 α_v 通道 A 先验")
print()

# 体系 B''（ε_μ 家族，α_v 不动）
I_eB2 = I_e0 - eps_mu*2/75
I_muB2 = I_mu0 + eps_mu
E_B2 = E0 - 8*eps_mu

print("=== 体系 B''（ε_μ 家族统一修正）===")
se = abs(I_eB2-I_e_exp)/rel_e
sm = abs(I_muB2-I_mu_exp)/rel_mu
sEt = abs(E_B2-E_exp)/sE
sc = abs((I_eB2-I_muB2)-I_em_exp)/rel_cross
print(f"  m_e/m_τ：σ_score = {se:.3f} {grade(se)}")
print(f"  m_μ/m_τ：σ_score = {sm:.3f} {grade(sm)}")
print(f"  E_τ：σ_score = {sEt:.3f} {grade(sEt)}")
print(f"  m_e/m_μ（无 m_τ）：σ_score = {sc:.3f} {grade(sc)}")
print(f"  m_τ 绝对：{M_Pl_MeV*math.exp(-E_B2):.2f} vs {m_tau_c}")
print()

print("=== 系数谱 ===")
print(f"  I_μ：+1（单位元）")
print(f"  I_e：−2/75 = −幂基/(N_gen·静默²) = −σ·幂基/静默（多重身份）")
print(f"  E_τ：−8 = −k_max")
print(f"  谱 = {{+1, −2/75, −8}} 全框架量——静默族修正'系数谱'成形")
print()

print("=== 体系对比 ===")
print("B'（α_v 6σ³ 修正）：m_e 0.064/m_μ 0.034/E_τ 0.018/m_e-m_μ 0.032")
print("B''（ε_μ 家族修正）：上述——若全链 ≤0.1σ_score 且系数谱全框架量——")
print("ε_μ 家族统一性优于 α_v 局域修正（但后验拟合参数 2→3？——ε_μ 是主参数、")
print("2/75 与 8 是框架量系数非拟合参数——参数归并后仍是 ε_μ 单参数）")
