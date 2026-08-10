#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 xu2021_fig7 截图精确提取数据点：聚类红/蓝像素质心，检测轴刻度。"""
from PIL import Image
import numpy as np

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im)
h, w, _ = a.shape

def mask(color, tol=70):
    return np.abs(a.astype(int) - np.array(color)).sum(axis=2) < tol

def clusters(mask2d, min_size=6, gap=12):
    """按连通分量聚类（简单贪心：按 x 排序后合并）"""
    ys, xs = np.where(mask2d)
    if len(xs) == 0:
        return []
    pts = sorted(zip(xs, ys))
    groups = []
    for x, y in pts:
        placed = False
        for g in groups:
            gx = sum(p[0] for p in g) / len(g)
            gy = sum(p[1] for p in g) / len(g)
            if abs(x - gx) < gap and abs(y - gy) < gap:
                g.append((x, y))
                placed = True
                break
        if not placed:
            groups.append([(x, y)])
    out = []
    for g in groups:
        if len(g) >= min_size:
            gx = sum(p[0] for p in g) / len(g)
            gy = sum(p[1] for p in g) / len(g)
            out.append((gx, gy, len(g)))
    return out

red = mask([200, 0, 0])
blue = mask([40, 90, 160])
print("red px:", red.sum(), "blue px:", blue.sum())
print("=== 红色聚类（x,y,n）===")
for c in sorted(clusters(red)):
    print("  (%.0f, %.0f, n=%d)" % c)
print("=== 蓝色聚类（x,y,n）===")
for c in sorted(clusters(blue)):
    print("  (%.0f, %.0f, n=%d)" % c)

# 检测黑色轴线/网格：统计每行/列的黑色像素密度
black = a.sum(axis=2) < 200
row_density = black.sum(axis=1)
col_density = black.sum(axis=0)
print("=== 黑色列密度峰值（可能是竖轴/刻度）===")
for cx in np.where(col_density > h * 0.3)[0]:
    print("  col %d: %d" % (cx, col_density[cx]))
print("=== 黑色行密度峰值（可能是横轴/刻度）===")
for ry in np.where(row_density > w * 0.3)[0]:
    print("  row %d: %d" % (ry, row_density[ry]))
