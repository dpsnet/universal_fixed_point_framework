# -*- coding: utf-8 -*-
"""
Phase 102 P7-5u：e^{−3e} 精确化攻坚——m_e/m_τ 目标指数 8.153992 系统搜索
==============================================================================
P7-4b：m_e/m_τ = e^{−3e} = 2.873397e−4（vs 实验 2.875854e−4——−0.0854%——超 0.01% 级）
P7-5t：域间张力根因 = e^{−3e} 复合误差——精确化可统一 m_e 链与 m_τ 锚
目标：x_target = −ln(2.875854e−4) = 8.153992（0.01% 级 = ±0.0008）
"""
import math, json

R_TARGET = 0.5109989/1776.86   # m_e/m_τ 实验
X_TARGET = -math.log(R_TARGET) # 8.153992
E = math.e
DH = 2.7095
LN15 = math.log(15)
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
SIG = 1/15.0
LN16_15 = math.log(16/15)
KAPPA = 6/math.pi

def dev(f, t): return (f/t-1)*100

print("P7-5u：e^{−3e} 精确化——x_target = %.6f 系统搜索" % X_TARGET)
print("="*78)
print("基准：3e = %.6f（偏差 %+.4f%%——P7-4b 当前候选）" % (3*E, dev(3*E, X_TARGET)))

print("\n[A] 单框架量线性/修正：")
cands = []
# 8 + 小量
for name, v in [("8(=k_max)", 8), ("8+σ×2.31", 8+SIG*2.31), ("8+Δλ_min×1.262", 8+DL_MIN*1.262),
                ("8+ln(16/15)×2.386", 8+LN16_15*2.386), ("3e−σ/78", 3*E-SIG/78.0),
                ("3e−1/1170", 3*E-1/1170.0), ("d_H×3.0094", DH*3.0094), ("3e×(1−σ²/190)", 3*E*(1-SIG**2/190))]:
    cands.append((name, v))
# 底族
for base, bn in [(2, "2"), (15, "15"), (16, "16"), (SIG, "σ"), (1/16.0, "1/16"), (math.e**(-DH), "e^-dH"),
                 (math.e**(-(DH+3)), "e^-(dH+3)"), (16/15.0, "16/15")]:
    a = X_TARGET/math.log(base)
    cands.append(("%s^%.4f" % (bn, a), base**a))
for name, v in cands:
    print("  %-24s = %.6f（偏差 %+.4f%%）" % (name, v, dev(v, X_TARGET)))

print("\n[B] 两参数搜索（a·3e ± b·框架量，a∈0.9..1.1，b 小量）：")
best = []
for a10 in range(95, 106):
    a = a10/100.0
    for bname, b in [("ln(16/15)", LN16_15), ("σ", SIG), ("σ²", SIG**2), ("σ³", SIG**3),
                     ("Δλ_min", DL_MIN), ("Δλ_min²", DL_MIN**2), ("δ=1/675", 1/675.0),
                     ("ln(15/14)", math.log(15/14)), ("σ×Δλ_min", SIG*DL_MIN), ("σ³×5", SIG**3*5)]:
        for s in [1, -1]:
            v = a*3*E + s*b
            d = abs(dev(v, X_TARGET))
            if d < 0.02:
                best.append((d, "%.3f·3e %+d·%s = %.6f" % (a, s, bname, v), v))
best.sort()
for d, s, v in best[:12]:
    print("  %+.4f%%: %s" % (d, s))

print("\n[C] 结构候选：")
# c 序列底族（paper11 谱公式）：r = (c_i/c_j)^α——α 框架候选
c1, c2, c3 = math.exp(-(DH+3)), math.exp(-DH), 1.0
pairs = [("c1/c2", c1/c2), ("c1/c3", c1/c3), ("c2/c3", c2/c3), ("c2/c1", c2/c1), ("c3/c2", c3/c2)]
for pn, pr in pairs:
    a = X_TARGET/math.log(pr)
    print("  (%s)^α：α = %.5f（偏差 vs 框架 α 候选：d_H/2=1.3548 %+.2f%%、e/2=1.3591 %+.2f%%、1.358 %+.2f%%）"
          % (pn, a, dev(a, DH/2), dev(a, E/2), dev(a, 1.358)))

print("\n[D] e^{−3e} 修正项直接解：")
eps = X_TARGET - 3*E
print("  x_target − 3e = %+.6f（需要修正项）" % eps)
for name, v in [("σ/78", SIG/78.0), ("1/1170", 1/1170.0), ("σ³×2.88", SIG**3*2.88), ("δ×0.589", 1/675.0*0.589),
                ("Δλ_min/142.8", DL_MIN/142.8), ("σ²/5.2", SIG**2/5.2), ("ln(16/15)×0.0132", LN16_15*0.0132)]:
    print("  %-18s = %+.7f（vs 需要 %+.7f——偏差 %+.2f%%）" % (name, v, eps, dev(v, eps)))

result = {"x_target": X_TARGET, "three_e_dev": dev(3*E, X_TARGET), "best_hits": [s for d, s, v in best[:6]]}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102_p7_5u_e3e.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
