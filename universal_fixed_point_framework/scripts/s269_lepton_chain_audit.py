# -*- coding: utf-8 -*-
"""S269: 轻子端全链当前状态审计（2026-10-28）

闭合"m_e/m_μ 不达标"开放项——一次性数值复核三轻子 + m_e/m_μ 当前 σ_score。
全部公式来自 S112-S117（E_τ^D）+ S129（σ_rel 勘误）+ S145/S145b（E_e 组装闭合）
+ S156/S173（I_μ 最终 + 2σ⁵ 升格裁决）。

框架量：
  σ = 1/15；σ³/σ⁵/σ⁸；e；ln15；ln(16/15)
  ε_μ = 144·e^{−16}·(1+6σ³)
  α_v' = 16/15 + √(2/3)·(1+6σ³)
  I_e = 3e − σ³(1+α_v')
  I_μ = e + 42·e^{−6} + 2σ⁵
  E_τ^D = 16ln15 + (7/10)ln(16/15) − 8ε_μ − (σ⁵−e^{−16}) − 2σ⁸(1+σ)
  E_e = E_τ^D + I_e − (27/80)·e^{−19}
  E_μ = E_τ^D + I_μ
  m_i = e^{−E_i}·M_Pl（M_Pl = 1 自然单位——用户裁决 2026-10-23）
  m_e/m_μ = e^{E_μ−E_e}

参考值（PDG/CODATA 2022 合成——σ_rel 用 S129 勘误口径）：
  m_e = 0.51099895000(15) MeV——σ_rel(e) = 2.94e-10
  m_μ = 105.6583755(23) MeV——σ_rel(μ) = 2.2e-8
  m_τ = 1776.86(12) MeV——σ_rel(τ) = 6.75e-5
  m_e/m_μ = 4.83633166(12)e-3——合成 σ_rel = √(σ_rel(e)²+σ_rel(μ)²)

σ_score = |预测−实验|/合成不确定度（用户纪律：≤1σ 达标/1-3σ 提示/>3σ 不达标）
"""
import math

sigma = 1/15
sig3, sig5, sig8 = sigma**3, sigma**5, sigma**8
e = math.e
ln15 = math.log(15)
ln16o15 = math.log(16/15)

eps_mu = 144 * e**(-16) * (1 + 6*sig3)
alpha_vp = 16/15 + math.sqrt(2/3) * (1 + 6*sig3)
I_e = 3*e - sig3 * (1 + alpha_vp)
I_mu = e + 42*e**(-6) + 2*sig5
E_tau_D = 16*ln15 + (7/10)*ln16o15 - 8*eps_mu - (sig5 - e**(-16)) - 2*sig8*(1+sigma)
E_e = E_tau_D + I_e - (27/80)*e**(-19)
E_mu = E_tau_D + I_mu

# 预测值
m_e_pred = math.exp(-E_e)
m_mu_pred = math.exp(-E_mu)
m_tau_pred = math.exp(-E_tau_D)
ratio_pred = math.exp(E_mu - E_e)

# 实验参考（MeV——与框架自然单位对齐需质量锚；比值无锚自由）
m_e_ref, s_rel_e = 0.51099895000, 2.94e-10
m_mu_ref, s_rel_mu = 105.6583755, 2.2e-8
m_tau_ref, s_rel_tau = 1776.86, 6.75e-5
ratio_ref = 4.83633166e-3

# σ_score（对数口径：Δln = 相对偏差——S111 勘误）
def score(pred, ref, s_rel):
    return abs(math.log(pred/ref)) / s_rel

sc_e = score(m_e_pred, m_e_ref, s_rel_e)
sc_mu = score(m_mu_pred, m_mu_ref, s_rel_mu)
sc_tau = score(m_tau_pred, m_tau_ref, s_rel_tau)
s_rel_ratio = math.sqrt(s_rel_e**2 + s_rel_mu**2)
sc_ratio = score(ratio_pred, ratio_ref, s_rel_ratio)

def grade(s):
    return "达标 ✓" if s <= 1 else ("提示" if s <= 3 else "不达标 ✗")

print("=== S269: 轻子端全链当前状态审计 ===\n")
print(f"框架输入: σ³={sig3:.10g}  σ⁵={sig5:.10g}  σ⁸={sig8:.10g}")
print(f"  ε_μ = 144e⁻¹⁶(1+6σ³) = {eps_mu:.6e}")
print(f"  α_v' = 16/15+√(2/3)(1+6σ³) = {alpha_vp:.10f}")
print(f"  I_e  = 3e−σ³(1+α_v') = {I_e:.10f}")
print(f"  I_μ  = e+42e⁻⁶+2σ⁵ = {I_mu:.10f}")
print(f"  E_τ^D = {E_tau_D:.12f}")
print(f"  E_e  = {E_e:.12f}")
print(f"  E_μ  = {E_mu:.12f}\n")

print(f"{'量':<10}{'预测':<22}{'参考':<16}{'σ_score':<10}{'判定':<8}")
print("-" * 66)
print(f"{'m_e':<10}{m_e_pred:<22.6g}{m_e_ref:<16.6g}{sc_e:<10.4g}{grade(sc_e)}")
print(f"{'m_μ':<10}{m_mu_pred:<22.6g}{m_mu_ref:<16.6g}{sc_mu:<10.4g}{grade(sc_mu)}")
print(f"{'m_τ':<10}{m_tau_pred:<22.6g}{m_tau_ref:<16.6g}{sc_tau:<10.4g}{grade(sc_tau)}")
print(f"{'m_e/m_μ':<10}{ratio_pred:<22.10g}{ratio_ref:<16.10g}{sc_ratio:<10.4g}{grade(sc_ratio)}")

print("\n结论：")
if max(sc_e, sc_mu, sc_tau, sc_ratio) <= 1:
    print("  ★ 三轻子 + m_e/m_μ 全部 ≤1σ 达标——'m_e/m_μ 不达标'开放项闭合确认")
else:
    print("  ★ 存在超 1σ 项——见上表——需攻坚")
print("  （诚实边界：绝对质量需质量锚——此处验证的是比值/间隔结构与 σ_score 判定；")
print("    m_e/m_μ 比值无锚自由——纯框架量）")
