#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""裁剪第三张截图区域查看。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\docs\12983e2a-d0e0-43a3-ab99-10a19dffc76f.png").convert("RGB")
regions = {
    "upper": (0, 150, 920, 350),   # 上部（y=150-350）
    "mid":   (0, 350, 920, 550),   # 中部
    "formula": (0, 690, 920, 870), # 下部（公式区）
}
for name, box in regions.items():
    c = im.crop(box)
    c2 = c.resize((c.width * 2, c.height * 2), Image.LANCZOS)
    p = rf"C:\Users\dps_n\Desktop\f3_{name}.png"
    c2.save(p)
    print("saved:", p, c2.size)
