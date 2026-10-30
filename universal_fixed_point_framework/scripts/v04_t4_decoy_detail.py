# -*- coding: utf-8 -*-
"""104az-214b：T4 decoy 命中的 σ 深度与参数身份明细
判定口径：若 decoy 命中含 σ < 1.493（真实最优）且参数全框架身份 → g_p/2"深命中唯一"亦崩；
若 decoy 命中全在 σ > 1.493 → g_p/2 保留"深命中质量唯一"。
"""
from fractions import Fraction
import random

K = [2, 3, 4, 5, 7, 8, 16, 25, 49, 64]
D = [45, 231, 320, 675, 65, 256, 14400, 16, 25, 64, 40, 100]
R = sorted({Fraction(k, d) for k in K for d in D})
M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]

T = 2.79284734463
SIG = 8.2e-8
Rf = [(p, float(p)) for p in R]

def scan_detail(target):
    """返回 σ≤5 命中列表 (σ, a, b, c, p, q)。"""
    hits = []
    for a in M:
        af = float(a)
        for b in M:
            bf = float(b)
            for c in M:
                cf = float(c)
                for p, pf in Rf:
                    for q, qf in Rf:
                        denom = cf + qf
                        if abs(denom) < 1e-15:
                            continue
                        d2 = bf / denom
                        if abs(d2) < 1e-15:
                            continue
                        vf = (af - pf) / d2
                        sd = abs(vf - target) / SIG
                        if sd <= 5.0:
                            hits.append((sd, a, b, c, p, q))
    return hits

# 真实目标与 decoy 集（与 v04_t4_decoy.py 同 seed/序列）
rng = random.Random(214)
decoys = [round(T * (0.9 + 0.2 * rng.random()), 8) for _ in range(8)]

print("===== 真实 g_p/2 =====", flush=True)
h = scan_detail(T)
h.sort()
print("σ≤5 命中 %d；top5：" % len(h), flush=True)
for sd, a, b, c, p, q in h[:5]:
    print("  σ=%.3f  A=%d B=%d C=%d p=%s q=%s" % (sd, a, b, c, p, q), flush=True)
print("", flush=True)

for i, dT in enumerate(decoys):
    h = scan_detail(dT)
    h.sort()
    if not h:
        print("decoy %d = %.8f：零命中" % (i, dT), flush=True)
    else:
        print("decoy %d = %.8f：σ≤5 命中 %d；top3：" % (i, dT, len(h)), flush=True)
        for sd, a, b, c, p, q in h[:3]:
            print("    σ=%.3f  A=%d B=%d C=%d p=%s q=%s" % (sd, a, b, c, p, q), flush=True)
    print("", flush=True)
