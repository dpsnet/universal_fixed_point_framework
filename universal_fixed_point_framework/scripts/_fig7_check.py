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
"""核查：1) x>850 是否还有蓝/绿点(3.01MPa); 2) 蓝点第4簇非单调原因。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
W, H = im.size
px = im.load()

def clusters_in(x0, x1, y0, y1, color, th=3):
    """在区域内找颜色簇，返回 (cx, cy, n)。color: 'green'/'blue'/'red'"""
    pts = []
    for x in range(x0, x1):
        for y in range(y0, y1):
            r, g, b = px[x, y]
            if color == 'green' and g > 100 and g > r + 20 and g > b + 20:
                pts.append((x, y))
            elif color == 'blue' and b > 130 and b > r + 30 and g < 150:
                pts.append((x, y))
            elif color == 'red' and r > 130 and r > g + 40 and r > b + 40:
                pts.append((x, y))
    if not pts:
        return []
    # 简单网格聚类
    grid = {}
    for x, y in pts:
        key = (x // 6, y // 6)
        grid.setdefault(key, []).append((x, y))
    clusters = []
    while grid:
        seed_k = next(iter(grid))
        stack = [seed_k]
        members = []
        while stack:
            k = stack.pop()
            if k not in grid:
                continue
            members.extend(grid.pop(k))
            gx, gy = k
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nk = (gx + dx, gy + dy)
                    if nk in grid:
                        stack.append(nk)
        if len(members) >= th:
            cx = sum(p[0] for p in members) / len(members)
            cy = sum(p[1] for p in members) / len(members)
            clusters.append((round(cx, 1), round(cy, 1), len(members)))
    return sorted(clusters)

print("== 蓝点 x>830, y 0-590 ==")
for c in clusters_in(830, W, 0, 590, 'blue'):
    print(c)
print("== 绿点 x>830, y 0-590 ==")
for c in clusters_in(830, W, 0, 590, 'green'):
    print(c)
print("== 蓝点 x 460-540, y 200-400 ==")
for c in clusters_in(460, 540, 200, 400, 'blue'):
    print(c)
print("== 绿点 x 460-540, y 200-400 ==")
for c in clusters_in(460, 540, 200, 400, 'green'):
    print(c)
print("== 红点 x 460-540, y 200-400 ==")
for c in clusters_in(460, 540, 200, 400, 'red'):
    print(c)
print("== 蓝点 x 830-982, y 100-260 全部像素点(排除图例) ==")
for c in clusters_in(830, W, 0, 420, 'blue'):
    print(c)
