#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""右下角图例区域彩色 ASCII 可视化。"""
import numpy as np
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)
x0, y0, x1, y1 = 700, 420, 962, 590
R, G, B = a[y0:y1, x0:x1, 0], a[y0:y1, x0:x1, 1], a[y0:y1, x0:x1, 2]

def char(r, g, b):
    if r > 150 and g < 90 and b < 90:
        return "R"
    if b > 150 and r < 90:
        return "B"
    if r > 150 and g > 150 and b > 150:
        return "W"
    if r < 100 and g < 100 and b < 100:
        return "K"
    if abs(r - g) < 30 and abs(g - b) < 30:
        return "G"
    return "."

th = 4
for yy in range(0, y1 - y0, th):
    line = []
    for xx in range(0, x1 - x0, th):
        r = R[yy:yy + th, xx:xx + th].mean()
        g = G[yy:yy + th, xx:xx + th].mean()
        b = B[yy:yy + th, xx:xx + th].mean()
        line.append(char(r, g, b))
    print(f"{y0+yy:4d} " + "".join(line))
