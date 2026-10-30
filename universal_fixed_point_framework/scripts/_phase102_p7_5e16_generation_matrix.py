# -*- coding: utf-8 -*-
"""
Phase 102 P7-5e-16：谱隙链族"代 × 层"矩阵 + m_s 边缘状态检验
===============================================================
4 成员（m_e/m_ud/m_τ/m_b）显示代结构：第一代 + 第三代，第二代缺席。
① 组织 8 质量的链归属矩阵（谱隙链/指数链/旋量塔/无）
② m_s 边缘检验：PDG 流质量 93.4±8 范围内扫描——81/8（=27·m_ud 因子）何时 <0.1%
"""
import json
import math

dH   = math.log(15)
kap  = 6/math.pi
Lam  = 210.3
kLam = kap*Lam
dlam_exact = math.pi/(24*dH+72)
kmax, Ngen = 8, 3
base = kLam*dlam_exact

print("="*104)
print("P7-5e-16：谱隙链族'代 × 层'矩阵 + m_s 边缘检验")
print("="*104)

# 链归属：谱隙因子（乘数；m_e 为 ÷18 → 乘数 1/18）
SPECTRAL = {"m_e": 1/18, "m_ud": 3/8, "m_tau": 193.0, "m_b": 454.111111}
EXPONENTIAL = {"m_e": "e^{−3e} (比值)", "m_mu": "e^{−(ln16+e^{−3})} (比值)", "m_tau": "2^{−64}(16/15)^{47/3}e^{−16δ} (绝对)"}
masses = {"m_e": (0.51099895, 1), "m_mu": (105.658375, 2), "m_tau": (1776.86, 3),
          "m_ud": (3.45, 1), "m_s": (93.4, 2), "m_b": (4180, 3),
          "m_c": (1270, 2), "m_t": (173100, 3)}

print("① 代 × 层矩阵（轻子 / 上型 / 下型）：")
rows = [("轻子", "m_e(1)", "m_μ(2)", "m_τ(3)"), ("上型", "—", "m_c(2)", "m_t(3)"), ("下型", "m_ud(1)", "m_s(2)", "m_b(3)")]
print("  %-10s %-22s %-22s %-22s" % ("", "第一代", "第二代", "第三代"))
for row in rows:
    print("  %-10s %-22s %-22s %-22s" % (row[0], row[1], row[2], row[3]))
print()
print("  谱隙链成员（代数因子）：m_e(2¹·3²)、m_ud(2^{−3}·3¹)、m_τ(2⁶·3¹+1)、m_b(2¹²·3^{−2}−1)")
print("  → ★ 代结构：第一代（m_e/m_ud）+ 第三代（m_τ/m_b）——第二代缺席（m_μ/m_s/m_c）")
print("  → ★ 第三代双命中（m_τ 轻子 + m_b 下型夸克）——第三代是'完整谱隙代'？")
print()

print("② m_s 边缘状态检验（PDG 流质量 93.4±8 = [85.4, 101.4]）：")
r_s_center = 93.4/base
print("  中心值 m_s = 93.4：m_s/(κΛΔλ) = %.4f vs 81/8 = 10.125（%.3f%%）" % (r_s_center, abs(r_s_center-10.125)/r_s_center*100))
# PDG 范围内扫描：81/8 命中 <0.1% 的 m_s 区间
target = 10.125
m_low, m_high = 85.4, 101.4
hit_low, hit_high = target*base*0.999, target*base*1.001
print("  81/8 命中 <0.1%% 需要的 m_s ∈ [%.2f, %.2f]（PDG 范围 %.1f–%.1f）" % (hit_low, hit_high, m_low, m_high))
overlap = max(0, min(hit_high, m_high) - max(hit_low, m_low))
print("  与 PDG 范围重叠 = %.2f MeV（PDG 宽度 %.1f MeV 的 %.0f%%）" % (overlap, m_high-m_low, overlap/(m_high-m_low)*100))
print("  中心值偏差 0.15%%——超 0.1%% 标准但完全在 PDG ±8 不确定度内")
print()

print("③′ 链归属总览（8 质量，双口径偏差）：")
dlam_reg = 0.0229
for mname, (mval, gen) in masses.items():
    r_ex = mval/(kLam*dlam_exact)
    r_reg = mval/(kLam*dlam_reg)
    if mname in SPECTRAL:
        f = SPECTRAL[mname]
        dev_ex = abs(f-r_ex)/r_ex*100
        dev_reg = abs(f-r_reg)/r_reg*100
        if dev_ex < 0.1 and dev_reg < 0.1:
            tag = "双口径达标 ★"
        elif dev_reg < 0.1:
            tag = "单口径达标（登记）"
        elif dev_ex < 0.1:
            tag = "单口径达标（框架精确）"
        else:
            tag = "双口径均超"
        print("  %-6s（第%d代）: 谱隙链 ×%.6f —— 框架精确 %+.4f%% / 登记 %+.4f%%  %s" % (mname, gen, f, (f/r_ex-1)*100, (f/r_reg-1)*100, tag))
    elif mname in EXPONENTIAL:
        print("  %-6s（第%d代）: 指数链（比值/绝对）" % (mname, gen))
    else:
        print("  %-6s（第%d代）: 无（>0.1%% 未命中）" % (mname, gen))
print()
print("④′ 判定（修正）：")
print("  ★ 双口径达标（稳健成员）：m_τ（0.045%%/0.097%%）、m_b（0.064%%/0.079%%）")
print("  ★ 单口径达标（口径敏感成员）：m_e（登记 ~0.00%% 但框架精确 +0.14%% 超）、m_ud（登记 −0.026%% 但框架精确 +0.12%% 超）")
print("  → '4 成员族'修正为'2 稳健 + 2 口径敏感'——m_e/m_ud 命中依赖 Δλ 口径选择（基底不确定度 0.14%% 内）")
print("  → 谱隙链族真实强度：m_τ/m_b 双口径稳健（第三代对）；m_e/m_ud 为候选（口径依赖）")
print("  m_s 中心值 0.15%% 超标准但 PDG ±8 内可命中 81/8——'不确定度内候选'（不达标）")
print()
print("exit 0")
