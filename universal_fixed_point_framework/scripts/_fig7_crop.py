#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""裁剪 xu2021_fig7 截图各部分放大，便于视觉读取。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
regions = {
    "full_2x": (0, 0, im.width, im.height),
    "title": (0, 0, im.width, 60),
    "legend": (700, 0, im.width, 708),
    "bottom": (0, 580, im.width, 708),
    "left": (0, 0, 130, 708),
}
for name, box in regions.items():
    c = im.crop(box)
    c2 = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
    p = r"C:\Users\dps_n\Desktop\xu7_" + name + ".png"
    c2.save(p)
    print("saved:", p, c2.size)
