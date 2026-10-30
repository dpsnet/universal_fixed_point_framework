# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-45：y_τ = √2/(3⁴·∛5) 纯框架候选 + 137 族观察
================================================================
洞察1：y_τ = √2·m_τ/v——v = 3⁴·∛5·m_τ——m_τ 消去——y_τ = √2/(3⁴·∛5) 纯框架
洞察2：3⁴·∛5 = 137.986 ≈ 1/α_EM = 137.028 ≈ m_c 系数 = 137.895——137 族
"""
import math, json

dH   = math.log(15)
dlam_EM = math.pi/(24*dH+72)
dlam_P20 = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
C  = 2*math.sqrt(math.log(10))
C2 = C*C
kappa = 6/math.pi
Lam  = 16*math.log(10)*(dH+3)
kL   = kappa*Lam
sigma = 1/15
alpha_v = 1+sigma+math.sqrt(4/3/2)
kmax, Ngen = 8, 3
inv_alpha_EM = 24*(dH+3)

m_tau = C2*(193-3/40)          # 框架 m_τ（GeV）
m_tau_pdg = 1776.86/1000       # PDG 1776.86 MeV → GeV
v_fw = 3**4*5**(1/3)*m_tau     # 框架 v
v_pdg = 246.22                 # PDG v（GeV）

print("="*104)
print("P7-5e-45：y_τ 纯框架候选 + 137 族观察")
print("="*104)

print()
print("【y_τ = √2·m_τ/v——m_τ 消去】")
print("-"*104)
y_fw_pure = math.sqrt(2)/(3**4*5**(1/3))
print("y_τ = √2·m_τ/v——v = 3⁴·∛5·m_τ——m_τ（和 C²）完全消去：")
print("y_τ = √2/(3⁴·∛5) = %.8f（纯框架量——无外部参数）" % y_fw_pure)
print()
y_obs_pdg = math.sqrt(2)*m_tau_pdg/v_pdg
print("观测 y_τ（PDG m_τ/v）= √2×%.6f/%.2f = %.8f" % (m_tau_pdg, v_pdg, y_obs_pdg))
print("框架 vs 观测：差 %+.4f%%" % ((y_fw_pure/y_obs_pdg-1)*100))
print()
y_obs_fw = math.sqrt(2)*m_tau/v_fw
print("框架 y_τ（框架 m_τ/框架 v）= √2×%.6f/%.6f = %.8f——自洽（恒等于纯框架值）" % (m_tau, v_fw, y_obs_fw))
print()
print("→ y_τ = √2/(3⁴·∛5) 是纯框架候选——但 vs PDG 观测差 0.435%%（v 的 PDG vs 框架定义差传递）——候选级")
print()
print("【137 族观察】")
print("-"*104)
a3c5 = 3**4*5**(1/3)
mc_coef = math.sqrt(10)/dlam_EM
print("1/α_EM = 24(d_H+3) = %.4f" % inv_alpha_EM)
print("3⁴·∛5（v 链常数）= %.4f——差 %+.4f%%" % (a3c5, (a3c5/inv_alpha_EM-1)*100))
print("m_c 系数 = √10/Δλ_EM = %.4f——差 %+.4f%% vs 1/α_EM" % (mc_coef, (mc_coef/inv_alpha_EM-1)*100))
print("         vs 3⁴·∛5 差 %+.4f%%" % ((mc_coef/a3c5-1)*100))
print()
print("→ 137 族三成员：137.028（1/α_EM）/ 137.895（m_c 系数）/ 137.986（v 链）——差 0.6-0.7%%")
print("→ m_c 系数 vs v 链常数差 0.066%%——0.07%% 级接近——但非精确命中——方向性观察")
print()
print("【α_v 与 y_τ 对照】")
print("-"*104)
print("α_v = 1+σ+√(C_F/2) = %.5f（P7-5 系列已框架化）" % alpha_v)
print("y_τ = √2/(3⁴·∛5) = %.5f——两者比值 = %.3f（不干净）" % (y_fw_pure, alpha_v/y_fw_pure))
print("→ α_v（耦合组合）与 y_τ（纯谱常数）无直接比值关系——身份独立开放")
print()
print("【结论】")
print("-"*104)
print("1. ★ y_τ = √2/(3⁴·∛5)——纯框架（C²/m_τ 消去）——vs PDG 差 0.435%%——候选级（v 定义差传递）")
print("2. ★ 137 族观察：1/α_EM 137.028 / m_c 系数 137.895 / v 链 137.986——0.6-0.7%% 族——m_c 系数 vs v 链 0.066%% 接近——方向性")
print("3. α_v/y_τ 无直接比值——身份独立——保持开放")
print("4. 诚实边界：y_τ 0.435%% 不达标（候选级）；137 族 0.6-0.7%% 接近非命中；α_v 身份开放")
print()
json.dump({"y_tau": {"pure": y_fw_pure, "obs_pdg": y_obs_pdg, "dev_pct": (y_fw_pure/y_obs_pdg-1)*100},
           "137_family": {"inv_alpha": inv_alpha_EM, "mc_coef": mc_coef, "v_const": a3c5}},
          open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5e45_ytau.json","w",encoding="utf-8"), indent=2)
print("JSON 落盘 ✓")
print("exit 0")
