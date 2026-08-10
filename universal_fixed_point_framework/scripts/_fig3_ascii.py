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
