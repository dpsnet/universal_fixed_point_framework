#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 pdfplumber 提取 feart-09-684592.pdf 全文文本，保存供检索。"""
import pdfplumber

SRC = r"C:\Users\dps_n\Downloads\feart-09-684592.pdf"
OUT = r"e:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\data\xu2021_pages\xu2021_fulltext.txt"

with pdfplumber.open(SRC) as pdf:
    print("pages:", len(pdf.pages))
    lines = []
    for i, page in enumerate(pdf.pages):
        t = page.extract_text() or ""
        lines.append("===== PAGE %d =====" % (i + 1))
        lines.append(t)
    txt = "\n".join(lines)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(txt)
    print("saved:", OUT, "chars:", len(txt))
