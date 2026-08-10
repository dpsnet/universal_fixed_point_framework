#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查蓝点 x 300-360, y 270-330 区域像素。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
px = im.load()
cnt = 0
for x in range(300, 360):
    for y in range(260, 340):
        r, g, b = px[x, y]
        if b > 130 and b > r + 30 and g < 150:
            cnt += 1
print("blue px in (300-360, 260-340):", cnt)
# 打印该区域中心像素颜色样例
for (cx, cy) in [(326, 295), (326, 300), (330, 295), (320, 295), (326, 290)]:
    print(cx, cy, px[cx, cy])
