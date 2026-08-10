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
