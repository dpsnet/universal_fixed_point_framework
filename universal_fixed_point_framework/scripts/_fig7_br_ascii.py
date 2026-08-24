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
"""右下角图例区域彩色 ASCII 可视化。"""
import numpy as np
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)
x0, y0, x1, y1 = 700, 420, 962, 590
R, G, B = a[y0:y1, x0:x1, 0], a[y0:y1, x0:x1, 1], a[y0:y1, x0:x1, 2]

def char(r, g, b):
    if r > 150 and g < 90 and b < 90:
        return "R"
    if b > 150 and r < 90:
        return "B"
    if r > 150 and g > 150 and b > 150:
        return "W"
    if r < 100 and g < 100 and b < 100:
        return "K"
    if abs(r - g) < 30 and abs(g - b) < 30:
        return "G"
    return "."

th = 4
for yy in range(0, y1 - y0, th):
    line = []
    for xx in range(0, x1 - x0, th):
        r = R[yy:yy + th, xx:xx + th].mean()
        g = G[yy:yy + th, xx:xx + th].mean()
        b = B[yy:yy + th, xx:xx + th].mean()
        line.append(char(r, g, b))
    print(f"{y0+yy:4d} " + "".join(line))
