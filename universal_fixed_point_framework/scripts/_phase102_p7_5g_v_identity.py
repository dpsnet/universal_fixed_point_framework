# -*- coding: utf-8 -*-
"""
Phase 102 P7-5g：v/M_Pl 框架身份搜索（y_τ 与 E_b 的共同瓶颈）
==============================================================================
目标：v/M_Pl = 246000/1.221e22 = 2.0147e-17，E_v = ln(M_Pl/v) = ?
若 E_v 有框架表达（如 16·dH−桥、dH×n 等），则 y_τ = √2·m_τ/v 全框架化。
对照组：E_τ = ln(M_Pl/m_τ) = 43.374（P7-5c：16·dH + ln(16/15)/3 = 43.37351）
        E_τ − E_v = ln(m_τ/v) = ln(1776.86/246000) = ?
"""
import math, json

M_PL = 1.221e22     # MeV
V_G = 246.0          # GeV
V_MEV = V_G*1000
M_TAU = 1776.86      # MeV
D_H = 2.7095
S_16 = 1/15.0        # σ = S_4

E_v = math.log(M_PL/V_MEV)
E_tau = math.log(M_PL/M_TAU)
y_tau_sm = math.sqrt(2)*M_TAU/V_MEV

print("P7-5g：v/M_Pl 框架身份搜索")
print("="*70)
print("  E_v   = ln(M_Pl/v) = ln(%.3e/%.1f) = %.6f" % (M_PL, V_MEV, E_v))
print("  E_tau = ln(M_Pl/m_τ) = %.6f（P7-5c 框架：16·dH+ln(16/15)/3 = %.5f）" % (E_tau, 16*D_H+math.log(16/15)/3))
print("  E_tau−E_v = ln(m_τ/v) = %.6f（= ln(%.3f/%.0f) = %.4f ✓）" % (E_tau-E_v, M_TAU, V_MEV, math.log(M_TAU/V_MEV)))
print("  y_τ(SM) = √2·m_τ/v = %.6f（实验反推口径）" % y_tau_sm)
print("  用 P7-5c 框架 m_τ：y_τ = √2×(m_τ/M_Pl)/(v/M_Pl) = %.6f（同一值，m_τ 侧已框架化）" % (math.sqrt(2)*math.exp(-E_tau)/math.exp(-E_v)))

# 候选搜索：E_v 与框架量组合
print("\n  E_v = %.5f 的框架候选：" % E_v)
cands = []
for expr, val in [
    ("16·dH − 4.91", 16*D_H - 4.91),
    ("d_H×14.2", D_H*14.2),
    ("16×2.4", 16*2.4),
    ("e×14.15", math.e*14.15),
    ("κ×20.14", (6/math.pi)*20.14),
    ("3·ln16−3.84", 3*math.log(16)-3.84),
    ("ln16+ln15+ln7", math.log(16)+math.log(15)+math.log(7)),
]:
    cands.append((expr, val, (val/E_v-1)*100))
cands.sort(key=lambda x: abs(x[2]))
for expr, val, dev in cands[:4]:
    print("    %-22s = %.5f（偏差 %+.2f%%）" % (expr, val, dev))

# 关键对照：m_τ/v 比值（自然单位可直接比的量）
print("\n  比值链（不依赖 M_Pl 绝对标度）：")
print("    m_τ/v = %.5e（实验）" % (M_TAU/V_MEV))
print("    e^{−ln(16/15)}/3 = %.5e（P7-5c 桥项 16/15 的代静默 /3？对照）" % (math.exp(-math.log(16/15))/3))
print("    m_τ/v vs E_τ−E_v 关系：ln(m_τ/v) = %.5f（16·dH+桥 的 v 侧差需框架化）" % math.log(M_TAU/V_MEV))

result = {"E_v": E_v, "E_tau": E_tau, "E_tau_minus_E_v": E_tau-E_v,
          "y_tau_sm": y_tau_sm, "v_over_Mpl": V_MEV/M_PL,
          "v_framework_status": "open（38.47 无干净框架身份）"}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5g_v_identity.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
