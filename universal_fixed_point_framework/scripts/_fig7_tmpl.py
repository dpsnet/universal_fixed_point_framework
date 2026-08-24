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
"""模板匹配：y 轴 '0'/'5' 模板识别 x 轴刻度字符。"""
import numpy as np
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (R < 150) & (G < 150) & (B < 150)

def extract(x0, x1, y0, y1):
    return dark[y0:y1, x0:x1].astype(np.uint8)

def split_chars(x0, x1, y0, y1, min_gap=3):
    """按列黑像素投影切分字符。"""
    sub = dark[y0:y1, x0:x1]
    col = sub.sum(axis=0)
    cols = np.where(col > 0)[0]
    if not len(cols):
        return []
    chars = []
    start = prev = cols[0]
    for c in cols[1:]:
        if c - prev > min_gap:
            chars.append((start, prev))
            start = c
        prev = c
    chars.append((start, prev))
    return [(x0 + s, x0 + e) for s, e in chars]

# y 轴模板：yl4="5"(行473), yl5="0"(行583)。x 范围 60..104
t5 = extract(60, 104, 461, 488)   # "5"（行 473±12）
t0 = extract(60, 104, 571, 598)   # "0"（行 583±12）
print("t5 shape:", t5.shape, " t0 shape:", t0.shape)

def norm(arr):
    arr = arr.copy()
    h, w = arr.shape
    # 去空白边缘
    rows = np.where(arr.sum(axis=1) > 0)[0]
    cols = np.where(arr.sum(axis=0) > 0)[0]
    if len(rows) == 0 or len(cols) == 0:
        return None
    return arr[rows.min():rows.max() + 1, cols.min():cols.max() + 1].astype(float)

t5c = norm(t5)
t0c = norm(t0)
print("t5 trimmed:", t5c.shape, " t0 trimmed:", t0c.shape)

def match(ch, tmpl):
    """IoU 相似度（缩放对齐）。"""
    chc = norm(ch)
    if chc is None or tmpl is None:
        return 0.0
    h1, w1 = chc.shape
    h2, w2 = tmpl.shape
    # 缩放 tmpl 到 ch 尺寸
    from PIL import Image as I2
    tmpl_img = I2.fromarray((tmpl * 255).astype(np.uint8))
    tmpl_r = tmpl_img.resize((w1, h1), I2.LANCZOS)
    tmpl_r = np.asarray(tmpl_r) > 100
    chb = chc > 0
    inter = (chb & tmpl_r).sum()
    union = (chb | tmpl_r).sum()
    return inter / union if union > 0 else 0.0

# x 轴标签：中心 113,250,393,535,675,817,960
cents = [113, 250, 393, 535, 675, 817, 960]
for i, c in enumerate(cents):
    chars = split_chars(c - 30, c + 30, 594, 630)
    desc = []
    for (x0, x1) in chars:
        ch = extract(x0, x1, 594, 630)
        s0 = match(ch, t0c)
        s5 = match(ch, t5c)
        # 其他数字候选：1=窄, 2/3/4/6 用宽高比区分
        h, w = ch.shape
        ratio = h / max(w, 1)
        if s0 > s5 and s0 > 0.5:
            desc.append("0")
        elif s5 > s0 and s5 > 0.5:
            desc.append("5")
        elif ratio > 2.2:
            desc.append("1")
        else:
            desc.append(f"?({s0:.2f}/{s5:.2f})")
    print(f"x label {i} (x≈{c}): {' '.join(desc)}")
