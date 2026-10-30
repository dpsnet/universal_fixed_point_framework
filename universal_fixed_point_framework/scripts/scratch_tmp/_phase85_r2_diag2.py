# -*- coding: utf-8 -*-
"""诊断：单星各连续谱带原始流量统计"""
import os, numpy as np

BASE = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts"
gid = "1003378611740398336"
d = np.load(os.path.join(BASE, "_desi_spec", gid + ".npz"), allow_pickle=True)
wl, fl, iv = d["wave"], d["flux"], d["ivar"]

for nm, bd in [("蓝3600-3640", (3600, 3640)), ("红3700-3750", (3700, 3750)),
               ("A4000-4060", (4000, 4060)), ("B5000-5800", (5000, 5800))]:
    m = (wl >= bd[0]) & (wl <= bd[1])
    n = int(np.sum(m))
    if n == 0:
        print(nm, "无点")
        continue
    f = fl[m]
    print("%s n=%d min=%.4g max=%.4g med=%.4g nleq0=%d nan=%d" % (
        nm, n, f.min(), f.max(), np.median(f), int(np.sum(f <= 0)), int(np.isnan(f).sum())))
print("wave 起点:", wl[0], "终点:", wl[-1], "点数:", len(wl))
