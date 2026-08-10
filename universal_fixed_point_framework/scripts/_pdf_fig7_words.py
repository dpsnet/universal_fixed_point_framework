#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提取 PDF 第 7、8 页的全部文字（含位置），定位图 7 轴刻度标签。"""
import pdfplumber

SRC = r"C:\Users\dps_n\Downloads\feart-09-684592.pdf"
with pdfplumber.open(SRC) as pdf:
    for pno in (6, 7):
        page = pdf.pages[pno]
        words = page.extract_words()
        print("===== PAGE %d: %d words =====" % (pno + 1, len(words)))
        # 只打印图形区域附近的词（x<595）
        for w in words:
            x0, top, x1, bottom = w["x0"], w["top"], w["x1"], w["bottom"]
            txt = w["text"]
            if txt.strip().isdigit() or txt.strip().replace(".", "").isdigit():
                print("  [%.0f,%.0f,%.0f,%.0f] %r" % (x0, top, x1, bottom, txt))
