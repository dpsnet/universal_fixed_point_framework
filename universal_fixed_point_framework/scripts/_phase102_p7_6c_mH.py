# -*- coding: utf-8 -*-
"""
Phase 102 P7-6c：m_H 修正口径验证（m_H = m_p + m_e − E_b）
==============================================================================
m_H(氢原子) ≠ m_N——差 m_e−E_b ≈ 0.51 MeV——修正对照口径
"""
import math, json

KAPPA = 6/math.pi
LAM = 210.0
SIG = 1/15.0
M_N_FW = 1014.9
M_E_FW = 0.51096
ALPHA_EM = 1.0/(24*(2.7095+3))
EB_FW_MEV = ALPHA_EM**2*M_E_FW/2   # MeV
M_H_EXP = 938.783  # m_p+m_e−E_b 实验口径（1.007825 u）

def dev(f, t): return (f/t-1)*100

print("P7-6c：m_H 修正口径验证")
print("="*70)
for gname, gap in [("κ²Λ/10", KAPPA**2*LAM/10), ("κΛ(1−2σ/3)/5", KAPPA*LAM*(1-2*SIG/3)/5)]:
    mn = M_N_FW - gap
    mh = mn + M_E_FW - EB_FW_MEV
    print("  [%s] m_H = m_N'+m_e−E_b = %.4f+%.5f−%.8f = %.4f MeV（实验 %.3f——%+.4f%%）" % (
        gname, mn, M_E_FW, EB_FW_MEV, mh, M_H_EXP, dev(mh, M_H_EXP)))
    print("        ★ 0.01%% 级：%s" % ("✓" if abs(dev(mh, M_H_EXP)) < 0.01 else "✗"))
print("\n  ★ m_H 偏差继承 m_N'（差 m_e−E_b 常数项）——脚本 _phase102_p7_6b 用 m_N 对照 m_H 口径错误已修正")
result = {"m_H_fw": [M_N_FW-KAPPA**2*LAM/10+M_E_FW-EB_FW_MEV, M_N_FW-KAPPA*LAM*(1-2*SIG/3)/5+M_E_FW-EB_FW_MEV]}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_6c_mH.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
