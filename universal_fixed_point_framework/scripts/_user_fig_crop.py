#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""裁剪用户截图：x 轴刻度 + 公式区域。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\docs\ScreenShot_2026-07-12_153343_036.png").convert("RGB")
W, H = im.size
regions = {
    "full_half": (0, int(H*0.45), W, H),     # 下半（可能含公式）
    "top":       (0, 0, W, int(H*0.5)),      # 上半（图）
}
for name, box in regions.items():
    c = im.crop(box)
    c2 = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    p = rf"C:\Users\dps_n\Desktop\uf_{name}.png"
    c2.save(p)
    print("saved:", p, c2.size)
