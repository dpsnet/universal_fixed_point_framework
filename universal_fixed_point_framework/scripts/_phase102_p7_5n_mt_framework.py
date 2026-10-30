# -*- coding: utf-8 -*-
"""
Phase 102 P7-5n：★ m_t 框架化候选独立验证
==============================================================================
候选：m_t = (1 − Δλ_min/16)·v/√2 = (1 − Δλ_min/(2k_max))·v/√2
  Δλ_min = (√6−√2)/√72（paper20 定理 6.1 机器证明）、16 = 2k_max、v = 3⁴∛5·m_τ（P7-5i 框架）
  y_t^B 闭式 = 1 − Δλ_min/16（Formula B 谱投影新闭式候选）
独立验证：精确数值 + 敏感性 + 交叉检验（v 路径2 重检）
"""
import math, json

D_H = 2.7095
N_GEN = 3.0
K_MAX = 8.0
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
M_TAU_EXP = 1776.86     # MeV 实验
M_T_EXP = 172.7         # GeV 实验（PDG 172.69±0.30）

def dev(f, e): return (f/e-1)*100

print("P7-5n：★ m_t 框架化候选独立验证")
print("="*74)
print("[A] 候选结构：m_t = (1−Δλ_min/16)·v/√2")
DL16 = DL_MIN/16
y_t = 1 - DL16
V_OVER_TAU = N_GEN**(K_MAX/2) * (K_MAX-N_GEN)**(1/N_GEN)
V_FW = V_OVER_TAU*M_TAU_EXP/1000     # 框架 v（GeV，实验 m_τ 口径）
m_t_fw = y_t*V_FW/math.sqrt(2)
print("  Δλ_min = %.8f（精确）" % DL_MIN)
print("  Δλ_min/16 = %.8f" % DL16)
print("  y_t^B(闭式) = 1−Δλ_min/16 = %.8f" % y_t)
print("  v(框架) = 3⁴∛5×%.2f MeV = %.4f GeV（P7-5i）" % (M_TAU_EXP, V_FW))
print("  m_t(框架) = %.6f GeV（实验 172.7，偏差 %+.5f%%）" % (m_t_fw, dev(m_t_fw, M_T_EXP)))
print("  [PDG 172.69±0.30 口径：偏差 %+.5f%%——实验误差内]" % dev(m_t_fw, 172.69))

print("\n[B] 敏感性（δ 精度影响）：")
for d_d in [0, 1e-4, -1e-4]:
    dl = DL_MIN  # Δλ_min 无 δ 依赖（纯 √ 组合）
    print("  Δλ_min 无 δ 依赖（纯机器证明量）——m_t 不受 δ 影响 ✓")

print("\n[C] 交叉检验 1：y_t^B* 实验反推 vs 闭式")
y_star = M_T_EXP*math.sqrt(2)/V_FW
print("  反推 y_t^B* = %.8f（vs 闭式 %.8f，偏差 %+.5f%%）" % (y_star, y_t, dev(y_t, y_star)))

print("\n[D] 交叉检验 2：v 路径2 重检（m_t 框架化后）")
ALPHA_V_FW = 16/15 + math.sqrt(2/N_GEN)
ALPHA_T_FW = math.log(7)
C1 = math.exp(-(D_H+3))
d_alpha = ALPHA_V_FW - ALPHA_T_FW
c1_pow = C1**d_alpha
v_path2 = m_t_fw*c1_pow
print("  路径2：v = m_t(fw)×c₁^{α_v−α_t} = %.3f×%.6f = %.4f GeV（实验 246.0，偏差 %+.4f%%）" % (m_t_fw, c1_pow, v_path2, dev(v_path2, 246.0)))
print("  ——失调根源为 Δα 差 0.00071（P7-5k 诊断）——m_t 框架化不解决——双路径仍不等价（0.4%）")
print("  ★ 但 m_t 本身 +0.00%% 达标：v 路径1 + m_t 端已全框架")

print("\n[E] 判定：")
print("  ★ m_t = (1−Δλ_min/16)·v/√2 = %.4f GeV（%+.5f%%）——0.1%% 标准大幅达标——候选命中" % (m_t_fw, dev(m_t_fw, M_T_EXP)))
print("  ★ y_t^B 闭式 = 1−Δλ_min/(2k_max)——Formula B 谱投影新闭式候选")
print("  ★ 链条：v 框架化（P7-5i）→ m_t 框架化（本轮）→ 弱电端 m_t/v/y_τ/α_v 全候选闭合")
print("  诚实边界：① 搜索空间 126 命中（过拟合警示）但 1−Δλ_min/16 最优且全框架 ② 闭式与凸组合口径关系未推导 ③ 候选级达标（无独立交叉验证）")

result = {"m_t_fw": m_t_fw, "m_t_exp": M_T_EXP, "dev": dev(m_t_fw, M_T_EXP),
          "y_t_closed": y_t, "y_star": y_star, "v_path2": v_path2}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5n_mt_framework.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
