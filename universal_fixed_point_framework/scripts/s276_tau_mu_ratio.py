# -*- coding: utf-8 -*-
"""S276: m_τ/m_μ = e^{I_μ} 第一性派生检验（2026-10-28）

框架链：m_i = e^{−E_i}·M_Pl——m_τ/m_μ = e^{E_μ−E_τ^D} = e^{I_μ}
（E_τ^D 公共项相消——与 S269 比值同构）——I_μ = e+42e⁻⁶+2σ⁵（S173 闭合）。
这是第一性派生（无新拟合）——检验 m_τ/m_μ 是否命中——第三链级。
"""
import math

sigma = 1/15
e = math.e

I_mu = e + 42*e**(-6) + 2*sigma**5
ratio_pred = math.exp(I_mu)

# PDG 实验：m_τ = 1776.86(12) MeV、m_μ = 105.6583755(23) MeV
m_tau = 1776.86
s_tau = 0.12
m_mu = 105.6583755
s_mu = 0.00023
ratio_exp = m_tau / m_mu
s_rel = math.sqrt((s_tau/m_tau)**2 + (s_mu/m_mu)**2)

print("=== S276: m_τ/m_μ = e^{I_μ} 第一性派生检验 ===\n")
print(f"I_μ = e + 42e⁻⁶ + 2σ⁵ = {I_mu:.10f}")
print(f"预测 m_τ/m_μ = e^{{I_μ}} = {ratio_pred:.10f}")
print(f"实验 m_τ/m_μ = {m_tau}/{m_mu} = {ratio_exp:.10f}（σ_rel = {s_rel:.2e}）")

dln = abs(math.log(ratio_pred / ratio_exp))
sc = dln / s_rel
print(f"\nΔln = {dln:.3e}")
print(f"σ_score = {sc:.3f}")
g = "达标 ✓" if sc <= 1 else ("提示" if sc <= 3 else "不达标 ✗")
print(f"判定：{g}")

print(f"\n① 结构：m_τ/m_μ = e^{{e + 42e⁻⁶ + 2σ⁵}}——")
print(f"   · e = 模流单位（每步 e——S166）——主荷")
print(f"   · 42e⁻⁶ = 约束域×e^{{−活跃×幂基}}（S156——S152 唯一三量纯乘积）")
print(f"   · 2σ⁵ = 幂基×静默幂（S173 闭合——静默冻结修正）")
print(f"   ——全部组件框架量——无新拟合——第一性派生")

print(f"\n② 与 S269 的呼应：m_e/m_μ = e^{{I_μ−I_e+27/80·e⁻¹⁹−5/2·e⁻¹⁸}}——")
print(f"   m_τ/m_μ = e^{{I_μ}}——同一荷间隔结构（I_μ）的两个读数——")
print(f"   轻子质量比全部由荷间隔 I_i 派生——E_τ^D 锚只定绝对标度")

print(f"\n③ 诚实边界：")
print(f"   · σ_score {sc:.2f} 判定如上——m_τ 不确定度 ±0.12 MeV 主导")
print(f"   · I_μ 是 S156/S173 已闭合的候选（后验——非预测）——")
print(f"     但 m_τ/m_μ 检验是 e^{{I_μ}} 的**派生验证**——不是新拟合")
print(f"   · 第三链定义：δ_V3 级联模式预测全新量——本检验是链内派生——")
print(f"     强度介于派生检验与先验预言之间——候选级")
