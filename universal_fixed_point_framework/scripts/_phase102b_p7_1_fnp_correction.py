# -*- coding: utf-8 -*-
"""
Phase 102b P7-1 续-11：F_np 候选第二修正项搜索
==============================================================================
F_np 候选：(b₀/10)³/Δλ₃ = 4.22497（+0.118%）——组件全框架但超 0.1% 边缘
攻第二修正项：×(1 ± 微组合)——目标闭合到 0.1% 内
微组合池：σ、σ²、Δλ_min、Δλ_min²、δ=1/675、σ³、Δλ_min/16 等小量
"""
import math, json, itertools

SIGMA = 1/15.0
DL_MIN = (math.sqrt(6)-math.sqrt(2))/math.sqrt(72)
DL3 = math.sqrt(2)*DL_MIN
DELTA = 1/675.0
B0 = 9.0
TEN = 10.0
TARGET = 4.220

BASE = (B0/TEN)**3/DL3
def dev(f, e): return (f/e-1)*100

print("Phase 102b P7-1 续-11：F_np 第二修正项搜索")
print("="*74)
print("  基准：(b₀/10)³/Δλ₃ = %.6f（偏差 %+.4f%%）" % (BASE, dev(BASE, TARGET)))

small = {"σ": SIGMA, "σ²": SIGMA**2, "σ³": SIGMA**3, "Δλ_min": DL_MIN, "Δλ_min²": DL_MIN**2,
         "δ=1/675": DELTA, "Δλ_min/16": DL_MIN/16, "σ/2": SIGMA/2, "σ/3": SIGMA/3,
         "σ/4": SIGMA/4, "σ/5": SIGMA/5, "σ/6": SIGMA/6, "σ/8": SIGMA/8, "σ/10": SIGMA/10,
         "σ/12": SIGMA/12, "σ/15": SIGMA/15, "Δλ_min/8": DL_MIN/8, "Δλ_min/6": DL_MIN/6,
         "Δλ_min/4": DL_MIN/4, "δ/2": DELTA/2, "δ/3": DELTA/3, "δ/4": DELTA/4}

print("\n[× (1 ± s) 单修正]")
hits = []
for name, s in small.items():
    for sign in [1, -1]:
        v = BASE*(1+sign*s)
        d = dev(v, TARGET)
        if abs(d) < 0.1:
            hits.append((abs(d), d, "×(1%+s)  s=%s" % ("−" if sign<0 else "+", name)))
hits.sort()
print("  <0.1%% 命中：%d" % len(hits))
for ad, d, s in hits[:10]:
    print("    [%+.4f%%] %s → %.5f" % (d, s, TARGET*(1+d/100)))

print("\n[× (1 ± s1 ± s2) 双修正]")
hits2 = []
for (n1, s1), (n2, s2) in itertools.combinations(small.items(), 2):
    for sg1 in [1, -1]:
        for sg2 in [1, -1]:
            v = BASE*(1+sg1*s1+sg2*s2)
            d = dev(v, TARGET)
            if abs(d) < 0.05:
                hits2.append((abs(d), d, "×(1%+s%s%+s%s)" % ("−" if sg1<0 else "+", n1, "−" if sg2<0 else "+", n2)))
hits2.sort()
print("  <0.05%% 命中：%d" % len(hits2))
for ad, d, s in hits2[:10]:
    print("    [%+.4f%%] %s → %.5f" % (d, s, TARGET*(1+d/100)))

print("\n[判定]")
if hits:
    print("  ★ 单修正命中：%s（偏差 %+.4f%%）" % (hits[0][2], hits[0][1]))
else:
    print("  无单修正闭合——F_np 候选维持边缘外——开放登记")
if hits2:
    print("  ★ 双修正命中：%s（偏差 %+.4f%%）——但双修正过拟合警示" % (hits2[0][2], hits2[0][1]))

result = {"base": BASE, "base_dev": dev(BASE, TARGET), "hits1": hits[:5], "hits2": hits2[:5]}
with open(r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_phase102b_p7_1_fnp_correction.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("\nexit 0")
