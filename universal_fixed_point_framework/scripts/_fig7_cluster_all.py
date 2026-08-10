#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全图三色精确聚类，输出所有数据点中心，供最终转录。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
W, H = im.size
px = im.load()

def find_clusters(color):
    pts = []
    for x in range(W):
        for y in range(0, 590):   # 排除底部 y 轴数字区
            r, g, b = px[x, y]
            if color == 'green' and g > 100 and g > r + 20 and g > b + 20:
                pts.append((x, y))
            elif color == 'blue' and b > 130 and b > r + 30 and g < 150:
                pts.append((x, y))
            elif color == 'red' and r > 130 and r > g + 40 and r > b + 40:
                pts.append((x, y))
    grid = {}
    for x, y in pts:
        grid.setdefault((x // 8, y // 8), []).append((x, y))
    cl = []
    while grid:
        seed = next(iter(grid))
        stack = [seed]
        mem = []
        while stack:
            k = stack.pop()
            if k not in grid:
                continue
            mem.extend(grid.pop(k))
            gx, gy = k
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nk = (gx + dx, gy + dy)
                    if nk in grid:
                        stack.append(nk)
        if len(mem) >= 30:
            cx = sum(p[0] for p in mem) / len(mem)
            cy = sum(p[1] for p in mem) / len(mem)
            cl.append((round(cx, 1), round(cy, 1), len(mem)))
    return sorted(cl, key=lambda t: (t[0], t[1]))

for cname in ['green', 'blue', 'red']:
    print(f"===== {cname} =====")
    for c in find_clusters(cname):
        print(c)
