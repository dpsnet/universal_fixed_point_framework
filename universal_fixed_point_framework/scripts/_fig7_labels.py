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
"""x 轴刻度标签 10 倍放大精确裁剪。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
# 标签中心：113, 250, 393, 535, 675, 817, 960
cents = [113, 250, 393, 535, 675, 817, 960]
for i, c in enumerate(cents):
    box = (c - 45, 590, c + 45, 660)
    crop = im.crop(box)
    crop = crop.resize((crop.width * 10, crop.height * 10), Image.LANCZOS)
    p = rf"C:\Users\dps_n\Desktop\xl{i}.png"
    crop.save(p)
    print("saved:", p, crop.size)
# y 轴：标签行 19,129,246,357,473,583
rows = [19, 129, 246, 357, 473, 583]
for i, r in enumerate(rows):
    box = (40, r - 12, 118, r + 12)
    crop = im.crop(box)
    crop = crop.resize((crop.width * 10, crop.height * 10), Image.LANCZOS)
    p = rf"C:\Users\dps_n\Desktop\yl{i}.png"
    crop.save(p)
    print("saved:", p, crop.size)
