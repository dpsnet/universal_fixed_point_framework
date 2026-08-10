#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""裁剪右下角与右上角图例候选区，细读内容。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
regions = {
    "br":   (740, 420, 962, 590),   # 右下角 R5/B5
    "tr":   (700, 40, 962, 300),    # 右上角 R0/B0/B1
    "center":(120, 200, 540, 430),  # 中间密集区
}
for name, box in regions.items():
    c = im.crop(box)
    c2 = c.resize((c.width * 4, c.height * 4), Image.LANCZOS)
    p = r"C:\Users\dps_n\Desktop\fig7d_" + name + ".png"
    c2.save(p)
    print("saved:", p, c2.size)
