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
"""精确检测 x/y 轴刻度线位置（轴线上方的深色短竖线），统一标定。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
px = im.load()

def dark(x, y):
    r, g, b = px[x, y]
    return r < 120 and g < 120 and b < 120

# x 轴刻度线：y 583-590 每列深色像素计数（跳过轴框线本身 y>=588）
xlines = []
for x in range(100, 975):
    c = sum(1 for y in range(584, 588) if dark(x, y))
    if c >= 2:
        xlines.append(x)
# 合并连续列
clusters = []
for x in xlines:
    if clusters and x - clusters[-1][-1] <= 2:
        clusters[-1].append(x)
    else:
        clusters.append([x])
print("x 轴刻度线中心:", [round(sum(c)/len(c), 1) for c in clusters])

# y 轴刻度线：x 108-114 每行深色像素计数（y 轴框线在 x~112）
ylines = []
for y in range(0, 590):
    c = sum(1 for x in range(108, 112) if dark(x, y))
    if c >= 2:
        ylines.append(y)
clusters = []
for y in ylines:
    if clusters and y - clusters[-1][-1] <= 2:
        clusters[-1].append(y)
    else:
        clusters.append([y])
print("y 轴刻度线中心:", [round(sum(c)/len(c), 1) for c in clusters])
