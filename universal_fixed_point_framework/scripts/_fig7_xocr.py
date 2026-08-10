#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""裁剪图7 x轴7个刻度标签 + 蓝绿最右点区域，放大供 OCR/目视。"""
from PIL import Image
import os

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
out = r"C:\Users\dps_n\Desktop"
# x 轴标签中心 col（7 个）与标签数字实际所在区域（标签中心下方 y 590-640）
labels = [113, 250, 393, 535, 675, 817, 960]
for i, c in enumerate(labels):
    box = (max(0, c-55), 585, min(im.width, c+55), 665)
    crop = im.crop(box)
    crop = crop.resize((crop.width*6, crop.height*6), Image.LANCZOS)
    p = os.path.join(out, f"xlab{i}.png")
    crop.save(p)
    print("saved", p, crop.size)

# 蓝绿最右点区域（x 850-982, y 100-260）放大
for nm, box in {"blgr": (850, 100, 982, 260)}.items():
    crop = im.crop(box)
    crop = crop.resize((crop.width*6, crop.height*6), Image.LANCZOS)
    p = os.path.join(out, f"{nm}.png")
    crop.save(p)
    print("saved", p, crop.size)
