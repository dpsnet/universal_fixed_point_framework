#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ASCII 显示 x 460-540, y 220-370（蓝点4/绿点4/红点4 区域）。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
px = im.load()

def ch(r, g, b):
    if r > 130 and r > g + 40 and r > b + 40:
        return 'R'
    if b > 130 and b > r + 30 and g < 150:
        return 'B'
    if g > 100 and g > r + 20 and g > b + 20:
        return 'G'
    return '.'

x0, x1, y0, y1 = 460, 540, 220, 370
for y in range(y0, y1, 2):
    line = []
    for x in range(x0, x1, 1):
        r, g, b = px[x, y]
        line.append(ch(r, g, b))
    print(f"{y:3d} " + ''.join(line))
