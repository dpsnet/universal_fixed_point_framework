# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
for kw in ["104az-101", "104az-102", "层级规则"]:
    i = t.find(kw)
    print(f"--- {kw}: idx={i} ---")
    if i >= 0:
        print(t[max(0, i-200):i+900].replace("\n", " "))
        print()
