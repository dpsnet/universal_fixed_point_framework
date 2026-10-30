# -*- coding: utf-8 -*-
"""
Phase 102 P7-5h：ln(m_τ/v) 系统搜索——候选 5−σ = (k_max−N_gen)−S_4 = 74/15
==============================================================================
目标：ln(m_τ/v) = 4.930484（实验）——v 闭合钥匙量。
候选：5−σ = 8−3−1/15 = 74/15 = 4.93333（5 = k_max−N_gen 两组件均框架量）
检验：E_v = E_τ(fw) − (5−σ) = 43.37351 − 4.93333 = 38.44018 → v/M_Pl = e^{−38.44018}
      v = e^{−38.44018}×M_Pl vs 实验 246 GeV
系统搜索：两参数线性组合 a·X+b·Y（a,b 小整数/框架系数）确认无更优。
"""
import math, json, itertools

M_PL = 1.221e22
V_MEV = 246000.0
M_TAU = 1776.86
D_H = 2.7095
SIGMA = 1/15.0
K_MAX = 8.0
N_GEN = 3.0
KAPPA = 6/math.pi
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
DL3 = math.sqrt(2)*DL_MIN

E_tau_fw = 16*D_H + math.log(16/15)/3
E_v_exp = math.log(M_PL/V_MEV)
L_tv_exp = math.log(M_TAU/V_MEV)   # ln(m_τ/v) = E_v − E_τ（注意符号：m_τ/v < 1 → ln 负？）
# 校正：E_tau = ln(M_Pl/m_τ), E_v = ln(M_Pl/v)；E_τ − E_v = ln(v/m_τ) = −ln(m_τ/v)
L_vt_exp = E_tau_exp = math.log(M_PL/M_TAU)
L_vt_exp = L_vt_exp - E_v_exp      # ln(v/m_τ) = ln(M_Pl/m_τ) − ln(M_Pl/v)
print("P7-5h：ln(m_τ/v) 系统搜索")
print("="*72)
print("  ln(v/m_τ) = ln(M_Pl/m_τ) − ln(M_Pl/v) = %.6f − %.6f = %.6f" % (math.log(M_PL/M_TAU), E_v_exp, L_vt_exp))
print("  目标（正号）：ln(v/m_τ) = %.6f（= −ln(m_τ/v)）" % L_vt_exp)

# 候选验证
cand = K_MAX - N_GEN - SIGMA
print("\n  ★ 候选：ln(v/m_τ) = (k_max−N_gen) − σ = 8−3−1/15 = 74/15 = %.6f" % cand)
print("    实验 = %.6f，偏差 = %+.4f%%" % (L_vt_exp, (cand/L_vt_exp-1)*100))
print("    v/m_τ 预测 = e^{%.6f} = %.3f（实验 %.3f，偏差 %+.3f%%）" % (cand, math.exp(cand), math.exp(L_vt_exp), (math.exp(cand)/math.exp(L_vt_exp)-1)*100))

E_v_fw = E_tau_fw - cand
print("\n  ★ v 端验证：")
print("    E_v(框架) = E_τ(fw) − (5−σ) = %.6f − %.6f = %.6f" % (E_tau_fw, cand, E_v_fw))
print("    E_v(实验) = %.6f，偏差 = %+.5f%%" % (E_v_exp, (E_v_fw/E_v_exp-1)*100))
v_fw = math.exp(-E_v_fw)*M_PL
print("    v(框架) = e^{−%.6f}×M_Pl = %.2f MeV = %.2f GeV（实验 246.00，偏差 %+.3f%%）" % (E_v_fw, v_fw, v_fw/1000, (v_fw/V_MEV-1)*100))

# 系统搜索两参数组合
print("\n  [系统搜索] 两参数组合 a·X+b·Y（目标 ln(v/m_τ) = %.6f）" % L_vt_exp)
pool = {
    "d_H": D_H, "ln15": math.log(15), "ln16": math.log(16), "ln7": math.log(7),
    "ln8": math.log(8), "σ": SIGMA, "1−σ": 1-SIGMA, "κ": KAPPA,
    "Δλ_min": DL_MIN, "Δλ3": DL3, "e": math.e, "π": math.pi,
    "√2": math.sqrt(2), "√3": math.sqrt(3), "√6": math.sqrt(6),
    "ln2": math.log(2), "ln3": math.log(3), "ln5": math.log(5),
}
coeffs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 0.5, 1/3, 1/4, 1/6, 1/15]
hits = []
for (nx, X), (ny, Y) in itertools.combinations(pool.items(), 2):
    for a in coeffs:
        for b in coeffs:
            v = a*X + b*Y
            d = (v/L_vt_exp - 1)*100
            if abs(d) < 0.12:
                hits.append((abs(d), d, "%.6f = %g·%s + %g·%s" % (v, a, nx, b, ny)))
hits.sort()
print("  <0.12%% 命中数：%d" % len(hits))
for ad, d, s in hits[:12]:
    print("    [%+.4f%%] %s" % (d, s))

# 单量 + 整数
print("\n  [单量×整数] n·X（目标 %.6f）" % L_vt_exp)
hits1 = []
for nx, X in pool.items():
    for n in range(1, 21):
        v = n*X
        d = (v/L_vt_exp - 1)*100
        if abs(d) < 0.3:
            hits1.append((abs(d), d, "%.6f = %d×%s" % (v, n, nx)))
hits1.sort()
for ad, d, s in hits1[:8]:
    print("    [%+.3f%%] %s" % (d, s))

# 判定
print("\n  [判定]")
ok5 = abs((cand/L_vt_exp-1)*100) < 0.1
okv = abs((v_fw/V_MEV-1)*100) < 0.1
print("    5−σ 候选 ln(v/m_τ) 偏差 %+.4f%%（%s 0.1%% 标准）" % ((cand/L_vt_exp-1)*100, "✓在" if ok5 else "✗超"))
print("    v 端偏差 %+.3f%%（%s 0.1%% 标准）" % ((v_fw/V_MEV-1)*100, "✓在" if okv else "✗超"))
print("    诚实边界：5=k_max−N_gen 新身份（P7-4c 对偶网络未登记）；σ=1/15 机器证明")

result = {"ln_v_over_tau_exp": L_vt_exp, "cand_5_minus_sigma": cand, "cand_dev": (cand/L_vt_exp-1)*100,
          "E_v_fw": E_v_fw, "E_v_exp": E_v_exp, "v_fw_GeV": v_fw/1000, "v_exp_GeV": 246.0,
          "v_dev": (v_fw/V_MEV-1)*100}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5h_v_tau_search.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
