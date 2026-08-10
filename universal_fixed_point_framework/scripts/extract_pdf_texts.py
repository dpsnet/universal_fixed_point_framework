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
