# -*- coding: utf-8 -*-
"""查 Koester 谱 3600-3750 流量值"""
import os, re, numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_koester_spec"
best = None
for fn in os.listdir(BASE):
    mm = re.match(r"fid\d+_([\d.]+)_([\d.]+)\.dat", fn)
    if not mm:
        continue
    t, g = float(mm.group(1)), float(mm.group(2))
    score = (t - 10059) ** 2 + (g - 8.0) ** 2
    if best is None or score < best[0]:
        best = (score, os.path.join(BASE, "_koester_spec", fn))
print("选中:", best[1])
arr = np.loadtxt(best[1])
wl, fl = arr[:, 0], arr[:, 1]
for nm, bd in [("3600-3640", (3600, 3640)), ("3700-3750", (3700, 3750))]:
    m = (wl >= bd[0]) & (wl <= bd[1])
    f = fl[m]
    print("%s n=%d min=%.4g max=%.4g med=%.4g nan=%d le0=%d" % (
        nm, len(f), f.min() if len(f) else -1, f.max() if len(f) else -1,
        np.median(f) if len(f) else -1, int(np.isnan(f).sum()), int(np.sum(f <= 0))))
# 检查 3600-4000 整段
m = (wl >= 3600) & (wl <= 4000)
print("3600-4000 全段 nan:", int(np.isnan(fl[m]).sum()), "le0:", int(np.sum(fl[m] <= 0)))
