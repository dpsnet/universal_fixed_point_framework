#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第二张截图上下区域裁剪。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\docs\ScreenShot_2026-07-12_153343_036.png").convert("RGB")
W, H = im.size
regions = {
    "top":   (0, 0, W, 400),
    "bot":   (0, 400, W, H),
    "mid2":  (0, 200, W, 420),
}
for name, box in regions.items():
    c = im.crop(box)
    c2 = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
    p = rf"C:\Users\dps_n\Desktop\f2_{name}.png"
    c2.save(p)
    print("saved:", p, c2.size)
