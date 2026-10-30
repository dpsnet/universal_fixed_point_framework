# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
p = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\notes\generative_chain_map.md"
t = open(p, encoding="utf-8").read()
for key in ('d_H', 'dH', '√7', '7+1/3'):
    i = t.find(key)
    while i >= 0:
        print(f"[{key} @{i}] ...{t[max(0,i-120):i+200]}...")
        print()
        i = t.find(key, i+1)
        if i > 40000: break
