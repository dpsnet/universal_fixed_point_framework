#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""裁剪 x 轴单位文字（y=620-670）和第一个/最后一个刻度数字。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
regions = {
    "xunit": (200, 615, 950, 690),      # x 轴单位（下半部）
    "x0":    (85, 590, 150, 636),        # 刻度 0
    "x1":    (222, 590, 290, 636),       # 刻度 1
    "x6":    (930, 590, 985, 636),       # 刻度 6（最后）
}
for name, box in regions.items():
    c = im.crop(box)
    c2 = c.resize((c.width * 10, c.height * 10), Image.LANCZOS)
    p = rf"C:\Users\dps_n\Desktop\fin_{name}.png"
    c2.save(p)
    print("saved:", p, c2.size)
