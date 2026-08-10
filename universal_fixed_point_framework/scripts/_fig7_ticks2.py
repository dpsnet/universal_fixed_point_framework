#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图 7 精确分析：数据点聚类（排除图例）+ 刻度线位置检测。"""
import numpy as np
from PIL import Image
from scipy import ndimage

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)  # (708, 982, 3)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def clusters(mask, label):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3), dtype=bool))
    objs = ndimage.find_objects(lab)
    pts = []
    for i in range(1, n + 1):
        sl = objs[i - 1]
        ys, xs = np.where(lab[sl] == i)
        cy, cx = ys.mean() + sl[0].start, xs.mean() + sl[1].start
        pts.append((round(cx, 1), round(cy, 1), int(len(ys))))
    return pts

# 红：R 高 G/B 低；蓝：B 高 R 低
red = (R > 150) & (G < 90) & (B < 90)
blue = (B > 150) & (R < 90) & (G < 110)
print("red px:", int(red.sum()), " blue px:", int(blue.sum()))
print("RED clusters (x, y, size):")
for p in clusters(red, "red"):
    print("  ", p)
print("BLUE clusters (x, y, size):")
for p in clusters(blue, "blue"):
    print("  ", p)

# 刻度线检测：绘图区内黑色短线。
# 左轴 x∈[105,125] 内的水平短线（y tick）；底轴 y∈[580,610] 内的垂直短线（x tick）
dark = (R < 100) & (G < 100) & (B < 100)

# y tick：在 x∈[104,126] 中找连通黑色区域，输出其 y 质心（水平短线）
ylab = dark[:, 104:126]
ylab_l, ylab_n = ndimage.label(ylab, structure=np.ones((3, 3), dtype=bool))
objs = ndimage.find_objects(ylab_l)
yticks = []
for i in range(1, ylab_n + 1):
    sl = objs[i - 1]
    ys, xs = np.where(ylab_l[sl] == i)
    if len(ys) < 4:
        continue
    yticks.append(round(ys.mean() + sl[0].start, 1))
print("Y tick positions (row):", sorted(yticks))

# x tick：在 y∈[582,608] 中找连通黑色区域，输出其 x 质心（垂直短线）
xlab = dark[582:608, :]
xlab_l, xlab_n = ndimage.label(xlab, structure=np.ones((3, 3), dtype=bool))
objs = ndimage.find_objects(xlab_l)
xticks = []
for i in range(1, xlab_n + 1):
    sl = objs[i - 1]
    ys, xs = np.where(xlab_l[sl] == i)
    if len(xs) < 4:
        continue
    xticks.append(round(xs.mean() + sl[1].start, 1))
print("X tick positions (col):", sorted(xticks))

# 边框位置复核
dark_col = dark.sum(axis=0)
dark_row = dark.sum(axis=1)
# 找长竖线/横线（>100 像素连续）
cols = np.where(dark_col > 200)[0]
rows = np.where(dark_row > 200)[0]
print("vertical line cols:", cols.min() if len(cols) else None, cols.max() if len(cols) else None)
print("horizontal line rows:", rows.min() if len(rows) else None, rows.max() if len(rows) else None)
