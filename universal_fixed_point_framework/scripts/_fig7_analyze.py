#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""定位 xu2021_fig7 截图中的红/蓝数据点像素坐标。"""
from PIL import Image
import numpy as np

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im)
h, w, _ = a.shape

def mask_for(color, tol=60):
    return (np.abs(a.astype(int) - np.array(color)).sum(axis=2) < tol)

red = mask_for([200, 0, 0])
blue = mask_for([40, 90, 160])
print("red px:", red.sum(), " blue px:", blue.sum())

for name, m in (("red", red), ("blue", blue)):
    ys, xs = np.where(m)
    if len(xs) == 0:
        continue
    # 聚类：按 x 分箱
    xs_r = np.round(xs / 20).astype(int)
    print("=== %s: x分布（每20px一箱）===" % name)
    for bx in range(xs_r.min(), xs_r.max() + 1):
        mm = xs_r == bx
        if mm.sum() == 0:
            continue
        print("  x[%4d-%4d]: n=%d, y范围[%4d,%4d], y均值=%.0f"
              % (bx*20, bx*20+19, mm.sum(), ys[mm].min(), ys[mm].max(), ys[mm].mean()))
