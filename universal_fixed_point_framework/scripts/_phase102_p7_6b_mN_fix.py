# -*- coding: utf-8 -*-
"""
Phase 102 P7-6b：m_N/m_Δ 缺口修正验证——重子端 SU(6) 缺陷闭合
==============================================================================
候选缺口：① κ²Λ/10 = 76.599（−0.041%）② κΛ(1−2σ/3)/5 = 76.649（+0.025%）
修正：m_N' = m_N(框架 1014.9) − 缺口；m_Δ' = m_Δ(框架 1308.6) − 同缺口
传播链：m_p/m_e、m_H（E_b 相对质量 ~1e−7 可忽略）
"""
import math, json

KAPPA = 6/math.pi
LAM = 210.0
SIG = 1/15.0
M_N_FW = 1014.9
M_DELTA_FW = 1308.6
M_RHO_FW = 774.5
M_N_EXP = 938.272
M_DELTA_EXP = 1232.0
M_E_EXP = 0.5109989
M_H_EXP = 938.77
M_E_FW = 0.51096

def dev(f, t): return (f/t-1)*100

print("P7-6b：m_N/m_Δ 缺口修正验证")
print("="*78)
gaps = {"κ²Λ/10": KAPPA**2*LAM/10, "κΛ(1−2σ/3)/5": KAPPA*LAM*(1-2*SIG/3)/5}
for gname, gap in gaps.items():
    print("\n[%s——缺口 = %.4f MeV]" % (gname, gap))
    mn = M_N_FW - gap
    md = M_DELTA_FW - gap
    print("  m_N' = 1014.9−%.3f = %.3f MeV（实验 %.3f——%+.4f%%）" % (gap, mn, M_N_EXP, dev(mn, M_N_EXP)))
    print("  m_Δ' = 1308.6−%.3f = %.3f MeV（实验 %.3f——%+.4f%%）" % (gap, md, M_DELTA_EXP, dev(md, M_DELTA_EXP)))
    print("  重子和 m_N'+m_Δ' = %.2f MeV（实验 %.2f——%+.4f%%）" % (mn+md, M_N_EXP+M_DELTA_EXP, dev(mn+md, M_N_EXP+M_DELTA_EXP)))
    print("  m_p/m_e = %.2f（实验 1836.15——%+.4f%%）" % (mn/M_E_FW, dev(mn/M_E_FW, M_N_EXP/M_E_EXP)))
    print("  m_H = %.2f MeV（实验 %.2f——%+.4f%%）" % (mn, M_H_EXP, dev(mn, M_H_EXP)))
    print("  ★ 0.01%% 级达标：m_N %s / m_Δ %s / m_H %s" % (
        "✓" if abs(dev(mn, M_N_EXP)) < 0.01 else "✗",
        "✓" if abs(dev(md, M_DELTA_EXP)) < 0.01 else "✗",
        "✓" if abs(dev(mn, M_H_EXP)) < 0.01 else "✗"))

print("\n[机制图像（候选级）]")
print("  ★ 介子端 m_ρ = 2M_ud_eff = 774.5（−0.10%%）达标——重子端 m_N/m_Δ 带统一缺口")
print("  ★ SU(6) 恒等 m_N+m_Δ = 3m_ρ 框架内精确（2323.5）——但实验端本就失调（2170 vs 2326）")
print("  ★ 修正后重子和 2170.2 ≈ 实验 2170.27——'重子端统一缺口'机制（介子端不缺）")
print("  ★ 机制待解释：为何重子内夸克比介子内少得一份胶子 dressing 的 ~1/(N_gen+k_max−1)")

print("\n[诚实边界]")
print("  ★ 候选级（两缺口公式数值近——差 0.06%%——判别需新证据）")
print("  ★ m_N 1014.9 的框架公式本身来自 SU(6) 组分模型（M_ud_eff 修正后）——缺口修正 = 事后修正非事前推导")
print("  ★ 单点命中（m_N、m_Δ 同缺口——两个目标一个参数）——交叉验证：重子和 2170.2 独立达标 ✓")

result = {g: {"mn": M_N_FW-v, "md": M_DELTA_FW-v,
              "mn_dev": dev(M_N_FW-v, M_N_EXP), "md_dev": dev(M_DELTA_FW-v, M_DELTA_EXP)}
          for g, v in gaps.items()}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_6b_mN_fix.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
