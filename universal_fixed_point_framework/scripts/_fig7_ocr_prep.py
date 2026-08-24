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
"""裁剪图 7 轴刻度区域供 OCR。"""
from PIL import Image

im = Image.open(r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf\xu2021_fig7_screenshot.png").convert("RGB")
regions = {
    "xaxis": (60, 585, 982, 660),   # x 轴刻度+单位
    "yaxis": (0, 0, 130, 708),       # y 轴
    "full":  (0, 0, 982, 708),       # 全图（OCR 图例/标题）
}
for name, box in regions.items():
    c = im.crop(box)
    c2 = c.resize((c.width * 3, c.height * 3), Image.LANCZOS)
    p = rf"C:\Users\dps_n\Desktop\ocr_{name}.png"
    c2.save(p)
    print("saved:", p, c2.size)
