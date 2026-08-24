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
"""ASCII 显示 x 290-370, y 250-350 彩色像素。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
px = im.load()

def ch(r, g, b):
    if r > 130 and r > g + 40 and r > b + 40:
        return 'R'
    if b > 130 and b > r + 30 and g < 150:
        return 'B'
    if g > 100 and g > r + 20 and g > b + 20:
        return 'G'
    return '.'

x0, x1, y0, y1 = 290, 370, 250, 350
for y in range(y0, y1, 2):
    line = []
    for x in range(x0, x1, 1):
        r, g, b = px[x, y]
        line.append(ch(r, g, b))
    print(f"{y:3d} " + ''.join(line))
