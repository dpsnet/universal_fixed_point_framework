# -*- coding: utf-8 -*-
"""S277: m_τ/m_e = e^{E_e−E_τ^D} 第一性派生检验（2026-10-28）

框架链：m_τ/m_e = e^{E_e−E_τ^D} = e^{I_e_next − 27/80·e⁻¹⁹}——
I_e_next = I_e + 5/2·e⁻¹⁸（S269b 修正）——I_e = 3e−σ³(1+α_v')——
这是 m_e 侧两个修正（S145 27/80·e⁻¹⁹ + S269b 5/2·e⁻¹⁸）的派生验证。
"""
import math

sigma = 1/15
e = math.e

alpha_vp = 16/15 + math.sqrt(2/3) * (1 + 6*sigma**3)
I_e = 3*e - sigma**3 * (1 + alpha_vp)
I_e_next = I_e + (5/2)*e**(-18)
exp_e = I_e_next - (27/80)*e**(-19)
ratio_pred = math.exp(exp_e)

# PDG 实验：m_τ = 1776.86(12)、m_e = 0.51099895000(15)
m_tau = 1776.86
s_tau = 0.12
m_e = 0.51099895
s_e = 0.00000015
ratio_exp = m_tau / m_e
s_rel = math.sqrt((s_tau/m_tau)**2 + (s_e/m_e)**2)

print("=== S277: m_τ/m_e = e^{E_e−E_τ^D} 派生检验 ===\n")
print(f"I_e = 3e−σ³(1+α_v') = {I_e:.10f}")
print(f"I_e_next = I_e + 5/2·e⁻¹⁸ = {I_e_next:.10f}")
print(f"E_e−E_τ^D = I_e_next − 27/80·e⁻¹⁹ = {exp_e:.10f}")
print(f"预测 m_τ/m_e = {ratio_pred:.10f}")
print(f"实验 m_τ/m_e = {m_tau}/{m_e} = {ratio_exp:.10f}（σ_rel = {s_rel:.2e}）")

dln = abs(math.log(ratio_pred / ratio_exp))
sc = dln / s_rel
print(f"\nΔln = {dln:.3e}")
print(f"σ_score = {sc:.3f}")
g = "达标 ✓" if sc <= 1 else ("提示" if sc <= 3 else "不达标 ✗")
print(f"判定：{g}")

print(f"\n① 结构分解：")
print(f"   · I_e = 3e−σ³(1+α_v')——3e = 活跃×模流单位——")
print(f"     σ³(1+α_v') = 活跃幂×(1+耦合系数)——韦达闭包 3")
print(f"   · −27/80·e⁻¹⁹：活跃³/(全态×静默)×e^{{−(全态+活跃)}}（S145）")
print(f"   · +5/2·e⁻¹⁸：静默/幂基×e^{{−(全态+幂基)}}（S269b——比值攻坚）")
print(f"   ——E_e 链（R_e 家族 j=2,3 两阶）的派生验证")

print(f"\n② 轻子质量比体系闭合（S276+S277）：")
print(f"   m_τ/m_μ = e^{{I_μ}}（σ_score 0.0004——S276）")
print(f"   m_τ/m_e = e^{{E_e−E_τ^D}}（本次）")
print(f"   m_e/m_μ = e^{{I_μ−E_e+E_τ^D}}（S269b——0.007σ 候选修正后）")
print(f"   ——三比值全由荷间隔 I_i 与 E_e 修正派生——E_τ^D 只定绝对标度")

print(f"\n③ 诚实边界：")
print(f"   · m_e/m_μ 的 5/2·e⁻¹⁸ 是后验候选——此处 m_τ/m_e 是派生验证——")
print(f"     若 m_τ/m_e 也精确命中——候选的跨比值一致性加强")
print(f"   · m_τ 不确定度 ±0.12 MeV 主导 σ_rel——高精度命中仍有意义")
