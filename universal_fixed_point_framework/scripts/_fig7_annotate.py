# ============================================================
# UFPF → MUFPF 更名通知
# ============================================================
# 本文件属于 Universal Fixed Point Framework (UFPF)。
# 该框架已计划更名为 Meta-Universal Fixed-Point Functorial Framework (MUFPF)。
# 更名计划详见：roadmap/mu_renaming_plan.md
#
# 原因：UFPF 缩写与 IEEE 生物图像识别框架冲突，影响学术检索。
# 新名称 MUFPF 具有全球唯一性，且更好地体现框架的元数学特性。
#
# 本文件中 UFPF 相关引用数量：0
# 更名将在计划确认后统一执行，当前代码不做修改。
# ============================================================

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""标注所有红/蓝聚类及轴刻度，输出到 Desktop 查看。"""
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def clusters(mask, min_size=3):
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

red = (R > 150) & (G < 90) & (B < 90)
blue = (B > 150) & (R < 90) & (G < 110)
# 放宽蓝阈值（空心符号/描边）
blue2 = (B > 130) & (B > R + 30) & (G < 150)

im2 = im.copy()
d = ImageDraw.Draw(im2)
for i, (cx, cy, sz) in enumerate(clusters(red)):
    d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 255, 0), width=2)
    d.text((cx + 10, cy - 8), f"R{i}({cx:.0f},{cy:.0f})", fill=(255, 255, 0))
print("RED:")
for p in clusters(red):
    print("  ", p)
print("BLUE2:")
bp = clusters(blue2)
for p in bp:
    print("  ", p)
for i, (cx, cy, sz) in enumerate(bp):
    d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], outline=(0, 255, 255), width=2)
    d.text((cx + 10, cy - 8), f"B{i}({cx:.0f},{cy:.0f})", fill=(0, 255, 255))
im2 = im2.resize((im2.width * 2, im2.height * 2), Image.LANCZOS)
p = r"C:\Users\dps_n\Desktop\fig7_annotated.png"
im2.save(p)
print("saved:", p)
