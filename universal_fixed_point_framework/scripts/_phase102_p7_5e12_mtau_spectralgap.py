# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-12：m_τ 谱隙链候选——κΛ·Δλ_min 基底扩展检验
==============================================================
P7-5e-11 未决项（m_e 跨族双重身份）的推论检验：
若 m_e = κΛ·Δλ_min/18（谱隙链）与 m_e/m_τ = e^{−3e}（指数链）同时成立
→ m_τ = κΛ·Δλ_min·e^{3e}/18 —— 检验 m_τ 是否有独立的谱隙链闭式。
直接扫描：m_τ/(κΛ·Δλ_min) 的代数身份（k_max/N_gen 计数系）。
"""
import json
import math

dH   = math.log(15)
kap  = 6/math.pi
Lam  = 210.3
kLam = kap*Lam
dlam_reg   = 0.0229
dlam_exact = math.pi/(24*dH+72)
e = math.e

m_tau = 1776.86      # 实验
m_mu  = 105.658375
m_e   = 0.51099895
m_ud  = 3.45

print("="*104)
print("P7-5e-12：m_τ 谱隙链候选——κΛ·Δλ_min 基底扩展检验")
print("="*104)

for dname, dlam in [("登记值口径", dlam_reg), ("框架精确值口径", dlam_exact)]:
    base = kLam*dlam
    print("── %s（基底 κΛ·Δλ_min = %.6f MeV）──" % (dname, base))
    r_tau = m_tau/base
    r_mu  = m_mu/base
    r_e   = m_e/base
    r_ud  = m_ud/base
    print("  m_τ/(κΛΔλ) = %.4f" % r_tau)
    print("  m_μ/(κΛΔλ) = %.4f" % r_mu)
    print("  m_e/(κΛΔλ) = %.4f" % r_e)
    print("  m_ud/(κΛΔλ)= %.4f" % r_ud)
    print()

# 代数闭式候选（m_τ 基底比）
CAND = {}
for i in range(180, 201):
    CAND[str(i)] = float(i)
CAND["k_max²·N_gen (192)"] = 192.0
CAND["k_max²·N_gen+1 (193)"] = 193.0
CAND["k_max²·N_gen−1 (191)"] = 191.0
CAND["2·N_gen⁴ (162)"] = 162.0
CAND["3·2⁶ (192)"] = 192.0
CAND["e^{3e}/18"] = math.exp(3*e)/18
CAND["16·dH·κ"] = 16*dH*kap
CAND["k_max³+N_gen (515)"] = 512+3
CAND["2^7·N_gen (384)"] = 384.0
CAND["k_max²·(N_gen+1) (256)"] = 256.0
CAND["(k_max²+1)·N_gen (195)"] = 195.0
CAND["(k_max²−1)·N_gen (189)"] = 189.0
CAND["(k_max²+N_gen)·N_gen (201)"] = 201.0
CAND["k_max²·N_gen+1"] = 193.0

r_tau = m_tau/(kLam*dlam_exact)
best = None
for cname, cval in CAND.items():
    dev = abs(r_tau - cval)/r_tau*100
    if best is None or dev < best[1]:
        best = (cname, dev)
print("★ m_τ/(κΛΔλ) 最佳闭式（框架精确值口径）：%s（%.3f%%）" % (best[0], best[1]))
m_tau_calc = (kLam*dlam_exact)*193.0
print("  → m_τ ≈ κΛ·Δλ_min^(EM)·(k_max²·N_gen+1) = %.3f vs 实验 %.3f（%+.3f%%）" % (m_tau_calc, m_tau, (m_tau_calc/m_tau-1)*100))
m_tau_calc_reg = (kLam*dlam_reg)*193.0
print("  登记值口径：%.3f（%+.3f%%）" % (m_tau_calc_reg, (m_tau_calc_reg/m_tau-1)*100))
print()
print("谱隙链族（κΛ·Δλ_min 基底）现成员：")
print("  m_e  = κΛΔλ/18（÷2·N_gen² = 2^(1)·3² 逆）")
print("  m_ud = κΛΔλ·3/8（×N_gen/k_max = 2^(−3)·3）")
print("  m_τ  = κΛΔλ·193（×k_max²·N_gen+1 = 2⁶·3+1）★ 新候选")
print("  m_μ  = 无命中（11.47 无代数身份——第二代缺席谱隙链）")
print()
print("交叉验证：")
print("  m_τ 现双路径——旋量塔链（2^{−64}(16/15)^{47/3}e^{−16δ}，+0.043%%）vs 谱隙链（×193，+0.045%%）")
print("  → 若成立：m_τ 绝对质量获两条独立框架路径（结构完全不同）")
print()
print("判定：")
print("  m_τ 谱隙链候选命中（×193 = k_max²·N_gen+1，两口径均 <0.1%%）——候选登记")
print("  193 = 192+1 = k_max²·N_gen+1：'旋量平方×代数+1'——+1 单位元修正（弱身份，诚实标注）")
print("  谱隙链族 = {m_e, m_ud, m_τ}（代数因子 2^(1)3²、2^(−3)3、2⁶3+1——2 幂指数 −3/1/6 无规律——不强行统一）")
print("  第二代 m_μ 缺席谱隙链（走指数链）——与 P7-5e-11 '接口层仅第一代成形' 互补")
print()
print("exit 0")
