# -*- coding: utf-8 -*-
"""
Phase 102 P7-5i：★ v 框架化候选验证——v/m_τ = 3⁴·∛5（全框架量）
==============================================================================
候选（P7-5h 搜索最优）：ln(v/m_τ) = (k_max/2)·ln(N_gen) + ln(k_max−N_gen)/N_gen
                    = 4·ln3 + ln5/3（4=k_max/2、3=N_gen、5=k_max−N_gen、1/3=1/N_gen）
等效：v/m_τ = 3⁴·∛5 = 138.508
检验：① v/m_τ ② v 绝对（框架 m_τ + 实验 m_τ 两口径）③ y_τ = √2/(v/m_τ) ④ E_v 继承
判定：双 0.1% 标准达标 → v 闭合候选 → y_τ 框架化（P7-5a 开放项消除）
"""
import math, json

M_PL = 1.221e22
M_TAU = 1776.86       # MeV 实验
M_TAU_FW = math.exp(-(16*2.7095 + math.log(16/15)/3))*M_PL  # P7-5c 框架 m_τ
V_EXP = 246000.0      # MeV
D_H = 2.7095
N_GEN = 3.0
K_MAX = 8.0

E_tau_fw = 16*D_H + math.log(16/15)/3
E_tau_exp = math.log(M_PL/M_TAU)
E_v_exp = math.log(M_PL/V_EXP)
L_vt_exp = E_tau_exp - E_v_exp

# 候选
L_vt_fw = (K_MAX/2)*math.log(N_GEN) + math.log(K_MAX-N_GEN)/N_GEN
V_OVER_TAU = N_GEN**(K_MAX/2) * (K_MAX-N_GEN)**(1/N_GEN)

def dev(f, e): return (f/e-1)*100

print("P7-5i：★ v 框架化候选验证")
print("="*74)
print("  候选结构：ln(v/m_τ) = (k_max/2)·ln(N_gen) + ln(k_max−N_gen)/N_gen")
print("             = 4·ln3 + ln5/3 = %.6f" % L_vt_fw)
print("  等效：    v/m_τ = 3⁴·∛5 = %.6f" % V_OVER_TAU)
print("  框架身份：4=k_max/2（补登）、3=N_gen（机器证明）、5=k_max−N_gen（补登）、1/3=1/N_gen")

print("\n[A] v/m_τ 比值检验：")
print("  预测 = 3⁴·∛5 = %.4f（实验 %.4f，偏差 %+.4f%%）" % (V_OVER_TAU, math.exp(L_vt_exp), dev(V_OVER_TAU, math.exp(L_vt_exp))))

print("\n[B] v 绝对检验：")
v1 = M_TAU*V_OVER_TAU
v2 = M_TAU_FW*V_OVER_TAU
print("  口径1（实验 m_τ）：v = %.1f MeV = %.2f GeV（实验 246.00，偏差 %+.4f%%）" % (v1, v1/1000, dev(v1, V_EXP)))
print("  口径2（框架 m_τ = %.2f MeV，+0.043%%）：v = %.1f MeV = %.2f GeV（偏差 %+.4f%%）" % (M_TAU_FW, v2, v2/1000, dev(v2, V_EXP)))

print("\n[C] E_v 继承检验：")
E_v_fw = E_tau_fw - L_vt_fw
print("  E_v(框架) = E_τ(fw) − ln(v/m_τ) = %.6f − %.6f = %.6f" % (E_tau_fw, L_vt_fw, E_v_fw))
print("  E_v(实验) = %.6f，偏差 %+.5f%%（指数放大 → v 偏差见 [B]）" % (E_v_exp, dev(E_v_fw, E_v_exp)))

print("\n[D] y_τ 框架化（P7-5a 开放项闭合检验）：")
y_fw = math.sqrt(2)/V_OVER_TAU
y_exp = math.sqrt(2)*M_TAU/V_EXP
print("  y_τ(框架) = √2/(3⁴·∛5) = %.7f（实验 %.7f，偏差 %+.4f%%）" % (y_fw, y_exp, dev(y_fw, y_exp)))
print("  → y_τ 全框架表达（不含任何实验输入）——P7-5a y_τ 平凡循环被 v 框架化解除")

print("\n[E] 判定：")
ok = [dev(V_OVER_TAU, math.exp(L_vt_exp)), dev(v1, V_EXP), dev(y_fw, y_exp)]
print("  v/m_τ %+.4f%%、v %+.4f%%、y_τ %+.4f%%——全部 %s 0.1%% 标准 → 达标候选命中" % (ok[0], ok[1], ok[2], "✓在" if all(abs(x)<0.1 for x in ok) else "✗部分超"))
print("  诚实边界：① 4=k_max/2、5=k_max−N_gen 身份补登（P7-4c 对偶网络新成员）")
print("             ② 搜索后最优（14 命中中唯一全框架量组合）——标注")
print("             ③ 无独立交叉验证（同 P7-5c 标准：候选级达标）")
print("             ④ v 是 y_τ 与电弱端瓶颈——本候选直接闭合 y_τ 端")

result = {"L_vt_fw": L_vt_fw, "L_vt_exp": L_vt_exp, "v_over_tau": V_OVER_TAU, "v_over_tau_dev": dev(V_OVER_TAU, math.exp(L_vt_exp)),
          "v_fw_MeV": v1, "v_dev": dev(v1, V_EXP), "y_tau_fw": y_fw, "y_tau_exp": y_exp, "y_tau_dev": dev(y_fw, y_exp),
          "E_v_fw": E_v_fw, "E_v_exp": E_v_exp, "structure": "v/m_tau = N_gen^(k_max/2) × (k_max-N_gen)^(1/N_gen) = 3^4·∛5"}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5i_v_framework.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
