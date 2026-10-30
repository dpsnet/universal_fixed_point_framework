# -*- coding: utf-8 -*-
"""提取 Schmidt 2005 表 1 完整内容（找 J1206 v 值）"""
import sys
try:
    import fitz  # pymupdf
    print('pymupdf OK', fitz.__doc__.split(chr(10))[0] if fitz.__doc__ else '')
except ImportError:
    print('NO pymupdf')
    sys.exit(1)

doc = fitz.open(r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts\_schmidt2005_full.pdf')
print('pages:', len(doc))
# 找表 1 所在页（高场星所在页）
for i, page in enumerate(doc):
    txt = page.get_text()
    if 'J234605' in txt or 'J120609' in txt or 'J100356' in txt:
        print('='*80)
        print('PAGE', i+1)
        print(txt)
        print('='*80)
