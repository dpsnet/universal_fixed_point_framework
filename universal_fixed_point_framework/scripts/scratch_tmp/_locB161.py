# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P = r"E:\workspace\hyper-resolution\universal_fixed_point_framework\RESEARCH_STATE.md"
t = open(P, encoding="utf-8").read()
for kw in ["Δλ_min", "Δλ₃", "织³", "织a³", "729/1000", "√2·Δλ", "sqrt2", "Δλ₃ =", "F_np"]:
    i = t.find(kw)
    if i >= 0:
        print(f"--- {kw} @ {i} ---")
        print(t[max(0,i-120):i+220].replace("\n", " "))
        print()
