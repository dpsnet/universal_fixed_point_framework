# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework"
rs = open(base + r"\RESEARCH_STATE.md", encoding="utf-8").read()
# 找所有含 d_H 的行段（前 60 字符上下文）
for m in re.finditer(r'd_H', rs):
    i = m.start()
    ctx = rs[max(0,i-80):i+120].replace('\n', ' ')
    print(f"@{i}: ...{ctx}...")
