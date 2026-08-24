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
"""提取 PDF 第 7-8 页所有图片，渲染整页查看布局。"""
import pdfplumber
import os

SRC = r"C:\Users\dps_n\Downloads\feart-09-684592.pdf"
OUTDIR = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_pages"
os.makedirs(OUTDIR, exist_ok=True)

with pdfplumber.open(SRC) as pdf:
    for pno in (6, 7):
        page = pdf.pages[pno]
        print("===== PAGE %d: %d images, %d words =====" % (pno + 1, len(page.images), len(page.extract_words())))
        for i, img in enumerate(page.images):
            print("  img %d: bbox=(%.0f,%.0f,%.0f,%.0f)" % (i, img["x0"], img["top"], img["x1"], img["bottom"]))
        # 渲染整页
        im = page.to_image(resolution=200)
        p = os.path.join(OUTDIR, "page%d.png" % (pno + 1))
        im.save(p)
        print("  saved:", p)
