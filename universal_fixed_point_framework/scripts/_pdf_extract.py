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
