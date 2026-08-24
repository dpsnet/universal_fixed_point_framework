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
"""从 PDF 第 7 页提取图 7 嵌入图片。"""
import pdfplumber
import os

SRC = r"C:\Users\dps_n\Downloads\feart-09-684592.pdf"
OUTDIR = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_fig7_pdf"
os.makedirs(OUTDIR, exist_ok=True)

with pdfplumber.open(SRC) as pdf:
    page = pdf.pages[6]  # 第 7 页（index 6）
    print("page size:", page.width, page.height)
    print("images on page 7:", len(page.images))
    for i, img in enumerate(page.images):
        x0, top, x1, bottom = img["x0"], img["top"], img["x1"], img["bottom"]
        print("  img %d: bbox=(%.0f,%.0f,%.0f,%.0f) size=%.0fx%.0f" %
              (i, x0, top, x1, bottom, x1 - x0, bottom - top))
        crop = page.within_bbox((x0, top, x1, bottom))
        im = crop.to_image(resolution=300)
        p = os.path.join(OUTDIR, "fig7_img%d.png" % i)
        im.save(p)
        print("  saved:", p)
