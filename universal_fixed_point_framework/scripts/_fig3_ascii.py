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
"""第三张截图整体 ASCII 布局。"""
import numpy as np
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\docs\12983e2a-d0e0-43a3-ab99-10a19dffc76f.png").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
# 蓝黑文本（B 高 R 低）
txt = (B > 120) & (R < 120)
# 非白像素（任意文本/图形）
nonwhite = ~((R > 235) & (G > 235) & (B > 235))

th = 4
H, W = nonwhite.shape
for yy in range(0, H, th):
    line = []
    for xx in range(0, W, th):
        blk = nonwhite[yy:yy + th, xx:xx + th].mean()
        t = txt[yy:yy + th, xx:xx + th].mean()
        ch = "B" if t > 0.3 else "#" if blk > 0.3 else "+" if blk > 0.1 else " "
        line.append(ch)
    s = "".join(line).rstrip()
    if s.strip():
        print(f"{yy:4d} {s}")
