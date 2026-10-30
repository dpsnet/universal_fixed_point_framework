# -*- coding: utf-8 -*-
"""Phase 104az-54b：线间比例（C 无关）+ 41MG 斜率排序（快速独立版）"""
import math
from _phase100_p3b_compression import eta_comp

names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}

print("=== 线间比例（C 无关的纯 n 依赖检验，C=3.03 交叉值）===")
theory = {4: 80.8, 5: 41.4, 6: 19.7, 7: 9.4}
obs = {4: 80.0, 5: 41.0, 6: 20.0, 7: 10.0}
for n in (5, 6, 7):
    r_t = theory[n]/theory[4]
    r_o = obs[n]/obs[4]
    print("  %s/Hβ = %.4f (理论) vs %.4f (观测) -> 偏差 %.3f%%" % (names[n], r_t, r_o, 100*abs(r_t-r_o)/r_o))

print("\n=== 41 MG 处 η_comp 斜率排序（p 变化稳定性，C(p)）===")
for p in (0.95, 0.99, 0.999):
    C = math.sqrt(2.0*math.log(1.0/(1.0-p)))
    slopes = {}
    vals = {}
    for n in (3,4,5,6,7):
        vals[n] = eta_comp(n, 4100.0, C)
        slopes[n] = (eta_comp(n, 4500.0, C) - eta_comp(n, 3700.0, C))/800.0
    order_v = sorted(vals, key=lambda n: -vals[n])
    order_s = sorted(slopes, key=lambda n: -slopes[n])
    print("  p=%.3f C=%.4f | η_comp(41) 序: %s | 斜率序: %s" % (
        p, C, " > ".join(names[n] for n in order_v), " > ".join(names[n] for n in order_s)))
print("  观测变浅序（B≥41 分档 d_pure 变化）：Hγ (−41%) > Hβ (−27%) > Hδ (−12%) > Hε (−2%)")
print("  -> 应匹配斜率序（非 η_comp 值序）：Hγ > Hβ > Hδ > Hε")
