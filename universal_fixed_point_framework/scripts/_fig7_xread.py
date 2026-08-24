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
"""细读 x 轴刻度数字（th=2）。"""
import numpy as np
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 120) & (G < 120) & (B < 120)

def art(arr):
    h, w = arr.shape
    out = []
    for y in range(0, h, 2):
        line = []
        for x in range(0, w, 2):
            blk = arr[y:y + 2, x:x + 2].mean()
            line.append("#" if blk > 0.25 else "+" if blk > 0.08 else " ")
        out.append("".join(line))
    return "\n".join(out)

# x 轴标签区域 y=594..628
xl = dark[594:630, 95:980]
cols = np.where(xl.sum(axis=0) > 0)[0]
groups = []
if len(cols):
    start = prev = cols[0]
    for c in cols[1:]:
        if c - prev > 25:
            groups.append((start, prev))
            start = c
        prev = c
    groups.append((start, prev))
print("label groups:", [(g[0] + 95, g[1] + 95) for g in groups])
for g in groups:
    x0a, x1a = max(0, g[0] + 95 - 4), g[1] + 95 + 4
    print(f"\n== x label at {x0a}..{x1a} ==")
    print(art(dark[594:630, x0a:x1a]))
