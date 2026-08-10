#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三色数据点聚类：绿(Well-1) 蓝(Well-2) 红(Well-3)。"""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def clusters(mask, min_size=8):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3), dtype=bool))
    objs = ndimage.find_objects(lab)
    pts = []
    for i in range(1, n + 1):
        sl = objs[i - 1]
        ys, xs = np.where(lab[sl] == i)
        if len(ys) < min_size:
            continue
        pts.append((round(xs.mean() + sl[1].start, 1), round(ys.mean() + sl[0].start, 1), int(len(ys))))
    return pts

# 绿：G 高 R/B 低
green = (G > 120) & (R < 110) & (B < 110)
# 绿像素也可能带黄偏色
green2 = (G > 100) & (G > R + 20) & (G > B + 20)
print("green px:", int(green.sum()), " green2 px:", int(green2.sum()))
print("GREEN clusters (x, y, size):")
for p in clusters(green2):
    print("  ", p)

# 图例区域（右下角 x>700, y>420）排除
legend_box = (700, 420, 962, 590)
print("\nLegend region points (排除):")
for name, mask in [("green", green2)]:
    for p in clusters(mask):
        if legend_box[0] < p[0] < legend_box[2] and legend_box[1] < p[1] < legend_box[3]:
            print("  ", name, p)

# 完整三色标注图
im2 = im.copy()
d = ImageDraw.Draw(im2)
red = (R > 150) & (G < 90) & (B < 90)
blue = (B > 150) & (R < 90) & (G < 110)
for i, (cx, cy, sz) in enumerate(clusters(red)):
    tag = "LEG" if (700 < cx < 962 and 420 < cy < 590) else f"R{i}"
    d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], outline=(255, 255, 0), width=2)
    d.text((cx + 8, cy - 8), tag, fill=(255, 255, 0))
for i, (cx, cy, sz) in enumerate(clusters(blue)):
    tag = "LEG" if (700 < cx < 962 and 420 < cy < 590) else f"B{i}"
    d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], outline=(0, 255, 255), width=2)
    d.text((cx + 8, cy - 8), tag, fill=(0, 255, 255))
for i, (cx, cy, sz) in enumerate(clusters(green2)):
    tag = "LEG" if (700 < cx < 962 and 420 < cy < 590) else f"G{i}"
    d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], outline=(255, 0, 255), width=2)
    d.text((cx + 8, cy - 8), tag, fill=(255, 0, 255))
im2 = im2.resize((im2.width * 2, im2.height * 2), Image.LANCZOS)
p = r"C:\Users\dps_n\Desktop\fig7_annotated3.png"
im2.save(p)
print("saved:", p)
