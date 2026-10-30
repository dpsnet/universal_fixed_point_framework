# -*- coding: utf-8 -*-
"""先验性检验 (a)：ε_μ 普适性——E_τ 链闭合（2026-10-26）

静默族修正假说的独立证据检验：
若 E_τ^new 的 1.9σ_score 偏差 = −8ε_μ（8 = 2³ 翻倍族）→ 同一 ε_μ 修正两条独立链
（m_e/m_μ 456σ_score 与 m_τ/E_τ 1.9σ_score）→ 假说获强独立证据。
联合反解判别：两链分别反解 ε_μ，一致性判别候选身份。
"""
import math

sigma = 1/15
s3 = sigma**3
m_e_c, m_mu_c, m_tau_c = 0.51099895069, 105.6583755, 1776.86
G_N_rel = 2.2e-5; M_Pl_rel = G_N_rel/2; M_Pl_MeV = 1.220890e22
rel_tau = 0.12/m_tau_c
sE = math.sqrt(M_Pl_rel**2+rel_tau**2)
rel_cross = math.sqrt((2.935e-8)**2+(2.177e-8)**2)

I_mu_pred = math.log(16) + math.e**(-3)
I_mu_exp = math.log(m_tau_c/m_mu_c)
I_e_pred = 3*math.e - s3*(1+16/15+math.sqrt(2/3)*(1+6*s3))
I_e_exp = math.log(m_tau_c/m_e_c)
E_pred = 16*math.log(15) + (7/10)*math.log(16/15)
E_exp = math.log(M_Pl_MeV/m_tau_c)

print("=== ① ε_μ 联合反解判别 ===")
eps_mu1 = I_mu_exp - I_mu_pred          # m_e/m_μ 链反解（α_v 修正后 I_e 侧闭合，ε_μ 在 I_μ）
eps_mu2 = (E_pred - E_exp)/8            # E_τ 链反解（若系数 = 8）
print(f"链1（m_μ）反解 ε_μ = {eps_mu1:.5e}")
print(f"链2（E_τ,÷8）反解 ε_μ = {eps_mu2:.5e}")
print(f"两反解差 = {(eps_mu2-eps_mu1)/eps_mu1*100:+.2f}%")
eps_cand = 144*math.e**(-16)
print(f"144e^{{−16}} 候选 = {eps_cand:.5e}——链1 差 {(eps_cand-eps_mu1)/eps_mu1*100:+.2f}%、链2 差 {(eps_cand-eps_mu2)/eps_mu2*100:+.2f}%")
print()

print("=== ② E_τ − 8ε_μ 闭合验证 ===")
for name, eps in [("144e^{−16}", eps_cand), ("链2精确", eps_mu2)]:
    E_new = E_pred - 8*eps
    sig = abs(E_new-E_exp)/sE
    m_tau_pred = M_Pl_MeV*math.exp(-E_new)
    print(f"E_τ−8×{name} = {E_new:.10f} → σ_score = {sig:.3f}（原 1.916）——m_τ' = {m_tau_pred:.2f}")
print()

print("=== ③ 系数 8 的精确值（若 ε_μ = 144e^{−16} 普适）===")
k_exact = (E_pred - E_exp)/eps_cand
print(f"k = (E_τ^new−E_exp)/ε_μ = {k_exact:.4f}（8 = 2³ 差 {(k_exact-8)/8*100:+.2f}%）")
print()

print("=== ④ 全链联合 σ 数（ε_μ = 144e^{−16}、α_v 修正、E_τ−kε_μ）===")
I_mu_new = I_mu_pred + eps_cand
I_em = I_e_pred - I_mu_new
I_em_exp = math.log(m_mu_c/m_e_c)
print(f"m_e/m_μ：σ_score = {abs(I_em-I_em_exp)/rel_cross:.2f}")
print(f"m_e/m_τ（I_e'）：σ_score = {abs(I_e_pred-I_e_exp)/(I_e_exp*2.935e-8):.3f}")
print(f"m_μ/m_τ（I_μ'）：σ_score = {abs(I_mu_new-I_mu_exp)/(I_mu_exp*2.177e-8):.3f}")
print(f"E_τ−kε_μ（k={k_exact:.4f}）：σ_score = {abs(E_pred-k_exact*eps_cand-E_exp)/sE:.3f}")
print()
print("=== ⑤ 语义判别：ε_μ 系数的框架身份 ===")
print(f"ε_μ×8 = 2³×(N_gen×不动点)²·e^{{−16}}——'翻倍³×代数静默²×全态静默'")
print(f"vs I_μ 里的 e^{{−3}}——若 ε_μ 普适：'轻子间隔修正 = 12²e^{{−16}}'")
print(f"k ≈ 8.08：8 = 2³——E_τ 链 ε_μ 系数 = 翻倍³（候选，差 1%）")
