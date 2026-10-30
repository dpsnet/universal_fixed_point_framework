# -*- coding: utf-8 -*-
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
base = r"E:\workspace\hyper-resolution\universal_fixed_point_framework"
rs = open(base + r"\RESEARCH_STATE.md", encoding="utf-8").read()
for pat in (r'σ/4', r'\(k_max\+1\)', r'2\.709', r'd_H 交叉', r'交叉验证候选'):
    print(f"##### pattern: {pat}")
    for m in re.finditer(pat, rs):
        i = m.start()
        ctx = rs[max(0,i-150):i+150].replace('\n', ' ')
        print(f"  @{i}: ...{ctx}...")
        print()
