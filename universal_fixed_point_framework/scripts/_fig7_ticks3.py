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
"""图 7 刻度线精确检测：边框 tick marks 位置。"""
import numpy as np
from PIL import Image
from scipy import ndimage

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 120) & (G < 120) & (B < 120)

# 底边框 y=590。x tick 短线：y∈[590,604]（向下伸出）的垂直短线段
xt = dark[590:604, 100:980]
l, n = ndimage.label(xt, structure=np.ones((3, 3), dtype=bool))
objs = ndimage.find_objects(l)
xticks = []
for i in range(1, n + 1):
    sl = objs[i - 1]
    ys, xs = np.where(l[sl] == i)
    if len(xs) < 3:
        continue
    xticks.append(round(xs.mean() + sl[1].start, 1))
print("X ticks (col):", sorted(xticks))

# 左边框 x=112。y tick 短线：x∈[98,112]（向左伸出）的水平短线段
yt = dark[0:620, 98:112]
l, n = ndimage.label(yt, structure=np.ones((3, 3), dtype=bool))
objs = ndimage.find_objects(l)
yticks = []
for i in range(1, n + 1):
    sl = objs[i - 1]
    ys, xs = np.where(l[sl] == i)
    if len(ys) < 3:
        continue
    yticks.append(round(ys.mean() + sl[0].start, 1))
print("Y ticks (row):", sorted(yticks))

# 刻度数字位置检测：左轴 x∈[60,100] 的数字（黑像素行投影），底轴 y∈[594,620] 的数字
xlbl = dark[13:590, 60:100]
rows = np.where(xlbl.sum(axis=1) > 0)[0]
print("Y label black rows (px, row):", [(int(r), int(xlbl.sum(axis=1)[r])) for r in rows[::3]][:40] if len(rows) else "none")

xl = dark[594:622, 100:975]
cols = np.where(xl.sum(axis=0) > 0)[0]
# 聚类相邻列
groups = []
if len(cols):
    start = prev = cols[0]
    for c in cols[1:]:
        if c - prev > 5:
            groups.append((start, prev))
            start = c
        prev = c
    groups.append((start, prev))
print("X label black col groups:", groups)
