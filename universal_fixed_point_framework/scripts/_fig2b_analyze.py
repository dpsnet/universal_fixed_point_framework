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
"""第二张截图（961x830）宽松阈值结构分析。"""
import numpy as np
from PIL import Image
from scipy import ndimage

im = Image.open(r"e:\workspace\hyper-resolution\docs\ScreenShot_2026-07-12_153343_036.png").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 140) & (G < 140) & (B < 140)

# 边框检测：投影
col_sum = dark.sum(axis=0)
row_sum = dark.sum(axis=1)
print("col>200 rows:", np.where(col_sum > 200)[0])
print("row>200 rows:", np.where(row_sum > 200)[0])
print("col max 5:", np.argsort(col_sum)[-5:], "row max 5:", np.argsort(row_sum)[-5:])

def clusters(mask, min_size=5):
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

red = (R > 140) & (R > G + 40) & (R > B + 40)
green = (G > 110) & (G > R + 25) & (G > B + 25)
blue = (B > 140) & (B > R + 40) & (B > G + 25)
print("px red", red.sum(), "green", green.sum(), "blue", blue.sum())
for name, m in [("RED", red), ("GREEN", green), ("BLUE", blue)]:
    c = clusters(m)
    if c:
        print(name + ":")
        for p in c:
            print("  ", p)
