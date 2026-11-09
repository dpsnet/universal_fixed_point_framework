# -*- coding: utf-8 -*-
"""
sin^2 theta_W 构造的正式族检验（v1.3 评审 §三 要求的记账手续）
语法（评审给定，照做）：
  C = 框架常数集 {2,3,4,5,7,8,15,16,24,42}
  尺度 M = {x*y} ∪ {x*(y+z)}，x,y,z ∈ C   → 257 个尺度
  分数 f = {p/q}，p,q ∈ C                 → 73 个分数
  候选质量 = M + f（按组合计数 257*73 = 18761；去重后 14694 个不同数值）
目标窗口（3σ，单位 GeV）：
  m_W = 80.3692 ± 0.040   （1σ = 0.0133）
  m_Z = 91.1880 ± 0.0063  （1σ = 0.0021）
派生：m_W/m_Z 3σ 窗、sin^2 theta_W = 1-(m_W/m_Z)^2 的 1σ 窗
输出：语法空间大小、各窗口命中数（组合计数与去重计数两种口径）、框架组合位置与基础命中率。
"""
from fractions import Fraction
import math
import bisect

C = frozenset([2, 3, 4, 5, 7, 8, 15, 16, 24, 42])
Cl = sorted(C)

scales = set()
for x in Cl:
    for y in Cl:
        scales.add(x * y)
for x in Cl:
    for y in Cl:
        for z in Cl:
            scales.add(x * (y + z))
scales = sorted(scales)

fracs = sorted({Fraction(p, q) for p in Cl for q in Cl})

combos = [(m, f, Fraction(m) + f) for m in scales for f in fracs]
vals = sorted({c[2] for c in combos})

print("|C|=%d  |scales|=%d  |fracs|=%d  |combos|=%d  |distinct values|=%d" % (
    len(C), len(scales), len(fracs), len(combos), len(vals)))

W1 = 0.0133
Z1 = 0.0021
MW, MZ = 80.3692, 91.1880
W_LO, W_HI = MW - 3 * W1, MW + 3 * W1
Z_LO, Z_HI = MZ - 3 * Z1, MZ + 3 * Z1

hitW = [(m, f, v) for (m, f, v) in combos if W_LO <= v <= W_HI]
hitZ = [(m, f, v) for (m, f, v) in combos if Z_LO <= v <= Z_HI]
print("m_W window [%.4f, %.4f]: combo hits=%d, distinct=%d" % (W_LO, W_HI, len(hitW), len({h[2] for h in hitW})))
for m, f, v in hitW[:12]:
    print("    %s + %s = %.5f" % (m, f, float(v)))
print("m_Z window [%.4f, %.4f]: combo hits=%d, distinct=%d" % (Z_LO, Z_HI, len(hitZ), len({h[2] for h in hitZ})))
for m, f, v in hitZ[:12]:
    print("    %s + %s = %.5f" % (m, f, float(v)))

sig_ratio = math.sqrt((W1 / MZ) ** 2 + (MW * Z1 / MZ ** 2) ** 2)
R_EXP = MW / MZ
R_LO, R_HI = R_EXP - 3 * sig_ratio, R_EXP + 3 * sig_ratio
print("\nratio exp=%.9f  sigma=%.3e  3sigma window=[%.9f, %.9f]" % (R_EXP, sig_ratio, R_LO, R_HI))

# 比值联合命中（去重值层；用于基础率）
vsort = [float(v) for v in vals]
pair_hits = []
for vw in vals:
    fw = float(vw)
    i = bisect.bisect_left(vsort, fw / R_HI)
    j = bisect.bisect_right(vsort, fw / R_LO)
    for k in range(i, j):
        pair_hits.append((vw, vals[k]))
print("ratio 3sigma pair hits (distinct-value layer) = %d ; base rate 1/%.1f" % (
    len(pair_hits), (len(vals) ** 2) / max(len(pair_hits), 1)))

S2_1 = 0.00026
S2_LO, S2_HI = 0.22321 - S2_1, 0.22321 + S2_1
s2hits = [(a, b) for a, b in pair_hits if S2_LO <= 1 - (float(a) / float(b)) ** 2 <= S2_HI]
print("sin2theta 1sigma hits (within ratio window) = %d ; base rate 1/%.1f" % (
    len(s2hits), (len(vals) ** 2) / max(len(s2hits), 1)))

FW_MW, FW_MZ = Fraction(643, 8), Fraction(1459, 16)
print("\nframework mW=643/8=%.6f in window: %s" % (float(FW_MW), W_LO <= float(FW_MW) <= W_HI))
print("framework mZ=1459/16=%.6f in window: %s" % (float(FW_MZ), Z_LO <= float(FW_MZ) <= Z_HI))
print("framework ratio=1286/1459=%.9f  sigma_score=%.4f" % (
    float(FW_MW / FW_MZ), (float(FW_MW / FW_MZ) - R_EXP) / sig_ratio))
print("framework sin2=%.9f  sigma_score=%.4f" % (
    float(1 - (FW_MW / FW_MZ) ** 2), (float(1 - (FW_MW / FW_MZ) ** 2) - 0.22321) / S2_1))
print("\nbase rate (combo layer): m_W 1/%.1f ; m_Z 1/%.1f" % (
    len(combos) / max(len(hitW), 1), len(combos) / max(len(hitZ), 1)))
