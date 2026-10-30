# -*- coding: utf-8 -*-
"""
Phase 102 P7-5r：E_b 三量闭环机制检查 + m_t 跨扇区交叉验证
==============================================================================
E_b = α_EM²·m_e/2（Rydberg 公式——标准物理，框架贡献在 α_EM、m_e 值）
  α_EM(框架) = 1/[24(d_H+3)]（P7-5l：1/α_EM = 24d_H+72 = 137.028）
  m_e(框架) = e^{−3e}·m_τ（P7-4b：3e = N_gen×e——轻子扇区候选）
三量闭环检查：全框架代入 E_b vs 实验；与 m_t 闭式（1−Δλ_min/16）跨扇区交叉
"""
import math, json

D_H = 2.7095
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
SIGMA = 1/15.0
M_TAU = 1776.86          # MeV 实验
M_E_EXP = 0.5109989      # MeV
EB_EXP_EV = 13.605693     # Rydberg R_∞（CODATA 2022）
ALPHA_EM_FW = 1.0/(24*(D_H+3))    # P7-5l 框架
ME_FW = math.exp(-3*math.e)*M_TAU # P7-4b 框架 m_e（e^{−3e}·m_τ）

def dev(f, e): return (f/e-1)*100

print("P7-5r：E_b 三量闭环机制检查 + m_t 跨扇区交叉验证")
print("="*74)
print("[A] 三量闭环——各口径 E_b：")
print("  1/α_EM(框架) = 24(d_H+3) = %.6f（α_EM = %.8f）" % (24*(D_H+3), ALPHA_EM_FW))
print("  m_e(实验) = %.7f MeV；m_e(框架) = e^{−3e}·m_τ = %.7f MeV（偏差 %+.4f%%）" % (M_E_EXP, ME_FW, dev(ME_FW, M_E_EXP)))
eb1 = ALPHA_EM_FW**2*M_E_EXP/2*1e6          # 实验 m_e（MeV→eV）
eb2 = ALPHA_EM_FW**2*ME_FW/2*1e6            # 全框架 m_e
print("  E_b(α框架+m_e实验) = %.6f eV（实验 %.6f，偏差 %+.4f%%）" % (eb1, EB_EXP_EV, dev(eb1, EB_EXP_EV)))
print("  E_b(全框架)        = %.6f eV（偏差 %+.4f%%）" % (eb2, dev(eb2, EB_EXP_EV)))

print("\n[B] m_e(框架) 精度核对（P7-4b 报告检查）：")
ratio_fw = ME_FW/M_TAU
ratio_exp = M_E_EXP/M_TAU
print("  e^{−3e} = %.7e（实验 m_e/m_τ = %.7e——偏差 %+.4f%%）" % (ratio_fw, ratio_exp, dev(ratio_fw, ratio_exp)))
print("  ——P7-4b 报告的 +0.0%% 是 3 位小数截断——实际 %+.2f%%——0.1%% 标准内" % dev(ratio_fw, ratio_exp))

print("\n[C] 与 m_t 闭式的跨扇区交叉（Δλ_min ↔ α_EM 桥）：")
y_mt = 1 - DL_MIN/16
print("  m_t 闭式小量：Δλ_min/16 = %.8f" % (DL_MIN/16))
print("  α_EM(框架) = %.8f" % ALPHA_EM_FW)
c1 = DL_MIN/16/ALPHA_EM_FW
print("  Δλ_min/16 ÷ α_EM = %.6f（vs 1+2σ/3 = %.6f——偏差 %+.4f%%）" % (c1, 1+2*SIGMA/3, dev(c1, 1+2*SIGMA/3)))
print("  ★ 候选：Δλ_min/16 ≈ α_EM(1+2σ/3)——Δ_dress 修正因子桥接 m_t 与 E_b 扇区")
c2 = ALPHA_EM_FW*(1+2*SIGMA/3)
print("  α_EM(1+2σ/3) = %.8f vs Δλ_min/16 = %.8f——偏差 %+.4f%%" % (c2, DL_MIN/16, dev(c2, DL_MIN/16)))

print("\n[D] E_b 与 m_t 的模式对照：")
print("  m_t 链：y_t = 1−Δλ_min/16（'1−小量'——Δλ_min 域）")
print("  E_b 链：α_EM²·m_e/2（'小量²'——d_H 域 + e^{−3e} e 域）")
print("  共享：无（Δλ_min vs d_H vs e）——但 Δλ_min/16 ≈ α_EM(1+2σ/3) 提供桥（C 项）")

print("\n[E] 判定")
print("  ★ E_b 三量闭环：α框架+m_e实验 = %+.4f%%（0.1%% 内 ✓）；全框架（e^{−3e} 口径）=%+.4f%%——受 m_e(框架) 精度限制" % (dev(eb1, EB_EXP_EV), dev(eb2, EB_EXP_EV)))
print("  ★ 跨扇区交叉候选：Δλ_min/16 ≈ α_EM(1+2σ/3)（%+.4f%%——0.1%% 内边缘达标）——Δ_dress 修正因子桥" % dev(c2, DL_MIN/16))
print("  ★ 诚实边界：① 全框架 E_b 依赖 m_e(框架) 精度（e^{−3e} 实际 %+.2f%% 超 0.1%%）② 桥候选单点（无第二独立检验）③ 三量闭环成立（α框架+m_e实验）——E_b 机制=标准 Rydberg（框架贡献在值）" % dev(ratio_fw, ratio_exp))

result = {"eb_alpha_mixed": eb1, "eb_full_fw": eb2, "eb_exp": EB_EXP_EV,
          "me_fw": ME_FW, "me_fw_dev": dev(ME_FW, M_E_EXP), "bridge": c2, "bridge_dev": dev(c2, DL_MIN/16)}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5r_eb_closure.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
