# -*- coding: utf-8 -*-
"""104az-208 补充核验：T5 族内 |g_n/2| ≤3σ 命中的最简分数分布"""
from fractions import Fraction
import time

M = [2, 3, 4, 5, 7, 8, 15, 16, 21, 42, 49, 105]
T = 1.91304273
S = 4.5e-7

counts = {}
total3 = 0
total5 = 0
t0 = time.time()
for a in M:
    for b in M:
        n1 = a * b
        for c in M:
            num = n1 + c
            if num <= 0:
                continue
            for d in M:
                for e in M:
                    m1 = d * e
                    for f in M:
                        den = m1 + f
                        if den == 0:
                            continue
                        fr = Fraction(num, den)
                        vf = float(fr)
                        sd = abs(vf - T) / S
                        if sd <= 3.0:
                            total3 += 1
                            counts[fr] = counts.get(fr, 0) + 1
                        if sd <= 5.0:
                            total5 += 1
print("≤3σ 命中总数: %d（%.1fs）" % (total3, time.time()-t0), flush=True)
print("最简分数种类数: %d" % len(counts), flush=True)
for fr, n in sorted(counts.items(), key=lambda x: -x[1])[:30]:
    v = float(fr)
    print("  %s = %.12f  σ=%.3f  命中 %d 次" % (fr, v, abs(v-T)/S, n), flush=True)
