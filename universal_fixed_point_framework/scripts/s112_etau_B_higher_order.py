# -*- coding: utf-8 -*-
# S112 E_τ^B 剩余偏差更高阶修正扫描（2026-10-27）
# 目标：E_τ^B 绝对偏差 1.2e-6 → < 2.9e-7（m_e 级——S111 核心开放项）
# E_τ^B = 16ln15 + (7/10)ln(16/15) − 8·ε_μ（B'''——ε_μ = 144e^{−16}(1+6σ³)）
# 扫描剩余偏差的框架候选（σ 系/e 系/组合——先证伪）

from math import log, e

M_Pl = 1.220890e22
m_tau = 1776.86
sigma = 1/15

ln15 = log(15)
ln16_15 = log(16/15)
E_tau_fw = 16*ln15 + (7/10)*ln16_15
E_tau_obs = -log(m_tau/M_Pl)

eps_mu = 144*e**(-16)*(1+6*sigma**3)
E_tau_B = E_tau_fw - 8*eps_mu
resid = E_tau_B - E_tau_obs
print(f"ε_μ = 144e^{{−16}}(1+6σ³) = {eps_mu:.10e}")
print(f"E_τ^B = E_τ − 8ε_μ = {E_tau_B:.10f}")
print(f"E_τ(obs) = {E_tau_obs:.10f}")
print(f"剩余偏差 = {resid:+.10e}（B''' 后——目标 < 2.9e-7）")
print(f"方向：E_τ^B 偏高 +{resid:.2e}——需再减 {resid:.2e}")

print("\n=== 框架候选扫描（先证伪——找 <3% 差） ===")
cands = {}
# σ 系
for n in range(4, 10):
    cands[f"σ^{n}"] = sigma**n
# e^{-16} 系
for k in [8, 9, 10, 11, 12, 14, 16]:
    cands[f"{k}·e^{{-16}}"] = k*e**(-16)
# ε_μ 系
cands["ε_μ/10"] = eps_mu/10
cands["ε_μ/14"] = eps_mu/14
cands["ε_μ/16"] = eps_mu/16
cands["ε_e·3（ε_e = −5σ⁶）"] = 3*5*sigma**6
cands["ε_e·2.8"] = 2.8*5*sigma**6
# 组合
cands["σ⁵ − e^{−16}"] = sigma**5 - e**(-16)
cands["σ⁵ + e^{−16}"] = sigma**5 + e**(-16)
cands["σ⁴/16"] = sigma**4/16
cands["σ⁴/15"] = sigma**4/15
cands["σ⁵(1+σ)"] = sigma**5*(1+sigma)
cands["σ⁵(1−σ)"] = sigma**5*(1-sigma)
cands["σ⁵(1+2σ)"] = sigma**5*(1+2*sigma)

# 符号：resid 为正——候选需为正（减项）
print(f"\n剩余偏差（需匹配）：+{resid:.3e}")
results = []
for name, v in cands.items():
    if v <= 0: continue
    ratio = v/resid
    d = abs(v - resid)
    rel = d/resid*100
    results.append((rel, name, v, ratio))
results.sort()
for rel, name, v, ratio in results[:15]:
    print(f"{name} = {v:.3e}——比值 {ratio:.4f}——差 {rel:.2f}%")

print("\n=== 判别 ===")
print("目标：E_τ 绝对偏差 < 2.9e-7——当前 B''' 后 1.2e-6——需更高阶项 ~1.2e-6")
