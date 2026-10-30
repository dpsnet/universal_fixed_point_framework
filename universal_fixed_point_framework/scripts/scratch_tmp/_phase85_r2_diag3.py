# -*- coding: utf-8 -*-
"""查 Koester 谱波长覆盖 + 各带有效性统计"""
import os, re, numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_koester_spec"
spans = []
for fn in os.listdir(BASE):
    if not fn.endswith(".dat"):
        continue
    arr = np.loadtxt(os.path.join(BASE, fn))
    spans.append((float(arr[0, 0]), float(arr[-1, 0]), len(arr)))
lo = min(s[0] for s in spans)
hi = max(s[1] for s in spans)
print("Koester 波长范围: %.0f - %.0f (n_files=%d)" % (lo, hi, len(spans)))
# 各带覆盖统计
for nm, bd in [("3600-3640", (3600, 3640)), ("3700-3750", (3700, 3750)), ("4000-4060", (4000, 4060)), ("4800-4840", (4800, 4840)), ("5000-5800", (5000, 5800))]:
    n_ok = sum(1 for s in spans if s[0] <= bd[0] and s[1] >= bd[1])
    print("%-10s 覆盖 %d/%d" % (nm, n_ok, len(spans)))
