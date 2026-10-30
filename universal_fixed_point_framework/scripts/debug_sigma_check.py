# -*- coding: utf-8 -*-
"""详查 transform 误伤：列出原文件中含 σ⁷ / σ = 1/15 的上下文及替换后形态"""
import sys, re
sys.path.insert(0, r'E:\workspace\hyper-resolution\universal_fixed_point_framework\scripts')
from rename_sigma_score import transform

path = r'E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md'
with open(path, encoding='utf-8') as f:
    t = f.read()
nt, nA, nB, nC = transform(t)

print("=== σ⁷ 原上下文 → 替换后 ===")
for m in re.finditer(r'.{18}σ⁷.{10}', t):
    s = m.group(0)
    # 对应替换后
    idx = m.start()
    after = nt[max(0,idx-4):idx+len(s)+2]
    print(f"  原: ...{s}...")
    print(f"  后: ...{after}...")
    print()
print("=== σ = 1/15 原上下文 → 替换后 ===")
for m in re.finditer(r'.{12}σ = 1/15.{8}', t):
    s = m.group(0)
    idx = m.start()
    after = nt[max(0,idx-4):idx+len(s)+2]
    print(f"  原: ...{s}...")
    print(f"  后: ...{after}...")
    print()
print(f"替换统计：A={nA} B={nB} C={nC}")
