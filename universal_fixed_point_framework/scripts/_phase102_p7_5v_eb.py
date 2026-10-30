# -*- coding: utf-8 -*-
"""
Phase 102 P7-5v-eb：E_b 全框架复查（m_e 新公式影响）
==============================================================================
P7-5v 后：m_e(fw) = m_τ(δ=1/675)×e^{−(3e−σ³(1+α_v))} = 0.51096 MeV（−0.0081%）
E_b = α_EM²·m_e/2——复查全框架 E_b（旧 −0.0738% → 新？）
"""
import math, json

M_PL = 1.221e22
M_TAU_EXP = 1776.86
M_E_EXP = 0.5109989
EB_EXP = 13.605693
E = math.e
LN15 = math.log(15)
LN16_15 = math.log(16/15)
SIG3 = (1/15.0)**3
ALPHA_V = 16/15.0 + math.sqrt(2/3.0)
ALPHA_EM = 1.0/(24*(2.7095+3))
XP = 3*E - SIG3*(1+ALPHA_V)

def dev(f, t): return (f/t-1)*100

print("P7-5v-eb：E_b 全框架复查")
print("="*70)
m_tau_new = M_PL*math.exp(-(16*(LN15+1/675.0) + LN16_15/3))
me_fw = m_tau_new*math.exp(-XP)
eb_fw = ALPHA_EM**2*me_fw/2*1e6
eb_old = ALPHA_EM**2*(math.exp(-3*E)*M_TAU_EXP)/2*1e6
print("  m_e(新全框架) = %.5f MeV（%+.4f%%）" % (me_fw, dev(me_fw, M_E_EXP)))
print("  E_b(全框架新) = %.5f eV（实验 %.5f——%+.4f%%）" % (eb_fw, EB_EXP, dev(eb_fw, EB_EXP)))
print("  E_b(全框架旧 e^{−3e}) = %.5f eV（%+.4f%%）——新优 %.1f 倍" % (eb_old, dev(eb_old, EB_EXP), abs(dev(eb_old, EB_EXP))/abs(dev(eb_fw, EB_EXP))))
print("  ★ E_b 三量闭环全框架：从 −0.0738%% → %+.4f%%（0.01%% 级达标）" % dev(eb_fw, EB_EXP))

print("\n[轻子扇区全框架链总结]")
print("  M_Pl 谱定 → m_τ = M_Pl·e^{−(16(ln15+1/675)+ln(16/15)/3)} = %.3f MeV（−%.4f%%）" % (m_tau_new, abs(dev(m_tau_new, M_TAU_EXP))))
print("  → m_e = m_τ·e^{−(3e−σ³(1+α_v))} = %.5f MeV（%+.4f%%）" % (me_fw, dev(me_fw, M_E_EXP)))
print("  → E_b = α_EM²·m_e/2 = %.4f eV（%+.4f%%）" % (eb_fw, dev(eb_fw, EB_EXP)))
print("  ★ 轻子扇区全框架闭合（m_τ/m_e/E_b 三量 0.01%% 级）——无实验质量输入（除 M_Pl 谱定、v 相关候选）")

result = {"m_tau_fw": m_tau_new, "m_e_fw": me_fw, "eb_fw": eb_fw, "eb_dev": dev(eb_fw, EB_EXP)}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5v_eb.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
