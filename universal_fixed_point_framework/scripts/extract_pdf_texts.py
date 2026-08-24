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

# -*- coding: utf-8 -*-
"""提取 docs 下两个 PDF 的全文文本到 Temp，用于数据转录。"""
import os
import fitz  # pymupdf

docs_dir = r"e:\workspace\hyper-resolution\docs"
out_dir = r"e:\workspace\hyper-resolution\Temp"
os.makedirs(out_dir, exist_ok=True)

jobs = [
    ("塔里木盆地塔中Ⅲ区奥陶系多相态油气藏成因及富集模式.pdf", "tazhong3_full.txt"),
    ("j.sd.20261402.13.pdf", "mahu_fengcheng_full.txt"),
]

for pdf_name, out_name in jobs:
    path = os.path.join(docs_dir, pdf_name)
    doc = fitz.open(path)
    parts = []
    for i, page in enumerate(doc):
        parts.append(f"\n===== PAGE {i+1} =====\n")
        parts.append(page.get_text("text"))
    text = "".join(parts)
    out_path = os.path.join(out_dir, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"{pdf_name}: {doc.page_count} pages -> {out_path} ({len(text)} chars)")
    doc.close()
