# -*- coding: utf-8 -*-
"""
Phase 102 P7-5q：闭式隐含 r_23 反推——结构差异判定
==============================================================================
P7-5p 发现：闭式 ⇔ |U_t2|² = 0.001578 vs 定理 5.5 的 sin²θ23 = 0.003299（×2.09）
本脚本：从闭式反推定理 5.5 隐含的 r_23 → m_c/m_t——判断差异是微调级还是结构级
结构：定理 5.5 反解——tan²θ = t²/(1+t²) = |U_t2|²；r_23 = (t²+r_λ)/(1+r_λ·t²)
"""
import math, json

D_H = 2.7095
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
ALPHA_V = 16/15 + math.sqrt(2/3.0)
BETA_U = 1.0531
C1, C2, C3 = math.exp(-(D_H+3)), math.exp(-D_H), 1.0
lam = [c**ALPHA_V for c in (C1, C2, C3)]
s = sum(lam)
L = [x/s for x in lam]
RLAM = L[1]/L[2]

def dev(f, e): return (f/e-1)*100

print("P7-5q：闭式隐含 r_23 反推（结构差异判定）")
print("="*74)
# 闭式 → |U_t2|²（P7-5p 精确）
need = (DL_MIN/16 - (1-L[2]))/(L[2]-L[1])
print("[A] 闭式等价条件：|U_t2|² = %.8f" % need)
# 定理 5.5 反解（|U_t2|² = sin²θ = t²/(1+t²)）
t2 = need/(1-need)
r23_implied = (t2 + RLAM)/(1 + RLAM*t2)
mc_mt_implied = r23_implied**BETA_U
mc_implied = mc_mt_implied*172.7
MC_MT_EXP = 1.27/172.7
print("[B] 反解定理 5.5：")
print("    tan²θ23 = %.8f" % t2)
print("    r_23(闭式隐含) = %.8f" % r23_implied)
print("    → m_c/m_t = r_23^{β_u} = %.6f（实验 1.27/172.7 = %.6f——偏差 %+.2f%%）" % (mc_mt_implied, MC_MT_EXP, dev(mc_mt_implied, MC_MT_EXP)))
print("    → m_c(隐含) = %.3f GeV（实验 1.27 GeV——偏差 %+.2f%%）" % (mc_implied, dev(mc_implied, 1.27)))

print("\n[C] 对照：定理 5.5 表口径 r_23 = (m_c/m_t)^{1/β} = %.6f（实验输入）" % (MC_MT_EXP**(1/BETA_U)))
print("    闭式隐含 r_23 = %.6f——差异 ×%.3f" % (r23_implied, r23_implied/(MC_MT_EXP**(1/BETA_U))))

print("\n[D] 判定")
print("  ★ 闭式隐含 m_c/m_t = 0.005921 vs 实验 0.007330（−19.2%%）——**结构级差异**（非 0.17%% 微调）")
print("  ★ |U_t2|² 微调搜索无意义：差异根源在 r_23 层（m_c/m_t 的 19%% 失调）")
print("  ★ 闭式更可能是独立近似公式（谱间隙单参数近似）而非凸组合推导——机制地位维持开放")
print("    可选方向：m_c 框架化（若 m_c 有框架值 1.023 GeV 则链闭合——但 PDG 1.27 不符，需先证伪实验口径）")

result = {"need_Ut2": need, "r23_implied": r23_implied, "mc_mt_implied": mc_mt_implied,
          "mc_implied": mc_implied, "mc_mt_exp": MC_MT_EXP, "delta": dev(mc_mt_implied, MC_MT_EXP)}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5q_implied_r23.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
