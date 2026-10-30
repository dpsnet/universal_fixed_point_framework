# -*- coding: utf-8 -*-
"""Phase 104az-54：p 扫描——C(p) 与其他观测指标（线级激活阈值 80/41/20/10 MG）的对应"""
import math
import numpy as np
from _phase100_p3b_compression import eta_comp

names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}
# 观测激活阈值（26.16j-94：B_0.8 切换点，LAMOST 各线激活阈值）
obs_thr = {4: 80.0, 5: 41.0, 6: 20.0, 7: 10.0}
obs_weight = {4: 1.0, 5: 1.0, 6: 1.0, 7: 0.3}  # Hε LAMOST 蓝端不可靠，降权

def cross_field(n, target, C, lo=1.0, hi=1e5):
    assert eta_comp(n, lo, C) < target < eta_comp(n, hi, C), (n, eta_comp(n, lo, C), eta_comp(n, hi, C))
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if eta_comp(n, mid, C) < target:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo+hi)

def C_of_p(p):
    return math.sqrt(2.0*math.log(1.0/(1.0-p)))

def eval_p(p, verbose=True):
    C = C_of_p(p)
    devs = {}
    for n in (4, 5, 6, 7):
        B = cross_field(n, 0.8, C)/100.0
        dev = 100.0*(B-obs_thr[n])/obs_thr[n]
        devs[n] = (B, dev)
    wsum = sum(obs_weight[n]*abs(devs[n][1]) for n in (4,5,6,7))
    wtot = sum(obs_weight.values())
    wdev = wsum/wtot
    if verbose:
        print("  p=%.4f C=%.4f | Hβ %.1f (%.1f%%) Hγ %.1f (%.1f%%) Hδ %.1f (%.1f%%) Hε %.1f (%.1f%%) | 加权平均 |dev| = %.2f%%"
              % (p, C, devs[4][0], devs[4][1], devs[5][0], devs[5][1], devs[6][0], devs[6][1], devs[7][0], devs[7][1], wdev))
    return wdev

print("=== p 网格扫描：C(p) vs 观测激活阈值（Hβ 80 / Hγ 41 / Hδ 20 / Hε 10 MG）===")
print("  观测激活阈值 = 26.16j-94 B_0.8 切换点（LAMOST 各线激活比例反推）")
results = []
for p in (0.90, 0.95, 0.98, 0.985, 0.99, 0.992, 0.995, 0.997, 0.999):
    wd = eval_p(p)
    results.append((wd, p))

results.sort()
print("\n  最优 p*（最小加权偏差）：p=%.4f, 加权平均 |dev|=%.2f%%" % (results[0][1], results[0][0]))

print("\n=== 框架身份候选 p 的偏差（1-p = 0.01 = (Nc·σ/2)^2）===")
eval_p(0.99, verbose=True)
eval_p(1.0 - (3.0/2.0/15.0)**2, verbose=True)

print("\n=== 线间比例（C 无关的纯 n 依赖检验）===")
print("  B_0.8 比例（C=3.03）：Hγ/Hβ = %.4f | Hδ/Hβ = %.4f | Hε/Hβ = %.4f" % (
    41.4/80.8, 19.7/80.8, 9.4/80.8))
print("  观测比例：            Hγ/Hβ = %.4f | Hδ/Hβ = %.4f | Hε/Hβ = %.4f" % (
    41.0/80.0, 20.0/80.0, 10.0/80.0))
print("  Hγ/Hβ 偏差 = %.3f%%（C 无关！）" % (100*abs(41.4/80.8 - 41.0/80.0)/(41.0/80.0)))
print("  Hδ/Hβ 偏差 = %.3f%%" % (100*abs(19.7/80.8 - 20.0/80.0)/(20.0/80.0)))
print("  Hε/Hβ 偏差 = %.3f%%（Hε LAMOST 蓝端不可靠，参考）" % (100*abs(9.4/80.8 - 10.0/80.0)/(10.0/80.0)))

print("\n=== 41 MG 处观测变浅梯度 vs η_comp(41MG, p) 斜率排序（p 变化稳定性）===")
for p in (0.95, 0.99, 0.999):
    C = C_of_p(p)
    vals = {n: eta_comp(n, 4100.0, C) for n in (4,5,6,7)}
    # 斜率近似：η_comp(45) - η_comp(37) 除以 8MG
    slopes = {}
    for n in (4,5,6,7):
        slopes[n] = (eta_comp(n, 4500.0, C) - eta_comp(n, 3700.0, C))/800.0
    order_v = sorted(vals, key=lambda n: -vals[n])
    order_s = sorted(slopes, key=lambda n: -slopes[n])
    print("  p=%.3f: η_comp(41) 序 %s（Hγ %.3f/Hβ %.3f/Hδ %.3f/Hε %.3f）| 斜率序 %s（观测变浅序 Hγ>Hβ>Hδ>Hε）"
          % (p, [names[n] for n in order_v], vals[5], vals[4], vals[6], vals[7], [names[n] for n in order_s]))
