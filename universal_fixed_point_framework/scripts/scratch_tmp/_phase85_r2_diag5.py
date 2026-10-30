# -*- coding: utf-8 -*-
"""查 Koester 谱 3600-3750 流量值（修正路径）"""
import os, re, numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
KDIR = os.path.join(BASE, "_koester_spec")
best = None
for fn in os.listdir(KDIR):
    mm = re.match(r"fid\d+_([\d.]+)_([\d.]+)\.dat", fn)
    if not mm:
        continue
    t, g = float(mm.group(1)), float(mm.group(2))
    score = (t - 10059) ** 2 + (g - 8.0) ** 2
    if best is None or score < best[0]:
        best = (score, os.path.join(KDIR, fn))
print("选中:", os.path.basename(best[1]))
arr = np.loadtxt(best[1])
wl, fl = arr[:, 0], arr[:, 1]
for nm, bd in [("3600-3640", (3600, 3640)), ("3700-3750", (3700, 3750)),
               ("4000-4060", (4000, 4060)), ("5000-5800", (5000, 5800))]:
    m = (wl >= bd[0]) & (wl <= bd[1])
    f = fl[m]
    print("%s n=%d min=%.4g max=%.4g med=%.4g nan=%d le0=%d" % (
        nm, len(f), f.min(), f.max(), np.median(f),
        int(np.isnan(f).sum()), int(np.sum(f <= 0))))
