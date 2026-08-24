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
"""x 轴标签二值化 ASCII 渲染，目视读取 0/0.5/1.0/1.5/2.5 标签。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
px = im.load()

labels = {0: 113, 1: 250, 2: 393, 3: 535, 5: 817}
for idx, c in labels.items():
    print(f"===== label {idx} (col ~{c}) =====")
    for y in range(586, 630, 1):
        line = []
        for x in range(c - 30, c + 31, 1):
            r, g, b = px[x, y]
            # 深色像素（文字）标记
            dark = (r < 120 and g < 120 and b < 120)
            line.append('#' if dark else '.')
        s = ''.join(line)
        if '#' in s:
            print(f"{y:3d} {s}")
