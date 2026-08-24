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
"""扫描 x 900-982 全高，输出所有非背景像素簇（判断是否还有更右的点）。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
W, H = im.size
px = im.load()

# 背景: 白(255,255,255)或浅灰。找出明显非背景像素
def is_fg(r, g, b):
    return not (r > 245 and g > 245 and b > 245) and not (abs(r-g) < 8 and abs(g-b) < 8 and r < 245)

for (x0, x1) in [(900, W), (820, 900)]:
    print(f"===== x {x0}-{x1} 非背景像素 =====")
    pts = []
    for x in range(x0, x1):
        for y in range(0, 590):
            r, g, b = px[x, y]
            if is_fg(r, g, b):
                pts.append((x, y, (r, g, b)))
    # 聚类
    grid = {}
    for x, y, c in pts:
        grid.setdefault((x // 8, y // 8), []).append((x, y, c))
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
        if len(mem) >= 10:
            xs = [p[0] for p in mem]; ys = [p[1] for p in mem]
            # 平均色
            rs = sum(p[2][0] for p in mem)//len(mem)
            gs = sum(p[2][1] for p in mem)//len(mem)
            bs = sum(p[2][2] for p in mem)//len(mem)
            cl.append((round(sum(xs)/len(xs),1), round(sum(ys)/len(ys),1), len(mem), (rs,gs,bs)))
    for c in sorted(cl, key=lambda t: t[1]):
        print(c)
