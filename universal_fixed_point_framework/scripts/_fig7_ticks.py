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
"""检测 xu2021_fig7 截图坐标轴刻度线位置（黑色短线），以校准 x/y 轴映射。"""
from PIL import Image
import numpy as np

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im)
h, w, _ = a.shape
black = a.sum(axis=2) < 200

# 之前检测：竖边框 col≈113 和 963；横边框 row≈15 和 589
x_left, x_right = 113, 963
y_top, y_bot = 15, 589

# 检测 x 轴下方（row 590-620）的垂直黑线段（刻度线）：列密度
print("=== x 轴下方刻度候选（row 590-620 黑色像素列分布）===")
for cx in range(x_left, x_right + 1):
    cnt = black[y_bot:y_bot + 35, cx].sum()
    if cnt > 15:
        print("  col %d: n=%d" % (cx, cnt))

# 检测 y 轴左侧（col 80-113）的水平黑线段（刻度线）：行分布
print("=== y 轴左侧刻度候选（col 78-112 黑色像素行分布）===")
for ry in range(y_top, y_bot + 1):
    cnt = black[ry, 78:112].sum()
    if cnt > 15:
        print("  row %d: n=%d" % (ry, cnt))
