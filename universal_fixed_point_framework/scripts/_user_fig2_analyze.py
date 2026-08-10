#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析用户第二张截图（920x919）。"""
import numpy as np
from PIL import Image
from scipy import ndimage

im = Image.open(r"e:\workspace\hyper-resolution\docs\12983e2a-d0e0-43a3-ab99-10a19dffc76f.png").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 130) & (G < 130) & (B < 130)

# 边框
col_sum = dark.sum(axis=0)
row_sum = dark.sum(axis=1)
cols = np.where(col_sum > H * 0.3)[0]
rows = np.where(row_sum > W * 0.3)[0]
print("size:", (W, H))
print("vlines cols:", (cols.min(), cols.max()) if len(cols) else None)
print("hlines rows:", (rows.min(), rows.max()) if len(rows) else None)

def clusters(mask, min_size=8):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3), dtype=bool))
    objs = ndimage.find_objects(lab)
    pts = []
    for i in range(1, n + 1):
        sl = objs[i - 1]
        ys, xs = np.where(lab[sl] == i)
        if len(ys) < min_size:
            continue
        pts.append((round(xs.mean() + sl[1].start, 1), round(ys.mean() + sl[0].start, 1), int(len(ys))))
    return pts

red = (R > 150) & (G < 90) & (B < 90)
green = (G > 120) & (R < 110) & (B < 110)
blue = (B > 150) & (R < 90) & (G < 110)
print("px: red", red.sum(), "green", green.sum(), "blue", blue.sum())
for name, m in [("RED", red), ("GREEN", green), ("BLUE", blue)]:
    print(name + ":")
    for p in clusters(m):
        print("  ", p)
