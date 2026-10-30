# -*- coding: utf-8 -*-
"""Phase 104az-52：η_comp=0.8 每线交叉场强扫描——同位 41 MG 检验"""
import json, math
import numpy as np
from _phase100_p3b_compression import eta_comp, tail_fraction
names = {3: "Hα", 4: "Hβ", 5: "Hγ", 6: "Hδ", 7: "Hε"}

def cross_field(n, target, C, lo=1.0, hi=1e5):
    """二分求 eta_comp(n,B)=target 的 B（特斯拉）"""
    assert eta_comp(n, lo, C) < target < eta_comp(n, hi, C), (n, eta_comp(n, lo, C), eta_comp(n, hi, C))
    for _ in range(60):
        mid = 0.5*(lo+hi)
        if eta_comp(n, mid, C) < target:
            lo = mid
        else:
            hi = mid
    return 0.5*(lo+hi)

for C in (2.0, 3.0, 3.03, 4.0):
    print("=== C = %.2f：η_comp = 0.8 每线交叉场强 ===" % C)
    for n in (3, 4, 5, 6, 7):
        B_T = cross_field(n, 0.8, C)
        B_MG = B_T / 100.0  # 特斯拉→MG（1MG=100T）
        print("  %s (n=%d): B_0.8 = %.2f MG  (%.1f T)" % (names[n], n, B_MG, B_T))
    print()

# C=3.03 时也输出 0.5/0.9 交叉作参考
print("=== C=3.03：η_comp = 0.5 / 0.8 / 0.9 交叉场强 ===")
for n in (3, 4, 5, 6, 7):
    row = []
    for t in (0.5, 0.8, 0.9):
        B_MG = cross_field(n, t, 3.03) / 100.0
        row.append("η=%.1f→%.0f MG" % (t, B_MG))
    print("  %s: %s" % (names[n], "  ".join(row)))

# 41 MG 处各线 η_comp 值
print("\n=== 41 MG 处各线 η_comp（C=3.03）——同位性定量 ===")
for n in (3, 4, 5, 6, 7):
    print("  %s (n=%d): η_comp(41MG) = %.4f" % (names[n], n, eta_comp(n, 4100.0, 3.03)))
