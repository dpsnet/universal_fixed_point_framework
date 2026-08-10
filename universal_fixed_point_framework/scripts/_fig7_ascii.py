#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ASCII 可视化读取图 7 轴刻度数字。"""
import numpy as np
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 120) & (G < 120) & (B < 120)

def ascii_art(arr, th=3):
    """arr: 2D bool; 输出每 th 像素采样的字符。"""
    h, w = arr.shape
    out = []
    for y in range(0, h, th):
        line = []
        for x in range(0, w, th):
            blk = arr[y:y + th, x:x + th].mean()
            line.append("#" if blk > 0.25 else "." if blk > 0.05 else " ")
        out.append("".join(line))
    return "\n".join(out)

# y 轴刻度数字 x∈[60,104]（边框 x=112 左侧）
print("=" * 60)
print("Y-AXIS labels (x=60..104):")
for (y0, y1) in [(0, 40), (105, 145), (215, 260), (330, 372), (445, 490), (560, 605)]:
    print(f"\n-- y={y0}..{y1} --")
    print(ascii_art(dark[y0:y1, 60:104], 3))

# x 轴刻度数字 y∈[594,626]
print("=" * 60)
print("X-AXIS labels (y=594..626):")
# 检测各标签块：y=594..626 内黑像素列投影聚类
xl = dark[594:626, 100:980]
cols = np.where(xl.sum(axis=0) > 0)[0]
groups = []
if len(cols):
    start = prev = cols[0]
    for c in cols[1:]:
        if c - prev > 40:      # 标签间空隙
            groups.append((start, prev))
            start = c
        prev = c
    groups.append((start, prev))
for g in groups:
    x0, x1 = g
    x0a, x1a = x0 + 100 - 5, x1 + 100 + 6
    print(f"\n-- xlabel at x={x0+100}..{x1+100} --")
    print(ascii_art(dark[594:626, max(0, x0a):x1a], 3))
