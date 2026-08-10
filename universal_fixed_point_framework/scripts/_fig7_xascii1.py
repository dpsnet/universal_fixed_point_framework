#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""x 轴刻度数字逐像素 ASCII（th=1）。"""
import numpy as np
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 150) & (G < 150) & (B < 150)  # 含抗锯齿灰

def art(x0, x1, y0=594, y1=630):
    sub = dark[y0:y1, x0:x1]
    # 每字符 = 1 像素列？不，每 2 列 1 字符
    h, w = sub.shape
    out = []
    for yy in range(h):
        line = ""
        for xx in range(0, w, 2):
            blk = sub[yy, xx:xx + 2].mean()
            line += "#" if blk > 0.4 else "+" if blk > 0.12 else " "
        out.append(line.rstrip())
    return "\n".join(out)

# 标签：中心 113, 250, 393, 535, 675, 817, 960，取 x 中心±30
cents = [113, 250, 393, 535, 675, 817, 960]
for i, c in enumerate(cents):
    print(f"\n===== x label {i} (x={c-30}..{c+30}) =====")
    print(art(c - 30, c + 30))
